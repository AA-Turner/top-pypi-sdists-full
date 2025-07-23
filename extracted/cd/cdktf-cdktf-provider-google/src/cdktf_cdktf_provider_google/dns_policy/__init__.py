r'''
# `google_dns_policy`

Refer to the Terraform Registry for docs: [`google_dns_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy).
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


class DnsPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsPolicy.DnsPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy google_dns_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        alternative_name_server_config: typing.Optional[typing.Union["DnsPolicyAlternativeNameServerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        dns64_config: typing.Optional[typing.Union["DnsPolicyDns64Config", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_inbound_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsPolicyNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DnsPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy google_dns_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: User assigned name for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#name DnsPolicy#name}
        :param alternative_name_server_config: alternative_name_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#alternative_name_server_config DnsPolicy#alternative_name_server_config}
        :param description: A textual description field. Defaults to 'Managed by Terraform'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#description DnsPolicy#description}
        :param dns64_config: dns64_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#dns64_config DnsPolicy#dns64_config}
        :param enable_inbound_forwarding: Allows networks bound to this policy to receive DNS queries sent by VMs or applications over VPN connections. When enabled, a virtual IP address will be allocated from each of the sub-networks that are bound to this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#enable_inbound_forwarding DnsPolicy#enable_inbound_forwarding}
        :param enable_logging: Controls whether logging is enabled for the networks bound to this policy. Defaults to no logging if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#enable_logging DnsPolicy#enable_logging}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#id DnsPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param networks: networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#networks DnsPolicy#networks}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#project DnsPolicy#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#timeouts DnsPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35715ffd4c0302d4a0918b35049ad30349ff32d6e133f52997bf14cca58ec363)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DnsPolicyConfig(
            name=name,
            alternative_name_server_config=alternative_name_server_config,
            description=description,
            dns64_config=dns64_config,
            enable_inbound_forwarding=enable_inbound_forwarding,
            enable_logging=enable_logging,
            id=id,
            networks=networks,
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
        '''Generates CDKTF code for importing a DnsPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DnsPolicy to import.
        :param import_from_id: The id of the existing DnsPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DnsPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c81136fc9e79837bfa4356d48d841b653d4d8cccd53db4ab48bb735501a6883)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAlternativeNameServerConfig")
    def put_alternative_name_server_config(
        self,
        *,
        target_name_servers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsPolicyAlternativeNameServerConfigTargetNameServers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param target_name_servers: target_name_servers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#target_name_servers DnsPolicy#target_name_servers}
        '''
        value = DnsPolicyAlternativeNameServerConfig(
            target_name_servers=target_name_servers
        )

        return typing.cast(None, jsii.invoke(self, "putAlternativeNameServerConfig", [value]))

    @jsii.member(jsii_name="putDns64Config")
    def put_dns64_config(
        self,
        *,
        scope: typing.Union["DnsPolicyDns64ConfigScope", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param scope: scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#scope DnsPolicy#scope}
        '''
        value = DnsPolicyDns64Config(scope=scope)

        return typing.cast(None, jsii.invoke(self, "putDns64Config", [value]))

    @jsii.member(jsii_name="putNetworks")
    def put_networks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsPolicyNetworks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67a80f2ecaca3b6215b3ec2ee5ca4ffc9066379b919a81be9b041e447c3a1ccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworks", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#create DnsPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#delete DnsPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#update DnsPolicy#update}.
        '''
        value = DnsPolicyTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAlternativeNameServerConfig")
    def reset_alternative_name_server_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlternativeNameServerConfig", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDns64Config")
    def reset_dns64_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDns64Config", []))

    @jsii.member(jsii_name="resetEnableInboundForwarding")
    def reset_enable_inbound_forwarding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableInboundForwarding", []))

    @jsii.member(jsii_name="resetEnableLogging")
    def reset_enable_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableLogging", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNetworks")
    def reset_networks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworks", []))

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
    @jsii.member(jsii_name="alternativeNameServerConfig")
    def alternative_name_server_config(
        self,
    ) -> "DnsPolicyAlternativeNameServerConfigOutputReference":
        return typing.cast("DnsPolicyAlternativeNameServerConfigOutputReference", jsii.get(self, "alternativeNameServerConfig"))

    @builtins.property
    @jsii.member(jsii_name="dns64Config")
    def dns64_config(self) -> "DnsPolicyDns64ConfigOutputReference":
        return typing.cast("DnsPolicyDns64ConfigOutputReference", jsii.get(self, "dns64Config"))

    @builtins.property
    @jsii.member(jsii_name="networks")
    def networks(self) -> "DnsPolicyNetworksList":
        return typing.cast("DnsPolicyNetworksList", jsii.get(self, "networks"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DnsPolicyTimeoutsOutputReference":
        return typing.cast("DnsPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="alternativeNameServerConfigInput")
    def alternative_name_server_config_input(
        self,
    ) -> typing.Optional["DnsPolicyAlternativeNameServerConfig"]:
        return typing.cast(typing.Optional["DnsPolicyAlternativeNameServerConfig"], jsii.get(self, "alternativeNameServerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dns64ConfigInput")
    def dns64_config_input(self) -> typing.Optional["DnsPolicyDns64Config"]:
        return typing.cast(typing.Optional["DnsPolicyDns64Config"], jsii.get(self, "dns64ConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enableInboundForwardingInput")
    def enable_inbound_forwarding_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInboundForwardingInput"))

    @builtins.property
    @jsii.member(jsii_name="enableLoggingInput")
    def enable_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networksInput")
    def networks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsPolicyNetworks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsPolicyNetworks"]]], jsii.get(self, "networksInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DnsPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DnsPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bb5f21bb66028b16ca07fff89ef82705b466f1ef6218b04d7b1abd8c0b0ddc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableInboundForwarding")
    def enable_inbound_forwarding(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableInboundForwarding"))

    @enable_inbound_forwarding.setter
    def enable_inbound_forwarding(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4629300fa928ee49a64d6fd3e9911df6da9fdd2ba9b60856749b79a3e7339fe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableInboundForwarding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableLogging")
    def enable_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableLogging"))

    @enable_logging.setter
    def enable_logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740f23949a9aa7b3fd391829ca14343ecbc3368c16075a3344877fdc45374c24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e183360e518b3bab3e8139b2a4927b9f6dada0378ab015c9d23ec05cd0c458e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9002849e0d689967918b7131bc65cfa5e55d926f19548f9285ad2a6588dc0082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f83d1cdc60c1a4b92d9caee096978c27436f1cea28c78d09bd45f893d142345a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsPolicy.DnsPolicyAlternativeNameServerConfig",
    jsii_struct_bases=[],
    name_mapping={"target_name_servers": "targetNameServers"},
)
class DnsPolicyAlternativeNameServerConfig:
    def __init__(
        self,
        *,
        target_name_servers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsPolicyAlternativeNameServerConfigTargetNameServers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param target_name_servers: target_name_servers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#target_name_servers DnsPolicy#target_name_servers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381bdc36d87f066d80c705b739e13bf691d35fb24fd455ffac3b854323771795)
            check_type(argname="argument target_name_servers", value=target_name_servers, expected_type=type_hints["target_name_servers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_name_servers": target_name_servers,
        }

    @builtins.property
    def target_name_servers(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsPolicyAlternativeNameServerConfigTargetNameServers"]]:
        '''target_name_servers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#target_name_servers DnsPolicy#target_name_servers}
        '''
        result = self._values.get("target_name_servers")
        assert result is not None, "Required property 'target_name_servers' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsPolicyAlternativeNameServerConfigTargetNameServers"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsPolicyAlternativeNameServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsPolicyAlternativeNameServerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsPolicy.DnsPolicyAlternativeNameServerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37210319299686a76ebe529ace7cb9143a03da614240e1320615b3a12c8e4458)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTargetNameServers")
    def put_target_name_servers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsPolicyAlternativeNameServerConfigTargetNameServers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efbb3488e57bc25c26e10e54da77695d1eec4b0c65f8fac5952b6c64f8389252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargetNameServers", [value]))

    @builtins.property
    @jsii.member(jsii_name="targetNameServers")
    def target_name_servers(
        self,
    ) -> "DnsPolicyAlternativeNameServerConfigTargetNameServersList":
        return typing.cast("DnsPolicyAlternativeNameServerConfigTargetNameServersList", jsii.get(self, "targetNameServers"))

    @builtins.property
    @jsii.member(jsii_name="targetNameServersInput")
    def target_name_servers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsPolicyAlternativeNameServerConfigTargetNameServers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsPolicyAlternativeNameServerConfigTargetNameServers"]]], jsii.get(self, "targetNameServersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DnsPolicyAlternativeNameServerConfig]:
        return typing.cast(typing.Optional[DnsPolicyAlternativeNameServerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DnsPolicyAlternativeNameServerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b2ce1d242b9c049642395eedaa221524fb20036c914ebf2ce74bb6c5adee65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsPolicy.DnsPolicyAlternativeNameServerConfigTargetNameServers",
    jsii_struct_bases=[],
    name_mapping={"ipv4_address": "ipv4Address", "forwarding_path": "forwardingPath"},
)
class DnsPolicyAlternativeNameServerConfigTargetNameServers:
    def __init__(
        self,
        *,
        ipv4_address: builtins.str,
        forwarding_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ipv4_address: IPv4 address to forward to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#ipv4_address DnsPolicy#ipv4_address}
        :param forwarding_path: Forwarding path for this TargetNameServer. If unset or 'default' Cloud DNS will make forwarding decision based on address ranges, i.e. RFC1918 addresses go to the VPC, Non-RFC1918 addresses go to the Internet. When set to 'private', Cloud DNS will always send queries through VPC for this target Possible values: ["default", "private"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#forwarding_path DnsPolicy#forwarding_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a7e8c99efbd05bf95e1910ed84ec83563af85be48357268a0016558fd74331e)
            check_type(argname="argument ipv4_address", value=ipv4_address, expected_type=type_hints["ipv4_address"])
            check_type(argname="argument forwarding_path", value=forwarding_path, expected_type=type_hints["forwarding_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ipv4_address": ipv4_address,
        }
        if forwarding_path is not None:
            self._values["forwarding_path"] = forwarding_path

    @builtins.property
    def ipv4_address(self) -> builtins.str:
        '''IPv4 address to forward to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#ipv4_address DnsPolicy#ipv4_address}
        '''
        result = self._values.get("ipv4_address")
        assert result is not None, "Required property 'ipv4_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def forwarding_path(self) -> typing.Optional[builtins.str]:
        '''Forwarding path for this TargetNameServer.

        If unset or 'default' Cloud DNS will make forwarding
        decision based on address ranges, i.e. RFC1918 addresses go to the VPC, Non-RFC1918 addresses go
        to the Internet. When set to 'private', Cloud DNS will always send queries through VPC for this target Possible values: ["default", "private"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#forwarding_path DnsPolicy#forwarding_path}
        '''
        result = self._values.get("forwarding_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsPolicyAlternativeNameServerConfigTargetNameServers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsPolicyAlternativeNameServerConfigTargetNameServersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsPolicy.DnsPolicyAlternativeNameServerConfigTargetNameServersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef87c1bf2fc126f15a8e78bb8cb19df2aedb8a3c5818f5444cdd268de83ede05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DnsPolicyAlternativeNameServerConfigTargetNameServersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333fd642ea2d836c3f4d019e7587111f384d827a67795abb429731e5b8effc08)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsPolicyAlternativeNameServerConfigTargetNameServersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__865cab259d334fe99301e416d568d287b2b64208b5d218a1cf78ce3ee7984780)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bda4e1a69e346afadb9a051626c6e3f6d5cc831eca51a89fe1bc158b5b975e12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd403b0722f866842e307b4d4a9fb2da3c04a83c0ecf052568bca6b917ae92b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsPolicyAlternativeNameServerConfigTargetNameServers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsPolicyAlternativeNameServerConfigTargetNameServers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsPolicyAlternativeNameServerConfigTargetNameServers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afdd56f449782982bfed8a596028f987b7375ca45825aa505b4b2c7d53e99e00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsPolicyAlternativeNameServerConfigTargetNameServersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsPolicy.DnsPolicyAlternativeNameServerConfigTargetNameServersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41487cda0949315b0ba8c19c92c23cf52231a42af2047449ca71c437fa99cecc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetForwardingPath")
    def reset_forwarding_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardingPath", []))

    @builtins.property
    @jsii.member(jsii_name="forwardingPathInput")
    def forwarding_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forwardingPathInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv4AddressInput")
    def ipv4_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv4AddressInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardingPath")
    def forwarding_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardingPath"))

    @forwarding_path.setter
    def forwarding_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ca02563a0fe6d80884974a43824bf50e4db1c5b3cbff13a7cef355e6f43abde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardingPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv4Address")
    def ipv4_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4Address"))

    @ipv4_address.setter
    def ipv4_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b1f8f4344461d14590ed64e4ec8b6edd746981c35ccbe855a56e61a3c7cf97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4Address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsPolicyAlternativeNameServerConfigTargetNameServers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsPolicyAlternativeNameServerConfigTargetNameServers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsPolicyAlternativeNameServerConfigTargetNameServers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4d8da4160aca4dc20d3c6791e03e03106b8558c4339c645d77a4a8f891f921f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsPolicy.DnsPolicyConfig",
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
        "alternative_name_server_config": "alternativeNameServerConfig",
        "description": "description",
        "dns64_config": "dns64Config",
        "enable_inbound_forwarding": "enableInboundForwarding",
        "enable_logging": "enableLogging",
        "id": "id",
        "networks": "networks",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class DnsPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        alternative_name_server_config: typing.Optional[typing.Union[DnsPolicyAlternativeNameServerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        dns64_config: typing.Optional[typing.Union["DnsPolicyDns64Config", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_inbound_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsPolicyNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DnsPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: User assigned name for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#name DnsPolicy#name}
        :param alternative_name_server_config: alternative_name_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#alternative_name_server_config DnsPolicy#alternative_name_server_config}
        :param description: A textual description field. Defaults to 'Managed by Terraform'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#description DnsPolicy#description}
        :param dns64_config: dns64_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#dns64_config DnsPolicy#dns64_config}
        :param enable_inbound_forwarding: Allows networks bound to this policy to receive DNS queries sent by VMs or applications over VPN connections. When enabled, a virtual IP address will be allocated from each of the sub-networks that are bound to this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#enable_inbound_forwarding DnsPolicy#enable_inbound_forwarding}
        :param enable_logging: Controls whether logging is enabled for the networks bound to this policy. Defaults to no logging if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#enable_logging DnsPolicy#enable_logging}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#id DnsPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param networks: networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#networks DnsPolicy#networks}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#project DnsPolicy#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#timeouts DnsPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(alternative_name_server_config, dict):
            alternative_name_server_config = DnsPolicyAlternativeNameServerConfig(**alternative_name_server_config)
        if isinstance(dns64_config, dict):
            dns64_config = DnsPolicyDns64Config(**dns64_config)
        if isinstance(timeouts, dict):
            timeouts = DnsPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29fd4fb5965fce1a13be73ca4bf300c71f705245ff3e38bf89f9bb2ce96549d7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument alternative_name_server_config", value=alternative_name_server_config, expected_type=type_hints["alternative_name_server_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dns64_config", value=dns64_config, expected_type=type_hints["dns64_config"])
            check_type(argname="argument enable_inbound_forwarding", value=enable_inbound_forwarding, expected_type=type_hints["enable_inbound_forwarding"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument networks", value=networks, expected_type=type_hints["networks"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
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
        if alternative_name_server_config is not None:
            self._values["alternative_name_server_config"] = alternative_name_server_config
        if description is not None:
            self._values["description"] = description
        if dns64_config is not None:
            self._values["dns64_config"] = dns64_config
        if enable_inbound_forwarding is not None:
            self._values["enable_inbound_forwarding"] = enable_inbound_forwarding
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if id is not None:
            self._values["id"] = id
        if networks is not None:
            self._values["networks"] = networks
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
    def name(self) -> builtins.str:
        '''User assigned name for this policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#name DnsPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alternative_name_server_config(
        self,
    ) -> typing.Optional[DnsPolicyAlternativeNameServerConfig]:
        '''alternative_name_server_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#alternative_name_server_config DnsPolicy#alternative_name_server_config}
        '''
        result = self._values.get("alternative_name_server_config")
        return typing.cast(typing.Optional[DnsPolicyAlternativeNameServerConfig], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A textual description field. Defaults to 'Managed by Terraform'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#description DnsPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns64_config(self) -> typing.Optional["DnsPolicyDns64Config"]:
        '''dns64_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#dns64_config DnsPolicy#dns64_config}
        '''
        result = self._values.get("dns64_config")
        return typing.cast(typing.Optional["DnsPolicyDns64Config"], result)

    @builtins.property
    def enable_inbound_forwarding(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows networks bound to this policy to receive DNS queries sent by VMs or applications over VPN connections.

        When enabled, a
        virtual IP address will be allocated from each of the sub-networks
        that are bound to this policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#enable_inbound_forwarding DnsPolicy#enable_inbound_forwarding}
        '''
        result = self._values.get("enable_inbound_forwarding")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Controls whether logging is enabled for the networks bound to this policy. Defaults to no logging if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#enable_logging DnsPolicy#enable_logging}
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#id DnsPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def networks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsPolicyNetworks"]]]:
        '''networks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#networks DnsPolicy#networks}
        '''
        result = self._values.get("networks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsPolicyNetworks"]]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#project DnsPolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DnsPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#timeouts DnsPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DnsPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsPolicy.DnsPolicyDns64Config",
    jsii_struct_bases=[],
    name_mapping={"scope": "scope"},
)
class DnsPolicyDns64Config:
    def __init__(
        self,
        *,
        scope: typing.Union["DnsPolicyDns64ConfigScope", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param scope: scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#scope DnsPolicy#scope}
        '''
        if isinstance(scope, dict):
            scope = DnsPolicyDns64ConfigScope(**scope)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33816e33b794897575ea255987077ffd2b08b2378caf53805f426d2cb406729b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scope": scope,
        }

    @builtins.property
    def scope(self) -> "DnsPolicyDns64ConfigScope":
        '''scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#scope DnsPolicy#scope}
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast("DnsPolicyDns64ConfigScope", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsPolicyDns64Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsPolicyDns64ConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsPolicy.DnsPolicyDns64ConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a699175f34785c2a049435e025a461757bd9f8276f2e19e809a9353dde9b543)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScope")
    def put_scope(
        self,
        *,
        all_queries: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param all_queries: Controls whether DNS64 is enabled globally at the network level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#all_queries DnsPolicy#all_queries}
        '''
        value = DnsPolicyDns64ConfigScope(all_queries=all_queries)

        return typing.cast(None, jsii.invoke(self, "putScope", [value]))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> "DnsPolicyDns64ConfigScopeOutputReference":
        return typing.cast("DnsPolicyDns64ConfigScopeOutputReference", jsii.get(self, "scope"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional["DnsPolicyDns64ConfigScope"]:
        return typing.cast(typing.Optional["DnsPolicyDns64ConfigScope"], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DnsPolicyDns64Config]:
        return typing.cast(typing.Optional[DnsPolicyDns64Config], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DnsPolicyDns64Config]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5967f2c8c67285c8127f8d016ca06d83bd1311b7cccca6ab8e08e4bfe8b97723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsPolicy.DnsPolicyDns64ConfigScope",
    jsii_struct_bases=[],
    name_mapping={"all_queries": "allQueries"},
)
class DnsPolicyDns64ConfigScope:
    def __init__(
        self,
        *,
        all_queries: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param all_queries: Controls whether DNS64 is enabled globally at the network level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#all_queries DnsPolicy#all_queries}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b4fa60c38bfdab8af67ad77ced9a8964c6ea65b98f92a928fd9edf3b231bc0)
            check_type(argname="argument all_queries", value=all_queries, expected_type=type_hints["all_queries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all_queries is not None:
            self._values["all_queries"] = all_queries

    @builtins.property
    def all_queries(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Controls whether DNS64 is enabled globally at the network level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#all_queries DnsPolicy#all_queries}
        '''
        result = self._values.get("all_queries")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsPolicyDns64ConfigScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsPolicyDns64ConfigScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsPolicy.DnsPolicyDns64ConfigScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__864435476cb9bc38de0a931fff2d3218773146f30b07f8dbda9fb4266af79de4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllQueries")
    def reset_all_queries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllQueries", []))

    @builtins.property
    @jsii.member(jsii_name="allQueriesInput")
    def all_queries_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allQueriesInput"))

    @builtins.property
    @jsii.member(jsii_name="allQueries")
    def all_queries(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allQueries"))

    @all_queries.setter
    def all_queries(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af8639bec427ac2cd55979df0cb3ca02bce6ac25a9eb0d1e4d056f4cc1e4b43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allQueries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DnsPolicyDns64ConfigScope]:
        return typing.cast(typing.Optional[DnsPolicyDns64ConfigScope], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DnsPolicyDns64ConfigScope]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fcd613983af68330961f4b47f143cb6fcadba7d6dfed111a97f53979db4b065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsPolicy.DnsPolicyNetworks",
    jsii_struct_bases=[],
    name_mapping={"network_url": "networkUrl"},
)
class DnsPolicyNetworks:
    def __init__(self, *, network_url: builtins.str) -> None:
        '''
        :param network_url: The id or fully qualified URL of the VPC network to forward queries to. This should be formatted like 'projects/{project}/global/networks/{network}' or 'https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#network_url DnsPolicy#network_url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02b6b414542d321a165ea8e1af92a62a9321d2312169f045e85e8b3f93f66646)
            check_type(argname="argument network_url", value=network_url, expected_type=type_hints["network_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_url": network_url,
        }

    @builtins.property
    def network_url(self) -> builtins.str:
        '''The id or fully qualified URL of the VPC network to forward queries to.

        This should be formatted like 'projects/{project}/global/networks/{network}' or
        'https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#network_url DnsPolicy#network_url}
        '''
        result = self._values.get("network_url")
        assert result is not None, "Required property 'network_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsPolicyNetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsPolicyNetworksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsPolicy.DnsPolicyNetworksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b449609b0741d21e599d29679aa1123841046b0c42c9d3c1670829b179c2bd3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DnsPolicyNetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3960f646bc5afa3553679a5ee4227c7e616559e4ad930b0cffd35cb86bfb9782)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsPolicyNetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45468d73d3305a2f6f3eeb116fb82e4a5e160c826623b742e98f78fb91d15753)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb9a21b4eb29a9d85839f272df11883c20833b32c256254b8d2ab337b351eb20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a66d3e64a019f84639ddd3653bd01e3cc4b1a29bed7c6d8e8955990666d70375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsPolicyNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsPolicyNetworks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsPolicyNetworks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961827c98b1f659e8c8134b385f24f1a8a33ae49189e8be2f0e3e3dd1f24268b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsPolicyNetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsPolicy.DnsPolicyNetworksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9536350058463efb1569fba5b13669f83f0b8d2d1fd628fd4cc1a72ffc3472ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="networkUrlInput")
    def network_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="networkUrl")
    def network_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUrl"))

    @network_url.setter
    def network_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__699fe80c1acba60ba668d5adef7abd00eedb1f561c188b3edaafcb2c69aee3d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsPolicyNetworks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsPolicyNetworks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsPolicyNetworks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5925bd79492ca2eb3d0796f0e7a105a6687c48357960ff2dab1ca46f51fd1da0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsPolicy.DnsPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DnsPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#create DnsPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#delete DnsPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#update DnsPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53db72875237dda35e7d9296267259c0215df5886a5126767cd2fb273685dbbb)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#create DnsPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#delete DnsPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_policy#update DnsPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsPolicy.DnsPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e481adba2ed783b56eea19ad101fb166b1059dc63847931df4f30c80032f0f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0739ad092e0997c75feab9725b3876f4203dca13abf6521d79073c3b774dbfce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d1ef6239151dbbc0d3adf63dad37d819a7dd7fdf05fcbd748934b5708334f2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5ad877b88a469c9915c236186285494cfa69175321b161d65925233091df40b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c4e6b99538ee3d3749e24b1fe88a967c2552eaaab77f25ebb1198e596da9997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DnsPolicy",
    "DnsPolicyAlternativeNameServerConfig",
    "DnsPolicyAlternativeNameServerConfigOutputReference",
    "DnsPolicyAlternativeNameServerConfigTargetNameServers",
    "DnsPolicyAlternativeNameServerConfigTargetNameServersList",
    "DnsPolicyAlternativeNameServerConfigTargetNameServersOutputReference",
    "DnsPolicyConfig",
    "DnsPolicyDns64Config",
    "DnsPolicyDns64ConfigOutputReference",
    "DnsPolicyDns64ConfigScope",
    "DnsPolicyDns64ConfigScopeOutputReference",
    "DnsPolicyNetworks",
    "DnsPolicyNetworksList",
    "DnsPolicyNetworksOutputReference",
    "DnsPolicyTimeouts",
    "DnsPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__35715ffd4c0302d4a0918b35049ad30349ff32d6e133f52997bf14cca58ec363(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    alternative_name_server_config: typing.Optional[typing.Union[DnsPolicyAlternativeNameServerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    dns64_config: typing.Optional[typing.Union[DnsPolicyDns64Config, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_inbound_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsPolicyNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DnsPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5c81136fc9e79837bfa4356d48d841b653d4d8cccd53db4ab48bb735501a6883(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a80f2ecaca3b6215b3ec2ee5ca4ffc9066379b919a81be9b041e447c3a1ccd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsPolicyNetworks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb5f21bb66028b16ca07fff89ef82705b466f1ef6218b04d7b1abd8c0b0ddc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4629300fa928ee49a64d6fd3e9911df6da9fdd2ba9b60856749b79a3e7339fe5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740f23949a9aa7b3fd391829ca14343ecbc3368c16075a3344877fdc45374c24(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e183360e518b3bab3e8139b2a4927b9f6dada0378ab015c9d23ec05cd0c458e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9002849e0d689967918b7131bc65cfa5e55d926f19548f9285ad2a6588dc0082(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83d1cdc60c1a4b92d9caee096978c27436f1cea28c78d09bd45f893d142345a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381bdc36d87f066d80c705b739e13bf691d35fb24fd455ffac3b854323771795(
    *,
    target_name_servers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsPolicyAlternativeNameServerConfigTargetNameServers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37210319299686a76ebe529ace7cb9143a03da614240e1320615b3a12c8e4458(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efbb3488e57bc25c26e10e54da77695d1eec4b0c65f8fac5952b6c64f8389252(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsPolicyAlternativeNameServerConfigTargetNameServers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b2ce1d242b9c049642395eedaa221524fb20036c914ebf2ce74bb6c5adee65(
    value: typing.Optional[DnsPolicyAlternativeNameServerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7e8c99efbd05bf95e1910ed84ec83563af85be48357268a0016558fd74331e(
    *,
    ipv4_address: builtins.str,
    forwarding_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef87c1bf2fc126f15a8e78bb8cb19df2aedb8a3c5818f5444cdd268de83ede05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333fd642ea2d836c3f4d019e7587111f384d827a67795abb429731e5b8effc08(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865cab259d334fe99301e416d568d287b2b64208b5d218a1cf78ce3ee7984780(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda4e1a69e346afadb9a051626c6e3f6d5cc831eca51a89fe1bc158b5b975e12(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd403b0722f866842e307b4d4a9fb2da3c04a83c0ecf052568bca6b917ae92b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afdd56f449782982bfed8a596028f987b7375ca45825aa505b4b2c7d53e99e00(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsPolicyAlternativeNameServerConfigTargetNameServers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41487cda0949315b0ba8c19c92c23cf52231a42af2047449ca71c437fa99cecc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca02563a0fe6d80884974a43824bf50e4db1c5b3cbff13a7cef355e6f43abde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b1f8f4344461d14590ed64e4ec8b6edd746981c35ccbe855a56e61a3c7cf97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d8da4160aca4dc20d3c6791e03e03106b8558c4339c645d77a4a8f891f921f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsPolicyAlternativeNameServerConfigTargetNameServers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29fd4fb5965fce1a13be73ca4bf300c71f705245ff3e38bf89f9bb2ce96549d7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    alternative_name_server_config: typing.Optional[typing.Union[DnsPolicyAlternativeNameServerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    dns64_config: typing.Optional[typing.Union[DnsPolicyDns64Config, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_inbound_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsPolicyNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DnsPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33816e33b794897575ea255987077ffd2b08b2378caf53805f426d2cb406729b(
    *,
    scope: typing.Union[DnsPolicyDns64ConfigScope, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a699175f34785c2a049435e025a461757bd9f8276f2e19e809a9353dde9b543(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5967f2c8c67285c8127f8d016ca06d83bd1311b7cccca6ab8e08e4bfe8b97723(
    value: typing.Optional[DnsPolicyDns64Config],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b4fa60c38bfdab8af67ad77ced9a8964c6ea65b98f92a928fd9edf3b231bc0(
    *,
    all_queries: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864435476cb9bc38de0a931fff2d3218773146f30b07f8dbda9fb4266af79de4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af8639bec427ac2cd55979df0cb3ca02bce6ac25a9eb0d1e4d056f4cc1e4b43(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fcd613983af68330961f4b47f143cb6fcadba7d6dfed111a97f53979db4b065(
    value: typing.Optional[DnsPolicyDns64ConfigScope],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b6b414542d321a165ea8e1af92a62a9321d2312169f045e85e8b3f93f66646(
    *,
    network_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b449609b0741d21e599d29679aa1123841046b0c42c9d3c1670829b179c2bd3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3960f646bc5afa3553679a5ee4227c7e616559e4ad930b0cffd35cb86bfb9782(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45468d73d3305a2f6f3eeb116fb82e4a5e160c826623b742e98f78fb91d15753(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9a21b4eb29a9d85839f272df11883c20833b32c256254b8d2ab337b351eb20(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66d3e64a019f84639ddd3653bd01e3cc4b1a29bed7c6d8e8955990666d70375(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961827c98b1f659e8c8134b385f24f1a8a33ae49189e8be2f0e3e3dd1f24268b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsPolicyNetworks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9536350058463efb1569fba5b13669f83f0b8d2d1fd628fd4cc1a72ffc3472ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699fe80c1acba60ba668d5adef7abd00eedb1f561c188b3edaafcb2c69aee3d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5925bd79492ca2eb3d0796f0e7a105a6687c48357960ff2dab1ca46f51fd1da0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsPolicyNetworks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53db72875237dda35e7d9296267259c0215df5886a5126767cd2fb273685dbbb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e481adba2ed783b56eea19ad101fb166b1059dc63847931df4f30c80032f0f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0739ad092e0997c75feab9725b3876f4203dca13abf6521d79073c3b774dbfce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d1ef6239151dbbc0d3adf63dad37d819a7dd7fdf05fcbd748934b5708334f2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ad877b88a469c9915c236186285494cfa69175321b161d65925233091df40b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4e6b99538ee3d3749e24b1fe88a967c2552eaaab77f25ebb1198e596da9997(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

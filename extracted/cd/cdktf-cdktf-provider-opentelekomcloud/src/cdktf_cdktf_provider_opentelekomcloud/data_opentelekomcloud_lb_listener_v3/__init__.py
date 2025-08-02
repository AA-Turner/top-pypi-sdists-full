r'''
# `data_opentelekomcloud_lb_listener_v3`

Refer to the Terraform Registry for docs: [`data_opentelekomcloud_lb_listener_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3).
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


class DataOpentelekomcloudLbListenerV3(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbListenerV3.DataOpentelekomcloudLbListenerV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3 opentelekomcloud_lb_listener_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        client_ca_tls_container_ref: typing.Optional[builtins.str] = None,
        client_timeout: typing.Optional[jsii.Number] = None,
        default_pool_id: typing.Optional[builtins.str] = None,
        default_tls_container_ref: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        keep_alive_timeout: typing.Optional[jsii.Number] = None,
        loadbalancer_id: typing.Optional[builtins.str] = None,
        member_address: typing.Optional[builtins.str] = None,
        member_device_id: typing.Optional[builtins.str] = None,
        member_timeout: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        protocol_port: typing.Optional[jsii.Number] = None,
        tls_ciphers_policy: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3 opentelekomcloud_lb_listener_v3} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param client_ca_tls_container_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#client_ca_tls_container_ref DataOpentelekomcloudLbListenerV3#client_ca_tls_container_ref}.
        :param client_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#client_timeout DataOpentelekomcloudLbListenerV3#client_timeout}.
        :param default_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#default_pool_id DataOpentelekomcloudLbListenerV3#default_pool_id}.
        :param default_tls_container_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#default_tls_container_ref DataOpentelekomcloudLbListenerV3#default_tls_container_ref}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#description DataOpentelekomcloudLbListenerV3#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#id DataOpentelekomcloudLbListenerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param keep_alive_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#keep_alive_timeout DataOpentelekomcloudLbListenerV3#keep_alive_timeout}.
        :param loadbalancer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#loadbalancer_id DataOpentelekomcloudLbListenerV3#loadbalancer_id}.
        :param member_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#member_address DataOpentelekomcloudLbListenerV3#member_address}.
        :param member_device_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#member_device_id DataOpentelekomcloudLbListenerV3#member_device_id}.
        :param member_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#member_timeout DataOpentelekomcloudLbListenerV3#member_timeout}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#name DataOpentelekomcloudLbListenerV3#name}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#protocol DataOpentelekomcloudLbListenerV3#protocol}.
        :param protocol_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#protocol_port DataOpentelekomcloudLbListenerV3#protocol_port}.
        :param tls_ciphers_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#tls_ciphers_policy DataOpentelekomcloudLbListenerV3#tls_ciphers_policy}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad224bce286b6c616c1c642a2844fd7895b20b30b3c8daabeef99839f860ad91)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpentelekomcloudLbListenerV3Config(
            client_ca_tls_container_ref=client_ca_tls_container_ref,
            client_timeout=client_timeout,
            default_pool_id=default_pool_id,
            default_tls_container_ref=default_tls_container_ref,
            description=description,
            id=id,
            keep_alive_timeout=keep_alive_timeout,
            loadbalancer_id=loadbalancer_id,
            member_address=member_address,
            member_device_id=member_device_id,
            member_timeout=member_timeout,
            name=name,
            protocol=protocol,
            protocol_port=protocol_port,
            tls_ciphers_policy=tls_ciphers_policy,
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
        '''Generates CDKTF code for importing a DataOpentelekomcloudLbListenerV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpentelekomcloudLbListenerV3 to import.
        :param import_from_id: The id of the existing DataOpentelekomcloudLbListenerV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpentelekomcloudLbListenerV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86e64062066d55e72ae86d19e7f6569de5f0389b3a541627d4c41fcaf5b6cd99)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetClientCaTlsContainerRef")
    def reset_client_ca_tls_container_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCaTlsContainerRef", []))

    @jsii.member(jsii_name="resetClientTimeout")
    def reset_client_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientTimeout", []))

    @jsii.member(jsii_name="resetDefaultPoolId")
    def reset_default_pool_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPoolId", []))

    @jsii.member(jsii_name="resetDefaultTlsContainerRef")
    def reset_default_tls_container_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTlsContainerRef", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKeepAliveTimeout")
    def reset_keep_alive_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepAliveTimeout", []))

    @jsii.member(jsii_name="resetLoadbalancerId")
    def reset_loadbalancer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadbalancerId", []))

    @jsii.member(jsii_name="resetMemberAddress")
    def reset_member_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemberAddress", []))

    @jsii.member(jsii_name="resetMemberDeviceId")
    def reset_member_device_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemberDeviceId", []))

    @jsii.member(jsii_name="resetMemberTimeout")
    def reset_member_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemberTimeout", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetProtocolPort")
    def reset_protocol_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocolPort", []))

    @jsii.member(jsii_name="resetTlsCiphersPolicy")
    def reset_tls_ciphers_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsCiphersPolicy", []))

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
    @jsii.member(jsii_name="adminStateUp")
    def admin_state_up(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "adminStateUp"))

    @builtins.property
    @jsii.member(jsii_name="advancedForwarding")
    def advanced_forwarding(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "advancedForwarding"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="http2Enable")
    def http2_enable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "http2Enable"))

    @builtins.property
    @jsii.member(jsii_name="insertHeaders")
    def insert_headers(self) -> "DataOpentelekomcloudLbListenerV3InsertHeadersList":
        return typing.cast("DataOpentelekomcloudLbListenerV3InsertHeadersList", jsii.get(self, "insertHeaders"))

    @builtins.property
    @jsii.member(jsii_name="ipGroup")
    def ip_group(self) -> "DataOpentelekomcloudLbListenerV3IpGroupList":
        return typing.cast("DataOpentelekomcloudLbListenerV3IpGroupList", jsii.get(self, "ipGroup"))

    @builtins.property
    @jsii.member(jsii_name="memberRetryEnable")
    def member_retry_enable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "memberRetryEnable"))

    @builtins.property
    @jsii.member(jsii_name="memoryRetryEnable")
    def memory_retry_enable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "memoryRetryEnable"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="securityPolicyId")
    def security_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityPolicyId"))

    @builtins.property
    @jsii.member(jsii_name="sniContainerRefs")
    def sni_container_refs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sniContainerRefs"))

    @builtins.property
    @jsii.member(jsii_name="sniMatchAlgo")
    def sni_match_algo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sniMatchAlgo"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="clientCaTlsContainerRefInput")
    def client_ca_tls_container_ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCaTlsContainerRefInput"))

    @builtins.property
    @jsii.member(jsii_name="clientTimeoutInput")
    def client_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "clientTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPoolIdInput")
    def default_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTlsContainerRefInput")
    def default_tls_container_ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTlsContainerRefInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keepAliveTimeoutInput")
    def keep_alive_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepAliveTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="loadbalancerIdInput")
    def loadbalancer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadbalancerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="memberAddressInput")
    def member_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memberAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="memberDeviceIdInput")
    def member_device_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memberDeviceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="memberTimeoutInput")
    def member_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memberTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolPortInput")
    def protocol_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "protocolPortInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsCiphersPolicyInput")
    def tls_ciphers_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsCiphersPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCaTlsContainerRef")
    def client_ca_tls_container_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCaTlsContainerRef"))

    @client_ca_tls_container_ref.setter
    def client_ca_tls_container_ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08d7d3f340acece115d31a6a89269f522a9685ff737e7c75b9e60f50e8fe6b99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCaTlsContainerRef", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientTimeout")
    def client_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientTimeout"))

    @client_timeout.setter
    def client_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc2fa3679c9532dfacf9303af4bca33832530a395960d635e8091b36ee56745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultPoolId")
    def default_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultPoolId"))

    @default_pool_id.setter
    def default_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__182d7994f4f7cb32dc77cb14c6ad8eb2d78b48dd23bad9c61cb70dbb1bb26cfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTlsContainerRef")
    def default_tls_container_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultTlsContainerRef"))

    @default_tls_container_ref.setter
    def default_tls_container_ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__093ed7e809dc87a67446d05706a4fc49a08d34e55eae4f289217095aeee76726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTlsContainerRef", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dcc299a9a104778c0ad7fa7554a7b68b86bc198c781635cf758162b4b850a88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d9927754f0dc2add712a071e557717bff3d4b558be27a863eabb651c334bbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keepAliveTimeout")
    def keep_alive_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepAliveTimeout"))

    @keep_alive_timeout.setter
    def keep_alive_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b0074a855ba11e0a4050309688c25a5b5565af4d6865ab3f848ec1e1982dec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepAliveTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadbalancerId")
    def loadbalancer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadbalancerId"))

    @loadbalancer_id.setter
    def loadbalancer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__086f3f2a72366fc6dce5b3500ed15302205dd01733ad7b998ae19bd07586fe78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadbalancerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memberAddress")
    def member_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memberAddress"))

    @member_address.setter
    def member_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b8e60e9cdf0c8c25a48c5cd9b0cacd0e1cd5f76399980a7eaf490d12e75331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memberDeviceId")
    def member_device_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memberDeviceId"))

    @member_device_id.setter
    def member_device_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__197bf9c50b775bd80fed4dc0bfae2c80f45387769cd1db74fa2ff4a1fc2cc3de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberDeviceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memberTimeout")
    def member_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memberTimeout"))

    @member_timeout.setter
    def member_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__580b83a812aa15d7e93bb8a69206dd066e21473b96b0f2b29a1001180e0d3968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b121a48dcae39cb17930f652da3546fc43cb1fbaa0fccde0e72e71da97d524)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9278cfdc6b9fd6203bdc16eb3debf3457c28f1b2a87135eaf2b9da003d6f519)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocolPort")
    def protocol_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "protocolPort"))

    @protocol_port.setter
    def protocol_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dff95f23b9ff589bb76d80d80ff613b94022581ca278a5756be3be2a122e26c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsCiphersPolicy")
    def tls_ciphers_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsCiphersPolicy"))

    @tls_ciphers_policy.setter
    def tls_ciphers_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077f5215fa977efbb08a025d41a301d95d9698936dc4d89a45e08b6b710b6720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsCiphersPolicy", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbListenerV3.DataOpentelekomcloudLbListenerV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "client_ca_tls_container_ref": "clientCaTlsContainerRef",
        "client_timeout": "clientTimeout",
        "default_pool_id": "defaultPoolId",
        "default_tls_container_ref": "defaultTlsContainerRef",
        "description": "description",
        "id": "id",
        "keep_alive_timeout": "keepAliveTimeout",
        "loadbalancer_id": "loadbalancerId",
        "member_address": "memberAddress",
        "member_device_id": "memberDeviceId",
        "member_timeout": "memberTimeout",
        "name": "name",
        "protocol": "protocol",
        "protocol_port": "protocolPort",
        "tls_ciphers_policy": "tlsCiphersPolicy",
    },
)
class DataOpentelekomcloudLbListenerV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        client_ca_tls_container_ref: typing.Optional[builtins.str] = None,
        client_timeout: typing.Optional[jsii.Number] = None,
        default_pool_id: typing.Optional[builtins.str] = None,
        default_tls_container_ref: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        keep_alive_timeout: typing.Optional[jsii.Number] = None,
        loadbalancer_id: typing.Optional[builtins.str] = None,
        member_address: typing.Optional[builtins.str] = None,
        member_device_id: typing.Optional[builtins.str] = None,
        member_timeout: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        protocol_port: typing.Optional[jsii.Number] = None,
        tls_ciphers_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param client_ca_tls_container_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#client_ca_tls_container_ref DataOpentelekomcloudLbListenerV3#client_ca_tls_container_ref}.
        :param client_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#client_timeout DataOpentelekomcloudLbListenerV3#client_timeout}.
        :param default_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#default_pool_id DataOpentelekomcloudLbListenerV3#default_pool_id}.
        :param default_tls_container_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#default_tls_container_ref DataOpentelekomcloudLbListenerV3#default_tls_container_ref}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#description DataOpentelekomcloudLbListenerV3#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#id DataOpentelekomcloudLbListenerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param keep_alive_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#keep_alive_timeout DataOpentelekomcloudLbListenerV3#keep_alive_timeout}.
        :param loadbalancer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#loadbalancer_id DataOpentelekomcloudLbListenerV3#loadbalancer_id}.
        :param member_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#member_address DataOpentelekomcloudLbListenerV3#member_address}.
        :param member_device_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#member_device_id DataOpentelekomcloudLbListenerV3#member_device_id}.
        :param member_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#member_timeout DataOpentelekomcloudLbListenerV3#member_timeout}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#name DataOpentelekomcloudLbListenerV3#name}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#protocol DataOpentelekomcloudLbListenerV3#protocol}.
        :param protocol_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#protocol_port DataOpentelekomcloudLbListenerV3#protocol_port}.
        :param tls_ciphers_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#tls_ciphers_policy DataOpentelekomcloudLbListenerV3#tls_ciphers_policy}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e316efec1aa3ebb1e07c08382a709a30bdc324dc19be874077581af17a99ede)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument client_ca_tls_container_ref", value=client_ca_tls_container_ref, expected_type=type_hints["client_ca_tls_container_ref"])
            check_type(argname="argument client_timeout", value=client_timeout, expected_type=type_hints["client_timeout"])
            check_type(argname="argument default_pool_id", value=default_pool_id, expected_type=type_hints["default_pool_id"])
            check_type(argname="argument default_tls_container_ref", value=default_tls_container_ref, expected_type=type_hints["default_tls_container_ref"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument keep_alive_timeout", value=keep_alive_timeout, expected_type=type_hints["keep_alive_timeout"])
            check_type(argname="argument loadbalancer_id", value=loadbalancer_id, expected_type=type_hints["loadbalancer_id"])
            check_type(argname="argument member_address", value=member_address, expected_type=type_hints["member_address"])
            check_type(argname="argument member_device_id", value=member_device_id, expected_type=type_hints["member_device_id"])
            check_type(argname="argument member_timeout", value=member_timeout, expected_type=type_hints["member_timeout"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument protocol_port", value=protocol_port, expected_type=type_hints["protocol_port"])
            check_type(argname="argument tls_ciphers_policy", value=tls_ciphers_policy, expected_type=type_hints["tls_ciphers_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if client_ca_tls_container_ref is not None:
            self._values["client_ca_tls_container_ref"] = client_ca_tls_container_ref
        if client_timeout is not None:
            self._values["client_timeout"] = client_timeout
        if default_pool_id is not None:
            self._values["default_pool_id"] = default_pool_id
        if default_tls_container_ref is not None:
            self._values["default_tls_container_ref"] = default_tls_container_ref
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if keep_alive_timeout is not None:
            self._values["keep_alive_timeout"] = keep_alive_timeout
        if loadbalancer_id is not None:
            self._values["loadbalancer_id"] = loadbalancer_id
        if member_address is not None:
            self._values["member_address"] = member_address
        if member_device_id is not None:
            self._values["member_device_id"] = member_device_id
        if member_timeout is not None:
            self._values["member_timeout"] = member_timeout
        if name is not None:
            self._values["name"] = name
        if protocol is not None:
            self._values["protocol"] = protocol
        if protocol_port is not None:
            self._values["protocol_port"] = protocol_port
        if tls_ciphers_policy is not None:
            self._values["tls_ciphers_policy"] = tls_ciphers_policy

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
    def client_ca_tls_container_ref(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#client_ca_tls_container_ref DataOpentelekomcloudLbListenerV3#client_ca_tls_container_ref}.'''
        result = self._values.get("client_ca_tls_container_ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#client_timeout DataOpentelekomcloudLbListenerV3#client_timeout}.'''
        result = self._values.get("client_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_pool_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#default_pool_id DataOpentelekomcloudLbListenerV3#default_pool_id}.'''
        result = self._values.get("default_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_tls_container_ref(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#default_tls_container_ref DataOpentelekomcloudLbListenerV3#default_tls_container_ref}.'''
        result = self._values.get("default_tls_container_ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#description DataOpentelekomcloudLbListenerV3#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#id DataOpentelekomcloudLbListenerV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keep_alive_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#keep_alive_timeout DataOpentelekomcloudLbListenerV3#keep_alive_timeout}.'''
        result = self._values.get("keep_alive_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def loadbalancer_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#loadbalancer_id DataOpentelekomcloudLbListenerV3#loadbalancer_id}.'''
        result = self._values.get("loadbalancer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#member_address DataOpentelekomcloudLbListenerV3#member_address}.'''
        result = self._values.get("member_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member_device_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#member_device_id DataOpentelekomcloudLbListenerV3#member_device_id}.'''
        result = self._values.get("member_device_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#member_timeout DataOpentelekomcloudLbListenerV3#member_timeout}.'''
        result = self._values.get("member_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#name DataOpentelekomcloudLbListenerV3#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#protocol DataOpentelekomcloudLbListenerV3#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol_port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#protocol_port DataOpentelekomcloudLbListenerV3#protocol_port}.'''
        result = self._values.get("protocol_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tls_ciphers_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_listener_v3#tls_ciphers_policy DataOpentelekomcloudLbListenerV3#tls_ciphers_policy}.'''
        result = self._values.get("tls_ciphers_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudLbListenerV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbListenerV3.DataOpentelekomcloudLbListenerV3InsertHeaders",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudLbListenerV3InsertHeaders:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudLbListenerV3InsertHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudLbListenerV3InsertHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbListenerV3.DataOpentelekomcloudLbListenerV3InsertHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__168e4c35e8a5650d237e0cb61cb153d3c18eb6f5e76a9b515ebd0c8129686c87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudLbListenerV3InsertHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c78c17714c897d93c266a7d7a53634bafc5832d33b078f0bf5693e4f5bd93f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudLbListenerV3InsertHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__365d8582fbe0e8d2e170a56a95d437d93e2b6b40ced20082a4b8f9d075f334b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1975572ddf78da899542a5d45fa04952beab68d8e494ad7d04a75edf74417ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5fec350d577466fb3770bff17e9402a4063d52538d4f04fd4ec497661f083e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudLbListenerV3InsertHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbListenerV3.DataOpentelekomcloudLbListenerV3InsertHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54641e444610f9206b83b3efe02bb277c73d21d22f28e8d77c75d921ff2757d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="forwardedForPort")
    def forwarded_for_port(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "forwardedForPort"))

    @builtins.property
    @jsii.member(jsii_name="forwardedHost")
    def forwarded_host(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "forwardedHost"))

    @builtins.property
    @jsii.member(jsii_name="forwardedPort")
    def forwarded_port(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "forwardedPort"))

    @builtins.property
    @jsii.member(jsii_name="forwardElbIp")
    def forward_elb_ip(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "forwardElbIp"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudLbListenerV3InsertHeaders]:
        return typing.cast(typing.Optional[DataOpentelekomcloudLbListenerV3InsertHeaders], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudLbListenerV3InsertHeaders],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c90fbb055844f07a5f9c1b9bf46f42276dd984552ea5fb5f2919ce680327586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbListenerV3.DataOpentelekomcloudLbListenerV3IpGroup",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudLbListenerV3IpGroup:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudLbListenerV3IpGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudLbListenerV3IpGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbListenerV3.DataOpentelekomcloudLbListenerV3IpGroupList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0be6c4e43be6a6854229f99c4968ce47c1c0077c4af0478cb82604aa4c6eaa6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudLbListenerV3IpGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14655b4b8c28a59616f87c4b3b43d64b5d56bf9300132831682030689f48e237)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudLbListenerV3IpGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25fe2e21e93fedb29c61c9989d079ada66b29f17ae5f2ed683e0432bba848744)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28fe07079c08dfa00a64713efe8f2f469d774856aa68f2cf5a8cf79dad3f1e11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2c53d46867acf5766dacf2b723b7779af5953996fbd918461bf062c047f65e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudLbListenerV3IpGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbListenerV3.DataOpentelekomcloudLbListenerV3IpGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2428a9957999ce5a1ca6c6c106f4414d97ff4938df10e78050a5c80e4e525b81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="enable")
    def enable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enable"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudLbListenerV3IpGroup]:
        return typing.cast(typing.Optional[DataOpentelekomcloudLbListenerV3IpGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudLbListenerV3IpGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__910fc2856c252fbca162ad2d7a4cd006a7f572780ed299ff528eb6195599ee19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataOpentelekomcloudLbListenerV3",
    "DataOpentelekomcloudLbListenerV3Config",
    "DataOpentelekomcloudLbListenerV3InsertHeaders",
    "DataOpentelekomcloudLbListenerV3InsertHeadersList",
    "DataOpentelekomcloudLbListenerV3InsertHeadersOutputReference",
    "DataOpentelekomcloudLbListenerV3IpGroup",
    "DataOpentelekomcloudLbListenerV3IpGroupList",
    "DataOpentelekomcloudLbListenerV3IpGroupOutputReference",
]

publication.publish()

def _typecheckingstub__ad224bce286b6c616c1c642a2844fd7895b20b30b3c8daabeef99839f860ad91(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    client_ca_tls_container_ref: typing.Optional[builtins.str] = None,
    client_timeout: typing.Optional[jsii.Number] = None,
    default_pool_id: typing.Optional[builtins.str] = None,
    default_tls_container_ref: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    keep_alive_timeout: typing.Optional[jsii.Number] = None,
    loadbalancer_id: typing.Optional[builtins.str] = None,
    member_address: typing.Optional[builtins.str] = None,
    member_device_id: typing.Optional[builtins.str] = None,
    member_timeout: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    protocol_port: typing.Optional[jsii.Number] = None,
    tls_ciphers_policy: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__86e64062066d55e72ae86d19e7f6569de5f0389b3a541627d4c41fcaf5b6cd99(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08d7d3f340acece115d31a6a89269f522a9685ff737e7c75b9e60f50e8fe6b99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc2fa3679c9532dfacf9303af4bca33832530a395960d635e8091b36ee56745(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182d7994f4f7cb32dc77cb14c6ad8eb2d78b48dd23bad9c61cb70dbb1bb26cfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__093ed7e809dc87a67446d05706a4fc49a08d34e55eae4f289217095aeee76726(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dcc299a9a104778c0ad7fa7554a7b68b86bc198c781635cf758162b4b850a88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d9927754f0dc2add712a071e557717bff3d4b558be27a863eabb651c334bbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b0074a855ba11e0a4050309688c25a5b5565af4d6865ab3f848ec1e1982dec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__086f3f2a72366fc6dce5b3500ed15302205dd01733ad7b998ae19bd07586fe78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b8e60e9cdf0c8c25a48c5cd9b0cacd0e1cd5f76399980a7eaf490d12e75331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__197bf9c50b775bd80fed4dc0bfae2c80f45387769cd1db74fa2ff4a1fc2cc3de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580b83a812aa15d7e93bb8a69206dd066e21473b96b0f2b29a1001180e0d3968(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b121a48dcae39cb17930f652da3546fc43cb1fbaa0fccde0e72e71da97d524(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9278cfdc6b9fd6203bdc16eb3debf3457c28f1b2a87135eaf2b9da003d6f519(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dff95f23b9ff589bb76d80d80ff613b94022581ca278a5756be3be2a122e26c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077f5215fa977efbb08a025d41a301d95d9698936dc4d89a45e08b6b710b6720(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e316efec1aa3ebb1e07c08382a709a30bdc324dc19be874077581af17a99ede(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    client_ca_tls_container_ref: typing.Optional[builtins.str] = None,
    client_timeout: typing.Optional[jsii.Number] = None,
    default_pool_id: typing.Optional[builtins.str] = None,
    default_tls_container_ref: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    keep_alive_timeout: typing.Optional[jsii.Number] = None,
    loadbalancer_id: typing.Optional[builtins.str] = None,
    member_address: typing.Optional[builtins.str] = None,
    member_device_id: typing.Optional[builtins.str] = None,
    member_timeout: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    protocol_port: typing.Optional[jsii.Number] = None,
    tls_ciphers_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168e4c35e8a5650d237e0cb61cb153d3c18eb6f5e76a9b515ebd0c8129686c87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c78c17714c897d93c266a7d7a53634bafc5832d33b078f0bf5693e4f5bd93f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__365d8582fbe0e8d2e170a56a95d437d93e2b6b40ced20082a4b8f9d075f334b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1975572ddf78da899542a5d45fa04952beab68d8e494ad7d04a75edf74417ab(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5fec350d577466fb3770bff17e9402a4063d52538d4f04fd4ec497661f083e6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54641e444610f9206b83b3efe02bb277c73d21d22f28e8d77c75d921ff2757d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c90fbb055844f07a5f9c1b9bf46f42276dd984552ea5fb5f2919ce680327586(
    value: typing.Optional[DataOpentelekomcloudLbListenerV3InsertHeaders],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be6c4e43be6a6854229f99c4968ce47c1c0077c4af0478cb82604aa4c6eaa6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14655b4b8c28a59616f87c4b3b43d64b5d56bf9300132831682030689f48e237(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25fe2e21e93fedb29c61c9989d079ada66b29f17ae5f2ed683e0432bba848744(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28fe07079c08dfa00a64713efe8f2f469d774856aa68f2cf5a8cf79dad3f1e11(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c53d46867acf5766dacf2b723b7779af5953996fbd918461bf062c047f65e4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2428a9957999ce5a1ca6c6c106f4414d97ff4938df10e78050a5c80e4e525b81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__910fc2856c252fbca162ad2d7a4cd006a7f572780ed299ff528eb6195599ee19(
    value: typing.Optional[DataOpentelekomcloudLbListenerV3IpGroup],
) -> None:
    """Type checking stubs"""
    pass

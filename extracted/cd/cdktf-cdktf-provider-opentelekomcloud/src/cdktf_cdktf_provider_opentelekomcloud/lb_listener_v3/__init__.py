r'''
# `opentelekomcloud_lb_listener_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_lb_listener_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3).
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


class LbListenerV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.lbListenerV3.LbListenerV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3 opentelekomcloud_lb_listener_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        loadbalancer_id: builtins.str,
        protocol: builtins.str,
        protocol_port: jsii.Number,
        admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        advanced_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_ca_tls_container_ref: typing.Optional[builtins.str] = None,
        client_timeout: typing.Optional[jsii.Number] = None,
        default_pool_id: typing.Optional[builtins.str] = None,
        default_tls_container_ref: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        http2_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        insert_headers: typing.Optional[typing.Union["LbListenerV3InsertHeaders", typing.Dict[builtins.str, typing.Any]]] = None,
        ip_group: typing.Optional[typing.Union["LbListenerV3IpGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        keep_alive_timeout: typing.Optional[jsii.Number] = None,
        member_retry_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        member_timeout: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        security_policy_id: typing.Optional[builtins.str] = None,
        sni_container_refs: typing.Optional[typing.Sequence[builtins.str]] = None,
        sni_match_algo: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tls_ciphers_policy: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3 opentelekomcloud_lb_listener_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param loadbalancer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#loadbalancer_id LbListenerV3#loadbalancer_id}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#protocol LbListenerV3#protocol}.
        :param protocol_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#protocol_port LbListenerV3#protocol_port}.
        :param admin_state_up: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#admin_state_up LbListenerV3#admin_state_up}.
        :param advanced_forwarding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#advanced_forwarding LbListenerV3#advanced_forwarding}.
        :param client_ca_tls_container_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#client_ca_tls_container_ref LbListenerV3#client_ca_tls_container_ref}.
        :param client_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#client_timeout LbListenerV3#client_timeout}.
        :param default_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#default_pool_id LbListenerV3#default_pool_id}.
        :param default_tls_container_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#default_tls_container_ref LbListenerV3#default_tls_container_ref}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#description LbListenerV3#description}.
        :param http2_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#http2_enable LbListenerV3#http2_enable}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#id LbListenerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insert_headers: insert_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#insert_headers LbListenerV3#insert_headers}
        :param ip_group: ip_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#ip_group LbListenerV3#ip_group}
        :param keep_alive_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#keep_alive_timeout LbListenerV3#keep_alive_timeout}.
        :param member_retry_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#member_retry_enable LbListenerV3#member_retry_enable}.
        :param member_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#member_timeout LbListenerV3#member_timeout}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#name LbListenerV3#name}.
        :param security_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#security_policy_id LbListenerV3#security_policy_id}.
        :param sni_container_refs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#sni_container_refs LbListenerV3#sni_container_refs}.
        :param sni_match_algo: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#sni_match_algo LbListenerV3#sni_match_algo}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#tags LbListenerV3#tags}.
        :param tls_ciphers_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#tls_ciphers_policy LbListenerV3#tls_ciphers_policy}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc619156b998afcf38331a9cfb41eb8e8efd1c80e3f5a5d9a598826bf56b3c34)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LbListenerV3Config(
            loadbalancer_id=loadbalancer_id,
            protocol=protocol,
            protocol_port=protocol_port,
            admin_state_up=admin_state_up,
            advanced_forwarding=advanced_forwarding,
            client_ca_tls_container_ref=client_ca_tls_container_ref,
            client_timeout=client_timeout,
            default_pool_id=default_pool_id,
            default_tls_container_ref=default_tls_container_ref,
            description=description,
            http2_enable=http2_enable,
            id=id,
            insert_headers=insert_headers,
            ip_group=ip_group,
            keep_alive_timeout=keep_alive_timeout,
            member_retry_enable=member_retry_enable,
            member_timeout=member_timeout,
            name=name,
            security_policy_id=security_policy_id,
            sni_container_refs=sni_container_refs,
            sni_match_algo=sni_match_algo,
            tags=tags,
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
        '''Generates CDKTF code for importing a LbListenerV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LbListenerV3 to import.
        :param import_from_id: The id of the existing LbListenerV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LbListenerV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0dc5df2d5508e56cfdf7a509fb5e20d089d6e1c3a269e32e8c0feb3ccfd0a9b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putInsertHeaders")
    def put_insert_headers(
        self,
        *,
        forwarded_for_port: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forwarded_host: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forwarded_port: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forward_elb_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param forwarded_for_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#forwarded_for_port LbListenerV3#forwarded_for_port}.
        :param forwarded_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#forwarded_host LbListenerV3#forwarded_host}.
        :param forwarded_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#forwarded_port LbListenerV3#forwarded_port}.
        :param forward_elb_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#forward_elb_ip LbListenerV3#forward_elb_ip}.
        '''
        value = LbListenerV3InsertHeaders(
            forwarded_for_port=forwarded_for_port,
            forwarded_host=forwarded_host,
            forwarded_port=forwarded_port,
            forward_elb_ip=forward_elb_ip,
        )

        return typing.cast(None, jsii.invoke(self, "putInsertHeaders", [value]))

    @jsii.member(jsii_name="putIpGroup")
    def put_ip_group(
        self,
        *,
        id: builtins.str,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#id LbListenerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#enable LbListenerV3#enable}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#type LbListenerV3#type}.
        '''
        value = LbListenerV3IpGroup(id=id, enable=enable, type=type)

        return typing.cast(None, jsii.invoke(self, "putIpGroup", [value]))

    @jsii.member(jsii_name="resetAdminStateUp")
    def reset_admin_state_up(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminStateUp", []))

    @jsii.member(jsii_name="resetAdvancedForwarding")
    def reset_advanced_forwarding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedForwarding", []))

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

    @jsii.member(jsii_name="resetHttp2Enable")
    def reset_http2_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp2Enable", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInsertHeaders")
    def reset_insert_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsertHeaders", []))

    @jsii.member(jsii_name="resetIpGroup")
    def reset_ip_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpGroup", []))

    @jsii.member(jsii_name="resetKeepAliveTimeout")
    def reset_keep_alive_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepAliveTimeout", []))

    @jsii.member(jsii_name="resetMemberRetryEnable")
    def reset_member_retry_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemberRetryEnable", []))

    @jsii.member(jsii_name="resetMemberTimeout")
    def reset_member_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemberTimeout", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSecurityPolicyId")
    def reset_security_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityPolicyId", []))

    @jsii.member(jsii_name="resetSniContainerRefs")
    def reset_sni_container_refs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSniContainerRefs", []))

    @jsii.member(jsii_name="resetSniMatchAlgo")
    def reset_sni_match_algo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSniMatchAlgo", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="insertHeaders")
    def insert_headers(self) -> "LbListenerV3InsertHeadersOutputReference":
        return typing.cast("LbListenerV3InsertHeadersOutputReference", jsii.get(self, "insertHeaders"))

    @builtins.property
    @jsii.member(jsii_name="ipGroup")
    def ip_group(self) -> "LbListenerV3IpGroupOutputReference":
        return typing.cast("LbListenerV3IpGroupOutputReference", jsii.get(self, "ipGroup"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="adminStateUpInput")
    def admin_state_up_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "adminStateUpInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedForwardingInput")
    def advanced_forwarding_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "advancedForwardingInput"))

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
    @jsii.member(jsii_name="http2EnableInput")
    def http2_enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "http2EnableInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="insertHeadersInput")
    def insert_headers_input(self) -> typing.Optional["LbListenerV3InsertHeaders"]:
        return typing.cast(typing.Optional["LbListenerV3InsertHeaders"], jsii.get(self, "insertHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="ipGroupInput")
    def ip_group_input(self) -> typing.Optional["LbListenerV3IpGroup"]:
        return typing.cast(typing.Optional["LbListenerV3IpGroup"], jsii.get(self, "ipGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="keepAliveTimeoutInput")
    def keep_alive_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepAliveTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="loadbalancerIdInput")
    def loadbalancer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadbalancerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="memberRetryEnableInput")
    def member_retry_enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "memberRetryEnableInput"))

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
    @jsii.member(jsii_name="securityPolicyIdInput")
    def security_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sniContainerRefsInput")
    def sni_container_refs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sniContainerRefsInput"))

    @builtins.property
    @jsii.member(jsii_name="sniMatchAlgoInput")
    def sni_match_algo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sniMatchAlgoInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsCiphersPolicyInput")
    def tls_ciphers_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsCiphersPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="adminStateUp")
    def admin_state_up(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "adminStateUp"))

    @admin_state_up.setter
    def admin_state_up(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8c391263f92998862502fccbba472deb4eb51974aca0dbf4fc852666047bfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminStateUp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="advancedForwarding")
    def advanced_forwarding(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "advancedForwarding"))

    @advanced_forwarding.setter
    def advanced_forwarding(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39390539cb46639c4df633929d3e2c08edd57dab2461cd9e247ad9afb8932872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advancedForwarding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCaTlsContainerRef")
    def client_ca_tls_container_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCaTlsContainerRef"))

    @client_ca_tls_container_ref.setter
    def client_ca_tls_container_ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab27435075b9e3db1820f9088ba002efb727c3783c4067c13f197ce64c9dfae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCaTlsContainerRef", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientTimeout")
    def client_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientTimeout"))

    @client_timeout.setter
    def client_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2d7f5c3d1716a6ad6a09ee0410097d4aba1f186f475e6d4024f14f3129610ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultPoolId")
    def default_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultPoolId"))

    @default_pool_id.setter
    def default_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__601419235f6a2662581f8b84548d10bd4105bf585c16f939bca31e096ee9b136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTlsContainerRef")
    def default_tls_container_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultTlsContainerRef"))

    @default_tls_container_ref.setter
    def default_tls_container_ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e43c3c262008838255f18d236f60682721ca7daf94e7b4e3a0f0a444f3a629d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTlsContainerRef", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d409d4d8f75495cd740996188c14fe4143cccb8630ce12a54b4c261b2cf73391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="http2Enable")
    def http2_enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "http2Enable"))

    @http2_enable.setter
    def http2_enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__632650c5140bb3e36703e09e16b125e18c02700c654048f6b4b1fedc0f322151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "http2Enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3744b01b9a123a8af3590a074639c4d9fcc40e6f339c312849d19fb5881ff7d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keepAliveTimeout")
    def keep_alive_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepAliveTimeout"))

    @keep_alive_timeout.setter
    def keep_alive_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b07878c842e2176bc1fc2c5e79fe12787e6e0b83e70568809e67245d9940cc15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepAliveTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadbalancerId")
    def loadbalancer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadbalancerId"))

    @loadbalancer_id.setter
    def loadbalancer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7e8c45cd34d9ef36d11ba650fe9ba61a285ff3059a39f4666fa17c40ba459a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadbalancerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memberRetryEnable")
    def member_retry_enable(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "memberRetryEnable"))

    @member_retry_enable.setter
    def member_retry_enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__796c442b67a770838a92a6ca418ee54e4d10af9921a7cfe830635af5c5430bf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberRetryEnable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memberTimeout")
    def member_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memberTimeout"))

    @member_timeout.setter
    def member_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e3cbf3269e80ea71a539a5d4151de67793b6215364033ea6ebd91787adac649)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5452554ee92482862cfe7dcbda73073176949b8e7daaae3c2b860a77d9ef7953)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff39f02169aeeacbb146b1b2d27c166222229fbab45279d28071c3d122ac415)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocolPort")
    def protocol_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "protocolPort"))

    @protocol_port.setter
    def protocol_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__144b58c544413aeb1f80f01036d4158ade3b7eec7b71b931e28327ee88b03ea5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityPolicyId")
    def security_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityPolicyId"))

    @security_policy_id.setter
    def security_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6da276fe4a2352194a2ae8e7fc481876bf51596af04647a66a35234d8dbac9b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sniContainerRefs")
    def sni_container_refs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sniContainerRefs"))

    @sni_container_refs.setter
    def sni_container_refs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa94406d374b6d1a5c04ecefe33077dfc46078df5c19bcaacfeb46b24be4b093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sniContainerRefs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sniMatchAlgo")
    def sni_match_algo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sniMatchAlgo"))

    @sni_match_algo.setter
    def sni_match_algo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa43fbcd4628f539f5614a006adc84a3129612301c217a404c1429626e34ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sniMatchAlgo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad6e549454c29fcc75631ac5a936178901073ad2ed193b80e0ddef4f74bdf18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsCiphersPolicy")
    def tls_ciphers_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsCiphersPolicy"))

    @tls_ciphers_policy.setter
    def tls_ciphers_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc84439cbe2ac55e7801a167dfd17835ee1d587bc510cf077d7d579a7fa70c68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsCiphersPolicy", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.lbListenerV3.LbListenerV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "loadbalancer_id": "loadbalancerId",
        "protocol": "protocol",
        "protocol_port": "protocolPort",
        "admin_state_up": "adminStateUp",
        "advanced_forwarding": "advancedForwarding",
        "client_ca_tls_container_ref": "clientCaTlsContainerRef",
        "client_timeout": "clientTimeout",
        "default_pool_id": "defaultPoolId",
        "default_tls_container_ref": "defaultTlsContainerRef",
        "description": "description",
        "http2_enable": "http2Enable",
        "id": "id",
        "insert_headers": "insertHeaders",
        "ip_group": "ipGroup",
        "keep_alive_timeout": "keepAliveTimeout",
        "member_retry_enable": "memberRetryEnable",
        "member_timeout": "memberTimeout",
        "name": "name",
        "security_policy_id": "securityPolicyId",
        "sni_container_refs": "sniContainerRefs",
        "sni_match_algo": "sniMatchAlgo",
        "tags": "tags",
        "tls_ciphers_policy": "tlsCiphersPolicy",
    },
)
class LbListenerV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        loadbalancer_id: builtins.str,
        protocol: builtins.str,
        protocol_port: jsii.Number,
        admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        advanced_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_ca_tls_container_ref: typing.Optional[builtins.str] = None,
        client_timeout: typing.Optional[jsii.Number] = None,
        default_pool_id: typing.Optional[builtins.str] = None,
        default_tls_container_ref: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        http2_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        insert_headers: typing.Optional[typing.Union["LbListenerV3InsertHeaders", typing.Dict[builtins.str, typing.Any]]] = None,
        ip_group: typing.Optional[typing.Union["LbListenerV3IpGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        keep_alive_timeout: typing.Optional[jsii.Number] = None,
        member_retry_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        member_timeout: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        security_policy_id: typing.Optional[builtins.str] = None,
        sni_container_refs: typing.Optional[typing.Sequence[builtins.str]] = None,
        sni_match_algo: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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
        :param loadbalancer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#loadbalancer_id LbListenerV3#loadbalancer_id}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#protocol LbListenerV3#protocol}.
        :param protocol_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#protocol_port LbListenerV3#protocol_port}.
        :param admin_state_up: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#admin_state_up LbListenerV3#admin_state_up}.
        :param advanced_forwarding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#advanced_forwarding LbListenerV3#advanced_forwarding}.
        :param client_ca_tls_container_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#client_ca_tls_container_ref LbListenerV3#client_ca_tls_container_ref}.
        :param client_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#client_timeout LbListenerV3#client_timeout}.
        :param default_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#default_pool_id LbListenerV3#default_pool_id}.
        :param default_tls_container_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#default_tls_container_ref LbListenerV3#default_tls_container_ref}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#description LbListenerV3#description}.
        :param http2_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#http2_enable LbListenerV3#http2_enable}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#id LbListenerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insert_headers: insert_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#insert_headers LbListenerV3#insert_headers}
        :param ip_group: ip_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#ip_group LbListenerV3#ip_group}
        :param keep_alive_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#keep_alive_timeout LbListenerV3#keep_alive_timeout}.
        :param member_retry_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#member_retry_enable LbListenerV3#member_retry_enable}.
        :param member_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#member_timeout LbListenerV3#member_timeout}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#name LbListenerV3#name}.
        :param security_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#security_policy_id LbListenerV3#security_policy_id}.
        :param sni_container_refs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#sni_container_refs LbListenerV3#sni_container_refs}.
        :param sni_match_algo: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#sni_match_algo LbListenerV3#sni_match_algo}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#tags LbListenerV3#tags}.
        :param tls_ciphers_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#tls_ciphers_policy LbListenerV3#tls_ciphers_policy}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(insert_headers, dict):
            insert_headers = LbListenerV3InsertHeaders(**insert_headers)
        if isinstance(ip_group, dict):
            ip_group = LbListenerV3IpGroup(**ip_group)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81318e785582ba82441f9855a53205422259121e5b7438f56468f1e7f2a8de05)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument loadbalancer_id", value=loadbalancer_id, expected_type=type_hints["loadbalancer_id"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument protocol_port", value=protocol_port, expected_type=type_hints["protocol_port"])
            check_type(argname="argument admin_state_up", value=admin_state_up, expected_type=type_hints["admin_state_up"])
            check_type(argname="argument advanced_forwarding", value=advanced_forwarding, expected_type=type_hints["advanced_forwarding"])
            check_type(argname="argument client_ca_tls_container_ref", value=client_ca_tls_container_ref, expected_type=type_hints["client_ca_tls_container_ref"])
            check_type(argname="argument client_timeout", value=client_timeout, expected_type=type_hints["client_timeout"])
            check_type(argname="argument default_pool_id", value=default_pool_id, expected_type=type_hints["default_pool_id"])
            check_type(argname="argument default_tls_container_ref", value=default_tls_container_ref, expected_type=type_hints["default_tls_container_ref"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument http2_enable", value=http2_enable, expected_type=type_hints["http2_enable"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument insert_headers", value=insert_headers, expected_type=type_hints["insert_headers"])
            check_type(argname="argument ip_group", value=ip_group, expected_type=type_hints["ip_group"])
            check_type(argname="argument keep_alive_timeout", value=keep_alive_timeout, expected_type=type_hints["keep_alive_timeout"])
            check_type(argname="argument member_retry_enable", value=member_retry_enable, expected_type=type_hints["member_retry_enable"])
            check_type(argname="argument member_timeout", value=member_timeout, expected_type=type_hints["member_timeout"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument security_policy_id", value=security_policy_id, expected_type=type_hints["security_policy_id"])
            check_type(argname="argument sni_container_refs", value=sni_container_refs, expected_type=type_hints["sni_container_refs"])
            check_type(argname="argument sni_match_algo", value=sni_match_algo, expected_type=type_hints["sni_match_algo"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tls_ciphers_policy", value=tls_ciphers_policy, expected_type=type_hints["tls_ciphers_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "loadbalancer_id": loadbalancer_id,
            "protocol": protocol,
            "protocol_port": protocol_port,
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
        if admin_state_up is not None:
            self._values["admin_state_up"] = admin_state_up
        if advanced_forwarding is not None:
            self._values["advanced_forwarding"] = advanced_forwarding
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
        if http2_enable is not None:
            self._values["http2_enable"] = http2_enable
        if id is not None:
            self._values["id"] = id
        if insert_headers is not None:
            self._values["insert_headers"] = insert_headers
        if ip_group is not None:
            self._values["ip_group"] = ip_group
        if keep_alive_timeout is not None:
            self._values["keep_alive_timeout"] = keep_alive_timeout
        if member_retry_enable is not None:
            self._values["member_retry_enable"] = member_retry_enable
        if member_timeout is not None:
            self._values["member_timeout"] = member_timeout
        if name is not None:
            self._values["name"] = name
        if security_policy_id is not None:
            self._values["security_policy_id"] = security_policy_id
        if sni_container_refs is not None:
            self._values["sni_container_refs"] = sni_container_refs
        if sni_match_algo is not None:
            self._values["sni_match_algo"] = sni_match_algo
        if tags is not None:
            self._values["tags"] = tags
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
    def loadbalancer_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#loadbalancer_id LbListenerV3#loadbalancer_id}.'''
        result = self._values.get("loadbalancer_id")
        assert result is not None, "Required property 'loadbalancer_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#protocol LbListenerV3#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#protocol_port LbListenerV3#protocol_port}.'''
        result = self._values.get("protocol_port")
        assert result is not None, "Required property 'protocol_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def admin_state_up(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#admin_state_up LbListenerV3#admin_state_up}.'''
        result = self._values.get("admin_state_up")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def advanced_forwarding(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#advanced_forwarding LbListenerV3#advanced_forwarding}.'''
        result = self._values.get("advanced_forwarding")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_ca_tls_container_ref(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#client_ca_tls_container_ref LbListenerV3#client_ca_tls_container_ref}.'''
        result = self._values.get("client_ca_tls_container_ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#client_timeout LbListenerV3#client_timeout}.'''
        result = self._values.get("client_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_pool_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#default_pool_id LbListenerV3#default_pool_id}.'''
        result = self._values.get("default_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_tls_container_ref(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#default_tls_container_ref LbListenerV3#default_tls_container_ref}.'''
        result = self._values.get("default_tls_container_ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#description LbListenerV3#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http2_enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#http2_enable LbListenerV3#http2_enable}.'''
        result = self._values.get("http2_enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#id LbListenerV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insert_headers(self) -> typing.Optional["LbListenerV3InsertHeaders"]:
        '''insert_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#insert_headers LbListenerV3#insert_headers}
        '''
        result = self._values.get("insert_headers")
        return typing.cast(typing.Optional["LbListenerV3InsertHeaders"], result)

    @builtins.property
    def ip_group(self) -> typing.Optional["LbListenerV3IpGroup"]:
        '''ip_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#ip_group LbListenerV3#ip_group}
        '''
        result = self._values.get("ip_group")
        return typing.cast(typing.Optional["LbListenerV3IpGroup"], result)

    @builtins.property
    def keep_alive_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#keep_alive_timeout LbListenerV3#keep_alive_timeout}.'''
        result = self._values.get("keep_alive_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def member_retry_enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#member_retry_enable LbListenerV3#member_retry_enable}.'''
        result = self._values.get("member_retry_enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def member_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#member_timeout LbListenerV3#member_timeout}.'''
        result = self._values.get("member_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#name LbListenerV3#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#security_policy_id LbListenerV3#security_policy_id}.'''
        result = self._values.get("security_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sni_container_refs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#sni_container_refs LbListenerV3#sni_container_refs}.'''
        result = self._values.get("sni_container_refs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sni_match_algo(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#sni_match_algo LbListenerV3#sni_match_algo}.'''
        result = self._values.get("sni_match_algo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#tags LbListenerV3#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tls_ciphers_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#tls_ciphers_policy LbListenerV3#tls_ciphers_policy}.'''
        result = self._values.get("tls_ciphers_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbListenerV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.lbListenerV3.LbListenerV3InsertHeaders",
    jsii_struct_bases=[],
    name_mapping={
        "forwarded_for_port": "forwardedForPort",
        "forwarded_host": "forwardedHost",
        "forwarded_port": "forwardedPort",
        "forward_elb_ip": "forwardElbIp",
    },
)
class LbListenerV3InsertHeaders:
    def __init__(
        self,
        *,
        forwarded_for_port: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forwarded_host: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forwarded_port: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forward_elb_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param forwarded_for_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#forwarded_for_port LbListenerV3#forwarded_for_port}.
        :param forwarded_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#forwarded_host LbListenerV3#forwarded_host}.
        :param forwarded_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#forwarded_port LbListenerV3#forwarded_port}.
        :param forward_elb_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#forward_elb_ip LbListenerV3#forward_elb_ip}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__071c25a6bccf8175d2f4c182b902fbcc4994a3a84a7e42d1db2ff0d43d89428a)
            check_type(argname="argument forwarded_for_port", value=forwarded_for_port, expected_type=type_hints["forwarded_for_port"])
            check_type(argname="argument forwarded_host", value=forwarded_host, expected_type=type_hints["forwarded_host"])
            check_type(argname="argument forwarded_port", value=forwarded_port, expected_type=type_hints["forwarded_port"])
            check_type(argname="argument forward_elb_ip", value=forward_elb_ip, expected_type=type_hints["forward_elb_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if forwarded_for_port is not None:
            self._values["forwarded_for_port"] = forwarded_for_port
        if forwarded_host is not None:
            self._values["forwarded_host"] = forwarded_host
        if forwarded_port is not None:
            self._values["forwarded_port"] = forwarded_port
        if forward_elb_ip is not None:
            self._values["forward_elb_ip"] = forward_elb_ip

    @builtins.property
    def forwarded_for_port(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#forwarded_for_port LbListenerV3#forwarded_for_port}.'''
        result = self._values.get("forwarded_for_port")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def forwarded_host(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#forwarded_host LbListenerV3#forwarded_host}.'''
        result = self._values.get("forwarded_host")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def forwarded_port(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#forwarded_port LbListenerV3#forwarded_port}.'''
        result = self._values.get("forwarded_port")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def forward_elb_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#forward_elb_ip LbListenerV3#forward_elb_ip}.'''
        result = self._values.get("forward_elb_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbListenerV3InsertHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbListenerV3InsertHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.lbListenerV3.LbListenerV3InsertHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aef017c68a2963b096ee760cba8b70555e8a1e90e1847714d7a147c971eaac1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetForwardedForPort")
    def reset_forwarded_for_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardedForPort", []))

    @jsii.member(jsii_name="resetForwardedHost")
    def reset_forwarded_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardedHost", []))

    @jsii.member(jsii_name="resetForwardedPort")
    def reset_forwarded_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardedPort", []))

    @jsii.member(jsii_name="resetForwardElbIp")
    def reset_forward_elb_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardElbIp", []))

    @builtins.property
    @jsii.member(jsii_name="forwardedForPortInput")
    def forwarded_for_port_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forwardedForPortInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardedHostInput")
    def forwarded_host_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forwardedHostInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardedPortInput")
    def forwarded_port_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forwardedPortInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardElbIpInput")
    def forward_elb_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forwardElbIpInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardedForPort")
    def forwarded_for_port(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forwardedForPort"))

    @forwarded_for_port.setter
    def forwarded_for_port(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f05ac3b8549944240bc3b5288020b84f5ed1f309547b9917a4e0aeb921416a49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardedForPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardedHost")
    def forwarded_host(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forwardedHost"))

    @forwarded_host.setter
    def forwarded_host(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab99c994a147c008e8377240a4e39f965653e677fc852c4781d8521a546a2f2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardedHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardedPort")
    def forwarded_port(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forwardedPort"))

    @forwarded_port.setter
    def forwarded_port(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d2ca4e8774dda5789f39d298b543d21f30ad69f65ceb1dfb9c0c47cee4428e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardedPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardElbIp")
    def forward_elb_ip(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forwardElbIp"))

    @forward_elb_ip.setter
    def forward_elb_ip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b2d49e733506991fcd6977c28e6d44fde49a5ccadee7f03338da92d92fe594d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardElbIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LbListenerV3InsertHeaders]:
        return typing.cast(typing.Optional[LbListenerV3InsertHeaders], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LbListenerV3InsertHeaders]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__850800adae653ed4155c6af9312ef15e28627d89adc7cbd538cedea37ed276e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.lbListenerV3.LbListenerV3IpGroup",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "enable": "enable", "type": "type"},
)
class LbListenerV3IpGroup:
    def __init__(
        self,
        *,
        id: builtins.str,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#id LbListenerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#enable LbListenerV3#enable}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#type LbListenerV3#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b45b631c3e37247b39f5f0bbca93e1c8e949b87967bf09e54b3a3156b79e341b)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if enable is not None:
            self._values["enable"] = enable
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#id LbListenerV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#enable LbListenerV3#enable}.'''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_listener_v3#type LbListenerV3#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbListenerV3IpGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbListenerV3IpGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.lbListenerV3.LbListenerV3IpGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfa691f4805346b9adf108feb461af68fcf71f5efdb05eeb87be6e296cb0d72a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnable")
    def reset_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnable", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="enableInput")
    def enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="enable")
    def enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enable"))

    @enable.setter
    def enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e312fa248f02745b42c818a3550f5f464fcf627103b2bee4c1b3cb6905c585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4327a053a7ba9692b0bb50294b36adabdd12ff250e90763a70ddd443965ba503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bca36fbf542d66d926f5cedc99985ccb31d553db9d57e083554c03e8d30b92a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LbListenerV3IpGroup]:
        return typing.cast(typing.Optional[LbListenerV3IpGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LbListenerV3IpGroup]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c39b51eb930c90c45881f30831e12be7c993d279bb2ad82acd6ae1e2b6f621)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LbListenerV3",
    "LbListenerV3Config",
    "LbListenerV3InsertHeaders",
    "LbListenerV3InsertHeadersOutputReference",
    "LbListenerV3IpGroup",
    "LbListenerV3IpGroupOutputReference",
]

publication.publish()

def _typecheckingstub__cc619156b998afcf38331a9cfb41eb8e8efd1c80e3f5a5d9a598826bf56b3c34(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    loadbalancer_id: builtins.str,
    protocol: builtins.str,
    protocol_port: jsii.Number,
    admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    advanced_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_ca_tls_container_ref: typing.Optional[builtins.str] = None,
    client_timeout: typing.Optional[jsii.Number] = None,
    default_pool_id: typing.Optional[builtins.str] = None,
    default_tls_container_ref: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    http2_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    insert_headers: typing.Optional[typing.Union[LbListenerV3InsertHeaders, typing.Dict[builtins.str, typing.Any]]] = None,
    ip_group: typing.Optional[typing.Union[LbListenerV3IpGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    keep_alive_timeout: typing.Optional[jsii.Number] = None,
    member_retry_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    member_timeout: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    security_policy_id: typing.Optional[builtins.str] = None,
    sni_container_refs: typing.Optional[typing.Sequence[builtins.str]] = None,
    sni_match_algo: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__a0dc5df2d5508e56cfdf7a509fb5e20d089d6e1c3a269e32e8c0feb3ccfd0a9b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8c391263f92998862502fccbba472deb4eb51974aca0dbf4fc852666047bfd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39390539cb46639c4df633929d3e2c08edd57dab2461cd9e247ad9afb8932872(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab27435075b9e3db1820f9088ba002efb727c3783c4067c13f197ce64c9dfae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d7f5c3d1716a6ad6a09ee0410097d4aba1f186f475e6d4024f14f3129610ac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__601419235f6a2662581f8b84548d10bd4105bf585c16f939bca31e096ee9b136(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e43c3c262008838255f18d236f60682721ca7daf94e7b4e3a0f0a444f3a629d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d409d4d8f75495cd740996188c14fe4143cccb8630ce12a54b4c261b2cf73391(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632650c5140bb3e36703e09e16b125e18c02700c654048f6b4b1fedc0f322151(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3744b01b9a123a8af3590a074639c4d9fcc40e6f339c312849d19fb5881ff7d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07878c842e2176bc1fc2c5e79fe12787e6e0b83e70568809e67245d9940cc15(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7e8c45cd34d9ef36d11ba650fe9ba61a285ff3059a39f4666fa17c40ba459a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796c442b67a770838a92a6ca418ee54e4d10af9921a7cfe830635af5c5430bf4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3cbf3269e80ea71a539a5d4151de67793b6215364033ea6ebd91787adac649(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5452554ee92482862cfe7dcbda73073176949b8e7daaae3c2b860a77d9ef7953(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff39f02169aeeacbb146b1b2d27c166222229fbab45279d28071c3d122ac415(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144b58c544413aeb1f80f01036d4158ade3b7eec7b71b931e28327ee88b03ea5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da276fe4a2352194a2ae8e7fc481876bf51596af04647a66a35234d8dbac9b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa94406d374b6d1a5c04ecefe33077dfc46078df5c19bcaacfeb46b24be4b093(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa43fbcd4628f539f5614a006adc84a3129612301c217a404c1429626e34ec5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad6e549454c29fcc75631ac5a936178901073ad2ed193b80e0ddef4f74bdf18(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc84439cbe2ac55e7801a167dfd17835ee1d587bc510cf077d7d579a7fa70c68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81318e785582ba82441f9855a53205422259121e5b7438f56468f1e7f2a8de05(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    loadbalancer_id: builtins.str,
    protocol: builtins.str,
    protocol_port: jsii.Number,
    admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    advanced_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_ca_tls_container_ref: typing.Optional[builtins.str] = None,
    client_timeout: typing.Optional[jsii.Number] = None,
    default_pool_id: typing.Optional[builtins.str] = None,
    default_tls_container_ref: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    http2_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    insert_headers: typing.Optional[typing.Union[LbListenerV3InsertHeaders, typing.Dict[builtins.str, typing.Any]]] = None,
    ip_group: typing.Optional[typing.Union[LbListenerV3IpGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    keep_alive_timeout: typing.Optional[jsii.Number] = None,
    member_retry_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    member_timeout: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    security_policy_id: typing.Optional[builtins.str] = None,
    sni_container_refs: typing.Optional[typing.Sequence[builtins.str]] = None,
    sni_match_algo: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tls_ciphers_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__071c25a6bccf8175d2f4c182b902fbcc4994a3a84a7e42d1db2ff0d43d89428a(
    *,
    forwarded_for_port: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forwarded_host: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forwarded_port: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forward_elb_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef017c68a2963b096ee760cba8b70555e8a1e90e1847714d7a147c971eaac1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05ac3b8549944240bc3b5288020b84f5ed1f309547b9917a4e0aeb921416a49(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab99c994a147c008e8377240a4e39f965653e677fc852c4781d8521a546a2f2c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d2ca4e8774dda5789f39d298b543d21f30ad69f65ceb1dfb9c0c47cee4428e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b2d49e733506991fcd6977c28e6d44fde49a5ccadee7f03338da92d92fe594d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__850800adae653ed4155c6af9312ef15e28627d89adc7cbd538cedea37ed276e0(
    value: typing.Optional[LbListenerV3InsertHeaders],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45b631c3e37247b39f5f0bbca93e1c8e949b87967bf09e54b3a3156b79e341b(
    *,
    id: builtins.str,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfa691f4805346b9adf108feb461af68fcf71f5efdb05eeb87be6e296cb0d72a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e312fa248f02745b42c818a3550f5f464fcf627103b2bee4c1b3cb6905c585(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4327a053a7ba9692b0bb50294b36adabdd12ff250e90763a70ddd443965ba503(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bca36fbf542d66d926f5cedc99985ccb31d553db9d57e083554c03e8d30b92a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c39b51eb930c90c45881f30831e12be7c993d279bb2ad82acd6ae1e2b6f621(
    value: typing.Optional[LbListenerV3IpGroup],
) -> None:
    """Type checking stubs"""
    pass

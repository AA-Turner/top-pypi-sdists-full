r'''
# `google_apigee_target_server`

Refer to the Terraform Registry for docs: [`google_apigee_target_server`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server).
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


class GoogleApigeeTargetServer(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeTargetServer.GoogleApigeeTargetServer",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server google_apigee_target_server}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        env_id: builtins.str,
        host: builtins.str,
        name: builtins.str,
        port: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        protocol: typing.Optional[builtins.str] = None,
        s_sl_info: typing.Optional[typing.Union["GoogleApigeeTargetServerSSlInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleApigeeTargetServerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server google_apigee_target_server} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param env_id: The Apigee environment group associated with the Apigee environment, in the format 'organizations/{{org_name}}/environments/{{env_name}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#env_id GoogleApigeeTargetServer#env_id}
        :param host: The host name this target connects to. Value must be a valid hostname as described by RFC-1123. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#host GoogleApigeeTargetServer#host}
        :param name: The resource id of this reference. Values must match the regular expression [\\w\\s-.]+. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#name GoogleApigeeTargetServer#name}
        :param port: The port number this target connects to on the given host. Value must be between 1 and 65535, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#port GoogleApigeeTargetServer#port}
        :param description: A human-readable description of this TargetServer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#description GoogleApigeeTargetServer#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#id GoogleApigeeTargetServer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_enabled: Enabling/disabling a TargetServer is useful when TargetServers are used in load balancing configurations, and one or more TargetServers need to taken out of rotation periodically. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#is_enabled GoogleApigeeTargetServer#is_enabled}
        :param protocol: Immutable. The protocol used by this TargetServer. Possible values: ["HTTP", "HTTP2", "GRPC_TARGET", "GRPC", "EXTERNAL_CALLOUT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#protocol GoogleApigeeTargetServer#protocol}
        :param s_sl_info: s_sl_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#s_sl_info GoogleApigeeTargetServer#s_sl_info}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#timeouts GoogleApigeeTargetServer#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__476ffd7d2ad278be67592050bffa65f282a28e08a14101b812f212308987eb44)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleApigeeTargetServerConfig(
            env_id=env_id,
            host=host,
            name=name,
            port=port,
            description=description,
            id=id,
            is_enabled=is_enabled,
            protocol=protocol,
            s_sl_info=s_sl_info,
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
        '''Generates CDKTF code for importing a GoogleApigeeTargetServer resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleApigeeTargetServer to import.
        :param import_from_id: The id of the existing GoogleApigeeTargetServer that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleApigeeTargetServer to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b06712460a69f99d42650413b477d6589e9b529d9475d25c0f3a6f6c8af7042)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSSlInfo")
    def put_s_sl_info(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        ciphers: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        common_name: typing.Optional[typing.Union["GoogleApigeeTargetServerSSlInfoCommonName", typing.Dict[builtins.str, typing.Any]]] = None,
        enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore_validation_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_alias: typing.Optional[builtins.str] = None,
        key_store: typing.Optional[builtins.str] = None,
        protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        trust_store: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Enables TLS. If false, neither one-way nor two-way TLS will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#enabled GoogleApigeeTargetServer#enabled}
        :param ciphers: The SSL/TLS cipher suites to be used. For programmable proxies, it must be one of the cipher suite names listed in: http://docs.oracle.com/javase/8/docs/technotes/guides/security/StandardNames.html#ciphersuites. For configurable proxies, it must follow the configuration specified in: https://commondatastorage.googleapis.com/chromium-boringssl-docs/ssl.h.html#Cipher-suite-configuration. This setting has no effect for configurable proxies when negotiating TLS 1.3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#ciphers GoogleApigeeTargetServer#ciphers}
        :param client_auth_enabled: Enables two-way TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#client_auth_enabled GoogleApigeeTargetServer#client_auth_enabled}
        :param common_name: common_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#common_name GoogleApigeeTargetServer#common_name}
        :param enforce: If true, TLS is strictly enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#enforce GoogleApigeeTargetServer#enforce}
        :param ignore_validation_errors: If true, Edge ignores TLS certificate errors. Valid when configuring TLS for target servers and target endpoints, and when configuring virtual hosts that use 2-way TLS. When used with a target endpoint/target server, if the backend system uses SNI and returns a cert with a subject Distinguished Name (DN) that does not match the hostname, there is no way to ignore the error and the connection fails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#ignore_validation_errors GoogleApigeeTargetServer#ignore_validation_errors}
        :param key_alias: Required if clientAuthEnabled is true. The resource ID for the alias containing the private key and cert. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#key_alias GoogleApigeeTargetServer#key_alias}
        :param key_store: Required if clientAuthEnabled is true. The resource ID of the keystore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#key_store GoogleApigeeTargetServer#key_store}
        :param protocols: The TLS versioins to be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#protocols GoogleApigeeTargetServer#protocols}
        :param trust_store: The resource ID of the truststore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#trust_store GoogleApigeeTargetServer#trust_store}
        '''
        value = GoogleApigeeTargetServerSSlInfo(
            enabled=enabled,
            ciphers=ciphers,
            client_auth_enabled=client_auth_enabled,
            common_name=common_name,
            enforce=enforce,
            ignore_validation_errors=ignore_validation_errors,
            key_alias=key_alias,
            key_store=key_store,
            protocols=protocols,
            trust_store=trust_store,
        )

        return typing.cast(None, jsii.invoke(self, "putSSlInfo", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#create GoogleApigeeTargetServer#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#delete GoogleApigeeTargetServer#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#update GoogleApigeeTargetServer#update}.
        '''
        value = GoogleApigeeTargetServerTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetSSlInfo")
    def reset_s_sl_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSSlInfo", []))

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
    @jsii.member(jsii_name="sSlInfo")
    def s_sl_info(self) -> "GoogleApigeeTargetServerSSlInfoOutputReference":
        return typing.cast("GoogleApigeeTargetServerSSlInfoOutputReference", jsii.get(self, "sSlInfo"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleApigeeTargetServerTimeoutsOutputReference":
        return typing.cast("GoogleApigeeTargetServerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="envIdInput")
    def env_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "envIdInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="sSlInfoInput")
    def s_sl_info_input(self) -> typing.Optional["GoogleApigeeTargetServerSSlInfo"]:
        return typing.cast(typing.Optional["GoogleApigeeTargetServerSSlInfo"], jsii.get(self, "sSlInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApigeeTargetServerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApigeeTargetServerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__107adaaef52eb4e10e69677408f3e0e0dcfd8c32050815b583537340abec6137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="envId")
    def env_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "envId"))

    @env_id.setter
    def env_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6afefd4e48c30b759a59fdb17c33e58dada6cade734aa5dc9634310e785a6fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "envId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b193b0284faaad7e73aa6bd01fd7331566d9105af16a61c421416c4a18bc8ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5e9307bf7cda0239eec8d86462fb75a9322c21c5724f7076c610a97b1c8d27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48cea43539544f3f1c073a16d52d29a94e39faef69f34c72c07095baa92830ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5df60ee624dde00b1147c0d71601eab94cec9c936a1aea445da5f8c037fa7113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24fea32516d5db70d8da9b936233bf393d7f0184422673500729b2edd1193e86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85a2624ebd2869ae9b0f657b3ee07c9298bbfc197d3a31bc3b32f17ec66c19e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeTargetServer.GoogleApigeeTargetServerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "env_id": "envId",
        "host": "host",
        "name": "name",
        "port": "port",
        "description": "description",
        "id": "id",
        "is_enabled": "isEnabled",
        "protocol": "protocol",
        "s_sl_info": "sSlInfo",
        "timeouts": "timeouts",
    },
)
class GoogleApigeeTargetServerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        env_id: builtins.str,
        host: builtins.str,
        name: builtins.str,
        port: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        protocol: typing.Optional[builtins.str] = None,
        s_sl_info: typing.Optional[typing.Union["GoogleApigeeTargetServerSSlInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleApigeeTargetServerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param env_id: The Apigee environment group associated with the Apigee environment, in the format 'organizations/{{org_name}}/environments/{{env_name}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#env_id GoogleApigeeTargetServer#env_id}
        :param host: The host name this target connects to. Value must be a valid hostname as described by RFC-1123. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#host GoogleApigeeTargetServer#host}
        :param name: The resource id of this reference. Values must match the regular expression [\\w\\s-.]+. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#name GoogleApigeeTargetServer#name}
        :param port: The port number this target connects to on the given host. Value must be between 1 and 65535, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#port GoogleApigeeTargetServer#port}
        :param description: A human-readable description of this TargetServer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#description GoogleApigeeTargetServer#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#id GoogleApigeeTargetServer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_enabled: Enabling/disabling a TargetServer is useful when TargetServers are used in load balancing configurations, and one or more TargetServers need to taken out of rotation periodically. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#is_enabled GoogleApigeeTargetServer#is_enabled}
        :param protocol: Immutable. The protocol used by this TargetServer. Possible values: ["HTTP", "HTTP2", "GRPC_TARGET", "GRPC", "EXTERNAL_CALLOUT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#protocol GoogleApigeeTargetServer#protocol}
        :param s_sl_info: s_sl_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#s_sl_info GoogleApigeeTargetServer#s_sl_info}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#timeouts GoogleApigeeTargetServer#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(s_sl_info, dict):
            s_sl_info = GoogleApigeeTargetServerSSlInfo(**s_sl_info)
        if isinstance(timeouts, dict):
            timeouts = GoogleApigeeTargetServerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36c9029369e37a94b65d793b561a40d5133af18a69da0e586d5ce232e902813a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument env_id", value=env_id, expected_type=type_hints["env_id"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument s_sl_info", value=s_sl_info, expected_type=type_hints["s_sl_info"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "env_id": env_id,
            "host": host,
            "name": name,
            "port": port,
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
        if id is not None:
            self._values["id"] = id
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if protocol is not None:
            self._values["protocol"] = protocol
        if s_sl_info is not None:
            self._values["s_sl_info"] = s_sl_info
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
    def env_id(self) -> builtins.str:
        '''The Apigee environment group associated with the Apigee environment, in the format 'organizations/{{org_name}}/environments/{{env_name}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#env_id GoogleApigeeTargetServer#env_id}
        '''
        result = self._values.get("env_id")
        assert result is not None, "Required property 'env_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''The host name this target connects to. Value must be a valid hostname as described by RFC-1123.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#host GoogleApigeeTargetServer#host}
        '''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource id of this reference. Values must match the regular expression [\\w\\s-.]+.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#name GoogleApigeeTargetServer#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port number this target connects to on the given host. Value must be between 1 and 65535, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#port GoogleApigeeTargetServer#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of this TargetServer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#description GoogleApigeeTargetServer#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#id GoogleApigeeTargetServer#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enabling/disabling a TargetServer is useful when TargetServers are used in load balancing configurations, and one or more TargetServers need to taken out of rotation periodically.

        Defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#is_enabled GoogleApigeeTargetServer#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Immutable. The protocol used by this TargetServer. Possible values: ["HTTP", "HTTP2", "GRPC_TARGET", "GRPC", "EXTERNAL_CALLOUT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#protocol GoogleApigeeTargetServer#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s_sl_info(self) -> typing.Optional["GoogleApigeeTargetServerSSlInfo"]:
        '''s_sl_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#s_sl_info GoogleApigeeTargetServer#s_sl_info}
        '''
        result = self._values.get("s_sl_info")
        return typing.cast(typing.Optional["GoogleApigeeTargetServerSSlInfo"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleApigeeTargetServerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#timeouts GoogleApigeeTargetServer#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleApigeeTargetServerTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeTargetServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeTargetServer.GoogleApigeeTargetServerSSlInfo",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "ciphers": "ciphers",
        "client_auth_enabled": "clientAuthEnabled",
        "common_name": "commonName",
        "enforce": "enforce",
        "ignore_validation_errors": "ignoreValidationErrors",
        "key_alias": "keyAlias",
        "key_store": "keyStore",
        "protocols": "protocols",
        "trust_store": "trustStore",
    },
)
class GoogleApigeeTargetServerSSlInfo:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        ciphers: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        common_name: typing.Optional[typing.Union["GoogleApigeeTargetServerSSlInfoCommonName", typing.Dict[builtins.str, typing.Any]]] = None,
        enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore_validation_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_alias: typing.Optional[builtins.str] = None,
        key_store: typing.Optional[builtins.str] = None,
        protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        trust_store: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Enables TLS. If false, neither one-way nor two-way TLS will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#enabled GoogleApigeeTargetServer#enabled}
        :param ciphers: The SSL/TLS cipher suites to be used. For programmable proxies, it must be one of the cipher suite names listed in: http://docs.oracle.com/javase/8/docs/technotes/guides/security/StandardNames.html#ciphersuites. For configurable proxies, it must follow the configuration specified in: https://commondatastorage.googleapis.com/chromium-boringssl-docs/ssl.h.html#Cipher-suite-configuration. This setting has no effect for configurable proxies when negotiating TLS 1.3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#ciphers GoogleApigeeTargetServer#ciphers}
        :param client_auth_enabled: Enables two-way TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#client_auth_enabled GoogleApigeeTargetServer#client_auth_enabled}
        :param common_name: common_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#common_name GoogleApigeeTargetServer#common_name}
        :param enforce: If true, TLS is strictly enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#enforce GoogleApigeeTargetServer#enforce}
        :param ignore_validation_errors: If true, Edge ignores TLS certificate errors. Valid when configuring TLS for target servers and target endpoints, and when configuring virtual hosts that use 2-way TLS. When used with a target endpoint/target server, if the backend system uses SNI and returns a cert with a subject Distinguished Name (DN) that does not match the hostname, there is no way to ignore the error and the connection fails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#ignore_validation_errors GoogleApigeeTargetServer#ignore_validation_errors}
        :param key_alias: Required if clientAuthEnabled is true. The resource ID for the alias containing the private key and cert. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#key_alias GoogleApigeeTargetServer#key_alias}
        :param key_store: Required if clientAuthEnabled is true. The resource ID of the keystore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#key_store GoogleApigeeTargetServer#key_store}
        :param protocols: The TLS versioins to be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#protocols GoogleApigeeTargetServer#protocols}
        :param trust_store: The resource ID of the truststore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#trust_store GoogleApigeeTargetServer#trust_store}
        '''
        if isinstance(common_name, dict):
            common_name = GoogleApigeeTargetServerSSlInfoCommonName(**common_name)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a921ddfe25e03fdb16f1b5063f8c4415bd0696fc54c1d211c372e60abbf6c187)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument ciphers", value=ciphers, expected_type=type_hints["ciphers"])
            check_type(argname="argument client_auth_enabled", value=client_auth_enabled, expected_type=type_hints["client_auth_enabled"])
            check_type(argname="argument common_name", value=common_name, expected_type=type_hints["common_name"])
            check_type(argname="argument enforce", value=enforce, expected_type=type_hints["enforce"])
            check_type(argname="argument ignore_validation_errors", value=ignore_validation_errors, expected_type=type_hints["ignore_validation_errors"])
            check_type(argname="argument key_alias", value=key_alias, expected_type=type_hints["key_alias"])
            check_type(argname="argument key_store", value=key_store, expected_type=type_hints["key_store"])
            check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
            check_type(argname="argument trust_store", value=trust_store, expected_type=type_hints["trust_store"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if ciphers is not None:
            self._values["ciphers"] = ciphers
        if client_auth_enabled is not None:
            self._values["client_auth_enabled"] = client_auth_enabled
        if common_name is not None:
            self._values["common_name"] = common_name
        if enforce is not None:
            self._values["enforce"] = enforce
        if ignore_validation_errors is not None:
            self._values["ignore_validation_errors"] = ignore_validation_errors
        if key_alias is not None:
            self._values["key_alias"] = key_alias
        if key_store is not None:
            self._values["key_store"] = key_store
        if protocols is not None:
            self._values["protocols"] = protocols
        if trust_store is not None:
            self._values["trust_store"] = trust_store

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Enables TLS. If false, neither one-way nor two-way TLS will be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#enabled GoogleApigeeTargetServer#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def ciphers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The SSL/TLS cipher suites to be used.

        For programmable proxies, it must be one of the cipher suite names listed in: http://docs.oracle.com/javase/8/docs/technotes/guides/security/StandardNames.html#ciphersuites. For configurable proxies, it must follow the configuration specified in: https://commondatastorage.googleapis.com/chromium-boringssl-docs/ssl.h.html#Cipher-suite-configuration. This setting has no effect for configurable proxies when negotiating TLS 1.3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#ciphers GoogleApigeeTargetServer#ciphers}
        '''
        result = self._values.get("ciphers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def client_auth_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables two-way TLS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#client_auth_enabled GoogleApigeeTargetServer#client_auth_enabled}
        '''
        result = self._values.get("client_auth_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def common_name(
        self,
    ) -> typing.Optional["GoogleApigeeTargetServerSSlInfoCommonName"]:
        '''common_name block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#common_name GoogleApigeeTargetServer#common_name}
        '''
        result = self._values.get("common_name")
        return typing.cast(typing.Optional["GoogleApigeeTargetServerSSlInfoCommonName"], result)

    @builtins.property
    def enforce(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, TLS is strictly enforced.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#enforce GoogleApigeeTargetServer#enforce}
        '''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ignore_validation_errors(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, Edge ignores TLS certificate errors.

        Valid when configuring TLS for target servers and target endpoints, and when configuring virtual hosts that use 2-way TLS. When used with a target endpoint/target server, if the backend system uses SNI and returns a cert with a subject Distinguished Name (DN) that does not match the hostname, there is no way to ignore the error and the connection fails.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#ignore_validation_errors GoogleApigeeTargetServer#ignore_validation_errors}
        '''
        result = self._values.get("ignore_validation_errors")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_alias(self) -> typing.Optional[builtins.str]:
        '''Required if clientAuthEnabled is true. The resource ID for the alias containing the private key and cert.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#key_alias GoogleApigeeTargetServer#key_alias}
        '''
        result = self._values.get("key_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_store(self) -> typing.Optional[builtins.str]:
        '''Required if clientAuthEnabled is true. The resource ID of the keystore.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#key_store GoogleApigeeTargetServer#key_store}
        '''
        result = self._values.get("key_store")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The TLS versioins to be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#protocols GoogleApigeeTargetServer#protocols}
        '''
        result = self._values.get("protocols")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def trust_store(self) -> typing.Optional[builtins.str]:
        '''The resource ID of the truststore.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#trust_store GoogleApigeeTargetServer#trust_store}
        '''
        result = self._values.get("trust_store")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeTargetServerSSlInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeTargetServer.GoogleApigeeTargetServerSSlInfoCommonName",
    jsii_struct_bases=[],
    name_mapping={"value": "value", "wildcard_match": "wildcardMatch"},
)
class GoogleApigeeTargetServerSSlInfoCommonName:
    def __init__(
        self,
        *,
        value: typing.Optional[builtins.str] = None,
        wildcard_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param value: The TLS Common Name string of the certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#value GoogleApigeeTargetServer#value}
        :param wildcard_match: Indicates whether the cert should be matched against as a wildcard cert. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#wildcard_match GoogleApigeeTargetServer#wildcard_match}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1b62b0d577c76a7664c862cafb6d6e3ac8e5e4f737fc4d3410c513f29986e69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument wildcard_match", value=wildcard_match, expected_type=type_hints["wildcard_match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value
        if wildcard_match is not None:
            self._values["wildcard_match"] = wildcard_match

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The TLS Common Name string of the certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#value GoogleApigeeTargetServer#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wildcard_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the cert should be matched against as a wildcard cert.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#wildcard_match GoogleApigeeTargetServer#wildcard_match}
        '''
        result = self._values.get("wildcard_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeTargetServerSSlInfoCommonName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeTargetServerSSlInfoCommonNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeTargetServer.GoogleApigeeTargetServerSSlInfoCommonNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ef8c7dffc3ac8d1bcb7258829ef820be60e0d5e73401a4b8e3738cc11210784)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @jsii.member(jsii_name="resetWildcardMatch")
    def reset_wildcard_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWildcardMatch", []))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="wildcardMatchInput")
    def wildcard_match_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "wildcardMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4c41aaecbce55723a817b6606146ba068a56ab2263681d04eb135b1340a7e29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wildcardMatch")
    def wildcard_match(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "wildcardMatch"))

    @wildcard_match.setter
    def wildcard_match(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5abaf66e309098a4cd4349c4b0295d904e202f40203f587b38f55d1a77b3b4b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wildcardMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeTargetServerSSlInfoCommonName]:
        return typing.cast(typing.Optional[GoogleApigeeTargetServerSSlInfoCommonName], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeTargetServerSSlInfoCommonName],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bca54787e689fd7ac9b16a1d54fce79ee5d56d9fb774a53ec60c60aef9b3b45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeTargetServerSSlInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeTargetServer.GoogleApigeeTargetServerSSlInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f86483b376fca8131755ff64fab11546334054c50a1f84239fed0eed3df5c2b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCommonName")
    def put_common_name(
        self,
        *,
        value: typing.Optional[builtins.str] = None,
        wildcard_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param value: The TLS Common Name string of the certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#value GoogleApigeeTargetServer#value}
        :param wildcard_match: Indicates whether the cert should be matched against as a wildcard cert. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#wildcard_match GoogleApigeeTargetServer#wildcard_match}
        '''
        value_ = GoogleApigeeTargetServerSSlInfoCommonName(
            value=value, wildcard_match=wildcard_match
        )

        return typing.cast(None, jsii.invoke(self, "putCommonName", [value_]))

    @jsii.member(jsii_name="resetCiphers")
    def reset_ciphers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCiphers", []))

    @jsii.member(jsii_name="resetClientAuthEnabled")
    def reset_client_auth_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientAuthEnabled", []))

    @jsii.member(jsii_name="resetCommonName")
    def reset_common_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommonName", []))

    @jsii.member(jsii_name="resetEnforce")
    def reset_enforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforce", []))

    @jsii.member(jsii_name="resetIgnoreValidationErrors")
    def reset_ignore_validation_errors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreValidationErrors", []))

    @jsii.member(jsii_name="resetKeyAlias")
    def reset_key_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyAlias", []))

    @jsii.member(jsii_name="resetKeyStore")
    def reset_key_store(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyStore", []))

    @jsii.member(jsii_name="resetProtocols")
    def reset_protocols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocols", []))

    @jsii.member(jsii_name="resetTrustStore")
    def reset_trust_store(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustStore", []))

    @builtins.property
    @jsii.member(jsii_name="commonName")
    def common_name(self) -> GoogleApigeeTargetServerSSlInfoCommonNameOutputReference:
        return typing.cast(GoogleApigeeTargetServerSSlInfoCommonNameOutputReference, jsii.get(self, "commonName"))

    @builtins.property
    @jsii.member(jsii_name="ciphersInput")
    def ciphers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ciphersInput"))

    @builtins.property
    @jsii.member(jsii_name="clientAuthEnabledInput")
    def client_auth_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "clientAuthEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="commonNameInput")
    def common_name_input(
        self,
    ) -> typing.Optional[GoogleApigeeTargetServerSSlInfoCommonName]:
        return typing.cast(typing.Optional[GoogleApigeeTargetServerSSlInfoCommonName], jsii.get(self, "commonNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreValidationErrorsInput")
    def ignore_validation_errors_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreValidationErrorsInput"))

    @builtins.property
    @jsii.member(jsii_name="keyAliasInput")
    def key_alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyAliasInput"))

    @builtins.property
    @jsii.member(jsii_name="keyStoreInput")
    def key_store_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolsInput")
    def protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "protocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="trustStoreInput")
    def trust_store_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trustStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="ciphers")
    def ciphers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ciphers"))

    @ciphers.setter
    def ciphers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b32310999493d6966a343e76f12d60e88e8633f7e02f483f09042d2ea401dad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ciphers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientAuthEnabled")
    def client_auth_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "clientAuthEnabled"))

    @client_auth_enabled.setter
    def client_auth_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73bc27ac3b58bdbad2a673d515bd9e20165cfb59ad2ebcb68665f6e5691bffcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientAuthEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494a715389374501bf79d70a4d65f6e85f797062c1c6189fededb63e7952c04a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforce")
    def enforce(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforce"))

    @enforce.setter
    def enforce(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8566ee10fe072c951f30c1c438b70da7203d10244217148a6c9c92d35255dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreValidationErrors")
    def ignore_validation_errors(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreValidationErrors"))

    @ignore_validation_errors.setter
    def ignore_validation_errors(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a929e96ffad7cd693a60fb4e5945b4499df12ca8e611091cb1b8c3d0882a0e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreValidationErrors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyAlias")
    def key_alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyAlias"))

    @key_alias.setter
    def key_alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19966ac53cf62a188a48a8c1655297940d1f3a9415fbef5f389c7969cf533b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyAlias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyStore")
    def key_store(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyStore"))

    @key_store.setter
    def key_store(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01b41fa68cbc666718698346476a199e60ecded3b0eb4c9a2b48f05ec34bb10e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyStore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocols")
    def protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "protocols"))

    @protocols.setter
    def protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b15aed15ec7ead427aecc45895095e6e97335c94bf009a467481555334b0f77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustStore")
    def trust_store(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustStore"))

    @trust_store.setter
    def trust_store(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c483537ad443433afff0d3983c0e7db094682650f2f0b46ab1452b7ae22d6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustStore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleApigeeTargetServerSSlInfo]:
        return typing.cast(typing.Optional[GoogleApigeeTargetServerSSlInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeTargetServerSSlInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa0afb8665aa0148122336b690d0a1c023dfc936d414a942d9be2929b2651076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeTargetServer.GoogleApigeeTargetServerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleApigeeTargetServerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#create GoogleApigeeTargetServer#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#delete GoogleApigeeTargetServer#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#update GoogleApigeeTargetServer#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30ba9c75563c404a3e2f30f3d009c3611cc353f0ce7b941ddb02b7fd28311004)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#create GoogleApigeeTargetServer#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#delete GoogleApigeeTargetServer#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_target_server#update GoogleApigeeTargetServer#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeTargetServerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeTargetServerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeTargetServer.GoogleApigeeTargetServerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__254c02c157fc41af99e5d3a116287730e41e044c771c25596d4f9768953a1dea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ef3fdefb3035f9a89effabab9fba0ad115847b3979840ddfe149c8a1b5955eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72776d96be9f4fc5d7b7faea4d2de1914fda897b718cd42ee4be5d071418157e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ecd030122d1b60a5909301188c0a5a0ff93d3ad3eb94fce43c4418e9d9ca72e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeTargetServerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeTargetServerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeTargetServerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ef8b0a64418f00c744469afad14a0b02c2e2bd7a89cfd833cd2dbddb07bcff9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleApigeeTargetServer",
    "GoogleApigeeTargetServerConfig",
    "GoogleApigeeTargetServerSSlInfo",
    "GoogleApigeeTargetServerSSlInfoCommonName",
    "GoogleApigeeTargetServerSSlInfoCommonNameOutputReference",
    "GoogleApigeeTargetServerSSlInfoOutputReference",
    "GoogleApigeeTargetServerTimeouts",
    "GoogleApigeeTargetServerTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__476ffd7d2ad278be67592050bffa65f282a28e08a14101b812f212308987eb44(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    env_id: builtins.str,
    host: builtins.str,
    name: builtins.str,
    port: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    protocol: typing.Optional[builtins.str] = None,
    s_sl_info: typing.Optional[typing.Union[GoogleApigeeTargetServerSSlInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleApigeeTargetServerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5b06712460a69f99d42650413b477d6589e9b529d9475d25c0f3a6f6c8af7042(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__107adaaef52eb4e10e69677408f3e0e0dcfd8c32050815b583537340abec6137(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6afefd4e48c30b759a59fdb17c33e58dada6cade734aa5dc9634310e785a6fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b193b0284faaad7e73aa6bd01fd7331566d9105af16a61c421416c4a18bc8ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5e9307bf7cda0239eec8d86462fb75a9322c21c5724f7076c610a97b1c8d27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48cea43539544f3f1c073a16d52d29a94e39faef69f34c72c07095baa92830ab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df60ee624dde00b1147c0d71601eab94cec9c936a1aea445da5f8c037fa7113(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24fea32516d5db70d8da9b936233bf393d7f0184422673500729b2edd1193e86(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a2624ebd2869ae9b0f657b3ee07c9298bbfc197d3a31bc3b32f17ec66c19e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c9029369e37a94b65d793b561a40d5133af18a69da0e586d5ce232e902813a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    env_id: builtins.str,
    host: builtins.str,
    name: builtins.str,
    port: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    protocol: typing.Optional[builtins.str] = None,
    s_sl_info: typing.Optional[typing.Union[GoogleApigeeTargetServerSSlInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleApigeeTargetServerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a921ddfe25e03fdb16f1b5063f8c4415bd0696fc54c1d211c372e60abbf6c187(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ciphers: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    common_name: typing.Optional[typing.Union[GoogleApigeeTargetServerSSlInfoCommonName, typing.Dict[builtins.str, typing.Any]]] = None,
    enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ignore_validation_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_alias: typing.Optional[builtins.str] = None,
    key_store: typing.Optional[builtins.str] = None,
    protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    trust_store: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b62b0d577c76a7664c862cafb6d6e3ac8e5e4f737fc4d3410c513f29986e69(
    *,
    value: typing.Optional[builtins.str] = None,
    wildcard_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef8c7dffc3ac8d1bcb7258829ef820be60e0d5e73401a4b8e3738cc11210784(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4c41aaecbce55723a817b6606146ba068a56ab2263681d04eb135b1340a7e29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5abaf66e309098a4cd4349c4b0295d904e202f40203f587b38f55d1a77b3b4b6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bca54787e689fd7ac9b16a1d54fce79ee5d56d9fb774a53ec60c60aef9b3b45(
    value: typing.Optional[GoogleApigeeTargetServerSSlInfoCommonName],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f86483b376fca8131755ff64fab11546334054c50a1f84239fed0eed3df5c2b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b32310999493d6966a343e76f12d60e88e8633f7e02f483f09042d2ea401dad(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73bc27ac3b58bdbad2a673d515bd9e20165cfb59ad2ebcb68665f6e5691bffcf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494a715389374501bf79d70a4d65f6e85f797062c1c6189fededb63e7952c04a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8566ee10fe072c951f30c1c438b70da7203d10244217148a6c9c92d35255dfc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a929e96ffad7cd693a60fb4e5945b4499df12ca8e611091cb1b8c3d0882a0e3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19966ac53cf62a188a48a8c1655297940d1f3a9415fbef5f389c7969cf533b31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b41fa68cbc666718698346476a199e60ecded3b0eb4c9a2b48f05ec34bb10e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b15aed15ec7ead427aecc45895095e6e97335c94bf009a467481555334b0f77(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c483537ad443433afff0d3983c0e7db094682650f2f0b46ab1452b7ae22d6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0afb8665aa0148122336b690d0a1c023dfc936d414a942d9be2929b2651076(
    value: typing.Optional[GoogleApigeeTargetServerSSlInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ba9c75563c404a3e2f30f3d009c3611cc353f0ce7b941ddb02b7fd28311004(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__254c02c157fc41af99e5d3a116287730e41e044c771c25596d4f9768953a1dea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef3fdefb3035f9a89effabab9fba0ad115847b3979840ddfe149c8a1b5955eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72776d96be9f4fc5d7b7faea4d2de1914fda897b718cd42ee4be5d071418157e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ecd030122d1b60a5909301188c0a5a0ff93d3ad3eb94fce43c4418e9d9ca72e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef8b0a64418f00c744469afad14a0b02c2e2bd7a89cfd833cd2dbddb07bcff9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeTargetServerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

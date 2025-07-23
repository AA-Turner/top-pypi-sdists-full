r'''
# `google_apigee_target_server`

Refer to the Terraform Registry for docs: [`google_apigee_target_server`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server).
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


class ApigeeTargetServer(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeTargetServer.ApigeeTargetServer",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server google_apigee_target_server}.'''

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
        s_sl_info: typing.Optional[typing.Union["ApigeeTargetServerSSlInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ApigeeTargetServerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server google_apigee_target_server} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param env_id: The Apigee environment group associated with the Apigee environment, in the format 'organizations/{{org_name}}/environments/{{env_name}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#env_id ApigeeTargetServer#env_id}
        :param host: The host name this target connects to. Value must be a valid hostname as described by RFC-1123. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#host ApigeeTargetServer#host}
        :param name: The resource id of this reference. Values must match the regular expression [\\w\\s-.]+. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#name ApigeeTargetServer#name}
        :param port: The port number this target connects to on the given host. Value must be between 1 and 65535, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#port ApigeeTargetServer#port}
        :param description: A human-readable description of this TargetServer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#description ApigeeTargetServer#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#id ApigeeTargetServer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_enabled: Enabling/disabling a TargetServer is useful when TargetServers are used in load balancing configurations, and one or more TargetServers need to taken out of rotation periodically. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#is_enabled ApigeeTargetServer#is_enabled}
        :param protocol: Immutable. The protocol used by this TargetServer. Possible values: ["HTTP", "HTTP2", "GRPC_TARGET", "GRPC", "EXTERNAL_CALLOUT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#protocol ApigeeTargetServer#protocol}
        :param s_sl_info: s_sl_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#s_sl_info ApigeeTargetServer#s_sl_info}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#timeouts ApigeeTargetServer#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67bc815922c8fa3f7494d1694759959bb76a834be648dde6892028d42b55ce24)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApigeeTargetServerConfig(
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
        '''Generates CDKTF code for importing a ApigeeTargetServer resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApigeeTargetServer to import.
        :param import_from_id: The id of the existing ApigeeTargetServer that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApigeeTargetServer to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75737feaac97b3f5086174cdd2fa9deec87985bbcf813fe46488edfebfe1ca17)
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
        common_name: typing.Optional[typing.Union["ApigeeTargetServerSSlInfoCommonName", typing.Dict[builtins.str, typing.Any]]] = None,
        enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore_validation_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_alias: typing.Optional[builtins.str] = None,
        key_store: typing.Optional[builtins.str] = None,
        protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        trust_store: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Enables TLS. If false, neither one-way nor two-way TLS will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#enabled ApigeeTargetServer#enabled}
        :param ciphers: The SSL/TLS cipher suites to be used. For programmable proxies, it must be one of the cipher suite names listed in: http://docs.oracle.com/javase/8/docs/technotes/guides/security/StandardNames.html#ciphersuites. For configurable proxies, it must follow the configuration specified in: https://commondatastorage.googleapis.com/chromium-boringssl-docs/ssl.h.html#Cipher-suite-configuration. This setting has no effect for configurable proxies when negotiating TLS 1.3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#ciphers ApigeeTargetServer#ciphers}
        :param client_auth_enabled: Enables two-way TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#client_auth_enabled ApigeeTargetServer#client_auth_enabled}
        :param common_name: common_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#common_name ApigeeTargetServer#common_name}
        :param enforce: If true, TLS is strictly enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#enforce ApigeeTargetServer#enforce}
        :param ignore_validation_errors: If true, Edge ignores TLS certificate errors. Valid when configuring TLS for target servers and target endpoints, and when configuring virtual hosts that use 2-way TLS. When used with a target endpoint/target server, if the backend system uses SNI and returns a cert with a subject Distinguished Name (DN) that does not match the hostname, there is no way to ignore the error and the connection fails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#ignore_validation_errors ApigeeTargetServer#ignore_validation_errors}
        :param key_alias: Required if clientAuthEnabled is true. The resource ID for the alias containing the private key and cert. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#key_alias ApigeeTargetServer#key_alias}
        :param key_store: Required if clientAuthEnabled is true. The resource ID of the keystore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#key_store ApigeeTargetServer#key_store}
        :param protocols: The TLS versioins to be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#protocols ApigeeTargetServer#protocols}
        :param trust_store: The resource ID of the truststore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#trust_store ApigeeTargetServer#trust_store}
        '''
        value = ApigeeTargetServerSSlInfo(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#create ApigeeTargetServer#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#delete ApigeeTargetServer#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#update ApigeeTargetServer#update}.
        '''
        value = ApigeeTargetServerTimeouts(create=create, delete=delete, update=update)

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
    def s_sl_info(self) -> "ApigeeTargetServerSSlInfoOutputReference":
        return typing.cast("ApigeeTargetServerSSlInfoOutputReference", jsii.get(self, "sSlInfo"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApigeeTargetServerTimeoutsOutputReference":
        return typing.cast("ApigeeTargetServerTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def s_sl_info_input(self) -> typing.Optional["ApigeeTargetServerSSlInfo"]:
        return typing.cast(typing.Optional["ApigeeTargetServerSSlInfo"], jsii.get(self, "sSlInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigeeTargetServerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigeeTargetServerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97c1b58a79458a5e0187d4d6ba0f44e5059bd020c3101ca9259f2ed632f43141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="envId")
    def env_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "envId"))

    @env_id.setter
    def env_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39d9c613bc94d75c44b49d1c372e7e1f5291451aaa89a6a8ae7cdf5ff41cae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "envId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed619f105cdf8fe98225345f9876a8aab5107cc5c008390b14f7ba330f3fd4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef462762eb7cf8c597150eecd2de5f74e74cdaf578d5fcdab44d393e87d87091)
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
            type_hints = typing.get_type_hints(_typecheckingstub__107c550a4d5b07c74f843bd2c67b1808b3837be18f902604bc28c454a0b9e567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea32426a1b5535e43454a69c98d8965107032d73c8b509e1d10437ea66ae9a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fba9a2700527de6bf7ece3e6749b17ac4a157440dc76b3802fa41681b2431b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__defaf71fba49ba9f7603fa99b3533ce2ce9df6c7ec331dbcc55b03378456e12d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeTargetServer.ApigeeTargetServerConfig",
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
class ApigeeTargetServerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        s_sl_info: typing.Optional[typing.Union["ApigeeTargetServerSSlInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ApigeeTargetServerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param env_id: The Apigee environment group associated with the Apigee environment, in the format 'organizations/{{org_name}}/environments/{{env_name}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#env_id ApigeeTargetServer#env_id}
        :param host: The host name this target connects to. Value must be a valid hostname as described by RFC-1123. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#host ApigeeTargetServer#host}
        :param name: The resource id of this reference. Values must match the regular expression [\\w\\s-.]+. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#name ApigeeTargetServer#name}
        :param port: The port number this target connects to on the given host. Value must be between 1 and 65535, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#port ApigeeTargetServer#port}
        :param description: A human-readable description of this TargetServer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#description ApigeeTargetServer#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#id ApigeeTargetServer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_enabled: Enabling/disabling a TargetServer is useful when TargetServers are used in load balancing configurations, and one or more TargetServers need to taken out of rotation periodically. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#is_enabled ApigeeTargetServer#is_enabled}
        :param protocol: Immutable. The protocol used by this TargetServer. Possible values: ["HTTP", "HTTP2", "GRPC_TARGET", "GRPC", "EXTERNAL_CALLOUT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#protocol ApigeeTargetServer#protocol}
        :param s_sl_info: s_sl_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#s_sl_info ApigeeTargetServer#s_sl_info}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#timeouts ApigeeTargetServer#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(s_sl_info, dict):
            s_sl_info = ApigeeTargetServerSSlInfo(**s_sl_info)
        if isinstance(timeouts, dict):
            timeouts = ApigeeTargetServerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ced43021476e0ae97e83951bacf3e163f4ffe7cb007e9013e1889c2a85935ad)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#env_id ApigeeTargetServer#env_id}
        '''
        result = self._values.get("env_id")
        assert result is not None, "Required property 'env_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''The host name this target connects to. Value must be a valid hostname as described by RFC-1123.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#host ApigeeTargetServer#host}
        '''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource id of this reference. Values must match the regular expression [\\w\\s-.]+.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#name ApigeeTargetServer#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port number this target connects to on the given host. Value must be between 1 and 65535, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#port ApigeeTargetServer#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of this TargetServer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#description ApigeeTargetServer#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#id ApigeeTargetServer#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#is_enabled ApigeeTargetServer#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Immutable. The protocol used by this TargetServer. Possible values: ["HTTP", "HTTP2", "GRPC_TARGET", "GRPC", "EXTERNAL_CALLOUT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#protocol ApigeeTargetServer#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s_sl_info(self) -> typing.Optional["ApigeeTargetServerSSlInfo"]:
        '''s_sl_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#s_sl_info ApigeeTargetServer#s_sl_info}
        '''
        result = self._values.get("s_sl_info")
        return typing.cast(typing.Optional["ApigeeTargetServerSSlInfo"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApigeeTargetServerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#timeouts ApigeeTargetServer#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApigeeTargetServerTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeTargetServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeTargetServer.ApigeeTargetServerSSlInfo",
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
class ApigeeTargetServerSSlInfo:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        ciphers: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        common_name: typing.Optional[typing.Union["ApigeeTargetServerSSlInfoCommonName", typing.Dict[builtins.str, typing.Any]]] = None,
        enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore_validation_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_alias: typing.Optional[builtins.str] = None,
        key_store: typing.Optional[builtins.str] = None,
        protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        trust_store: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Enables TLS. If false, neither one-way nor two-way TLS will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#enabled ApigeeTargetServer#enabled}
        :param ciphers: The SSL/TLS cipher suites to be used. For programmable proxies, it must be one of the cipher suite names listed in: http://docs.oracle.com/javase/8/docs/technotes/guides/security/StandardNames.html#ciphersuites. For configurable proxies, it must follow the configuration specified in: https://commondatastorage.googleapis.com/chromium-boringssl-docs/ssl.h.html#Cipher-suite-configuration. This setting has no effect for configurable proxies when negotiating TLS 1.3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#ciphers ApigeeTargetServer#ciphers}
        :param client_auth_enabled: Enables two-way TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#client_auth_enabled ApigeeTargetServer#client_auth_enabled}
        :param common_name: common_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#common_name ApigeeTargetServer#common_name}
        :param enforce: If true, TLS is strictly enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#enforce ApigeeTargetServer#enforce}
        :param ignore_validation_errors: If true, Edge ignores TLS certificate errors. Valid when configuring TLS for target servers and target endpoints, and when configuring virtual hosts that use 2-way TLS. When used with a target endpoint/target server, if the backend system uses SNI and returns a cert with a subject Distinguished Name (DN) that does not match the hostname, there is no way to ignore the error and the connection fails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#ignore_validation_errors ApigeeTargetServer#ignore_validation_errors}
        :param key_alias: Required if clientAuthEnabled is true. The resource ID for the alias containing the private key and cert. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#key_alias ApigeeTargetServer#key_alias}
        :param key_store: Required if clientAuthEnabled is true. The resource ID of the keystore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#key_store ApigeeTargetServer#key_store}
        :param protocols: The TLS versioins to be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#protocols ApigeeTargetServer#protocols}
        :param trust_store: The resource ID of the truststore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#trust_store ApigeeTargetServer#trust_store}
        '''
        if isinstance(common_name, dict):
            common_name = ApigeeTargetServerSSlInfoCommonName(**common_name)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ee81d3fac026e605233b8c859302198b72fb723c6c960adf652901b7e91ec0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#enabled ApigeeTargetServer#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def ciphers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The SSL/TLS cipher suites to be used.

        For programmable proxies, it must be one of the cipher suite names listed in: http://docs.oracle.com/javase/8/docs/technotes/guides/security/StandardNames.html#ciphersuites. For configurable proxies, it must follow the configuration specified in: https://commondatastorage.googleapis.com/chromium-boringssl-docs/ssl.h.html#Cipher-suite-configuration. This setting has no effect for configurable proxies when negotiating TLS 1.3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#ciphers ApigeeTargetServer#ciphers}
        '''
        result = self._values.get("ciphers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def client_auth_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables two-way TLS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#client_auth_enabled ApigeeTargetServer#client_auth_enabled}
        '''
        result = self._values.get("client_auth_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def common_name(self) -> typing.Optional["ApigeeTargetServerSSlInfoCommonName"]:
        '''common_name block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#common_name ApigeeTargetServer#common_name}
        '''
        result = self._values.get("common_name")
        return typing.cast(typing.Optional["ApigeeTargetServerSSlInfoCommonName"], result)

    @builtins.property
    def enforce(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, TLS is strictly enforced.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#enforce ApigeeTargetServer#enforce}
        '''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ignore_validation_errors(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, Edge ignores TLS certificate errors.

        Valid when configuring TLS for target servers and target endpoints, and when configuring virtual hosts that use 2-way TLS. When used with a target endpoint/target server, if the backend system uses SNI and returns a cert with a subject Distinguished Name (DN) that does not match the hostname, there is no way to ignore the error and the connection fails.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#ignore_validation_errors ApigeeTargetServer#ignore_validation_errors}
        '''
        result = self._values.get("ignore_validation_errors")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_alias(self) -> typing.Optional[builtins.str]:
        '''Required if clientAuthEnabled is true. The resource ID for the alias containing the private key and cert.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#key_alias ApigeeTargetServer#key_alias}
        '''
        result = self._values.get("key_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_store(self) -> typing.Optional[builtins.str]:
        '''Required if clientAuthEnabled is true. The resource ID of the keystore.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#key_store ApigeeTargetServer#key_store}
        '''
        result = self._values.get("key_store")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The TLS versioins to be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#protocols ApigeeTargetServer#protocols}
        '''
        result = self._values.get("protocols")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def trust_store(self) -> typing.Optional[builtins.str]:
        '''The resource ID of the truststore.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#trust_store ApigeeTargetServer#trust_store}
        '''
        result = self._values.get("trust_store")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeTargetServerSSlInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeTargetServer.ApigeeTargetServerSSlInfoCommonName",
    jsii_struct_bases=[],
    name_mapping={"value": "value", "wildcard_match": "wildcardMatch"},
)
class ApigeeTargetServerSSlInfoCommonName:
    def __init__(
        self,
        *,
        value: typing.Optional[builtins.str] = None,
        wildcard_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param value: The TLS Common Name string of the certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#value ApigeeTargetServer#value}
        :param wildcard_match: Indicates whether the cert should be matched against as a wildcard cert. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#wildcard_match ApigeeTargetServer#wildcard_match}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed169680f78b2cb1a14d0a23b1932f5bdb9f50908017f91495be8032b83792d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#value ApigeeTargetServer#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wildcard_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the cert should be matched against as a wildcard cert.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#wildcard_match ApigeeTargetServer#wildcard_match}
        '''
        result = self._values.get("wildcard_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeTargetServerSSlInfoCommonName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeTargetServerSSlInfoCommonNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeTargetServer.ApigeeTargetServerSSlInfoCommonNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c74534549b770f8552fbbef1b2ac6ee3df9827e8bee3e70451fc86c9692d13d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6423ee175f175ca1b5a2c0cb886c53553d0e5ddab289e9e30885fcde61622a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__121492a26d4d5fefd9267e11319acf5655602d8faadaf890da5e45466eb612b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wildcardMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigeeTargetServerSSlInfoCommonName]:
        return typing.cast(typing.Optional[ApigeeTargetServerSSlInfoCommonName], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeTargetServerSSlInfoCommonName],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d28e80bc1f9dff9bedcd63842693aba1cec71fdbf5c3109292599d103c290499)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeTargetServerSSlInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeTargetServer.ApigeeTargetServerSSlInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76cdfb45da59be07ee2cdee793e789bcefe89d3e0a410fc2f70cdc607bc9cc5b)
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
        :param value: The TLS Common Name string of the certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#value ApigeeTargetServer#value}
        :param wildcard_match: Indicates whether the cert should be matched against as a wildcard cert. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#wildcard_match ApigeeTargetServer#wildcard_match}
        '''
        value_ = ApigeeTargetServerSSlInfoCommonName(
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
    def common_name(self) -> ApigeeTargetServerSSlInfoCommonNameOutputReference:
        return typing.cast(ApigeeTargetServerSSlInfoCommonNameOutputReference, jsii.get(self, "commonName"))

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
    def common_name_input(self) -> typing.Optional[ApigeeTargetServerSSlInfoCommonName]:
        return typing.cast(typing.Optional[ApigeeTargetServerSSlInfoCommonName], jsii.get(self, "commonNameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a016dfc3e68318b25a1684ca129de34faa372524ba72896b788b02972c5d693d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__630483ca1f050c7973f32ecc98184e861c7fd3a6876bcac7eb4be9c6e64c9793)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e22e22ecc7fbd150d1db47897768e177ba5fda9c19a001106e1b396c86e20c5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a4ff3e95e3cc8088a0e99ca0a1b01f7fb81a2f161157d9a3ca329d8f30d736a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0688a510748c20f0b283b92921a151e8f83dd7343c7a300195522d4cc89df5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreValidationErrors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyAlias")
    def key_alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyAlias"))

    @key_alias.setter
    def key_alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64f8c4e5f63336e63cb32e74623b7c824c783c24220c89c474c768c75de5240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyAlias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyStore")
    def key_store(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyStore"))

    @key_store.setter
    def key_store(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__046add6880e67f2f562b5ddbb0c610b11f855ddf581fc02e9af6b9b8b21f0109)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyStore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocols")
    def protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "protocols"))

    @protocols.setter
    def protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__747941e7241c571bd567d4f668d49704a6f81acdcaf38c55e1e544825d1d53e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustStore")
    def trust_store(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustStore"))

    @trust_store.setter
    def trust_store(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a505ee95bcd499682f3e2aec69199db38f8f8b2f3c328aca3951a606bf7a7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustStore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigeeTargetServerSSlInfo]:
        return typing.cast(typing.Optional[ApigeeTargetServerSSlInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApigeeTargetServerSSlInfo]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4998eac40b0ad7ebd0001bb770d8141f1b57da0ed493e657737015e69eb0120b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeTargetServer.ApigeeTargetServerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ApigeeTargetServerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#create ApigeeTargetServer#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#delete ApigeeTargetServer#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#update ApigeeTargetServer#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bec7325f52632d287ed2a8264de4f646f86c662be3fe408b3176daf2246c038)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#create ApigeeTargetServer#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#delete ApigeeTargetServer#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_target_server#update ApigeeTargetServer#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeTargetServerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeTargetServerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeTargetServer.ApigeeTargetServerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d0d3c7a0dd47b410f2095172587f3095c212165964c0c7eac4bbc16bdfe2935)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8507d144cdff38c08eac8db982bdf18e4fc6d5150476cf081828e9079fea796e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf56be1ec8854288acdd84f61edb9d4a60149c5d2394f1b1ba7d4cca73c15105)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2011c6efa5d0212c3774cc72ddfafd3e58ae3d93f033a8d535d123b3b321488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeTargetServerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeTargetServerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeTargetServerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c67026a8f3241f121fc4204174633bbb14334d9907bc4d1471524bf00d158ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApigeeTargetServer",
    "ApigeeTargetServerConfig",
    "ApigeeTargetServerSSlInfo",
    "ApigeeTargetServerSSlInfoCommonName",
    "ApigeeTargetServerSSlInfoCommonNameOutputReference",
    "ApigeeTargetServerSSlInfoOutputReference",
    "ApigeeTargetServerTimeouts",
    "ApigeeTargetServerTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__67bc815922c8fa3f7494d1694759959bb76a834be648dde6892028d42b55ce24(
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
    s_sl_info: typing.Optional[typing.Union[ApigeeTargetServerSSlInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ApigeeTargetServerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__75737feaac97b3f5086174cdd2fa9deec87985bbcf813fe46488edfebfe1ca17(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c1b58a79458a5e0187d4d6ba0f44e5059bd020c3101ca9259f2ed632f43141(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39d9c613bc94d75c44b49d1c372e7e1f5291451aaa89a6a8ae7cdf5ff41cae2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed619f105cdf8fe98225345f9876a8aab5107cc5c008390b14f7ba330f3fd4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef462762eb7cf8c597150eecd2de5f74e74cdaf578d5fcdab44d393e87d87091(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__107c550a4d5b07c74f843bd2c67b1808b3837be18f902604bc28c454a0b9e567(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea32426a1b5535e43454a69c98d8965107032d73c8b509e1d10437ea66ae9a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fba9a2700527de6bf7ece3e6749b17ac4a157440dc76b3802fa41681b2431b0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__defaf71fba49ba9f7603fa99b3533ce2ce9df6c7ec331dbcc55b03378456e12d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ced43021476e0ae97e83951bacf3e163f4ffe7cb007e9013e1889c2a85935ad(
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
    s_sl_info: typing.Optional[typing.Union[ApigeeTargetServerSSlInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ApigeeTargetServerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ee81d3fac026e605233b8c859302198b72fb723c6c960adf652901b7e91ec0(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ciphers: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    common_name: typing.Optional[typing.Union[ApigeeTargetServerSSlInfoCommonName, typing.Dict[builtins.str, typing.Any]]] = None,
    enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ignore_validation_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_alias: typing.Optional[builtins.str] = None,
    key_store: typing.Optional[builtins.str] = None,
    protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    trust_store: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed169680f78b2cb1a14d0a23b1932f5bdb9f50908017f91495be8032b83792d(
    *,
    value: typing.Optional[builtins.str] = None,
    wildcard_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74534549b770f8552fbbef1b2ac6ee3df9827e8bee3e70451fc86c9692d13d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6423ee175f175ca1b5a2c0cb886c53553d0e5ddab289e9e30885fcde61622a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__121492a26d4d5fefd9267e11319acf5655602d8faadaf890da5e45466eb612b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28e80bc1f9dff9bedcd63842693aba1cec71fdbf5c3109292599d103c290499(
    value: typing.Optional[ApigeeTargetServerSSlInfoCommonName],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76cdfb45da59be07ee2cdee793e789bcefe89d3e0a410fc2f70cdc607bc9cc5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a016dfc3e68318b25a1684ca129de34faa372524ba72896b788b02972c5d693d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630483ca1f050c7973f32ecc98184e861c7fd3a6876bcac7eb4be9c6e64c9793(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22e22ecc7fbd150d1db47897768e177ba5fda9c19a001106e1b396c86e20c5a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4ff3e95e3cc8088a0e99ca0a1b01f7fb81a2f161157d9a3ca329d8f30d736a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0688a510748c20f0b283b92921a151e8f83dd7343c7a300195522d4cc89df5c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64f8c4e5f63336e63cb32e74623b7c824c783c24220c89c474c768c75de5240(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046add6880e67f2f562b5ddbb0c610b11f855ddf581fc02e9af6b9b8b21f0109(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__747941e7241c571bd567d4f668d49704a6f81acdcaf38c55e1e544825d1d53e8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a505ee95bcd499682f3e2aec69199db38f8f8b2f3c328aca3951a606bf7a7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4998eac40b0ad7ebd0001bb770d8141f1b57da0ed493e657737015e69eb0120b(
    value: typing.Optional[ApigeeTargetServerSSlInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bec7325f52632d287ed2a8264de4f646f86c662be3fe408b3176daf2246c038(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d0d3c7a0dd47b410f2095172587f3095c212165964c0c7eac4bbc16bdfe2935(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8507d144cdff38c08eac8db982bdf18e4fc6d5150476cf081828e9079fea796e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf56be1ec8854288acdd84f61edb9d4a60149c5d2394f1b1ba7d4cca73c15105(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2011c6efa5d0212c3774cc72ddfafd3e58ae3d93f033a8d535d123b3b321488(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c67026a8f3241f121fc4204174633bbb14334d9907bc4d1471524bf00d158ac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeTargetServerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

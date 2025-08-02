r'''
# `opentelekomcloud_waf_domain_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_waf_domain_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1).
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


class WafDomainV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDomainV1.WafDomainV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1 opentelekomcloud_waf_domain_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        hostname: builtins.str,
        proxy: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        server: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDomainV1Server", typing.Dict[builtins.str, typing.Any]]]],
        block_page: typing.Optional[typing.Union["WafDomainV1BlockPage", typing.Dict[builtins.str, typing.Any]]] = None,
        certificate_id: typing.Optional[builtins.str] = None,
        cipher: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        policy_id: typing.Optional[builtins.str] = None,
        sip_header_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        sip_header_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["WafDomainV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1 opentelekomcloud_waf_domain_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#hostname WafDomainV1#hostname}.
        :param proxy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#proxy WafDomainV1#proxy}.
        :param server: server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#server WafDomainV1#server}
        :param block_page: block_page block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#block_page WafDomainV1#block_page}
        :param certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#certificate_id WafDomainV1#certificate_id}.
        :param cipher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#cipher WafDomainV1#cipher}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#id WafDomainV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#policy_id WafDomainV1#policy_id}.
        :param sip_header_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#sip_header_list WafDomainV1#sip_header_list}.
        :param sip_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#sip_header_name WafDomainV1#sip_header_name}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#timeouts WafDomainV1#timeouts}
        :param tls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#tls WafDomainV1#tls}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__355667572a91664231d0f373bf96c73fb4a40e42111f3fa0f109684e5f2f7524)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WafDomainV1Config(
            hostname=hostname,
            proxy=proxy,
            server=server,
            block_page=block_page,
            certificate_id=certificate_id,
            cipher=cipher,
            id=id,
            policy_id=policy_id,
            sip_header_list=sip_header_list,
            sip_header_name=sip_header_name,
            timeouts=timeouts,
            tls=tls,
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
        '''Generates CDKTF code for importing a WafDomainV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WafDomainV1 to import.
        :param import_from_id: The id of the existing WafDomainV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WafDomainV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe4867a3b77e79a9ebf19734bb4cfd0731ddf49c7a00840128241526b5ee8b7e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBlockPage")
    def put_block_page(
        self,
        *,
        template: builtins.str,
        content: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        redirect_url: typing.Optional[builtins.str] = None,
        status_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#template WafDomainV1#template}.
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#content WafDomainV1#content}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#content_type WafDomainV1#content_type}.
        :param redirect_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#redirect_url WafDomainV1#redirect_url}.
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#status_code WafDomainV1#status_code}.
        '''
        value = WafDomainV1BlockPage(
            template=template,
            content=content,
            content_type=content_type,
            redirect_url=redirect_url,
            status_code=status_code,
        )

        return typing.cast(None, jsii.invoke(self, "putBlockPage", [value]))

    @jsii.member(jsii_name="putServer")
    def put_server(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDomainV1Server", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d90655c5c57981e5a1bcc2b0af3fb1eda0bcabf091157ae354416bff3a849300)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServer", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#create WafDomainV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#delete WafDomainV1#delete}.
        '''
        value = WafDomainV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBlockPage")
    def reset_block_page(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockPage", []))

    @jsii.member(jsii_name="resetCertificateId")
    def reset_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateId", []))

    @jsii.member(jsii_name="resetCipher")
    def reset_cipher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCipher", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPolicyId")
    def reset_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyId", []))

    @jsii.member(jsii_name="resetSipHeaderList")
    def reset_sip_header_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSipHeaderList", []))

    @jsii.member(jsii_name="resetSipHeaderName")
    def reset_sip_header_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSipHeaderName", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTls")
    def reset_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTls", []))

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
    @jsii.member(jsii_name="accessCode")
    def access_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessCode"))

    @builtins.property
    @jsii.member(jsii_name="accessStatus")
    def access_status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accessStatus"))

    @builtins.property
    @jsii.member(jsii_name="blockPage")
    def block_page(self) -> "WafDomainV1BlockPageOutputReference":
        return typing.cast("WafDomainV1BlockPageOutputReference", jsii.get(self, "blockPage"))

    @builtins.property
    @jsii.member(jsii_name="cname")
    def cname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cname"))

    @builtins.property
    @jsii.member(jsii_name="protectStatus")
    def protect_status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "protectStatus"))

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> "WafDomainV1ServerList":
        return typing.cast("WafDomainV1ServerList", jsii.get(self, "server"))

    @builtins.property
    @jsii.member(jsii_name="subDomain")
    def sub_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subDomain"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "WafDomainV1TimeoutsOutputReference":
        return typing.cast("WafDomainV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="txtCode")
    def txt_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "txtCode"))

    @builtins.property
    @jsii.member(jsii_name="blockPageInput")
    def block_page_input(self) -> typing.Optional["WafDomainV1BlockPage"]:
        return typing.cast(typing.Optional["WafDomainV1BlockPage"], jsii.get(self, "blockPageInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateIdInput")
    def certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cipherInput")
    def cipher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cipherInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyInput")
    def proxy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "proxyInput"))

    @builtins.property
    @jsii.member(jsii_name="serverInput")
    def server_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDomainV1Server"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDomainV1Server"]]], jsii.get(self, "serverInput"))

    @builtins.property
    @jsii.member(jsii_name="sipHeaderListInput")
    def sip_header_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sipHeaderListInput"))

    @builtins.property
    @jsii.member(jsii_name="sipHeaderNameInput")
    def sip_header_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sipHeaderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WafDomainV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WafDomainV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsInput")
    def tls_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateId")
    def certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateId"))

    @certificate_id.setter
    def certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__130da73924bc144ebd596eafd30c548cf3e63769b80572aaa724f110e14e9a52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cipher")
    def cipher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cipher"))

    @cipher.setter
    def cipher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7446aca65ec1b474b8dd6cf45e5fbff2c9c75b0bd40e6a7d791b1a7ce7fd7b44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cipher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08df57b9c560bafd9492040141abd88fe1f6fa0812de0b2ff37ad577c99020b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69df74e4b517cd2e63a7135fc18e55886fd075f52c871c3e8ce26c32e8336f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c52f2a22b1046afaf01aa53a7886f5575a1186a95c9b8bcedede53c843cb5e5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxy")
    def proxy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "proxy"))

    @proxy.setter
    def proxy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d2019c0fff694dfe55e6918749de13e0ad53586654ba2032bddd7c3aa67aabc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sipHeaderList")
    def sip_header_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sipHeaderList"))

    @sip_header_list.setter
    def sip_header_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b6dca869615da336763b3c2ece22ddbd9773b7f37128665a73380e912dd5c05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sipHeaderList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sipHeaderName")
    def sip_header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sipHeaderName"))

    @sip_header_name.setter
    def sip_header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9282efd7b21208e64cfe6b83dd6d987117f4f9f8e8fc725e8e18f603b28e353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sipHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tls")
    def tls(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tls"))

    @tls.setter
    def tls(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c1379c6efffed10398f96166139b89c2e9761869c427906c7d7784b8ac868b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tls", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDomainV1.WafDomainV1BlockPage",
    jsii_struct_bases=[],
    name_mapping={
        "template": "template",
        "content": "content",
        "content_type": "contentType",
        "redirect_url": "redirectUrl",
        "status_code": "statusCode",
    },
)
class WafDomainV1BlockPage:
    def __init__(
        self,
        *,
        template: builtins.str,
        content: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        redirect_url: typing.Optional[builtins.str] = None,
        status_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#template WafDomainV1#template}.
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#content WafDomainV1#content}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#content_type WafDomainV1#content_type}.
        :param redirect_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#redirect_url WafDomainV1#redirect_url}.
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#status_code WafDomainV1#status_code}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53da4deebe8d16c7640b966031c8772f53afe0c34bf5999b9d532219af2b80c2)
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument redirect_url", value=redirect_url, expected_type=type_hints["redirect_url"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "template": template,
        }
        if content is not None:
            self._values["content"] = content
        if content_type is not None:
            self._values["content_type"] = content_type
        if redirect_url is not None:
            self._values["redirect_url"] = redirect_url
        if status_code is not None:
            self._values["status_code"] = status_code

    @builtins.property
    def template(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#template WafDomainV1#template}.'''
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#content WafDomainV1#content}.'''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#content_type WafDomainV1#content_type}.'''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#redirect_url WafDomainV1#redirect_url}.'''
        result = self._values.get("redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#status_code WafDomainV1#status_code}.'''
        result = self._values.get("status_code")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDomainV1BlockPage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDomainV1BlockPageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDomainV1.WafDomainV1BlockPageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f051963a079ebac9f1bdea6078b4378b6df47280011481429924afe92fa15331)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContent")
    def reset_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContent", []))

    @jsii.member(jsii_name="resetContentType")
    def reset_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentType", []))

    @jsii.member(jsii_name="resetRedirectUrl")
    def reset_redirect_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUrl", []))

    @jsii.member(jsii_name="resetStatusCode")
    def reset_status_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatusCode", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUrlInput")
    def redirect_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="templateInput")
    def template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e031912302648b49eb2769be4c852c611ac4dfa639636dd1fc6cc894f593cbf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a40c1d21473faff49209097fa5be80f88ce57f6c8f410a30d618e1086449fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUrl")
    def redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUrl"))

    @redirect_url.setter
    def redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78395847e79072b0f117f91fbed442910677e5bf718bc97d216fcdf87169c2f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e62f8986d785bbcdecd58e0743ea52a8691bd0a6d1c0d1807897c6a657f27e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "template"))

    @template.setter
    def template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a542425f6dad15ea03f8ffd907092c75b83392582af8b4fa5cb0b70f3a56096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "template", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WafDomainV1BlockPage]:
        return typing.cast(typing.Optional[WafDomainV1BlockPage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[WafDomainV1BlockPage]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce26e2bd5356caad9081198c2e69aa7eb55ca714c3fd9d0cc1889556d48cea47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDomainV1.WafDomainV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "hostname": "hostname",
        "proxy": "proxy",
        "server": "server",
        "block_page": "blockPage",
        "certificate_id": "certificateId",
        "cipher": "cipher",
        "id": "id",
        "policy_id": "policyId",
        "sip_header_list": "sipHeaderList",
        "sip_header_name": "sipHeaderName",
        "timeouts": "timeouts",
        "tls": "tls",
    },
)
class WafDomainV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        hostname: builtins.str,
        proxy: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        server: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDomainV1Server", typing.Dict[builtins.str, typing.Any]]]],
        block_page: typing.Optional[typing.Union[WafDomainV1BlockPage, typing.Dict[builtins.str, typing.Any]]] = None,
        certificate_id: typing.Optional[builtins.str] = None,
        cipher: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        policy_id: typing.Optional[builtins.str] = None,
        sip_header_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        sip_header_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["WafDomainV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#hostname WafDomainV1#hostname}.
        :param proxy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#proxy WafDomainV1#proxy}.
        :param server: server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#server WafDomainV1#server}
        :param block_page: block_page block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#block_page WafDomainV1#block_page}
        :param certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#certificate_id WafDomainV1#certificate_id}.
        :param cipher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#cipher WafDomainV1#cipher}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#id WafDomainV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#policy_id WafDomainV1#policy_id}.
        :param sip_header_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#sip_header_list WafDomainV1#sip_header_list}.
        :param sip_header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#sip_header_name WafDomainV1#sip_header_name}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#timeouts WafDomainV1#timeouts}
        :param tls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#tls WafDomainV1#tls}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(block_page, dict):
            block_page = WafDomainV1BlockPage(**block_page)
        if isinstance(timeouts, dict):
            timeouts = WafDomainV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24849aae9af7b55d4d5d47f1551daf76eb91731a5926859aa2f76fd234fdebc7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument proxy", value=proxy, expected_type=type_hints["proxy"])
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument block_page", value=block_page, expected_type=type_hints["block_page"])
            check_type(argname="argument certificate_id", value=certificate_id, expected_type=type_hints["certificate_id"])
            check_type(argname="argument cipher", value=cipher, expected_type=type_hints["cipher"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument sip_header_list", value=sip_header_list, expected_type=type_hints["sip_header_list"])
            check_type(argname="argument sip_header_name", value=sip_header_name, expected_type=type_hints["sip_header_name"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hostname": hostname,
            "proxy": proxy,
            "server": server,
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
        if block_page is not None:
            self._values["block_page"] = block_page
        if certificate_id is not None:
            self._values["certificate_id"] = certificate_id
        if cipher is not None:
            self._values["cipher"] = cipher
        if id is not None:
            self._values["id"] = id
        if policy_id is not None:
            self._values["policy_id"] = policy_id
        if sip_header_list is not None:
            self._values["sip_header_list"] = sip_header_list
        if sip_header_name is not None:
            self._values["sip_header_name"] = sip_header_name
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if tls is not None:
            self._values["tls"] = tls

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
    def hostname(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#hostname WafDomainV1#hostname}.'''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def proxy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#proxy WafDomainV1#proxy}.'''
        result = self._values.get("proxy")
        assert result is not None, "Required property 'proxy' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def server(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDomainV1Server"]]:
        '''server block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#server WafDomainV1#server}
        '''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDomainV1Server"]], result)

    @builtins.property
    def block_page(self) -> typing.Optional[WafDomainV1BlockPage]:
        '''block_page block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#block_page WafDomainV1#block_page}
        '''
        result = self._values.get("block_page")
        return typing.cast(typing.Optional[WafDomainV1BlockPage], result)

    @builtins.property
    def certificate_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#certificate_id WafDomainV1#certificate_id}.'''
        result = self._values.get("certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cipher(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#cipher WafDomainV1#cipher}.'''
        result = self._values.get("cipher")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#id WafDomainV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#policy_id WafDomainV1#policy_id}.'''
        result = self._values.get("policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sip_header_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#sip_header_list WafDomainV1#sip_header_list}.'''
        result = self._values.get("sip_header_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sip_header_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#sip_header_name WafDomainV1#sip_header_name}.'''
        result = self._values.get("sip_header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["WafDomainV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#timeouts WafDomainV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["WafDomainV1Timeouts"], result)

    @builtins.property
    def tls(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#tls WafDomainV1#tls}.'''
        result = self._values.get("tls")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDomainV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDomainV1.WafDomainV1Server",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "port": "port",
        "back_protocol": "backProtocol",
        "client_protocol": "clientProtocol",
        "front_protocol": "frontProtocol",
        "server_protocol": "serverProtocol",
    },
)
class WafDomainV1Server:
    def __init__(
        self,
        *,
        address: builtins.str,
        port: builtins.str,
        back_protocol: typing.Optional[builtins.str] = None,
        client_protocol: typing.Optional[builtins.str] = None,
        front_protocol: typing.Optional[builtins.str] = None,
        server_protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#address WafDomainV1#address}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#port WafDomainV1#port}.
        :param back_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#back_protocol WafDomainV1#back_protocol}.
        :param client_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#client_protocol WafDomainV1#client_protocol}.
        :param front_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#front_protocol WafDomainV1#front_protocol}.
        :param server_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#server_protocol WafDomainV1#server_protocol}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67630b8cc89328bb0c70cb3acd051aeeeed94ad6f9d891a0302e863c44c9dfa7)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument back_protocol", value=back_protocol, expected_type=type_hints["back_protocol"])
            check_type(argname="argument client_protocol", value=client_protocol, expected_type=type_hints["client_protocol"])
            check_type(argname="argument front_protocol", value=front_protocol, expected_type=type_hints["front_protocol"])
            check_type(argname="argument server_protocol", value=server_protocol, expected_type=type_hints["server_protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
            "port": port,
        }
        if back_protocol is not None:
            self._values["back_protocol"] = back_protocol
        if client_protocol is not None:
            self._values["client_protocol"] = client_protocol
        if front_protocol is not None:
            self._values["front_protocol"] = front_protocol
        if server_protocol is not None:
            self._values["server_protocol"] = server_protocol

    @builtins.property
    def address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#address WafDomainV1#address}.'''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#port WafDomainV1#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def back_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#back_protocol WafDomainV1#back_protocol}.'''
        result = self._values.get("back_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#client_protocol WafDomainV1#client_protocol}.'''
        result = self._values.get("client_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def front_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#front_protocol WafDomainV1#front_protocol}.'''
        result = self._values.get("front_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#server_protocol WafDomainV1#server_protocol}.'''
        result = self._values.get("server_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDomainV1Server(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDomainV1ServerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDomainV1.WafDomainV1ServerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7772e11b24002c628c0309363bc7e7e4e186bf97b8d6b2f8bd1e70cb084a0a36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "WafDomainV1ServerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e39e81af5086a55b962eaede878e86542e1d6f814cdc29cc000d267fface626a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WafDomainV1ServerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44c52c5ddad7576886b367c1359594b5801c53a9558aa1f2a47e8af8be6ee127)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d3858a35c2f6098b65c278bb7119684ecea49ab61e7a5c7178b1db99cbf407e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ac419f37245455f407b19b7edec3bd81505853359bdcf399562aef852ecc3f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDomainV1Server]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDomainV1Server]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDomainV1Server]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5273531a0f55579364ccd9b774d6a92cb63266d14ec572ae143e56d2ad581ae9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WafDomainV1ServerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDomainV1.WafDomainV1ServerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a2eb287c773c1002c26d7609f5103e27f18289bc36f205d8f5aa5b5ee72b4d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBackProtocol")
    def reset_back_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackProtocol", []))

    @jsii.member(jsii_name="resetClientProtocol")
    def reset_client_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientProtocol", []))

    @jsii.member(jsii_name="resetFrontProtocol")
    def reset_front_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrontProtocol", []))

    @jsii.member(jsii_name="resetServerProtocol")
    def reset_server_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerProtocol", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="backProtocolInput")
    def back_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="clientProtocolInput")
    def client_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="frontProtocolInput")
    def front_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frontProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="serverProtocolInput")
    def server_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686a065a968f6947e6dc93bdf48e8fb8cf9c955a0a181f331da7e220a4b36e11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backProtocol")
    def back_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backProtocol"))

    @back_protocol.setter
    def back_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c6fcc7ffd7b1bbaeac8e929e2d495007a2c0107218ad93e90e8c8cc97c6d584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientProtocol")
    def client_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientProtocol"))

    @client_protocol.setter
    def client_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4886f6ce26f08cc56e208f9fc40a688a715e660ac77a5be213b2028ef6201996)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frontProtocol")
    def front_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frontProtocol"))

    @front_protocol.setter
    def front_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23218aeb53a4a3ac0ddeea4451ac8d1344c6be96b67c00a1ad46376bf20106c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frontProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb6ec13123e5b22d04f6fd4c45a396bffdd7c3322e23b22ce69452770230706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverProtocol")
    def server_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverProtocol"))

    @server_protocol.setter
    def server_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ad97d646fb69ee84ecc72ddc2c7ba394fc67050289c9f9c8b2f7873db1761e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDomainV1Server]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDomainV1Server]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDomainV1Server]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175dfbb70a3cc4228971a07bd75b78c00d268f7e8eec3dc7f5315dfb731eb377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDomainV1.WafDomainV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class WafDomainV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#create WafDomainV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#delete WafDomainV1#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44b4b199efa2d783e21de3afa339215f94c6e79292dcab4d2884b4dc02f042f0)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#create WafDomainV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_domain_v1#delete WafDomainV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDomainV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDomainV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDomainV1.WafDomainV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80253c18858344edd886e619e4dfe4ffc898e3ca22b0cd196239878f4ff2a0ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6072d676b2e83e1ebd59adbd0d57358fdcb4f188ff122d7a0a12168d04a0f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d5146819248444dc8bb809932d5aeedae8c94ddd2a47285cb099004ce99c7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDomainV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDomainV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDomainV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47d3c3d47c5d56e4e032d54cc537f761a72be9f3ba9c9067cd64f423269d0b3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WafDomainV1",
    "WafDomainV1BlockPage",
    "WafDomainV1BlockPageOutputReference",
    "WafDomainV1Config",
    "WafDomainV1Server",
    "WafDomainV1ServerList",
    "WafDomainV1ServerOutputReference",
    "WafDomainV1Timeouts",
    "WafDomainV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__355667572a91664231d0f373bf96c73fb4a40e42111f3fa0f109684e5f2f7524(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    hostname: builtins.str,
    proxy: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    server: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDomainV1Server, typing.Dict[builtins.str, typing.Any]]]],
    block_page: typing.Optional[typing.Union[WafDomainV1BlockPage, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate_id: typing.Optional[builtins.str] = None,
    cipher: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    policy_id: typing.Optional[builtins.str] = None,
    sip_header_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    sip_header_name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[WafDomainV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__fe4867a3b77e79a9ebf19734bb4cfd0731ddf49c7a00840128241526b5ee8b7e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90655c5c57981e5a1bcc2b0af3fb1eda0bcabf091157ae354416bff3a849300(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDomainV1Server, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__130da73924bc144ebd596eafd30c548cf3e63769b80572aaa724f110e14e9a52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7446aca65ec1b474b8dd6cf45e5fbff2c9c75b0bd40e6a7d791b1a7ce7fd7b44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08df57b9c560bafd9492040141abd88fe1f6fa0812de0b2ff37ad577c99020b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69df74e4b517cd2e63a7135fc18e55886fd075f52c871c3e8ce26c32e8336f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52f2a22b1046afaf01aa53a7886f5575a1186a95c9b8bcedede53c843cb5e5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d2019c0fff694dfe55e6918749de13e0ad53586654ba2032bddd7c3aa67aabc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b6dca869615da336763b3c2ece22ddbd9773b7f37128665a73380e912dd5c05(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9282efd7b21208e64cfe6b83dd6d987117f4f9f8e8fc725e8e18f603b28e353(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c1379c6efffed10398f96166139b89c2e9761869c427906c7d7784b8ac868b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53da4deebe8d16c7640b966031c8772f53afe0c34bf5999b9d532219af2b80c2(
    *,
    template: builtins.str,
    content: typing.Optional[builtins.str] = None,
    content_type: typing.Optional[builtins.str] = None,
    redirect_url: typing.Optional[builtins.str] = None,
    status_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f051963a079ebac9f1bdea6078b4378b6df47280011481429924afe92fa15331(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e031912302648b49eb2769be4c852c611ac4dfa639636dd1fc6cc894f593cbf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a40c1d21473faff49209097fa5be80f88ce57f6c8f410a30d618e1086449fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78395847e79072b0f117f91fbed442910677e5bf718bc97d216fcdf87169c2f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e62f8986d785bbcdecd58e0743ea52a8691bd0a6d1c0d1807897c6a657f27e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a542425f6dad15ea03f8ffd907092c75b83392582af8b4fa5cb0b70f3a56096(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce26e2bd5356caad9081198c2e69aa7eb55ca714c3fd9d0cc1889556d48cea47(
    value: typing.Optional[WafDomainV1BlockPage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24849aae9af7b55d4d5d47f1551daf76eb91731a5926859aa2f76fd234fdebc7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hostname: builtins.str,
    proxy: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    server: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDomainV1Server, typing.Dict[builtins.str, typing.Any]]]],
    block_page: typing.Optional[typing.Union[WafDomainV1BlockPage, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate_id: typing.Optional[builtins.str] = None,
    cipher: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    policy_id: typing.Optional[builtins.str] = None,
    sip_header_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    sip_header_name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[WafDomainV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67630b8cc89328bb0c70cb3acd051aeeeed94ad6f9d891a0302e863c44c9dfa7(
    *,
    address: builtins.str,
    port: builtins.str,
    back_protocol: typing.Optional[builtins.str] = None,
    client_protocol: typing.Optional[builtins.str] = None,
    front_protocol: typing.Optional[builtins.str] = None,
    server_protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7772e11b24002c628c0309363bc7e7e4e186bf97b8d6b2f8bd1e70cb084a0a36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39e81af5086a55b962eaede878e86542e1d6f814cdc29cc000d267fface626a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c52c5ddad7576886b367c1359594b5801c53a9558aa1f2a47e8af8be6ee127(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d3858a35c2f6098b65c278bb7119684ecea49ab61e7a5c7178b1db99cbf407e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac419f37245455f407b19b7edec3bd81505853359bdcf399562aef852ecc3f7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5273531a0f55579364ccd9b774d6a92cb63266d14ec572ae143e56d2ad581ae9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDomainV1Server]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2eb287c773c1002c26d7609f5103e27f18289bc36f205d8f5aa5b5ee72b4d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686a065a968f6947e6dc93bdf48e8fb8cf9c955a0a181f331da7e220a4b36e11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6fcc7ffd7b1bbaeac8e929e2d495007a2c0107218ad93e90e8c8cc97c6d584(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4886f6ce26f08cc56e208f9fc40a688a715e660ac77a5be213b2028ef6201996(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23218aeb53a4a3ac0ddeea4451ac8d1344c6be96b67c00a1ad46376bf20106c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb6ec13123e5b22d04f6fd4c45a396bffdd7c3322e23b22ce69452770230706(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad97d646fb69ee84ecc72ddc2c7ba394fc67050289c9f9c8b2f7873db1761e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175dfbb70a3cc4228971a07bd75b78c00d268f7e8eec3dc7f5315dfb731eb377(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDomainV1Server]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44b4b199efa2d783e21de3afa339215f94c6e79292dcab4d2884b4dc02f042f0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80253c18858344edd886e619e4dfe4ffc898e3ca22b0cd196239878f4ff2a0ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6072d676b2e83e1ebd59adbd0d57358fdcb4f188ff122d7a0a12168d04a0f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d5146819248444dc8bb809932d5aeedae8c94ddd2a47285cb099004ce99c7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d3c3d47c5d56e4e032d54cc537f761a72be9f3ba9c9067cd64f423269d0b3e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDomainV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

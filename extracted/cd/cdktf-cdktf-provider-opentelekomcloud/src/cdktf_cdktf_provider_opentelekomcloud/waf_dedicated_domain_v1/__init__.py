r'''
# `opentelekomcloud_waf_dedicated_domain_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_waf_dedicated_domain_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1).
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


class WafDedicatedDomainV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedDomainV1.WafDedicatedDomainV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1 opentelekomcloud_waf_dedicated_domain_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        domain: builtins.str,
        server: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDedicatedDomainV1Server", typing.Dict[builtins.str, typing.Any]]]],
        certificate_id: typing.Optional[builtins.str] = None,
        cipher: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        keep_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pci3_ds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pci_dss: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policy_id: typing.Optional[builtins.str] = None,
        protect_status: typing.Optional[jsii.Number] = None,
        proxy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        timeout_config: typing.Optional[typing.Union["WafDedicatedDomainV1TimeoutConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tls: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1 opentelekomcloud_waf_dedicated_domain_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#domain WafDedicatedDomainV1#domain}.
        :param server: server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#server WafDedicatedDomainV1#server}
        :param certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#certificate_id WafDedicatedDomainV1#certificate_id}.
        :param cipher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#cipher WafDedicatedDomainV1#cipher}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#id WafDedicatedDomainV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param keep_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#keep_policy WafDedicatedDomainV1#keep_policy}.
        :param pci3_ds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#pci_3ds WafDedicatedDomainV1#pci_3ds}.
        :param pci_dss: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#pci_dss WafDedicatedDomainV1#pci_dss}.
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#policy_id WafDedicatedDomainV1#policy_id}.
        :param protect_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#protect_status WafDedicatedDomainV1#protect_status}.
        :param proxy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#proxy WafDedicatedDomainV1#proxy}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#region WafDedicatedDomainV1#region}.
        :param timeout_config: timeout_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#timeout_config WafDedicatedDomainV1#timeout_config}
        :param tls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#tls WafDedicatedDomainV1#tls}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dcfae05f99e6d2d6822b808ff1ac27e051f67a59a0d4f58e988f06e9035ada0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WafDedicatedDomainV1Config(
            domain=domain,
            server=server,
            certificate_id=certificate_id,
            cipher=cipher,
            id=id,
            keep_policy=keep_policy,
            pci3_ds=pci3_ds,
            pci_dss=pci_dss,
            policy_id=policy_id,
            protect_status=protect_status,
            proxy=proxy,
            region=region,
            timeout_config=timeout_config,
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
        '''Generates CDKTF code for importing a WafDedicatedDomainV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WafDedicatedDomainV1 to import.
        :param import_from_id: The id of the existing WafDedicatedDomainV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WafDedicatedDomainV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67a8ab757470ece73363adcf4f746388026dd754b7d2b97172e2e209578731e6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putServer")
    def put_server(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDedicatedDomainV1Server", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3a7341236c51cdf55f9736e335f0d71a249ceda6c8c9b257f9637ac8684555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServer", [value]))

    @jsii.member(jsii_name="putTimeoutConfig")
    def put_timeout_config(
        self,
        *,
        connect_timeout: typing.Optional[jsii.Number] = None,
        read_timeout: typing.Optional[jsii.Number] = None,
        send_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connect_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#connect_timeout WafDedicatedDomainV1#connect_timeout}.
        :param read_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#read_timeout WafDedicatedDomainV1#read_timeout}.
        :param send_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#send_timeout WafDedicatedDomainV1#send_timeout}.
        '''
        value = WafDedicatedDomainV1TimeoutConfig(
            connect_timeout=connect_timeout,
            read_timeout=read_timeout,
            send_timeout=send_timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putTimeoutConfig", [value]))

    @jsii.member(jsii_name="resetCertificateId")
    def reset_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateId", []))

    @jsii.member(jsii_name="resetCipher")
    def reset_cipher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCipher", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKeepPolicy")
    def reset_keep_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepPolicy", []))

    @jsii.member(jsii_name="resetPci3Ds")
    def reset_pci3_ds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPci3Ds", []))

    @jsii.member(jsii_name="resetPciDss")
    def reset_pci_dss(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPciDss", []))

    @jsii.member(jsii_name="resetPolicyId")
    def reset_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyId", []))

    @jsii.member(jsii_name="resetProtectStatus")
    def reset_protect_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtectStatus", []))

    @jsii.member(jsii_name="resetProxy")
    def reset_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxy", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTimeoutConfig")
    def reset_timeout_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutConfig", []))

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
    @jsii.member(jsii_name="accessStatus")
    def access_status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accessStatus"))

    @builtins.property
    @jsii.member(jsii_name="alarmPage")
    def alarm_page(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "alarmPage"))

    @builtins.property
    @jsii.member(jsii_name="certificateName")
    def certificate_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateName"))

    @builtins.property
    @jsii.member(jsii_name="complianceCertification")
    def compliance_certification(self) -> _cdktf_9a9027ec.BooleanMap:
        return typing.cast(_cdktf_9a9027ec.BooleanMap, jsii.get(self, "complianceCertification"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> "WafDedicatedDomainV1ServerList":
        return typing.cast("WafDedicatedDomainV1ServerList", jsii.get(self, "server"))

    @builtins.property
    @jsii.member(jsii_name="timeoutConfig")
    def timeout_config(self) -> "WafDedicatedDomainV1TimeoutConfigOutputReference":
        return typing.cast("WafDedicatedDomainV1TimeoutConfigOutputReference", jsii.get(self, "timeoutConfig"))

    @builtins.property
    @jsii.member(jsii_name="trafficIdentifier")
    def traffic_identifier(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "trafficIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="certificateIdInput")
    def certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cipherInput")
    def cipher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cipherInput"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keepPolicyInput")
    def keep_policy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keepPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="pci3DsInput")
    def pci3_ds_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pci3DsInput"))

    @builtins.property
    @jsii.member(jsii_name="pciDssInput")
    def pci_dss_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pciDssInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="protectStatusInput")
    def protect_status_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "protectStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyInput")
    def proxy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "proxyInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="serverInput")
    def server_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedDomainV1Server"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedDomainV1Server"]]], jsii.get(self, "serverInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutConfigInput")
    def timeout_config_input(
        self,
    ) -> typing.Optional["WafDedicatedDomainV1TimeoutConfig"]:
        return typing.cast(typing.Optional["WafDedicatedDomainV1TimeoutConfig"], jsii.get(self, "timeoutConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__17192936ccbe3aa3c303e08a3629dd3e61299ac3cea7c6a7a0faec6518406f61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cipher")
    def cipher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cipher"))

    @cipher.setter
    def cipher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73abc754fddb8d08615c15dfb794d5a33be3e521b411f41ea076a02621658389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cipher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ca94b8c937ad4afb4377e2ce8df15e1326c340a66d902ace211a48b91877ba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50cca013edc43dee1c6a47318f3a792c618ccac153bccd01b3b17bf8a6eb2a4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keepPolicy")
    def keep_policy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "keepPolicy"))

    @keep_policy.setter
    def keep_policy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a087659fbf5e39c60d6eced55dc645e30a723238eaadb463506de408dbe2f603)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pci3Ds")
    def pci3_ds(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pci3Ds"))

    @pci3_ds.setter
    def pci3_ds(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ecaf61cf3c6cf8b5ad1453c65d73d6be2b7b7b485228da6fa3ae6932a5ebdbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pci3Ds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pciDss")
    def pci_dss(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pciDss"))

    @pci_dss.setter
    def pci_dss(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b8cbeca16de749df505b3c83389dc1699f3d4a2c197759129ca352647c9ea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pciDss", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd83a360aa0e44dbbe9732e45ecdb2f495402a95e215c65279bc6b2437f1027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protectStatus")
    def protect_status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "protectStatus"))

    @protect_status.setter
    def protect_status(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ec63b361d57325c5d45bb828bba71a01e99ec52096ce69566255dfd9f1b777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protectStatus", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__36795a1c135dc32889b3027915a1d790f3655597e59abcc6bf5ba814f1a0fbfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc014e48faa8300e5cfcf4f8eb0440de7840b7862bd9be6a636f00749c392b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tls")
    def tls(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tls"))

    @tls.setter
    def tls(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db2596d9837b7e69693272f8528df5c9d033fa14e6b1eb18b70903fa07e1b08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tls", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedDomainV1.WafDedicatedDomainV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "domain": "domain",
        "server": "server",
        "certificate_id": "certificateId",
        "cipher": "cipher",
        "id": "id",
        "keep_policy": "keepPolicy",
        "pci3_ds": "pci3Ds",
        "pci_dss": "pciDss",
        "policy_id": "policyId",
        "protect_status": "protectStatus",
        "proxy": "proxy",
        "region": "region",
        "timeout_config": "timeoutConfig",
        "tls": "tls",
    },
)
class WafDedicatedDomainV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        domain: builtins.str,
        server: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDedicatedDomainV1Server", typing.Dict[builtins.str, typing.Any]]]],
        certificate_id: typing.Optional[builtins.str] = None,
        cipher: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        keep_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pci3_ds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pci_dss: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policy_id: typing.Optional[builtins.str] = None,
        protect_status: typing.Optional[jsii.Number] = None,
        proxy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        timeout_config: typing.Optional[typing.Union["WafDedicatedDomainV1TimeoutConfig", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#domain WafDedicatedDomainV1#domain}.
        :param server: server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#server WafDedicatedDomainV1#server}
        :param certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#certificate_id WafDedicatedDomainV1#certificate_id}.
        :param cipher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#cipher WafDedicatedDomainV1#cipher}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#id WafDedicatedDomainV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param keep_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#keep_policy WafDedicatedDomainV1#keep_policy}.
        :param pci3_ds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#pci_3ds WafDedicatedDomainV1#pci_3ds}.
        :param pci_dss: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#pci_dss WafDedicatedDomainV1#pci_dss}.
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#policy_id WafDedicatedDomainV1#policy_id}.
        :param protect_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#protect_status WafDedicatedDomainV1#protect_status}.
        :param proxy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#proxy WafDedicatedDomainV1#proxy}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#region WafDedicatedDomainV1#region}.
        :param timeout_config: timeout_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#timeout_config WafDedicatedDomainV1#timeout_config}
        :param tls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#tls WafDedicatedDomainV1#tls}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeout_config, dict):
            timeout_config = WafDedicatedDomainV1TimeoutConfig(**timeout_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__181310c7fa7c2c491cba79138afd611af1297ff7ee8dc706a674f849e83d60b4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument certificate_id", value=certificate_id, expected_type=type_hints["certificate_id"])
            check_type(argname="argument cipher", value=cipher, expected_type=type_hints["cipher"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument keep_policy", value=keep_policy, expected_type=type_hints["keep_policy"])
            check_type(argname="argument pci3_ds", value=pci3_ds, expected_type=type_hints["pci3_ds"])
            check_type(argname="argument pci_dss", value=pci_dss, expected_type=type_hints["pci_dss"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument protect_status", value=protect_status, expected_type=type_hints["protect_status"])
            check_type(argname="argument proxy", value=proxy, expected_type=type_hints["proxy"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeout_config", value=timeout_config, expected_type=type_hints["timeout_config"])
            check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain": domain,
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
        if certificate_id is not None:
            self._values["certificate_id"] = certificate_id
        if cipher is not None:
            self._values["cipher"] = cipher
        if id is not None:
            self._values["id"] = id
        if keep_policy is not None:
            self._values["keep_policy"] = keep_policy
        if pci3_ds is not None:
            self._values["pci3_ds"] = pci3_ds
        if pci_dss is not None:
            self._values["pci_dss"] = pci_dss
        if policy_id is not None:
            self._values["policy_id"] = policy_id
        if protect_status is not None:
            self._values["protect_status"] = protect_status
        if proxy is not None:
            self._values["proxy"] = proxy
        if region is not None:
            self._values["region"] = region
        if timeout_config is not None:
            self._values["timeout_config"] = timeout_config
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
    def domain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#domain WafDedicatedDomainV1#domain}.'''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedDomainV1Server"]]:
        '''server block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#server WafDedicatedDomainV1#server}
        '''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedDomainV1Server"]], result)

    @builtins.property
    def certificate_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#certificate_id WafDedicatedDomainV1#certificate_id}.'''
        result = self._values.get("certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cipher(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#cipher WafDedicatedDomainV1#cipher}.'''
        result = self._values.get("cipher")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#id WafDedicatedDomainV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keep_policy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#keep_policy WafDedicatedDomainV1#keep_policy}.'''
        result = self._values.get("keep_policy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def pci3_ds(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#pci_3ds WafDedicatedDomainV1#pci_3ds}.'''
        result = self._values.get("pci3_ds")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def pci_dss(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#pci_dss WafDedicatedDomainV1#pci_dss}.'''
        result = self._values.get("pci_dss")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#policy_id WafDedicatedDomainV1#policy_id}.'''
        result = self._values.get("policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protect_status(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#protect_status WafDedicatedDomainV1#protect_status}.'''
        result = self._values.get("protect_status")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def proxy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#proxy WafDedicatedDomainV1#proxy}.'''
        result = self._values.get("proxy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#region WafDedicatedDomainV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_config(self) -> typing.Optional["WafDedicatedDomainV1TimeoutConfig"]:
        '''timeout_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#timeout_config WafDedicatedDomainV1#timeout_config}
        '''
        result = self._values.get("timeout_config")
        return typing.cast(typing.Optional["WafDedicatedDomainV1TimeoutConfig"], result)

    @builtins.property
    def tls(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#tls WafDedicatedDomainV1#tls}.'''
        result = self._values.get("tls")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedDomainV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedDomainV1.WafDedicatedDomainV1Server",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "client_protocol": "clientProtocol",
        "port": "port",
        "server_protocol": "serverProtocol",
        "type": "type",
        "vpc_id": "vpcId",
    },
)
class WafDedicatedDomainV1Server:
    def __init__(
        self,
        *,
        address: builtins.str,
        client_protocol: builtins.str,
        port: jsii.Number,
        server_protocol: builtins.str,
        type: builtins.str,
        vpc_id: builtins.str,
    ) -> None:
        '''
        :param address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#address WafDedicatedDomainV1#address}.
        :param client_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#client_protocol WafDedicatedDomainV1#client_protocol}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#port WafDedicatedDomainV1#port}.
        :param server_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#server_protocol WafDedicatedDomainV1#server_protocol}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#type WafDedicatedDomainV1#type}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#vpc_id WafDedicatedDomainV1#vpc_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716db5bc12009d68cd115b9896012530725e1aa7d7ff7eeab87927a0a67a93c1)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument client_protocol", value=client_protocol, expected_type=type_hints["client_protocol"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument server_protocol", value=server_protocol, expected_type=type_hints["server_protocol"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
            "client_protocol": client_protocol,
            "port": port,
            "server_protocol": server_protocol,
            "type": type,
            "vpc_id": vpc_id,
        }

    @builtins.property
    def address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#address WafDedicatedDomainV1#address}.'''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#client_protocol WafDedicatedDomainV1#client_protocol}.'''
        result = self._values.get("client_protocol")
        assert result is not None, "Required property 'client_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#port WafDedicatedDomainV1#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def server_protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#server_protocol WafDedicatedDomainV1#server_protocol}.'''
        result = self._values.get("server_protocol")
        assert result is not None, "Required property 'server_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#type WafDedicatedDomainV1#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#vpc_id WafDedicatedDomainV1#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedDomainV1Server(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDedicatedDomainV1ServerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedDomainV1.WafDedicatedDomainV1ServerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4be3a06017dc6e9ec3ac5796f32f8c182e3dfeb924b5442a78d683827c6fa568)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "WafDedicatedDomainV1ServerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39b480f1e3ee987ebe7424f31bf80e2fd7a61542fbf98b3908ac87a96c5d47c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WafDedicatedDomainV1ServerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__595a96e3e8354fd1cec93e6c080037bcd982b7392d4eb2abfa4cd2869749d39c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29fd4d204f567acc284da1f0450a931417a83c6e5c9944dce53dd2e3ff6d97ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c6ab76dc590d135817a00b45aa7683344150dc020189faaeb2265f382b8f1c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedDomainV1Server]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedDomainV1Server]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedDomainV1Server]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38c6dfc7d1eccf00e6e8478478c41e3d382d68e73dd5617e12959e098a0a7e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WafDedicatedDomainV1ServerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedDomainV1.WafDedicatedDomainV1ServerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2227d4db2bf5555a4b8022571c0b8ecaa3e8d347e0d79224f5249b209ba192b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="clientProtocolInput")
    def client_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="serverProtocolInput")
    def server_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab5d84b01b4cc6852d18dfc3bb72ad1ccffc92563d4bc5eb9a812a301ca025e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientProtocol")
    def client_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientProtocol"))

    @client_protocol.setter
    def client_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__179af6da012d218e5f2599864d6476570e757bf39d38ba0051b114fa8a5bdb6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b631d2d13299b4a5202d6893e57f420539dc11732f8c56de9274b9c7912e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverProtocol")
    def server_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverProtocol"))

    @server_protocol.setter
    def server_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f50d8396ae1fe691172d8ceebe126ea4d799289f30bc880befae131607c4d8cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69538ff902383c6265f1c53fce149dd46165f5973e5f3fbffda37f8a5ce57e51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718f995639d9b0536647c29642640833c2e7b138f4867d3c3f501d12b926f445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedDomainV1Server]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedDomainV1Server]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedDomainV1Server]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34c23237ddc7f2d08c2ee5e00880eb094f1239643d22d561295b4072c309be63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedDomainV1.WafDedicatedDomainV1TimeoutConfig",
    jsii_struct_bases=[],
    name_mapping={
        "connect_timeout": "connectTimeout",
        "read_timeout": "readTimeout",
        "send_timeout": "sendTimeout",
    },
)
class WafDedicatedDomainV1TimeoutConfig:
    def __init__(
        self,
        *,
        connect_timeout: typing.Optional[jsii.Number] = None,
        read_timeout: typing.Optional[jsii.Number] = None,
        send_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connect_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#connect_timeout WafDedicatedDomainV1#connect_timeout}.
        :param read_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#read_timeout WafDedicatedDomainV1#read_timeout}.
        :param send_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#send_timeout WafDedicatedDomainV1#send_timeout}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a56fd6e35369bc366a6e59ab6deeabb0c079c62415c0b693bb5b50bd37962ab)
            check_type(argname="argument connect_timeout", value=connect_timeout, expected_type=type_hints["connect_timeout"])
            check_type(argname="argument read_timeout", value=read_timeout, expected_type=type_hints["read_timeout"])
            check_type(argname="argument send_timeout", value=send_timeout, expected_type=type_hints["send_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connect_timeout is not None:
            self._values["connect_timeout"] = connect_timeout
        if read_timeout is not None:
            self._values["read_timeout"] = read_timeout
        if send_timeout is not None:
            self._values["send_timeout"] = send_timeout

    @builtins.property
    def connect_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#connect_timeout WafDedicatedDomainV1#connect_timeout}.'''
        result = self._values.get("connect_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def read_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#read_timeout WafDedicatedDomainV1#read_timeout}.'''
        result = self._values.get("read_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def send_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_domain_v1#send_timeout WafDedicatedDomainV1#send_timeout}.'''
        result = self._values.get("send_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedDomainV1TimeoutConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDedicatedDomainV1TimeoutConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedDomainV1.WafDedicatedDomainV1TimeoutConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__517b4f8a4b9771ba643f99005eff09820440a525be8e6d2baf0b51f91920abf2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConnectTimeout")
    def reset_connect_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectTimeout", []))

    @jsii.member(jsii_name="resetReadTimeout")
    def reset_read_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadTimeout", []))

    @jsii.member(jsii_name="resetSendTimeout")
    def reset_send_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="connectTimeoutInput")
    def connect_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "connectTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="readTimeoutInput")
    def read_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "readTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="sendTimeoutInput")
    def send_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sendTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="connectTimeout")
    def connect_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "connectTimeout"))

    @connect_timeout.setter
    def connect_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__945a3ad4e8a3e724b0ff4c0cc9eb6685bfb36e48c09fc67b63f75fe9aa7849d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readTimeout")
    def read_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "readTimeout"))

    @read_timeout.setter
    def read_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75017daf35ae019f7a75fd5d8acedfc094cc5939d9e17f4e954b0005f6c83127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendTimeout")
    def send_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sendTimeout"))

    @send_timeout.setter
    def send_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3425e51ed021d31172081d8cf190d899b54be29596a363ccb10938477e75d9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WafDedicatedDomainV1TimeoutConfig]:
        return typing.cast(typing.Optional[WafDedicatedDomainV1TimeoutConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WafDedicatedDomainV1TimeoutConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a821ca83e9634603aa15f68517f3a410f772d135e91a9a877e822116aabc4d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WafDedicatedDomainV1",
    "WafDedicatedDomainV1Config",
    "WafDedicatedDomainV1Server",
    "WafDedicatedDomainV1ServerList",
    "WafDedicatedDomainV1ServerOutputReference",
    "WafDedicatedDomainV1TimeoutConfig",
    "WafDedicatedDomainV1TimeoutConfigOutputReference",
]

publication.publish()

def _typecheckingstub__8dcfae05f99e6d2d6822b808ff1ac27e051f67a59a0d4f58e988f06e9035ada0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    domain: builtins.str,
    server: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedDomainV1Server, typing.Dict[builtins.str, typing.Any]]]],
    certificate_id: typing.Optional[builtins.str] = None,
    cipher: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    keep_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pci3_ds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pci_dss: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    policy_id: typing.Optional[builtins.str] = None,
    protect_status: typing.Optional[jsii.Number] = None,
    proxy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    timeout_config: typing.Optional[typing.Union[WafDedicatedDomainV1TimeoutConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__67a8ab757470ece73363adcf4f746388026dd754b7d2b97172e2e209578731e6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3a7341236c51cdf55f9736e335f0d71a249ceda6c8c9b257f9637ac8684555(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedDomainV1Server, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17192936ccbe3aa3c303e08a3629dd3e61299ac3cea7c6a7a0faec6518406f61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73abc754fddb8d08615c15dfb794d5a33be3e521b411f41ea076a02621658389(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ca94b8c937ad4afb4377e2ce8df15e1326c340a66d902ace211a48b91877ba9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50cca013edc43dee1c6a47318f3a792c618ccac153bccd01b3b17bf8a6eb2a4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a087659fbf5e39c60d6eced55dc645e30a723238eaadb463506de408dbe2f603(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ecaf61cf3c6cf8b5ad1453c65d73d6be2b7b7b485228da6fa3ae6932a5ebdbd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b8cbeca16de749df505b3c83389dc1699f3d4a2c197759129ca352647c9ea8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd83a360aa0e44dbbe9732e45ecdb2f495402a95e215c65279bc6b2437f1027(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ec63b361d57325c5d45bb828bba71a01e99ec52096ce69566255dfd9f1b777(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36795a1c135dc32889b3027915a1d790f3655597e59abcc6bf5ba814f1a0fbfe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc014e48faa8300e5cfcf4f8eb0440de7840b7862bd9be6a636f00749c392b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db2596d9837b7e69693272f8528df5c9d033fa14e6b1eb18b70903fa07e1b08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__181310c7fa7c2c491cba79138afd611af1297ff7ee8dc706a674f849e83d60b4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    domain: builtins.str,
    server: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedDomainV1Server, typing.Dict[builtins.str, typing.Any]]]],
    certificate_id: typing.Optional[builtins.str] = None,
    cipher: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    keep_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pci3_ds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pci_dss: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    policy_id: typing.Optional[builtins.str] = None,
    protect_status: typing.Optional[jsii.Number] = None,
    proxy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    timeout_config: typing.Optional[typing.Union[WafDedicatedDomainV1TimeoutConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tls: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716db5bc12009d68cd115b9896012530725e1aa7d7ff7eeab87927a0a67a93c1(
    *,
    address: builtins.str,
    client_protocol: builtins.str,
    port: jsii.Number,
    server_protocol: builtins.str,
    type: builtins.str,
    vpc_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be3a06017dc6e9ec3ac5796f32f8c182e3dfeb924b5442a78d683827c6fa568(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39b480f1e3ee987ebe7424f31bf80e2fd7a61542fbf98b3908ac87a96c5d47c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__595a96e3e8354fd1cec93e6c080037bcd982b7392d4eb2abfa4cd2869749d39c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29fd4d204f567acc284da1f0450a931417a83c6e5c9944dce53dd2e3ff6d97ea(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6ab76dc590d135817a00b45aa7683344150dc020189faaeb2265f382b8f1c8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38c6dfc7d1eccf00e6e8478478c41e3d382d68e73dd5617e12959e098a0a7e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedDomainV1Server]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2227d4db2bf5555a4b8022571c0b8ecaa3e8d347e0d79224f5249b209ba192b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab5d84b01b4cc6852d18dfc3bb72ad1ccffc92563d4bc5eb9a812a301ca025e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179af6da012d218e5f2599864d6476570e757bf39d38ba0051b114fa8a5bdb6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b631d2d13299b4a5202d6893e57f420539dc11732f8c56de9274b9c7912e2d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f50d8396ae1fe691172d8ceebe126ea4d799289f30bc880befae131607c4d8cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69538ff902383c6265f1c53fce149dd46165f5973e5f3fbffda37f8a5ce57e51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718f995639d9b0536647c29642640833c2e7b138f4867d3c3f501d12b926f445(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c23237ddc7f2d08c2ee5e00880eb094f1239643d22d561295b4072c309be63(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedDomainV1Server]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a56fd6e35369bc366a6e59ab6deeabb0c079c62415c0b693bb5b50bd37962ab(
    *,
    connect_timeout: typing.Optional[jsii.Number] = None,
    read_timeout: typing.Optional[jsii.Number] = None,
    send_timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517b4f8a4b9771ba643f99005eff09820440a525be8e6d2baf0b51f91920abf2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__945a3ad4e8a3e724b0ff4c0cc9eb6685bfb36e48c09fc67b63f75fe9aa7849d7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75017daf35ae019f7a75fd5d8acedfc094cc5939d9e17f4e954b0005f6c83127(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3425e51ed021d31172081d8cf190d899b54be29596a363ccb10938477e75d9c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a821ca83e9634603aa15f68517f3a410f772d135e91a9a877e822116aabc4d9(
    value: typing.Optional[WafDedicatedDomainV1TimeoutConfig],
) -> None:
    """Type checking stubs"""
    pass

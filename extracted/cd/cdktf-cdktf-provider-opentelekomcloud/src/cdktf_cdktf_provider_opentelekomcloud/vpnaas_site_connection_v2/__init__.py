r'''
# `opentelekomcloud_vpnaas_site_connection_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_vpnaas_site_connection_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2).
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


class VpnaasSiteConnectionV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.vpnaasSiteConnectionV2.VpnaasSiteConnectionV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2 opentelekomcloud_vpnaas_site_connection_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        ikepolicy_id: builtins.str,
        ipsecpolicy_id: builtins.str,
        peer_address: builtins.str,
        peer_id: builtins.str,
        psk: builtins.str,
        vpnservice_id: builtins.str,
        admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        dpd: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VpnaasSiteConnectionV2Dpd", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        initiator: typing.Optional[builtins.str] = None,
        local_ep_group_id: typing.Optional[builtins.str] = None,
        local_id: typing.Optional[builtins.str] = None,
        mtu: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        peer_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        peer_ep_group_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VpnaasSiteConnectionV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        value_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2 opentelekomcloud_vpnaas_site_connection_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param ikepolicy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#ikepolicy_id VpnaasSiteConnectionV2#ikepolicy_id}.
        :param ipsecpolicy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#ipsecpolicy_id VpnaasSiteConnectionV2#ipsecpolicy_id}.
        :param peer_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#peer_address VpnaasSiteConnectionV2#peer_address}.
        :param peer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#peer_id VpnaasSiteConnectionV2#peer_id}.
        :param psk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#psk VpnaasSiteConnectionV2#psk}.
        :param vpnservice_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#vpnservice_id VpnaasSiteConnectionV2#vpnservice_id}.
        :param admin_state_up: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#admin_state_up VpnaasSiteConnectionV2#admin_state_up}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#description VpnaasSiteConnectionV2#description}.
        :param dpd: dpd block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#dpd VpnaasSiteConnectionV2#dpd}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#id VpnaasSiteConnectionV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initiator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#initiator VpnaasSiteConnectionV2#initiator}.
        :param local_ep_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#local_ep_group_id VpnaasSiteConnectionV2#local_ep_group_id}.
        :param local_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#local_id VpnaasSiteConnectionV2#local_id}.
        :param mtu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#mtu VpnaasSiteConnectionV2#mtu}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#name VpnaasSiteConnectionV2#name}.
        :param peer_cidrs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#peer_cidrs VpnaasSiteConnectionV2#peer_cidrs}.
        :param peer_ep_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#peer_ep_group_id VpnaasSiteConnectionV2#peer_ep_group_id}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#region VpnaasSiteConnectionV2#region}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#tags VpnaasSiteConnectionV2#tags}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#tenant_id VpnaasSiteConnectionV2#tenant_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#timeouts VpnaasSiteConnectionV2#timeouts}
        :param value_specs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#value_specs VpnaasSiteConnectionV2#value_specs}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__554368250e9b7a1d5325e526727e0196dcb0224e55f2eeb5b8954b06dec60bb2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VpnaasSiteConnectionV2Config(
            ikepolicy_id=ikepolicy_id,
            ipsecpolicy_id=ipsecpolicy_id,
            peer_address=peer_address,
            peer_id=peer_id,
            psk=psk,
            vpnservice_id=vpnservice_id,
            admin_state_up=admin_state_up,
            description=description,
            dpd=dpd,
            id=id,
            initiator=initiator,
            local_ep_group_id=local_ep_group_id,
            local_id=local_id,
            mtu=mtu,
            name=name,
            peer_cidrs=peer_cidrs,
            peer_ep_group_id=peer_ep_group_id,
            region=region,
            tags=tags,
            tenant_id=tenant_id,
            timeouts=timeouts,
            value_specs=value_specs,
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
        '''Generates CDKTF code for importing a VpnaasSiteConnectionV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VpnaasSiteConnectionV2 to import.
        :param import_from_id: The id of the existing VpnaasSiteConnectionV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VpnaasSiteConnectionV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60d3c0759f797c9105a6bc366f5a2254d5043faa47fbc534161d7e84b5449a27)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDpd")
    def put_dpd(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VpnaasSiteConnectionV2Dpd", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ca4b40c2ad961acba3c34a380d0dc91765782fcffb03c3788a2d3343b431ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDpd", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#create VpnaasSiteConnectionV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#delete VpnaasSiteConnectionV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#update VpnaasSiteConnectionV2#update}.
        '''
        value = VpnaasSiteConnectionV2Timeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdminStateUp")
    def reset_admin_state_up(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminStateUp", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDpd")
    def reset_dpd(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDpd", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInitiator")
    def reset_initiator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitiator", []))

    @jsii.member(jsii_name="resetLocalEpGroupId")
    def reset_local_ep_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalEpGroupId", []))

    @jsii.member(jsii_name="resetLocalId")
    def reset_local_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalId", []))

    @jsii.member(jsii_name="resetMtu")
    def reset_mtu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMtu", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPeerCidrs")
    def reset_peer_cidrs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerCidrs", []))

    @jsii.member(jsii_name="resetPeerEpGroupId")
    def reset_peer_ep_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerEpGroupId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetValueSpecs")
    def reset_value_specs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueSpecs", []))

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
    @jsii.member(jsii_name="dpd")
    def dpd(self) -> "VpnaasSiteConnectionV2DpdList":
        return typing.cast("VpnaasSiteConnectionV2DpdList", jsii.get(self, "dpd"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VpnaasSiteConnectionV2TimeoutsOutputReference":
        return typing.cast("VpnaasSiteConnectionV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="adminStateUpInput")
    def admin_state_up_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "adminStateUpInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dpdInput")
    def dpd_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnaasSiteConnectionV2Dpd"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnaasSiteConnectionV2Dpd"]]], jsii.get(self, "dpdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ikepolicyIdInput")
    def ikepolicy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ikepolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="initiatorInput")
    def initiator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "initiatorInput"))

    @builtins.property
    @jsii.member(jsii_name="ipsecpolicyIdInput")
    def ipsecpolicy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipsecpolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="localEpGroupIdInput")
    def local_ep_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localEpGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="localIdInput")
    def local_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localIdInput"))

    @builtins.property
    @jsii.member(jsii_name="mtuInput")
    def mtu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "mtuInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="peerAddressInput")
    def peer_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="peerCidrsInput")
    def peer_cidrs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "peerCidrsInput"))

    @builtins.property
    @jsii.member(jsii_name="peerEpGroupIdInput")
    def peer_ep_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerEpGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="peerIdInput")
    def peer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="pskInput")
    def psk_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pskInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VpnaasSiteConnectionV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VpnaasSiteConnectionV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="valueSpecsInput")
    def value_specs_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "valueSpecsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnserviceIdInput")
    def vpnservice_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpnserviceIdInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2392619e7ce0c1edb8323a402b7ba12fd7e54cb751d2f489e9ccd3b1ee3e91d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminStateUp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5047abbdd080a759d8ca0effe6a776f4fb602d86bf79d076edc81aa237f47ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__075f6032dbb5bd5d9d126ac52fdee3014f66b37617f26eb5c27f4f5e0bc55726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ikepolicyId")
    def ikepolicy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ikepolicyId"))

    @ikepolicy_id.setter
    def ikepolicy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76fd3c54fc9bbb5d7edbe3f5f9d4e8f78510a855fc7984264a7e79b9c08e5052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ikepolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initiator")
    def initiator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "initiator"))

    @initiator.setter
    def initiator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca5afa791167bff54ddadaf5daa7ddf07e016a8ba1e4f626120fe205ceaf14cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initiator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipsecpolicyId")
    def ipsecpolicy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipsecpolicyId"))

    @ipsecpolicy_id.setter
    def ipsecpolicy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b31cd092e901721f2e7d89b4e53e1937af67f918340244a60cf1ab13fe7edd5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipsecpolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localEpGroupId")
    def local_ep_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localEpGroupId"))

    @local_ep_group_id.setter
    def local_ep_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d4a15db898d438c9a7831c431e18e174640b09acf6b26b8a590debf23dffa38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localEpGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localId")
    def local_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localId"))

    @local_id.setter
    def local_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ab62b2bf7cf252ae50257359eb6053a55e4afa8bf268098b2fa7b62bf65b99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mtu")
    def mtu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mtu"))

    @mtu.setter
    def mtu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b8e6ee79eef7fa7158c1fa1a64a2c7fba8e066b819c1a7dc715653e7d8366f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mtu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb6ef749ffeb325ee27b195b1fee4f8afef9e2eaa82c8b6e005e61ca1398d13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerAddress")
    def peer_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerAddress"))

    @peer_address.setter
    def peer_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c066441385aa115d4eebfd09a7795d4ddc8eda5140b5e2ff47cc19876a8050d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerCidrs")
    def peer_cidrs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "peerCidrs"))

    @peer_cidrs.setter
    def peer_cidrs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3332e039256ecb038ce4781d4a364a56dc14176586e28bdd09439f9b6d781c24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerCidrs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerEpGroupId")
    def peer_ep_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerEpGroupId"))

    @peer_ep_group_id.setter
    def peer_ep_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bea875cf6d52e17da41cc90d75a642538d46f9251953689e3982cee97ca8fae3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerEpGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerId")
    def peer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerId"))

    @peer_id.setter
    def peer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__512e7aedb6c93ff5e2302ddf750621652251ad87cf58ad6b3a527d6598facb0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="psk")
    def psk(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "psk"))

    @psk.setter
    def psk(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db798a0652d9da1d7e1c40e60c680e76175e5f92e257bc4a1b60078c8fd8205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "psk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e6c6ce3a70c79b7b309960e4267cb67cea109f29495b70f0bdf9b0b39398aeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d622a071b8b715e3b38062b9eca962fc438bc54c3f85448b350b6ded5abcc24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716840af8a310922f4206e8cef6c786618184d273ada03e14d09142e9ee2b646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueSpecs")
    def value_specs(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "valueSpecs"))

    @value_specs.setter
    def value_specs(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6426384e7967d631b8c480a8287b39d50ce05c7041408c3a5499bef0b5d54630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueSpecs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpnserviceId")
    def vpnservice_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpnserviceId"))

    @vpnservice_id.setter
    def vpnservice_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b3abec1506d12f1ebe2015106e1ff0b144c5c640b4d3f937d268034855c5732)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpnserviceId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.vpnaasSiteConnectionV2.VpnaasSiteConnectionV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "ikepolicy_id": "ikepolicyId",
        "ipsecpolicy_id": "ipsecpolicyId",
        "peer_address": "peerAddress",
        "peer_id": "peerId",
        "psk": "psk",
        "vpnservice_id": "vpnserviceId",
        "admin_state_up": "adminStateUp",
        "description": "description",
        "dpd": "dpd",
        "id": "id",
        "initiator": "initiator",
        "local_ep_group_id": "localEpGroupId",
        "local_id": "localId",
        "mtu": "mtu",
        "name": "name",
        "peer_cidrs": "peerCidrs",
        "peer_ep_group_id": "peerEpGroupId",
        "region": "region",
        "tags": "tags",
        "tenant_id": "tenantId",
        "timeouts": "timeouts",
        "value_specs": "valueSpecs",
    },
)
class VpnaasSiteConnectionV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        ikepolicy_id: builtins.str,
        ipsecpolicy_id: builtins.str,
        peer_address: builtins.str,
        peer_id: builtins.str,
        psk: builtins.str,
        vpnservice_id: builtins.str,
        admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        dpd: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VpnaasSiteConnectionV2Dpd", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        initiator: typing.Optional[builtins.str] = None,
        local_ep_group_id: typing.Optional[builtins.str] = None,
        local_id: typing.Optional[builtins.str] = None,
        mtu: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        peer_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        peer_ep_group_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VpnaasSiteConnectionV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        value_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param ikepolicy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#ikepolicy_id VpnaasSiteConnectionV2#ikepolicy_id}.
        :param ipsecpolicy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#ipsecpolicy_id VpnaasSiteConnectionV2#ipsecpolicy_id}.
        :param peer_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#peer_address VpnaasSiteConnectionV2#peer_address}.
        :param peer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#peer_id VpnaasSiteConnectionV2#peer_id}.
        :param psk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#psk VpnaasSiteConnectionV2#psk}.
        :param vpnservice_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#vpnservice_id VpnaasSiteConnectionV2#vpnservice_id}.
        :param admin_state_up: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#admin_state_up VpnaasSiteConnectionV2#admin_state_up}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#description VpnaasSiteConnectionV2#description}.
        :param dpd: dpd block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#dpd VpnaasSiteConnectionV2#dpd}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#id VpnaasSiteConnectionV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initiator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#initiator VpnaasSiteConnectionV2#initiator}.
        :param local_ep_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#local_ep_group_id VpnaasSiteConnectionV2#local_ep_group_id}.
        :param local_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#local_id VpnaasSiteConnectionV2#local_id}.
        :param mtu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#mtu VpnaasSiteConnectionV2#mtu}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#name VpnaasSiteConnectionV2#name}.
        :param peer_cidrs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#peer_cidrs VpnaasSiteConnectionV2#peer_cidrs}.
        :param peer_ep_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#peer_ep_group_id VpnaasSiteConnectionV2#peer_ep_group_id}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#region VpnaasSiteConnectionV2#region}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#tags VpnaasSiteConnectionV2#tags}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#tenant_id VpnaasSiteConnectionV2#tenant_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#timeouts VpnaasSiteConnectionV2#timeouts}
        :param value_specs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#value_specs VpnaasSiteConnectionV2#value_specs}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = VpnaasSiteConnectionV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdcdf88a4a55a48852c910d3a5b7c4e5dec001353984db5cc1a34ad4d3a11d44)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument ikepolicy_id", value=ikepolicy_id, expected_type=type_hints["ikepolicy_id"])
            check_type(argname="argument ipsecpolicy_id", value=ipsecpolicy_id, expected_type=type_hints["ipsecpolicy_id"])
            check_type(argname="argument peer_address", value=peer_address, expected_type=type_hints["peer_address"])
            check_type(argname="argument peer_id", value=peer_id, expected_type=type_hints["peer_id"])
            check_type(argname="argument psk", value=psk, expected_type=type_hints["psk"])
            check_type(argname="argument vpnservice_id", value=vpnservice_id, expected_type=type_hints["vpnservice_id"])
            check_type(argname="argument admin_state_up", value=admin_state_up, expected_type=type_hints["admin_state_up"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dpd", value=dpd, expected_type=type_hints["dpd"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument initiator", value=initiator, expected_type=type_hints["initiator"])
            check_type(argname="argument local_ep_group_id", value=local_ep_group_id, expected_type=type_hints["local_ep_group_id"])
            check_type(argname="argument local_id", value=local_id, expected_type=type_hints["local_id"])
            check_type(argname="argument mtu", value=mtu, expected_type=type_hints["mtu"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument peer_cidrs", value=peer_cidrs, expected_type=type_hints["peer_cidrs"])
            check_type(argname="argument peer_ep_group_id", value=peer_ep_group_id, expected_type=type_hints["peer_ep_group_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument value_specs", value=value_specs, expected_type=type_hints["value_specs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ikepolicy_id": ikepolicy_id,
            "ipsecpolicy_id": ipsecpolicy_id,
            "peer_address": peer_address,
            "peer_id": peer_id,
            "psk": psk,
            "vpnservice_id": vpnservice_id,
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
        if description is not None:
            self._values["description"] = description
        if dpd is not None:
            self._values["dpd"] = dpd
        if id is not None:
            self._values["id"] = id
        if initiator is not None:
            self._values["initiator"] = initiator
        if local_ep_group_id is not None:
            self._values["local_ep_group_id"] = local_ep_group_id
        if local_id is not None:
            self._values["local_id"] = local_id
        if mtu is not None:
            self._values["mtu"] = mtu
        if name is not None:
            self._values["name"] = name
        if peer_cidrs is not None:
            self._values["peer_cidrs"] = peer_cidrs
        if peer_ep_group_id is not None:
            self._values["peer_ep_group_id"] = peer_ep_group_id
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if value_specs is not None:
            self._values["value_specs"] = value_specs

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
    def ikepolicy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#ikepolicy_id VpnaasSiteConnectionV2#ikepolicy_id}.'''
        result = self._values.get("ikepolicy_id")
        assert result is not None, "Required property 'ikepolicy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ipsecpolicy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#ipsecpolicy_id VpnaasSiteConnectionV2#ipsecpolicy_id}.'''
        result = self._values.get("ipsecpolicy_id")
        assert result is not None, "Required property 'ipsecpolicy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#peer_address VpnaasSiteConnectionV2#peer_address}.'''
        result = self._values.get("peer_address")
        assert result is not None, "Required property 'peer_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#peer_id VpnaasSiteConnectionV2#peer_id}.'''
        result = self._values.get("peer_id")
        assert result is not None, "Required property 'peer_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def psk(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#psk VpnaasSiteConnectionV2#psk}.'''
        result = self._values.get("psk")
        assert result is not None, "Required property 'psk' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpnservice_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#vpnservice_id VpnaasSiteConnectionV2#vpnservice_id}.'''
        result = self._values.get("vpnservice_id")
        assert result is not None, "Required property 'vpnservice_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_state_up(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#admin_state_up VpnaasSiteConnectionV2#admin_state_up}.'''
        result = self._values.get("admin_state_up")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#description VpnaasSiteConnectionV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dpd(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnaasSiteConnectionV2Dpd"]]]:
        '''dpd block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#dpd VpnaasSiteConnectionV2#dpd}
        '''
        result = self._values.get("dpd")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnaasSiteConnectionV2Dpd"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#id VpnaasSiteConnectionV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initiator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#initiator VpnaasSiteConnectionV2#initiator}.'''
        result = self._values.get("initiator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_ep_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#local_ep_group_id VpnaasSiteConnectionV2#local_ep_group_id}.'''
        result = self._values.get("local_ep_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#local_id VpnaasSiteConnectionV2#local_id}.'''
        result = self._values.get("local_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mtu(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#mtu VpnaasSiteConnectionV2#mtu}.'''
        result = self._values.get("mtu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#name VpnaasSiteConnectionV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#peer_cidrs VpnaasSiteConnectionV2#peer_cidrs}.'''
        result = self._values.get("peer_cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def peer_ep_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#peer_ep_group_id VpnaasSiteConnectionV2#peer_ep_group_id}.'''
        result = self._values.get("peer_ep_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#region VpnaasSiteConnectionV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#tags VpnaasSiteConnectionV2#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#tenant_id VpnaasSiteConnectionV2#tenant_id}.'''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VpnaasSiteConnectionV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#timeouts VpnaasSiteConnectionV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VpnaasSiteConnectionV2Timeouts"], result)

    @builtins.property
    def value_specs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#value_specs VpnaasSiteConnectionV2#value_specs}.'''
        result = self._values.get("value_specs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnaasSiteConnectionV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.vpnaasSiteConnectionV2.VpnaasSiteConnectionV2Dpd",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "interval": "interval", "timeout": "timeout"},
)
class VpnaasSiteConnectionV2Dpd:
    def __init__(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        interval: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#action VpnaasSiteConnectionV2#action}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#interval VpnaasSiteConnectionV2#interval}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#timeout VpnaasSiteConnectionV2#timeout}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c2ed13e3c4b6c3651282f9ff48638e6d08570eb7ea7b583b86e9a591d9122cf)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if interval is not None:
            self._values["interval"] = interval
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#action VpnaasSiteConnectionV2#action}.'''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#interval VpnaasSiteConnectionV2#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#timeout VpnaasSiteConnectionV2#timeout}.'''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnaasSiteConnectionV2Dpd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnaasSiteConnectionV2DpdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.vpnaasSiteConnectionV2.VpnaasSiteConnectionV2DpdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63ca9b0f60c7e75f2588254f6493734579b16b13c5183b9d50fbb9ff71cce941)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VpnaasSiteConnectionV2DpdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2afc9cc8caf17ef7055e6a4c6c511f5322d350d8f25b06ff97f1c65e1cb6e3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VpnaasSiteConnectionV2DpdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e9a294a01d6571f79ed533cd55a27ce915d45eecd8a7922f018c721c3d9eb2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9754dae6e85a0e162ddb2f9671df488d8123a5e0b8cd93a120cb7578b8b1faa2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2f01e4405b2f995289c1a1950bc1b4dcae7fa5a1fa68b7ba612bba2dc34a9e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnaasSiteConnectionV2Dpd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnaasSiteConnectionV2Dpd]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnaasSiteConnectionV2Dpd]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94fb468d9e072d24ffe790ed70d84dd019ceb3f8a02a77dc5b526b7f85ea46b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VpnaasSiteConnectionV2DpdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.vpnaasSiteConnectionV2.VpnaasSiteConnectionV2DpdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afef318dcaff6fda83e8e8879cd764bb2cfe6b5fd7d238aa2726bf9b1c222c18)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b048cc0e829042e9702cedf61b1ea261ae86e0903bace2c5e6bacd8f66f2038f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f7d4ab7cb73b9009c64bbeb6af58c7d505ae099f7e3b5c8c81c301bad42899)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e27b3d2cd38f9b6f78b38b07690c88c8037cb3247347554ae29f8f53124cc4bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnaasSiteConnectionV2Dpd]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnaasSiteConnectionV2Dpd]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnaasSiteConnectionV2Dpd]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f61b5db6385d5269588497a5bc1b0e1034a75c0fcd6fbcf79d0494ccb77d149)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.vpnaasSiteConnectionV2.VpnaasSiteConnectionV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class VpnaasSiteConnectionV2Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#create VpnaasSiteConnectionV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#delete VpnaasSiteConnectionV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#update VpnaasSiteConnectionV2#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c99d8ccb0177263e6aa6d21fe8ac8703b1566d7a2a980c5d0cc59be42fe57ad)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#create VpnaasSiteConnectionV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#delete VpnaasSiteConnectionV2#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_site_connection_v2#update VpnaasSiteConnectionV2#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnaasSiteConnectionV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnaasSiteConnectionV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.vpnaasSiteConnectionV2.VpnaasSiteConnectionV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a26bd6e7c4824927331a9573117a305869e2f05be1b27f9c1364aaf7802505ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1263e102e4cbe43d450f531d7427b599be1d67a0b769ae7638fe350079fa1a58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0c716451bf30222035cf671efefd645faf7a2d29afaa147fc65b95f076ccc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f427bddd39001d2b5c76160b9f90182e96d4f553210dcab4de579989e6aaf55b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnaasSiteConnectionV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnaasSiteConnectionV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnaasSiteConnectionV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7c238142afd069cebae61733a73c65945a312df65542c8d20f958412f604ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VpnaasSiteConnectionV2",
    "VpnaasSiteConnectionV2Config",
    "VpnaasSiteConnectionV2Dpd",
    "VpnaasSiteConnectionV2DpdList",
    "VpnaasSiteConnectionV2DpdOutputReference",
    "VpnaasSiteConnectionV2Timeouts",
    "VpnaasSiteConnectionV2TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__554368250e9b7a1d5325e526727e0196dcb0224e55f2eeb5b8954b06dec60bb2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    ikepolicy_id: builtins.str,
    ipsecpolicy_id: builtins.str,
    peer_address: builtins.str,
    peer_id: builtins.str,
    psk: builtins.str,
    vpnservice_id: builtins.str,
    admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    dpd: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnaasSiteConnectionV2Dpd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    initiator: typing.Optional[builtins.str] = None,
    local_ep_group_id: typing.Optional[builtins.str] = None,
    local_id: typing.Optional[builtins.str] = None,
    mtu: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    peer_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    peer_ep_group_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VpnaasSiteConnectionV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    value_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__60d3c0759f797c9105a6bc366f5a2254d5043faa47fbc534161d7e84b5449a27(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ca4b40c2ad961acba3c34a380d0dc91765782fcffb03c3788a2d3343b431ef6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnaasSiteConnectionV2Dpd, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2392619e7ce0c1edb8323a402b7ba12fd7e54cb751d2f489e9ccd3b1ee3e91d0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5047abbdd080a759d8ca0effe6a776f4fb602d86bf79d076edc81aa237f47ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075f6032dbb5bd5d9d126ac52fdee3014f66b37617f26eb5c27f4f5e0bc55726(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76fd3c54fc9bbb5d7edbe3f5f9d4e8f78510a855fc7984264a7e79b9c08e5052(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca5afa791167bff54ddadaf5daa7ddf07e016a8ba1e4f626120fe205ceaf14cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31cd092e901721f2e7d89b4e53e1937af67f918340244a60cf1ab13fe7edd5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d4a15db898d438c9a7831c431e18e174640b09acf6b26b8a590debf23dffa38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ab62b2bf7cf252ae50257359eb6053a55e4afa8bf268098b2fa7b62bf65b99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b8e6ee79eef7fa7158c1fa1a64a2c7fba8e066b819c1a7dc715653e7d8366f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb6ef749ffeb325ee27b195b1fee4f8afef9e2eaa82c8b6e005e61ca1398d13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c066441385aa115d4eebfd09a7795d4ddc8eda5140b5e2ff47cc19876a8050d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3332e039256ecb038ce4781d4a364a56dc14176586e28bdd09439f9b6d781c24(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea875cf6d52e17da41cc90d75a642538d46f9251953689e3982cee97ca8fae3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512e7aedb6c93ff5e2302ddf750621652251ad87cf58ad6b3a527d6598facb0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db798a0652d9da1d7e1c40e60c680e76175e5f92e257bc4a1b60078c8fd8205(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6c6ce3a70c79b7b309960e4267cb67cea109f29495b70f0bdf9b0b39398aeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d622a071b8b715e3b38062b9eca962fc438bc54c3f85448b350b6ded5abcc24(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716840af8a310922f4206e8cef6c786618184d273ada03e14d09142e9ee2b646(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6426384e7967d631b8c480a8287b39d50ce05c7041408c3a5499bef0b5d54630(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3abec1506d12f1ebe2015106e1ff0b144c5c640b4d3f937d268034855c5732(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdcdf88a4a55a48852c910d3a5b7c4e5dec001353984db5cc1a34ad4d3a11d44(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ikepolicy_id: builtins.str,
    ipsecpolicy_id: builtins.str,
    peer_address: builtins.str,
    peer_id: builtins.str,
    psk: builtins.str,
    vpnservice_id: builtins.str,
    admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    dpd: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnaasSiteConnectionV2Dpd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    initiator: typing.Optional[builtins.str] = None,
    local_ep_group_id: typing.Optional[builtins.str] = None,
    local_id: typing.Optional[builtins.str] = None,
    mtu: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    peer_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    peer_ep_group_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VpnaasSiteConnectionV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    value_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2ed13e3c4b6c3651282f9ff48638e6d08570eb7ea7b583b86e9a591d9122cf(
    *,
    action: typing.Optional[builtins.str] = None,
    interval: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ca9b0f60c7e75f2588254f6493734579b16b13c5183b9d50fbb9ff71cce941(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2afc9cc8caf17ef7055e6a4c6c511f5322d350d8f25b06ff97f1c65e1cb6e3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e9a294a01d6571f79ed533cd55a27ce915d45eecd8a7922f018c721c3d9eb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9754dae6e85a0e162ddb2f9671df488d8123a5e0b8cd93a120cb7578b8b1faa2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f01e4405b2f995289c1a1950bc1b4dcae7fa5a1fa68b7ba612bba2dc34a9e7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94fb468d9e072d24ffe790ed70d84dd019ceb3f8a02a77dc5b526b7f85ea46b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnaasSiteConnectionV2Dpd]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afef318dcaff6fda83e8e8879cd764bb2cfe6b5fd7d238aa2726bf9b1c222c18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b048cc0e829042e9702cedf61b1ea261ae86e0903bace2c5e6bacd8f66f2038f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f7d4ab7cb73b9009c64bbeb6af58c7d505ae099f7e3b5c8c81c301bad42899(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27b3d2cd38f9b6f78b38b07690c88c8037cb3247347554ae29f8f53124cc4bc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f61b5db6385d5269588497a5bc1b0e1034a75c0fcd6fbcf79d0494ccb77d149(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnaasSiteConnectionV2Dpd]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c99d8ccb0177263e6aa6d21fe8ac8703b1566d7a2a980c5d0cc59be42fe57ad(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26bd6e7c4824927331a9573117a305869e2f05be1b27f9c1364aaf7802505ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1263e102e4cbe43d450f531d7427b599be1d67a0b769ae7638fe350079fa1a58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0c716451bf30222035cf671efefd645faf7a2d29afaa147fc65b95f076ccc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f427bddd39001d2b5c76160b9f90182e96d4f553210dcab4de579989e6aaf55b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c238142afd069cebae61733a73c65945a312df65542c8d20f958412f604ee4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnaasSiteConnectionV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

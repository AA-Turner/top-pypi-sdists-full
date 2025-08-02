r'''
# `opentelekomcloud_vpnaas_ipsec_policy_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_vpnaas_ipsec_policy_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2).
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


class VpnaasIpsecPolicyV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.vpnaasIpsecPolicyV2.VpnaasIpsecPolicyV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2 opentelekomcloud_vpnaas_ipsec_policy_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        auth_algorithm: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        encapsulation_mode: typing.Optional[builtins.str] = None,
        encryption_algorithm: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lifetime: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VpnaasIpsecPolicyV2Lifetime", typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        pfs: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VpnaasIpsecPolicyV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transform_protocol: typing.Optional[builtins.str] = None,
        value_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2 opentelekomcloud_vpnaas_ipsec_policy_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param auth_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#auth_algorithm VpnaasIpsecPolicyV2#auth_algorithm}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#description VpnaasIpsecPolicyV2#description}.
        :param encapsulation_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#encapsulation_mode VpnaasIpsecPolicyV2#encapsulation_mode}.
        :param encryption_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#encryption_algorithm VpnaasIpsecPolicyV2#encryption_algorithm}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#id VpnaasIpsecPolicyV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lifetime: lifetime block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#lifetime VpnaasIpsecPolicyV2#lifetime}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#name VpnaasIpsecPolicyV2#name}.
        :param pfs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#pfs VpnaasIpsecPolicyV2#pfs}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#region VpnaasIpsecPolicyV2#region}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#tenant_id VpnaasIpsecPolicyV2#tenant_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#timeouts VpnaasIpsecPolicyV2#timeouts}
        :param transform_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#transform_protocol VpnaasIpsecPolicyV2#transform_protocol}.
        :param value_specs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#value_specs VpnaasIpsecPolicyV2#value_specs}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7fc0ee5e77aede23e0cb6b51f10693436eaa2132a96f5b18e93af24685841d5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VpnaasIpsecPolicyV2Config(
            auth_algorithm=auth_algorithm,
            description=description,
            encapsulation_mode=encapsulation_mode,
            encryption_algorithm=encryption_algorithm,
            id=id,
            lifetime=lifetime,
            name=name,
            pfs=pfs,
            region=region,
            tenant_id=tenant_id,
            timeouts=timeouts,
            transform_protocol=transform_protocol,
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
        '''Generates CDKTF code for importing a VpnaasIpsecPolicyV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VpnaasIpsecPolicyV2 to import.
        :param import_from_id: The id of the existing VpnaasIpsecPolicyV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VpnaasIpsecPolicyV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573e48046919aa8f5e8ece16215fb424c2618a432d37cae737a980721e0881ae)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLifetime")
    def put_lifetime(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VpnaasIpsecPolicyV2Lifetime", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbaca245c3bcc045f9975ad33548a9f79042bd692662beef4949e0073e29d54e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLifetime", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#create VpnaasIpsecPolicyV2#create}.
        '''
        value = VpnaasIpsecPolicyV2Timeouts(create=create)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAuthAlgorithm")
    def reset_auth_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthAlgorithm", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEncapsulationMode")
    def reset_encapsulation_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncapsulationMode", []))

    @jsii.member(jsii_name="resetEncryptionAlgorithm")
    def reset_encryption_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionAlgorithm", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLifetime")
    def reset_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifetime", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPfs")
    def reset_pfs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPfs", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTransformProtocol")
    def reset_transform_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransformProtocol", []))

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
    @jsii.member(jsii_name="lifetime")
    def lifetime(self) -> "VpnaasIpsecPolicyV2LifetimeList":
        return typing.cast("VpnaasIpsecPolicyV2LifetimeList", jsii.get(self, "lifetime"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VpnaasIpsecPolicyV2TimeoutsOutputReference":
        return typing.cast("VpnaasIpsecPolicyV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="authAlgorithmInput")
    def auth_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="encapsulationModeInput")
    def encapsulation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encapsulationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionAlgorithmInput")
    def encryption_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lifetimeInput")
    def lifetime_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnaasIpsecPolicyV2Lifetime"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnaasIpsecPolicyV2Lifetime"]]], jsii.get(self, "lifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pfsInput")
    def pfs_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pfsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VpnaasIpsecPolicyV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VpnaasIpsecPolicyV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="transformProtocolInput")
    def transform_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transformProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="valueSpecsInput")
    def value_specs_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "valueSpecsInput"))

    @builtins.property
    @jsii.member(jsii_name="authAlgorithm")
    def auth_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authAlgorithm"))

    @auth_algorithm.setter
    def auth_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6d9bcf40e10b8d292ee38f4cb0c6602c6857172d2f2a33db36c0f29215e8ba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__655d14bfc707ee79eb41bc38e97d9fa65d3d00a7e43690a7eaa347d9ec4a2536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encapsulationMode")
    def encapsulation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encapsulationMode"))

    @encapsulation_mode.setter
    def encapsulation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78958ca614f20e14757afc367deea5efc1e267c6d15e7f4fc56c907842ebda97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encapsulationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionAlgorithm")
    def encryption_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionAlgorithm"))

    @encryption_algorithm.setter
    def encryption_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91242000285c4af459e4feb95b450f595ae5c0793ce9b434e946873d591cf055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed729c07ebdd56a7b15a29dc2233761821e716a1a47249e7e0c79e7f626d93d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c6b6b006834c66069f80abe7ec87e530da5040f49e0bd6ca5e6c04ab59c5a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pfs")
    def pfs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pfs"))

    @pfs.setter
    def pfs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a328d69097eaf715c14ac9ab1ee51cc3f3fd6d2180d07e3ed8436afeed1811f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pfs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e398a5e50a15e2f13150dc2fbfde60366e456ddf061f546935a82163ec80a84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6df86677f6404e6486769311b849228382e0183ee2d845598723ed13b14828a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transformProtocol")
    def transform_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transformProtocol"))

    @transform_protocol.setter
    def transform_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f11949f9d2cec140eec1ebe6d737ef8e6c90d27210945175cf9a5174e44db0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transformProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueSpecs")
    def value_specs(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "valueSpecs"))

    @value_specs.setter
    def value_specs(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66f057ea74d0ecf8a4e553276b1dc573536f8b1a4b3df437983d990a2aa2905b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueSpecs", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.vpnaasIpsecPolicyV2.VpnaasIpsecPolicyV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "auth_algorithm": "authAlgorithm",
        "description": "description",
        "encapsulation_mode": "encapsulationMode",
        "encryption_algorithm": "encryptionAlgorithm",
        "id": "id",
        "lifetime": "lifetime",
        "name": "name",
        "pfs": "pfs",
        "region": "region",
        "tenant_id": "tenantId",
        "timeouts": "timeouts",
        "transform_protocol": "transformProtocol",
        "value_specs": "valueSpecs",
    },
)
class VpnaasIpsecPolicyV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        auth_algorithm: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        encapsulation_mode: typing.Optional[builtins.str] = None,
        encryption_algorithm: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lifetime: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VpnaasIpsecPolicyV2Lifetime", typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        pfs: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VpnaasIpsecPolicyV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transform_protocol: typing.Optional[builtins.str] = None,
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
        :param auth_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#auth_algorithm VpnaasIpsecPolicyV2#auth_algorithm}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#description VpnaasIpsecPolicyV2#description}.
        :param encapsulation_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#encapsulation_mode VpnaasIpsecPolicyV2#encapsulation_mode}.
        :param encryption_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#encryption_algorithm VpnaasIpsecPolicyV2#encryption_algorithm}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#id VpnaasIpsecPolicyV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lifetime: lifetime block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#lifetime VpnaasIpsecPolicyV2#lifetime}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#name VpnaasIpsecPolicyV2#name}.
        :param pfs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#pfs VpnaasIpsecPolicyV2#pfs}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#region VpnaasIpsecPolicyV2#region}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#tenant_id VpnaasIpsecPolicyV2#tenant_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#timeouts VpnaasIpsecPolicyV2#timeouts}
        :param transform_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#transform_protocol VpnaasIpsecPolicyV2#transform_protocol}.
        :param value_specs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#value_specs VpnaasIpsecPolicyV2#value_specs}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = VpnaasIpsecPolicyV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b90ffbf7754889beb81013d82db4d852facdb206b138114e23290d90e84a26c2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument auth_algorithm", value=auth_algorithm, expected_type=type_hints["auth_algorithm"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encapsulation_mode", value=encapsulation_mode, expected_type=type_hints["encapsulation_mode"])
            check_type(argname="argument encryption_algorithm", value=encryption_algorithm, expected_type=type_hints["encryption_algorithm"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lifetime", value=lifetime, expected_type=type_hints["lifetime"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pfs", value=pfs, expected_type=type_hints["pfs"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument transform_protocol", value=transform_protocol, expected_type=type_hints["transform_protocol"])
            check_type(argname="argument value_specs", value=value_specs, expected_type=type_hints["value_specs"])
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
        if auth_algorithm is not None:
            self._values["auth_algorithm"] = auth_algorithm
        if description is not None:
            self._values["description"] = description
        if encapsulation_mode is not None:
            self._values["encapsulation_mode"] = encapsulation_mode
        if encryption_algorithm is not None:
            self._values["encryption_algorithm"] = encryption_algorithm
        if id is not None:
            self._values["id"] = id
        if lifetime is not None:
            self._values["lifetime"] = lifetime
        if name is not None:
            self._values["name"] = name
        if pfs is not None:
            self._values["pfs"] = pfs
        if region is not None:
            self._values["region"] = region
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if transform_protocol is not None:
            self._values["transform_protocol"] = transform_protocol
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
    def auth_algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#auth_algorithm VpnaasIpsecPolicyV2#auth_algorithm}.'''
        result = self._values.get("auth_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#description VpnaasIpsecPolicyV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encapsulation_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#encapsulation_mode VpnaasIpsecPolicyV2#encapsulation_mode}.'''
        result = self._values.get("encapsulation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#encryption_algorithm VpnaasIpsecPolicyV2#encryption_algorithm}.'''
        result = self._values.get("encryption_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#id VpnaasIpsecPolicyV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifetime(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnaasIpsecPolicyV2Lifetime"]]]:
        '''lifetime block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#lifetime VpnaasIpsecPolicyV2#lifetime}
        '''
        result = self._values.get("lifetime")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnaasIpsecPolicyV2Lifetime"]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#name VpnaasIpsecPolicyV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pfs(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#pfs VpnaasIpsecPolicyV2#pfs}.'''
        result = self._values.get("pfs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#region VpnaasIpsecPolicyV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#tenant_id VpnaasIpsecPolicyV2#tenant_id}.'''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VpnaasIpsecPolicyV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#timeouts VpnaasIpsecPolicyV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VpnaasIpsecPolicyV2Timeouts"], result)

    @builtins.property
    def transform_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#transform_protocol VpnaasIpsecPolicyV2#transform_protocol}.'''
        result = self._values.get("transform_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_specs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#value_specs VpnaasIpsecPolicyV2#value_specs}.'''
        result = self._values.get("value_specs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnaasIpsecPolicyV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.vpnaasIpsecPolicyV2.VpnaasIpsecPolicyV2Lifetime",
    jsii_struct_bases=[],
    name_mapping={"units": "units", "value": "value"},
)
class VpnaasIpsecPolicyV2Lifetime:
    def __init__(
        self,
        *,
        units: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#units VpnaasIpsecPolicyV2#units}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#value VpnaasIpsecPolicyV2#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7736391b428c5f1e04de14f157dc278bb3252e2965b95b45d1068bbe07d9383f)
            check_type(argname="argument units", value=units, expected_type=type_hints["units"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if units is not None:
            self._values["units"] = units
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def units(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#units VpnaasIpsecPolicyV2#units}.'''
        result = self._values.get("units")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#value VpnaasIpsecPolicyV2#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnaasIpsecPolicyV2Lifetime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnaasIpsecPolicyV2LifetimeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.vpnaasIpsecPolicyV2.VpnaasIpsecPolicyV2LifetimeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1795d7ca63d9806a6d8881072cd106bf708a08666f36d70c061ebc7c1b764d5c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VpnaasIpsecPolicyV2LifetimeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4cb3c873964f56268b230f7c2cb886d10e3a7a772a9f62081a780ebf409f757)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VpnaasIpsecPolicyV2LifetimeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608f798dde1bd61da048c72897c9a0ef99af04100cd46a9c365b04f1fd14ccc0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b8f812451402255b69ca6f3ad354c32dfd7db1e8c4cb9928e48674c93ead984)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cf511a0cd4a17c34979132579ceb75a0b2c2b98cd5f63dcede549639b55c1a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnaasIpsecPolicyV2Lifetime]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnaasIpsecPolicyV2Lifetime]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnaasIpsecPolicyV2Lifetime]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f500041f0b3b24feaa7cadaafffab7f7a3ec5c2f0733939ab1851f5dfcac62e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VpnaasIpsecPolicyV2LifetimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.vpnaasIpsecPolicyV2.VpnaasIpsecPolicyV2LifetimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b92c3447d31be26365d21f5a841be5735ef63e0db39ef7494132c7b9f99ed34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetUnits")
    def reset_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnits", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="unitsInput")
    def units_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitsInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="units")
    def units(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "units"))

    @units.setter
    def units(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e44e3c50b5a3684f1ddb321e9390f3030144ccbd612f561335787439c49de0cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "units", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b04f4fe110571f96c0e3b2dfd27ef904681f280608ad9e0659f5ee7ff8536a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnaasIpsecPolicyV2Lifetime]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnaasIpsecPolicyV2Lifetime]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnaasIpsecPolicyV2Lifetime]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a50b7f5d8ee014ce2829025da20af3aaf437cc35c3a0d65d8ea9e313c9b418a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.vpnaasIpsecPolicyV2.VpnaasIpsecPolicyV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create"},
)
class VpnaasIpsecPolicyV2Timeouts:
    def __init__(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#create VpnaasIpsecPolicyV2#create}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5a8ecfeecbce3d2c83fc60b6324d4fe4a14c18c9b4898fd20a3686582cdf8e3)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/vpnaas_ipsec_policy_v2#create VpnaasIpsecPolicyV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnaasIpsecPolicyV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnaasIpsecPolicyV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.vpnaasIpsecPolicyV2.VpnaasIpsecPolicyV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccb7fbf0a7a8e7cc9f5b0717ca3a5163bfbfee5e324512143ad95448cc9ed38a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a7e53dcf3ca3201ff0bf9a1040b92feab4dbc5fe130eec13b355660310ae4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnaasIpsecPolicyV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnaasIpsecPolicyV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnaasIpsecPolicyV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e186a15a44d99c0fafc31f4e8612ffbcef0f121f52ecb75c260bfdb7ccc924c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VpnaasIpsecPolicyV2",
    "VpnaasIpsecPolicyV2Config",
    "VpnaasIpsecPolicyV2Lifetime",
    "VpnaasIpsecPolicyV2LifetimeList",
    "VpnaasIpsecPolicyV2LifetimeOutputReference",
    "VpnaasIpsecPolicyV2Timeouts",
    "VpnaasIpsecPolicyV2TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c7fc0ee5e77aede23e0cb6b51f10693436eaa2132a96f5b18e93af24685841d5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    auth_algorithm: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    encapsulation_mode: typing.Optional[builtins.str] = None,
    encryption_algorithm: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lifetime: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnaasIpsecPolicyV2Lifetime, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    pfs: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VpnaasIpsecPolicyV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transform_protocol: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__573e48046919aa8f5e8ece16215fb424c2618a432d37cae737a980721e0881ae(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbaca245c3bcc045f9975ad33548a9f79042bd692662beef4949e0073e29d54e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnaasIpsecPolicyV2Lifetime, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d9bcf40e10b8d292ee38f4cb0c6602c6857172d2f2a33db36c0f29215e8ba3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__655d14bfc707ee79eb41bc38e97d9fa65d3d00a7e43690a7eaa347d9ec4a2536(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78958ca614f20e14757afc367deea5efc1e267c6d15e7f4fc56c907842ebda97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91242000285c4af459e4feb95b450f595ae5c0793ce9b434e946873d591cf055(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed729c07ebdd56a7b15a29dc2233761821e716a1a47249e7e0c79e7f626d93d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c6b6b006834c66069f80abe7ec87e530da5040f49e0bd6ca5e6c04ab59c5a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a328d69097eaf715c14ac9ab1ee51cc3f3fd6d2180d07e3ed8436afeed1811f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e398a5e50a15e2f13150dc2fbfde60366e456ddf061f546935a82163ec80a84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df86677f6404e6486769311b849228382e0183ee2d845598723ed13b14828a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f11949f9d2cec140eec1ebe6d737ef8e6c90d27210945175cf9a5174e44db0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66f057ea74d0ecf8a4e553276b1dc573536f8b1a4b3df437983d990a2aa2905b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90ffbf7754889beb81013d82db4d852facdb206b138114e23290d90e84a26c2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_algorithm: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    encapsulation_mode: typing.Optional[builtins.str] = None,
    encryption_algorithm: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lifetime: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnaasIpsecPolicyV2Lifetime, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    pfs: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VpnaasIpsecPolicyV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transform_protocol: typing.Optional[builtins.str] = None,
    value_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7736391b428c5f1e04de14f157dc278bb3252e2965b95b45d1068bbe07d9383f(
    *,
    units: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1795d7ca63d9806a6d8881072cd106bf708a08666f36d70c061ebc7c1b764d5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4cb3c873964f56268b230f7c2cb886d10e3a7a772a9f62081a780ebf409f757(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608f798dde1bd61da048c72897c9a0ef99af04100cd46a9c365b04f1fd14ccc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8f812451402255b69ca6f3ad354c32dfd7db1e8c4cb9928e48674c93ead984(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf511a0cd4a17c34979132579ceb75a0b2c2b98cd5f63dcede549639b55c1a6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f500041f0b3b24feaa7cadaafffab7f7a3ec5c2f0733939ab1851f5dfcac62e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnaasIpsecPolicyV2Lifetime]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b92c3447d31be26365d21f5a841be5735ef63e0db39ef7494132c7b9f99ed34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44e3c50b5a3684f1ddb321e9390f3030144ccbd612f561335787439c49de0cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b04f4fe110571f96c0e3b2dfd27ef904681f280608ad9e0659f5ee7ff8536a7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a50b7f5d8ee014ce2829025da20af3aaf437cc35c3a0d65d8ea9e313c9b418a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnaasIpsecPolicyV2Lifetime]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a8ecfeecbce3d2c83fc60b6324d4fe4a14c18c9b4898fd20a3686582cdf8e3(
    *,
    create: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb7fbf0a7a8e7cc9f5b0717ca3a5163bfbfee5e324512143ad95448cc9ed38a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a7e53dcf3ca3201ff0bf9a1040b92feab4dbc5fe130eec13b355660310ae4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e186a15a44d99c0fafc31f4e8612ffbcef0f121f52ecb75c260bfdb7ccc924c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnaasIpsecPolicyV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `data_opentelekomcloud_hss_hosts_v5`

Refer to the Terraform Registry for docs: [`data_opentelekomcloud_hss_hosts_v5`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5).
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


class DataOpentelekomcloudHssHostsV5(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssHostsV5.DataOpentelekomcloudHssHostsV5",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5 opentelekomcloud_hss_hosts_v5}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        agent_status: typing.Optional[builtins.str] = None,
        asset_value: typing.Optional[builtins.str] = None,
        detect_result: typing.Optional[builtins.str] = None,
        group_id: typing.Optional[builtins.str] = None,
        host_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        os_type: typing.Optional[builtins.str] = None,
        policy_group_id: typing.Optional[builtins.str] = None,
        protect_charging_mode: typing.Optional[builtins.str] = None,
        protect_status: typing.Optional[builtins.str] = None,
        protect_version: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5 opentelekomcloud_hss_hosts_v5} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param agent_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#agent_status DataOpentelekomcloudHssHostsV5#agent_status}.
        :param asset_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#asset_value DataOpentelekomcloudHssHostsV5#asset_value}.
        :param detect_result: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#detect_result DataOpentelekomcloudHssHostsV5#detect_result}.
        :param group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#group_id DataOpentelekomcloudHssHostsV5#group_id}.
        :param host_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#host_id DataOpentelekomcloudHssHostsV5#host_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#id DataOpentelekomcloudHssHostsV5#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#name DataOpentelekomcloudHssHostsV5#name}.
        :param os_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#os_type DataOpentelekomcloudHssHostsV5#os_type}.
        :param policy_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#policy_group_id DataOpentelekomcloudHssHostsV5#policy_group_id}.
        :param protect_charging_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#protect_charging_mode DataOpentelekomcloudHssHostsV5#protect_charging_mode}.
        :param protect_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#protect_status DataOpentelekomcloudHssHostsV5#protect_status}.
        :param protect_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#protect_version DataOpentelekomcloudHssHostsV5#protect_version}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#status DataOpentelekomcloudHssHostsV5#status}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bde849010582320a62365525b5a63255ae32470bd7f05c608ff5ef992cf99c7e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpentelekomcloudHssHostsV5Config(
            agent_status=agent_status,
            asset_value=asset_value,
            detect_result=detect_result,
            group_id=group_id,
            host_id=host_id,
            id=id,
            name=name,
            os_type=os_type,
            policy_group_id=policy_group_id,
            protect_charging_mode=protect_charging_mode,
            protect_status=protect_status,
            protect_version=protect_version,
            status=status,
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
        '''Generates CDKTF code for importing a DataOpentelekomcloudHssHostsV5 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpentelekomcloudHssHostsV5 to import.
        :param import_from_id: The id of the existing DataOpentelekomcloudHssHostsV5 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpentelekomcloudHssHostsV5 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd9fbc66760b88b930e200268ec560155399cd0b6f214be596c7dfd9d94dc68)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAgentStatus")
    def reset_agent_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgentStatus", []))

    @jsii.member(jsii_name="resetAssetValue")
    def reset_asset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssetValue", []))

    @jsii.member(jsii_name="resetDetectResult")
    def reset_detect_result(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDetectResult", []))

    @jsii.member(jsii_name="resetGroupId")
    def reset_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupId", []))

    @jsii.member(jsii_name="resetHostId")
    def reset_host_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOsType")
    def reset_os_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsType", []))

    @jsii.member(jsii_name="resetPolicyGroupId")
    def reset_policy_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyGroupId", []))

    @jsii.member(jsii_name="resetProtectChargingMode")
    def reset_protect_charging_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtectChargingMode", []))

    @jsii.member(jsii_name="resetProtectStatus")
    def reset_protect_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtectStatus", []))

    @jsii.member(jsii_name="resetProtectVersion")
    def reset_protect_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtectVersion", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

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
    @jsii.member(jsii_name="hosts")
    def hosts(self) -> "DataOpentelekomcloudHssHostsV5HostsList":
        return typing.cast("DataOpentelekomcloudHssHostsV5HostsList", jsii.get(self, "hosts"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="agentStatusInput")
    def agent_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="assetValueInput")
    def asset_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assetValueInput"))

    @builtins.property
    @jsii.member(jsii_name="detectResultInput")
    def detect_result_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "detectResultInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="hostIdInput")
    def host_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="osTypeInput")
    def os_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="policyGroupIdInput")
    def policy_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="protectChargingModeInput")
    def protect_charging_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protectChargingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="protectStatusInput")
    def protect_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protectStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="protectVersionInput")
    def protect_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protectVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="agentStatus")
    def agent_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentStatus"))

    @agent_status.setter
    def agent_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bea23cd26dff280ef69d007eaac0ccd148aa3ffe3770154ec2b4ca06b7cc42d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="assetValue")
    def asset_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assetValue"))

    @asset_value.setter
    def asset_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d4d26bc0c931bb521d72b58506ee6b0fcbfe852fac7008f15b5f817484f181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="detectResult")
    def detect_result(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "detectResult"))

    @detect_result.setter
    def detect_result(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__078e4ba8f2de071b680e7e08b925987803572a122284a19be6a127557318c918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectResult", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3abc4097cbf6b033ce3bd74cf04493d60747260412def69295d14e31126ede45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostId")
    def host_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostId"))

    @host_id.setter
    def host_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42b4e88403a73b6016a6f204f7d50a1c4f3787323446d8f8ae801afe233e16b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__031956269377168ae05cf60fa427075949039ba57615ab513e087085b808bccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba0781f991cc11043230b4f3adb67d97a521231e8b38c40d97113add1059bd26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @os_type.setter
    def os_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__129f68ae413e5c58d55f6e66fb8fc818254457b9f8023887378d805a9209d07e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyGroupId")
    def policy_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyGroupId"))

    @policy_group_id.setter
    def policy_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__424f6f8e6cfbf69150ff61ca8ceed0b15774cf13e1b5fb4058aaf13b58f677a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protectChargingMode")
    def protect_charging_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectChargingMode"))

    @protect_charging_mode.setter
    def protect_charging_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c6f0a5f560536dc75d9753f9fd974c4753e2430914bdf97cf93c2aad2b302aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protectChargingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protectStatus")
    def protect_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectStatus"))

    @protect_status.setter
    def protect_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d2599c25b9dcbdcb80178547cdea1465c66913dbba3780a003f63ad060957d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protectStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protectVersion")
    def protect_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectVersion"))

    @protect_version.setter
    def protect_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1db00fe45469ac9161f425f7a6a16599f602af4bd967192e80f4dc03a681f9f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protectVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d72ad17295288862148849eb127d0c011cb9da984d7a3a65868d37d3ace1c192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssHostsV5.DataOpentelekomcloudHssHostsV5Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "agent_status": "agentStatus",
        "asset_value": "assetValue",
        "detect_result": "detectResult",
        "group_id": "groupId",
        "host_id": "hostId",
        "id": "id",
        "name": "name",
        "os_type": "osType",
        "policy_group_id": "policyGroupId",
        "protect_charging_mode": "protectChargingMode",
        "protect_status": "protectStatus",
        "protect_version": "protectVersion",
        "status": "status",
    },
)
class DataOpentelekomcloudHssHostsV5Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        agent_status: typing.Optional[builtins.str] = None,
        asset_value: typing.Optional[builtins.str] = None,
        detect_result: typing.Optional[builtins.str] = None,
        group_id: typing.Optional[builtins.str] = None,
        host_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        os_type: typing.Optional[builtins.str] = None,
        policy_group_id: typing.Optional[builtins.str] = None,
        protect_charging_mode: typing.Optional[builtins.str] = None,
        protect_status: typing.Optional[builtins.str] = None,
        protect_version: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param agent_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#agent_status DataOpentelekomcloudHssHostsV5#agent_status}.
        :param asset_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#asset_value DataOpentelekomcloudHssHostsV5#asset_value}.
        :param detect_result: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#detect_result DataOpentelekomcloudHssHostsV5#detect_result}.
        :param group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#group_id DataOpentelekomcloudHssHostsV5#group_id}.
        :param host_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#host_id DataOpentelekomcloudHssHostsV5#host_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#id DataOpentelekomcloudHssHostsV5#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#name DataOpentelekomcloudHssHostsV5#name}.
        :param os_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#os_type DataOpentelekomcloudHssHostsV5#os_type}.
        :param policy_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#policy_group_id DataOpentelekomcloudHssHostsV5#policy_group_id}.
        :param protect_charging_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#protect_charging_mode DataOpentelekomcloudHssHostsV5#protect_charging_mode}.
        :param protect_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#protect_status DataOpentelekomcloudHssHostsV5#protect_status}.
        :param protect_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#protect_version DataOpentelekomcloudHssHostsV5#protect_version}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#status DataOpentelekomcloudHssHostsV5#status}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44554964d40eb19104d52b821f89e174e6ddb783f0b5833f56a9700fe22383dd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument agent_status", value=agent_status, expected_type=type_hints["agent_status"])
            check_type(argname="argument asset_value", value=asset_value, expected_type=type_hints["asset_value"])
            check_type(argname="argument detect_result", value=detect_result, expected_type=type_hints["detect_result"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument host_id", value=host_id, expected_type=type_hints["host_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument os_type", value=os_type, expected_type=type_hints["os_type"])
            check_type(argname="argument policy_group_id", value=policy_group_id, expected_type=type_hints["policy_group_id"])
            check_type(argname="argument protect_charging_mode", value=protect_charging_mode, expected_type=type_hints["protect_charging_mode"])
            check_type(argname="argument protect_status", value=protect_status, expected_type=type_hints["protect_status"])
            check_type(argname="argument protect_version", value=protect_version, expected_type=type_hints["protect_version"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
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
        if agent_status is not None:
            self._values["agent_status"] = agent_status
        if asset_value is not None:
            self._values["asset_value"] = asset_value
        if detect_result is not None:
            self._values["detect_result"] = detect_result
        if group_id is not None:
            self._values["group_id"] = group_id
        if host_id is not None:
            self._values["host_id"] = host_id
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if os_type is not None:
            self._values["os_type"] = os_type
        if policy_group_id is not None:
            self._values["policy_group_id"] = policy_group_id
        if protect_charging_mode is not None:
            self._values["protect_charging_mode"] = protect_charging_mode
        if protect_status is not None:
            self._values["protect_status"] = protect_status
        if protect_version is not None:
            self._values["protect_version"] = protect_version
        if status is not None:
            self._values["status"] = status

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
    def agent_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#agent_status DataOpentelekomcloudHssHostsV5#agent_status}.'''
        result = self._values.get("agent_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#asset_value DataOpentelekomcloudHssHostsV5#asset_value}.'''
        result = self._values.get("asset_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def detect_result(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#detect_result DataOpentelekomcloudHssHostsV5#detect_result}.'''
        result = self._values.get("detect_result")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#group_id DataOpentelekomcloudHssHostsV5#group_id}.'''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#host_id DataOpentelekomcloudHssHostsV5#host_id}.'''
        result = self._values.get("host_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#id DataOpentelekomcloudHssHostsV5#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#name DataOpentelekomcloudHssHostsV5#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#os_type DataOpentelekomcloudHssHostsV5#os_type}.'''
        result = self._values.get("os_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#policy_group_id DataOpentelekomcloudHssHostsV5#policy_group_id}.'''
        result = self._values.get("policy_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protect_charging_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#protect_charging_mode DataOpentelekomcloudHssHostsV5#protect_charging_mode}.'''
        result = self._values.get("protect_charging_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protect_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#protect_status DataOpentelekomcloudHssHostsV5#protect_status}.'''
        result = self._values.get("protect_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protect_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#protect_version DataOpentelekomcloudHssHostsV5#protect_version}.'''
        result = self._values.get("protect_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_hosts_v5#status DataOpentelekomcloudHssHostsV5#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudHssHostsV5Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssHostsV5.DataOpentelekomcloudHssHostsV5Hosts",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudHssHostsV5Hosts:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudHssHostsV5Hosts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudHssHostsV5HostsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssHostsV5.DataOpentelekomcloudHssHostsV5HostsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef13738f1a81029ef288a7e702e73da3330b784fbbc0ebc6978d0e17476fefd4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudHssHostsV5HostsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d2f6b6b3814f8273f01a1e5abe02c9a62f90ddf815abb78a4fdab6e3014751)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudHssHostsV5HostsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e339355056b8beeb1b0b948a0a234790fc485d31ff983ce06487c968c11cfd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38f28e07ffaef31dd997ca9cab3312f0ad872ba20c3718196dbac7dc14c85208)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2effdffeb50e2451100fd96549eb53816852001dbade33f49ca44ce44f404491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudHssHostsV5HostsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssHostsV5.DataOpentelekomcloudHssHostsV5HostsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcf75c34d490412a9117cb46da97c2d0f56af5f4b76b94b5a4902ed871852a89)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="agentId")
    def agent_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentId"))

    @builtins.property
    @jsii.member(jsii_name="agentStatus")
    def agent_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentStatus"))

    @builtins.property
    @jsii.member(jsii_name="assetRiskNum")
    def asset_risk_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "assetRiskNum"))

    @builtins.property
    @jsii.member(jsii_name="assetValue")
    def asset_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assetValue"))

    @builtins.property
    @jsii.member(jsii_name="baselineRiskNum")
    def baseline_risk_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "baselineRiskNum"))

    @builtins.property
    @jsii.member(jsii_name="detectResult")
    def detect_result(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "detectResult"))

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="intrusionRiskNum")
    def intrusion_risk_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intrusionRiskNum"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @builtins.property
    @jsii.member(jsii_name="policyGroupId")
    def policy_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyGroupId"))

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @builtins.property
    @jsii.member(jsii_name="protectChargingMode")
    def protect_charging_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectChargingMode"))

    @builtins.property
    @jsii.member(jsii_name="protectStatus")
    def protect_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectStatus"))

    @builtins.property
    @jsii.member(jsii_name="protectVersion")
    def protect_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectVersion"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="vulnerabilityRiskNum")
    def vulnerability_risk_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vulnerabilityRiskNum"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataOpentelekomcloudHssHostsV5Hosts]:
        return typing.cast(typing.Optional[DataOpentelekomcloudHssHostsV5Hosts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudHssHostsV5Hosts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3840ebcabe6b1b7f6a25d12b25b8695b035f5427c7ff9d3140d71e650a0cac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataOpentelekomcloudHssHostsV5",
    "DataOpentelekomcloudHssHostsV5Config",
    "DataOpentelekomcloudHssHostsV5Hosts",
    "DataOpentelekomcloudHssHostsV5HostsList",
    "DataOpentelekomcloudHssHostsV5HostsOutputReference",
]

publication.publish()

def _typecheckingstub__bde849010582320a62365525b5a63255ae32470bd7f05c608ff5ef992cf99c7e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    agent_status: typing.Optional[builtins.str] = None,
    asset_value: typing.Optional[builtins.str] = None,
    detect_result: typing.Optional[builtins.str] = None,
    group_id: typing.Optional[builtins.str] = None,
    host_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    os_type: typing.Optional[builtins.str] = None,
    policy_group_id: typing.Optional[builtins.str] = None,
    protect_charging_mode: typing.Optional[builtins.str] = None,
    protect_status: typing.Optional[builtins.str] = None,
    protect_version: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__4fd9fbc66760b88b930e200268ec560155399cd0b6f214be596c7dfd9d94dc68(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea23cd26dff280ef69d007eaac0ccd148aa3ffe3770154ec2b4ca06b7cc42d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d4d26bc0c931bb521d72b58506ee6b0fcbfe852fac7008f15b5f817484f181(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078e4ba8f2de071b680e7e08b925987803572a122284a19be6a127557318c918(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3abc4097cbf6b033ce3bd74cf04493d60747260412def69295d14e31126ede45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b4e88403a73b6016a6f204f7d50a1c4f3787323446d8f8ae801afe233e16b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031956269377168ae05cf60fa427075949039ba57615ab513e087085b808bccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0781f991cc11043230b4f3adb67d97a521231e8b38c40d97113add1059bd26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__129f68ae413e5c58d55f6e66fb8fc818254457b9f8023887378d805a9209d07e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424f6f8e6cfbf69150ff61ca8ceed0b15774cf13e1b5fb4058aaf13b58f677a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6f0a5f560536dc75d9753f9fd974c4753e2430914bdf97cf93c2aad2b302aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d2599c25b9dcbdcb80178547cdea1465c66913dbba3780a003f63ad060957d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db00fe45469ac9161f425f7a6a16599f602af4bd967192e80f4dc03a681f9f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d72ad17295288862148849eb127d0c011cb9da984d7a3a65868d37d3ace1c192(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44554964d40eb19104d52b821f89e174e6ddb783f0b5833f56a9700fe22383dd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    agent_status: typing.Optional[builtins.str] = None,
    asset_value: typing.Optional[builtins.str] = None,
    detect_result: typing.Optional[builtins.str] = None,
    group_id: typing.Optional[builtins.str] = None,
    host_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    os_type: typing.Optional[builtins.str] = None,
    policy_group_id: typing.Optional[builtins.str] = None,
    protect_charging_mode: typing.Optional[builtins.str] = None,
    protect_status: typing.Optional[builtins.str] = None,
    protect_version: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef13738f1a81029ef288a7e702e73da3330b784fbbc0ebc6978d0e17476fefd4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d2f6b6b3814f8273f01a1e5abe02c9a62f90ddf815abb78a4fdab6e3014751(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e339355056b8beeb1b0b948a0a234790fc485d31ff983ce06487c968c11cfd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f28e07ffaef31dd997ca9cab3312f0ad872ba20c3718196dbac7dc14c85208(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2effdffeb50e2451100fd96549eb53816852001dbade33f49ca44ce44f404491(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcf75c34d490412a9117cb46da97c2d0f56af5f4b76b94b5a4902ed871852a89(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3840ebcabe6b1b7f6a25d12b25b8695b035f5427c7ff9d3140d71e650a0cac(
    value: typing.Optional[DataOpentelekomcloudHssHostsV5Hosts],
) -> None:
    """Type checking stubs"""
    pass

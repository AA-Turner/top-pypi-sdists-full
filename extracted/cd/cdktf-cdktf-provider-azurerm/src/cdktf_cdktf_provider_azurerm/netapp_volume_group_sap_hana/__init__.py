r'''
# `azurerm_netapp_volume_group_sap_hana`

Refer to the Terraform Registry for docs: [`azurerm_netapp_volume_group_sap_hana`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana).
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


class NetappVolumeGroupSapHana(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupSapHana.NetappVolumeGroupSapHana",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana azurerm_netapp_volume_group_sap_hana}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_name: builtins.str,
        application_identifier: builtins.str,
        group_description: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        volume: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetappVolumeGroupSapHanaVolume", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetappVolumeGroupSapHanaTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana azurerm_netapp_volume_group_sap_hana} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#account_name NetappVolumeGroupSapHana#account_name}.
        :param application_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#application_identifier NetappVolumeGroupSapHana#application_identifier}.
        :param group_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#group_description NetappVolumeGroupSapHana#group_description}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#location NetappVolumeGroupSapHana#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#name NetappVolumeGroupSapHana#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#resource_group_name NetappVolumeGroupSapHana#resource_group_name}.
        :param volume: volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#volume NetappVolumeGroupSapHana#volume}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#id NetappVolumeGroupSapHana#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#timeouts NetappVolumeGroupSapHana#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f0da41290dfa97a97e0e9fbc43af44c117d3ddeb2233933582f8a282c6ac41f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetappVolumeGroupSapHanaConfig(
            account_name=account_name,
            application_identifier=application_identifier,
            group_description=group_description,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            volume=volume,
            id=id,
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
        '''Generates CDKTF code for importing a NetappVolumeGroupSapHana resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetappVolumeGroupSapHana to import.
        :param import_from_id: The id of the existing NetappVolumeGroupSapHana that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetappVolumeGroupSapHana to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__befe5efb2839b0c55d8b6b034f3542f539966d2ddf1e039bc47d3acf31b1a8f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#create NetappVolumeGroupSapHana#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#delete NetappVolumeGroupSapHana#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#read NetappVolumeGroupSapHana#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#update NetappVolumeGroupSapHana#update}.
        '''
        value = NetappVolumeGroupSapHanaTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVolume")
    def put_volume(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetappVolumeGroupSapHanaVolume", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5000b5baf29d890bba0263cb9244a6ad33673877fcd609259a5fb6ccc63b8c36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolume", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetappVolumeGroupSapHanaTimeoutsOutputReference":
        return typing.cast("NetappVolumeGroupSapHanaTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="volume")
    def volume(self) -> "NetappVolumeGroupSapHanaVolumeList":
        return typing.cast("NetappVolumeGroupSapHanaVolumeList", jsii.get(self, "volume"))

    @builtins.property
    @jsii.member(jsii_name="accountNameInput")
    def account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationIdentifierInput")
    def application_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="groupDescriptionInput")
    def group_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetappVolumeGroupSapHanaTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetappVolumeGroupSapHanaTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeInput")
    def volume_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeGroupSapHanaVolume"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeGroupSapHanaVolume"]]], jsii.get(self, "volumeInput"))

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad76f873f78964483629d23a1eb4ba1d36bbe51c882716b7c8a9e2ed2f785ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationIdentifier")
    def application_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationIdentifier"))

    @application_identifier.setter
    def application_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2586cfc685fcaf7309a02c494695eadc663df38fb9c26741374dccf6fd24ea96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupDescription")
    def group_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupDescription"))

    @group_description.setter
    def group_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c239af6d2eda4b04429551f0a2e6a37ebc76391cb0a03354fcd4b74a7bf4f27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dddebcf115694a20bde1513c395bc519cda623edaeea3955660b7a0a092a373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ff33e731597c0fd4bdc8d9ad63de39f911cc03da37414ed97d551b3335b6989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1f05a7d2b265858e17d01d4508b14262d5abd1b5ac0eb564687c8d90beeaa36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae43215af2f4efc5e070d8838f303d6e09f7f884bba676ee00682a8fa232687)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupSapHana.NetappVolumeGroupSapHanaConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_name": "accountName",
        "application_identifier": "applicationIdentifier",
        "group_description": "groupDescription",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "volume": "volume",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class NetappVolumeGroupSapHanaConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_name: builtins.str,
        application_identifier: builtins.str,
        group_description: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        volume: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetappVolumeGroupSapHanaVolume", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetappVolumeGroupSapHanaTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#account_name NetappVolumeGroupSapHana#account_name}.
        :param application_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#application_identifier NetappVolumeGroupSapHana#application_identifier}.
        :param group_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#group_description NetappVolumeGroupSapHana#group_description}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#location NetappVolumeGroupSapHana#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#name NetappVolumeGroupSapHana#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#resource_group_name NetappVolumeGroupSapHana#resource_group_name}.
        :param volume: volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#volume NetappVolumeGroupSapHana#volume}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#id NetappVolumeGroupSapHana#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#timeouts NetappVolumeGroupSapHana#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = NetappVolumeGroupSapHanaTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30ca5f3df6d465e97ed4e99e0774bfdab3a91c197664ecdf9d44c10ac671069c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument application_identifier", value=application_identifier, expected_type=type_hints["application_identifier"])
            check_type(argname="argument group_description", value=group_description, expected_type=type_hints["group_description"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_name": account_name,
            "application_identifier": application_identifier,
            "group_description": group_description,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "volume": volume,
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
        if id is not None:
            self._values["id"] = id
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
    def account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#account_name NetappVolumeGroupSapHana#account_name}.'''
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#application_identifier NetappVolumeGroupSapHana#application_identifier}.'''
        result = self._values.get("application_identifier")
        assert result is not None, "Required property 'application_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_description(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#group_description NetappVolumeGroupSapHana#group_description}.'''
        result = self._values.get("group_description")
        assert result is not None, "Required property 'group_description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#location NetappVolumeGroupSapHana#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#name NetappVolumeGroupSapHana#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#resource_group_name NetappVolumeGroupSapHana#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeGroupSapHanaVolume"]]:
        '''volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#volume NetappVolumeGroupSapHana#volume}
        '''
        result = self._values.get("volume")
        assert result is not None, "Required property 'volume' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeGroupSapHanaVolume"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#id NetappVolumeGroupSapHana#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetappVolumeGroupSapHanaTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#timeouts NetappVolumeGroupSapHana#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetappVolumeGroupSapHanaTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeGroupSapHanaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupSapHana.NetappVolumeGroupSapHanaTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class NetappVolumeGroupSapHanaTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#create NetappVolumeGroupSapHana#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#delete NetappVolumeGroupSapHana#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#read NetappVolumeGroupSapHana#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#update NetappVolumeGroupSapHana#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722701c1dbcab9a091a0de5c0fae87220d132aa2190a45b6bb2a33de1d6181d8)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#create NetappVolumeGroupSapHana#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#delete NetappVolumeGroupSapHana#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#read NetappVolumeGroupSapHana#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#update NetappVolumeGroupSapHana#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeGroupSapHanaTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeGroupSapHanaTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupSapHana.NetappVolumeGroupSapHanaTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f597e67c95a81f7c672b6b77d8bd5335920ca328052e2abc82f00081aa5adf95)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5ab10fb1932d7fd17ca7573a37ff3472459bfdc8c7d74eaaf17de5af16c84c68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dc6db7a45148371d57fcdde8eda0708e945bc91890fb857bd291cdbe9f045ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37ffde5e1ba763c4d7c293e65403982fe20bc497d0436f45a73fdaad3e2cb33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c88c2188c3edf8314ac964675228c3f07a0d98574b33e1b8362aff1a01be3ad5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupSapHanaTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupSapHanaTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupSapHanaTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fa41a2ef1d3843f78eebc8ec4c5aeabffd17b155ef7b18e71de7f2d9af554f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupSapHana.NetappVolumeGroupSapHanaVolume",
    jsii_struct_bases=[],
    name_mapping={
        "capacity_pool_id": "capacityPoolId",
        "export_policy_rule": "exportPolicyRule",
        "name": "name",
        "protocols": "protocols",
        "security_style": "securityStyle",
        "service_level": "serviceLevel",
        "snapshot_directory_visible": "snapshotDirectoryVisible",
        "storage_quota_in_gb": "storageQuotaInGb",
        "subnet_id": "subnetId",
        "throughput_in_mibps": "throughputInMibps",
        "volume_path": "volumePath",
        "volume_spec_name": "volumeSpecName",
        "data_protection_replication": "dataProtectionReplication",
        "data_protection_snapshot_policy": "dataProtectionSnapshotPolicy",
        "proximity_placement_group_id": "proximityPlacementGroupId",
        "tags": "tags",
    },
)
class NetappVolumeGroupSapHanaVolume:
    def __init__(
        self,
        *,
        capacity_pool_id: builtins.str,
        export_policy_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetappVolumeGroupSapHanaVolumeExportPolicyRule", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        protocols: typing.Sequence[builtins.str],
        security_style: builtins.str,
        service_level: builtins.str,
        snapshot_directory_visible: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        storage_quota_in_gb: jsii.Number,
        subnet_id: builtins.str,
        throughput_in_mibps: jsii.Number,
        volume_path: builtins.str,
        volume_spec_name: builtins.str,
        data_protection_replication: typing.Optional[typing.Union["NetappVolumeGroupSapHanaVolumeDataProtectionReplication", typing.Dict[builtins.str, typing.Any]]] = None,
        data_protection_snapshot_policy: typing.Optional[typing.Union["NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        proximity_placement_group_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param capacity_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#capacity_pool_id NetappVolumeGroupSapHana#capacity_pool_id}.
        :param export_policy_rule: export_policy_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#export_policy_rule NetappVolumeGroupSapHana#export_policy_rule}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#name NetappVolumeGroupSapHana#name}.
        :param protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#protocols NetappVolumeGroupSapHana#protocols}.
        :param security_style: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#security_style NetappVolumeGroupSapHana#security_style}.
        :param service_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#service_level NetappVolumeGroupSapHana#service_level}.
        :param snapshot_directory_visible: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#snapshot_directory_visible NetappVolumeGroupSapHana#snapshot_directory_visible}.
        :param storage_quota_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#storage_quota_in_gb NetappVolumeGroupSapHana#storage_quota_in_gb}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#subnet_id NetappVolumeGroupSapHana#subnet_id}.
        :param throughput_in_mibps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#throughput_in_mibps NetappVolumeGroupSapHana#throughput_in_mibps}.
        :param volume_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#volume_path NetappVolumeGroupSapHana#volume_path}.
        :param volume_spec_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#volume_spec_name NetappVolumeGroupSapHana#volume_spec_name}.
        :param data_protection_replication: data_protection_replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#data_protection_replication NetappVolumeGroupSapHana#data_protection_replication}
        :param data_protection_snapshot_policy: data_protection_snapshot_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#data_protection_snapshot_policy NetappVolumeGroupSapHana#data_protection_snapshot_policy}
        :param proximity_placement_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#proximity_placement_group_id NetappVolumeGroupSapHana#proximity_placement_group_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#tags NetappVolumeGroupSapHana#tags}.
        '''
        if isinstance(data_protection_replication, dict):
            data_protection_replication = NetappVolumeGroupSapHanaVolumeDataProtectionReplication(**data_protection_replication)
        if isinstance(data_protection_snapshot_policy, dict):
            data_protection_snapshot_policy = NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicy(**data_protection_snapshot_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd8faf965e63c696a68a3b5a1a9b3611bd5f5959d6e9f8da697a88efa1f3b6a)
            check_type(argname="argument capacity_pool_id", value=capacity_pool_id, expected_type=type_hints["capacity_pool_id"])
            check_type(argname="argument export_policy_rule", value=export_policy_rule, expected_type=type_hints["export_policy_rule"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
            check_type(argname="argument security_style", value=security_style, expected_type=type_hints["security_style"])
            check_type(argname="argument service_level", value=service_level, expected_type=type_hints["service_level"])
            check_type(argname="argument snapshot_directory_visible", value=snapshot_directory_visible, expected_type=type_hints["snapshot_directory_visible"])
            check_type(argname="argument storage_quota_in_gb", value=storage_quota_in_gb, expected_type=type_hints["storage_quota_in_gb"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument throughput_in_mibps", value=throughput_in_mibps, expected_type=type_hints["throughput_in_mibps"])
            check_type(argname="argument volume_path", value=volume_path, expected_type=type_hints["volume_path"])
            check_type(argname="argument volume_spec_name", value=volume_spec_name, expected_type=type_hints["volume_spec_name"])
            check_type(argname="argument data_protection_replication", value=data_protection_replication, expected_type=type_hints["data_protection_replication"])
            check_type(argname="argument data_protection_snapshot_policy", value=data_protection_snapshot_policy, expected_type=type_hints["data_protection_snapshot_policy"])
            check_type(argname="argument proximity_placement_group_id", value=proximity_placement_group_id, expected_type=type_hints["proximity_placement_group_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity_pool_id": capacity_pool_id,
            "export_policy_rule": export_policy_rule,
            "name": name,
            "protocols": protocols,
            "security_style": security_style,
            "service_level": service_level,
            "snapshot_directory_visible": snapshot_directory_visible,
            "storage_quota_in_gb": storage_quota_in_gb,
            "subnet_id": subnet_id,
            "throughput_in_mibps": throughput_in_mibps,
            "volume_path": volume_path,
            "volume_spec_name": volume_spec_name,
        }
        if data_protection_replication is not None:
            self._values["data_protection_replication"] = data_protection_replication
        if data_protection_snapshot_policy is not None:
            self._values["data_protection_snapshot_policy"] = data_protection_snapshot_policy
        if proximity_placement_group_id is not None:
            self._values["proximity_placement_group_id"] = proximity_placement_group_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def capacity_pool_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#capacity_pool_id NetappVolumeGroupSapHana#capacity_pool_id}.'''
        result = self._values.get("capacity_pool_id")
        assert result is not None, "Required property 'capacity_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def export_policy_rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeGroupSapHanaVolumeExportPolicyRule"]]:
        '''export_policy_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#export_policy_rule NetappVolumeGroupSapHana#export_policy_rule}
        '''
        result = self._values.get("export_policy_rule")
        assert result is not None, "Required property 'export_policy_rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeGroupSapHanaVolumeExportPolicyRule"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#name NetappVolumeGroupSapHana#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocols(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#protocols NetappVolumeGroupSapHana#protocols}.'''
        result = self._values.get("protocols")
        assert result is not None, "Required property 'protocols' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def security_style(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#security_style NetappVolumeGroupSapHana#security_style}.'''
        result = self._values.get("security_style")
        assert result is not None, "Required property 'security_style' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_level(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#service_level NetappVolumeGroupSapHana#service_level}.'''
        result = self._values.get("service_level")
        assert result is not None, "Required property 'service_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def snapshot_directory_visible(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#snapshot_directory_visible NetappVolumeGroupSapHana#snapshot_directory_visible}.'''
        result = self._values.get("snapshot_directory_visible")
        assert result is not None, "Required property 'snapshot_directory_visible' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def storage_quota_in_gb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#storage_quota_in_gb NetappVolumeGroupSapHana#storage_quota_in_gb}.'''
        result = self._values.get("storage_quota_in_gb")
        assert result is not None, "Required property 'storage_quota_in_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#subnet_id NetappVolumeGroupSapHana#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def throughput_in_mibps(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#throughput_in_mibps NetappVolumeGroupSapHana#throughput_in_mibps}.'''
        result = self._values.get("throughput_in_mibps")
        assert result is not None, "Required property 'throughput_in_mibps' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def volume_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#volume_path NetappVolumeGroupSapHana#volume_path}.'''
        result = self._values.get("volume_path")
        assert result is not None, "Required property 'volume_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume_spec_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#volume_spec_name NetappVolumeGroupSapHana#volume_spec_name}.'''
        result = self._values.get("volume_spec_name")
        assert result is not None, "Required property 'volume_spec_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_protection_replication(
        self,
    ) -> typing.Optional["NetappVolumeGroupSapHanaVolumeDataProtectionReplication"]:
        '''data_protection_replication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#data_protection_replication NetappVolumeGroupSapHana#data_protection_replication}
        '''
        result = self._values.get("data_protection_replication")
        return typing.cast(typing.Optional["NetappVolumeGroupSapHanaVolumeDataProtectionReplication"], result)

    @builtins.property
    def data_protection_snapshot_policy(
        self,
    ) -> typing.Optional["NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicy"]:
        '''data_protection_snapshot_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#data_protection_snapshot_policy NetappVolumeGroupSapHana#data_protection_snapshot_policy}
        '''
        result = self._values.get("data_protection_snapshot_policy")
        return typing.cast(typing.Optional["NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicy"], result)

    @builtins.property
    def proximity_placement_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#proximity_placement_group_id NetappVolumeGroupSapHana#proximity_placement_group_id}.'''
        result = self._values.get("proximity_placement_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#tags NetappVolumeGroupSapHana#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeGroupSapHanaVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupSapHana.NetappVolumeGroupSapHanaVolumeDataProtectionReplication",
    jsii_struct_bases=[],
    name_mapping={
        "remote_volume_location": "remoteVolumeLocation",
        "remote_volume_resource_id": "remoteVolumeResourceId",
        "replication_frequency": "replicationFrequency",
        "endpoint_type": "endpointType",
    },
)
class NetappVolumeGroupSapHanaVolumeDataProtectionReplication:
    def __init__(
        self,
        *,
        remote_volume_location: builtins.str,
        remote_volume_resource_id: builtins.str,
        replication_frequency: builtins.str,
        endpoint_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param remote_volume_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#remote_volume_location NetappVolumeGroupSapHana#remote_volume_location}.
        :param remote_volume_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#remote_volume_resource_id NetappVolumeGroupSapHana#remote_volume_resource_id}.
        :param replication_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#replication_frequency NetappVolumeGroupSapHana#replication_frequency}.
        :param endpoint_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#endpoint_type NetappVolumeGroupSapHana#endpoint_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c09995b52ef9687e7fa985b468d8280e34ecf751305851d0542cb41563e5b5d)
            check_type(argname="argument remote_volume_location", value=remote_volume_location, expected_type=type_hints["remote_volume_location"])
            check_type(argname="argument remote_volume_resource_id", value=remote_volume_resource_id, expected_type=type_hints["remote_volume_resource_id"])
            check_type(argname="argument replication_frequency", value=replication_frequency, expected_type=type_hints["replication_frequency"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "remote_volume_location": remote_volume_location,
            "remote_volume_resource_id": remote_volume_resource_id,
            "replication_frequency": replication_frequency,
        }
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type

    @builtins.property
    def remote_volume_location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#remote_volume_location NetappVolumeGroupSapHana#remote_volume_location}.'''
        result = self._values.get("remote_volume_location")
        assert result is not None, "Required property 'remote_volume_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def remote_volume_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#remote_volume_resource_id NetappVolumeGroupSapHana#remote_volume_resource_id}.'''
        result = self._values.get("remote_volume_resource_id")
        assert result is not None, "Required property 'remote_volume_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replication_frequency(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#replication_frequency NetappVolumeGroupSapHana#replication_frequency}.'''
        result = self._values.get("replication_frequency")
        assert result is not None, "Required property 'replication_frequency' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#endpoint_type NetappVolumeGroupSapHana#endpoint_type}.'''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeGroupSapHanaVolumeDataProtectionReplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeGroupSapHanaVolumeDataProtectionReplicationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupSapHana.NetappVolumeGroupSapHanaVolumeDataProtectionReplicationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b9e083e39a6fab41a43fb7f36097d98c7a32e9dc70842a064b540634439779f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEndpointType")
    def reset_endpoint_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointType", []))

    @builtins.property
    @jsii.member(jsii_name="endpointTypeInput")
    def endpoint_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteVolumeLocationInput")
    def remote_volume_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteVolumeLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteVolumeResourceIdInput")
    def remote_volume_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteVolumeResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationFrequencyInput")
    def replication_frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replicationFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointType")
    def endpoint_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointType"))

    @endpoint_type.setter
    def endpoint_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b12b7ea7b4f5282bc06c78b5763407875d32220127ecc8c504e0795ac97d697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteVolumeLocation")
    def remote_volume_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteVolumeLocation"))

    @remote_volume_location.setter
    def remote_volume_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be014ac4e603cbd119d73d4a1fa3cdc9ae6056bf98aa97d94af3e00c0bce61c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteVolumeLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteVolumeResourceId")
    def remote_volume_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteVolumeResourceId"))

    @remote_volume_resource_id.setter
    def remote_volume_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e60ca4259a8d798e093fb86ee124ce96fd7bdde8eb380b572320cd81e60a2aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteVolumeResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicationFrequency")
    def replication_frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replicationFrequency"))

    @replication_frequency.setter
    def replication_frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d08f65eb17c2476582308dba87e82b94e34b458b05e7fca35cc17337631b52d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetappVolumeGroupSapHanaVolumeDataProtectionReplication]:
        return typing.cast(typing.Optional[NetappVolumeGroupSapHanaVolumeDataProtectionReplication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappVolumeGroupSapHanaVolumeDataProtectionReplication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b811397ffcaa60ea9d0597f0be01bf9f5ce3239b10a60ec9da21684f267dc53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupSapHana.NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicy",
    jsii_struct_bases=[],
    name_mapping={"snapshot_policy_id": "snapshotPolicyId"},
)
class NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicy:
    def __init__(self, *, snapshot_policy_id: builtins.str) -> None:
        '''
        :param snapshot_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#snapshot_policy_id NetappVolumeGroupSapHana#snapshot_policy_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d9a505cea7c7bebce83590841216af1432e5763a74d6de31cf2b2c68d94ab8)
            check_type(argname="argument snapshot_policy_id", value=snapshot_policy_id, expected_type=type_hints["snapshot_policy_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "snapshot_policy_id": snapshot_policy_id,
        }

    @builtins.property
    def snapshot_policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#snapshot_policy_id NetappVolumeGroupSapHana#snapshot_policy_id}.'''
        result = self._values.get("snapshot_policy_id")
        assert result is not None, "Required property 'snapshot_policy_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupSapHana.NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b932e24f2618dcd9e99fbfdb21aa29ccae30f551d661d71f092d86ebd418a45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="snapshotPolicyIdInput")
    def snapshot_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotPolicyId")
    def snapshot_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshotPolicyId"))

    @snapshot_policy_id.setter
    def snapshot_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f130e9d2296949455ce4ded95a87245942fa9f5cdb74635eefea6ddc05296525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicy]:
        return typing.cast(typing.Optional[NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c1e6ad2634845a121912c8cac2741ff1f10b5d08fa6e1fd554edad2a0efd58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupSapHana.NetappVolumeGroupSapHanaVolumeExportPolicyRule",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_clients": "allowedClients",
        "nfsv3_enabled": "nfsv3Enabled",
        "nfsv41_enabled": "nfsv41Enabled",
        "rule_index": "ruleIndex",
        "root_access_enabled": "rootAccessEnabled",
        "unix_read_only": "unixReadOnly",
        "unix_read_write": "unixReadWrite",
    },
)
class NetappVolumeGroupSapHanaVolumeExportPolicyRule:
    def __init__(
        self,
        *,
        allowed_clients: builtins.str,
        nfsv3_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        nfsv41_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        rule_index: jsii.Number,
        root_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        unix_read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        unix_read_write: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_clients: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#allowed_clients NetappVolumeGroupSapHana#allowed_clients}.
        :param nfsv3_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#nfsv3_enabled NetappVolumeGroupSapHana#nfsv3_enabled}.
        :param nfsv41_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#nfsv41_enabled NetappVolumeGroupSapHana#nfsv41_enabled}.
        :param rule_index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#rule_index NetappVolumeGroupSapHana#rule_index}.
        :param root_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#root_access_enabled NetappVolumeGroupSapHana#root_access_enabled}.
        :param unix_read_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#unix_read_only NetappVolumeGroupSapHana#unix_read_only}.
        :param unix_read_write: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#unix_read_write NetappVolumeGroupSapHana#unix_read_write}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__634dd91ce87ce48c150e8ff44f55eb193a28bc2c91b8d6222f70dae42e400af3)
            check_type(argname="argument allowed_clients", value=allowed_clients, expected_type=type_hints["allowed_clients"])
            check_type(argname="argument nfsv3_enabled", value=nfsv3_enabled, expected_type=type_hints["nfsv3_enabled"])
            check_type(argname="argument nfsv41_enabled", value=nfsv41_enabled, expected_type=type_hints["nfsv41_enabled"])
            check_type(argname="argument rule_index", value=rule_index, expected_type=type_hints["rule_index"])
            check_type(argname="argument root_access_enabled", value=root_access_enabled, expected_type=type_hints["root_access_enabled"])
            check_type(argname="argument unix_read_only", value=unix_read_only, expected_type=type_hints["unix_read_only"])
            check_type(argname="argument unix_read_write", value=unix_read_write, expected_type=type_hints["unix_read_write"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_clients": allowed_clients,
            "nfsv3_enabled": nfsv3_enabled,
            "nfsv41_enabled": nfsv41_enabled,
            "rule_index": rule_index,
        }
        if root_access_enabled is not None:
            self._values["root_access_enabled"] = root_access_enabled
        if unix_read_only is not None:
            self._values["unix_read_only"] = unix_read_only
        if unix_read_write is not None:
            self._values["unix_read_write"] = unix_read_write

    @builtins.property
    def allowed_clients(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#allowed_clients NetappVolumeGroupSapHana#allowed_clients}.'''
        result = self._values.get("allowed_clients")
        assert result is not None, "Required property 'allowed_clients' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nfsv3_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#nfsv3_enabled NetappVolumeGroupSapHana#nfsv3_enabled}.'''
        result = self._values.get("nfsv3_enabled")
        assert result is not None, "Required property 'nfsv3_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def nfsv41_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#nfsv41_enabled NetappVolumeGroupSapHana#nfsv41_enabled}.'''
        result = self._values.get("nfsv41_enabled")
        assert result is not None, "Required property 'nfsv41_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def rule_index(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#rule_index NetappVolumeGroupSapHana#rule_index}.'''
        result = self._values.get("rule_index")
        assert result is not None, "Required property 'rule_index' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def root_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#root_access_enabled NetappVolumeGroupSapHana#root_access_enabled}.'''
        result = self._values.get("root_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def unix_read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#unix_read_only NetappVolumeGroupSapHana#unix_read_only}.'''
        result = self._values.get("unix_read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def unix_read_write(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#unix_read_write NetappVolumeGroupSapHana#unix_read_write}.'''
        result = self._values.get("unix_read_write")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeGroupSapHanaVolumeExportPolicyRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeGroupSapHanaVolumeExportPolicyRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupSapHana.NetappVolumeGroupSapHanaVolumeExportPolicyRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dac409954226896c29137cdb39095f9a91998877b20e74114b17267454c7ffc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetappVolumeGroupSapHanaVolumeExportPolicyRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e5b13a9effa4307da99d42022bd92f917de2f94c926ef5f38ceba5a617b7e4d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetappVolumeGroupSapHanaVolumeExportPolicyRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebec04459d5b90f1c30111207957fb7286e2011e6d08f9d7a35c4c630f54bb99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93402a0a54e40149e54ac16ad4c96097c0ecf258fdb1551af33d0e45bf6f4a6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__272da5cf75e7884cc7858bdbd0d256da99de3314a952dbcd6e0911245d89197a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupSapHanaVolumeExportPolicyRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupSapHanaVolumeExportPolicyRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupSapHanaVolumeExportPolicyRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b36c9434094d87f02168e631206126e0f8ae5b6abb3a5c66a33317f03d82031d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetappVolumeGroupSapHanaVolumeExportPolicyRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupSapHana.NetappVolumeGroupSapHanaVolumeExportPolicyRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__414ff96ea53b83b8e29fd3c1a86853c85769184c54498b44ab87bb3d6d7da292)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetRootAccessEnabled")
    def reset_root_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootAccessEnabled", []))

    @jsii.member(jsii_name="resetUnixReadOnly")
    def reset_unix_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnixReadOnly", []))

    @jsii.member(jsii_name="resetUnixReadWrite")
    def reset_unix_read_write(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnixReadWrite", []))

    @builtins.property
    @jsii.member(jsii_name="allowedClientsInput")
    def allowed_clients_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowedClientsInput"))

    @builtins.property
    @jsii.member(jsii_name="nfsv3EnabledInput")
    def nfsv3_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nfsv3EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nfsv41EnabledInput")
    def nfsv41_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nfsv41EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="rootAccessEnabledInput")
    def root_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rootAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleIndexInput")
    def rule_index_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ruleIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="unixReadOnlyInput")
    def unix_read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "unixReadOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="unixReadWriteInput")
    def unix_read_write_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "unixReadWriteInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedClients")
    def allowed_clients(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowedClients"))

    @allowed_clients.setter
    def allowed_clients(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70173ef41f0a616adacc7a8dc45cfaabafa5a6aec418a341083afb25f79554c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedClients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nfsv3Enabled")
    def nfsv3_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nfsv3Enabled"))

    @nfsv3_enabled.setter
    def nfsv3_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3797eb2f845d352276fcc2f4ba124cef9ceacc543622917f0c88bc9b02ae0c2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nfsv3Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nfsv41Enabled")
    def nfsv41_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nfsv41Enabled"))

    @nfsv41_enabled.setter
    def nfsv41_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dbcdb732fdf80caa4c0e221b9ce35607ea48d526ae2462af6971495785f0b34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nfsv41Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootAccessEnabled")
    def root_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rootAccessEnabled"))

    @root_access_enabled.setter
    def root_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014cc849e50a95c00853e819d218b632b861400f855bdf39d0468c5ce67d5c4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleIndex")
    def rule_index(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ruleIndex"))

    @rule_index.setter
    def rule_index(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5014bed0ba87d5ecb49247962d6289d6b6d8e0fc223155641143f5e0ba0bb94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unixReadOnly")
    def unix_read_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "unixReadOnly"))

    @unix_read_only.setter
    def unix_read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa77499dd8ea2805f29b12d36b7010c22070d53f6f809cdfd87dc2b520620680)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unixReadOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unixReadWrite")
    def unix_read_write(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "unixReadWrite"))

    @unix_read_write.setter
    def unix_read_write(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc5bc4df994de1f7886a3700624bf24e32093d7617f1472b6407b53eb1b7b2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unixReadWrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupSapHanaVolumeExportPolicyRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupSapHanaVolumeExportPolicyRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupSapHanaVolumeExportPolicyRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8ac770f860b0ba7f0c6d1b93676434d2cce9cadadce73f7964879b4c5e974b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetappVolumeGroupSapHanaVolumeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupSapHana.NetappVolumeGroupSapHanaVolumeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8afd8464e788c6a924456fe2647706f6250285476f7f861322e40c3a96f6887)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetappVolumeGroupSapHanaVolumeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd925c193337e76bfcd27b00afc255f8a210541d9042205dd506cf9e0660839)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetappVolumeGroupSapHanaVolumeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__230d31ea3258072fc56fd4a716f99ced0b0770cecdb42efcbc468fb32bd15292)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abbff871af5452447370fcf57d250cdb47a44c14ddb5a8c003cc9e0154dbb120)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcda9b30025fe50faec23c31fa67c48a5f0b21898867b5734abfdf4fb81cb029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupSapHanaVolume]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupSapHanaVolume]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupSapHanaVolume]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc5941925f309ccae414173d420f119e0ffab67628e7e3befda65937c9e90a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetappVolumeGroupSapHanaVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupSapHana.NetappVolumeGroupSapHanaVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d69fabd6e352e2581efc99164b71249b8f30c91bfa5ed2cd3c3fe572a5dae34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDataProtectionReplication")
    def put_data_protection_replication(
        self,
        *,
        remote_volume_location: builtins.str,
        remote_volume_resource_id: builtins.str,
        replication_frequency: builtins.str,
        endpoint_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param remote_volume_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#remote_volume_location NetappVolumeGroupSapHana#remote_volume_location}.
        :param remote_volume_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#remote_volume_resource_id NetappVolumeGroupSapHana#remote_volume_resource_id}.
        :param replication_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#replication_frequency NetappVolumeGroupSapHana#replication_frequency}.
        :param endpoint_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#endpoint_type NetappVolumeGroupSapHana#endpoint_type}.
        '''
        value = NetappVolumeGroupSapHanaVolumeDataProtectionReplication(
            remote_volume_location=remote_volume_location,
            remote_volume_resource_id=remote_volume_resource_id,
            replication_frequency=replication_frequency,
            endpoint_type=endpoint_type,
        )

        return typing.cast(None, jsii.invoke(self, "putDataProtectionReplication", [value]))

    @jsii.member(jsii_name="putDataProtectionSnapshotPolicy")
    def put_data_protection_snapshot_policy(
        self,
        *,
        snapshot_policy_id: builtins.str,
    ) -> None:
        '''
        :param snapshot_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_sap_hana#snapshot_policy_id NetappVolumeGroupSapHana#snapshot_policy_id}.
        '''
        value = NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicy(
            snapshot_policy_id=snapshot_policy_id
        )

        return typing.cast(None, jsii.invoke(self, "putDataProtectionSnapshotPolicy", [value]))

    @jsii.member(jsii_name="putExportPolicyRule")
    def put_export_policy_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetappVolumeGroupSapHanaVolumeExportPolicyRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0e7bb77fcb24dc057d1225bc77aaefa5012d50ca8ff9b81dd6cbeca1a6b2df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExportPolicyRule", [value]))

    @jsii.member(jsii_name="resetDataProtectionReplication")
    def reset_data_protection_replication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataProtectionReplication", []))

    @jsii.member(jsii_name="resetDataProtectionSnapshotPolicy")
    def reset_data_protection_snapshot_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataProtectionSnapshotPolicy", []))

    @jsii.member(jsii_name="resetProximityPlacementGroupId")
    def reset_proximity_placement_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProximityPlacementGroupId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionReplication")
    def data_protection_replication(
        self,
    ) -> NetappVolumeGroupSapHanaVolumeDataProtectionReplicationOutputReference:
        return typing.cast(NetappVolumeGroupSapHanaVolumeDataProtectionReplicationOutputReference, jsii.get(self, "dataProtectionReplication"))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionSnapshotPolicy")
    def data_protection_snapshot_policy(
        self,
    ) -> NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicyOutputReference:
        return typing.cast(NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicyOutputReference, jsii.get(self, "dataProtectionSnapshotPolicy"))

    @builtins.property
    @jsii.member(jsii_name="exportPolicyRule")
    def export_policy_rule(self) -> NetappVolumeGroupSapHanaVolumeExportPolicyRuleList:
        return typing.cast(NetappVolumeGroupSapHanaVolumeExportPolicyRuleList, jsii.get(self, "exportPolicyRule"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="mountIpAddresses")
    def mount_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "mountIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="capacityPoolIdInput")
    def capacity_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "capacityPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionReplicationInput")
    def data_protection_replication_input(
        self,
    ) -> typing.Optional[NetappVolumeGroupSapHanaVolumeDataProtectionReplication]:
        return typing.cast(typing.Optional[NetappVolumeGroupSapHanaVolumeDataProtectionReplication], jsii.get(self, "dataProtectionReplicationInput"))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionSnapshotPolicyInput")
    def data_protection_snapshot_policy_input(
        self,
    ) -> typing.Optional[NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicy]:
        return typing.cast(typing.Optional[NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicy], jsii.get(self, "dataProtectionSnapshotPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="exportPolicyRuleInput")
    def export_policy_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupSapHanaVolumeExportPolicyRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupSapHanaVolumeExportPolicyRule]]], jsii.get(self, "exportPolicyRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolsInput")
    def protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "protocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="proximityPlacementGroupIdInput")
    def proximity_placement_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proximityPlacementGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="securityStyleInput")
    def security_style_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityStyleInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceLevelInput")
    def service_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotDirectoryVisibleInput")
    def snapshot_directory_visible_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "snapshotDirectoryVisibleInput"))

    @builtins.property
    @jsii.member(jsii_name="storageQuotaInGbInput")
    def storage_quota_in_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageQuotaInGbInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="throughputInMibpsInput")
    def throughput_in_mibps_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throughputInMibpsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumePathInput")
    def volume_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumePathInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeSpecNameInput")
    def volume_spec_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeSpecNameInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityPoolId")
    def capacity_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "capacityPoolId"))

    @capacity_pool_id.setter
    def capacity_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90d04d3e6f29e10e38071296a95a5bcff4c9be79a1c2f0e1a11d0e65112c2a34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82ff29465c8ef621adb9cac8eeff4769c37a962c629a087f9fbebd61cd4de1f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocols")
    def protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "protocols"))

    @protocols.setter
    def protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39f0caca0815c2fcdd6f9df8c6f0f9395e97412945c7b32584e46d77d7cc09fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proximityPlacementGroupId")
    def proximity_placement_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proximityPlacementGroupId"))

    @proximity_placement_group_id.setter
    def proximity_placement_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bf4fc44cef2dc9cf12138f29ba0a91075e6ea014bf10e51be7805d744eac364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proximityPlacementGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityStyle")
    def security_style(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityStyle"))

    @security_style.setter
    def security_style(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9492fb7896da04c0e8f6ea6f519632cfec04f139546dc55da329a01df4b33a75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityStyle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceLevel")
    def service_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceLevel"))

    @service_level.setter
    def service_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d26b9fb418fc64ea95436d16cb0b8123dd26ca55d80d5fd91286fe205dced3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotDirectoryVisible")
    def snapshot_directory_visible(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "snapshotDirectoryVisible"))

    @snapshot_directory_visible.setter
    def snapshot_directory_visible(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c5d7b40fdb6dea303889342ff7ed82a169b3a215ddac4b1791c12055813839)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotDirectoryVisible", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageQuotaInGb")
    def storage_quota_in_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageQuotaInGb"))

    @storage_quota_in_gb.setter
    def storage_quota_in_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__735968c7e70ab8c43d24ea30d0eff065d8ddcdb1b8d4b1c836785fc45602af31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageQuotaInGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41c23223d2d9002d3f34541e90b80f8eb1147396d65bc294679d8e4ae0917f89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7880d78ceaa1b4786ed251cca6e9958917d5008f4078f9c9b64fe29202076842)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throughputInMibps")
    def throughput_in_mibps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throughputInMibps"))

    @throughput_in_mibps.setter
    def throughput_in_mibps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6e162f83f6ef242fcbb9cf19da6fb9a4b119d724438292b7c2967afda9d37dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughputInMibps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumePath")
    def volume_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumePath"))

    @volume_path.setter
    def volume_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be56764e2ba890171b01ea844a446148e8d5f84d659658fee5378bd9752d91f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeSpecName")
    def volume_spec_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeSpecName"))

    @volume_spec_name.setter
    def volume_spec_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8b10629baf3756ca39e2f887878bab57ee69ee1f93d54d516fcebae4095ab7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeSpecName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupSapHanaVolume]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupSapHanaVolume]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupSapHanaVolume]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc053cd30e06fa8ccb912e2a7d1b2e49b48e290a25315a5819f86e331fb079e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetappVolumeGroupSapHana",
    "NetappVolumeGroupSapHanaConfig",
    "NetappVolumeGroupSapHanaTimeouts",
    "NetappVolumeGroupSapHanaTimeoutsOutputReference",
    "NetappVolumeGroupSapHanaVolume",
    "NetappVolumeGroupSapHanaVolumeDataProtectionReplication",
    "NetappVolumeGroupSapHanaVolumeDataProtectionReplicationOutputReference",
    "NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicy",
    "NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicyOutputReference",
    "NetappVolumeGroupSapHanaVolumeExportPolicyRule",
    "NetappVolumeGroupSapHanaVolumeExportPolicyRuleList",
    "NetappVolumeGroupSapHanaVolumeExportPolicyRuleOutputReference",
    "NetappVolumeGroupSapHanaVolumeList",
    "NetappVolumeGroupSapHanaVolumeOutputReference",
]

publication.publish()

def _typecheckingstub__2f0da41290dfa97a97e0e9fbc43af44c117d3ddeb2233933582f8a282c6ac41f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_name: builtins.str,
    application_identifier: builtins.str,
    group_description: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    volume: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetappVolumeGroupSapHanaVolume, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetappVolumeGroupSapHanaTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__befe5efb2839b0c55d8b6b034f3542f539966d2ddf1e039bc47d3acf31b1a8f6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5000b5baf29d890bba0263cb9244a6ad33673877fcd609259a5fb6ccc63b8c36(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetappVolumeGroupSapHanaVolume, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad76f873f78964483629d23a1eb4ba1d36bbe51c882716b7c8a9e2ed2f785ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2586cfc685fcaf7309a02c494695eadc663df38fb9c26741374dccf6fd24ea96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c239af6d2eda4b04429551f0a2e6a37ebc76391cb0a03354fcd4b74a7bf4f27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dddebcf115694a20bde1513c395bc519cda623edaeea3955660b7a0a092a373(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff33e731597c0fd4bdc8d9ad63de39f911cc03da37414ed97d551b3335b6989(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1f05a7d2b265858e17d01d4508b14262d5abd1b5ac0eb564687c8d90beeaa36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae43215af2f4efc5e070d8838f303d6e09f7f884bba676ee00682a8fa232687(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ca5f3df6d465e97ed4e99e0774bfdab3a91c197664ecdf9d44c10ac671069c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_name: builtins.str,
    application_identifier: builtins.str,
    group_description: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    volume: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetappVolumeGroupSapHanaVolume, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetappVolumeGroupSapHanaTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722701c1dbcab9a091a0de5c0fae87220d132aa2190a45b6bb2a33de1d6181d8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f597e67c95a81f7c672b6b77d8bd5335920ca328052e2abc82f00081aa5adf95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab10fb1932d7fd17ca7573a37ff3472459bfdc8c7d74eaaf17de5af16c84c68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc6db7a45148371d57fcdde8eda0708e945bc91890fb857bd291cdbe9f045ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37ffde5e1ba763c4d7c293e65403982fe20bc497d0436f45a73fdaad3e2cb33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88c2188c3edf8314ac964675228c3f07a0d98574b33e1b8362aff1a01be3ad5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa41a2ef1d3843f78eebc8ec4c5aeabffd17b155ef7b18e71de7f2d9af554f1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupSapHanaTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd8faf965e63c696a68a3b5a1a9b3611bd5f5959d6e9f8da697a88efa1f3b6a(
    *,
    capacity_pool_id: builtins.str,
    export_policy_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetappVolumeGroupSapHanaVolumeExportPolicyRule, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    protocols: typing.Sequence[builtins.str],
    security_style: builtins.str,
    service_level: builtins.str,
    snapshot_directory_visible: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    storage_quota_in_gb: jsii.Number,
    subnet_id: builtins.str,
    throughput_in_mibps: jsii.Number,
    volume_path: builtins.str,
    volume_spec_name: builtins.str,
    data_protection_replication: typing.Optional[typing.Union[NetappVolumeGroupSapHanaVolumeDataProtectionReplication, typing.Dict[builtins.str, typing.Any]]] = None,
    data_protection_snapshot_policy: typing.Optional[typing.Union[NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    proximity_placement_group_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c09995b52ef9687e7fa985b468d8280e34ecf751305851d0542cb41563e5b5d(
    *,
    remote_volume_location: builtins.str,
    remote_volume_resource_id: builtins.str,
    replication_frequency: builtins.str,
    endpoint_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9e083e39a6fab41a43fb7f36097d98c7a32e9dc70842a064b540634439779f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b12b7ea7b4f5282bc06c78b5763407875d32220127ecc8c504e0795ac97d697(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be014ac4e603cbd119d73d4a1fa3cdc9ae6056bf98aa97d94af3e00c0bce61c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e60ca4259a8d798e093fb86ee124ce96fd7bdde8eb380b572320cd81e60a2aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d08f65eb17c2476582308dba87e82b94e34b458b05e7fca35cc17337631b52d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b811397ffcaa60ea9d0597f0be01bf9f5ce3239b10a60ec9da21684f267dc53(
    value: typing.Optional[NetappVolumeGroupSapHanaVolumeDataProtectionReplication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d9a505cea7c7bebce83590841216af1432e5763a74d6de31cf2b2c68d94ab8(
    *,
    snapshot_policy_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b932e24f2618dcd9e99fbfdb21aa29ccae30f551d661d71f092d86ebd418a45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f130e9d2296949455ce4ded95a87245942fa9f5cdb74635eefea6ddc05296525(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c1e6ad2634845a121912c8cac2741ff1f10b5d08fa6e1fd554edad2a0efd58(
    value: typing.Optional[NetappVolumeGroupSapHanaVolumeDataProtectionSnapshotPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__634dd91ce87ce48c150e8ff44f55eb193a28bc2c91b8d6222f70dae42e400af3(
    *,
    allowed_clients: builtins.str,
    nfsv3_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    nfsv41_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    rule_index: jsii.Number,
    root_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    unix_read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    unix_read_write: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dac409954226896c29137cdb39095f9a91998877b20e74114b17267454c7ffc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e5b13a9effa4307da99d42022bd92f917de2f94c926ef5f38ceba5a617b7e4d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebec04459d5b90f1c30111207957fb7286e2011e6d08f9d7a35c4c630f54bb99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93402a0a54e40149e54ac16ad4c96097c0ecf258fdb1551af33d0e45bf6f4a6f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272da5cf75e7884cc7858bdbd0d256da99de3314a952dbcd6e0911245d89197a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36c9434094d87f02168e631206126e0f8ae5b6abb3a5c66a33317f03d82031d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupSapHanaVolumeExportPolicyRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__414ff96ea53b83b8e29fd3c1a86853c85769184c54498b44ab87bb3d6d7da292(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70173ef41f0a616adacc7a8dc45cfaabafa5a6aec418a341083afb25f79554c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3797eb2f845d352276fcc2f4ba124cef9ceacc543622917f0c88bc9b02ae0c2c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dbcdb732fdf80caa4c0e221b9ce35607ea48d526ae2462af6971495785f0b34(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014cc849e50a95c00853e819d218b632b861400f855bdf39d0468c5ce67d5c4f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5014bed0ba87d5ecb49247962d6289d6b6d8e0fc223155641143f5e0ba0bb94(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa77499dd8ea2805f29b12d36b7010c22070d53f6f809cdfd87dc2b520620680(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc5bc4df994de1f7886a3700624bf24e32093d7617f1472b6407b53eb1b7b2e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8ac770f860b0ba7f0c6d1b93676434d2cce9cadadce73f7964879b4c5e974b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupSapHanaVolumeExportPolicyRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8afd8464e788c6a924456fe2647706f6250285476f7f861322e40c3a96f6887(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd925c193337e76bfcd27b00afc255f8a210541d9042205dd506cf9e0660839(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230d31ea3258072fc56fd4a716f99ced0b0770cecdb42efcbc468fb32bd15292(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abbff871af5452447370fcf57d250cdb47a44c14ddb5a8c003cc9e0154dbb120(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcda9b30025fe50faec23c31fa67c48a5f0b21898867b5734abfdf4fb81cb029(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc5941925f309ccae414173d420f119e0ffab67628e7e3befda65937c9e90a18(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupSapHanaVolume]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d69fabd6e352e2581efc99164b71249b8f30c91bfa5ed2cd3c3fe572a5dae34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0e7bb77fcb24dc057d1225bc77aaefa5012d50ca8ff9b81dd6cbeca1a6b2df(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetappVolumeGroupSapHanaVolumeExportPolicyRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90d04d3e6f29e10e38071296a95a5bcff4c9be79a1c2f0e1a11d0e65112c2a34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82ff29465c8ef621adb9cac8eeff4769c37a962c629a087f9fbebd61cd4de1f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f0caca0815c2fcdd6f9df8c6f0f9395e97412945c7b32584e46d77d7cc09fb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf4fc44cef2dc9cf12138f29ba0a91075e6ea014bf10e51be7805d744eac364(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9492fb7896da04c0e8f6ea6f519632cfec04f139546dc55da329a01df4b33a75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d26b9fb418fc64ea95436d16cb0b8123dd26ca55d80d5fd91286fe205dced3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c5d7b40fdb6dea303889342ff7ed82a169b3a215ddac4b1791c12055813839(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735968c7e70ab8c43d24ea30d0eff065d8ddcdb1b8d4b1c836785fc45602af31(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c23223d2d9002d3f34541e90b80f8eb1147396d65bc294679d8e4ae0917f89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7880d78ceaa1b4786ed251cca6e9958917d5008f4078f9c9b64fe29202076842(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e162f83f6ef242fcbb9cf19da6fb9a4b119d724438292b7c2967afda9d37dc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be56764e2ba890171b01ea844a446148e8d5f84d659658fee5378bd9752d91f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8b10629baf3756ca39e2f887878bab57ee69ee1f93d54d516fcebae4095ab7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc053cd30e06fa8ccb912e2a7d1b2e49b48e290a25315a5819f86e331fb079e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupSapHanaVolume]],
) -> None:
    """Type checking stubs"""
    pass

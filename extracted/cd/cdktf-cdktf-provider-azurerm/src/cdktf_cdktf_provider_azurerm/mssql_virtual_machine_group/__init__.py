r'''
# `azurerm_mssql_virtual_machine_group`

Refer to the Terraform Registry for docs: [`azurerm_mssql_virtual_machine_group`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group).
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


class MssqlVirtualMachineGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineGroup.MssqlVirtualMachineGroup",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group azurerm_mssql_virtual_machine_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sql_image_offer: builtins.str,
        sql_image_sku: builtins.str,
        wsfc_domain_profile: typing.Union["MssqlVirtualMachineGroupWsfcDomainProfile", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MssqlVirtualMachineGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group azurerm_mssql_virtual_machine_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#location MssqlVirtualMachineGroup#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#name MssqlVirtualMachineGroup#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#resource_group_name MssqlVirtualMachineGroup#resource_group_name}.
        :param sql_image_offer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#sql_image_offer MssqlVirtualMachineGroup#sql_image_offer}.
        :param sql_image_sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#sql_image_sku MssqlVirtualMachineGroup#sql_image_sku}.
        :param wsfc_domain_profile: wsfc_domain_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#wsfc_domain_profile MssqlVirtualMachineGroup#wsfc_domain_profile}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#id MssqlVirtualMachineGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#tags MssqlVirtualMachineGroup#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#timeouts MssqlVirtualMachineGroup#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b8b2834a4ad494099e09d0b895547dbf753ca5e5aa2fcaff359bc21114999e0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MssqlVirtualMachineGroupConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            sql_image_offer=sql_image_offer,
            sql_image_sku=sql_image_sku,
            wsfc_domain_profile=wsfc_domain_profile,
            id=id,
            tags=tags,
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
        '''Generates CDKTF code for importing a MssqlVirtualMachineGroup resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MssqlVirtualMachineGroup to import.
        :param import_from_id: The id of the existing MssqlVirtualMachineGroup that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MssqlVirtualMachineGroup to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c980800d24557727f42bbf47acdfdabab93fee477a882f84c6b5c744b2840f)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#create MssqlVirtualMachineGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#delete MssqlVirtualMachineGroup#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#read MssqlVirtualMachineGroup#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#update MssqlVirtualMachineGroup#update}.
        '''
        value = MssqlVirtualMachineGroupTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWsfcDomainProfile")
    def put_wsfc_domain_profile(
        self,
        *,
        cluster_subnet_type: builtins.str,
        fqdn: builtins.str,
        cluster_bootstrap_account_name: typing.Optional[builtins.str] = None,
        cluster_operator_account_name: typing.Optional[builtins.str] = None,
        organizational_unit_path: typing.Optional[builtins.str] = None,
        sql_service_account_name: typing.Optional[builtins.str] = None,
        storage_account_primary_key: typing.Optional[builtins.str] = None,
        storage_account_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster_subnet_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#cluster_subnet_type MssqlVirtualMachineGroup#cluster_subnet_type}.
        :param fqdn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#fqdn MssqlVirtualMachineGroup#fqdn}.
        :param cluster_bootstrap_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#cluster_bootstrap_account_name MssqlVirtualMachineGroup#cluster_bootstrap_account_name}.
        :param cluster_operator_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#cluster_operator_account_name MssqlVirtualMachineGroup#cluster_operator_account_name}.
        :param organizational_unit_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#organizational_unit_path MssqlVirtualMachineGroup#organizational_unit_path}.
        :param sql_service_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#sql_service_account_name MssqlVirtualMachineGroup#sql_service_account_name}.
        :param storage_account_primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#storage_account_primary_key MssqlVirtualMachineGroup#storage_account_primary_key}.
        :param storage_account_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#storage_account_url MssqlVirtualMachineGroup#storage_account_url}.
        '''
        value = MssqlVirtualMachineGroupWsfcDomainProfile(
            cluster_subnet_type=cluster_subnet_type,
            fqdn=fqdn,
            cluster_bootstrap_account_name=cluster_bootstrap_account_name,
            cluster_operator_account_name=cluster_operator_account_name,
            organizational_unit_path=organizational_unit_path,
            sql_service_account_name=sql_service_account_name,
            storage_account_primary_key=storage_account_primary_key,
            storage_account_url=storage_account_url,
        )

        return typing.cast(None, jsii.invoke(self, "putWsfcDomainProfile", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    def timeouts(self) -> "MssqlVirtualMachineGroupTimeoutsOutputReference":
        return typing.cast("MssqlVirtualMachineGroupTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="wsfcDomainProfile")
    def wsfc_domain_profile(
        self,
    ) -> "MssqlVirtualMachineGroupWsfcDomainProfileOutputReference":
        return typing.cast("MssqlVirtualMachineGroupWsfcDomainProfileOutputReference", jsii.get(self, "wsfcDomainProfile"))

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
    @jsii.member(jsii_name="sqlImageOfferInput")
    def sql_image_offer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlImageOfferInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlImageSkuInput")
    def sql_image_sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlImageSkuInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MssqlVirtualMachineGroupTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MssqlVirtualMachineGroupTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="wsfcDomainProfileInput")
    def wsfc_domain_profile_input(
        self,
    ) -> typing.Optional["MssqlVirtualMachineGroupWsfcDomainProfile"]:
        return typing.cast(typing.Optional["MssqlVirtualMachineGroupWsfcDomainProfile"], jsii.get(self, "wsfcDomainProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__578d9ca8e59a02490b2d1cccd36bea5f61e4160e320ec95468345fbb62c991b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26da78fda02b238dc5143a9b5e4eb6af4f2143420d44698568d2a0b0eb9e1f84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487a97a5a5e37fd891f0f6c6fd7791b459148126120827124a6e12085bc096bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53445b41246150a8e051345989e90de2a3fbc263c538d34903d14b5fb24c8859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlImageOffer")
    def sql_image_offer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlImageOffer"))

    @sql_image_offer.setter
    def sql_image_offer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc0fd2860e3315d9dc552d200ef5ca1bf82f4cdf64e96b0d00d893ae3409dbde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlImageOffer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlImageSku")
    def sql_image_sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlImageSku"))

    @sql_image_sku.setter
    def sql_image_sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cae30be0c0dbdd3760fbaf6ccc672629c8ca52d8924478334d0f0ce1622ae9f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlImageSku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e846b6336172b4b88b017a3990ec9b998380ddb68fdef0a9a835e3ab445adf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineGroup.MssqlVirtualMachineGroupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "sql_image_offer": "sqlImageOffer",
        "sql_image_sku": "sqlImageSku",
        "wsfc_domain_profile": "wsfcDomainProfile",
        "id": "id",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class MssqlVirtualMachineGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sql_image_offer: builtins.str,
        sql_image_sku: builtins.str,
        wsfc_domain_profile: typing.Union["MssqlVirtualMachineGroupWsfcDomainProfile", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MssqlVirtualMachineGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#location MssqlVirtualMachineGroup#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#name MssqlVirtualMachineGroup#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#resource_group_name MssqlVirtualMachineGroup#resource_group_name}.
        :param sql_image_offer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#sql_image_offer MssqlVirtualMachineGroup#sql_image_offer}.
        :param sql_image_sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#sql_image_sku MssqlVirtualMachineGroup#sql_image_sku}.
        :param wsfc_domain_profile: wsfc_domain_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#wsfc_domain_profile MssqlVirtualMachineGroup#wsfc_domain_profile}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#id MssqlVirtualMachineGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#tags MssqlVirtualMachineGroup#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#timeouts MssqlVirtualMachineGroup#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(wsfc_domain_profile, dict):
            wsfc_domain_profile = MssqlVirtualMachineGroupWsfcDomainProfile(**wsfc_domain_profile)
        if isinstance(timeouts, dict):
            timeouts = MssqlVirtualMachineGroupTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__247eb85e76e9efc6edd7e172484472132a6bb54f1385833e4e296b3eaca9322b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument sql_image_offer", value=sql_image_offer, expected_type=type_hints["sql_image_offer"])
            check_type(argname="argument sql_image_sku", value=sql_image_sku, expected_type=type_hints["sql_image_sku"])
            check_type(argname="argument wsfc_domain_profile", value=wsfc_domain_profile, expected_type=type_hints["wsfc_domain_profile"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "sql_image_offer": sql_image_offer,
            "sql_image_sku": sql_image_sku,
            "wsfc_domain_profile": wsfc_domain_profile,
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
        if tags is not None:
            self._values["tags"] = tags
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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#location MssqlVirtualMachineGroup#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#name MssqlVirtualMachineGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#resource_group_name MssqlVirtualMachineGroup#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql_image_offer(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#sql_image_offer MssqlVirtualMachineGroup#sql_image_offer}.'''
        result = self._values.get("sql_image_offer")
        assert result is not None, "Required property 'sql_image_offer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql_image_sku(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#sql_image_sku MssqlVirtualMachineGroup#sql_image_sku}.'''
        result = self._values.get("sql_image_sku")
        assert result is not None, "Required property 'sql_image_sku' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def wsfc_domain_profile(self) -> "MssqlVirtualMachineGroupWsfcDomainProfile":
        '''wsfc_domain_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#wsfc_domain_profile MssqlVirtualMachineGroup#wsfc_domain_profile}
        '''
        result = self._values.get("wsfc_domain_profile")
        assert result is not None, "Required property 'wsfc_domain_profile' is missing"
        return typing.cast("MssqlVirtualMachineGroupWsfcDomainProfile", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#id MssqlVirtualMachineGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#tags MssqlVirtualMachineGroup#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MssqlVirtualMachineGroupTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#timeouts MssqlVirtualMachineGroup#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MssqlVirtualMachineGroupTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineGroup.MssqlVirtualMachineGroupTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MssqlVirtualMachineGroupTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#create MssqlVirtualMachineGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#delete MssqlVirtualMachineGroup#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#read MssqlVirtualMachineGroup#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#update MssqlVirtualMachineGroup#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42a9fbb9602674aaaf88286460b5b931e6ac8e603658aad36c29ecca8f695f24)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#create MssqlVirtualMachineGroup#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#delete MssqlVirtualMachineGroup#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#read MssqlVirtualMachineGroup#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#update MssqlVirtualMachineGroup#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineGroupTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlVirtualMachineGroupTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineGroup.MssqlVirtualMachineGroupTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fcf3898c0acfdb1db998c76ce72e34d453063e041f7833a4341ba631cba8fe3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a4454b2090c6fa1f1b1d472083f7401a59f046909785143cec6f25b9dfb7406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebdfea50d1ceb4418975f99b5ba5b0e7c33ec8c29732d0a83a96666b79161ed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f98afa90d6beff6b233b8a6c4f9fbcb5c8f5581cbbc4632fb9af2a85cad707f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee48157e70e057aa9e14b9a1283d7d24c6f51deaa6e3bd7d0f3be6d2ec2ce0f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineGroupTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineGroupTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineGroupTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a90895bdf893c58d13f52360327c7552b757dffaf89e8d2fb20daab3c9097360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineGroup.MssqlVirtualMachineGroupWsfcDomainProfile",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_subnet_type": "clusterSubnetType",
        "fqdn": "fqdn",
        "cluster_bootstrap_account_name": "clusterBootstrapAccountName",
        "cluster_operator_account_name": "clusterOperatorAccountName",
        "organizational_unit_path": "organizationalUnitPath",
        "sql_service_account_name": "sqlServiceAccountName",
        "storage_account_primary_key": "storageAccountPrimaryKey",
        "storage_account_url": "storageAccountUrl",
    },
)
class MssqlVirtualMachineGroupWsfcDomainProfile:
    def __init__(
        self,
        *,
        cluster_subnet_type: builtins.str,
        fqdn: builtins.str,
        cluster_bootstrap_account_name: typing.Optional[builtins.str] = None,
        cluster_operator_account_name: typing.Optional[builtins.str] = None,
        organizational_unit_path: typing.Optional[builtins.str] = None,
        sql_service_account_name: typing.Optional[builtins.str] = None,
        storage_account_primary_key: typing.Optional[builtins.str] = None,
        storage_account_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster_subnet_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#cluster_subnet_type MssqlVirtualMachineGroup#cluster_subnet_type}.
        :param fqdn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#fqdn MssqlVirtualMachineGroup#fqdn}.
        :param cluster_bootstrap_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#cluster_bootstrap_account_name MssqlVirtualMachineGroup#cluster_bootstrap_account_name}.
        :param cluster_operator_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#cluster_operator_account_name MssqlVirtualMachineGroup#cluster_operator_account_name}.
        :param organizational_unit_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#organizational_unit_path MssqlVirtualMachineGroup#organizational_unit_path}.
        :param sql_service_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#sql_service_account_name MssqlVirtualMachineGroup#sql_service_account_name}.
        :param storage_account_primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#storage_account_primary_key MssqlVirtualMachineGroup#storage_account_primary_key}.
        :param storage_account_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#storage_account_url MssqlVirtualMachineGroup#storage_account_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdbb4db7f400cb15077a6462123378bd82af2c8cec0a85c709dc863734bd8c00)
            check_type(argname="argument cluster_subnet_type", value=cluster_subnet_type, expected_type=type_hints["cluster_subnet_type"])
            check_type(argname="argument fqdn", value=fqdn, expected_type=type_hints["fqdn"])
            check_type(argname="argument cluster_bootstrap_account_name", value=cluster_bootstrap_account_name, expected_type=type_hints["cluster_bootstrap_account_name"])
            check_type(argname="argument cluster_operator_account_name", value=cluster_operator_account_name, expected_type=type_hints["cluster_operator_account_name"])
            check_type(argname="argument organizational_unit_path", value=organizational_unit_path, expected_type=type_hints["organizational_unit_path"])
            check_type(argname="argument sql_service_account_name", value=sql_service_account_name, expected_type=type_hints["sql_service_account_name"])
            check_type(argname="argument storage_account_primary_key", value=storage_account_primary_key, expected_type=type_hints["storage_account_primary_key"])
            check_type(argname="argument storage_account_url", value=storage_account_url, expected_type=type_hints["storage_account_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_subnet_type": cluster_subnet_type,
            "fqdn": fqdn,
        }
        if cluster_bootstrap_account_name is not None:
            self._values["cluster_bootstrap_account_name"] = cluster_bootstrap_account_name
        if cluster_operator_account_name is not None:
            self._values["cluster_operator_account_name"] = cluster_operator_account_name
        if organizational_unit_path is not None:
            self._values["organizational_unit_path"] = organizational_unit_path
        if sql_service_account_name is not None:
            self._values["sql_service_account_name"] = sql_service_account_name
        if storage_account_primary_key is not None:
            self._values["storage_account_primary_key"] = storage_account_primary_key
        if storage_account_url is not None:
            self._values["storage_account_url"] = storage_account_url

    @builtins.property
    def cluster_subnet_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#cluster_subnet_type MssqlVirtualMachineGroup#cluster_subnet_type}.'''
        result = self._values.get("cluster_subnet_type")
        assert result is not None, "Required property 'cluster_subnet_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fqdn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#fqdn MssqlVirtualMachineGroup#fqdn}.'''
        result = self._values.get("fqdn")
        assert result is not None, "Required property 'fqdn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_bootstrap_account_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#cluster_bootstrap_account_name MssqlVirtualMachineGroup#cluster_bootstrap_account_name}.'''
        result = self._values.get("cluster_bootstrap_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_operator_account_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#cluster_operator_account_name MssqlVirtualMachineGroup#cluster_operator_account_name}.'''
        result = self._values.get("cluster_operator_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organizational_unit_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#organizational_unit_path MssqlVirtualMachineGroup#organizational_unit_path}.'''
        result = self._values.get("organizational_unit_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_service_account_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#sql_service_account_name MssqlVirtualMachineGroup#sql_service_account_name}.'''
        result = self._values.get("sql_service_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_primary_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#storage_account_primary_key MssqlVirtualMachineGroup#storage_account_primary_key}.'''
        result = self._values.get("storage_account_primary_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_group#storage_account_url MssqlVirtualMachineGroup#storage_account_url}.'''
        result = self._values.get("storage_account_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineGroupWsfcDomainProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlVirtualMachineGroupWsfcDomainProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineGroup.MssqlVirtualMachineGroupWsfcDomainProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90dcc4abdc743ecbb78e1e67b6e4b69df520df948b076ab87200118d9b4e5ca7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClusterBootstrapAccountName")
    def reset_cluster_bootstrap_account_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterBootstrapAccountName", []))

    @jsii.member(jsii_name="resetClusterOperatorAccountName")
    def reset_cluster_operator_account_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterOperatorAccountName", []))

    @jsii.member(jsii_name="resetOrganizationalUnitPath")
    def reset_organizational_unit_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationalUnitPath", []))

    @jsii.member(jsii_name="resetSqlServiceAccountName")
    def reset_sql_service_account_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlServiceAccountName", []))

    @jsii.member(jsii_name="resetStorageAccountPrimaryKey")
    def reset_storage_account_primary_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountPrimaryKey", []))

    @jsii.member(jsii_name="resetStorageAccountUrl")
    def reset_storage_account_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountUrl", []))

    @builtins.property
    @jsii.member(jsii_name="clusterBootstrapAccountNameInput")
    def cluster_bootstrap_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterBootstrapAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterOperatorAccountNameInput")
    def cluster_operator_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterOperatorAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterSubnetTypeInput")
    def cluster_subnet_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterSubnetTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="fqdnInput")
    def fqdn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fqdnInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationalUnitPathInput")
    def organizational_unit_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationalUnitPathInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlServiceAccountNameInput")
    def sql_service_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlServiceAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountPrimaryKeyInput")
    def storage_account_primary_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountPrimaryKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountUrlInput")
    def storage_account_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterBootstrapAccountName")
    def cluster_bootstrap_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterBootstrapAccountName"))

    @cluster_bootstrap_account_name.setter
    def cluster_bootstrap_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1fefa17a298c7ed806280e3f59966a15bb4874be83c537bb4b1574462dd71e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterBootstrapAccountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterOperatorAccountName")
    def cluster_operator_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterOperatorAccountName"))

    @cluster_operator_account_name.setter
    def cluster_operator_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a230563f1d7de3cdd63d049b9a573d6ed2b87208350e78fc101691de28379adf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterOperatorAccountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterSubnetType")
    def cluster_subnet_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterSubnetType"))

    @cluster_subnet_type.setter
    def cluster_subnet_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__549a45abec0c32794c2a522248f72ebdb6e6535904879187a69339b4ce5f4c24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterSubnetType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))

    @fqdn.setter
    def fqdn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c1e80774b28283755dccb816e4ab4d1c9761d343789efc815f7f4f9c7bdaef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fqdn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationalUnitPath")
    def organizational_unit_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationalUnitPath"))

    @organizational_unit_path.setter
    def organizational_unit_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b84511c9c8056cd111f0ada0870e74515b98a99e2fcd057cfc0667ec75a88a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationalUnitPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlServiceAccountName")
    def sql_service_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlServiceAccountName"))

    @sql_service_account_name.setter
    def sql_service_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__926bdae4c7e78ab0fb5f69fbb04371f2fb8fb26578d1d34234ed2a5633477393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlServiceAccountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountPrimaryKey")
    def storage_account_primary_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountPrimaryKey"))

    @storage_account_primary_key.setter
    def storage_account_primary_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3944a76298a49222b988e18c28b475fb68d3566f98321efbe7c953af2a3f2cbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountPrimaryKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountUrl")
    def storage_account_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountUrl"))

    @storage_account_url.setter
    def storage_account_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eadbd77c87c1c9d0d489f84b3af5a034b795d4132dec30161fefe2cf59e7021c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MssqlVirtualMachineGroupWsfcDomainProfile]:
        return typing.cast(typing.Optional[MssqlVirtualMachineGroupWsfcDomainProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlVirtualMachineGroupWsfcDomainProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8016a2cfcd6e32e03743803439cc6e5385d57ccdfe59bc4ad1ed4269dc386fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MssqlVirtualMachineGroup",
    "MssqlVirtualMachineGroupConfig",
    "MssqlVirtualMachineGroupTimeouts",
    "MssqlVirtualMachineGroupTimeoutsOutputReference",
    "MssqlVirtualMachineGroupWsfcDomainProfile",
    "MssqlVirtualMachineGroupWsfcDomainProfileOutputReference",
]

publication.publish()

def _typecheckingstub__9b8b2834a4ad494099e09d0b895547dbf753ca5e5aa2fcaff359bc21114999e0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sql_image_offer: builtins.str,
    sql_image_sku: builtins.str,
    wsfc_domain_profile: typing.Union[MssqlVirtualMachineGroupWsfcDomainProfile, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MssqlVirtualMachineGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__46c980800d24557727f42bbf47acdfdabab93fee477a882f84c6b5c744b2840f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__578d9ca8e59a02490b2d1cccd36bea5f61e4160e320ec95468345fbb62c991b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26da78fda02b238dc5143a9b5e4eb6af4f2143420d44698568d2a0b0eb9e1f84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487a97a5a5e37fd891f0f6c6fd7791b459148126120827124a6e12085bc096bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53445b41246150a8e051345989e90de2a3fbc263c538d34903d14b5fb24c8859(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0fd2860e3315d9dc552d200ef5ca1bf82f4cdf64e96b0d00d893ae3409dbde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae30be0c0dbdd3760fbaf6ccc672629c8ca52d8924478334d0f0ce1622ae9f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e846b6336172b4b88b017a3990ec9b998380ddb68fdef0a9a835e3ab445adf5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247eb85e76e9efc6edd7e172484472132a6bb54f1385833e4e296b3eaca9322b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sql_image_offer: builtins.str,
    sql_image_sku: builtins.str,
    wsfc_domain_profile: typing.Union[MssqlVirtualMachineGroupWsfcDomainProfile, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MssqlVirtualMachineGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a9fbb9602674aaaf88286460b5b931e6ac8e603658aad36c29ecca8f695f24(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fcf3898c0acfdb1db998c76ce72e34d453063e041f7833a4341ba631cba8fe3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4454b2090c6fa1f1b1d472083f7401a59f046909785143cec6f25b9dfb7406(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebdfea50d1ceb4418975f99b5ba5b0e7c33ec8c29732d0a83a96666b79161ed7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f98afa90d6beff6b233b8a6c4f9fbcb5c8f5581cbbc4632fb9af2a85cad707f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee48157e70e057aa9e14b9a1283d7d24c6f51deaa6e3bd7d0f3be6d2ec2ce0f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90895bdf893c58d13f52360327c7552b757dffaf89e8d2fb20daab3c9097360(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineGroupTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdbb4db7f400cb15077a6462123378bd82af2c8cec0a85c709dc863734bd8c00(
    *,
    cluster_subnet_type: builtins.str,
    fqdn: builtins.str,
    cluster_bootstrap_account_name: typing.Optional[builtins.str] = None,
    cluster_operator_account_name: typing.Optional[builtins.str] = None,
    organizational_unit_path: typing.Optional[builtins.str] = None,
    sql_service_account_name: typing.Optional[builtins.str] = None,
    storage_account_primary_key: typing.Optional[builtins.str] = None,
    storage_account_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90dcc4abdc743ecbb78e1e67b6e4b69df520df948b076ab87200118d9b4e5ca7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1fefa17a298c7ed806280e3f59966a15bb4874be83c537bb4b1574462dd71e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a230563f1d7de3cdd63d049b9a573d6ed2b87208350e78fc101691de28379adf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__549a45abec0c32794c2a522248f72ebdb6e6535904879187a69339b4ce5f4c24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1e80774b28283755dccb816e4ab4d1c9761d343789efc815f7f4f9c7bdaef6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b84511c9c8056cd111f0ada0870e74515b98a99e2fcd057cfc0667ec75a88a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926bdae4c7e78ab0fb5f69fbb04371f2fb8fb26578d1d34234ed2a5633477393(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3944a76298a49222b988e18c28b475fb68d3566f98321efbe7c953af2a3f2cbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eadbd77c87c1c9d0d489f84b3af5a034b795d4132dec30161fefe2cf59e7021c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8016a2cfcd6e32e03743803439cc6e5385d57ccdfe59bc4ad1ed4269dc386fc(
    value: typing.Optional[MssqlVirtualMachineGroupWsfcDomainProfile],
) -> None:
    """Type checking stubs"""
    pass

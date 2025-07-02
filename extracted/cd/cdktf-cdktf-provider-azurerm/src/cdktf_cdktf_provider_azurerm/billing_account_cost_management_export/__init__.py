r'''
# `azurerm_billing_account_cost_management_export`

Refer to the Terraform Registry for docs: [`azurerm_billing_account_cost_management_export`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export).
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


class BillingAccountCostManagementExport(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.billingAccountCostManagementExport.BillingAccountCostManagementExport",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export azurerm_billing_account_cost_management_export}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        billing_account_id: builtins.str,
        export_data_options: typing.Union["BillingAccountCostManagementExportExportDataOptions", typing.Dict[builtins.str, typing.Any]],
        export_data_storage_location: typing.Union["BillingAccountCostManagementExportExportDataStorageLocation", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        recurrence_period_end_date: builtins.str,
        recurrence_period_start_date: builtins.str,
        recurrence_type: builtins.str,
        active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        file_format: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BillingAccountCostManagementExportTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export azurerm_billing_account_cost_management_export} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param billing_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#billing_account_id BillingAccountCostManagementExport#billing_account_id}.
        :param export_data_options: export_data_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#export_data_options BillingAccountCostManagementExport#export_data_options}
        :param export_data_storage_location: export_data_storage_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#export_data_storage_location BillingAccountCostManagementExport#export_data_storage_location}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#name BillingAccountCostManagementExport#name}.
        :param recurrence_period_end_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#recurrence_period_end_date BillingAccountCostManagementExport#recurrence_period_end_date}.
        :param recurrence_period_start_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#recurrence_period_start_date BillingAccountCostManagementExport#recurrence_period_start_date}.
        :param recurrence_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#recurrence_type BillingAccountCostManagementExport#recurrence_type}.
        :param active: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#active BillingAccountCostManagementExport#active}.
        :param file_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#file_format BillingAccountCostManagementExport#file_format}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#id BillingAccountCostManagementExport#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#timeouts BillingAccountCostManagementExport#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34a6789ef9834ffc3c2dfcb3e8b7c675332da60a5a00ceea89c435d466144030)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BillingAccountCostManagementExportConfig(
            billing_account_id=billing_account_id,
            export_data_options=export_data_options,
            export_data_storage_location=export_data_storage_location,
            name=name,
            recurrence_period_end_date=recurrence_period_end_date,
            recurrence_period_start_date=recurrence_period_start_date,
            recurrence_type=recurrence_type,
            active=active,
            file_format=file_format,
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
        '''Generates CDKTF code for importing a BillingAccountCostManagementExport resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BillingAccountCostManagementExport to import.
        :param import_from_id: The id of the existing BillingAccountCostManagementExport that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BillingAccountCostManagementExport to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73b07910b6d2fbdce8dfbc3d1df46429907107a890431690eed52f87d7100f88)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putExportDataOptions")
    def put_export_data_options(
        self,
        *,
        time_frame: builtins.str,
        type: builtins.str,
    ) -> None:
        '''
        :param time_frame: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#time_frame BillingAccountCostManagementExport#time_frame}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#type BillingAccountCostManagementExport#type}.
        '''
        value = BillingAccountCostManagementExportExportDataOptions(
            time_frame=time_frame, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putExportDataOptions", [value]))

    @jsii.member(jsii_name="putExportDataStorageLocation")
    def put_export_data_storage_location(
        self,
        *,
        container_id: builtins.str,
        root_folder_path: builtins.str,
    ) -> None:
        '''
        :param container_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#container_id BillingAccountCostManagementExport#container_id}.
        :param root_folder_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#root_folder_path BillingAccountCostManagementExport#root_folder_path}.
        '''
        value = BillingAccountCostManagementExportExportDataStorageLocation(
            container_id=container_id, root_folder_path=root_folder_path
        )

        return typing.cast(None, jsii.invoke(self, "putExportDataStorageLocation", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#create BillingAccountCostManagementExport#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#delete BillingAccountCostManagementExport#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#read BillingAccountCostManagementExport#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#update BillingAccountCostManagementExport#update}.
        '''
        value = BillingAccountCostManagementExportTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetActive")
    def reset_active(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActive", []))

    @jsii.member(jsii_name="resetFileFormat")
    def reset_file_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileFormat", []))

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
    @jsii.member(jsii_name="exportDataOptions")
    def export_data_options(
        self,
    ) -> "BillingAccountCostManagementExportExportDataOptionsOutputReference":
        return typing.cast("BillingAccountCostManagementExportExportDataOptionsOutputReference", jsii.get(self, "exportDataOptions"))

    @builtins.property
    @jsii.member(jsii_name="exportDataStorageLocation")
    def export_data_storage_location(
        self,
    ) -> "BillingAccountCostManagementExportExportDataStorageLocationOutputReference":
        return typing.cast("BillingAccountCostManagementExportExportDataStorageLocationOutputReference", jsii.get(self, "exportDataStorageLocation"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BillingAccountCostManagementExportTimeoutsOutputReference":
        return typing.cast("BillingAccountCostManagementExportTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="activeInput")
    def active_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "activeInput"))

    @builtins.property
    @jsii.member(jsii_name="billingAccountIdInput")
    def billing_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="exportDataOptionsInput")
    def export_data_options_input(
        self,
    ) -> typing.Optional["BillingAccountCostManagementExportExportDataOptions"]:
        return typing.cast(typing.Optional["BillingAccountCostManagementExportExportDataOptions"], jsii.get(self, "exportDataOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="exportDataStorageLocationInput")
    def export_data_storage_location_input(
        self,
    ) -> typing.Optional["BillingAccountCostManagementExportExportDataStorageLocation"]:
        return typing.cast(typing.Optional["BillingAccountCostManagementExportExportDataStorageLocation"], jsii.get(self, "exportDataStorageLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="fileFormatInput")
    def file_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrencePeriodEndDateInput")
    def recurrence_period_end_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recurrencePeriodEndDateInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrencePeriodStartDateInput")
    def recurrence_period_start_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recurrencePeriodStartDateInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceTypeInput")
    def recurrence_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recurrenceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BillingAccountCostManagementExportTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BillingAccountCostManagementExportTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="active")
    def active(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "active"))

    @active.setter
    def active(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__174e348d0bbfc66be73ae95365b2c6e402a6035985e3c712ce41e832a7f94d42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "active", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="billingAccountId")
    def billing_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "billingAccountId"))

    @billing_account_id.setter
    def billing_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1a2195f9ae442d2c8dd67c795ecb98eea6b979b622d6fa4c72cfedbfd649068)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileFormat")
    def file_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileFormat"))

    @file_format.setter
    def file_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e46020d6b8d06a503fa617863e67a22f1345b5867bbacfaecdbbf1700cf8f7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e60515bf388b8e4deee1c6c03582d12d97e12b9816d522836717eecf56e7497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__277b8c9a5471392cc8eca6cacfdb5d8842c42a9d7fdf3640fc6eb304bae44a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recurrencePeriodEndDate")
    def recurrence_period_end_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurrencePeriodEndDate"))

    @recurrence_period_end_date.setter
    def recurrence_period_end_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2beecb209601c67e25a7abfe3b47f532779bad7fa1f12411528018371d422837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrencePeriodEndDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recurrencePeriodStartDate")
    def recurrence_period_start_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurrencePeriodStartDate"))

    @recurrence_period_start_date.setter
    def recurrence_period_start_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5170206cba723d5c98fd4af062cdde4eb0fdc2b735155f752b550f95e52ca37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrencePeriodStartDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recurrenceType")
    def recurrence_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurrenceType"))

    @recurrence_type.setter
    def recurrence_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374cb11a65c18d8d426c8beb09f4161ead5eecc9691aadd6630c055fd4616c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrenceType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.billingAccountCostManagementExport.BillingAccountCostManagementExportConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "billing_account_id": "billingAccountId",
        "export_data_options": "exportDataOptions",
        "export_data_storage_location": "exportDataStorageLocation",
        "name": "name",
        "recurrence_period_end_date": "recurrencePeriodEndDate",
        "recurrence_period_start_date": "recurrencePeriodStartDate",
        "recurrence_type": "recurrenceType",
        "active": "active",
        "file_format": "fileFormat",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class BillingAccountCostManagementExportConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        billing_account_id: builtins.str,
        export_data_options: typing.Union["BillingAccountCostManagementExportExportDataOptions", typing.Dict[builtins.str, typing.Any]],
        export_data_storage_location: typing.Union["BillingAccountCostManagementExportExportDataStorageLocation", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        recurrence_period_end_date: builtins.str,
        recurrence_period_start_date: builtins.str,
        recurrence_type: builtins.str,
        active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        file_format: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BillingAccountCostManagementExportTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param billing_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#billing_account_id BillingAccountCostManagementExport#billing_account_id}.
        :param export_data_options: export_data_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#export_data_options BillingAccountCostManagementExport#export_data_options}
        :param export_data_storage_location: export_data_storage_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#export_data_storage_location BillingAccountCostManagementExport#export_data_storage_location}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#name BillingAccountCostManagementExport#name}.
        :param recurrence_period_end_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#recurrence_period_end_date BillingAccountCostManagementExport#recurrence_period_end_date}.
        :param recurrence_period_start_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#recurrence_period_start_date BillingAccountCostManagementExport#recurrence_period_start_date}.
        :param recurrence_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#recurrence_type BillingAccountCostManagementExport#recurrence_type}.
        :param active: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#active BillingAccountCostManagementExport#active}.
        :param file_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#file_format BillingAccountCostManagementExport#file_format}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#id BillingAccountCostManagementExport#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#timeouts BillingAccountCostManagementExport#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(export_data_options, dict):
            export_data_options = BillingAccountCostManagementExportExportDataOptions(**export_data_options)
        if isinstance(export_data_storage_location, dict):
            export_data_storage_location = BillingAccountCostManagementExportExportDataStorageLocation(**export_data_storage_location)
        if isinstance(timeouts, dict):
            timeouts = BillingAccountCostManagementExportTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f09a36fa9939bb22d7471d43b465d65aa3873f8445bb049978b06e7b7558aa)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument billing_account_id", value=billing_account_id, expected_type=type_hints["billing_account_id"])
            check_type(argname="argument export_data_options", value=export_data_options, expected_type=type_hints["export_data_options"])
            check_type(argname="argument export_data_storage_location", value=export_data_storage_location, expected_type=type_hints["export_data_storage_location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument recurrence_period_end_date", value=recurrence_period_end_date, expected_type=type_hints["recurrence_period_end_date"])
            check_type(argname="argument recurrence_period_start_date", value=recurrence_period_start_date, expected_type=type_hints["recurrence_period_start_date"])
            check_type(argname="argument recurrence_type", value=recurrence_type, expected_type=type_hints["recurrence_type"])
            check_type(argname="argument active", value=active, expected_type=type_hints["active"])
            check_type(argname="argument file_format", value=file_format, expected_type=type_hints["file_format"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "billing_account_id": billing_account_id,
            "export_data_options": export_data_options,
            "export_data_storage_location": export_data_storage_location,
            "name": name,
            "recurrence_period_end_date": recurrence_period_end_date,
            "recurrence_period_start_date": recurrence_period_start_date,
            "recurrence_type": recurrence_type,
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
        if active is not None:
            self._values["active"] = active
        if file_format is not None:
            self._values["file_format"] = file_format
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
    def billing_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#billing_account_id BillingAccountCostManagementExport#billing_account_id}.'''
        result = self._values.get("billing_account_id")
        assert result is not None, "Required property 'billing_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def export_data_options(
        self,
    ) -> "BillingAccountCostManagementExportExportDataOptions":
        '''export_data_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#export_data_options BillingAccountCostManagementExport#export_data_options}
        '''
        result = self._values.get("export_data_options")
        assert result is not None, "Required property 'export_data_options' is missing"
        return typing.cast("BillingAccountCostManagementExportExportDataOptions", result)

    @builtins.property
    def export_data_storage_location(
        self,
    ) -> "BillingAccountCostManagementExportExportDataStorageLocation":
        '''export_data_storage_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#export_data_storage_location BillingAccountCostManagementExport#export_data_storage_location}
        '''
        result = self._values.get("export_data_storage_location")
        assert result is not None, "Required property 'export_data_storage_location' is missing"
        return typing.cast("BillingAccountCostManagementExportExportDataStorageLocation", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#name BillingAccountCostManagementExport#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def recurrence_period_end_date(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#recurrence_period_end_date BillingAccountCostManagementExport#recurrence_period_end_date}.'''
        result = self._values.get("recurrence_period_end_date")
        assert result is not None, "Required property 'recurrence_period_end_date' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def recurrence_period_start_date(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#recurrence_period_start_date BillingAccountCostManagementExport#recurrence_period_start_date}.'''
        result = self._values.get("recurrence_period_start_date")
        assert result is not None, "Required property 'recurrence_period_start_date' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def recurrence_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#recurrence_type BillingAccountCostManagementExport#recurrence_type}.'''
        result = self._values.get("recurrence_type")
        assert result is not None, "Required property 'recurrence_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#active BillingAccountCostManagementExport#active}.'''
        result = self._values.get("active")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def file_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#file_format BillingAccountCostManagementExport#file_format}.'''
        result = self._values.get("file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#id BillingAccountCostManagementExport#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BillingAccountCostManagementExportTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#timeouts BillingAccountCostManagementExport#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BillingAccountCostManagementExportTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BillingAccountCostManagementExportConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.billingAccountCostManagementExport.BillingAccountCostManagementExportExportDataOptions",
    jsii_struct_bases=[],
    name_mapping={"time_frame": "timeFrame", "type": "type"},
)
class BillingAccountCostManagementExportExportDataOptions:
    def __init__(self, *, time_frame: builtins.str, type: builtins.str) -> None:
        '''
        :param time_frame: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#time_frame BillingAccountCostManagementExport#time_frame}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#type BillingAccountCostManagementExport#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ef77146454894ce7b8b8eabb41cd8d4e64fc2de3017d6349fcf5c173b5170b)
            check_type(argname="argument time_frame", value=time_frame, expected_type=type_hints["time_frame"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "time_frame": time_frame,
            "type": type,
        }

    @builtins.property
    def time_frame(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#time_frame BillingAccountCostManagementExport#time_frame}.'''
        result = self._values.get("time_frame")
        assert result is not None, "Required property 'time_frame' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#type BillingAccountCostManagementExport#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BillingAccountCostManagementExportExportDataOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BillingAccountCostManagementExportExportDataOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.billingAccountCostManagementExport.BillingAccountCostManagementExportExportDataOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e7ea04c3a9983a48f48a1ab5edf9340c50013a96a80dcaf31726be94d79d6a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="timeFrameInput")
    def time_frame_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeFrameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeFrame")
    def time_frame(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeFrame"))

    @time_frame.setter
    def time_frame(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea776126d93247792ea77ad91d5c6980151e779c3ad6f68d3a92e2d91ffdcbc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeFrame", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9ff67dafccf9a68da6c778e419d2deda7a1e8a77864943e892a8c81166bdd0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BillingAccountCostManagementExportExportDataOptions]:
        return typing.cast(typing.Optional[BillingAccountCostManagementExportExportDataOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BillingAccountCostManagementExportExportDataOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58dae0f0f7cfce76302ea1b72639865c5be079c10283709fcd57847598f3a28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.billingAccountCostManagementExport.BillingAccountCostManagementExportExportDataStorageLocation",
    jsii_struct_bases=[],
    name_mapping={"container_id": "containerId", "root_folder_path": "rootFolderPath"},
)
class BillingAccountCostManagementExportExportDataStorageLocation:
    def __init__(
        self,
        *,
        container_id: builtins.str,
        root_folder_path: builtins.str,
    ) -> None:
        '''
        :param container_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#container_id BillingAccountCostManagementExport#container_id}.
        :param root_folder_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#root_folder_path BillingAccountCostManagementExport#root_folder_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efe414bf794ee0b5cb640ef04ef76b7cd2731438a7f7207e0187cdde229983a3)
            check_type(argname="argument container_id", value=container_id, expected_type=type_hints["container_id"])
            check_type(argname="argument root_folder_path", value=root_folder_path, expected_type=type_hints["root_folder_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_id": container_id,
            "root_folder_path": root_folder_path,
        }

    @builtins.property
    def container_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#container_id BillingAccountCostManagementExport#container_id}.'''
        result = self._values.get("container_id")
        assert result is not None, "Required property 'container_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def root_folder_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#root_folder_path BillingAccountCostManagementExport#root_folder_path}.'''
        result = self._values.get("root_folder_path")
        assert result is not None, "Required property 'root_folder_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BillingAccountCostManagementExportExportDataStorageLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BillingAccountCostManagementExportExportDataStorageLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.billingAccountCostManagementExport.BillingAccountCostManagementExportExportDataStorageLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecb13f1efe061352b458a2dd5ca739bcffc51001708d4d6ac32dad8aa8387a36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="containerIdInput")
    def container_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="rootFolderPathInput")
    def root_folder_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootFolderPathInput"))

    @builtins.property
    @jsii.member(jsii_name="containerId")
    def container_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerId"))

    @container_id.setter
    def container_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7921e6048e4303a2c1ac0e260b7270632ab9ea993cbacdb2b0fac75d60792cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootFolderPath")
    def root_folder_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootFolderPath"))

    @root_folder_path.setter
    def root_folder_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62c8b4d2405c299d30623dcf3a977f23b6bf6c774525385de0046882e809863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootFolderPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BillingAccountCostManagementExportExportDataStorageLocation]:
        return typing.cast(typing.Optional[BillingAccountCostManagementExportExportDataStorageLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BillingAccountCostManagementExportExportDataStorageLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__927ff2cdf586485cbf421b5bf8584fe78ecd84e23a06b74859de5ca237c70139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.billingAccountCostManagementExport.BillingAccountCostManagementExportTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class BillingAccountCostManagementExportTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#create BillingAccountCostManagementExport#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#delete BillingAccountCostManagementExport#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#read BillingAccountCostManagementExport#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#update BillingAccountCostManagementExport#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3bbfcac004d19b65e9fbdd85d74fd1737148ef16b32d07d9c771521406735c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#create BillingAccountCostManagementExport#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#delete BillingAccountCostManagementExport#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#read BillingAccountCostManagementExport#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/billing_account_cost_management_export#update BillingAccountCostManagementExport#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BillingAccountCostManagementExportTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BillingAccountCostManagementExportTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.billingAccountCostManagementExport.BillingAccountCostManagementExportTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bfdbdef0f9a634d56612710949cb4294b6f3678ec222444e927eb39a141703b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b18d3b202ba89392ac706359f74f84c0ad92300cfffb0cc7dd883a0524f46e5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4eedc5b716ec4eddf3e3c7fff7d4e410b8d09aaa9084a654316daa3002895c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb12a60287d1dbb352049edbeb2309dbb6a5a59200c21377e547b632713a442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc85867525d638be2b2a5472017e45ec5648403590b65e51a56225c789918bd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BillingAccountCostManagementExportTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BillingAccountCostManagementExportTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BillingAccountCostManagementExportTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24b1feaa0006de91bc5f2c62667391cd2d96b7d2384b523d61d71d039d617c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BillingAccountCostManagementExport",
    "BillingAccountCostManagementExportConfig",
    "BillingAccountCostManagementExportExportDataOptions",
    "BillingAccountCostManagementExportExportDataOptionsOutputReference",
    "BillingAccountCostManagementExportExportDataStorageLocation",
    "BillingAccountCostManagementExportExportDataStorageLocationOutputReference",
    "BillingAccountCostManagementExportTimeouts",
    "BillingAccountCostManagementExportTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__34a6789ef9834ffc3c2dfcb3e8b7c675332da60a5a00ceea89c435d466144030(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    billing_account_id: builtins.str,
    export_data_options: typing.Union[BillingAccountCostManagementExportExportDataOptions, typing.Dict[builtins.str, typing.Any]],
    export_data_storage_location: typing.Union[BillingAccountCostManagementExportExportDataStorageLocation, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    recurrence_period_end_date: builtins.str,
    recurrence_period_start_date: builtins.str,
    recurrence_type: builtins.str,
    active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    file_format: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BillingAccountCostManagementExportTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__73b07910b6d2fbdce8dfbc3d1df46429907107a890431690eed52f87d7100f88(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__174e348d0bbfc66be73ae95365b2c6e402a6035985e3c712ce41e832a7f94d42(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a2195f9ae442d2c8dd67c795ecb98eea6b979b622d6fa4c72cfedbfd649068(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e46020d6b8d06a503fa617863e67a22f1345b5867bbacfaecdbbf1700cf8f7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e60515bf388b8e4deee1c6c03582d12d97e12b9816d522836717eecf56e7497(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__277b8c9a5471392cc8eca6cacfdb5d8842c42a9d7fdf3640fc6eb304bae44a10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2beecb209601c67e25a7abfe3b47f532779bad7fa1f12411528018371d422837(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5170206cba723d5c98fd4af062cdde4eb0fdc2b735155f752b550f95e52ca37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374cb11a65c18d8d426c8beb09f4161ead5eecc9691aadd6630c055fd4616c20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f09a36fa9939bb22d7471d43b465d65aa3873f8445bb049978b06e7b7558aa(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    billing_account_id: builtins.str,
    export_data_options: typing.Union[BillingAccountCostManagementExportExportDataOptions, typing.Dict[builtins.str, typing.Any]],
    export_data_storage_location: typing.Union[BillingAccountCostManagementExportExportDataStorageLocation, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    recurrence_period_end_date: builtins.str,
    recurrence_period_start_date: builtins.str,
    recurrence_type: builtins.str,
    active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    file_format: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BillingAccountCostManagementExportTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ef77146454894ce7b8b8eabb41cd8d4e64fc2de3017d6349fcf5c173b5170b(
    *,
    time_frame: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e7ea04c3a9983a48f48a1ab5edf9340c50013a96a80dcaf31726be94d79d6a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea776126d93247792ea77ad91d5c6980151e779c3ad6f68d3a92e2d91ffdcbc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ff67dafccf9a68da6c778e419d2deda7a1e8a77864943e892a8c81166bdd0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58dae0f0f7cfce76302ea1b72639865c5be079c10283709fcd57847598f3a28(
    value: typing.Optional[BillingAccountCostManagementExportExportDataOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe414bf794ee0b5cb640ef04ef76b7cd2731438a7f7207e0187cdde229983a3(
    *,
    container_id: builtins.str,
    root_folder_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb13f1efe061352b458a2dd5ca739bcffc51001708d4d6ac32dad8aa8387a36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7921e6048e4303a2c1ac0e260b7270632ab9ea993cbacdb2b0fac75d60792cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62c8b4d2405c299d30623dcf3a977f23b6bf6c774525385de0046882e809863(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__927ff2cdf586485cbf421b5bf8584fe78ecd84e23a06b74859de5ca237c70139(
    value: typing.Optional[BillingAccountCostManagementExportExportDataStorageLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3bbfcac004d19b65e9fbdd85d74fd1737148ef16b32d07d9c771521406735c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bfdbdef0f9a634d56612710949cb4294b6f3678ec222444e927eb39a141703b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18d3b202ba89392ac706359f74f84c0ad92300cfffb0cc7dd883a0524f46e5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4eedc5b716ec4eddf3e3c7fff7d4e410b8d09aaa9084a654316daa3002895c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb12a60287d1dbb352049edbeb2309dbb6a5a59200c21377e547b632713a442(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc85867525d638be2b2a5472017e45ec5648403590b65e51a56225c789918bd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b1feaa0006de91bc5f2c62667391cd2d96b7d2384b523d61d71d039d617c32(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BillingAccountCostManagementExportTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

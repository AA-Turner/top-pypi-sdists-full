r'''
# `datadog_azure_uc_config`

Refer to the Terraform Registry for docs: [`datadog_azure_uc_config`](https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config).
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


class AzureUcConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.azureUcConfig.AzureUcConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config datadog_azure_uc_config}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account_id: builtins.str,
        actual_bill_config: typing.Union["AzureUcConfigActualBillConfig", typing.Dict[builtins.str, typing.Any]],
        amortized_bill_config: typing.Union["AzureUcConfigAmortizedBillConfig", typing.Dict[builtins.str, typing.Any]],
        client_id: builtins.str,
        scope: builtins.str,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config datadog_azure_uc_config} Resource.

        :param scope_: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The tenant ID of the Azure account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#account_id AzureUcConfig#account_id}
        :param actual_bill_config: actual_bill_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#actual_bill_config AzureUcConfig#actual_bill_config}
        :param amortized_bill_config: amortized_bill_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#amortized_bill_config AzureUcConfig#amortized_bill_config}
        :param client_id: The client ID of the Azure account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#client_id AzureUcConfig#client_id}
        :param scope: The scope of your observed subscription. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#scope AzureUcConfig#scope}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ff038216101e1d15cf3494eed4c4f79f97722a5ab007076456b18b432c387f7)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = AzureUcConfigConfig(
            account_id=account_id,
            actual_bill_config=actual_bill_config,
            amortized_bill_config=amortized_bill_config,
            client_id=client_id,
            scope=scope,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope_, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a AzureUcConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AzureUcConfig to import.
        :param import_from_id: The id of the existing AzureUcConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AzureUcConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4708a522c7c9c629b14387aae94b0e3e4ba04a680aa53aa09f376785fd99e44c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActualBillConfig")
    def put_actual_bill_config(
        self,
        *,
        export_name: builtins.str,
        export_path: builtins.str,
        storage_account: builtins.str,
        storage_container: builtins.str,
    ) -> None:
        '''
        :param export_name: The name of the configured Azure Export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#export_name AzureUcConfig#export_name}
        :param export_path: The path where the Azure Export is saved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#export_path AzureUcConfig#export_path}
        :param storage_account: The name of the storage account where the Azure Export is saved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#storage_account AzureUcConfig#storage_account}
        :param storage_container: The name of the storage container where the Azure Export is saved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#storage_container AzureUcConfig#storage_container}
        '''
        value = AzureUcConfigActualBillConfig(
            export_name=export_name,
            export_path=export_path,
            storage_account=storage_account,
            storage_container=storage_container,
        )

        return typing.cast(None, jsii.invoke(self, "putActualBillConfig", [value]))

    @jsii.member(jsii_name="putAmortizedBillConfig")
    def put_amortized_bill_config(
        self,
        *,
        export_name: builtins.str,
        export_path: builtins.str,
        storage_account: builtins.str,
        storage_container: builtins.str,
    ) -> None:
        '''
        :param export_name: The name of the configured Azure Export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#export_name AzureUcConfig#export_name}
        :param export_path: The path where the Azure Export is saved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#export_path AzureUcConfig#export_path}
        :param storage_account: The name of the storage account where the Azure Export is saved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#storage_account AzureUcConfig#storage_account}
        :param storage_container: The name of the storage container where the Azure Export is saved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#storage_container AzureUcConfig#storage_container}
        '''
        value = AzureUcConfigAmortizedBillConfig(
            export_name=export_name,
            export_path=export_path,
            storage_account=storage_account,
            storage_container=storage_container,
        )

        return typing.cast(None, jsii.invoke(self, "putAmortizedBillConfig", [value]))

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
    @jsii.member(jsii_name="actualBillConfig")
    def actual_bill_config(self) -> "AzureUcConfigActualBillConfigOutputReference":
        return typing.cast("AzureUcConfigActualBillConfigOutputReference", jsii.get(self, "actualBillConfig"))

    @builtins.property
    @jsii.member(jsii_name="amortizedBillConfig")
    def amortized_bill_config(
        self,
    ) -> "AzureUcConfigAmortizedBillConfigOutputReference":
        return typing.cast("AzureUcConfigAmortizedBillConfigOutputReference", jsii.get(self, "amortizedBillConfig"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="errorMessages")
    def error_messages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "errorMessages"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="statusUpdatedAt")
    def status_updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="actualBillConfigInput")
    def actual_bill_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AzureUcConfigActualBillConfig"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AzureUcConfigActualBillConfig"]], jsii.get(self, "actualBillConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="amortizedBillConfigInput")
    def amortized_bill_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AzureUcConfigAmortizedBillConfig"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AzureUcConfigAmortizedBillConfig"]], jsii.get(self, "amortizedBillConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf0cc28bfabd2101557ba9d4ab0f0b528b60a2794d00e0a14a898fae36bacf98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123d7bdfd0b2737ffcf9a8b87eba9096e0c2eb39d2bc9572119206f014f43de4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a356860480b8b295bcc6c29404723f95c5ce9359d6e0f25e664077574085b435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.azureUcConfig.AzureUcConfigActualBillConfig",
    jsii_struct_bases=[],
    name_mapping={
        "export_name": "exportName",
        "export_path": "exportPath",
        "storage_account": "storageAccount",
        "storage_container": "storageContainer",
    },
)
class AzureUcConfigActualBillConfig:
    def __init__(
        self,
        *,
        export_name: builtins.str,
        export_path: builtins.str,
        storage_account: builtins.str,
        storage_container: builtins.str,
    ) -> None:
        '''
        :param export_name: The name of the configured Azure Export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#export_name AzureUcConfig#export_name}
        :param export_path: The path where the Azure Export is saved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#export_path AzureUcConfig#export_path}
        :param storage_account: The name of the storage account where the Azure Export is saved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#storage_account AzureUcConfig#storage_account}
        :param storage_container: The name of the storage container where the Azure Export is saved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#storage_container AzureUcConfig#storage_container}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab4973ab69bb07ee03d002193daa165b666610b3dde462efc99669a6e65afea6)
            check_type(argname="argument export_name", value=export_name, expected_type=type_hints["export_name"])
            check_type(argname="argument export_path", value=export_path, expected_type=type_hints["export_path"])
            check_type(argname="argument storage_account", value=storage_account, expected_type=type_hints["storage_account"])
            check_type(argname="argument storage_container", value=storage_container, expected_type=type_hints["storage_container"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "export_name": export_name,
            "export_path": export_path,
            "storage_account": storage_account,
            "storage_container": storage_container,
        }

    @builtins.property
    def export_name(self) -> builtins.str:
        '''The name of the configured Azure Export.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#export_name AzureUcConfig#export_name}
        '''
        result = self._values.get("export_name")
        assert result is not None, "Required property 'export_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def export_path(self) -> builtins.str:
        '''The path where the Azure Export is saved.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#export_path AzureUcConfig#export_path}
        '''
        result = self._values.get("export_path")
        assert result is not None, "Required property 'export_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account(self) -> builtins.str:
        '''The name of the storage account where the Azure Export is saved.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#storage_account AzureUcConfig#storage_account}
        '''
        result = self._values.get("storage_account")
        assert result is not None, "Required property 'storage_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_container(self) -> builtins.str:
        '''The name of the storage container where the Azure Export is saved.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#storage_container AzureUcConfig#storage_container}
        '''
        result = self._values.get("storage_container")
        assert result is not None, "Required property 'storage_container' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzureUcConfigActualBillConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AzureUcConfigActualBillConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.azureUcConfig.AzureUcConfigActualBillConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4417fbac6c1a798a4cd962004971bed10a87f074b0acdf036fe6198485d7ee4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="exportNameInput")
    def export_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportNameInput"))

    @builtins.property
    @jsii.member(jsii_name="exportPathInput")
    def export_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportPathInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountInput")
    def storage_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="storageContainerInput")
    def storage_container_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageContainerInput"))

    @builtins.property
    @jsii.member(jsii_name="exportName")
    def export_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportName"))

    @export_name.setter
    def export_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3fb02ed0f5ad83bfaf1a7ca9e8e36c8ad3518f95a6cf29ea38eba9573f287b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exportPath")
    def export_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportPath"))

    @export_path.setter
    def export_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7cea43924f817e9b96279bcf148fb08de61d973fcd319919dbc4293749004f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccount")
    def storage_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccount"))

    @storage_account.setter
    def storage_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10cfb7e7d760bbdad57620c8f249d4e366f2f86933d0b97b5f69e80c3233ecb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageContainer")
    def storage_container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageContainer"))

    @storage_container.setter
    def storage_container(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3b3457925bf3e1aff4776bd315a24b1f3b65f672d33344cf04d43613e1d8a78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageContainer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AzureUcConfigActualBillConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AzureUcConfigActualBillConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AzureUcConfigActualBillConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67309b04ba712067d4f7b932c37830734ecd5b209aabebdb77fcfd62c16d3767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.azureUcConfig.AzureUcConfigAmortizedBillConfig",
    jsii_struct_bases=[],
    name_mapping={
        "export_name": "exportName",
        "export_path": "exportPath",
        "storage_account": "storageAccount",
        "storage_container": "storageContainer",
    },
)
class AzureUcConfigAmortizedBillConfig:
    def __init__(
        self,
        *,
        export_name: builtins.str,
        export_path: builtins.str,
        storage_account: builtins.str,
        storage_container: builtins.str,
    ) -> None:
        '''
        :param export_name: The name of the configured Azure Export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#export_name AzureUcConfig#export_name}
        :param export_path: The path where the Azure Export is saved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#export_path AzureUcConfig#export_path}
        :param storage_account: The name of the storage account where the Azure Export is saved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#storage_account AzureUcConfig#storage_account}
        :param storage_container: The name of the storage container where the Azure Export is saved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#storage_container AzureUcConfig#storage_container}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a98ab6d5caf18f1dee394d4b3310012e6f06dd1eb0f903ff414f1cfaf47ffa89)
            check_type(argname="argument export_name", value=export_name, expected_type=type_hints["export_name"])
            check_type(argname="argument export_path", value=export_path, expected_type=type_hints["export_path"])
            check_type(argname="argument storage_account", value=storage_account, expected_type=type_hints["storage_account"])
            check_type(argname="argument storage_container", value=storage_container, expected_type=type_hints["storage_container"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "export_name": export_name,
            "export_path": export_path,
            "storage_account": storage_account,
            "storage_container": storage_container,
        }

    @builtins.property
    def export_name(self) -> builtins.str:
        '''The name of the configured Azure Export.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#export_name AzureUcConfig#export_name}
        '''
        result = self._values.get("export_name")
        assert result is not None, "Required property 'export_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def export_path(self) -> builtins.str:
        '''The path where the Azure Export is saved.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#export_path AzureUcConfig#export_path}
        '''
        result = self._values.get("export_path")
        assert result is not None, "Required property 'export_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account(self) -> builtins.str:
        '''The name of the storage account where the Azure Export is saved.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#storage_account AzureUcConfig#storage_account}
        '''
        result = self._values.get("storage_account")
        assert result is not None, "Required property 'storage_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_container(self) -> builtins.str:
        '''The name of the storage container where the Azure Export is saved.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#storage_container AzureUcConfig#storage_container}
        '''
        result = self._values.get("storage_container")
        assert result is not None, "Required property 'storage_container' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzureUcConfigAmortizedBillConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AzureUcConfigAmortizedBillConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.azureUcConfig.AzureUcConfigAmortizedBillConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e55b524738fa503c34dd2a84996de173da0218b8844b991af74c4d45b4c69409)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="exportNameInput")
    def export_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportNameInput"))

    @builtins.property
    @jsii.member(jsii_name="exportPathInput")
    def export_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportPathInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountInput")
    def storage_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="storageContainerInput")
    def storage_container_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageContainerInput"))

    @builtins.property
    @jsii.member(jsii_name="exportName")
    def export_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportName"))

    @export_name.setter
    def export_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22aed334f89fd9b57140aadc6b3321fc7e26970ef8f29ea3587ee264b2977669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exportPath")
    def export_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportPath"))

    @export_path.setter
    def export_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e63201aafaa962e25edd1912563e27bb9a30ee3de475db41e6eeb35f3be60240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccount")
    def storage_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccount"))

    @storage_account.setter
    def storage_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1113c93f903c4865fa447593f2c8e999ebc1b0d11b055cacbd11cfa17e54f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageContainer")
    def storage_container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageContainer"))

    @storage_container.setter
    def storage_container(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c128f6d6bda40d218bd5ddfdb6348f221bf78aa9c7eaeec634077cdff978ab8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageContainer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AzureUcConfigAmortizedBillConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AzureUcConfigAmortizedBillConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AzureUcConfigAmortizedBillConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0fa13125ccb0506c4e8fcfdf0ae64572c8b48d77d914067a484bfb8054d95e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.azureUcConfig.AzureUcConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_id": "accountId",
        "actual_bill_config": "actualBillConfig",
        "amortized_bill_config": "amortizedBillConfig",
        "client_id": "clientId",
        "scope": "scope",
    },
)
class AzureUcConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_id: builtins.str,
        actual_bill_config: typing.Union[AzureUcConfigActualBillConfig, typing.Dict[builtins.str, typing.Any]],
        amortized_bill_config: typing.Union[AzureUcConfigAmortizedBillConfig, typing.Dict[builtins.str, typing.Any]],
        client_id: builtins.str,
        scope: builtins.str,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The tenant ID of the Azure account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#account_id AzureUcConfig#account_id}
        :param actual_bill_config: actual_bill_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#actual_bill_config AzureUcConfig#actual_bill_config}
        :param amortized_bill_config: amortized_bill_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#amortized_bill_config AzureUcConfig#amortized_bill_config}
        :param client_id: The client ID of the Azure account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#client_id AzureUcConfig#client_id}
        :param scope: The scope of your observed subscription. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#scope AzureUcConfig#scope}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(actual_bill_config, dict):
            actual_bill_config = AzureUcConfigActualBillConfig(**actual_bill_config)
        if isinstance(amortized_bill_config, dict):
            amortized_bill_config = AzureUcConfigAmortizedBillConfig(**amortized_bill_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__737cbfca498ce42e3d9d54fbf98a7ccb7694cdd92a182126660305cf69257e47)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument actual_bill_config", value=actual_bill_config, expected_type=type_hints["actual_bill_config"])
            check_type(argname="argument amortized_bill_config", value=amortized_bill_config, expected_type=type_hints["amortized_bill_config"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "actual_bill_config": actual_bill_config,
            "amortized_bill_config": amortized_bill_config,
            "client_id": client_id,
            "scope": scope,
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
    def account_id(self) -> builtins.str:
        '''The tenant ID of the Azure account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#account_id AzureUcConfig#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actual_bill_config(self) -> AzureUcConfigActualBillConfig:
        '''actual_bill_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#actual_bill_config AzureUcConfig#actual_bill_config}
        '''
        result = self._values.get("actual_bill_config")
        assert result is not None, "Required property 'actual_bill_config' is missing"
        return typing.cast(AzureUcConfigActualBillConfig, result)

    @builtins.property
    def amortized_bill_config(self) -> AzureUcConfigAmortizedBillConfig:
        '''amortized_bill_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#amortized_bill_config AzureUcConfig#amortized_bill_config}
        '''
        result = self._values.get("amortized_bill_config")
        assert result is not None, "Required property 'amortized_bill_config' is missing"
        return typing.cast(AzureUcConfigAmortizedBillConfig, result)

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The client ID of the Azure account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#client_id AzureUcConfig#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> builtins.str:
        '''The scope of your observed subscription.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/azure_uc_config#scope AzureUcConfig#scope}
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzureUcConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AzureUcConfig",
    "AzureUcConfigActualBillConfig",
    "AzureUcConfigActualBillConfigOutputReference",
    "AzureUcConfigAmortizedBillConfig",
    "AzureUcConfigAmortizedBillConfigOutputReference",
    "AzureUcConfigConfig",
]

publication.publish()

def _typecheckingstub__7ff038216101e1d15cf3494eed4c4f79f97722a5ab007076456b18b432c387f7(
    scope_: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account_id: builtins.str,
    actual_bill_config: typing.Union[AzureUcConfigActualBillConfig, typing.Dict[builtins.str, typing.Any]],
    amortized_bill_config: typing.Union[AzureUcConfigAmortizedBillConfig, typing.Dict[builtins.str, typing.Any]],
    client_id: builtins.str,
    scope: builtins.str,
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

def _typecheckingstub__4708a522c7c9c629b14387aae94b0e3e4ba04a680aa53aa09f376785fd99e44c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf0cc28bfabd2101557ba9d4ab0f0b528b60a2794d00e0a14a898fae36bacf98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123d7bdfd0b2737ffcf9a8b87eba9096e0c2eb39d2bc9572119206f014f43de4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a356860480b8b295bcc6c29404723f95c5ce9359d6e0f25e664077574085b435(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab4973ab69bb07ee03d002193daa165b666610b3dde462efc99669a6e65afea6(
    *,
    export_name: builtins.str,
    export_path: builtins.str,
    storage_account: builtins.str,
    storage_container: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4417fbac6c1a798a4cd962004971bed10a87f074b0acdf036fe6198485d7ee4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3fb02ed0f5ad83bfaf1a7ca9e8e36c8ad3518f95a6cf29ea38eba9573f287b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7cea43924f817e9b96279bcf148fb08de61d973fcd319919dbc4293749004f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10cfb7e7d760bbdad57620c8f249d4e366f2f86933d0b97b5f69e80c3233ecb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b3457925bf3e1aff4776bd315a24b1f3b65f672d33344cf04d43613e1d8a78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67309b04ba712067d4f7b932c37830734ecd5b209aabebdb77fcfd62c16d3767(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AzureUcConfigActualBillConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98ab6d5caf18f1dee394d4b3310012e6f06dd1eb0f903ff414f1cfaf47ffa89(
    *,
    export_name: builtins.str,
    export_path: builtins.str,
    storage_account: builtins.str,
    storage_container: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55b524738fa503c34dd2a84996de173da0218b8844b991af74c4d45b4c69409(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22aed334f89fd9b57140aadc6b3321fc7e26970ef8f29ea3587ee264b2977669(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63201aafaa962e25edd1912563e27bb9a30ee3de475db41e6eeb35f3be60240(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1113c93f903c4865fa447593f2c8e999ebc1b0d11b055cacbd11cfa17e54f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c128f6d6bda40d218bd5ddfdb6348f221bf78aa9c7eaeec634077cdff978ab8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0fa13125ccb0506c4e8fcfdf0ae64572c8b48d77d914067a484bfb8054d95e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AzureUcConfigAmortizedBillConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737cbfca498ce42e3d9d54fbf98a7ccb7694cdd92a182126660305cf69257e47(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    actual_bill_config: typing.Union[AzureUcConfigActualBillConfig, typing.Dict[builtins.str, typing.Any]],
    amortized_bill_config: typing.Union[AzureUcConfigAmortizedBillConfig, typing.Dict[builtins.str, typing.Any]],
    client_id: builtins.str,
    scope: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

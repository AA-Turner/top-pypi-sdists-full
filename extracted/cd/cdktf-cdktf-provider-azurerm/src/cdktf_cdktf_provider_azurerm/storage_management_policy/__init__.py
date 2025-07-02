r'''
# `azurerm_storage_management_policy`

Refer to the Terraform Registry for docs: [`azurerm_storage_management_policy`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy).
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


class StorageManagementPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy azurerm_storage_management_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        storage_account_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageManagementPolicyRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["StorageManagementPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy azurerm_storage_management_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#storage_account_id StorageManagementPolicy#storage_account_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#id StorageManagementPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#rule StorageManagementPolicy#rule}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#timeouts StorageManagementPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ee8a56eec37adb7c2a3f4ab5c2c39f7b43d0b2f1090b071a5b0f357e2c803cf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StorageManagementPolicyConfig(
            storage_account_id=storage_account_id,
            id=id,
            rule=rule,
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
        '''Generates CDKTF code for importing a StorageManagementPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StorageManagementPolicy to import.
        :param import_from_id: The id of the existing StorageManagementPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StorageManagementPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e6dffe171cac358fd0bcfe9de3cfe46c2b187df7ad05ffcecd412e43338097b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageManagementPolicyRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d068943ccb7c1809a7332bd71437368ec1c12960f8b9165fc98040c4112a49d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#create StorageManagementPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete StorageManagementPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#read StorageManagementPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#update StorageManagementPolicy#update}.
        '''
        value = StorageManagementPolicyTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRule")
    def reset_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRule", []))

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
    @jsii.member(jsii_name="rule")
    def rule(self) -> "StorageManagementPolicyRuleList":
        return typing.cast("StorageManagementPolicyRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "StorageManagementPolicyTimeoutsOutputReference":
        return typing.cast("StorageManagementPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageManagementPolicyRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageManagementPolicyRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountIdInput")
    def storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageManagementPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageManagementPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b25e37a7180e2ac254c304fe2f379e70147561190d9de234696cd10047f7bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountId")
    def storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountId"))

    @storage_account_id.setter
    def storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c050fc41b9dfa37f39ee45fc5d76b56bd10a9a6d96b77714123009104df9b54e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "storage_account_id": "storageAccountId",
        "id": "id",
        "rule": "rule",
        "timeouts": "timeouts",
    },
)
class StorageManagementPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        storage_account_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageManagementPolicyRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["StorageManagementPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#storage_account_id StorageManagementPolicy#storage_account_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#id StorageManagementPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#rule StorageManagementPolicy#rule}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#timeouts StorageManagementPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = StorageManagementPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83792fd5c10fbe180019ebd31024dacb4d3599d0422fa0fbf9cd54d7e917c45)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "storage_account_id": storage_account_id,
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
        if rule is not None:
            self._values["rule"] = rule
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
    def storage_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#storage_account_id StorageManagementPolicy#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        assert result is not None, "Required property 'storage_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#id StorageManagementPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageManagementPolicyRule"]]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#rule StorageManagementPolicy#rule}
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageManagementPolicyRule"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["StorageManagementPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#timeouts StorageManagementPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["StorageManagementPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageManagementPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyRule",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "enabled": "enabled",
        "filters": "filters",
        "name": "name",
    },
)
class StorageManagementPolicyRule:
    def __init__(
        self,
        *,
        actions: typing.Union["StorageManagementPolicyRuleActions", typing.Dict[builtins.str, typing.Any]],
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        filters: typing.Union["StorageManagementPolicyRuleFilters", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#actions StorageManagementPolicy#actions}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#enabled StorageManagementPolicy#enabled}.
        :param filters: filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#filters StorageManagementPolicy#filters}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#name StorageManagementPolicy#name}.
        '''
        if isinstance(actions, dict):
            actions = StorageManagementPolicyRuleActions(**actions)
        if isinstance(filters, dict):
            filters = StorageManagementPolicyRuleFilters(**filters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce437933eb5193414ff2ae7039cfa1972463d81a080e5888a2936b9c01ee126b)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "enabled": enabled,
            "filters": filters,
            "name": name,
        }

    @builtins.property
    def actions(self) -> "StorageManagementPolicyRuleActions":
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#actions StorageManagementPolicy#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast("StorageManagementPolicyRuleActions", result)

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#enabled StorageManagementPolicy#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def filters(self) -> "StorageManagementPolicyRuleFilters":
        '''filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#filters StorageManagementPolicy#filters}
        '''
        result = self._values.get("filters")
        assert result is not None, "Required property 'filters' is missing"
        return typing.cast("StorageManagementPolicyRuleFilters", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#name StorageManagementPolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageManagementPolicyRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyRuleActions",
    jsii_struct_bases=[],
    name_mapping={
        "base_blob": "baseBlob",
        "snapshot": "snapshot",
        "version": "version",
    },
)
class StorageManagementPolicyRuleActions:
    def __init__(
        self,
        *,
        base_blob: typing.Optional[typing.Union["StorageManagementPolicyRuleActionsBaseBlob", typing.Dict[builtins.str, typing.Any]]] = None,
        snapshot: typing.Optional[typing.Union["StorageManagementPolicyRuleActionsSnapshot", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[typing.Union["StorageManagementPolicyRuleActionsVersion", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param base_blob: base_blob block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#base_blob StorageManagementPolicy#base_blob}
        :param snapshot: snapshot block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#snapshot StorageManagementPolicy#snapshot}
        :param version: version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#version StorageManagementPolicy#version}
        '''
        if isinstance(base_blob, dict):
            base_blob = StorageManagementPolicyRuleActionsBaseBlob(**base_blob)
        if isinstance(snapshot, dict):
            snapshot = StorageManagementPolicyRuleActionsSnapshot(**snapshot)
        if isinstance(version, dict):
            version = StorageManagementPolicyRuleActionsVersion(**version)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__569c9e26e48015bf9b3337c30b019937ac89e9c867cfa552ce1ddf283e9def6e)
            check_type(argname="argument base_blob", value=base_blob, expected_type=type_hints["base_blob"])
            check_type(argname="argument snapshot", value=snapshot, expected_type=type_hints["snapshot"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if base_blob is not None:
            self._values["base_blob"] = base_blob
        if snapshot is not None:
            self._values["snapshot"] = snapshot
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def base_blob(
        self,
    ) -> typing.Optional["StorageManagementPolicyRuleActionsBaseBlob"]:
        '''base_blob block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#base_blob StorageManagementPolicy#base_blob}
        '''
        result = self._values.get("base_blob")
        return typing.cast(typing.Optional["StorageManagementPolicyRuleActionsBaseBlob"], result)

    @builtins.property
    def snapshot(self) -> typing.Optional["StorageManagementPolicyRuleActionsSnapshot"]:
        '''snapshot block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#snapshot StorageManagementPolicy#snapshot}
        '''
        result = self._values.get("snapshot")
        return typing.cast(typing.Optional["StorageManagementPolicyRuleActionsSnapshot"], result)

    @builtins.property
    def version(self) -> typing.Optional["StorageManagementPolicyRuleActionsVersion"]:
        '''version block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#version StorageManagementPolicy#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional["StorageManagementPolicyRuleActionsVersion"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageManagementPolicyRuleActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyRuleActionsBaseBlob",
    jsii_struct_bases=[],
    name_mapping={
        "auto_tier_to_hot_from_cool_enabled": "autoTierToHotFromCoolEnabled",
        "delete_after_days_since_creation_greater_than": "deleteAfterDaysSinceCreationGreaterThan",
        "delete_after_days_since_last_access_time_greater_than": "deleteAfterDaysSinceLastAccessTimeGreaterThan",
        "delete_after_days_since_modification_greater_than": "deleteAfterDaysSinceModificationGreaterThan",
        "tier_to_archive_after_days_since_creation_greater_than": "tierToArchiveAfterDaysSinceCreationGreaterThan",
        "tier_to_archive_after_days_since_last_access_time_greater_than": "tierToArchiveAfterDaysSinceLastAccessTimeGreaterThan",
        "tier_to_archive_after_days_since_last_tier_change_greater_than": "tierToArchiveAfterDaysSinceLastTierChangeGreaterThan",
        "tier_to_archive_after_days_since_modification_greater_than": "tierToArchiveAfterDaysSinceModificationGreaterThan",
        "tier_to_cold_after_days_since_creation_greater_than": "tierToColdAfterDaysSinceCreationGreaterThan",
        "tier_to_cold_after_days_since_last_access_time_greater_than": "tierToColdAfterDaysSinceLastAccessTimeGreaterThan",
        "tier_to_cold_after_days_since_modification_greater_than": "tierToColdAfterDaysSinceModificationGreaterThan",
        "tier_to_cool_after_days_since_creation_greater_than": "tierToCoolAfterDaysSinceCreationGreaterThan",
        "tier_to_cool_after_days_since_last_access_time_greater_than": "tierToCoolAfterDaysSinceLastAccessTimeGreaterThan",
        "tier_to_cool_after_days_since_modification_greater_than": "tierToCoolAfterDaysSinceModificationGreaterThan",
    },
)
class StorageManagementPolicyRuleActionsBaseBlob:
    def __init__(
        self,
        *,
        auto_tier_to_hot_from_cool_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
        delete_after_days_since_last_access_time_greater_than: typing.Optional[jsii.Number] = None,
        delete_after_days_since_modification_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_archive_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_archive_after_days_since_last_access_time_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_archive_after_days_since_last_tier_change_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_archive_after_days_since_modification_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_cold_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_cold_after_days_since_last_access_time_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_cold_after_days_since_modification_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_cool_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_cool_after_days_since_last_access_time_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_cool_after_days_since_modification_greater_than: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param auto_tier_to_hot_from_cool_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#auto_tier_to_hot_from_cool_enabled StorageManagementPolicy#auto_tier_to_hot_from_cool_enabled}.
        :param delete_after_days_since_creation_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete_after_days_since_creation_greater_than StorageManagementPolicy#delete_after_days_since_creation_greater_than}.
        :param delete_after_days_since_last_access_time_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete_after_days_since_last_access_time_greater_than StorageManagementPolicy#delete_after_days_since_last_access_time_greater_than}.
        :param delete_after_days_since_modification_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete_after_days_since_modification_greater_than StorageManagementPolicy#delete_after_days_since_modification_greater_than}.
        :param tier_to_archive_after_days_since_creation_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_creation_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_creation_greater_than}.
        :param tier_to_archive_after_days_since_last_access_time_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_last_access_time_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_last_access_time_greater_than}.
        :param tier_to_archive_after_days_since_last_tier_change_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_last_tier_change_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_last_tier_change_greater_than}.
        :param tier_to_archive_after_days_since_modification_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_modification_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_modification_greater_than}.
        :param tier_to_cold_after_days_since_creation_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cold_after_days_since_creation_greater_than StorageManagementPolicy#tier_to_cold_after_days_since_creation_greater_than}.
        :param tier_to_cold_after_days_since_last_access_time_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cold_after_days_since_last_access_time_greater_than StorageManagementPolicy#tier_to_cold_after_days_since_last_access_time_greater_than}.
        :param tier_to_cold_after_days_since_modification_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cold_after_days_since_modification_greater_than StorageManagementPolicy#tier_to_cold_after_days_since_modification_greater_than}.
        :param tier_to_cool_after_days_since_creation_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cool_after_days_since_creation_greater_than StorageManagementPolicy#tier_to_cool_after_days_since_creation_greater_than}.
        :param tier_to_cool_after_days_since_last_access_time_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cool_after_days_since_last_access_time_greater_than StorageManagementPolicy#tier_to_cool_after_days_since_last_access_time_greater_than}.
        :param tier_to_cool_after_days_since_modification_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cool_after_days_since_modification_greater_than StorageManagementPolicy#tier_to_cool_after_days_since_modification_greater_than}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ea7720aa03bc82d65058a94a34ab2b6d356431acf43820014d7e85e8609e178)
            check_type(argname="argument auto_tier_to_hot_from_cool_enabled", value=auto_tier_to_hot_from_cool_enabled, expected_type=type_hints["auto_tier_to_hot_from_cool_enabled"])
            check_type(argname="argument delete_after_days_since_creation_greater_than", value=delete_after_days_since_creation_greater_than, expected_type=type_hints["delete_after_days_since_creation_greater_than"])
            check_type(argname="argument delete_after_days_since_last_access_time_greater_than", value=delete_after_days_since_last_access_time_greater_than, expected_type=type_hints["delete_after_days_since_last_access_time_greater_than"])
            check_type(argname="argument delete_after_days_since_modification_greater_than", value=delete_after_days_since_modification_greater_than, expected_type=type_hints["delete_after_days_since_modification_greater_than"])
            check_type(argname="argument tier_to_archive_after_days_since_creation_greater_than", value=tier_to_archive_after_days_since_creation_greater_than, expected_type=type_hints["tier_to_archive_after_days_since_creation_greater_than"])
            check_type(argname="argument tier_to_archive_after_days_since_last_access_time_greater_than", value=tier_to_archive_after_days_since_last_access_time_greater_than, expected_type=type_hints["tier_to_archive_after_days_since_last_access_time_greater_than"])
            check_type(argname="argument tier_to_archive_after_days_since_last_tier_change_greater_than", value=tier_to_archive_after_days_since_last_tier_change_greater_than, expected_type=type_hints["tier_to_archive_after_days_since_last_tier_change_greater_than"])
            check_type(argname="argument tier_to_archive_after_days_since_modification_greater_than", value=tier_to_archive_after_days_since_modification_greater_than, expected_type=type_hints["tier_to_archive_after_days_since_modification_greater_than"])
            check_type(argname="argument tier_to_cold_after_days_since_creation_greater_than", value=tier_to_cold_after_days_since_creation_greater_than, expected_type=type_hints["tier_to_cold_after_days_since_creation_greater_than"])
            check_type(argname="argument tier_to_cold_after_days_since_last_access_time_greater_than", value=tier_to_cold_after_days_since_last_access_time_greater_than, expected_type=type_hints["tier_to_cold_after_days_since_last_access_time_greater_than"])
            check_type(argname="argument tier_to_cold_after_days_since_modification_greater_than", value=tier_to_cold_after_days_since_modification_greater_than, expected_type=type_hints["tier_to_cold_after_days_since_modification_greater_than"])
            check_type(argname="argument tier_to_cool_after_days_since_creation_greater_than", value=tier_to_cool_after_days_since_creation_greater_than, expected_type=type_hints["tier_to_cool_after_days_since_creation_greater_than"])
            check_type(argname="argument tier_to_cool_after_days_since_last_access_time_greater_than", value=tier_to_cool_after_days_since_last_access_time_greater_than, expected_type=type_hints["tier_to_cool_after_days_since_last_access_time_greater_than"])
            check_type(argname="argument tier_to_cool_after_days_since_modification_greater_than", value=tier_to_cool_after_days_since_modification_greater_than, expected_type=type_hints["tier_to_cool_after_days_since_modification_greater_than"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_tier_to_hot_from_cool_enabled is not None:
            self._values["auto_tier_to_hot_from_cool_enabled"] = auto_tier_to_hot_from_cool_enabled
        if delete_after_days_since_creation_greater_than is not None:
            self._values["delete_after_days_since_creation_greater_than"] = delete_after_days_since_creation_greater_than
        if delete_after_days_since_last_access_time_greater_than is not None:
            self._values["delete_after_days_since_last_access_time_greater_than"] = delete_after_days_since_last_access_time_greater_than
        if delete_after_days_since_modification_greater_than is not None:
            self._values["delete_after_days_since_modification_greater_than"] = delete_after_days_since_modification_greater_than
        if tier_to_archive_after_days_since_creation_greater_than is not None:
            self._values["tier_to_archive_after_days_since_creation_greater_than"] = tier_to_archive_after_days_since_creation_greater_than
        if tier_to_archive_after_days_since_last_access_time_greater_than is not None:
            self._values["tier_to_archive_after_days_since_last_access_time_greater_than"] = tier_to_archive_after_days_since_last_access_time_greater_than
        if tier_to_archive_after_days_since_last_tier_change_greater_than is not None:
            self._values["tier_to_archive_after_days_since_last_tier_change_greater_than"] = tier_to_archive_after_days_since_last_tier_change_greater_than
        if tier_to_archive_after_days_since_modification_greater_than is not None:
            self._values["tier_to_archive_after_days_since_modification_greater_than"] = tier_to_archive_after_days_since_modification_greater_than
        if tier_to_cold_after_days_since_creation_greater_than is not None:
            self._values["tier_to_cold_after_days_since_creation_greater_than"] = tier_to_cold_after_days_since_creation_greater_than
        if tier_to_cold_after_days_since_last_access_time_greater_than is not None:
            self._values["tier_to_cold_after_days_since_last_access_time_greater_than"] = tier_to_cold_after_days_since_last_access_time_greater_than
        if tier_to_cold_after_days_since_modification_greater_than is not None:
            self._values["tier_to_cold_after_days_since_modification_greater_than"] = tier_to_cold_after_days_since_modification_greater_than
        if tier_to_cool_after_days_since_creation_greater_than is not None:
            self._values["tier_to_cool_after_days_since_creation_greater_than"] = tier_to_cool_after_days_since_creation_greater_than
        if tier_to_cool_after_days_since_last_access_time_greater_than is not None:
            self._values["tier_to_cool_after_days_since_last_access_time_greater_than"] = tier_to_cool_after_days_since_last_access_time_greater_than
        if tier_to_cool_after_days_since_modification_greater_than is not None:
            self._values["tier_to_cool_after_days_since_modification_greater_than"] = tier_to_cool_after_days_since_modification_greater_than

    @builtins.property
    def auto_tier_to_hot_from_cool_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#auto_tier_to_hot_from_cool_enabled StorageManagementPolicy#auto_tier_to_hot_from_cool_enabled}.'''
        result = self._values.get("auto_tier_to_hot_from_cool_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delete_after_days_since_creation_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete_after_days_since_creation_greater_than StorageManagementPolicy#delete_after_days_since_creation_greater_than}.'''
        result = self._values.get("delete_after_days_since_creation_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def delete_after_days_since_last_access_time_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete_after_days_since_last_access_time_greater_than StorageManagementPolicy#delete_after_days_since_last_access_time_greater_than}.'''
        result = self._values.get("delete_after_days_since_last_access_time_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def delete_after_days_since_modification_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete_after_days_since_modification_greater_than StorageManagementPolicy#delete_after_days_since_modification_greater_than}.'''
        result = self._values.get("delete_after_days_since_modification_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_to_archive_after_days_since_creation_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_creation_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_creation_greater_than}.'''
        result = self._values.get("tier_to_archive_after_days_since_creation_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_to_archive_after_days_since_last_access_time_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_last_access_time_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_last_access_time_greater_than}.'''
        result = self._values.get("tier_to_archive_after_days_since_last_access_time_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_to_archive_after_days_since_last_tier_change_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_last_tier_change_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_last_tier_change_greater_than}.'''
        result = self._values.get("tier_to_archive_after_days_since_last_tier_change_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_to_archive_after_days_since_modification_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_modification_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_modification_greater_than}.'''
        result = self._values.get("tier_to_archive_after_days_since_modification_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_to_cold_after_days_since_creation_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cold_after_days_since_creation_greater_than StorageManagementPolicy#tier_to_cold_after_days_since_creation_greater_than}.'''
        result = self._values.get("tier_to_cold_after_days_since_creation_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_to_cold_after_days_since_last_access_time_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cold_after_days_since_last_access_time_greater_than StorageManagementPolicy#tier_to_cold_after_days_since_last_access_time_greater_than}.'''
        result = self._values.get("tier_to_cold_after_days_since_last_access_time_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_to_cold_after_days_since_modification_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cold_after_days_since_modification_greater_than StorageManagementPolicy#tier_to_cold_after_days_since_modification_greater_than}.'''
        result = self._values.get("tier_to_cold_after_days_since_modification_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_to_cool_after_days_since_creation_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cool_after_days_since_creation_greater_than StorageManagementPolicy#tier_to_cool_after_days_since_creation_greater_than}.'''
        result = self._values.get("tier_to_cool_after_days_since_creation_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_to_cool_after_days_since_last_access_time_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cool_after_days_since_last_access_time_greater_than StorageManagementPolicy#tier_to_cool_after_days_since_last_access_time_greater_than}.'''
        result = self._values.get("tier_to_cool_after_days_since_last_access_time_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_to_cool_after_days_since_modification_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cool_after_days_since_modification_greater_than StorageManagementPolicy#tier_to_cool_after_days_since_modification_greater_than}.'''
        result = self._values.get("tier_to_cool_after_days_since_modification_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageManagementPolicyRuleActionsBaseBlob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageManagementPolicyRuleActionsBaseBlobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyRuleActionsBaseBlobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0ffc3a5a1658b1dafc6ea71155640198dd73779eb8a24885821dcb4e70f1cc2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAutoTierToHotFromCoolEnabled")
    def reset_auto_tier_to_hot_from_cool_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoTierToHotFromCoolEnabled", []))

    @jsii.member(jsii_name="resetDeleteAfterDaysSinceCreationGreaterThan")
    def reset_delete_after_days_since_creation_greater_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteAfterDaysSinceCreationGreaterThan", []))

    @jsii.member(jsii_name="resetDeleteAfterDaysSinceLastAccessTimeGreaterThan")
    def reset_delete_after_days_since_last_access_time_greater_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteAfterDaysSinceLastAccessTimeGreaterThan", []))

    @jsii.member(jsii_name="resetDeleteAfterDaysSinceModificationGreaterThan")
    def reset_delete_after_days_since_modification_greater_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteAfterDaysSinceModificationGreaterThan", []))

    @jsii.member(jsii_name="resetTierToArchiveAfterDaysSinceCreationGreaterThan")
    def reset_tier_to_archive_after_days_since_creation_greater_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierToArchiveAfterDaysSinceCreationGreaterThan", []))

    @jsii.member(jsii_name="resetTierToArchiveAfterDaysSinceLastAccessTimeGreaterThan")
    def reset_tier_to_archive_after_days_since_last_access_time_greater_than(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierToArchiveAfterDaysSinceLastAccessTimeGreaterThan", []))

    @jsii.member(jsii_name="resetTierToArchiveAfterDaysSinceLastTierChangeGreaterThan")
    def reset_tier_to_archive_after_days_since_last_tier_change_greater_than(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierToArchiveAfterDaysSinceLastTierChangeGreaterThan", []))

    @jsii.member(jsii_name="resetTierToArchiveAfterDaysSinceModificationGreaterThan")
    def reset_tier_to_archive_after_days_since_modification_greater_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierToArchiveAfterDaysSinceModificationGreaterThan", []))

    @jsii.member(jsii_name="resetTierToColdAfterDaysSinceCreationGreaterThan")
    def reset_tier_to_cold_after_days_since_creation_greater_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierToColdAfterDaysSinceCreationGreaterThan", []))

    @jsii.member(jsii_name="resetTierToColdAfterDaysSinceLastAccessTimeGreaterThan")
    def reset_tier_to_cold_after_days_since_last_access_time_greater_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierToColdAfterDaysSinceLastAccessTimeGreaterThan", []))

    @jsii.member(jsii_name="resetTierToColdAfterDaysSinceModificationGreaterThan")
    def reset_tier_to_cold_after_days_since_modification_greater_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierToColdAfterDaysSinceModificationGreaterThan", []))

    @jsii.member(jsii_name="resetTierToCoolAfterDaysSinceCreationGreaterThan")
    def reset_tier_to_cool_after_days_since_creation_greater_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierToCoolAfterDaysSinceCreationGreaterThan", []))

    @jsii.member(jsii_name="resetTierToCoolAfterDaysSinceLastAccessTimeGreaterThan")
    def reset_tier_to_cool_after_days_since_last_access_time_greater_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierToCoolAfterDaysSinceLastAccessTimeGreaterThan", []))

    @jsii.member(jsii_name="resetTierToCoolAfterDaysSinceModificationGreaterThan")
    def reset_tier_to_cool_after_days_since_modification_greater_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierToCoolAfterDaysSinceModificationGreaterThan", []))

    @builtins.property
    @jsii.member(jsii_name="autoTierToHotFromCoolEnabledInput")
    def auto_tier_to_hot_from_cool_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoTierToHotFromCoolEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteAfterDaysSinceCreationGreaterThanInput")
    def delete_after_days_since_creation_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deleteAfterDaysSinceCreationGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteAfterDaysSinceLastAccessTimeGreaterThanInput")
    def delete_after_days_since_last_access_time_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deleteAfterDaysSinceLastAccessTimeGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteAfterDaysSinceModificationGreaterThanInput")
    def delete_after_days_since_modification_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deleteAfterDaysSinceModificationGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="tierToArchiveAfterDaysSinceCreationGreaterThanInput")
    def tier_to_archive_after_days_since_creation_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tierToArchiveAfterDaysSinceCreationGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="tierToArchiveAfterDaysSinceLastAccessTimeGreaterThanInput")
    def tier_to_archive_after_days_since_last_access_time_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tierToArchiveAfterDaysSinceLastAccessTimeGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="tierToArchiveAfterDaysSinceLastTierChangeGreaterThanInput")
    def tier_to_archive_after_days_since_last_tier_change_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tierToArchiveAfterDaysSinceLastTierChangeGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="tierToArchiveAfterDaysSinceModificationGreaterThanInput")
    def tier_to_archive_after_days_since_modification_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tierToArchiveAfterDaysSinceModificationGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="tierToColdAfterDaysSinceCreationGreaterThanInput")
    def tier_to_cold_after_days_since_creation_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tierToColdAfterDaysSinceCreationGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="tierToColdAfterDaysSinceLastAccessTimeGreaterThanInput")
    def tier_to_cold_after_days_since_last_access_time_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tierToColdAfterDaysSinceLastAccessTimeGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="tierToColdAfterDaysSinceModificationGreaterThanInput")
    def tier_to_cold_after_days_since_modification_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tierToColdAfterDaysSinceModificationGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="tierToCoolAfterDaysSinceCreationGreaterThanInput")
    def tier_to_cool_after_days_since_creation_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tierToCoolAfterDaysSinceCreationGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="tierToCoolAfterDaysSinceLastAccessTimeGreaterThanInput")
    def tier_to_cool_after_days_since_last_access_time_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tierToCoolAfterDaysSinceLastAccessTimeGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="tierToCoolAfterDaysSinceModificationGreaterThanInput")
    def tier_to_cool_after_days_since_modification_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tierToCoolAfterDaysSinceModificationGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="autoTierToHotFromCoolEnabled")
    def auto_tier_to_hot_from_cool_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoTierToHotFromCoolEnabled"))

    @auto_tier_to_hot_from_cool_enabled.setter
    def auto_tier_to_hot_from_cool_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f87f2f4f7f928e99e4a171fbd50d978c70e377469604c5c1d78302a027f58cd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoTierToHotFromCoolEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteAfterDaysSinceCreationGreaterThan")
    def delete_after_days_since_creation_greater_than(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deleteAfterDaysSinceCreationGreaterThan"))

    @delete_after_days_since_creation_greater_than.setter
    def delete_after_days_since_creation_greater_than(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__317af771180932a7807117f9a9ec1c10c28f9260fdbbc13f09b83e0c05c5cb0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteAfterDaysSinceCreationGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteAfterDaysSinceLastAccessTimeGreaterThan")
    def delete_after_days_since_last_access_time_greater_than(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deleteAfterDaysSinceLastAccessTimeGreaterThan"))

    @delete_after_days_since_last_access_time_greater_than.setter
    def delete_after_days_since_last_access_time_greater_than(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__846c068721bfcf5b7fded1e7c7a769162a23f7aeaeeecfd23a3995fda72c1060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteAfterDaysSinceLastAccessTimeGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteAfterDaysSinceModificationGreaterThan")
    def delete_after_days_since_modification_greater_than(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deleteAfterDaysSinceModificationGreaterThan"))

    @delete_after_days_since_modification_greater_than.setter
    def delete_after_days_since_modification_greater_than(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f47f9e1970bff40f5c69d994e0b776dfe561563ba21d34f88acedc05d6e89899)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteAfterDaysSinceModificationGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierToArchiveAfterDaysSinceCreationGreaterThan")
    def tier_to_archive_after_days_since_creation_greater_than(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tierToArchiveAfterDaysSinceCreationGreaterThan"))

    @tier_to_archive_after_days_since_creation_greater_than.setter
    def tier_to_archive_after_days_since_creation_greater_than(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ea5bfe9b43b7b0acb0d39eac719af364869bfb232cb3dfe81a9284f493bb48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierToArchiveAfterDaysSinceCreationGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierToArchiveAfterDaysSinceLastAccessTimeGreaterThan")
    def tier_to_archive_after_days_since_last_access_time_greater_than(
        self,
    ) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tierToArchiveAfterDaysSinceLastAccessTimeGreaterThan"))

    @tier_to_archive_after_days_since_last_access_time_greater_than.setter
    def tier_to_archive_after_days_since_last_access_time_greater_than(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ce7ee0884b2468da0a2788947d61293448f5657bdabf34b629d18f2ef01e7f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierToArchiveAfterDaysSinceLastAccessTimeGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierToArchiveAfterDaysSinceLastTierChangeGreaterThan")
    def tier_to_archive_after_days_since_last_tier_change_greater_than(
        self,
    ) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tierToArchiveAfterDaysSinceLastTierChangeGreaterThan"))

    @tier_to_archive_after_days_since_last_tier_change_greater_than.setter
    def tier_to_archive_after_days_since_last_tier_change_greater_than(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c50701381a935fccbbae808d7eac4f4ce535d9c303180716e62aa8bff5bbf15b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierToArchiveAfterDaysSinceLastTierChangeGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierToArchiveAfterDaysSinceModificationGreaterThan")
    def tier_to_archive_after_days_since_modification_greater_than(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tierToArchiveAfterDaysSinceModificationGreaterThan"))

    @tier_to_archive_after_days_since_modification_greater_than.setter
    def tier_to_archive_after_days_since_modification_greater_than(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b240a731f150ac7119b17d624eb74b13e2ef73248e651f633eb7d0f1f9a5e37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierToArchiveAfterDaysSinceModificationGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierToColdAfterDaysSinceCreationGreaterThan")
    def tier_to_cold_after_days_since_creation_greater_than(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tierToColdAfterDaysSinceCreationGreaterThan"))

    @tier_to_cold_after_days_since_creation_greater_than.setter
    def tier_to_cold_after_days_since_creation_greater_than(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba212f79ad6b698228026e1cdb806cc9d5e469e284cc7709404ca8cebde5b567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierToColdAfterDaysSinceCreationGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierToColdAfterDaysSinceLastAccessTimeGreaterThan")
    def tier_to_cold_after_days_since_last_access_time_greater_than(
        self,
    ) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tierToColdAfterDaysSinceLastAccessTimeGreaterThan"))

    @tier_to_cold_after_days_since_last_access_time_greater_than.setter
    def tier_to_cold_after_days_since_last_access_time_greater_than(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55aa4e91f34c5b37662c29f3b1a54e32a0cdeeafe14d4638a47db1d2440693ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierToColdAfterDaysSinceLastAccessTimeGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierToColdAfterDaysSinceModificationGreaterThan")
    def tier_to_cold_after_days_since_modification_greater_than(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tierToColdAfterDaysSinceModificationGreaterThan"))

    @tier_to_cold_after_days_since_modification_greater_than.setter
    def tier_to_cold_after_days_since_modification_greater_than(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c11b73cd437db89e11508a29502d0d81896b032afd05ae2e101f37c9b5c1e5ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierToColdAfterDaysSinceModificationGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierToCoolAfterDaysSinceCreationGreaterThan")
    def tier_to_cool_after_days_since_creation_greater_than(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tierToCoolAfterDaysSinceCreationGreaterThan"))

    @tier_to_cool_after_days_since_creation_greater_than.setter
    def tier_to_cool_after_days_since_creation_greater_than(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08ba82d2501556cfa2a31a257cbe876424e90f62a1660c27f0d1f472f918f5e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierToCoolAfterDaysSinceCreationGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierToCoolAfterDaysSinceLastAccessTimeGreaterThan")
    def tier_to_cool_after_days_since_last_access_time_greater_than(
        self,
    ) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tierToCoolAfterDaysSinceLastAccessTimeGreaterThan"))

    @tier_to_cool_after_days_since_last_access_time_greater_than.setter
    def tier_to_cool_after_days_since_last_access_time_greater_than(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d47459954eac94a84124384c095fe07bc82fd331e2317841b6a8efafe076dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierToCoolAfterDaysSinceLastAccessTimeGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierToCoolAfterDaysSinceModificationGreaterThan")
    def tier_to_cool_after_days_since_modification_greater_than(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tierToCoolAfterDaysSinceModificationGreaterThan"))

    @tier_to_cool_after_days_since_modification_greater_than.setter
    def tier_to_cool_after_days_since_modification_greater_than(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b049ac66f46ce8b86f0c1ec42642557cb30ef28f194098c68215233c471b9358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierToCoolAfterDaysSinceModificationGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageManagementPolicyRuleActionsBaseBlob]:
        return typing.cast(typing.Optional[StorageManagementPolicyRuleActionsBaseBlob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageManagementPolicyRuleActionsBaseBlob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07ba30159715b8055a4c3951da04a110c3fe2e578aa3694e6dfd418a76f7df9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageManagementPolicyRuleActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyRuleActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e251e02008c4321b61b1ecfd6e6b5bac4b0f4c13e106207db4e4b50ad0cd23c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBaseBlob")
    def put_base_blob(
        self,
        *,
        auto_tier_to_hot_from_cool_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
        delete_after_days_since_last_access_time_greater_than: typing.Optional[jsii.Number] = None,
        delete_after_days_since_modification_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_archive_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_archive_after_days_since_last_access_time_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_archive_after_days_since_last_tier_change_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_archive_after_days_since_modification_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_cold_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_cold_after_days_since_last_access_time_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_cold_after_days_since_modification_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_cool_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_cool_after_days_since_last_access_time_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_cool_after_days_since_modification_greater_than: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param auto_tier_to_hot_from_cool_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#auto_tier_to_hot_from_cool_enabled StorageManagementPolicy#auto_tier_to_hot_from_cool_enabled}.
        :param delete_after_days_since_creation_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete_after_days_since_creation_greater_than StorageManagementPolicy#delete_after_days_since_creation_greater_than}.
        :param delete_after_days_since_last_access_time_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete_after_days_since_last_access_time_greater_than StorageManagementPolicy#delete_after_days_since_last_access_time_greater_than}.
        :param delete_after_days_since_modification_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete_after_days_since_modification_greater_than StorageManagementPolicy#delete_after_days_since_modification_greater_than}.
        :param tier_to_archive_after_days_since_creation_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_creation_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_creation_greater_than}.
        :param tier_to_archive_after_days_since_last_access_time_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_last_access_time_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_last_access_time_greater_than}.
        :param tier_to_archive_after_days_since_last_tier_change_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_last_tier_change_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_last_tier_change_greater_than}.
        :param tier_to_archive_after_days_since_modification_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_modification_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_modification_greater_than}.
        :param tier_to_cold_after_days_since_creation_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cold_after_days_since_creation_greater_than StorageManagementPolicy#tier_to_cold_after_days_since_creation_greater_than}.
        :param tier_to_cold_after_days_since_last_access_time_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cold_after_days_since_last_access_time_greater_than StorageManagementPolicy#tier_to_cold_after_days_since_last_access_time_greater_than}.
        :param tier_to_cold_after_days_since_modification_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cold_after_days_since_modification_greater_than StorageManagementPolicy#tier_to_cold_after_days_since_modification_greater_than}.
        :param tier_to_cool_after_days_since_creation_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cool_after_days_since_creation_greater_than StorageManagementPolicy#tier_to_cool_after_days_since_creation_greater_than}.
        :param tier_to_cool_after_days_since_last_access_time_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cool_after_days_since_last_access_time_greater_than StorageManagementPolicy#tier_to_cool_after_days_since_last_access_time_greater_than}.
        :param tier_to_cool_after_days_since_modification_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cool_after_days_since_modification_greater_than StorageManagementPolicy#tier_to_cool_after_days_since_modification_greater_than}.
        '''
        value = StorageManagementPolicyRuleActionsBaseBlob(
            auto_tier_to_hot_from_cool_enabled=auto_tier_to_hot_from_cool_enabled,
            delete_after_days_since_creation_greater_than=delete_after_days_since_creation_greater_than,
            delete_after_days_since_last_access_time_greater_than=delete_after_days_since_last_access_time_greater_than,
            delete_after_days_since_modification_greater_than=delete_after_days_since_modification_greater_than,
            tier_to_archive_after_days_since_creation_greater_than=tier_to_archive_after_days_since_creation_greater_than,
            tier_to_archive_after_days_since_last_access_time_greater_than=tier_to_archive_after_days_since_last_access_time_greater_than,
            tier_to_archive_after_days_since_last_tier_change_greater_than=tier_to_archive_after_days_since_last_tier_change_greater_than,
            tier_to_archive_after_days_since_modification_greater_than=tier_to_archive_after_days_since_modification_greater_than,
            tier_to_cold_after_days_since_creation_greater_than=tier_to_cold_after_days_since_creation_greater_than,
            tier_to_cold_after_days_since_last_access_time_greater_than=tier_to_cold_after_days_since_last_access_time_greater_than,
            tier_to_cold_after_days_since_modification_greater_than=tier_to_cold_after_days_since_modification_greater_than,
            tier_to_cool_after_days_since_creation_greater_than=tier_to_cool_after_days_since_creation_greater_than,
            tier_to_cool_after_days_since_last_access_time_greater_than=tier_to_cool_after_days_since_last_access_time_greater_than,
            tier_to_cool_after_days_since_modification_greater_than=tier_to_cool_after_days_since_modification_greater_than,
        )

        return typing.cast(None, jsii.invoke(self, "putBaseBlob", [value]))

    @jsii.member(jsii_name="putSnapshot")
    def put_snapshot(
        self,
        *,
        change_tier_to_archive_after_days_since_creation: typing.Optional[jsii.Number] = None,
        change_tier_to_cool_after_days_since_creation: typing.Optional[jsii.Number] = None,
        delete_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_archive_after_days_since_last_tier_change_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_cold_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param change_tier_to_archive_after_days_since_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#change_tier_to_archive_after_days_since_creation StorageManagementPolicy#change_tier_to_archive_after_days_since_creation}.
        :param change_tier_to_cool_after_days_since_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#change_tier_to_cool_after_days_since_creation StorageManagementPolicy#change_tier_to_cool_after_days_since_creation}.
        :param delete_after_days_since_creation_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete_after_days_since_creation_greater_than StorageManagementPolicy#delete_after_days_since_creation_greater_than}.
        :param tier_to_archive_after_days_since_last_tier_change_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_last_tier_change_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_last_tier_change_greater_than}.
        :param tier_to_cold_after_days_since_creation_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cold_after_days_since_creation_greater_than StorageManagementPolicy#tier_to_cold_after_days_since_creation_greater_than}.
        '''
        value = StorageManagementPolicyRuleActionsSnapshot(
            change_tier_to_archive_after_days_since_creation=change_tier_to_archive_after_days_since_creation,
            change_tier_to_cool_after_days_since_creation=change_tier_to_cool_after_days_since_creation,
            delete_after_days_since_creation_greater_than=delete_after_days_since_creation_greater_than,
            tier_to_archive_after_days_since_last_tier_change_greater_than=tier_to_archive_after_days_since_last_tier_change_greater_than,
            tier_to_cold_after_days_since_creation_greater_than=tier_to_cold_after_days_since_creation_greater_than,
        )

        return typing.cast(None, jsii.invoke(self, "putSnapshot", [value]))

    @jsii.member(jsii_name="putVersion")
    def put_version(
        self,
        *,
        change_tier_to_archive_after_days_since_creation: typing.Optional[jsii.Number] = None,
        change_tier_to_cool_after_days_since_creation: typing.Optional[jsii.Number] = None,
        delete_after_days_since_creation: typing.Optional[jsii.Number] = None,
        tier_to_archive_after_days_since_last_tier_change_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_cold_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param change_tier_to_archive_after_days_since_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#change_tier_to_archive_after_days_since_creation StorageManagementPolicy#change_tier_to_archive_after_days_since_creation}.
        :param change_tier_to_cool_after_days_since_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#change_tier_to_cool_after_days_since_creation StorageManagementPolicy#change_tier_to_cool_after_days_since_creation}.
        :param delete_after_days_since_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete_after_days_since_creation StorageManagementPolicy#delete_after_days_since_creation}.
        :param tier_to_archive_after_days_since_last_tier_change_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_last_tier_change_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_last_tier_change_greater_than}.
        :param tier_to_cold_after_days_since_creation_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cold_after_days_since_creation_greater_than StorageManagementPolicy#tier_to_cold_after_days_since_creation_greater_than}.
        '''
        value = StorageManagementPolicyRuleActionsVersion(
            change_tier_to_archive_after_days_since_creation=change_tier_to_archive_after_days_since_creation,
            change_tier_to_cool_after_days_since_creation=change_tier_to_cool_after_days_since_creation,
            delete_after_days_since_creation=delete_after_days_since_creation,
            tier_to_archive_after_days_since_last_tier_change_greater_than=tier_to_archive_after_days_since_last_tier_change_greater_than,
            tier_to_cold_after_days_since_creation_greater_than=tier_to_cold_after_days_since_creation_greater_than,
        )

        return typing.cast(None, jsii.invoke(self, "putVersion", [value]))

    @jsii.member(jsii_name="resetBaseBlob")
    def reset_base_blob(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseBlob", []))

    @jsii.member(jsii_name="resetSnapshot")
    def reset_snapshot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshot", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="baseBlob")
    def base_blob(self) -> StorageManagementPolicyRuleActionsBaseBlobOutputReference:
        return typing.cast(StorageManagementPolicyRuleActionsBaseBlobOutputReference, jsii.get(self, "baseBlob"))

    @builtins.property
    @jsii.member(jsii_name="snapshot")
    def snapshot(self) -> "StorageManagementPolicyRuleActionsSnapshotOutputReference":
        return typing.cast("StorageManagementPolicyRuleActionsSnapshotOutputReference", jsii.get(self, "snapshot"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> "StorageManagementPolicyRuleActionsVersionOutputReference":
        return typing.cast("StorageManagementPolicyRuleActionsVersionOutputReference", jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="baseBlobInput")
    def base_blob_input(
        self,
    ) -> typing.Optional[StorageManagementPolicyRuleActionsBaseBlob]:
        return typing.cast(typing.Optional[StorageManagementPolicyRuleActionsBaseBlob], jsii.get(self, "baseBlobInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotInput")
    def snapshot_input(
        self,
    ) -> typing.Optional["StorageManagementPolicyRuleActionsSnapshot"]:
        return typing.cast(typing.Optional["StorageManagementPolicyRuleActionsSnapshot"], jsii.get(self, "snapshotInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(
        self,
    ) -> typing.Optional["StorageManagementPolicyRuleActionsVersion"]:
        return typing.cast(typing.Optional["StorageManagementPolicyRuleActionsVersion"], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageManagementPolicyRuleActions]:
        return typing.cast(typing.Optional[StorageManagementPolicyRuleActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageManagementPolicyRuleActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fa4f6c573e7c89b7978448558610a9f111833ad5cdef5de678fec49250d61b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyRuleActionsSnapshot",
    jsii_struct_bases=[],
    name_mapping={
        "change_tier_to_archive_after_days_since_creation": "changeTierToArchiveAfterDaysSinceCreation",
        "change_tier_to_cool_after_days_since_creation": "changeTierToCoolAfterDaysSinceCreation",
        "delete_after_days_since_creation_greater_than": "deleteAfterDaysSinceCreationGreaterThan",
        "tier_to_archive_after_days_since_last_tier_change_greater_than": "tierToArchiveAfterDaysSinceLastTierChangeGreaterThan",
        "tier_to_cold_after_days_since_creation_greater_than": "tierToColdAfterDaysSinceCreationGreaterThan",
    },
)
class StorageManagementPolicyRuleActionsSnapshot:
    def __init__(
        self,
        *,
        change_tier_to_archive_after_days_since_creation: typing.Optional[jsii.Number] = None,
        change_tier_to_cool_after_days_since_creation: typing.Optional[jsii.Number] = None,
        delete_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_archive_after_days_since_last_tier_change_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_cold_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param change_tier_to_archive_after_days_since_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#change_tier_to_archive_after_days_since_creation StorageManagementPolicy#change_tier_to_archive_after_days_since_creation}.
        :param change_tier_to_cool_after_days_since_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#change_tier_to_cool_after_days_since_creation StorageManagementPolicy#change_tier_to_cool_after_days_since_creation}.
        :param delete_after_days_since_creation_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete_after_days_since_creation_greater_than StorageManagementPolicy#delete_after_days_since_creation_greater_than}.
        :param tier_to_archive_after_days_since_last_tier_change_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_last_tier_change_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_last_tier_change_greater_than}.
        :param tier_to_cold_after_days_since_creation_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cold_after_days_since_creation_greater_than StorageManagementPolicy#tier_to_cold_after_days_since_creation_greater_than}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e648db8e62af2ad285e79470ab120076c11968b1b5fbfc1abb8756ffc1be7571)
            check_type(argname="argument change_tier_to_archive_after_days_since_creation", value=change_tier_to_archive_after_days_since_creation, expected_type=type_hints["change_tier_to_archive_after_days_since_creation"])
            check_type(argname="argument change_tier_to_cool_after_days_since_creation", value=change_tier_to_cool_after_days_since_creation, expected_type=type_hints["change_tier_to_cool_after_days_since_creation"])
            check_type(argname="argument delete_after_days_since_creation_greater_than", value=delete_after_days_since_creation_greater_than, expected_type=type_hints["delete_after_days_since_creation_greater_than"])
            check_type(argname="argument tier_to_archive_after_days_since_last_tier_change_greater_than", value=tier_to_archive_after_days_since_last_tier_change_greater_than, expected_type=type_hints["tier_to_archive_after_days_since_last_tier_change_greater_than"])
            check_type(argname="argument tier_to_cold_after_days_since_creation_greater_than", value=tier_to_cold_after_days_since_creation_greater_than, expected_type=type_hints["tier_to_cold_after_days_since_creation_greater_than"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if change_tier_to_archive_after_days_since_creation is not None:
            self._values["change_tier_to_archive_after_days_since_creation"] = change_tier_to_archive_after_days_since_creation
        if change_tier_to_cool_after_days_since_creation is not None:
            self._values["change_tier_to_cool_after_days_since_creation"] = change_tier_to_cool_after_days_since_creation
        if delete_after_days_since_creation_greater_than is not None:
            self._values["delete_after_days_since_creation_greater_than"] = delete_after_days_since_creation_greater_than
        if tier_to_archive_after_days_since_last_tier_change_greater_than is not None:
            self._values["tier_to_archive_after_days_since_last_tier_change_greater_than"] = tier_to_archive_after_days_since_last_tier_change_greater_than
        if tier_to_cold_after_days_since_creation_greater_than is not None:
            self._values["tier_to_cold_after_days_since_creation_greater_than"] = tier_to_cold_after_days_since_creation_greater_than

    @builtins.property
    def change_tier_to_archive_after_days_since_creation(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#change_tier_to_archive_after_days_since_creation StorageManagementPolicy#change_tier_to_archive_after_days_since_creation}.'''
        result = self._values.get("change_tier_to_archive_after_days_since_creation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def change_tier_to_cool_after_days_since_creation(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#change_tier_to_cool_after_days_since_creation StorageManagementPolicy#change_tier_to_cool_after_days_since_creation}.'''
        result = self._values.get("change_tier_to_cool_after_days_since_creation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def delete_after_days_since_creation_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete_after_days_since_creation_greater_than StorageManagementPolicy#delete_after_days_since_creation_greater_than}.'''
        result = self._values.get("delete_after_days_since_creation_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_to_archive_after_days_since_last_tier_change_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_last_tier_change_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_last_tier_change_greater_than}.'''
        result = self._values.get("tier_to_archive_after_days_since_last_tier_change_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_to_cold_after_days_since_creation_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cold_after_days_since_creation_greater_than StorageManagementPolicy#tier_to_cold_after_days_since_creation_greater_than}.'''
        result = self._values.get("tier_to_cold_after_days_since_creation_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageManagementPolicyRuleActionsSnapshot(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageManagementPolicyRuleActionsSnapshotOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyRuleActionsSnapshotOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f06f5759910e05d09b766724494f6150f815e2177f399da33073695e8db9c0f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetChangeTierToArchiveAfterDaysSinceCreation")
    def reset_change_tier_to_archive_after_days_since_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChangeTierToArchiveAfterDaysSinceCreation", []))

    @jsii.member(jsii_name="resetChangeTierToCoolAfterDaysSinceCreation")
    def reset_change_tier_to_cool_after_days_since_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChangeTierToCoolAfterDaysSinceCreation", []))

    @jsii.member(jsii_name="resetDeleteAfterDaysSinceCreationGreaterThan")
    def reset_delete_after_days_since_creation_greater_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteAfterDaysSinceCreationGreaterThan", []))

    @jsii.member(jsii_name="resetTierToArchiveAfterDaysSinceLastTierChangeGreaterThan")
    def reset_tier_to_archive_after_days_since_last_tier_change_greater_than(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierToArchiveAfterDaysSinceLastTierChangeGreaterThan", []))

    @jsii.member(jsii_name="resetTierToColdAfterDaysSinceCreationGreaterThan")
    def reset_tier_to_cold_after_days_since_creation_greater_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierToColdAfterDaysSinceCreationGreaterThan", []))

    @builtins.property
    @jsii.member(jsii_name="changeTierToArchiveAfterDaysSinceCreationInput")
    def change_tier_to_archive_after_days_since_creation_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "changeTierToArchiveAfterDaysSinceCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="changeTierToCoolAfterDaysSinceCreationInput")
    def change_tier_to_cool_after_days_since_creation_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "changeTierToCoolAfterDaysSinceCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteAfterDaysSinceCreationGreaterThanInput")
    def delete_after_days_since_creation_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deleteAfterDaysSinceCreationGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="tierToArchiveAfterDaysSinceLastTierChangeGreaterThanInput")
    def tier_to_archive_after_days_since_last_tier_change_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tierToArchiveAfterDaysSinceLastTierChangeGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="tierToColdAfterDaysSinceCreationGreaterThanInput")
    def tier_to_cold_after_days_since_creation_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tierToColdAfterDaysSinceCreationGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="changeTierToArchiveAfterDaysSinceCreation")
    def change_tier_to_archive_after_days_since_creation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "changeTierToArchiveAfterDaysSinceCreation"))

    @change_tier_to_archive_after_days_since_creation.setter
    def change_tier_to_archive_after_days_since_creation(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51b2b0cd67a5487b3e2e0699ccf710fe231491ad836086201fc49698f7b5f932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "changeTierToArchiveAfterDaysSinceCreation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="changeTierToCoolAfterDaysSinceCreation")
    def change_tier_to_cool_after_days_since_creation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "changeTierToCoolAfterDaysSinceCreation"))

    @change_tier_to_cool_after_days_since_creation.setter
    def change_tier_to_cool_after_days_since_creation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b818d3d273aef85750d1c6b0c29888e2cd4aca3503d3dafb137ed4d70c3697b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "changeTierToCoolAfterDaysSinceCreation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteAfterDaysSinceCreationGreaterThan")
    def delete_after_days_since_creation_greater_than(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deleteAfterDaysSinceCreationGreaterThan"))

    @delete_after_days_since_creation_greater_than.setter
    def delete_after_days_since_creation_greater_than(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f55ab3a288f861b3969feeb1bb64f0f625785b0fb726961162e0a86b5f6c65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteAfterDaysSinceCreationGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierToArchiveAfterDaysSinceLastTierChangeGreaterThan")
    def tier_to_archive_after_days_since_last_tier_change_greater_than(
        self,
    ) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tierToArchiveAfterDaysSinceLastTierChangeGreaterThan"))

    @tier_to_archive_after_days_since_last_tier_change_greater_than.setter
    def tier_to_archive_after_days_since_last_tier_change_greater_than(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26972456ba0bd33e7d2a77769ea2b4c73dc3dcebbfd1f86c8f324671aa1531e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierToArchiveAfterDaysSinceLastTierChangeGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierToColdAfterDaysSinceCreationGreaterThan")
    def tier_to_cold_after_days_since_creation_greater_than(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tierToColdAfterDaysSinceCreationGreaterThan"))

    @tier_to_cold_after_days_since_creation_greater_than.setter
    def tier_to_cold_after_days_since_creation_greater_than(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9059c6ddb21d9f48c3d4175422e4974b4a400f7e4c1a55ee56a8e9ee3bb4910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierToColdAfterDaysSinceCreationGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageManagementPolicyRuleActionsSnapshot]:
        return typing.cast(typing.Optional[StorageManagementPolicyRuleActionsSnapshot], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageManagementPolicyRuleActionsSnapshot],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f3f718a2680c85c248a3fdcb09b3a4bcfdcfa9874b732593e14401428ade39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyRuleActionsVersion",
    jsii_struct_bases=[],
    name_mapping={
        "change_tier_to_archive_after_days_since_creation": "changeTierToArchiveAfterDaysSinceCreation",
        "change_tier_to_cool_after_days_since_creation": "changeTierToCoolAfterDaysSinceCreation",
        "delete_after_days_since_creation": "deleteAfterDaysSinceCreation",
        "tier_to_archive_after_days_since_last_tier_change_greater_than": "tierToArchiveAfterDaysSinceLastTierChangeGreaterThan",
        "tier_to_cold_after_days_since_creation_greater_than": "tierToColdAfterDaysSinceCreationGreaterThan",
    },
)
class StorageManagementPolicyRuleActionsVersion:
    def __init__(
        self,
        *,
        change_tier_to_archive_after_days_since_creation: typing.Optional[jsii.Number] = None,
        change_tier_to_cool_after_days_since_creation: typing.Optional[jsii.Number] = None,
        delete_after_days_since_creation: typing.Optional[jsii.Number] = None,
        tier_to_archive_after_days_since_last_tier_change_greater_than: typing.Optional[jsii.Number] = None,
        tier_to_cold_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param change_tier_to_archive_after_days_since_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#change_tier_to_archive_after_days_since_creation StorageManagementPolicy#change_tier_to_archive_after_days_since_creation}.
        :param change_tier_to_cool_after_days_since_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#change_tier_to_cool_after_days_since_creation StorageManagementPolicy#change_tier_to_cool_after_days_since_creation}.
        :param delete_after_days_since_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete_after_days_since_creation StorageManagementPolicy#delete_after_days_since_creation}.
        :param tier_to_archive_after_days_since_last_tier_change_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_last_tier_change_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_last_tier_change_greater_than}.
        :param tier_to_cold_after_days_since_creation_greater_than: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cold_after_days_since_creation_greater_than StorageManagementPolicy#tier_to_cold_after_days_since_creation_greater_than}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b755c1b38da43bb1cc01ce3e97e04d652cae0457e32a127facda7db59d028e)
            check_type(argname="argument change_tier_to_archive_after_days_since_creation", value=change_tier_to_archive_after_days_since_creation, expected_type=type_hints["change_tier_to_archive_after_days_since_creation"])
            check_type(argname="argument change_tier_to_cool_after_days_since_creation", value=change_tier_to_cool_after_days_since_creation, expected_type=type_hints["change_tier_to_cool_after_days_since_creation"])
            check_type(argname="argument delete_after_days_since_creation", value=delete_after_days_since_creation, expected_type=type_hints["delete_after_days_since_creation"])
            check_type(argname="argument tier_to_archive_after_days_since_last_tier_change_greater_than", value=tier_to_archive_after_days_since_last_tier_change_greater_than, expected_type=type_hints["tier_to_archive_after_days_since_last_tier_change_greater_than"])
            check_type(argname="argument tier_to_cold_after_days_since_creation_greater_than", value=tier_to_cold_after_days_since_creation_greater_than, expected_type=type_hints["tier_to_cold_after_days_since_creation_greater_than"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if change_tier_to_archive_after_days_since_creation is not None:
            self._values["change_tier_to_archive_after_days_since_creation"] = change_tier_to_archive_after_days_since_creation
        if change_tier_to_cool_after_days_since_creation is not None:
            self._values["change_tier_to_cool_after_days_since_creation"] = change_tier_to_cool_after_days_since_creation
        if delete_after_days_since_creation is not None:
            self._values["delete_after_days_since_creation"] = delete_after_days_since_creation
        if tier_to_archive_after_days_since_last_tier_change_greater_than is not None:
            self._values["tier_to_archive_after_days_since_last_tier_change_greater_than"] = tier_to_archive_after_days_since_last_tier_change_greater_than
        if tier_to_cold_after_days_since_creation_greater_than is not None:
            self._values["tier_to_cold_after_days_since_creation_greater_than"] = tier_to_cold_after_days_since_creation_greater_than

    @builtins.property
    def change_tier_to_archive_after_days_since_creation(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#change_tier_to_archive_after_days_since_creation StorageManagementPolicy#change_tier_to_archive_after_days_since_creation}.'''
        result = self._values.get("change_tier_to_archive_after_days_since_creation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def change_tier_to_cool_after_days_since_creation(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#change_tier_to_cool_after_days_since_creation StorageManagementPolicy#change_tier_to_cool_after_days_since_creation}.'''
        result = self._values.get("change_tier_to_cool_after_days_since_creation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def delete_after_days_since_creation(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete_after_days_since_creation StorageManagementPolicy#delete_after_days_since_creation}.'''
        result = self._values.get("delete_after_days_since_creation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_to_archive_after_days_since_last_tier_change_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_archive_after_days_since_last_tier_change_greater_than StorageManagementPolicy#tier_to_archive_after_days_since_last_tier_change_greater_than}.'''
        result = self._values.get("tier_to_archive_after_days_since_last_tier_change_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_to_cold_after_days_since_creation_greater_than(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#tier_to_cold_after_days_since_creation_greater_than StorageManagementPolicy#tier_to_cold_after_days_since_creation_greater_than}.'''
        result = self._values.get("tier_to_cold_after_days_since_creation_greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageManagementPolicyRuleActionsVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageManagementPolicyRuleActionsVersionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyRuleActionsVersionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09c5e5cf498ec46ce3a78c60ab13f1e6f2c81ad491008f28c588fbd9c756303c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetChangeTierToArchiveAfterDaysSinceCreation")
    def reset_change_tier_to_archive_after_days_since_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChangeTierToArchiveAfterDaysSinceCreation", []))

    @jsii.member(jsii_name="resetChangeTierToCoolAfterDaysSinceCreation")
    def reset_change_tier_to_cool_after_days_since_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChangeTierToCoolAfterDaysSinceCreation", []))

    @jsii.member(jsii_name="resetDeleteAfterDaysSinceCreation")
    def reset_delete_after_days_since_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteAfterDaysSinceCreation", []))

    @jsii.member(jsii_name="resetTierToArchiveAfterDaysSinceLastTierChangeGreaterThan")
    def reset_tier_to_archive_after_days_since_last_tier_change_greater_than(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierToArchiveAfterDaysSinceLastTierChangeGreaterThan", []))

    @jsii.member(jsii_name="resetTierToColdAfterDaysSinceCreationGreaterThan")
    def reset_tier_to_cold_after_days_since_creation_greater_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierToColdAfterDaysSinceCreationGreaterThan", []))

    @builtins.property
    @jsii.member(jsii_name="changeTierToArchiveAfterDaysSinceCreationInput")
    def change_tier_to_archive_after_days_since_creation_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "changeTierToArchiveAfterDaysSinceCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="changeTierToCoolAfterDaysSinceCreationInput")
    def change_tier_to_cool_after_days_since_creation_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "changeTierToCoolAfterDaysSinceCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteAfterDaysSinceCreationInput")
    def delete_after_days_since_creation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deleteAfterDaysSinceCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="tierToArchiveAfterDaysSinceLastTierChangeGreaterThanInput")
    def tier_to_archive_after_days_since_last_tier_change_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tierToArchiveAfterDaysSinceLastTierChangeGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="tierToColdAfterDaysSinceCreationGreaterThanInput")
    def tier_to_cold_after_days_since_creation_greater_than_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tierToColdAfterDaysSinceCreationGreaterThanInput"))

    @builtins.property
    @jsii.member(jsii_name="changeTierToArchiveAfterDaysSinceCreation")
    def change_tier_to_archive_after_days_since_creation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "changeTierToArchiveAfterDaysSinceCreation"))

    @change_tier_to_archive_after_days_since_creation.setter
    def change_tier_to_archive_after_days_since_creation(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af3308845e022025ee2643d8550027dcdfa1b9218d05a210350c8ed0ee55113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "changeTierToArchiveAfterDaysSinceCreation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="changeTierToCoolAfterDaysSinceCreation")
    def change_tier_to_cool_after_days_since_creation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "changeTierToCoolAfterDaysSinceCreation"))

    @change_tier_to_cool_after_days_since_creation.setter
    def change_tier_to_cool_after_days_since_creation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb8801dda3a4bb28430eb4a8f6547a667c5bd0f1b06597b89c93e35f22284779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "changeTierToCoolAfterDaysSinceCreation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteAfterDaysSinceCreation")
    def delete_after_days_since_creation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deleteAfterDaysSinceCreation"))

    @delete_after_days_since_creation.setter
    def delete_after_days_since_creation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__281aa376966cb0c048e802136b9a43c9d0af39a9766eb6d65b6bb75ae73b505c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteAfterDaysSinceCreation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierToArchiveAfterDaysSinceLastTierChangeGreaterThan")
    def tier_to_archive_after_days_since_last_tier_change_greater_than(
        self,
    ) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tierToArchiveAfterDaysSinceLastTierChangeGreaterThan"))

    @tier_to_archive_after_days_since_last_tier_change_greater_than.setter
    def tier_to_archive_after_days_since_last_tier_change_greater_than(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__210d3db090008b4e5aa60bb4028ec94eaf762146c14467304ac007542dcfa44a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierToArchiveAfterDaysSinceLastTierChangeGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierToColdAfterDaysSinceCreationGreaterThan")
    def tier_to_cold_after_days_since_creation_greater_than(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tierToColdAfterDaysSinceCreationGreaterThan"))

    @tier_to_cold_after_days_since_creation_greater_than.setter
    def tier_to_cold_after_days_since_creation_greater_than(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0842b81f077e0c0cb8fa806d2938789dc6defe4c873449cd938ae85f676becad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierToColdAfterDaysSinceCreationGreaterThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageManagementPolicyRuleActionsVersion]:
        return typing.cast(typing.Optional[StorageManagementPolicyRuleActionsVersion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageManagementPolicyRuleActionsVersion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9962a38c0f380d433490211d2132bcdf824c51f294be3a69561999681301fb57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyRuleFilters",
    jsii_struct_bases=[],
    name_mapping={
        "blob_types": "blobTypes",
        "match_blob_index_tag": "matchBlobIndexTag",
        "prefix_match": "prefixMatch",
    },
)
class StorageManagementPolicyRuleFilters:
    def __init__(
        self,
        *,
        blob_types: typing.Sequence[builtins.str],
        match_blob_index_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageManagementPolicyRuleFiltersMatchBlobIndexTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
        prefix_match: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param blob_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#blob_types StorageManagementPolicy#blob_types}.
        :param match_blob_index_tag: match_blob_index_tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#match_blob_index_tag StorageManagementPolicy#match_blob_index_tag}
        :param prefix_match: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#prefix_match StorageManagementPolicy#prefix_match}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4932dfee554c4f976587cbbf77521ac32ded59573f3fb608fe14e68f91e4bb50)
            check_type(argname="argument blob_types", value=blob_types, expected_type=type_hints["blob_types"])
            check_type(argname="argument match_blob_index_tag", value=match_blob_index_tag, expected_type=type_hints["match_blob_index_tag"])
            check_type(argname="argument prefix_match", value=prefix_match, expected_type=type_hints["prefix_match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "blob_types": blob_types,
        }
        if match_blob_index_tag is not None:
            self._values["match_blob_index_tag"] = match_blob_index_tag
        if prefix_match is not None:
            self._values["prefix_match"] = prefix_match

    @builtins.property
    def blob_types(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#blob_types StorageManagementPolicy#blob_types}.'''
        result = self._values.get("blob_types")
        assert result is not None, "Required property 'blob_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def match_blob_index_tag(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageManagementPolicyRuleFiltersMatchBlobIndexTag"]]]:
        '''match_blob_index_tag block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#match_blob_index_tag StorageManagementPolicy#match_blob_index_tag}
        '''
        result = self._values.get("match_blob_index_tag")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageManagementPolicyRuleFiltersMatchBlobIndexTag"]]], result)

    @builtins.property
    def prefix_match(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#prefix_match StorageManagementPolicy#prefix_match}.'''
        result = self._values.get("prefix_match")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageManagementPolicyRuleFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyRuleFiltersMatchBlobIndexTag",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value", "operation": "operation"},
)
class StorageManagementPolicyRuleFiltersMatchBlobIndexTag:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: builtins.str,
        operation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#name StorageManagementPolicy#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#value StorageManagementPolicy#value}.
        :param operation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#operation StorageManagementPolicy#operation}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__985b35484c6b185e898d57737378f555c705bedb52be90ea5308f96d8859b298)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }
        if operation is not None:
            self._values["operation"] = operation

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#name StorageManagementPolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#value StorageManagementPolicy#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#operation StorageManagementPolicy#operation}.'''
        result = self._values.get("operation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageManagementPolicyRuleFiltersMatchBlobIndexTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageManagementPolicyRuleFiltersMatchBlobIndexTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyRuleFiltersMatchBlobIndexTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3116f22faca6a73186bed67025a4c485bb4b26c46aa106fec322b883f7dfaf87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StorageManagementPolicyRuleFiltersMatchBlobIndexTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fcbb48ea3c217ad1da2fad3793547b5d7c148cb9b064009854bb24162ff0032)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageManagementPolicyRuleFiltersMatchBlobIndexTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4b306ff862b64f33518e88b5d9f5b9247f12fe9c185488018d8da55192bcca3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d5005ecbfe12f1e7f16b561ac42d43f391161760a06d3480c2b3110ddc07f9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66615457a24dd1416a371c48244ff75960868c3b0816d778390020467e1d22fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageManagementPolicyRuleFiltersMatchBlobIndexTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageManagementPolicyRuleFiltersMatchBlobIndexTag]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageManagementPolicyRuleFiltersMatchBlobIndexTag]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35500b6b6918d66459d3bbb218e49458fb73c3d83b3f2ca511f7c4645205ad9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageManagementPolicyRuleFiltersMatchBlobIndexTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyRuleFiltersMatchBlobIndexTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__604035bc20b5eece0c97cb4e2279468888a257cc22f99778fa3853f79cb2697d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOperation")
    def reset_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperation", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="operationInput")
    def operation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2b6fd76e8eaf71c1e83fef2c9f350ff860fc48b1190610ffbb23d44ff9ccb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operation"))

    @operation.setter
    def operation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a826d72e9f9fefe7a5b243711738ef3f1eeff58de2d69689ee852c36b05fe8ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ab05bdb14db21788db9c0f4e312c76e0066dd2d30beae1fb3852df20d5e959)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageManagementPolicyRuleFiltersMatchBlobIndexTag]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageManagementPolicyRuleFiltersMatchBlobIndexTag]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageManagementPolicyRuleFiltersMatchBlobIndexTag]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5f9d146b7d0db78fc4e3070f15f9ddb57ca34b6667e7ef78cd80dbb00eb631f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageManagementPolicyRuleFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyRuleFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f5a850d9e2fb3cbae0cdef729b1a08da5f72bbda06f0369ade25b31ba0aac90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMatchBlobIndexTag")
    def put_match_blob_index_tag(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageManagementPolicyRuleFiltersMatchBlobIndexTag, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69515c95ce1bb9343af5fe4b4bb950d18adae654af3751e18f7c4d6465fa2d95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatchBlobIndexTag", [value]))

    @jsii.member(jsii_name="resetMatchBlobIndexTag")
    def reset_match_blob_index_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchBlobIndexTag", []))

    @jsii.member(jsii_name="resetPrefixMatch")
    def reset_prefix_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixMatch", []))

    @builtins.property
    @jsii.member(jsii_name="matchBlobIndexTag")
    def match_blob_index_tag(
        self,
    ) -> StorageManagementPolicyRuleFiltersMatchBlobIndexTagList:
        return typing.cast(StorageManagementPolicyRuleFiltersMatchBlobIndexTagList, jsii.get(self, "matchBlobIndexTag"))

    @builtins.property
    @jsii.member(jsii_name="blobTypesInput")
    def blob_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "blobTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="matchBlobIndexTagInput")
    def match_blob_index_tag_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageManagementPolicyRuleFiltersMatchBlobIndexTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageManagementPolicyRuleFiltersMatchBlobIndexTag]]], jsii.get(self, "matchBlobIndexTagInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixMatchInput")
    def prefix_match_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "prefixMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="blobTypes")
    def blob_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "blobTypes"))

    @blob_types.setter
    def blob_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d82271dbc31d9f6cf2040113ce2ae809c84096e08e3ae8d555bd37a9be60e9e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blobTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixMatch")
    def prefix_match(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "prefixMatch"))

    @prefix_match.setter
    def prefix_match(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4311ccb2bb859ff0690cf4653c765b2a6bb714c3ae2c53924e3229575c55ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageManagementPolicyRuleFilters]:
        return typing.cast(typing.Optional[StorageManagementPolicyRuleFilters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageManagementPolicyRuleFilters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dfb816cf2c49adc0ac8d6eea835a96c848350def100cc9b0e8005dbcc3824be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageManagementPolicyRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c5595508174564daee6c13cc5284056b50957a276558cb00ff054475f56cb88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "StorageManagementPolicyRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4167adfd401229818ba618253e05ed6708660b4ea7e3a6aaf44387c445975cd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageManagementPolicyRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4766d1e0fdc4b0d01236c2b199246a45f73fa986d6aa1a6d8ad36cc9b8aed0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10766191d730e1c0baaa3ff83dbd7dcff2674a85ac12ffb4ada58926c254520d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__022b4df2b7091fabfa6d5ad758dc146a46196435fb349089b06054985fe5aa7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageManagementPolicyRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageManagementPolicyRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageManagementPolicyRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__318baa9645d0654db72a080535f86fcf2db2e4462b36b27d7269934b833c97b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageManagementPolicyRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87235a6ab93bf7601cc557fa602361c0756a127f7ccc7b0276c15713d3bbc5ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        *,
        base_blob: typing.Optional[typing.Union[StorageManagementPolicyRuleActionsBaseBlob, typing.Dict[builtins.str, typing.Any]]] = None,
        snapshot: typing.Optional[typing.Union[StorageManagementPolicyRuleActionsSnapshot, typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[typing.Union[StorageManagementPolicyRuleActionsVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param base_blob: base_blob block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#base_blob StorageManagementPolicy#base_blob}
        :param snapshot: snapshot block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#snapshot StorageManagementPolicy#snapshot}
        :param version: version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#version StorageManagementPolicy#version}
        '''
        value = StorageManagementPolicyRuleActions(
            base_blob=base_blob, snapshot=snapshot, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putFilters")
    def put_filters(
        self,
        *,
        blob_types: typing.Sequence[builtins.str],
        match_blob_index_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageManagementPolicyRuleFiltersMatchBlobIndexTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
        prefix_match: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param blob_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#blob_types StorageManagementPolicy#blob_types}.
        :param match_blob_index_tag: match_blob_index_tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#match_blob_index_tag StorageManagementPolicy#match_blob_index_tag}
        :param prefix_match: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#prefix_match StorageManagementPolicy#prefix_match}.
        '''
        value = StorageManagementPolicyRuleFilters(
            blob_types=blob_types,
            match_blob_index_tag=match_blob_index_tag,
            prefix_match=prefix_match,
        )

        return typing.cast(None, jsii.invoke(self, "putFilters", [value]))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> StorageManagementPolicyRuleActionsOutputReference:
        return typing.cast(StorageManagementPolicyRuleActionsOutputReference, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="filters")
    def filters(self) -> StorageManagementPolicyRuleFiltersOutputReference:
        return typing.cast(StorageManagementPolicyRuleFiltersOutputReference, jsii.get(self, "filters"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[StorageManagementPolicyRuleActions]:
        return typing.cast(typing.Optional[StorageManagementPolicyRuleActions], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="filtersInput")
    def filters_input(self) -> typing.Optional[StorageManagementPolicyRuleFilters]:
        return typing.cast(typing.Optional[StorageManagementPolicyRuleFilters], jsii.get(self, "filtersInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8ff58a0ddfe117c58647b575fbaa43313260ded16a90fd25339297daf0bdbfe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa9817ac098d6171f27a4cf0877a8b8448c16a240af9196170f0d048ccf3833)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageManagementPolicyRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageManagementPolicyRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageManagementPolicyRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df36d77f69409c337df0a00e32bac26a8225e2c10170d2f18b5d6e2edcc22c94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class StorageManagementPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#create StorageManagementPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete StorageManagementPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#read StorageManagementPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#update StorageManagementPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b104ef49ddbf59696f1f6eeec528951a2989e8d7a23c9d50956b700fae4dae)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#create StorageManagementPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#delete StorageManagementPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#read StorageManagementPolicy#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_management_policy#update StorageManagementPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageManagementPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageManagementPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageManagementPolicy.StorageManagementPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9b6e72ef736b9cd583c7ed5280291f83ab4d4876eda5132b32bdf7c2e9e4d2e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0525d511c122c600515c64cb65c99144ccacd20a0c7697e4450966871087cc2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ed30a6f6ff9f743addc065710b0752d06ee69195c8e1d1c931492edca7daf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9979f9c39b9b7e83468d73df575c9aff8106d6e974b5c53d90bc1259daeab9c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29ea12b43dfe898842f62c94018a09dcef4f8b6882dd9a6f51dbf3afb03b8e7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageManagementPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageManagementPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageManagementPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__990b8855cc8aa7f93e9c33c133bfc936b7476658af6a9265364a1f2ed05a9bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StorageManagementPolicy",
    "StorageManagementPolicyConfig",
    "StorageManagementPolicyRule",
    "StorageManagementPolicyRuleActions",
    "StorageManagementPolicyRuleActionsBaseBlob",
    "StorageManagementPolicyRuleActionsBaseBlobOutputReference",
    "StorageManagementPolicyRuleActionsOutputReference",
    "StorageManagementPolicyRuleActionsSnapshot",
    "StorageManagementPolicyRuleActionsSnapshotOutputReference",
    "StorageManagementPolicyRuleActionsVersion",
    "StorageManagementPolicyRuleActionsVersionOutputReference",
    "StorageManagementPolicyRuleFilters",
    "StorageManagementPolicyRuleFiltersMatchBlobIndexTag",
    "StorageManagementPolicyRuleFiltersMatchBlobIndexTagList",
    "StorageManagementPolicyRuleFiltersMatchBlobIndexTagOutputReference",
    "StorageManagementPolicyRuleFiltersOutputReference",
    "StorageManagementPolicyRuleList",
    "StorageManagementPolicyRuleOutputReference",
    "StorageManagementPolicyTimeouts",
    "StorageManagementPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6ee8a56eec37adb7c2a3f4ab5c2c39f7b43d0b2f1090b071a5b0f357e2c803cf(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    storage_account_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageManagementPolicyRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[StorageManagementPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3e6dffe171cac358fd0bcfe9de3cfe46c2b187df7ad05ffcecd412e43338097b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d068943ccb7c1809a7332bd71437368ec1c12960f8b9165fc98040c4112a49d8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageManagementPolicyRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b25e37a7180e2ac254c304fe2f379e70147561190d9de234696cd10047f7bc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c050fc41b9dfa37f39ee45fc5d76b56bd10a9a6d96b77714123009104df9b54e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83792fd5c10fbe180019ebd31024dacb4d3599d0422fa0fbf9cd54d7e917c45(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage_account_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageManagementPolicyRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[StorageManagementPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce437933eb5193414ff2ae7039cfa1972463d81a080e5888a2936b9c01ee126b(
    *,
    actions: typing.Union[StorageManagementPolicyRuleActions, typing.Dict[builtins.str, typing.Any]],
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    filters: typing.Union[StorageManagementPolicyRuleFilters, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__569c9e26e48015bf9b3337c30b019937ac89e9c867cfa552ce1ddf283e9def6e(
    *,
    base_blob: typing.Optional[typing.Union[StorageManagementPolicyRuleActionsBaseBlob, typing.Dict[builtins.str, typing.Any]]] = None,
    snapshot: typing.Optional[typing.Union[StorageManagementPolicyRuleActionsSnapshot, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[typing.Union[StorageManagementPolicyRuleActionsVersion, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ea7720aa03bc82d65058a94a34ab2b6d356431acf43820014d7e85e8609e178(
    *,
    auto_tier_to_hot_from_cool_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
    delete_after_days_since_last_access_time_greater_than: typing.Optional[jsii.Number] = None,
    delete_after_days_since_modification_greater_than: typing.Optional[jsii.Number] = None,
    tier_to_archive_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
    tier_to_archive_after_days_since_last_access_time_greater_than: typing.Optional[jsii.Number] = None,
    tier_to_archive_after_days_since_last_tier_change_greater_than: typing.Optional[jsii.Number] = None,
    tier_to_archive_after_days_since_modification_greater_than: typing.Optional[jsii.Number] = None,
    tier_to_cold_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
    tier_to_cold_after_days_since_last_access_time_greater_than: typing.Optional[jsii.Number] = None,
    tier_to_cold_after_days_since_modification_greater_than: typing.Optional[jsii.Number] = None,
    tier_to_cool_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
    tier_to_cool_after_days_since_last_access_time_greater_than: typing.Optional[jsii.Number] = None,
    tier_to_cool_after_days_since_modification_greater_than: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ffc3a5a1658b1dafc6ea71155640198dd73779eb8a24885821dcb4e70f1cc2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f87f2f4f7f928e99e4a171fbd50d978c70e377469604c5c1d78302a027f58cd4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317af771180932a7807117f9a9ec1c10c28f9260fdbbc13f09b83e0c05c5cb0c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846c068721bfcf5b7fded1e7c7a769162a23f7aeaeeecfd23a3995fda72c1060(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f47f9e1970bff40f5c69d994e0b776dfe561563ba21d34f88acedc05d6e89899(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ea5bfe9b43b7b0acb0d39eac719af364869bfb232cb3dfe81a9284f493bb48(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce7ee0884b2468da0a2788947d61293448f5657bdabf34b629d18f2ef01e7f0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c50701381a935fccbbae808d7eac4f4ce535d9c303180716e62aa8bff5bbf15b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b240a731f150ac7119b17d624eb74b13e2ef73248e651f633eb7d0f1f9a5e37(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba212f79ad6b698228026e1cdb806cc9d5e469e284cc7709404ca8cebde5b567(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55aa4e91f34c5b37662c29f3b1a54e32a0cdeeafe14d4638a47db1d2440693ad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11b73cd437db89e11508a29502d0d81896b032afd05ae2e101f37c9b5c1e5ba(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ba82d2501556cfa2a31a257cbe876424e90f62a1660c27f0d1f472f918f5e7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d47459954eac94a84124384c095fe07bc82fd331e2317841b6a8efafe076dd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b049ac66f46ce8b86f0c1ec42642557cb30ef28f194098c68215233c471b9358(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07ba30159715b8055a4c3951da04a110c3fe2e578aa3694e6dfd418a76f7df9(
    value: typing.Optional[StorageManagementPolicyRuleActionsBaseBlob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e251e02008c4321b61b1ecfd6e6b5bac4b0f4c13e106207db4e4b50ad0cd23c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa4f6c573e7c89b7978448558610a9f111833ad5cdef5de678fec49250d61b6(
    value: typing.Optional[StorageManagementPolicyRuleActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e648db8e62af2ad285e79470ab120076c11968b1b5fbfc1abb8756ffc1be7571(
    *,
    change_tier_to_archive_after_days_since_creation: typing.Optional[jsii.Number] = None,
    change_tier_to_cool_after_days_since_creation: typing.Optional[jsii.Number] = None,
    delete_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
    tier_to_archive_after_days_since_last_tier_change_greater_than: typing.Optional[jsii.Number] = None,
    tier_to_cold_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06f5759910e05d09b766724494f6150f815e2177f399da33073695e8db9c0f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b2b0cd67a5487b3e2e0699ccf710fe231491ad836086201fc49698f7b5f932(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b818d3d273aef85750d1c6b0c29888e2cd4aca3503d3dafb137ed4d70c3697b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f55ab3a288f861b3969feeb1bb64f0f625785b0fb726961162e0a86b5f6c65(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26972456ba0bd33e7d2a77769ea2b4c73dc3dcebbfd1f86c8f324671aa1531e0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9059c6ddb21d9f48c3d4175422e4974b4a400f7e4c1a55ee56a8e9ee3bb4910(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f3f718a2680c85c248a3fdcb09b3a4bcfdcfa9874b732593e14401428ade39(
    value: typing.Optional[StorageManagementPolicyRuleActionsSnapshot],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b755c1b38da43bb1cc01ce3e97e04d652cae0457e32a127facda7db59d028e(
    *,
    change_tier_to_archive_after_days_since_creation: typing.Optional[jsii.Number] = None,
    change_tier_to_cool_after_days_since_creation: typing.Optional[jsii.Number] = None,
    delete_after_days_since_creation: typing.Optional[jsii.Number] = None,
    tier_to_archive_after_days_since_last_tier_change_greater_than: typing.Optional[jsii.Number] = None,
    tier_to_cold_after_days_since_creation_greater_than: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c5e5cf498ec46ce3a78c60ab13f1e6f2c81ad491008f28c588fbd9c756303c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af3308845e022025ee2643d8550027dcdfa1b9218d05a210350c8ed0ee55113(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb8801dda3a4bb28430eb4a8f6547a667c5bd0f1b06597b89c93e35f22284779(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281aa376966cb0c048e802136b9a43c9d0af39a9766eb6d65b6bb75ae73b505c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__210d3db090008b4e5aa60bb4028ec94eaf762146c14467304ac007542dcfa44a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0842b81f077e0c0cb8fa806d2938789dc6defe4c873449cd938ae85f676becad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9962a38c0f380d433490211d2132bcdf824c51f294be3a69561999681301fb57(
    value: typing.Optional[StorageManagementPolicyRuleActionsVersion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4932dfee554c4f976587cbbf77521ac32ded59573f3fb608fe14e68f91e4bb50(
    *,
    blob_types: typing.Sequence[builtins.str],
    match_blob_index_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageManagementPolicyRuleFiltersMatchBlobIndexTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
    prefix_match: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__985b35484c6b185e898d57737378f555c705bedb52be90ea5308f96d8859b298(
    *,
    name: builtins.str,
    value: builtins.str,
    operation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3116f22faca6a73186bed67025a4c485bb4b26c46aa106fec322b883f7dfaf87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fcbb48ea3c217ad1da2fad3793547b5d7c148cb9b064009854bb24162ff0032(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b306ff862b64f33518e88b5d9f5b9247f12fe9c185488018d8da55192bcca3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5005ecbfe12f1e7f16b561ac42d43f391161760a06d3480c2b3110ddc07f9b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66615457a24dd1416a371c48244ff75960868c3b0816d778390020467e1d22fa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35500b6b6918d66459d3bbb218e49458fb73c3d83b3f2ca511f7c4645205ad9f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageManagementPolicyRuleFiltersMatchBlobIndexTag]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604035bc20b5eece0c97cb4e2279468888a257cc22f99778fa3853f79cb2697d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2b6fd76e8eaf71c1e83fef2c9f350ff860fc48b1190610ffbb23d44ff9ccb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a826d72e9f9fefe7a5b243711738ef3f1eeff58de2d69689ee852c36b05fe8ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ab05bdb14db21788db9c0f4e312c76e0066dd2d30beae1fb3852df20d5e959(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5f9d146b7d0db78fc4e3070f15f9ddb57ca34b6667e7ef78cd80dbb00eb631f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageManagementPolicyRuleFiltersMatchBlobIndexTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5a850d9e2fb3cbae0cdef729b1a08da5f72bbda06f0369ade25b31ba0aac90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69515c95ce1bb9343af5fe4b4bb950d18adae654af3751e18f7c4d6465fa2d95(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageManagementPolicyRuleFiltersMatchBlobIndexTag, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d82271dbc31d9f6cf2040113ce2ae809c84096e08e3ae8d555bd37a9be60e9e9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4311ccb2bb859ff0690cf4653c765b2a6bb714c3ae2c53924e3229575c55ee9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dfb816cf2c49adc0ac8d6eea835a96c848350def100cc9b0e8005dbcc3824be(
    value: typing.Optional[StorageManagementPolicyRuleFilters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5595508174564daee6c13cc5284056b50957a276558cb00ff054475f56cb88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4167adfd401229818ba618253e05ed6708660b4ea7e3a6aaf44387c445975cd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4766d1e0fdc4b0d01236c2b199246a45f73fa986d6aa1a6d8ad36cc9b8aed0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10766191d730e1c0baaa3ff83dbd7dcff2674a85ac12ffb4ada58926c254520d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__022b4df2b7091fabfa6d5ad758dc146a46196435fb349089b06054985fe5aa7a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318baa9645d0654db72a080535f86fcf2db2e4462b36b27d7269934b833c97b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageManagementPolicyRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87235a6ab93bf7601cc557fa602361c0756a127f7ccc7b0276c15713d3bbc5ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff58a0ddfe117c58647b575fbaa43313260ded16a90fd25339297daf0bdbfe4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa9817ac098d6171f27a4cf0877a8b8448c16a240af9196170f0d048ccf3833(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df36d77f69409c337df0a00e32bac26a8225e2c10170d2f18b5d6e2edcc22c94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageManagementPolicyRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b104ef49ddbf59696f1f6eeec528951a2989e8d7a23c9d50956b700fae4dae(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b6e72ef736b9cd583c7ed5280291f83ab4d4876eda5132b32bdf7c2e9e4d2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0525d511c122c600515c64cb65c99144ccacd20a0c7697e4450966871087cc2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ed30a6f6ff9f743addc065710b0752d06ee69195c8e1d1c931492edca7daf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9979f9c39b9b7e83468d73df575c9aff8106d6e974b5c53d90bc1259daeab9c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ea12b43dfe898842f62c94018a09dcef4f8b6882dd9a6f51dbf3afb03b8e7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990b8855cc8aa7f93e9c33c133bfc936b7476658af6a9265364a1f2ed05a9bcb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageManagementPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

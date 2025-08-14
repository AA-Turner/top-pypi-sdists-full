r'''
# `data_datadog_csm_threats_agent_rules`

Refer to the Terraform Registry for docs: [`data_datadog_csm_threats_agent_rules`](https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/data-sources/csm_threats_agent_rules).
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


class DataDatadogCsmThreatsAgentRules(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCsmThreatsAgentRules.DataDatadogCsmThreatsAgentRules",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/data-sources/csm_threats_agent_rules datadog_csm_threats_agent_rules}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        policy_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/data-sources/csm_threats_agent_rules datadog_csm_threats_agent_rules} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param policy_id: Listing only the rules in the policy with this field as the ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/data-sources/csm_threats_agent_rules#policy_id DataDatadogCsmThreatsAgentRules#policy_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80a5378c53bb769aba893ca55e93517d4041241c480e3c1a39dc34faa41c5a2a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataDatadogCsmThreatsAgentRulesConfig(
            policy_id=policy_id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataDatadogCsmThreatsAgentRules resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataDatadogCsmThreatsAgentRules to import.
        :param import_from_id: The id of the existing DataDatadogCsmThreatsAgentRules that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/data-sources/csm_threats_agent_rules#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataDatadogCsmThreatsAgentRules to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f23e00873bee1348193fce407ec1eb580b626ad776c894ab43282b3cee48b0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetPolicyId")
    def reset_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyId", []))

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
    @jsii.member(jsii_name="agentRules")
    def agent_rules(self) -> "DataDatadogCsmThreatsAgentRulesAgentRulesList":
        return typing.cast("DataDatadogCsmThreatsAgentRulesAgentRulesList", jsii.get(self, "agentRules"))

    @builtins.property
    @jsii.member(jsii_name="agentRulesIds")
    def agent_rules_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "agentRulesIds"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec8b17148a17ac6be8f6a8545d9418a28a24e8eb5ebb81e4357c5d8858105838)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.dataDatadogCsmThreatsAgentRules.DataDatadogCsmThreatsAgentRulesAgentRules",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataDatadogCsmThreatsAgentRulesAgentRules:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatadogCsmThreatsAgentRulesAgentRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.dataDatadogCsmThreatsAgentRules.DataDatadogCsmThreatsAgentRulesAgentRulesActions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataDatadogCsmThreatsAgentRulesAgentRulesActions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatadogCsmThreatsAgentRulesAgentRulesActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.dataDatadogCsmThreatsAgentRules.DataDatadogCsmThreatsAgentRulesAgentRulesActionsHash",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataDatadogCsmThreatsAgentRulesAgentRulesActionsHash:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatadogCsmThreatsAgentRulesAgentRulesActionsHash(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatadogCsmThreatsAgentRulesAgentRulesActionsHashOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCsmThreatsAgentRules.DataDatadogCsmThreatsAgentRulesAgentRulesActionsHashOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5bdce4a694d0dbf504c0b6724b99b5f580bccc7ea73bdd673e4b8a0ff69e1ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataDatadogCsmThreatsAgentRulesAgentRulesActionsHash]:
        return typing.cast(typing.Optional[DataDatadogCsmThreatsAgentRulesAgentRulesActionsHash], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataDatadogCsmThreatsAgentRulesAgentRulesActionsHash],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69214056596ea07cbcac4d963fa2b1b15943c2587a39297dd22e169451784875)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatadogCsmThreatsAgentRulesAgentRulesActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCsmThreatsAgentRules.DataDatadogCsmThreatsAgentRulesAgentRulesActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c447c8beefa4cb268fcf571700bebeb605e98721d01dca9e7ab58605bdbb4d45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataDatadogCsmThreatsAgentRulesAgentRulesActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bac5fbc3d49e342947395194044df94a6b9955d04d27bce277059daacc3db96)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataDatadogCsmThreatsAgentRulesAgentRulesActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab8c5f833a58ef1f443713f90f5b31d8a89b97a6bf99fe3ddd4a7fdc94cfb9df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8047bcb8c0000558efea844edca0307534879c71716d23cdadcf531e3c5ca153)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bebf7c8f50be6e3e4a2ad905ec5891f963f8de6fd1144832d6582f9fabc85254)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataDatadogCsmThreatsAgentRulesAgentRulesActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCsmThreatsAgentRules.DataDatadogCsmThreatsAgentRulesAgentRulesActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__610b387f4dabb3b4f230332c613f0eda8454c683267d09587c12e885cce2a8e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hash")
    def hash(
        self,
    ) -> DataDatadogCsmThreatsAgentRulesAgentRulesActionsHashOutputReference:
        return typing.cast(DataDatadogCsmThreatsAgentRulesAgentRulesActionsHashOutputReference, jsii.get(self, "hash"))

    @builtins.property
    @jsii.member(jsii_name="set")
    def set(
        self,
    ) -> "DataDatadogCsmThreatsAgentRulesAgentRulesActionsSetOutputReference":
        return typing.cast("DataDatadogCsmThreatsAgentRulesAgentRulesActionsSetOutputReference", jsii.get(self, "set"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataDatadogCsmThreatsAgentRulesAgentRulesActions]:
        return typing.cast(typing.Optional[DataDatadogCsmThreatsAgentRulesAgentRulesActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataDatadogCsmThreatsAgentRulesAgentRulesActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__148e0bb4eceb6aa81aa3d1987a65bd4a85e7f9ddcb7a1058398e5d5944514c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.dataDatadogCsmThreatsAgentRules.DataDatadogCsmThreatsAgentRulesAgentRulesActionsSet",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataDatadogCsmThreatsAgentRulesAgentRulesActionsSet:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatadogCsmThreatsAgentRulesAgentRulesActionsSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatadogCsmThreatsAgentRulesAgentRulesActionsSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCsmThreatsAgentRules.DataDatadogCsmThreatsAgentRulesAgentRulesActionsSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c2db9c3a040e38f009c655c728ab890b8fc81c90a82c0789763070a571ae1c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="append")
    def append(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "append"))

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "field"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ttl"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataDatadogCsmThreatsAgentRulesAgentRulesActionsSet]:
        return typing.cast(typing.Optional[DataDatadogCsmThreatsAgentRulesAgentRulesActionsSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataDatadogCsmThreatsAgentRulesAgentRulesActionsSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88624dc5deef175719e359612814f1e5644101932c5e80d02bffd2a95de52336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatadogCsmThreatsAgentRulesAgentRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCsmThreatsAgentRules.DataDatadogCsmThreatsAgentRulesAgentRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__169751bfa0ada31e7c83f8f538c78a673d57cead8f26be7f942c15f408954058)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataDatadogCsmThreatsAgentRulesAgentRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ea3c2e36803cff1a541c0d4b4726fd3633baf77a8171b09aaac12ffb0f861b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataDatadogCsmThreatsAgentRulesAgentRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__556f14f5ce8e06a9a99b1f8a55a09b4df0f3ba25188d45a7f60f59f5a237752d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a04eca2440890672cafb47a1ba4781bdb1f31cc851a7527a300c2eb17e0ac0f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b06b5feff4c864dea03a9ae37cc31d4e4bfd1e44a817d16d5b360a4511c787fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataDatadogCsmThreatsAgentRulesAgentRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCsmThreatsAgentRules.DataDatadogCsmThreatsAgentRulesAgentRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7c43cf730fd6d0603b553f8ebe2711e06a831f09a565c984ed4e798a1cd331d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> DataDatadogCsmThreatsAgentRulesAgentRulesActionsList:
        return typing.cast(DataDatadogCsmThreatsAgentRulesAgentRulesActionsList, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="productTags")
    def product_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "productTags"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataDatadogCsmThreatsAgentRulesAgentRules]:
        return typing.cast(typing.Optional[DataDatadogCsmThreatsAgentRulesAgentRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataDatadogCsmThreatsAgentRulesAgentRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dfe9af427054c1f32a13af8b9078d0de2ac5f81078c0af369eb3bec9cdc7480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.dataDatadogCsmThreatsAgentRules.DataDatadogCsmThreatsAgentRulesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "policy_id": "policyId",
    },
)
class DataDatadogCsmThreatsAgentRulesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        policy_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param policy_id: Listing only the rules in the policy with this field as the ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/data-sources/csm_threats_agent_rules#policy_id DataDatadogCsmThreatsAgentRules#policy_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b234486b7f8a26370588821e9672e9ada091a7a5599dd0c1803d37b97485bbd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
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
        if policy_id is not None:
            self._values["policy_id"] = policy_id

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
    def policy_id(self) -> typing.Optional[builtins.str]:
        '''Listing only the rules in the policy with this field as the ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/data-sources/csm_threats_agent_rules#policy_id DataDatadogCsmThreatsAgentRules#policy_id}
        '''
        result = self._values.get("policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatadogCsmThreatsAgentRulesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataDatadogCsmThreatsAgentRules",
    "DataDatadogCsmThreatsAgentRulesAgentRules",
    "DataDatadogCsmThreatsAgentRulesAgentRulesActions",
    "DataDatadogCsmThreatsAgentRulesAgentRulesActionsHash",
    "DataDatadogCsmThreatsAgentRulesAgentRulesActionsHashOutputReference",
    "DataDatadogCsmThreatsAgentRulesAgentRulesActionsList",
    "DataDatadogCsmThreatsAgentRulesAgentRulesActionsOutputReference",
    "DataDatadogCsmThreatsAgentRulesAgentRulesActionsSet",
    "DataDatadogCsmThreatsAgentRulesAgentRulesActionsSetOutputReference",
    "DataDatadogCsmThreatsAgentRulesAgentRulesList",
    "DataDatadogCsmThreatsAgentRulesAgentRulesOutputReference",
    "DataDatadogCsmThreatsAgentRulesConfig",
]

publication.publish()

def _typecheckingstub__80a5378c53bb769aba893ca55e93517d4041241c480e3c1a39dc34faa41c5a2a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    policy_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__36f23e00873bee1348193fce407ec1eb580b626ad776c894ab43282b3cee48b0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec8b17148a17ac6be8f6a8545d9418a28a24e8eb5ebb81e4357c5d8858105838(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5bdce4a694d0dbf504c0b6724b99b5f580bccc7ea73bdd673e4b8a0ff69e1ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69214056596ea07cbcac4d963fa2b1b15943c2587a39297dd22e169451784875(
    value: typing.Optional[DataDatadogCsmThreatsAgentRulesAgentRulesActionsHash],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c447c8beefa4cb268fcf571700bebeb605e98721d01dca9e7ab58605bdbb4d45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bac5fbc3d49e342947395194044df94a6b9955d04d27bce277059daacc3db96(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8c5f833a58ef1f443713f90f5b31d8a89b97a6bf99fe3ddd4a7fdc94cfb9df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8047bcb8c0000558efea844edca0307534879c71716d23cdadcf531e3c5ca153(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bebf7c8f50be6e3e4a2ad905ec5891f963f8de6fd1144832d6582f9fabc85254(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610b387f4dabb3b4f230332c613f0eda8454c683267d09587c12e885cce2a8e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148e0bb4eceb6aa81aa3d1987a65bd4a85e7f9ddcb7a1058398e5d5944514c9f(
    value: typing.Optional[DataDatadogCsmThreatsAgentRulesAgentRulesActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2db9c3a040e38f009c655c728ab890b8fc81c90a82c0789763070a571ae1c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88624dc5deef175719e359612814f1e5644101932c5e80d02bffd2a95de52336(
    value: typing.Optional[DataDatadogCsmThreatsAgentRulesAgentRulesActionsSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__169751bfa0ada31e7c83f8f538c78a673d57cead8f26be7f942c15f408954058(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ea3c2e36803cff1a541c0d4b4726fd3633baf77a8171b09aaac12ffb0f861b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556f14f5ce8e06a9a99b1f8a55a09b4df0f3ba25188d45a7f60f59f5a237752d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a04eca2440890672cafb47a1ba4781bdb1f31cc851a7527a300c2eb17e0ac0f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b06b5feff4c864dea03a9ae37cc31d4e4bfd1e44a817d16d5b360a4511c787fa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7c43cf730fd6d0603b553f8ebe2711e06a831f09a565c984ed4e798a1cd331d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dfe9af427054c1f32a13af8b9078d0de2ac5f81078c0af369eb3bec9cdc7480(
    value: typing.Optional[DataDatadogCsmThreatsAgentRulesAgentRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b234486b7f8a26370588821e9672e9ada091a7a5599dd0c1803d37b97485bbd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    policy_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

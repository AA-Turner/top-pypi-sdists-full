r'''
# `google_compute_firewall_policy_with_rules`

Refer to the Terraform Registry for docs: [`google_compute_firewall_policy_with_rules`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules).
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


class ComputeFirewallPolicyWithRules(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRules",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules google_compute_firewall_policy_with_rules}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        parent: builtins.str,
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeFirewallPolicyWithRulesRule", typing.Dict[builtins.str, typing.Any]]]],
        short_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeFirewallPolicyWithRulesTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules google_compute_firewall_policy_with_rules} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param parent: The parent of this FirewallPolicy in the Cloud Resource Hierarchy. Format: organizations/{organization_id} or folders/{folder_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#parent ComputeFirewallPolicyWithRules#parent}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#rule ComputeFirewallPolicyWithRules#rule}
        :param short_name: A textual name of the security policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#short_name ComputeFirewallPolicyWithRules#short_name}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#description ComputeFirewallPolicyWithRules#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#id ComputeFirewallPolicyWithRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#timeouts ComputeFirewallPolicyWithRules#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c57eadbc5dabdff07cea5ec6d41995950b61a55b148075f4b4fc2240f43f90dd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeFirewallPolicyWithRulesConfig(
            parent=parent,
            rule=rule,
            short_name=short_name,
            description=description,
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
        '''Generates CDKTF code for importing a ComputeFirewallPolicyWithRules resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeFirewallPolicyWithRules to import.
        :param import_from_id: The id of the existing ComputeFirewallPolicyWithRules that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeFirewallPolicyWithRules to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b52c0899e18617f394e74b17a6c84f561b5a3698ae17e92ae236459f359b399b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeFirewallPolicyWithRulesRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__121ed78fb1b0a21270c079f1e8c5446206acc572b26c22f80126598b845f45df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#create ComputeFirewallPolicyWithRules#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#delete ComputeFirewallPolicyWithRules#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#update ComputeFirewallPolicyWithRules#update}.
        '''
        value = ComputeFirewallPolicyWithRulesTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

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
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="fingerprint")
    def fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fingerprint"))

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @builtins.property
    @jsii.member(jsii_name="predefinedRules")
    def predefined_rules(self) -> "ComputeFirewallPolicyWithRulesPredefinedRulesList":
        return typing.cast("ComputeFirewallPolicyWithRulesPredefinedRulesList", jsii.get(self, "predefinedRules"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "ComputeFirewallPolicyWithRulesRuleList":
        return typing.cast("ComputeFirewallPolicyWithRulesRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="ruleTupleCount")
    def rule_tuple_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ruleTupleCount"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="selfLinkWithId")
    def self_link_with_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLinkWithId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeFirewallPolicyWithRulesTimeoutsOutputReference":
        return typing.cast("ComputeFirewallPolicyWithRulesTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyWithRulesRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyWithRulesRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="shortNameInput")
    def short_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shortNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeFirewallPolicyWithRulesTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeFirewallPolicyWithRulesTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2cf45d93edd8933831121bbaef7df185c37db9509e4f44ce54b6e3dcfa6af1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61ecc6faad7e432fc793fb1e53948725f1091c41dd58a721077c0969b5642915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa77c342e863ee78cfebe81f34c60a158e101b71271ef2d577b3fbb5e1b8d01f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shortName")
    def short_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shortName"))

    @short_name.setter
    def short_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd0ce4d9db428c9d09ab06416c852b2c852c8fae6ece650c2563829d8ee9d933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shortName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "parent": "parent",
        "rule": "rule",
        "short_name": "shortName",
        "description": "description",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class ComputeFirewallPolicyWithRulesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        parent: builtins.str,
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeFirewallPolicyWithRulesRule", typing.Dict[builtins.str, typing.Any]]]],
        short_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeFirewallPolicyWithRulesTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param parent: The parent of this FirewallPolicy in the Cloud Resource Hierarchy. Format: organizations/{organization_id} or folders/{folder_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#parent ComputeFirewallPolicyWithRules#parent}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#rule ComputeFirewallPolicyWithRules#rule}
        :param short_name: A textual name of the security policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#short_name ComputeFirewallPolicyWithRules#short_name}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#description ComputeFirewallPolicyWithRules#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#id ComputeFirewallPolicyWithRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#timeouts ComputeFirewallPolicyWithRules#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ComputeFirewallPolicyWithRulesTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0fa84cd4378edd2f5558126cf0e721ac2d660f770a327845fdb0dc1b71f47bf)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument short_name", value=short_name, expected_type=type_hints["short_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parent": parent,
            "rule": rule,
            "short_name": short_name,
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
        if description is not None:
            self._values["description"] = description
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
    def parent(self) -> builtins.str:
        '''The parent of this FirewallPolicy in the Cloud Resource Hierarchy. Format: organizations/{organization_id} or folders/{folder_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#parent ComputeFirewallPolicyWithRules#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyWithRulesRule"]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#rule ComputeFirewallPolicyWithRules#rule}
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyWithRulesRule"]], result)

    @builtins.property
    def short_name(self) -> builtins.str:
        '''A textual name of the security policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#short_name ComputeFirewallPolicyWithRules#short_name}
        '''
        result = self._values.get("short_name")
        assert result is not None, "Required property 'short_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#description ComputeFirewallPolicyWithRules#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#id ComputeFirewallPolicyWithRules#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeFirewallPolicyWithRulesTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#timeouts ComputeFirewallPolicyWithRules#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeFirewallPolicyWithRulesTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyWithRulesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesPredefinedRules",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeFirewallPolicyWithRulesPredefinedRules:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyWithRulesPredefinedRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeFirewallPolicyWithRulesPredefinedRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesPredefinedRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a13949702a7ef613d679c3bc77238e512589ac1905b3d5b9db8418de6863c431)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeFirewallPolicyWithRulesPredefinedRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a120dc72b7ec73bad02f31d1fbb3ac54438fc147c6d883cce804a799d3058c9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeFirewallPolicyWithRulesPredefinedRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27071a2928ffc50b13110b30adeb75e14e11a61dbc5b5611d45092a34bd51190)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09bb2c594d629cbfba118242f6992a580a96a6f2dfb4cab5599054e6e53de17d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a723ab61cfa125ebc3b5f8ba357afc1ada37c8e6a54cee1e83c1adaf4f1f9021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesPredefinedRulesMatch",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeFirewallPolicyWithRulesPredefinedRulesMatch:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyWithRulesPredefinedRulesMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4Config",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4Config:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4a9d55dd190f2a4ed3e12618cf24893394f551c58aca07da67ba5caab2f602c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec287ea870d720b22b774e1c90020e867b1fc445d84b2604255b1ab3aa258c9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a113d26c181adb0ba2cdfda643309a6359ac11fddf786c6d69ceef6352cc7b0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3db47c0a31bc5e517feab50e77ae4ef3e254f939bcefc7e6f21f50b2cdfb0bff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c96ae5069e3ea275e5954b6ed5323d3765cbee8f9b0a1fa66f08335f2ead6168)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3da16b4977871d59686bea100e4ec55bac56103504bf798da8133b0a15a3f1fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ports"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4Config]:
        return typing.cast(typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4Config], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4Config],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00953c81932025f0e18053d28a9c90e009b009a9c4c68d34c4a92c86da81911c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeFirewallPolicyWithRulesPredefinedRulesMatchList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesPredefinedRulesMatchList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e6844d13d3bf10fd81c4ee772e0a0abaaad9f0089e68307fd7fa4ab5f557893)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeFirewallPolicyWithRulesPredefinedRulesMatchOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d992b99415f6d161d48258f7155c86cda783f53cf565247a7d1e247ee876ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeFirewallPolicyWithRulesPredefinedRulesMatchOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f35d9d0884189c5772bc37dbc84322f6b8b386007d44c210c3a30ee26b43d814)
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
            type_hints = typing.get_type_hints(_typecheckingstub__364faa8364bcf9181326dd8d04fa9d3364074d055cfff9edefb153e60a0ceb16)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5ab8bdb457bd7b8fbf5835f5cd86da147bcc063d40a38e59b23604336e0a40f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeFirewallPolicyWithRulesPredefinedRulesMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesPredefinedRulesMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ff8207c21f851234d3669acdf9a83188df5dd4031f34443e5228c091e655e79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="destAddressGroups")
    def dest_address_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destAddressGroups"))

    @builtins.property
    @jsii.member(jsii_name="destFqdns")
    def dest_fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destFqdns"))

    @builtins.property
    @jsii.member(jsii_name="destIpRanges")
    def dest_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destIpRanges"))

    @builtins.property
    @jsii.member(jsii_name="destRegionCodes")
    def dest_region_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destRegionCodes"))

    @builtins.property
    @jsii.member(jsii_name="destThreatIntelligences")
    def dest_threat_intelligences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destThreatIntelligences"))

    @builtins.property
    @jsii.member(jsii_name="layer4Config")
    def layer4_config(
        self,
    ) -> ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigList:
        return typing.cast(ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigList, jsii.get(self, "layer4Config"))

    @builtins.property
    @jsii.member(jsii_name="srcAddressGroups")
    def src_address_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcAddressGroups"))

    @builtins.property
    @jsii.member(jsii_name="srcFqdns")
    def src_fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcFqdns"))

    @builtins.property
    @jsii.member(jsii_name="srcIpRanges")
    def src_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcIpRanges"))

    @builtins.property
    @jsii.member(jsii_name="srcRegionCodes")
    def src_region_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcRegionCodes"))

    @builtins.property
    @jsii.member(jsii_name="srcSecureTag")
    def src_secure_tag(
        self,
    ) -> "ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagList":
        return typing.cast("ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagList", jsii.get(self, "srcSecureTag"))

    @builtins.property
    @jsii.member(jsii_name="srcThreatIntelligences")
    def src_threat_intelligences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcThreatIntelligences"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRulesMatch]:
        return typing.cast(typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRulesMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRulesMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c59c227c9b14b5761f733a632cd39652dd144e9cd7ed0b3c705c81e7e48cf172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTag",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTag:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea562b20df90e6806addda56d751b5feb58d277508133142db5ba3aa6a1dc99d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f501a3c6953a2604b61034c785af7de28be331176883c6bd2eccda3859f4be82)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3370e999972505917f090bb4befcee3a6c9bcc7504f19680f6d690be642c5a90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c419f284dce17cfb626a200cb063b6bc123d8e9df25dead4e690298e127080b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcd223ffd02ecc096fa650cbe102bd7e02357b91c5abe042e54db8ce7b4ac2b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34b17abcd686f6cd6746990fec4cb4d3ee217379171b2676cfb641181fb47afe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTag]:
        return typing.cast(typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTag], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTag],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__544ec24469e7c097bbc4138613912949388e24ebe91fb2c9848f2e3400ff99e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeFirewallPolicyWithRulesPredefinedRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesPredefinedRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__399d404dc834215bf94346fdceaec664b2ad7ac334270bc1853928bab5e80484)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "disabled"))

    @builtins.property
    @jsii.member(jsii_name="enableLogging")
    def enable_logging(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enableLogging"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> ComputeFirewallPolicyWithRulesPredefinedRulesMatchList:
        return typing.cast(ComputeFirewallPolicyWithRulesPredefinedRulesMatchList, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @builtins.property
    @jsii.member(jsii_name="securityProfileGroup")
    def security_profile_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityProfileGroup"))

    @builtins.property
    @jsii.member(jsii_name="targetResources")
    def target_resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetResources"))

    @builtins.property
    @jsii.member(jsii_name="targetSecureTag")
    def target_secure_tag(
        self,
    ) -> "ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTagList":
        return typing.cast("ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTagList", jsii.get(self, "targetSecureTag"))

    @builtins.property
    @jsii.member(jsii_name="targetServiceAccounts")
    def target_service_accounts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetServiceAccounts"))

    @builtins.property
    @jsii.member(jsii_name="tlsInspect")
    def tls_inspect(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "tlsInspect"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRules]:
        return typing.cast(typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1d1bb0539c40dd3968ee477934c2f749d23b8f918c8398ae6b547bb1df234c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTag",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTag:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b7aceb9cbdbeffd5642f7a5fddaafea224da2fecbe9292bbae542ab78ebc07b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f4f0a1f5bdcbd6f560048daea6b8701aa9d4e310367e8ebef01bb5d22513816)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2af953ca453197ef8324a850667819a87b432d13826473c333d5fb4678e2dce9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1ac0de5fb8ff87dbb21fca7acc56e3270741de712aeb79db6fb743a1cb71d42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61e9d52cd0e2259382a253a36e69573f0d5d034bc1587b3b6d3fb09a33905527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a29c25e47537bdf16f06c60515f3f2ee0b1c5eabebee9a91b6e058fdb991028)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTag]:
        return typing.cast(typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTag], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTag],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46c3296c52e8a72a8fa939baa946ed3b6a5765c4f806f95380e23653aa09357)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesRule",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "match": "match",
        "priority": "priority",
        "description": "description",
        "direction": "direction",
        "disabled": "disabled",
        "enable_logging": "enableLogging",
        "rule_name": "ruleName",
        "security_profile_group": "securityProfileGroup",
        "target_resources": "targetResources",
        "target_secure_tag": "targetSecureTag",
        "target_service_accounts": "targetServiceAccounts",
        "tls_inspect": "tlsInspect",
    },
)
class ComputeFirewallPolicyWithRulesRule:
    def __init__(
        self,
        *,
        action: builtins.str,
        match: typing.Union["ComputeFirewallPolicyWithRulesRuleMatch", typing.Dict[builtins.str, typing.Any]],
        priority: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        direction: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        security_profile_group: typing.Optional[builtins.str] = None,
        target_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_secure_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeFirewallPolicyWithRulesRuleTargetSecureTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        tls_inspect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param action: The Action to perform when the client connection triggers the rule. Can currently be either "allow", "deny", "apply_security_profile_group" or "goto_next". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#action ComputeFirewallPolicyWithRules#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#match ComputeFirewallPolicyWithRules#match}
        :param priority: An integer indicating the priority of a rule in the list. The priority must be a value between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest priority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#priority ComputeFirewallPolicyWithRules#priority}
        :param description: A description of the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#description ComputeFirewallPolicyWithRules#description}
        :param direction: The direction in which this rule applies. If unspecified an INGRESS rule is created. Possible values: ["INGRESS", "EGRESS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#direction ComputeFirewallPolicyWithRules#direction}
        :param disabled: Denotes whether the firewall policy rule is disabled. When set to true, the firewall policy rule is not enforced and traffic behaves as if it did not exist. If this is unspecified, the firewall policy rule will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#disabled ComputeFirewallPolicyWithRules#disabled}
        :param enable_logging: Denotes whether to enable logging for a particular rule. If logging is enabled, logs will be exported to the configured export destination in Stackdriver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#enable_logging ComputeFirewallPolicyWithRules#enable_logging}
        :param rule_name: An optional name for the rule. This field is not a unique identifier and can be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#rule_name ComputeFirewallPolicyWithRules#rule_name}
        :param security_profile_group: A fully-qualified URL of a SecurityProfile resource instance. Example: https://networksecurity.googleapis.com/v1/projects/{project}/locations/{location}/securityProfileGroups/my-security-profile-group Must be specified if action is 'apply_security_profile_group'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#security_profile_group ComputeFirewallPolicyWithRules#security_profile_group}
        :param target_resources: A list of network resource URLs to which this rule applies. This field allows you to control which network's VMs get this rule. If this field is left blank, all VMs within the organization will receive the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#target_resources ComputeFirewallPolicyWithRules#target_resources}
        :param target_secure_tag: target_secure_tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#target_secure_tag ComputeFirewallPolicyWithRules#target_secure_tag}
        :param target_service_accounts: A list of service accounts indicating the sets of instances that are applied with this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#target_service_accounts ComputeFirewallPolicyWithRules#target_service_accounts}
        :param tls_inspect: Boolean flag indicating if the traffic should be TLS decrypted. It can be set only if action = 'apply_security_profile_group' and cannot be set for other actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#tls_inspect ComputeFirewallPolicyWithRules#tls_inspect}
        '''
        if isinstance(match, dict):
            match = ComputeFirewallPolicyWithRulesRuleMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa6ea40db83bec1754a22af5eba10d053060b5c5029d7020714ef787ba152d5c)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument security_profile_group", value=security_profile_group, expected_type=type_hints["security_profile_group"])
            check_type(argname="argument target_resources", value=target_resources, expected_type=type_hints["target_resources"])
            check_type(argname="argument target_secure_tag", value=target_secure_tag, expected_type=type_hints["target_secure_tag"])
            check_type(argname="argument target_service_accounts", value=target_service_accounts, expected_type=type_hints["target_service_accounts"])
            check_type(argname="argument tls_inspect", value=tls_inspect, expected_type=type_hints["tls_inspect"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "match": match,
            "priority": priority,
        }
        if description is not None:
            self._values["description"] = description
        if direction is not None:
            self._values["direction"] = direction
        if disabled is not None:
            self._values["disabled"] = disabled
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if security_profile_group is not None:
            self._values["security_profile_group"] = security_profile_group
        if target_resources is not None:
            self._values["target_resources"] = target_resources
        if target_secure_tag is not None:
            self._values["target_secure_tag"] = target_secure_tag
        if target_service_accounts is not None:
            self._values["target_service_accounts"] = target_service_accounts
        if tls_inspect is not None:
            self._values["tls_inspect"] = tls_inspect

    @builtins.property
    def action(self) -> builtins.str:
        '''The Action to perform when the client connection triggers the rule. Can currently be either "allow", "deny", "apply_security_profile_group" or "goto_next".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#action ComputeFirewallPolicyWithRules#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match(self) -> "ComputeFirewallPolicyWithRulesRuleMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#match ComputeFirewallPolicyWithRules#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("ComputeFirewallPolicyWithRulesRuleMatch", result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''An integer indicating the priority of a rule in the list.

        The priority must be a value
        between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the
        highest priority and 2147483647 is the lowest priority.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#priority ComputeFirewallPolicyWithRules#priority}
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#description ComputeFirewallPolicyWithRules#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def direction(self) -> typing.Optional[builtins.str]:
        '''The direction in which this rule applies. If unspecified an INGRESS rule is created. Possible values: ["INGRESS", "EGRESS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#direction ComputeFirewallPolicyWithRules#direction}
        '''
        result = self._values.get("direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Denotes whether the firewall policy rule is disabled.

        When set to true,
        the firewall policy rule is not enforced and traffic behaves as if it did
        not exist. If this is unspecified, the firewall policy rule will be
        enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#disabled ComputeFirewallPolicyWithRules#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Denotes whether to enable logging for a particular rule.

        If logging is enabled, logs will be exported to the
        configured export destination in Stackdriver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#enable_logging ComputeFirewallPolicyWithRules#enable_logging}
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the rule. This field is not a unique identifier and can be updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#rule_name ComputeFirewallPolicyWithRules#rule_name}
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_profile_group(self) -> typing.Optional[builtins.str]:
        '''A fully-qualified URL of a SecurityProfile resource instance. Example: https://networksecurity.googleapis.com/v1/projects/{project}/locations/{location}/securityProfileGroups/my-security-profile-group Must be specified if action is 'apply_security_profile_group'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#security_profile_group ComputeFirewallPolicyWithRules#security_profile_group}
        '''
        result = self._values.get("security_profile_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of network resource URLs to which this rule applies.

        This field allows you to control which network's VMs get
        this rule. If this field is left blank, all VMs
        within the organization will receive the rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#target_resources ComputeFirewallPolicyWithRules#target_resources}
        '''
        result = self._values.get("target_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_secure_tag(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyWithRulesRuleTargetSecureTag"]]]:
        '''target_secure_tag block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#target_secure_tag ComputeFirewallPolicyWithRules#target_secure_tag}
        '''
        result = self._values.get("target_secure_tag")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyWithRulesRuleTargetSecureTag"]]], result)

    @builtins.property
    def target_service_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of service accounts indicating the sets of instances that are applied with this rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#target_service_accounts ComputeFirewallPolicyWithRules#target_service_accounts}
        '''
        result = self._values.get("target_service_accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tls_inspect(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean flag indicating if the traffic should be TLS decrypted.

        It can be set only if action = 'apply_security_profile_group' and cannot be set for other actions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#tls_inspect ComputeFirewallPolicyWithRules#tls_inspect}
        '''
        result = self._values.get("tls_inspect")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyWithRulesRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeFirewallPolicyWithRulesRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae5e0da7e64b90f079d25dc405556647cceb8a85772b70e8156a9941424fb486)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeFirewallPolicyWithRulesRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758e4ccbd368b00d52a396ecb24bc416f847b616dba92f49c15169606931a501)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeFirewallPolicyWithRulesRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56c47b191b5170123c05eff150c082d6b7e26433e56b34a5569954365d102e52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__034204c7d7f632044a1990f89d7c41b322d935506a6aea486f8046a8ee98a880)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7deb573164d1fc15a782359f5651b1d4ea42bf75f3d9cd5bed22840259590579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a315c654a70e5cc835ab927924c8b8bdd951913083435e90d6273cc29343d058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesRuleMatch",
    jsii_struct_bases=[],
    name_mapping={
        "layer4_config": "layer4Config",
        "dest_address_groups": "destAddressGroups",
        "dest_fqdns": "destFqdns",
        "dest_ip_ranges": "destIpRanges",
        "dest_region_codes": "destRegionCodes",
        "dest_threat_intelligences": "destThreatIntelligences",
        "src_address_groups": "srcAddressGroups",
        "src_fqdns": "srcFqdns",
        "src_ip_ranges": "srcIpRanges",
        "src_region_codes": "srcRegionCodes",
        "src_secure_tag": "srcSecureTag",
        "src_threat_intelligences": "srcThreatIntelligences",
    },
)
class ComputeFirewallPolicyWithRulesRuleMatch:
    def __init__(
        self,
        *,
        layer4_config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeFirewallPolicyWithRulesRuleMatchLayer4Config", typing.Dict[builtins.str, typing.Any]]]],
        dest_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_secure_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
        src_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param layer4_config: layer4_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#layer4_config ComputeFirewallPolicyWithRules#layer4_config}
        :param dest_address_groups: Address groups which should be matched against the traffic destination. Maximum number of destination address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#dest_address_groups ComputeFirewallPolicyWithRules#dest_address_groups}
        :param dest_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic destination. Maximum number of destination fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#dest_fqdns ComputeFirewallPolicyWithRules#dest_fqdns}
        :param dest_ip_ranges: Destination IP address range in CIDR format. Required for EGRESS rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#dest_ip_ranges ComputeFirewallPolicyWithRules#dest_ip_ranges}
        :param dest_region_codes: Region codes whose IP addresses will be used to match for destination of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of destination region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#dest_region_codes ComputeFirewallPolicyWithRules#dest_region_codes}
        :param dest_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#dest_threat_intelligences ComputeFirewallPolicyWithRules#dest_threat_intelligences}
        :param src_address_groups: Address groups which should be matched against the traffic source. Maximum number of source address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_address_groups ComputeFirewallPolicyWithRules#src_address_groups}
        :param src_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic source. Maximum number of source fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_fqdns ComputeFirewallPolicyWithRules#src_fqdns}
        :param src_ip_ranges: Source IP address range in CIDR format. Required for INGRESS rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_ip_ranges ComputeFirewallPolicyWithRules#src_ip_ranges}
        :param src_region_codes: Region codes whose IP addresses will be used to match for source of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of source region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_region_codes ComputeFirewallPolicyWithRules#src_region_codes}
        :param src_secure_tag: src_secure_tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_secure_tag ComputeFirewallPolicyWithRules#src_secure_tag}
        :param src_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_threat_intelligences ComputeFirewallPolicyWithRules#src_threat_intelligences}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fce2d9ecdcf34bb12ab69cd460714e7dc7254801a8ccb969908bf416a1b26027)
            check_type(argname="argument layer4_config", value=layer4_config, expected_type=type_hints["layer4_config"])
            check_type(argname="argument dest_address_groups", value=dest_address_groups, expected_type=type_hints["dest_address_groups"])
            check_type(argname="argument dest_fqdns", value=dest_fqdns, expected_type=type_hints["dest_fqdns"])
            check_type(argname="argument dest_ip_ranges", value=dest_ip_ranges, expected_type=type_hints["dest_ip_ranges"])
            check_type(argname="argument dest_region_codes", value=dest_region_codes, expected_type=type_hints["dest_region_codes"])
            check_type(argname="argument dest_threat_intelligences", value=dest_threat_intelligences, expected_type=type_hints["dest_threat_intelligences"])
            check_type(argname="argument src_address_groups", value=src_address_groups, expected_type=type_hints["src_address_groups"])
            check_type(argname="argument src_fqdns", value=src_fqdns, expected_type=type_hints["src_fqdns"])
            check_type(argname="argument src_ip_ranges", value=src_ip_ranges, expected_type=type_hints["src_ip_ranges"])
            check_type(argname="argument src_region_codes", value=src_region_codes, expected_type=type_hints["src_region_codes"])
            check_type(argname="argument src_secure_tag", value=src_secure_tag, expected_type=type_hints["src_secure_tag"])
            check_type(argname="argument src_threat_intelligences", value=src_threat_intelligences, expected_type=type_hints["src_threat_intelligences"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "layer4_config": layer4_config,
        }
        if dest_address_groups is not None:
            self._values["dest_address_groups"] = dest_address_groups
        if dest_fqdns is not None:
            self._values["dest_fqdns"] = dest_fqdns
        if dest_ip_ranges is not None:
            self._values["dest_ip_ranges"] = dest_ip_ranges
        if dest_region_codes is not None:
            self._values["dest_region_codes"] = dest_region_codes
        if dest_threat_intelligences is not None:
            self._values["dest_threat_intelligences"] = dest_threat_intelligences
        if src_address_groups is not None:
            self._values["src_address_groups"] = src_address_groups
        if src_fqdns is not None:
            self._values["src_fqdns"] = src_fqdns
        if src_ip_ranges is not None:
            self._values["src_ip_ranges"] = src_ip_ranges
        if src_region_codes is not None:
            self._values["src_region_codes"] = src_region_codes
        if src_secure_tag is not None:
            self._values["src_secure_tag"] = src_secure_tag
        if src_threat_intelligences is not None:
            self._values["src_threat_intelligences"] = src_threat_intelligences

    @builtins.property
    def layer4_config(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyWithRulesRuleMatchLayer4Config"]]:
        '''layer4_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#layer4_config ComputeFirewallPolicyWithRules#layer4_config}
        '''
        result = self._values.get("layer4_config")
        assert result is not None, "Required property 'layer4_config' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyWithRulesRuleMatchLayer4Config"]], result)

    @builtins.property
    def dest_address_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Address groups which should be matched against the traffic destination. Maximum number of destination address groups is 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#dest_address_groups ComputeFirewallPolicyWithRules#dest_address_groups}
        '''
        result = self._values.get("dest_address_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_fqdns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Fully Qualified Domain Name (FQDN) which should be matched against traffic destination. Maximum number of destination fqdn allowed is 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#dest_fqdns ComputeFirewallPolicyWithRules#dest_fqdns}
        '''
        result = self._values.get("dest_fqdns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Destination IP address range in CIDR format. Required for EGRESS rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#dest_ip_ranges ComputeFirewallPolicyWithRules#dest_ip_ranges}
        '''
        result = self._values.get("dest_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_region_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Region codes whose IP addresses will be used to match for destination of traffic.

        Should be specified as 2 letter country code defined as per
        ISO 3166 alpha-2 country codes. ex."US"
        Maximum number of destination region codes allowed is 5000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#dest_region_codes ComputeFirewallPolicyWithRules#dest_region_codes}
        '''
        result = self._values.get("dest_region_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_threat_intelligences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic destination.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#dest_threat_intelligences ComputeFirewallPolicyWithRules#dest_threat_intelligences}
        '''
        result = self._values.get("dest_threat_intelligences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_address_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Address groups which should be matched against the traffic source. Maximum number of source address groups is 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_address_groups ComputeFirewallPolicyWithRules#src_address_groups}
        '''
        result = self._values.get("src_address_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_fqdns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Fully Qualified Domain Name (FQDN) which should be matched against traffic source. Maximum number of source fqdn allowed is 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_fqdns ComputeFirewallPolicyWithRules#src_fqdns}
        '''
        result = self._values.get("src_fqdns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Source IP address range in CIDR format. Required for INGRESS rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_ip_ranges ComputeFirewallPolicyWithRules#src_ip_ranges}
        '''
        result = self._values.get("src_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_region_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Region codes whose IP addresses will be used to match for source of traffic.

        Should be specified as 2 letter country code defined as per
        ISO 3166 alpha-2 country codes. ex."US"
        Maximum number of source region codes allowed is 5000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_region_codes ComputeFirewallPolicyWithRules#src_region_codes}
        '''
        result = self._values.get("src_region_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_secure_tag(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag"]]]:
        '''src_secure_tag block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_secure_tag ComputeFirewallPolicyWithRules#src_secure_tag}
        '''
        result = self._values.get("src_secure_tag")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag"]]], result)

    @builtins.property
    def src_threat_intelligences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_threat_intelligences ComputeFirewallPolicyWithRules#src_threat_intelligences}
        '''
        result = self._values.get("src_threat_intelligences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyWithRulesRuleMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesRuleMatchLayer4Config",
    jsii_struct_bases=[],
    name_mapping={"ip_protocol": "ipProtocol", "ports": "ports"},
)
class ComputeFirewallPolicyWithRulesRuleMatchLayer4Config:
    def __init__(
        self,
        *,
        ip_protocol: builtins.str,
        ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ip_protocol: The IP protocol to which this rule applies. The protocol type is required when creating a firewall rule. This value can either be one of the following well known protocol strings (tcp, udp, icmp, esp, ah, ipip, sctp), or the IP protocol number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#ip_protocol ComputeFirewallPolicyWithRules#ip_protocol}
        :param ports: An optional list of ports to which this rule applies. This field is only applicable for UDP or TCP protocol. Each entry must be either an integer or a range. If not specified, this rule applies to connections through any port. Example inputs include: ["22"], ["80","443"], and ["12345-12349"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#ports ComputeFirewallPolicyWithRules#ports}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb7bcda1f72940a4218c8fa6f8ba07367df9343009c95510a487f4f7c80a8350)
            check_type(argname="argument ip_protocol", value=ip_protocol, expected_type=type_hints["ip_protocol"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_protocol": ip_protocol,
        }
        if ports is not None:
            self._values["ports"] = ports

    @builtins.property
    def ip_protocol(self) -> builtins.str:
        '''The IP protocol to which this rule applies.

        The protocol
        type is required when creating a firewall rule.
        This value can either be one of the following well
        known protocol strings (tcp, udp, icmp, esp, ah, ipip, sctp),
        or the IP protocol number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#ip_protocol ComputeFirewallPolicyWithRules#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An optional list of ports to which this rule applies.

        This field
        is only applicable for UDP or TCP protocol. Each entry must be
        either an integer or a range. If not specified, this rule
        applies to connections through any port.
        Example inputs include: ["22"], ["80","443"], and
        ["12345-12349"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#ports ComputeFirewallPolicyWithRules#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyWithRulesRuleMatchLayer4Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeFirewallPolicyWithRulesRuleMatchLayer4ConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesRuleMatchLayer4ConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4ec269f4004f473c4b4c5cabc8a4cb63a178bfe594a04001cd36276dca888e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeFirewallPolicyWithRulesRuleMatchLayer4ConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5176c52ef4f3ef691a6be766ca65e5ec959bc18962a6dc0fab34a016628e222)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeFirewallPolicyWithRulesRuleMatchLayer4ConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2aa7e7beb13b581325e9271eb4c492c5a45eaa8c0712fc17560352561537365)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d9b6bf3ed8462900dbd42af084c25dec346cedab0c4a3d38e6f55949189bf6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ed805db06ce0cc110758420910efb0a149e0b5d0009d4337f55aef09f309cb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRuleMatchLayer4Config]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRuleMatchLayer4Config]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRuleMatchLayer4Config]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c7243dc823d431dd3a675085e67b496231b3adff53a67f798e5559610000716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeFirewallPolicyWithRulesRuleMatchLayer4ConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesRuleMatchLayer4ConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e02cb1d34601f2a53f1f2f570c9ac125fcca01ecb15c36aa4676c47eb2bf7e2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPorts")
    def reset_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPorts", []))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolInput")
    def ip_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f34126bf54a5d260a4def3cad9ee2c71e78b6341edfb8f7abed87df48e75976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aeb57e008f9ca986d9c1e2ec5cc5fdbac2b9f01786cdba3c075f25d50980d0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesRuleMatchLayer4Config]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesRuleMatchLayer4Config]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesRuleMatchLayer4Config]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3c0d5582233f97bac8a9f9c47e1ac2cb5ebd23a6fcc598008f704188aba0bcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeFirewallPolicyWithRulesRuleMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesRuleMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7e7a9d1a6a9391ff1f666342a0ff730b14c01109b0fc5bac05de76cec33d54a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLayer4Config")
    def put_layer4_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyWithRulesRuleMatchLayer4Config, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e39b805d4c6a4a94d3a8c8c1979813021568b0afc43b93f7943dbd820edd8198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLayer4Config", [value]))

    @jsii.member(jsii_name="putSrcSecureTag")
    def put_src_secure_tag(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e43797084a1c539717e5e09d1c6d4f163683839f32efe1805d6383315aa16011)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSrcSecureTag", [value]))

    @jsii.member(jsii_name="resetDestAddressGroups")
    def reset_dest_address_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestAddressGroups", []))

    @jsii.member(jsii_name="resetDestFqdns")
    def reset_dest_fqdns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestFqdns", []))

    @jsii.member(jsii_name="resetDestIpRanges")
    def reset_dest_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestIpRanges", []))

    @jsii.member(jsii_name="resetDestRegionCodes")
    def reset_dest_region_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestRegionCodes", []))

    @jsii.member(jsii_name="resetDestThreatIntelligences")
    def reset_dest_threat_intelligences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestThreatIntelligences", []))

    @jsii.member(jsii_name="resetSrcAddressGroups")
    def reset_src_address_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcAddressGroups", []))

    @jsii.member(jsii_name="resetSrcFqdns")
    def reset_src_fqdns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcFqdns", []))

    @jsii.member(jsii_name="resetSrcIpRanges")
    def reset_src_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcIpRanges", []))

    @jsii.member(jsii_name="resetSrcRegionCodes")
    def reset_src_region_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcRegionCodes", []))

    @jsii.member(jsii_name="resetSrcSecureTag")
    def reset_src_secure_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcSecureTag", []))

    @jsii.member(jsii_name="resetSrcThreatIntelligences")
    def reset_src_threat_intelligences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcThreatIntelligences", []))

    @builtins.property
    @jsii.member(jsii_name="layer4Config")
    def layer4_config(self) -> ComputeFirewallPolicyWithRulesRuleMatchLayer4ConfigList:
        return typing.cast(ComputeFirewallPolicyWithRulesRuleMatchLayer4ConfigList, jsii.get(self, "layer4Config"))

    @builtins.property
    @jsii.member(jsii_name="srcSecureTag")
    def src_secure_tag(
        self,
    ) -> "ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTagList":
        return typing.cast("ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTagList", jsii.get(self, "srcSecureTag"))

    @builtins.property
    @jsii.member(jsii_name="destAddressGroupsInput")
    def dest_address_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destAddressGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="destFqdnsInput")
    def dest_fqdns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destFqdnsInput"))

    @builtins.property
    @jsii.member(jsii_name="destIpRangesInput")
    def dest_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="destRegionCodesInput")
    def dest_region_codes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destRegionCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="destThreatIntelligencesInput")
    def dest_threat_intelligences_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destThreatIntelligencesInput"))

    @builtins.property
    @jsii.member(jsii_name="layer4ConfigInput")
    def layer4_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRuleMatchLayer4Config]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRuleMatchLayer4Config]]], jsii.get(self, "layer4ConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="srcAddressGroupsInput")
    def src_address_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcAddressGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="srcFqdnsInput")
    def src_fqdns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcFqdnsInput"))

    @builtins.property
    @jsii.member(jsii_name="srcIpRangesInput")
    def src_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="srcRegionCodesInput")
    def src_region_codes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcRegionCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="srcSecureTagInput")
    def src_secure_tag_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag"]]], jsii.get(self, "srcSecureTagInput"))

    @builtins.property
    @jsii.member(jsii_name="srcThreatIntelligencesInput")
    def src_threat_intelligences_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcThreatIntelligencesInput"))

    @builtins.property
    @jsii.member(jsii_name="destAddressGroups")
    def dest_address_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destAddressGroups"))

    @dest_address_groups.setter
    def dest_address_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a45293a2d629f0eb375e831ecd30f9c54cedd43e55563c2576614d50fa7f066)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destAddressGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destFqdns")
    def dest_fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destFqdns"))

    @dest_fqdns.setter
    def dest_fqdns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a956d306e0d726f6976cd6f8cfbf6e3192e65542e7a5d6457be1e19fb0b15e7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destFqdns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destIpRanges")
    def dest_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destIpRanges"))

    @dest_ip_ranges.setter
    def dest_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd9273416da391dbea0f3d21902cd90bb72a29c9608a2d225d84411804fdaeaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destRegionCodes")
    def dest_region_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destRegionCodes"))

    @dest_region_codes.setter
    def dest_region_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1da1192118f39ce15c2ca61c31035c8c80706adeee683f45f36961d0353dbddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destRegionCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destThreatIntelligences")
    def dest_threat_intelligences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destThreatIntelligences"))

    @dest_threat_intelligences.setter
    def dest_threat_intelligences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c41cbc3002d8aedd8491f1f1af16a4ad53561046cd02a5d59d9583c69ded575d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destThreatIntelligences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcAddressGroups")
    def src_address_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcAddressGroups"))

    @src_address_groups.setter
    def src_address_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0838f10bf4ecc12b690d1bccc32352afbbb416971494a8d7fbe5a35a6e3c6746)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcAddressGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcFqdns")
    def src_fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcFqdns"))

    @src_fqdns.setter
    def src_fqdns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c38c46e075375f9f111888761751d6eaccf7dfefd5e99971ef850dc33551a1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcFqdns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcIpRanges")
    def src_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcIpRanges"))

    @src_ip_ranges.setter
    def src_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d39a2b25835d0c3d7fdffb41717d708663672c2718c1efe4824434a29687c31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcRegionCodes")
    def src_region_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcRegionCodes"))

    @src_region_codes.setter
    def src_region_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04bbf841e5c547319180ce1b2a0ddf5e65ab04e3552d42535160c0c7fa2b5859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRegionCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcThreatIntelligences")
    def src_threat_intelligences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcThreatIntelligences"))

    @src_threat_intelligences.setter
    def src_threat_intelligences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baabcf0733be3ea4a26a0c3be3e4ce53802085e56241bc7460fdc7aa1cffdfa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcThreatIntelligences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeFirewallPolicyWithRulesRuleMatch]:
        return typing.cast(typing.Optional[ComputeFirewallPolicyWithRulesRuleMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeFirewallPolicyWithRulesRuleMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ad0d2eb25ea1b3666e7ab00d3ab8a582b39cb30df60c77012e50f6e8d624b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Name of the secure tag, created with TagManager's TagValue API.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ea016315f8b4ca576c83c2923625ee297a28ed988578d0a1fe961bf750d407)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the secure tag, created with TagManager's TagValue API.

        :pattern:

        tagValues/[0-9]+

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#name ComputeFirewallPolicyWithRules#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6092d9cdd0c0d4c5c5ac3127572e9cd9f12a29fe50ee328754ea7bea98bc7c71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbed65e40d3a429323fb94ae09d32408ddecdcd3feecbbcc04b7dc548f6c4a69)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1279b6aa854f9d23b2e0bdbb808adec63ece42e6614d67fc08c1ccd0160864)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e531d5f472e0f2c3d2f3efc7d003613e475f64cc5800c7fb1612e476fc30b93f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5c99c6cd0b5de07ba533caf90983126ed29a1ed8149b1afab26fe287e288004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5937f8d4ee505140754ccb4e07862ac725b018932aef05ad9ce708009ccae178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7542debd9ab7413a050879abb3fb042bfbfc7fcf9924a1798016cf71850a6c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d699aed9bfb9275da5316156e82605487bdacc608b73a1df4ee026e3234884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a574afc6090cbf71b4baf07e460b28605da912d6cbfbdac6b8c939d523e29ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeFirewallPolicyWithRulesRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8bdd42a0e54cdabe28eb57aaae6954b861edaaf53e60cb724a1844be2be5324)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        layer4_config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyWithRulesRuleMatchLayer4Config, typing.Dict[builtins.str, typing.Any]]]],
        dest_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_secure_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
        src_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param layer4_config: layer4_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#layer4_config ComputeFirewallPolicyWithRules#layer4_config}
        :param dest_address_groups: Address groups which should be matched against the traffic destination. Maximum number of destination address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#dest_address_groups ComputeFirewallPolicyWithRules#dest_address_groups}
        :param dest_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic destination. Maximum number of destination fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#dest_fqdns ComputeFirewallPolicyWithRules#dest_fqdns}
        :param dest_ip_ranges: Destination IP address range in CIDR format. Required for EGRESS rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#dest_ip_ranges ComputeFirewallPolicyWithRules#dest_ip_ranges}
        :param dest_region_codes: Region codes whose IP addresses will be used to match for destination of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of destination region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#dest_region_codes ComputeFirewallPolicyWithRules#dest_region_codes}
        :param dest_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#dest_threat_intelligences ComputeFirewallPolicyWithRules#dest_threat_intelligences}
        :param src_address_groups: Address groups which should be matched against the traffic source. Maximum number of source address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_address_groups ComputeFirewallPolicyWithRules#src_address_groups}
        :param src_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic source. Maximum number of source fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_fqdns ComputeFirewallPolicyWithRules#src_fqdns}
        :param src_ip_ranges: Source IP address range in CIDR format. Required for INGRESS rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_ip_ranges ComputeFirewallPolicyWithRules#src_ip_ranges}
        :param src_region_codes: Region codes whose IP addresses will be used to match for source of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of source region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_region_codes ComputeFirewallPolicyWithRules#src_region_codes}
        :param src_secure_tag: src_secure_tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_secure_tag ComputeFirewallPolicyWithRules#src_secure_tag}
        :param src_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#src_threat_intelligences ComputeFirewallPolicyWithRules#src_threat_intelligences}
        '''
        value = ComputeFirewallPolicyWithRulesRuleMatch(
            layer4_config=layer4_config,
            dest_address_groups=dest_address_groups,
            dest_fqdns=dest_fqdns,
            dest_ip_ranges=dest_ip_ranges,
            dest_region_codes=dest_region_codes,
            dest_threat_intelligences=dest_threat_intelligences,
            src_address_groups=src_address_groups,
            src_fqdns=src_fqdns,
            src_ip_ranges=src_ip_ranges,
            src_region_codes=src_region_codes,
            src_secure_tag=src_secure_tag,
            src_threat_intelligences=src_threat_intelligences,
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="putTargetSecureTag")
    def put_target_secure_tag(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeFirewallPolicyWithRulesRuleTargetSecureTag", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__227355b1e6c1dbfe10201ac89542d5e877cd4ff9be66e60bb8c70834d9ec2294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargetSecureTag", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDirection")
    def reset_direction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirection", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetEnableLogging")
    def reset_enable_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableLogging", []))

    @jsii.member(jsii_name="resetRuleName")
    def reset_rule_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleName", []))

    @jsii.member(jsii_name="resetSecurityProfileGroup")
    def reset_security_profile_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityProfileGroup", []))

    @jsii.member(jsii_name="resetTargetResources")
    def reset_target_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetResources", []))

    @jsii.member(jsii_name="resetTargetSecureTag")
    def reset_target_secure_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetSecureTag", []))

    @jsii.member(jsii_name="resetTargetServiceAccounts")
    def reset_target_service_accounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetServiceAccounts", []))

    @jsii.member(jsii_name="resetTlsInspect")
    def reset_tls_inspect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsInspect", []))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> ComputeFirewallPolicyWithRulesRuleMatchOutputReference:
        return typing.cast(ComputeFirewallPolicyWithRulesRuleMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="targetSecureTag")
    def target_secure_tag(
        self,
    ) -> "ComputeFirewallPolicyWithRulesRuleTargetSecureTagList":
        return typing.cast("ComputeFirewallPolicyWithRulesRuleTargetSecureTagList", jsii.get(self, "targetSecureTag"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="directionInput")
    def direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directionInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enableLoggingInput")
    def enable_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[ComputeFirewallPolicyWithRulesRuleMatch]:
        return typing.cast(typing.Optional[ComputeFirewallPolicyWithRulesRuleMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleNameInput")
    def rule_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="securityProfileGroupInput")
    def security_profile_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityProfileGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourcesInput")
    def target_resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetSecureTagInput")
    def target_secure_tag_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyWithRulesRuleTargetSecureTag"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyWithRulesRuleTargetSecureTag"]]], jsii.get(self, "targetSecureTagInput"))

    @builtins.property
    @jsii.member(jsii_name="targetServiceAccountsInput")
    def target_service_accounts_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetServiceAccountsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsInspectInput")
    def tls_inspect_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsInspectInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f0abe8b99c66940492f58150a2e46a27ebd4457fc9218830a996f11562ee3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5562fc8b468f92a2ee2e3e9d952d4911fc33bc3589d3c039e1d6bb466ed23bfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e267eaca3c278abbc6ecb7a0ea12eeb1a768e900523af9424300ed9ef799c039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "direction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ebf34a72bd80ea0109f415006feca36869da28922ef5b828502a74cbb95c994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableLogging")
    def enable_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableLogging"))

    @enable_logging.setter
    def enable_logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67cbef6f6ef205e7af8558fbe6eafcd961ae4176189f478786b74a552b4e6688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72d168db2977773e4e6ccc083ae91c399417fde952e00bf0f91eb90c4d0cac2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4340bb143c08dcee8f35d2b5e060970f05d0b9856d03a5a9a627ff0fa2327a35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityProfileGroup")
    def security_profile_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityProfileGroup"))

    @security_profile_group.setter
    def security_profile_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44432967cf8144849112d875a86fbbbaf1afbd92db69f1c2d70868ad3e52f904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityProfileGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetResources")
    def target_resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetResources"))

    @target_resources.setter
    def target_resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db85a8adf2a612268edddc70a56482ebd9154656de68c9142b0d7bc20fece1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetServiceAccounts")
    def target_service_accounts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetServiceAccounts"))

    @target_service_accounts.setter
    def target_service_accounts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcbdbde38cfeea5395ff097285236118e0ed9f3dd87597f49cc3cda6d693b7a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetServiceAccounts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsInspect")
    def tls_inspect(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tlsInspect"))

    @tls_inspect.setter
    def tls_inspect(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f57034246adbcff2d18fbfc03d9777b477589cc58a18e022f1d9f8653dd1314a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsInspect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f650b1433c80ad36617bb2a9040fc3080566d598d666b83d983d79be12a6e4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesRuleTargetSecureTag",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ComputeFirewallPolicyWithRulesRuleTargetSecureTag:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Name of the secure tag, created with TagManager's TagValue API.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9ce0d81bd1fa3a1c9d8c4e92142567b6a5704c603eebd9c57cf33c07634654d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the secure tag, created with TagManager's TagValue API.

        :pattern:

        tagValues/[0-9]+

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#name ComputeFirewallPolicyWithRules#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyWithRulesRuleTargetSecureTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeFirewallPolicyWithRulesRuleTargetSecureTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesRuleTargetSecureTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15eed367c86ab91b388861f7efc46c8b217f7e9aad42bcc3ec5d82ae807330a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeFirewallPolicyWithRulesRuleTargetSecureTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47be8fc299a83fbd22aed39f26bb4a9b494b143ba173cf1c9fb3d9f774f3391e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeFirewallPolicyWithRulesRuleTargetSecureTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a543fa502920ed8e57bf9756f1e460b16eff385670c204b77548d8999961084)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c55ec5ce7acbbd5725d11773f7944318e5948a906e4e58d8d3cbf67a23ce971c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e8a66dd654c8a22d6c1ebeefc7acc971563fd86741b97e623eb76faf7cf4cb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRuleTargetSecureTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRuleTargetSecureTag]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRuleTargetSecureTag]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f3573bbf918df0764f54a878ed4dcb9f51f46153b627ebba4e032551a1bd7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeFirewallPolicyWithRulesRuleTargetSecureTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesRuleTargetSecureTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__090aecb45d2fa5dd5bc8f0d091c09d15e717b03cd9f088a58cc08d46aa09d2a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a72098e78052a056f5979721ee31aff31cf8869805cd085fafdba67fbb81ece4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesRuleTargetSecureTag]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesRuleTargetSecureTag]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesRuleTargetSecureTag]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__456ff5ad97f78fc118ee8de167b71b6012a161dbb85ba34175c53558583ef45b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeFirewallPolicyWithRulesTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#create ComputeFirewallPolicyWithRules#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#delete ComputeFirewallPolicyWithRules#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#update ComputeFirewallPolicyWithRules#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be1a737f8bfa37d6b5dc640e980a4aaad35406b19cea84d7f4c7f470c58a6cc2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#create ComputeFirewallPolicyWithRules#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#delete ComputeFirewallPolicyWithRules#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_with_rules#update ComputeFirewallPolicyWithRules#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyWithRulesTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeFirewallPolicyWithRulesTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyWithRules.ComputeFirewallPolicyWithRulesTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74b4987da9194889e1c628db228a5ff97b77d416d41c9303097bc0b50d42a335)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af2823ccbf98bedaf0070a39de5f17d5773113d9d1b3588c61199582e0450f32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6345768c20cf588784674a9f178ee6c5ef1029151811e7c77d1c2e28206e5fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__502454bac77ed3f07dc0705aa17966517f80192d95df3375bdae382aee78f0ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b39a1bbc4d2e6a7f1262b1a30559b85f9beb796bb69e4a11f75017a5a48c937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeFirewallPolicyWithRules",
    "ComputeFirewallPolicyWithRulesConfig",
    "ComputeFirewallPolicyWithRulesPredefinedRules",
    "ComputeFirewallPolicyWithRulesPredefinedRulesList",
    "ComputeFirewallPolicyWithRulesPredefinedRulesMatch",
    "ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4Config",
    "ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigList",
    "ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigOutputReference",
    "ComputeFirewallPolicyWithRulesPredefinedRulesMatchList",
    "ComputeFirewallPolicyWithRulesPredefinedRulesMatchOutputReference",
    "ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTag",
    "ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagList",
    "ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagOutputReference",
    "ComputeFirewallPolicyWithRulesPredefinedRulesOutputReference",
    "ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTag",
    "ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTagList",
    "ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTagOutputReference",
    "ComputeFirewallPolicyWithRulesRule",
    "ComputeFirewallPolicyWithRulesRuleList",
    "ComputeFirewallPolicyWithRulesRuleMatch",
    "ComputeFirewallPolicyWithRulesRuleMatchLayer4Config",
    "ComputeFirewallPolicyWithRulesRuleMatchLayer4ConfigList",
    "ComputeFirewallPolicyWithRulesRuleMatchLayer4ConfigOutputReference",
    "ComputeFirewallPolicyWithRulesRuleMatchOutputReference",
    "ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag",
    "ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTagList",
    "ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTagOutputReference",
    "ComputeFirewallPolicyWithRulesRuleOutputReference",
    "ComputeFirewallPolicyWithRulesRuleTargetSecureTag",
    "ComputeFirewallPolicyWithRulesRuleTargetSecureTagList",
    "ComputeFirewallPolicyWithRulesRuleTargetSecureTagOutputReference",
    "ComputeFirewallPolicyWithRulesTimeouts",
    "ComputeFirewallPolicyWithRulesTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c57eadbc5dabdff07cea5ec6d41995950b61a55b148075f4b4fc2240f43f90dd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    parent: builtins.str,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyWithRulesRule, typing.Dict[builtins.str, typing.Any]]]],
    short_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeFirewallPolicyWithRulesTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b52c0899e18617f394e74b17a6c84f561b5a3698ae17e92ae236459f359b399b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__121ed78fb1b0a21270c079f1e8c5446206acc572b26c22f80126598b845f45df(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyWithRulesRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2cf45d93edd8933831121bbaef7df185c37db9509e4f44ce54b6e3dcfa6af1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ecc6faad7e432fc793fb1e53948725f1091c41dd58a721077c0969b5642915(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa77c342e863ee78cfebe81f34c60a158e101b71271ef2d577b3fbb5e1b8d01f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0ce4d9db428c9d09ab06416c852b2c852c8fae6ece650c2563829d8ee9d933(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0fa84cd4378edd2f5558126cf0e721ac2d660f770a327845fdb0dc1b71f47bf(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parent: builtins.str,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyWithRulesRule, typing.Dict[builtins.str, typing.Any]]]],
    short_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeFirewallPolicyWithRulesTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a13949702a7ef613d679c3bc77238e512589ac1905b3d5b9db8418de6863c431(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a120dc72b7ec73bad02f31d1fbb3ac54438fc147c6d883cce804a799d3058c9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27071a2928ffc50b13110b30adeb75e14e11a61dbc5b5611d45092a34bd51190(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09bb2c594d629cbfba118242f6992a580a96a6f2dfb4cab5599054e6e53de17d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a723ab61cfa125ebc3b5f8ba357afc1ada37c8e6a54cee1e83c1adaf4f1f9021(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a9d55dd190f2a4ed3e12618cf24893394f551c58aca07da67ba5caab2f602c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec287ea870d720b22b774e1c90020e867b1fc445d84b2604255b1ab3aa258c9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a113d26c181adb0ba2cdfda643309a6359ac11fddf786c6d69ceef6352cc7b0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db47c0a31bc5e517feab50e77ae4ef3e254f939bcefc7e6f21f50b2cdfb0bff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96ae5069e3ea275e5954b6ed5323d3765cbee8f9b0a1fa66f08335f2ead6168(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da16b4977871d59686bea100e4ec55bac56103504bf798da8133b0a15a3f1fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00953c81932025f0e18053d28a9c90e009b009a9c4c68d34c4a92c86da81911c(
    value: typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRulesMatchLayer4Config],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6844d13d3bf10fd81c4ee772e0a0abaaad9f0089e68307fd7fa4ab5f557893(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d992b99415f6d161d48258f7155c86cda783f53cf565247a7d1e247ee876ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f35d9d0884189c5772bc37dbc84322f6b8b386007d44c210c3a30ee26b43d814(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__364faa8364bcf9181326dd8d04fa9d3364074d055cfff9edefb153e60a0ceb16(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ab8bdb457bd7b8fbf5835f5cd86da147bcc063d40a38e59b23604336e0a40f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff8207c21f851234d3669acdf9a83188df5dd4031f34443e5228c091e655e79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59c227c9b14b5761f733a632cd39652dd144e9cd7ed0b3c705c81e7e48cf172(
    value: typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRulesMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea562b20df90e6806addda56d751b5feb58d277508133142db5ba3aa6a1dc99d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f501a3c6953a2604b61034c785af7de28be331176883c6bd2eccda3859f4be82(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3370e999972505917f090bb4befcee3a6c9bcc7504f19680f6d690be642c5a90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c419f284dce17cfb626a200cb063b6bc123d8e9df25dead4e690298e127080b2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd223ffd02ecc096fa650cbe102bd7e02357b91c5abe042e54db8ce7b4ac2b3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b17abcd686f6cd6746990fec4cb4d3ee217379171b2676cfb641181fb47afe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544ec24469e7c097bbc4138613912949388e24ebe91fb2c9848f2e3400ff99e0(
    value: typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTag],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__399d404dc834215bf94346fdceaec664b2ad7ac334270bc1853928bab5e80484(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d1bb0539c40dd3968ee477934c2f749d23b8f918c8398ae6b547bb1df234c1(
    value: typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b7aceb9cbdbeffd5642f7a5fddaafea224da2fecbe9292bbae542ab78ebc07b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f4f0a1f5bdcbd6f560048daea6b8701aa9d4e310367e8ebef01bb5d22513816(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2af953ca453197ef8324a850667819a87b432d13826473c333d5fb4678e2dce9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ac0de5fb8ff87dbb21fca7acc56e3270741de712aeb79db6fb743a1cb71d42(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e9d52cd0e2259382a253a36e69573f0d5d034bc1587b3b6d3fb09a33905527(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a29c25e47537bdf16f06c60515f3f2ee0b1c5eabebee9a91b6e058fdb991028(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46c3296c52e8a72a8fa939baa946ed3b6a5765c4f806f95380e23653aa09357(
    value: typing.Optional[ComputeFirewallPolicyWithRulesPredefinedRulesTargetSecureTag],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa6ea40db83bec1754a22af5eba10d053060b5c5029d7020714ef787ba152d5c(
    *,
    action: builtins.str,
    match: typing.Union[ComputeFirewallPolicyWithRulesRuleMatch, typing.Dict[builtins.str, typing.Any]],
    priority: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    direction: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    security_profile_group: typing.Optional[builtins.str] = None,
    target_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_secure_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyWithRulesRuleTargetSecureTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    tls_inspect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5e0da7e64b90f079d25dc405556647cceb8a85772b70e8156a9941424fb486(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758e4ccbd368b00d52a396ecb24bc416f847b616dba92f49c15169606931a501(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c47b191b5170123c05eff150c082d6b7e26433e56b34a5569954365d102e52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034204c7d7f632044a1990f89d7c41b322d935506a6aea486f8046a8ee98a880(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7deb573164d1fc15a782359f5651b1d4ea42bf75f3d9cd5bed22840259590579(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a315c654a70e5cc835ab927924c8b8bdd951913083435e90d6273cc29343d058(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce2d9ecdcf34bb12ab69cd460714e7dc7254801a8ccb969908bf416a1b26027(
    *,
    layer4_config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyWithRulesRuleMatchLayer4Config, typing.Dict[builtins.str, typing.Any]]]],
    dest_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_secure_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
    src_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7bcda1f72940a4218c8fa6f8ba07367df9343009c95510a487f4f7c80a8350(
    *,
    ip_protocol: builtins.str,
    ports: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ec269f4004f473c4b4c5cabc8a4cb63a178bfe594a04001cd36276dca888e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5176c52ef4f3ef691a6be766ca65e5ec959bc18962a6dc0fab34a016628e222(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2aa7e7beb13b581325e9271eb4c492c5a45eaa8c0712fc17560352561537365(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9b6bf3ed8462900dbd42af084c25dec346cedab0c4a3d38e6f55949189bf6a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed805db06ce0cc110758420910efb0a149e0b5d0009d4337f55aef09f309cb9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c7243dc823d431dd3a675085e67b496231b3adff53a67f798e5559610000716(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRuleMatchLayer4Config]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02cb1d34601f2a53f1f2f570c9ac125fcca01ecb15c36aa4676c47eb2bf7e2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f34126bf54a5d260a4def3cad9ee2c71e78b6341edfb8f7abed87df48e75976(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aeb57e008f9ca986d9c1e2ec5cc5fdbac2b9f01786cdba3c075f25d50980d0b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c0d5582233f97bac8a9f9c47e1ac2cb5ebd23a6fcc598008f704188aba0bcc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesRuleMatchLayer4Config]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e7a9d1a6a9391ff1f666342a0ff730b14c01109b0fc5bac05de76cec33d54a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39b805d4c6a4a94d3a8c8c1979813021568b0afc43b93f7943dbd820edd8198(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyWithRulesRuleMatchLayer4Config, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e43797084a1c539717e5e09d1c6d4f163683839f32efe1805d6383315aa16011(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a45293a2d629f0eb375e831ecd30f9c54cedd43e55563c2576614d50fa7f066(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a956d306e0d726f6976cd6f8cfbf6e3192e65542e7a5d6457be1e19fb0b15e7c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd9273416da391dbea0f3d21902cd90bb72a29c9608a2d225d84411804fdaeaa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da1192118f39ce15c2ca61c31035c8c80706adeee683f45f36961d0353dbddb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c41cbc3002d8aedd8491f1f1af16a4ad53561046cd02a5d59d9583c69ded575d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0838f10bf4ecc12b690d1bccc32352afbbb416971494a8d7fbe5a35a6e3c6746(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c38c46e075375f9f111888761751d6eaccf7dfefd5e99971ef850dc33551a1a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d39a2b25835d0c3d7fdffb41717d708663672c2718c1efe4824434a29687c31(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bbf841e5c547319180ce1b2a0ddf5e65ab04e3552d42535160c0c7fa2b5859(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baabcf0733be3ea4a26a0c3be3e4ce53802085e56241bc7460fdc7aa1cffdfa0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad0d2eb25ea1b3666e7ab00d3ab8a582b39cb30df60c77012e50f6e8d624b31(
    value: typing.Optional[ComputeFirewallPolicyWithRulesRuleMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ea016315f8b4ca576c83c2923625ee297a28ed988578d0a1fe961bf750d407(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6092d9cdd0c0d4c5c5ac3127572e9cd9f12a29fe50ee328754ea7bea98bc7c71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbed65e40d3a429323fb94ae09d32408ddecdcd3feecbbcc04b7dc548f6c4a69(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1279b6aa854f9d23b2e0bdbb808adec63ece42e6614d67fc08c1ccd0160864(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e531d5f472e0f2c3d2f3efc7d003613e475f64cc5800c7fb1612e476fc30b93f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c99c6cd0b5de07ba533caf90983126ed29a1ed8149b1afab26fe287e288004(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5937f8d4ee505140754ccb4e07862ac725b018932aef05ad9ce708009ccae178(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7542debd9ab7413a050879abb3fb042bfbfc7fcf9924a1798016cf71850a6c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d699aed9bfb9275da5316156e82605487bdacc608b73a1df4ee026e3234884(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a574afc6090cbf71b4baf07e460b28605da912d6cbfbdac6b8c939d523e29ab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesRuleMatchSrcSecureTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8bdd42a0e54cdabe28eb57aaae6954b861edaaf53e60cb724a1844be2be5324(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__227355b1e6c1dbfe10201ac89542d5e877cd4ff9be66e60bb8c70834d9ec2294(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyWithRulesRuleTargetSecureTag, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f0abe8b99c66940492f58150a2e46a27ebd4457fc9218830a996f11562ee3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5562fc8b468f92a2ee2e3e9d952d4911fc33bc3589d3c039e1d6bb466ed23bfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e267eaca3c278abbc6ecb7a0ea12eeb1a768e900523af9424300ed9ef799c039(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ebf34a72bd80ea0109f415006feca36869da28922ef5b828502a74cbb95c994(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67cbef6f6ef205e7af8558fbe6eafcd961ae4176189f478786b74a552b4e6688(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d168db2977773e4e6ccc083ae91c399417fde952e00bf0f91eb90c4d0cac2d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4340bb143c08dcee8f35d2b5e060970f05d0b9856d03a5a9a627ff0fa2327a35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44432967cf8144849112d875a86fbbbaf1afbd92db69f1c2d70868ad3e52f904(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db85a8adf2a612268edddc70a56482ebd9154656de68c9142b0d7bc20fece1f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcbdbde38cfeea5395ff097285236118e0ed9f3dd87597f49cc3cda6d693b7a1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f57034246adbcff2d18fbfc03d9777b477589cc58a18e022f1d9f8653dd1314a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f650b1433c80ad36617bb2a9040fc3080566d598d666b83d983d79be12a6e4c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ce0d81bd1fa3a1c9d8c4e92142567b6a5704c603eebd9c57cf33c07634654d(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15eed367c86ab91b388861f7efc46c8b217f7e9aad42bcc3ec5d82ae807330a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47be8fc299a83fbd22aed39f26bb4a9b494b143ba173cf1c9fb3d9f774f3391e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a543fa502920ed8e57bf9756f1e460b16eff385670c204b77548d8999961084(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55ec5ce7acbbd5725d11773f7944318e5948a906e4e58d8d3cbf67a23ce971c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8a66dd654c8a22d6c1ebeefc7acc971563fd86741b97e623eb76faf7cf4cb3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f3573bbf918df0764f54a878ed4dcb9f51f46153b627ebba4e032551a1bd7e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyWithRulesRuleTargetSecureTag]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090aecb45d2fa5dd5bc8f0d091c09d15e717b03cd9f088a58cc08d46aa09d2a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72098e78052a056f5979721ee31aff31cf8869805cd085fafdba67fbb81ece4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__456ff5ad97f78fc118ee8de167b71b6012a161dbb85ba34175c53558583ef45b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesRuleTargetSecureTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1a737f8bfa37d6b5dc640e980a4aaad35406b19cea84d7f4c7f470c58a6cc2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b4987da9194889e1c628db228a5ff97b77d416d41c9303097bc0b50d42a335(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2823ccbf98bedaf0070a39de5f17d5773113d9d1b3588c61199582e0450f32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6345768c20cf588784674a9f178ee6c5ef1029151811e7c77d1c2e28206e5fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502454bac77ed3f07dc0705aa17966517f80192d95df3375bdae382aee78f0ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b39a1bbc4d2e6a7f1262b1a30559b85f9beb796bb69e4a11f75017a5a48c937(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyWithRulesTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

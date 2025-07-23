r'''
# `google_compute_region_network_firewall_policy_with_rules`

Refer to the Terraform Registry for docs: [`google_compute_region_network_firewall_policy_with_rules`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules).
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


class ComputeRegionNetworkFirewallPolicyWithRules(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRules",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules google_compute_region_network_firewall_policy_with_rules}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionNetworkFirewallPolicyWithRulesRule", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionNetworkFirewallPolicyWithRulesTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules google_compute_region_network_firewall_policy_with_rules} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: User-provided name of the Network firewall policy. The name should be unique in the project in which the firewall policy is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#name ComputeRegionNetworkFirewallPolicyWithRules#name}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#rule ComputeRegionNetworkFirewallPolicyWithRules#rule}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#description ComputeRegionNetworkFirewallPolicyWithRules#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#id ComputeRegionNetworkFirewallPolicyWithRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#project ComputeRegionNetworkFirewallPolicyWithRules#project}.
        :param region: The region of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#region ComputeRegionNetworkFirewallPolicyWithRules#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#timeouts ComputeRegionNetworkFirewallPolicyWithRules#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d3b82021d45b19a8eb7ae6c4d6bb7b6e435c8cb3f79a2f19df73288a657128b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeRegionNetworkFirewallPolicyWithRulesConfig(
            name=name,
            rule=rule,
            description=description,
            id=id,
            project=project,
            region=region,
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
        '''Generates CDKTF code for importing a ComputeRegionNetworkFirewallPolicyWithRules resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeRegionNetworkFirewallPolicyWithRules to import.
        :param import_from_id: The id of the existing ComputeRegionNetworkFirewallPolicyWithRules that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeRegionNetworkFirewallPolicyWithRules to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6296f3046e52349495f90c04c0c5dc41db12ea6cacd369a989aae57b4d28ba9d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionNetworkFirewallPolicyWithRulesRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f514a637558b83c3bb4a6f60e6fcb3b93de73c63cf47ef202fd0bb267c44bd1)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#create ComputeRegionNetworkFirewallPolicyWithRules#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#delete ComputeRegionNetworkFirewallPolicyWithRules#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#update ComputeRegionNetworkFirewallPolicyWithRules#update}.
        '''
        value = ComputeRegionNetworkFirewallPolicyWithRulesTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="networkFirewallPolicyId")
    def network_firewall_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkFirewallPolicyId"))

    @builtins.property
    @jsii.member(jsii_name="predefinedRules")
    def predefined_rules(
        self,
    ) -> "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesList":
        return typing.cast("ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesList", jsii.get(self, "predefinedRules"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "ComputeRegionNetworkFirewallPolicyWithRulesRuleList":
        return typing.cast("ComputeRegionNetworkFirewallPolicyWithRulesRuleList", jsii.get(self, "rule"))

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
    def timeouts(
        self,
    ) -> "ComputeRegionNetworkFirewallPolicyWithRulesTimeoutsOutputReference":
        return typing.cast("ComputeRegionNetworkFirewallPolicyWithRulesTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyWithRulesRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyWithRulesRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionNetworkFirewallPolicyWithRulesTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionNetworkFirewallPolicyWithRulesTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__679d44d39667fb584fb7f9f88368a68bd9720114289fb75878170a75cd927d3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80d52f0c1142d468f7aa7ee10449ba71bb3510bf992ef251db9b270dd3530e9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77fd95b503226481bf533df75d8e7ccd9cc4baf121a7d3c8d63705795e577412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c17740557ab03474ff107ec56017e6747114132ea324cdc5034803ac91ccaf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b70499db20e48e9f3fad9c9899eb76b14c5d97d1396ed0eda639b0c40215f84e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "rule": "rule",
        "description": "description",
        "id": "id",
        "project": "project",
        "region": "region",
        "timeouts": "timeouts",
    },
)
class ComputeRegionNetworkFirewallPolicyWithRulesConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        name: builtins.str,
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionNetworkFirewallPolicyWithRulesRule", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionNetworkFirewallPolicyWithRulesTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: User-provided name of the Network firewall policy. The name should be unique in the project in which the firewall policy is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#name ComputeRegionNetworkFirewallPolicyWithRules#name}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#rule ComputeRegionNetworkFirewallPolicyWithRules#rule}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#description ComputeRegionNetworkFirewallPolicyWithRules#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#id ComputeRegionNetworkFirewallPolicyWithRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#project ComputeRegionNetworkFirewallPolicyWithRules#project}.
        :param region: The region of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#region ComputeRegionNetworkFirewallPolicyWithRules#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#timeouts ComputeRegionNetworkFirewallPolicyWithRules#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ComputeRegionNetworkFirewallPolicyWithRulesTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af89d8480a2b29785e3c174f62e3d2229175a4d6a6523ae8dd2cd151140632f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "rule": rule,
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
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
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
    def name(self) -> builtins.str:
        '''User-provided name of the Network firewall policy.

        The name should be unique in the project in which the firewall policy is created.
        The name must be 1-63 characters long, and comply with RFC1035. Specifically,
        the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?
        which means the first character must be a lowercase letter, and all following characters must be a dash,
        lowercase letter, or digit, except the last character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#name ComputeRegionNetworkFirewallPolicyWithRules#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyWithRulesRule"]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#rule ComputeRegionNetworkFirewallPolicyWithRules#rule}
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyWithRulesRule"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#description ComputeRegionNetworkFirewallPolicyWithRules#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#id ComputeRegionNetworkFirewallPolicyWithRules#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#project ComputeRegionNetworkFirewallPolicyWithRules#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#region ComputeRegionNetworkFirewallPolicyWithRules#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["ComputeRegionNetworkFirewallPolicyWithRulesTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#timeouts ComputeRegionNetworkFirewallPolicyWithRules#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeRegionNetworkFirewallPolicyWithRulesTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyWithRulesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRules",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRules:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d64fd7801d40912cce25a1c0df6980a846c45376a8167f8724b30518ce80af7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87409cce58b73e9d7f54f6cfc3a9b20ff560621f2f988c30aaf455dfee77a704)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e8c335ad7032cf872ba20d956fcd2ceeb955d123d6f2df6740f4436f473f5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__177beb2e62ac972385672a62795accdeb3999e69c06ebbdf2dfb23b693a38f67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66cd642cb3f43da3ae94861af39bb436298c0cfa20955ccd01fcdb9c9a3e16ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatch",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatch:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4Config",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4Config:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d2acbb5ae6513f4e3837bffe69162a5278902dc0ff5ddce01927f41dc335b41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1746a6ff60407ea1a7b2121986d92ec99e88d0f113d944f784bc465b24ac283)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00df435bcad5de70bdacd70b963af3e20087e853cb060400ed083f7516bbdc1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4448980e32987c9b6d2f1dd010cb01c6414d2def7bdd0930c0897637e33a3e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06bb224dc9d965521713de7be53c586ee76d338845d6fa0d229574a54f21dd18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c71d88f34bd57299fdd2b096fac75b121758b922f537b94432bb16511661de0)
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
    ) -> typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4Config]:
        return typing.cast(typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4Config], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4Config],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b1936a03c95d0d54325127a059153a762993eec0c4aa927510097af8402475)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94a62eadc5f1f2da5a17a69f2cd2929bd28296964ec74e040474ab6a0ecb2623)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6edd6a9629337269863fd10f15b9a075f23fb0971566c982cae0f5e1759c274)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__102aa27a686c6f84c7a271bd8beb11c16d09a6df7504411dfcadb46aba92793f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cab7e5df5d1d280f9977130a7d587778931fe894a4b790b9a31d164abcddb86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84df2edd1295839fd268289d0e7bbe931d927fb9fc57e20ceda1d81cc4687a3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf12810ddc9be9ce5f0fdd6a58663c5392d02b1db43ef74104fc63f954d37c8c)
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
    ) -> ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigList:
        return typing.cast(ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigList, jsii.get(self, "layer4Config"))

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
    ) -> "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagList":
        return typing.cast("ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagList", jsii.get(self, "srcSecureTag"))

    @builtins.property
    @jsii.member(jsii_name="srcThreatIntelligences")
    def src_threat_intelligences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcThreatIntelligences"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatch]:
        return typing.cast(typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b06f0689fdd6b3d0fd9c7531c360909b03774fad879f84ad1e46ce2620acfe13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTag",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTag:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__261238ba20a0356fca082170403b2846eac3f3d200b54645120813c4d70ef753)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__068354671a65efc99eb1fd6975f42eb15596c379a44f85d25abf3b7dbff53902)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__079cc9a39095aa874ffc922ad861fcd2bb086e8f7362a4a89ca8c395110eb756)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b93eb7690f07bb2c680888827ddfa67b26b02f46aa687cba3d229d1099d60de0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__295c5a30bfb15916c8c072978d0defe9b2cc51d71c9e106514392eba07ff80aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b6b63cd0e9c9414e75d13226be5cea1dff06d2acf0fdd89e7e5632466ff0d54)
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
    ) -> typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTag]:
        return typing.cast(typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTag], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTag],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fa6d2033dffe6aff82b9bece629e0c276395d5f2710ceacae962badacaea6c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12810e37a5e949ea7e2c6b46e3463c1b27e9350f94c6cbbf1396f1dc9198aa5c)
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
    def match(
        self,
    ) -> ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchList:
        return typing.cast(ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchList, jsii.get(self, "match"))

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
    @jsii.member(jsii_name="targetSecureTag")
    def target_secure_tag(
        self,
    ) -> "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTagList":
        return typing.cast("ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTagList", jsii.get(self, "targetSecureTag"))

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
    ) -> typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRules]:
        return typing.cast(typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd3c5b2b220772ed8098c2e3af9f8851da5ed7b942692072c79d5c5459ae5c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTag",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTag:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b8d4e1c46898008d8cc94475756d6fbac057df887d90bcbcbb04654d42fbeac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13b3a01ceee8ecaee98075ccddf2229ba77671b72d7c28d240e2b98ed54cebfa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d242e813d245ce31cbba95c4fbbfe327bd57d6d483f5b3788968c41cd7d498f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7a36a5f27bca28a05f61145720d7e441a30677d568e1524576e0b2ac236bab0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__737c8e38fa994afeddf5bd17489817adf121666d978e238f452875195ee288f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8030c00e7ab8a03cdef83c33dd809f8db9dfe1d7331dd4370dc354d07db5efe4)
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
    ) -> typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTag]:
        return typing.cast(typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTag], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTag],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb952fdedde698c78d134975c3b1d870ec1ac878f3e5a563898395d136741f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesRule",
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
        "target_secure_tag": "targetSecureTag",
        "target_service_accounts": "targetServiceAccounts",
        "tls_inspect": "tlsInspect",
    },
)
class ComputeRegionNetworkFirewallPolicyWithRulesRule:
    def __init__(
        self,
        *,
        action: builtins.str,
        match: typing.Union["ComputeRegionNetworkFirewallPolicyWithRulesRuleMatch", typing.Dict[builtins.str, typing.Any]],
        priority: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        direction: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        security_profile_group: typing.Optional[builtins.str] = None,
        target_secure_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        tls_inspect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param action: The Action to perform when the client connection triggers the rule. Can currently be either "allow", "deny", "apply_security_profile_group" or "goto_next". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#action ComputeRegionNetworkFirewallPolicyWithRules#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#match ComputeRegionNetworkFirewallPolicyWithRules#match}
        :param priority: An integer indicating the priority of a rule in the list. The priority must be a value between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest priority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#priority ComputeRegionNetworkFirewallPolicyWithRules#priority}
        :param description: A description of the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#description ComputeRegionNetworkFirewallPolicyWithRules#description}
        :param direction: The direction in which this rule applies. If unspecified an INGRESS rule is created. Possible values: ["INGRESS", "EGRESS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#direction ComputeRegionNetworkFirewallPolicyWithRules#direction}
        :param disabled: Denotes whether the firewall policy rule is disabled. When set to true, the firewall policy rule is not enforced and traffic behaves as if it did not exist. If this is unspecified, the firewall policy rule will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#disabled ComputeRegionNetworkFirewallPolicyWithRules#disabled}
        :param enable_logging: Denotes whether to enable logging for a particular rule. If logging is enabled, logs will be exported to the configured export destination in Stackdriver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#enable_logging ComputeRegionNetworkFirewallPolicyWithRules#enable_logging}
        :param rule_name: An optional name for the rule. This field is not a unique identifier and can be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#rule_name ComputeRegionNetworkFirewallPolicyWithRules#rule_name}
        :param security_profile_group: A fully-qualified URL of a SecurityProfile resource instance. Example: https://networksecurity.googleapis.com/v1/projects/{project}/locations/{location}/securityProfileGroups/my-security-profile-group Must be specified if action is 'apply_security_profile_group'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#security_profile_group ComputeRegionNetworkFirewallPolicyWithRules#security_profile_group}
        :param target_secure_tag: target_secure_tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#target_secure_tag ComputeRegionNetworkFirewallPolicyWithRules#target_secure_tag}
        :param target_service_accounts: A list of service accounts indicating the sets of instances that are applied with this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#target_service_accounts ComputeRegionNetworkFirewallPolicyWithRules#target_service_accounts}
        :param tls_inspect: Boolean flag indicating if the traffic should be TLS decrypted. It can be set only if action = 'apply_security_profile_group' and cannot be set for other actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#tls_inspect ComputeRegionNetworkFirewallPolicyWithRules#tls_inspect}
        '''
        if isinstance(match, dict):
            match = ComputeRegionNetworkFirewallPolicyWithRulesRuleMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6043c1ad9471dea3114ef1bcf566f30e7108e18a0334db2ad0f978ac8421aa37)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument security_profile_group", value=security_profile_group, expected_type=type_hints["security_profile_group"])
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
        if target_secure_tag is not None:
            self._values["target_secure_tag"] = target_secure_tag
        if target_service_accounts is not None:
            self._values["target_service_accounts"] = target_service_accounts
        if tls_inspect is not None:
            self._values["tls_inspect"] = tls_inspect

    @builtins.property
    def action(self) -> builtins.str:
        '''The Action to perform when the client connection triggers the rule. Can currently be either "allow", "deny", "apply_security_profile_group" or "goto_next".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#action ComputeRegionNetworkFirewallPolicyWithRules#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match(self) -> "ComputeRegionNetworkFirewallPolicyWithRulesRuleMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#match ComputeRegionNetworkFirewallPolicyWithRules#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("ComputeRegionNetworkFirewallPolicyWithRulesRuleMatch", result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''An integer indicating the priority of a rule in the list.

        The priority must be a value
        between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the
        highest priority and 2147483647 is the lowest priority.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#priority ComputeRegionNetworkFirewallPolicyWithRules#priority}
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#description ComputeRegionNetworkFirewallPolicyWithRules#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def direction(self) -> typing.Optional[builtins.str]:
        '''The direction in which this rule applies. If unspecified an INGRESS rule is created. Possible values: ["INGRESS", "EGRESS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#direction ComputeRegionNetworkFirewallPolicyWithRules#direction}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#disabled ComputeRegionNetworkFirewallPolicyWithRules#disabled}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#enable_logging ComputeRegionNetworkFirewallPolicyWithRules#enable_logging}
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the rule. This field is not a unique identifier and can be updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#rule_name ComputeRegionNetworkFirewallPolicyWithRules#rule_name}
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_profile_group(self) -> typing.Optional[builtins.str]:
        '''A fully-qualified URL of a SecurityProfile resource instance. Example: https://networksecurity.googleapis.com/v1/projects/{project}/locations/{location}/securityProfileGroups/my-security-profile-group Must be specified if action is 'apply_security_profile_group'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#security_profile_group ComputeRegionNetworkFirewallPolicyWithRules#security_profile_group}
        '''
        result = self._values.get("security_profile_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_secure_tag(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag"]]]:
        '''target_secure_tag block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#target_secure_tag ComputeRegionNetworkFirewallPolicyWithRules#target_secure_tag}
        '''
        result = self._values.get("target_secure_tag")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag"]]], result)

    @builtins.property
    def target_service_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of service accounts indicating the sets of instances that are applied with this rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#target_service_accounts ComputeRegionNetworkFirewallPolicyWithRules#target_service_accounts}
        '''
        result = self._values.get("target_service_accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tls_inspect(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean flag indicating if the traffic should be TLS decrypted.

        It can be set only if action = 'apply_security_profile_group' and cannot be set for other actions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#tls_inspect ComputeRegionNetworkFirewallPolicyWithRules#tls_inspect}
        '''
        result = self._values.get("tls_inspect")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyWithRulesRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkFirewallPolicyWithRulesRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ee1796ca9bff5172a923da4c61473a19c3d52afac3cb98d198a5ab9ea1cbdb5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionNetworkFirewallPolicyWithRulesRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e058f2b527c0fe184b1493b2579e5591506337b6f56a84b3e94d44251addbb3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionNetworkFirewallPolicyWithRulesRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce06265e23d705c22270180837cb6311109d38d4b18385f49c9bd3c389cbeec8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74703d18125ac2d61a3da77c2671944609dfa64116d6e593469c8786869779a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72281baf1682f590fcec760043388a3ba1d5b3a7d77819e722fcf5eb14298440)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4e0da22bdd20611fa344208dc468cca4217e89be94ca31305597e9890185d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesRuleMatch",
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
class ComputeRegionNetworkFirewallPolicyWithRulesRuleMatch:
    def __init__(
        self,
        *,
        layer4_config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config", typing.Dict[builtins.str, typing.Any]]]],
        dest_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_secure_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
        src_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param layer4_config: layer4_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#layer4_config ComputeRegionNetworkFirewallPolicyWithRules#layer4_config}
        :param dest_address_groups: Address groups which should be matched against the traffic destination. Maximum number of destination address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#dest_address_groups ComputeRegionNetworkFirewallPolicyWithRules#dest_address_groups}
        :param dest_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic destination. Maximum number of destination fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#dest_fqdns ComputeRegionNetworkFirewallPolicyWithRules#dest_fqdns}
        :param dest_ip_ranges: Destination IP address range in CIDR format. Required for EGRESS rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#dest_ip_ranges ComputeRegionNetworkFirewallPolicyWithRules#dest_ip_ranges}
        :param dest_region_codes: Region codes whose IP addresses will be used to match for destination of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of destination region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#dest_region_codes ComputeRegionNetworkFirewallPolicyWithRules#dest_region_codes}
        :param dest_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#dest_threat_intelligences ComputeRegionNetworkFirewallPolicyWithRules#dest_threat_intelligences}
        :param src_address_groups: Address groups which should be matched against the traffic source. Maximum number of source address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_address_groups ComputeRegionNetworkFirewallPolicyWithRules#src_address_groups}
        :param src_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic source. Maximum number of source fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_fqdns ComputeRegionNetworkFirewallPolicyWithRules#src_fqdns}
        :param src_ip_ranges: Source IP address range in CIDR format. Required for INGRESS rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_ip_ranges ComputeRegionNetworkFirewallPolicyWithRules#src_ip_ranges}
        :param src_region_codes: Region codes whose IP addresses will be used to match for source of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of source region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_region_codes ComputeRegionNetworkFirewallPolicyWithRules#src_region_codes}
        :param src_secure_tag: src_secure_tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_secure_tag ComputeRegionNetworkFirewallPolicyWithRules#src_secure_tag}
        :param src_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_threat_intelligences ComputeRegionNetworkFirewallPolicyWithRules#src_threat_intelligences}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a052b90b2b272013a9bf7722a599de246cd5f8ff1b8cb33646a11e99c6a762d)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config"]]:
        '''layer4_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#layer4_config ComputeRegionNetworkFirewallPolicyWithRules#layer4_config}
        '''
        result = self._values.get("layer4_config")
        assert result is not None, "Required property 'layer4_config' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config"]], result)

    @builtins.property
    def dest_address_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Address groups which should be matched against the traffic destination. Maximum number of destination address groups is 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#dest_address_groups ComputeRegionNetworkFirewallPolicyWithRules#dest_address_groups}
        '''
        result = self._values.get("dest_address_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_fqdns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Fully Qualified Domain Name (FQDN) which should be matched against traffic destination. Maximum number of destination fqdn allowed is 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#dest_fqdns ComputeRegionNetworkFirewallPolicyWithRules#dest_fqdns}
        '''
        result = self._values.get("dest_fqdns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Destination IP address range in CIDR format. Required for EGRESS rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#dest_ip_ranges ComputeRegionNetworkFirewallPolicyWithRules#dest_ip_ranges}
        '''
        result = self._values.get("dest_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_region_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Region codes whose IP addresses will be used to match for destination of traffic.

        Should be specified as 2 letter country code defined as per
        ISO 3166 alpha-2 country codes. ex."US"
        Maximum number of destination region codes allowed is 5000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#dest_region_codes ComputeRegionNetworkFirewallPolicyWithRules#dest_region_codes}
        '''
        result = self._values.get("dest_region_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_threat_intelligences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic destination.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#dest_threat_intelligences ComputeRegionNetworkFirewallPolicyWithRules#dest_threat_intelligences}
        '''
        result = self._values.get("dest_threat_intelligences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_address_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Address groups which should be matched against the traffic source. Maximum number of source address groups is 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_address_groups ComputeRegionNetworkFirewallPolicyWithRules#src_address_groups}
        '''
        result = self._values.get("src_address_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_fqdns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Fully Qualified Domain Name (FQDN) which should be matched against traffic source. Maximum number of source fqdn allowed is 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_fqdns ComputeRegionNetworkFirewallPolicyWithRules#src_fqdns}
        '''
        result = self._values.get("src_fqdns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Source IP address range in CIDR format. Required for INGRESS rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_ip_ranges ComputeRegionNetworkFirewallPolicyWithRules#src_ip_ranges}
        '''
        result = self._values.get("src_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_region_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Region codes whose IP addresses will be used to match for source of traffic.

        Should be specified as 2 letter country code defined as per
        ISO 3166 alpha-2 country codes. ex."US"
        Maximum number of source region codes allowed is 5000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_region_codes ComputeRegionNetworkFirewallPolicyWithRules#src_region_codes}
        '''
        result = self._values.get("src_region_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_secure_tag(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag"]]]:
        '''src_secure_tag block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_secure_tag ComputeRegionNetworkFirewallPolicyWithRules#src_secure_tag}
        '''
        result = self._values.get("src_secure_tag")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag"]]], result)

    @builtins.property
    def src_threat_intelligences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_threat_intelligences ComputeRegionNetworkFirewallPolicyWithRules#src_threat_intelligences}
        '''
        result = self._values.get("src_threat_intelligences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyWithRulesRuleMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config",
    jsii_struct_bases=[],
    name_mapping={"ip_protocol": "ipProtocol", "ports": "ports"},
)
class ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config:
    def __init__(
        self,
        *,
        ip_protocol: builtins.str,
        ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ip_protocol: The IP protocol to which this rule applies. The protocol type is required when creating a firewall rule. This value can either be one of the following well known protocol strings (tcp, udp, icmp, esp, ah, ipip, sctp), or the IP protocol number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#ip_protocol ComputeRegionNetworkFirewallPolicyWithRules#ip_protocol}
        :param ports: An optional list of ports to which this rule applies. This field is only applicable for UDP or TCP protocol. Each entry must be either an integer or a range. If not specified, this rule applies to connections through any port. Example inputs include: ["22"], ["80","443"], and ["12345-12349"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#ports ComputeRegionNetworkFirewallPolicyWithRules#ports}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fa9c41751b2bcd42650e8168d5ba179857aa3d8724874dc9119c197a5cf7fba)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#ip_protocol ComputeRegionNetworkFirewallPolicyWithRules#ip_protocol}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#ports ComputeRegionNetworkFirewallPolicyWithRules#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4ConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4ConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6dfa86184b4b9e6ce9ff1ab9966e846cc616fc835c8c3e6a5cd8fa6607fe346)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4ConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c44942f81dcecc504844774ff9134bc38df1c26ec2054859e8fe163199c1a628)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4ConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dda1f38065db0ccdf7b6ca55707a2ed83b31390fad5aa674131bb78750383c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3092e05ac93e7f9d03d50cf00610c4d5135192eb1f690736ee2821729dcee9a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ec85b9b4f389b3c47eea38ba034cf42b673ba48acbd936bec53e4ca7bbe9600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1cfc7fcb68beda326a819b64e37710b3030630f5c60cd40bf1380f51449a7ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4ConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4ConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b6cdee9225e037ed89dc8619f7cd8309f1785e9496b90a351f976d0342de6c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74a060c974d1c48a9fbae2b164370fc169d1f45ea3da39015ddfcd975f8b12ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cafdf738858e9c86f7a3fc184a75fe8d7c314f65a48e7191be25a0a19121feb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c51a393e1081aea127273fdcd0efe2a59497c59562db3f046ebf324367e36fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__207c07c8a20aaf8cd33d5b139e67ca976183f63eaaa61c184d049562614e6742)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLayer4Config")
    def put_layer4_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__666f7113f8c965ca702ce4cd97a0b2f8fdb855405b1faa016ad4b397e0964ebe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLayer4Config", [value]))

    @jsii.member(jsii_name="putSrcSecureTag")
    def put_src_secure_tag(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e1d34a27c3fea339b3c76fcee8efe8e31ad689fc632539acbfdf9ee8f64018b)
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
    def layer4_config(
        self,
    ) -> ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4ConfigList:
        return typing.cast(ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4ConfigList, jsii.get(self, "layer4Config"))

    @builtins.property
    @jsii.member(jsii_name="srcSecureTag")
    def src_secure_tag(
        self,
    ) -> "ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTagList":
        return typing.cast("ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTagList", jsii.get(self, "srcSecureTag"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config]]], jsii.get(self, "layer4ConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag"]]], jsii.get(self, "srcSecureTagInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__65322f0ea9df5e48bee26b43d8323c8cfed71787ed8ea22caa3b1d5ee539bd70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destAddressGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destFqdns")
    def dest_fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destFqdns"))

    @dest_fqdns.setter
    def dest_fqdns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8a54b0e908c738f6a0966a4997ed0b9b4a22fa0c0a7b21583426d9f683625f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destFqdns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destIpRanges")
    def dest_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destIpRanges"))

    @dest_ip_ranges.setter
    def dest_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf8052e127df401ba58fe6bd9282fe88a3764270375fd1205294e768dc4f60f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destRegionCodes")
    def dest_region_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destRegionCodes"))

    @dest_region_codes.setter
    def dest_region_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57cda7c40de16b3568479bf7217cdbb221d38ca6a19612d5ac3440537cde8540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destRegionCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destThreatIntelligences")
    def dest_threat_intelligences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destThreatIntelligences"))

    @dest_threat_intelligences.setter
    def dest_threat_intelligences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3177c4b84155de0c75a2bc8ef2e9266c3347307839f1914910e0be910ca06166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destThreatIntelligences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcAddressGroups")
    def src_address_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcAddressGroups"))

    @src_address_groups.setter
    def src_address_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c2573fcb3f9b532fb417a1ee6377eeeb1cf780187804bc4914f39a164a1334f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcAddressGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcFqdns")
    def src_fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcFqdns"))

    @src_fqdns.setter
    def src_fqdns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5217ca058d47444e94e3d851b144f0c2decd2e14f3ec6e69fc40182c0b3a20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcFqdns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcIpRanges")
    def src_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcIpRanges"))

    @src_ip_ranges.setter
    def src_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__083a66e316f85ff2ca2df8bbd4def3f066def1d0597ccf20ffa85322fb568016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcRegionCodes")
    def src_region_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcRegionCodes"))

    @src_region_codes.setter
    def src_region_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5611fa366d00e034511f90d51476e1e92f49fcdef271ec67393600e4bf02f5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRegionCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcThreatIntelligences")
    def src_threat_intelligences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcThreatIntelligences"))

    @src_threat_intelligences.setter
    def src_threat_intelligences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e7f3572c2b8c55f6bbef1a71d64cb686e2850680b17c1492b00e6d4e73a125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcThreatIntelligences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatch]:
        return typing.cast(typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6885ffa8e21e16fdd5d2a3e88ce7fa45f8d9559a15bd3e3b90c4113ad9f292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Name of the secure tag, created with TagManager's TagValue API.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3406c35c88d0e0167feb04198a46d04c1cc3f5c12b093d58ecf94671b7b14bf)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the secure tag, created with TagManager's TagValue API.

        :pattern:

        tagValues/[0-9]+

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#name ComputeRegionNetworkFirewallPolicyWithRules#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07f6e6786f5f52eedc1835096510582fbe510376354f59edc77defa580ef4e46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__261ede22cbbd28a7c10e06bb1f91e612031fbb538132bb4ee78d08ae7b0658c2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb1ef92c824d7b2073f79cbcb6afe61de5d2601c90918dddf6c97e25f9d7ce9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37844f06ba5f1a51c2dbe8181d5aeb5c2b13cef37484682de00380463033f046)
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
            type_hints = typing.get_type_hints(_typecheckingstub__361448c714cd1c735f0ae9c2fea7dda9fc42ddf58fb8e8bcfbb1daeaee99bf4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d27194dd0d52405d41076f421f268db6ca99f6c3c9466bc4627f544aa5a5688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dd983fa410a8f0cc2289b75b2435adc5f0ca14cf7b8d7c022379347be6ff67e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__799810dcaaa57477318175d789f3971a88d9d1e6ceb6d4cc94c339cbeb8e04e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8afccea631a355d0af7c9863296cd0d3c8aed42da46e4948407633ac494ece47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionNetworkFirewallPolicyWithRulesRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__950c42f667b4d7140c4ea0a3953860e2d7aff59783f3df0153b2794595d11f25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        layer4_config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config, typing.Dict[builtins.str, typing.Any]]]],
        dest_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_secure_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
        src_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param layer4_config: layer4_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#layer4_config ComputeRegionNetworkFirewallPolicyWithRules#layer4_config}
        :param dest_address_groups: Address groups which should be matched against the traffic destination. Maximum number of destination address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#dest_address_groups ComputeRegionNetworkFirewallPolicyWithRules#dest_address_groups}
        :param dest_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic destination. Maximum number of destination fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#dest_fqdns ComputeRegionNetworkFirewallPolicyWithRules#dest_fqdns}
        :param dest_ip_ranges: Destination IP address range in CIDR format. Required for EGRESS rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#dest_ip_ranges ComputeRegionNetworkFirewallPolicyWithRules#dest_ip_ranges}
        :param dest_region_codes: Region codes whose IP addresses will be used to match for destination of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of destination region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#dest_region_codes ComputeRegionNetworkFirewallPolicyWithRules#dest_region_codes}
        :param dest_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#dest_threat_intelligences ComputeRegionNetworkFirewallPolicyWithRules#dest_threat_intelligences}
        :param src_address_groups: Address groups which should be matched against the traffic source. Maximum number of source address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_address_groups ComputeRegionNetworkFirewallPolicyWithRules#src_address_groups}
        :param src_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic source. Maximum number of source fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_fqdns ComputeRegionNetworkFirewallPolicyWithRules#src_fqdns}
        :param src_ip_ranges: Source IP address range in CIDR format. Required for INGRESS rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_ip_ranges ComputeRegionNetworkFirewallPolicyWithRules#src_ip_ranges}
        :param src_region_codes: Region codes whose IP addresses will be used to match for source of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of source region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_region_codes ComputeRegionNetworkFirewallPolicyWithRules#src_region_codes}
        :param src_secure_tag: src_secure_tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_secure_tag ComputeRegionNetworkFirewallPolicyWithRules#src_secure_tag}
        :param src_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#src_threat_intelligences ComputeRegionNetworkFirewallPolicyWithRules#src_threat_intelligences}
        '''
        value = ComputeRegionNetworkFirewallPolicyWithRulesRuleMatch(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d352fc3fbe32df10d958ba51fc41c86fee0ac26591d2812cec518347dd86c6b)
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
    def match(
        self,
    ) -> ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchOutputReference:
        return typing.cast(ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="targetSecureTag")
    def target_secure_tag(
        self,
    ) -> "ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTagList":
        return typing.cast("ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTagList", jsii.get(self, "targetSecureTag"))

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
    def match_input(
        self,
    ) -> typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatch]:
        return typing.cast(typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatch], jsii.get(self, "matchInput"))

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
    @jsii.member(jsii_name="targetSecureTagInput")
    def target_secure_tag_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag"]]], jsii.get(self, "targetSecureTagInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4908db96e1d42a523c8a9fea177bd24db8ad98ff5f96014a11473ee5e7b7841f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f494f19fcd9b6477e3b2981211b8f6bdd9c8aa0247813d9be317f8b741a6f91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c6d00720f59994371ad3c166a21130ddcf118859803275af6246f96b466aa2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3e37ed55ca1e5ad6e456969e462507654cd6cf18fae2a9dce5225868f180a01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__544fdb8c5e65b4ff34a573dbeee723550a017e3c8bbef3aa29044e839f0c83e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f18cb7110697e4ed367c59d94b5219bd1b54bf69a8fbb1c20ce8563623a0c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d7892d72c6cc22c3119b4907c2a9c979061bc4fa15f40d42710b3b3b612c58c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityProfileGroup")
    def security_profile_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityProfileGroup"))

    @security_profile_group.setter
    def security_profile_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f1f65a83052c0e5e71222a2ad08fcf9767640a4a8dbce5ba42ba6181507f6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityProfileGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetServiceAccounts")
    def target_service_accounts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetServiceAccounts"))

    @target_service_accounts.setter
    def target_service_accounts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a9c5613a996c7a4e20c1f190b7843f186dfa430417d4b339e3dbb10bcfe7e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7089b97d3a70f17391ad5353924c967d81800baabcf28560398edee8d8f7dc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsInspect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc7ceffcb578509a05c4e7adf5f43f942de13dd388e80b0fb5cf955881c283a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Name of the secure tag, created with TagManager's TagValue API.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8528d52d9d3c2ab24d4f09c657beeb9b6f3a8b997237582d139512d7d8318e4a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the secure tag, created with TagManager's TagValue API.

        :pattern:

        tagValues/[0-9]+

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#name ComputeRegionNetworkFirewallPolicyWithRules#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45aa09bdab94283b303f6be3592528b8937c7b24a25d919beb87c5947e2b4293)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__807121868bf5c7343e7937129392a064c182fb88b2d33346e24398309b66982a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae1ecd9ccdb5454e29db96ef5061a4a12e5081d76c05fa28119c8b9eee52162)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be9ea4c992907e8398a179b15a168c8356a1ecc189058d998b65c64d29fc7d8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5078ed0525783f1fe389bb45b9f4c4ab3492318c9a0cc26bed92f62aa02c92a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d8f52fadac36333a9c67ce86f7fa1a1fca39fd4f1979ba3d4be57e88708c942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb366608e13434e206ba5c86720b21d163ba566fd74eff11b99ec19ce665646f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d09849468ae03b003e1e47cb21c7f553f34e9e94d6f09e570f367fbe5199d8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06cd896fe7313c0a51a3eb8e4bdb54d0fab1740f10d0a7eb63c32745697b4984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeRegionNetworkFirewallPolicyWithRulesTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#create ComputeRegionNetworkFirewallPolicyWithRules#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#delete ComputeRegionNetworkFirewallPolicyWithRules#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#update ComputeRegionNetworkFirewallPolicyWithRules#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b05135f1254cfb3aa631d4688d09dd3d2729e78538213ea0e60c8614015aa0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#create ComputeRegionNetworkFirewallPolicyWithRules#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#delete ComputeRegionNetworkFirewallPolicyWithRules#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_with_rules#update ComputeRegionNetworkFirewallPolicyWithRules#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyWithRulesTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkFirewallPolicyWithRulesTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyWithRules.ComputeRegionNetworkFirewallPolicyWithRulesTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d33c14c3b0f6395da0f76c97910a0ce7daac813f4b81ea011931c25b280e8ca8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecbc99313488cf76afc5bbd1c42df6de3ef0d93789ac85fa9a2d44e3432f80dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c03b3ae800a9b2fd185fd47cd7087e71b1888449689b97e4d3f442636839cf43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22cae8b13da9875d34d97eebb24b6f93a7457a23a166b211c4e1e3f235adf7a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21b6eee2aa944083fd9a9a5dd2577aafd8b0f406dcc08cc120a3e89a87c07c07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeRegionNetworkFirewallPolicyWithRules",
    "ComputeRegionNetworkFirewallPolicyWithRulesConfig",
    "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRules",
    "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesList",
    "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatch",
    "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4Config",
    "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigList",
    "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4ConfigOutputReference",
    "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchList",
    "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchOutputReference",
    "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTag",
    "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagList",
    "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTagOutputReference",
    "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesOutputReference",
    "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTag",
    "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTagList",
    "ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTagOutputReference",
    "ComputeRegionNetworkFirewallPolicyWithRulesRule",
    "ComputeRegionNetworkFirewallPolicyWithRulesRuleList",
    "ComputeRegionNetworkFirewallPolicyWithRulesRuleMatch",
    "ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config",
    "ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4ConfigList",
    "ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4ConfigOutputReference",
    "ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchOutputReference",
    "ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag",
    "ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTagList",
    "ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTagOutputReference",
    "ComputeRegionNetworkFirewallPolicyWithRulesRuleOutputReference",
    "ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag",
    "ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTagList",
    "ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTagOutputReference",
    "ComputeRegionNetworkFirewallPolicyWithRulesTimeouts",
    "ComputeRegionNetworkFirewallPolicyWithRulesTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__5d3b82021d45b19a8eb7ae6c4d6bb7b6e435c8cb3f79a2f19df73288a657128b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyWithRulesRule, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionNetworkFirewallPolicyWithRulesTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6296f3046e52349495f90c04c0c5dc41db12ea6cacd369a989aae57b4d28ba9d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f514a637558b83c3bb4a6f60e6fcb3b93de73c63cf47ef202fd0bb267c44bd1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyWithRulesRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679d44d39667fb584fb7f9f88368a68bd9720114289fb75878170a75cd927d3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d52f0c1142d468f7aa7ee10449ba71bb3510bf992ef251db9b270dd3530e9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77fd95b503226481bf533df75d8e7ccd9cc4baf121a7d3c8d63705795e577412(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c17740557ab03474ff107ec56017e6747114132ea324cdc5034803ac91ccaf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b70499db20e48e9f3fad9c9899eb76b14c5d97d1396ed0eda639b0c40215f84e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af89d8480a2b29785e3c174f62e3d2229175a4d6a6523ae8dd2cd151140632f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyWithRulesRule, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionNetworkFirewallPolicyWithRulesTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d64fd7801d40912cce25a1c0df6980a846c45376a8167f8724b30518ce80af7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87409cce58b73e9d7f54f6cfc3a9b20ff560621f2f988c30aaf455dfee77a704(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e8c335ad7032cf872ba20d956fcd2ceeb955d123d6f2df6740f4436f473f5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177beb2e62ac972385672a62795accdeb3999e69c06ebbdf2dfb23b693a38f67(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cd642cb3f43da3ae94861af39bb436298c0cfa20955ccd01fcdb9c9a3e16ec(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d2acbb5ae6513f4e3837bffe69162a5278902dc0ff5ddce01927f41dc335b41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1746a6ff60407ea1a7b2121986d92ec99e88d0f113d944f784bc465b24ac283(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00df435bcad5de70bdacd70b963af3e20087e853cb060400ed083f7516bbdc1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4448980e32987c9b6d2f1dd010cb01c6414d2def7bdd0930c0897637e33a3e2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06bb224dc9d965521713de7be53c586ee76d338845d6fa0d229574a54f21dd18(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c71d88f34bd57299fdd2b096fac75b121758b922f537b94432bb16511661de0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b1936a03c95d0d54325127a059153a762993eec0c4aa927510097af8402475(
    value: typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchLayer4Config],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a62eadc5f1f2da5a17a69f2cd2929bd28296964ec74e040474ab6a0ecb2623(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6edd6a9629337269863fd10f15b9a075f23fb0971566c982cae0f5e1759c274(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102aa27a686c6f84c7a271bd8beb11c16d09a6df7504411dfcadb46aba92793f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cab7e5df5d1d280f9977130a7d587778931fe894a4b790b9a31d164abcddb86(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84df2edd1295839fd268289d0e7bbe931d927fb9fc57e20ceda1d81cc4687a3e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf12810ddc9be9ce5f0fdd6a58663c5392d02b1db43ef74104fc63f954d37c8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b06f0689fdd6b3d0fd9c7531c360909b03774fad879f84ad1e46ce2620acfe13(
    value: typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261238ba20a0356fca082170403b2846eac3f3d200b54645120813c4d70ef753(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068354671a65efc99eb1fd6975f42eb15596c379a44f85d25abf3b7dbff53902(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079cc9a39095aa874ffc922ad861fcd2bb086e8f7362a4a89ca8c395110eb756(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93eb7690f07bb2c680888827ddfa67b26b02f46aa687cba3d229d1099d60de0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__295c5a30bfb15916c8c072978d0defe9b2cc51d71c9e106514392eba07ff80aa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b6b63cd0e9c9414e75d13226be5cea1dff06d2acf0fdd89e7e5632466ff0d54(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa6d2033dffe6aff82b9bece629e0c276395d5f2710ceacae962badacaea6c8(
    value: typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesMatchSrcSecureTag],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12810e37a5e949ea7e2c6b46e3463c1b27e9350f94c6cbbf1396f1dc9198aa5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd3c5b2b220772ed8098c2e3af9f8851da5ed7b942692072c79d5c5459ae5c1(
    value: typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8d4e1c46898008d8cc94475756d6fbac057df887d90bcbcbb04654d42fbeac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b3a01ceee8ecaee98075ccddf2229ba77671b72d7c28d240e2b98ed54cebfa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d242e813d245ce31cbba95c4fbbfe327bd57d6d483f5b3788968c41cd7d498f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a36a5f27bca28a05f61145720d7e441a30677d568e1524576e0b2ac236bab0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737c8e38fa994afeddf5bd17489817adf121666d978e238f452875195ee288f3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8030c00e7ab8a03cdef83c33dd809f8db9dfe1d7331dd4370dc354d07db5efe4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb952fdedde698c78d134975c3b1d870ec1ac878f3e5a563898395d136741f4(
    value: typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesPredefinedRulesTargetSecureTag],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6043c1ad9471dea3114ef1bcf566f30e7108e18a0334db2ad0f978ac8421aa37(
    *,
    action: builtins.str,
    match: typing.Union[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatch, typing.Dict[builtins.str, typing.Any]],
    priority: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    direction: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    security_profile_group: typing.Optional[builtins.str] = None,
    target_secure_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    tls_inspect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee1796ca9bff5172a923da4c61473a19c3d52afac3cb98d198a5ab9ea1cbdb5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e058f2b527c0fe184b1493b2579e5591506337b6f56a84b3e94d44251addbb3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce06265e23d705c22270180837cb6311109d38d4b18385f49c9bd3c389cbeec8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74703d18125ac2d61a3da77c2671944609dfa64116d6e593469c8786869779a2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72281baf1682f590fcec760043388a3ba1d5b3a7d77819e722fcf5eb14298440(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4e0da22bdd20611fa344208dc468cca4217e89be94ca31305597e9890185d4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a052b90b2b272013a9bf7722a599de246cd5f8ff1b8cb33646a11e99c6a762d(
    *,
    layer4_config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config, typing.Dict[builtins.str, typing.Any]]]],
    dest_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_secure_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
    src_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa9c41751b2bcd42650e8168d5ba179857aa3d8724874dc9119c197a5cf7fba(
    *,
    ip_protocol: builtins.str,
    ports: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6dfa86184b4b9e6ce9ff1ab9966e846cc616fc835c8c3e6a5cd8fa6607fe346(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44942f81dcecc504844774ff9134bc38df1c26ec2054859e8fe163199c1a628(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dda1f38065db0ccdf7b6ca55707a2ed83b31390fad5aa674131bb78750383c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3092e05ac93e7f9d03d50cf00610c4d5135192eb1f690736ee2821729dcee9a2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec85b9b4f389b3c47eea38ba034cf42b673ba48acbd936bec53e4ca7bbe9600(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1cfc7fcb68beda326a819b64e37710b3030630f5c60cd40bf1380f51449a7ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6cdee9225e037ed89dc8619f7cd8309f1785e9496b90a351f976d0342de6c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a060c974d1c48a9fbae2b164370fc169d1f45ea3da39015ddfcd975f8b12ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cafdf738858e9c86f7a3fc184a75fe8d7c314f65a48e7191be25a0a19121feb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c51a393e1081aea127273fdcd0efe2a59497c59562db3f046ebf324367e36fe1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207c07c8a20aaf8cd33d5b139e67ca976183f63eaaa61c184d049562614e6742(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__666f7113f8c965ca702ce4cd97a0b2f8fdb855405b1faa016ad4b397e0964ebe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchLayer4Config, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1d34a27c3fea339b3c76fcee8efe8e31ad689fc632539acbfdf9ee8f64018b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65322f0ea9df5e48bee26b43d8323c8cfed71787ed8ea22caa3b1d5ee539bd70(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8a54b0e908c738f6a0966a4997ed0b9b4a22fa0c0a7b21583426d9f683625f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf8052e127df401ba58fe6bd9282fe88a3764270375fd1205294e768dc4f60f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57cda7c40de16b3568479bf7217cdbb221d38ca6a19612d5ac3440537cde8540(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3177c4b84155de0c75a2bc8ef2e9266c3347307839f1914910e0be910ca06166(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2573fcb3f9b532fb417a1ee6377eeeb1cf780187804bc4914f39a164a1334f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5217ca058d47444e94e3d851b144f0c2decd2e14f3ec6e69fc40182c0b3a20(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083a66e316f85ff2ca2df8bbd4def3f066def1d0597ccf20ffa85322fb568016(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5611fa366d00e034511f90d51476e1e92f49fcdef271ec67393600e4bf02f5c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e7f3572c2b8c55f6bbef1a71d64cb686e2850680b17c1492b00e6d4e73a125(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6885ffa8e21e16fdd5d2a3e88ce7fa45f8d9559a15bd3e3b90c4113ad9f292(
    value: typing.Optional[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3406c35c88d0e0167feb04198a46d04c1cc3f5c12b093d58ecf94671b7b14bf(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f6e6786f5f52eedc1835096510582fbe510376354f59edc77defa580ef4e46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261ede22cbbd28a7c10e06bb1f91e612031fbb538132bb4ee78d08ae7b0658c2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb1ef92c824d7b2073f79cbcb6afe61de5d2601c90918dddf6c97e25f9d7ce9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37844f06ba5f1a51c2dbe8181d5aeb5c2b13cef37484682de00380463033f046(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361448c714cd1c735f0ae9c2fea7dda9fc42ddf58fb8e8bcfbb1daeaee99bf4f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d27194dd0d52405d41076f421f268db6ca99f6c3c9466bc4627f544aa5a5688(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd983fa410a8f0cc2289b75b2435adc5f0ca14cf7b8d7c022379347be6ff67e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799810dcaaa57477318175d789f3971a88d9d1e6ceb6d4cc94c339cbeb8e04e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8afccea631a355d0af7c9863296cd0d3c8aed42da46e4948407633ac494ece47(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesRuleMatchSrcSecureTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__950c42f667b4d7140c4ea0a3953860e2d7aff59783f3df0153b2794595d11f25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d352fc3fbe32df10d958ba51fc41c86fee0ac26591d2812cec518347dd86c6b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4908db96e1d42a523c8a9fea177bd24db8ad98ff5f96014a11473ee5e7b7841f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f494f19fcd9b6477e3b2981211b8f6bdd9c8aa0247813d9be317f8b741a6f91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c6d00720f59994371ad3c166a21130ddcf118859803275af6246f96b466aa2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e37ed55ca1e5ad6e456969e462507654cd6cf18fae2a9dce5225868f180a01(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544fdb8c5e65b4ff34a573dbeee723550a017e3c8bbef3aa29044e839f0c83e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f18cb7110697e4ed367c59d94b5219bd1b54bf69a8fbb1c20ce8563623a0c8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d7892d72c6cc22c3119b4907c2a9c979061bc4fa15f40d42710b3b3b612c58c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f1f65a83052c0e5e71222a2ad08fcf9767640a4a8dbce5ba42ba6181507f6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a9c5613a996c7a4e20c1f190b7843f186dfa430417d4b339e3dbb10bcfe7e1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7089b97d3a70f17391ad5353924c967d81800baabcf28560398edee8d8f7dc3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7ceffcb578509a05c4e7adf5f43f942de13dd388e80b0fb5cf955881c283a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8528d52d9d3c2ab24d4f09c657beeb9b6f3a8b997237582d139512d7d8318e4a(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45aa09bdab94283b303f6be3592528b8937c7b24a25d919beb87c5947e2b4293(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807121868bf5c7343e7937129392a064c182fb88b2d33346e24398309b66982a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae1ecd9ccdb5454e29db96ef5061a4a12e5081d76c05fa28119c8b9eee52162(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9ea4c992907e8398a179b15a168c8356a1ecc189058d998b65c64d29fc7d8a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5078ed0525783f1fe389bb45b9f4c4ab3492318c9a0cc26bed92f62aa02c92a1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d8f52fadac36333a9c67ce86f7fa1a1fca39fd4f1979ba3d4be57e88708c942(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb366608e13434e206ba5c86720b21d163ba566fd74eff11b99ec19ce665646f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d09849468ae03b003e1e47cb21c7f553f34e9e94d6f09e570f367fbe5199d8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06cd896fe7313c0a51a3eb8e4bdb54d0fab1740f10d0a7eb63c32745697b4984(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesRuleTargetSecureTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b05135f1254cfb3aa631d4688d09dd3d2729e78538213ea0e60c8614015aa0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d33c14c3b0f6395da0f76c97910a0ce7daac813f4b81ea011931c25b280e8ca8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbc99313488cf76afc5bbd1c42df6de3ef0d93789ac85fa9a2d44e3432f80dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03b3ae800a9b2fd185fd47cd7087e71b1888449689b97e4d3f442636839cf43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22cae8b13da9875d34d97eebb24b6f93a7457a23a166b211c4e1e3f235adf7a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b6eee2aa944083fd9a9a5dd2577aafd8b0f406dcc08cc120a3e89a87c07c07(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyWithRulesTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

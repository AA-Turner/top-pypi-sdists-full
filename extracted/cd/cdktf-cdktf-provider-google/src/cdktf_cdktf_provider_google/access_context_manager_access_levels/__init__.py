r'''
# `google_access_context_manager_access_levels`

Refer to the Terraform Registry for docs: [`google_access_context_manager_access_levels`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels).
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


class AccessContextManagerAccessLevels(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevels",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels google_access_context_manager_access_levels}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        parent: builtins.str,
        access_levels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerAccessLevelsAccessLevels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerAccessLevelsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels google_access_context_manager_access_levels} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param parent: The AccessPolicy this AccessLevel lives in. Format: accessPolicies/{policy_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#parent AccessContextManagerAccessLevels#parent}
        :param access_levels: access_levels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#access_levels AccessContextManagerAccessLevels#access_levels}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#id AccessContextManagerAccessLevels#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#timeouts AccessContextManagerAccessLevels#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99b3a3db400c571aa4c62cdba24572c96f8ca4ecba925f247dde68e20dc25d16)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccessContextManagerAccessLevelsConfig(
            parent=parent,
            access_levels=access_levels,
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
        '''Generates CDKTF code for importing a AccessContextManagerAccessLevels resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AccessContextManagerAccessLevels to import.
        :param import_from_id: The id of the existing AccessContextManagerAccessLevels that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AccessContextManagerAccessLevels to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6bbe6aaf11713dad54491c0ac7b3c12d5abd3599e007caa410723b1a462a72)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccessLevels")
    def put_access_levels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerAccessLevelsAccessLevels", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73bdc277ea7d716f5e8ad60c155e51d4389e24ac2c043eb1a71048aa5d92b6a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccessLevels", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#create AccessContextManagerAccessLevels#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#delete AccessContextManagerAccessLevels#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#update AccessContextManagerAccessLevels#update}.
        '''
        value = AccessContextManagerAccessLevelsTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccessLevels")
    def reset_access_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevels", []))

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
    @jsii.member(jsii_name="accessLevels")
    def access_levels(self) -> "AccessContextManagerAccessLevelsAccessLevelsList":
        return typing.cast("AccessContextManagerAccessLevelsAccessLevelsList", jsii.get(self, "accessLevels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AccessContextManagerAccessLevelsTimeoutsOutputReference":
        return typing.cast("AccessContextManagerAccessLevelsTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="accessLevelsInput")
    def access_levels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelsAccessLevels"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelsAccessLevels"]]], jsii.get(self, "accessLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AccessContextManagerAccessLevelsTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AccessContextManagerAccessLevelsTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3be4aebbaf982691512e5b6c78c0d220ad531950b83678c0a727441ba29a924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da7e7aff61159885dd64a37c47da8a78a437e74f54961f8dafef79e7d34c096b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevels",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "title": "title",
        "basic": "basic",
        "custom": "custom",
        "description": "description",
    },
)
class AccessContextManagerAccessLevelsAccessLevels:
    def __init__(
        self,
        *,
        name: builtins.str,
        title: builtins.str,
        basic: typing.Optional[typing.Union["AccessContextManagerAccessLevelsAccessLevelsBasic", typing.Dict[builtins.str, typing.Any]]] = None,
        custom: typing.Optional[typing.Union["AccessContextManagerAccessLevelsAccessLevelsCustom", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Resource name for the Access Level. The short_name component must begin with a letter and only include alphanumeric and '_'. Format: accessPolicies/{policy_id}/accessLevels/{short_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#name AccessContextManagerAccessLevels#name}
        :param title: Human readable title. Must be unique within the Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#title AccessContextManagerAccessLevels#title}
        :param basic: basic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#basic AccessContextManagerAccessLevels#basic}
        :param custom: custom block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#custom AccessContextManagerAccessLevels#custom}
        :param description: Description of the AccessLevel and its use. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#description AccessContextManagerAccessLevels#description}
        '''
        if isinstance(basic, dict):
            basic = AccessContextManagerAccessLevelsAccessLevelsBasic(**basic)
        if isinstance(custom, dict):
            custom = AccessContextManagerAccessLevelsAccessLevelsCustom(**custom)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76bb22e18234df1321f53e57d2458adaf99892cf1e52562e91a8bd07ce51ebe8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument basic", value=basic, expected_type=type_hints["basic"])
            check_type(argname="argument custom", value=custom, expected_type=type_hints["custom"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "title": title,
        }
        if basic is not None:
            self._values["basic"] = basic
        if custom is not None:
            self._values["custom"] = custom
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def name(self) -> builtins.str:
        '''Resource name for the Access Level.

        The short_name component must begin
        with a letter and only include alphanumeric and '_'.
        Format: accessPolicies/{policy_id}/accessLevels/{short_name}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#name AccessContextManagerAccessLevels#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Human readable title. Must be unique within the Policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#title AccessContextManagerAccessLevels#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def basic(
        self,
    ) -> typing.Optional["AccessContextManagerAccessLevelsAccessLevelsBasic"]:
        '''basic block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#basic AccessContextManagerAccessLevels#basic}
        '''
        result = self._values.get("basic")
        return typing.cast(typing.Optional["AccessContextManagerAccessLevelsAccessLevelsBasic"], result)

    @builtins.property
    def custom(
        self,
    ) -> typing.Optional["AccessContextManagerAccessLevelsAccessLevelsCustom"]:
        '''custom block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#custom AccessContextManagerAccessLevels#custom}
        '''
        result = self._values.get("custom")
        return typing.cast(typing.Optional["AccessContextManagerAccessLevelsAccessLevelsCustom"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the AccessLevel and its use. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#description AccessContextManagerAccessLevels#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelsAccessLevels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsBasic",
    jsii_struct_bases=[],
    name_mapping={
        "conditions": "conditions",
        "combining_function": "combiningFunction",
    },
)
class AccessContextManagerAccessLevelsAccessLevelsBasic:
    def __init__(
        self,
        *,
        conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerAccessLevelsAccessLevelsBasicConditions", typing.Dict[builtins.str, typing.Any]]]],
        combining_function: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#conditions AccessContextManagerAccessLevels#conditions}
        :param combining_function: How the conditions list should be combined to determine if a request is granted this AccessLevel. If AND is used, each Condition in conditions must be satisfied for the AccessLevel to be applied. If OR is used, at least one Condition in conditions must be satisfied for the AccessLevel to be applied. Default value: "AND" Possible values: ["AND", "OR"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#combining_function AccessContextManagerAccessLevels#combining_function}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d30a7af8c126611df03d587e1e2ff6bee8e5ad03111e54f69703b2904a487ad)
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument combining_function", value=combining_function, expected_type=type_hints["combining_function"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "conditions": conditions,
        }
        if combining_function is not None:
            self._values["combining_function"] = combining_function

    @builtins.property
    def conditions(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelsAccessLevelsBasicConditions"]]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#conditions AccessContextManagerAccessLevels#conditions}
        '''
        result = self._values.get("conditions")
        assert result is not None, "Required property 'conditions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelsAccessLevelsBasicConditions"]], result)

    @builtins.property
    def combining_function(self) -> typing.Optional[builtins.str]:
        '''How the conditions list should be combined to determine if a request is granted this AccessLevel.

        If AND is used, each Condition in
        conditions must be satisfied for the AccessLevel to be applied. If
        OR is used, at least one Condition in conditions must be satisfied
        for the AccessLevel to be applied. Default value: "AND" Possible values: ["AND", "OR"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#combining_function AccessContextManagerAccessLevels#combining_function}
        '''
        result = self._values.get("combining_function")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelsAccessLevelsBasic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsBasicConditions",
    jsii_struct_bases=[],
    name_mapping={
        "device_policy": "devicePolicy",
        "ip_subnetworks": "ipSubnetworks",
        "members": "members",
        "negate": "negate",
        "regions": "regions",
        "required_access_levels": "requiredAccessLevels",
        "vpc_network_sources": "vpcNetworkSources",
    },
)
class AccessContextManagerAccessLevelsAccessLevelsBasicConditions:
    def __init__(
        self,
        *,
        device_policy: typing.Optional[typing.Union["AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        ip_subnetworks: typing.Optional[typing.Sequence[builtins.str]] = None,
        members: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        required_access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_network_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param device_policy: device_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#device_policy AccessContextManagerAccessLevels#device_policy}
        :param ip_subnetworks: A list of CIDR block IP subnetwork specification. May be IPv4 or IPv6. Note that for a CIDR IP address block, the specified IP address portion must be properly truncated (i.e. all the host bits must be zero) or the input is considered malformed. For example, "192.0.2.0/24" is accepted but "192.0.2.1/24" is not. Similarly, for IPv6, "2001:db8::/32" is accepted whereas "2001:db8::1/32" is not. The originating IP of a request must be in one of the listed subnets in order for this Condition to be true. If empty, all IP addresses are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#ip_subnetworks AccessContextManagerAccessLevels#ip_subnetworks}
        :param members: An allowed list of members (users, service accounts). Using groups is not supported yet. The signed-in user originating the request must be a part of one of the provided members. If not specified, a request may come from any user (logged in/not logged in, not present in any groups, etc.). Formats: 'user:{emailid}', 'serviceAccount:{emailid}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#members AccessContextManagerAccessLevels#members}
        :param negate: Whether to negate the Condition. If true, the Condition becomes a NAND over its non-empty fields, each field must be false for the Condition overall to be satisfied. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#negate AccessContextManagerAccessLevels#negate}
        :param regions: The request must originate from one of the provided countries/regions. Format: A valid ISO 3166-1 alpha-2 code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#regions AccessContextManagerAccessLevels#regions}
        :param required_access_levels: A list of other access levels defined in the same Policy, referenced by resource name. Referencing an AccessLevel which does not exist is an error. All access levels listed must be granted for the Condition to be true. Format: accessPolicies/{policy_id}/accessLevels/{short_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#required_access_levels AccessContextManagerAccessLevels#required_access_levels}
        :param vpc_network_sources: vpc_network_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#vpc_network_sources AccessContextManagerAccessLevels#vpc_network_sources}
        '''
        if isinstance(device_policy, dict):
            device_policy = AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicy(**device_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f0f273e1ce59ed5bf2c29edce4a077d17bf5cbd333780a01d40ebbdb5a1dab1)
            check_type(argname="argument device_policy", value=device_policy, expected_type=type_hints["device_policy"])
            check_type(argname="argument ip_subnetworks", value=ip_subnetworks, expected_type=type_hints["ip_subnetworks"])
            check_type(argname="argument members", value=members, expected_type=type_hints["members"])
            check_type(argname="argument negate", value=negate, expected_type=type_hints["negate"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument required_access_levels", value=required_access_levels, expected_type=type_hints["required_access_levels"])
            check_type(argname="argument vpc_network_sources", value=vpc_network_sources, expected_type=type_hints["vpc_network_sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if device_policy is not None:
            self._values["device_policy"] = device_policy
        if ip_subnetworks is not None:
            self._values["ip_subnetworks"] = ip_subnetworks
        if members is not None:
            self._values["members"] = members
        if negate is not None:
            self._values["negate"] = negate
        if regions is not None:
            self._values["regions"] = regions
        if required_access_levels is not None:
            self._values["required_access_levels"] = required_access_levels
        if vpc_network_sources is not None:
            self._values["vpc_network_sources"] = vpc_network_sources

    @builtins.property
    def device_policy(
        self,
    ) -> typing.Optional["AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicy"]:
        '''device_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#device_policy AccessContextManagerAccessLevels#device_policy}
        '''
        result = self._values.get("device_policy")
        return typing.cast(typing.Optional["AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicy"], result)

    @builtins.property
    def ip_subnetworks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of CIDR block IP subnetwork specification.

        May be IPv4
        or IPv6.
        Note that for a CIDR IP address block, the specified IP address
        portion must be properly truncated (i.e. all the host bits must
        be zero) or the input is considered malformed. For example,
        "192.0.2.0/24" is accepted but "192.0.2.1/24" is not. Similarly,
        for IPv6, "2001:db8::/32" is accepted whereas "2001:db8::1/32"
        is not. The originating IP of a request must be in one of the
        listed subnets in order for this Condition to be true.
        If empty, all IP addresses are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#ip_subnetworks AccessContextManagerAccessLevels#ip_subnetworks}
        '''
        result = self._values.get("ip_subnetworks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def members(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An allowed list of members (users, service accounts). Using groups is not supported yet.

        The signed-in user originating the request must be a part of one
        of the provided members. If not specified, a request may come
        from any user (logged in/not logged in, not present in any
        groups, etc.).
        Formats: 'user:{emailid}', 'serviceAccount:{emailid}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#members AccessContextManagerAccessLevels#members}
        '''
        result = self._values.get("members")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to negate the Condition.

        If true, the Condition becomes
        a NAND over its non-empty fields, each field must be false for
        the Condition overall to be satisfied. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#negate AccessContextManagerAccessLevels#negate}
        '''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The request must originate from one of the provided countries/regions. Format: A valid ISO 3166-1 alpha-2 code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#regions AccessContextManagerAccessLevels#regions}
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def required_access_levels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of other access levels defined in the same Policy, referenced by resource name.

        Referencing an AccessLevel which
        does not exist is an error. All access levels listed must be
        granted for the Condition to be true.
        Format: accessPolicies/{policy_id}/accessLevels/{short_name}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#required_access_levels AccessContextManagerAccessLevels#required_access_levels}
        '''
        result = self._values.get("required_access_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_network_sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources"]]]:
        '''vpc_network_sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#vpc_network_sources AccessContextManagerAccessLevels#vpc_network_sources}
        '''
        result = self._values.get("vpc_network_sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelsAccessLevelsBasicConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_device_management_levels": "allowedDeviceManagementLevels",
        "allowed_encryption_statuses": "allowedEncryptionStatuses",
        "os_constraints": "osConstraints",
        "require_admin_approval": "requireAdminApproval",
        "require_corp_owned": "requireCorpOwned",
        "require_screen_lock": "requireScreenLock",
    },
)
class AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicy:
    def __init__(
        self,
        *,
        allowed_device_management_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_encryption_statuses: typing.Optional[typing.Sequence[builtins.str]] = None,
        os_constraints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        require_admin_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_corp_owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_screen_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_device_management_levels: A list of allowed device management levels. An empty list allows all management levels. Possible values: ["MANAGEMENT_UNSPECIFIED", "NONE", "BASIC", "COMPLETE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#allowed_device_management_levels AccessContextManagerAccessLevels#allowed_device_management_levels}
        :param allowed_encryption_statuses: A list of allowed encryptions statuses. An empty list allows all statuses. Possible values: ["ENCRYPTION_UNSPECIFIED", "ENCRYPTION_UNSUPPORTED", "UNENCRYPTED", "ENCRYPTED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#allowed_encryption_statuses AccessContextManagerAccessLevels#allowed_encryption_statuses}
        :param os_constraints: os_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#os_constraints AccessContextManagerAccessLevels#os_constraints}
        :param require_admin_approval: Whether the device needs to be approved by the customer admin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#require_admin_approval AccessContextManagerAccessLevels#require_admin_approval}
        :param require_corp_owned: Whether the device needs to be corp owned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#require_corp_owned AccessContextManagerAccessLevels#require_corp_owned}
        :param require_screen_lock: Whether or not screenlock is required for the DevicePolicy to be true. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#require_screen_lock AccessContextManagerAccessLevels#require_screen_lock}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35f47594524f45e68da05fcf92ccd6a755368a88462b46af8611cbf192666d17)
            check_type(argname="argument allowed_device_management_levels", value=allowed_device_management_levels, expected_type=type_hints["allowed_device_management_levels"])
            check_type(argname="argument allowed_encryption_statuses", value=allowed_encryption_statuses, expected_type=type_hints["allowed_encryption_statuses"])
            check_type(argname="argument os_constraints", value=os_constraints, expected_type=type_hints["os_constraints"])
            check_type(argname="argument require_admin_approval", value=require_admin_approval, expected_type=type_hints["require_admin_approval"])
            check_type(argname="argument require_corp_owned", value=require_corp_owned, expected_type=type_hints["require_corp_owned"])
            check_type(argname="argument require_screen_lock", value=require_screen_lock, expected_type=type_hints["require_screen_lock"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_device_management_levels is not None:
            self._values["allowed_device_management_levels"] = allowed_device_management_levels
        if allowed_encryption_statuses is not None:
            self._values["allowed_encryption_statuses"] = allowed_encryption_statuses
        if os_constraints is not None:
            self._values["os_constraints"] = os_constraints
        if require_admin_approval is not None:
            self._values["require_admin_approval"] = require_admin_approval
        if require_corp_owned is not None:
            self._values["require_corp_owned"] = require_corp_owned
        if require_screen_lock is not None:
            self._values["require_screen_lock"] = require_screen_lock

    @builtins.property
    def allowed_device_management_levels(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of allowed device management levels. An empty list allows all management levels. Possible values: ["MANAGEMENT_UNSPECIFIED", "NONE", "BASIC", "COMPLETE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#allowed_device_management_levels AccessContextManagerAccessLevels#allowed_device_management_levels}
        '''
        result = self._values.get("allowed_device_management_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_encryption_statuses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of allowed encryptions statuses. An empty list allows all statuses. Possible values: ["ENCRYPTION_UNSPECIFIED", "ENCRYPTION_UNSUPPORTED", "UNENCRYPTED", "ENCRYPTED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#allowed_encryption_statuses AccessContextManagerAccessLevels#allowed_encryption_statuses}
        '''
        result = self._values.get("allowed_encryption_statuses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def os_constraints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints"]]]:
        '''os_constraints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#os_constraints AccessContextManagerAccessLevels#os_constraints}
        '''
        result = self._values.get("os_constraints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints"]]], result)

    @builtins.property
    def require_admin_approval(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the device needs to be approved by the customer admin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#require_admin_approval AccessContextManagerAccessLevels#require_admin_approval}
        '''
        result = self._values.get("require_admin_approval")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_corp_owned(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the device needs to be corp owned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#require_corp_owned AccessContextManagerAccessLevels#require_corp_owned}
        '''
        result = self._values.get("require_corp_owned")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_screen_lock(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not screenlock is required for the DevicePolicy to be true. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#require_screen_lock AccessContextManagerAccessLevels#require_screen_lock}
        '''
        result = self._values.get("require_screen_lock")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints",
    jsii_struct_bases=[],
    name_mapping={"os_type": "osType", "minimum_version": "minimumVersion"},
)
class AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints:
    def __init__(
        self,
        *,
        os_type: builtins.str,
        minimum_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os_type: The operating system type of the device. Possible values: ["OS_UNSPECIFIED", "DESKTOP_MAC", "DESKTOP_WINDOWS", "DESKTOP_LINUX", "DESKTOP_CHROME_OS", "ANDROID", "IOS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#os_type AccessContextManagerAccessLevels#os_type}
        :param minimum_version: The minimum allowed OS version. If not set, any version of this OS satisfies the constraint. Format: "major.minor.patch" such as "10.5.301", "9.2.1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#minimum_version AccessContextManagerAccessLevels#minimum_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de33b07e8e0f2d86321cb3831777e88e67abe351a28240496fdb19c917ded34)
            check_type(argname="argument os_type", value=os_type, expected_type=type_hints["os_type"])
            check_type(argname="argument minimum_version", value=minimum_version, expected_type=type_hints["minimum_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "os_type": os_type,
        }
        if minimum_version is not None:
            self._values["minimum_version"] = minimum_version

    @builtins.property
    def os_type(self) -> builtins.str:
        '''The operating system type of the device. Possible values: ["OS_UNSPECIFIED", "DESKTOP_MAC", "DESKTOP_WINDOWS", "DESKTOP_LINUX", "DESKTOP_CHROME_OS", "ANDROID", "IOS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#os_type AccessContextManagerAccessLevels#os_type}
        '''
        result = self._values.get("os_type")
        assert result is not None, "Required property 'os_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def minimum_version(self) -> typing.Optional[builtins.str]:
        '''The minimum allowed OS version.

        If not set, any version
        of this OS satisfies the constraint.
        Format: "major.minor.patch" such as "10.5.301", "9.2.1".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#minimum_version AccessContextManagerAccessLevels#minimum_version}
        '''
        result = self._values.get("minimum_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3ec9f5c339f85c1027c14e30c85917a4fbdbb87c0d6883e9e5b8a7ed62813be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c76683a09f297a4bdbc1dedeafaa4b48f75a4fafb0384ee5e20e32a65f7b2e5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c730bbf49a045c269db81fb285dd853f31d0717c848a95f8763d5cd982644637)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cfe5e9df109049d89da80f846b25a39b6bcf7c28b1be1b0d0b58ce289f66a20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ecaf59eeef42f2c1a1db6d8d6bd5d87fa8ca807cce7c59e1ac06e6f4cf1b60a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ebb12333bf5b2835f15c75953de10bf41dc33129f185caf562f8b078098aa7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a734af6cf91825bc43ee74e52da1a878bd92cb4494630f1514110fb4a67abf2c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMinimumVersion")
    def reset_minimum_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumVersion", []))

    @builtins.property
    @jsii.member(jsii_name="minimumVersionInput")
    def minimum_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="osTypeInput")
    def os_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumVersion")
    def minimum_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumVersion"))

    @minimum_version.setter
    def minimum_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7cfdf33bae963f9f712861c3618db28fb0ffb5e1bfd129f7c30e4b4cd83fae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @os_type.setter
    def os_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d256bee017a458e768b3142c3bc7449bc40b65cd5b10235d5f4ee8ec78b7e40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cda12230b2246bb8eba488b20c18b73f6685a96e97e65d058955af9b6a9af541)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38198c55564dc81e5e427d008e31eef21c9d45f4ca2ec63439595c6ad60674f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOsConstraints")
    def put_os_constraints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73d3cdd206dde21d0e9dcfdda494fee66b7586395cfe6eca4a22506d927fd18a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOsConstraints", [value]))

    @jsii.member(jsii_name="resetAllowedDeviceManagementLevels")
    def reset_allowed_device_management_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedDeviceManagementLevels", []))

    @jsii.member(jsii_name="resetAllowedEncryptionStatuses")
    def reset_allowed_encryption_statuses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedEncryptionStatuses", []))

    @jsii.member(jsii_name="resetOsConstraints")
    def reset_os_constraints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsConstraints", []))

    @jsii.member(jsii_name="resetRequireAdminApproval")
    def reset_require_admin_approval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireAdminApproval", []))

    @jsii.member(jsii_name="resetRequireCorpOwned")
    def reset_require_corp_owned(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireCorpOwned", []))

    @jsii.member(jsii_name="resetRequireScreenLock")
    def reset_require_screen_lock(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireScreenLock", []))

    @builtins.property
    @jsii.member(jsii_name="osConstraints")
    def os_constraints(
        self,
    ) -> AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraintsList:
        return typing.cast(AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraintsList, jsii.get(self, "osConstraints"))

    @builtins.property
    @jsii.member(jsii_name="allowedDeviceManagementLevelsInput")
    def allowed_device_management_levels_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedDeviceManagementLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedEncryptionStatusesInput")
    def allowed_encryption_statuses_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedEncryptionStatusesInput"))

    @builtins.property
    @jsii.member(jsii_name="osConstraintsInput")
    def os_constraints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints]]], jsii.get(self, "osConstraintsInput"))

    @builtins.property
    @jsii.member(jsii_name="requireAdminApprovalInput")
    def require_admin_approval_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireAdminApprovalInput"))

    @builtins.property
    @jsii.member(jsii_name="requireCorpOwnedInput")
    def require_corp_owned_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireCorpOwnedInput"))

    @builtins.property
    @jsii.member(jsii_name="requireScreenLockInput")
    def require_screen_lock_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireScreenLockInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedDeviceManagementLevels")
    def allowed_device_management_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedDeviceManagementLevels"))

    @allowed_device_management_levels.setter
    def allowed_device_management_levels(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7fc11e679a6d68b0b037e7e0e7421cba009c3c92b9fe139eb4e8696393c54e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedDeviceManagementLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedEncryptionStatuses")
    def allowed_encryption_statuses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedEncryptionStatuses"))

    @allowed_encryption_statuses.setter
    def allowed_encryption_statuses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__747c91de5454cc507ba59fa1302149540e3173ee4eae47349d019269f940c509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedEncryptionStatuses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireAdminApproval")
    def require_admin_approval(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireAdminApproval"))

    @require_admin_approval.setter
    def require_admin_approval(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c84a892fc1d197a344110f4184e54edc75a5d983bbd0926ea0debcacec369bab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireAdminApproval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireCorpOwned")
    def require_corp_owned(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireCorpOwned"))

    @require_corp_owned.setter
    def require_corp_owned(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db4b1070ecee7fe7a0f7461d8f2f630fead91d9d97c223a7c29786d86d924c7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireCorpOwned", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireScreenLock")
    def require_screen_lock(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireScreenLock"))

    @require_screen_lock.setter
    def require_screen_lock(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__370dd1c0b921eb2b5b984a9bcfe3e4a36351659be3e195f7c6cf6b5a4dbc875f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireScreenLock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicy]:
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9849113b5da926c00b672e40d36ad689cf74ff7bc1e2291e718c326b3df11d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerAccessLevelsAccessLevelsBasicConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsBasicConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6bc73d226e88d96890ecc2629bc93caa9ce437c51a694793cf6fb3e92cf4e7d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87d7c5858f31d5a0a857602b5058e0e5e52c93c8cd2dab87296cbbceba3d6890)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerAccessLevelsAccessLevelsBasicConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85afa213eb9f09e05f18db9cd0ac91679d3ae8053e28a356446d710a95d2654c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8aae6d1579d904eee70e06df567033d263c6712e5f97d9b52b33a96a20451038)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0de52c4f73444c679744c5e0bc10d3299042c1c506eca7a8ca7144be30cbbb36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevelsBasicConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevelsBasicConditions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevelsBasicConditions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d680163a54ebaf8cab2bd9f62bf9a0f6a461490ddb8d70ddcf9df18c589e32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerAccessLevelsAccessLevelsBasicConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsBasicConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9541b8410c5c2f8553c87be73d425844db2928c4055b90da348aa5b7ba4637d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDevicePolicy")
    def put_device_policy(
        self,
        *,
        allowed_device_management_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_encryption_statuses: typing.Optional[typing.Sequence[builtins.str]] = None,
        os_constraints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints, typing.Dict[builtins.str, typing.Any]]]]] = None,
        require_admin_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_corp_owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_screen_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_device_management_levels: A list of allowed device management levels. An empty list allows all management levels. Possible values: ["MANAGEMENT_UNSPECIFIED", "NONE", "BASIC", "COMPLETE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#allowed_device_management_levels AccessContextManagerAccessLevels#allowed_device_management_levels}
        :param allowed_encryption_statuses: A list of allowed encryptions statuses. An empty list allows all statuses. Possible values: ["ENCRYPTION_UNSPECIFIED", "ENCRYPTION_UNSUPPORTED", "UNENCRYPTED", "ENCRYPTED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#allowed_encryption_statuses AccessContextManagerAccessLevels#allowed_encryption_statuses}
        :param os_constraints: os_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#os_constraints AccessContextManagerAccessLevels#os_constraints}
        :param require_admin_approval: Whether the device needs to be approved by the customer admin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#require_admin_approval AccessContextManagerAccessLevels#require_admin_approval}
        :param require_corp_owned: Whether the device needs to be corp owned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#require_corp_owned AccessContextManagerAccessLevels#require_corp_owned}
        :param require_screen_lock: Whether or not screenlock is required for the DevicePolicy to be true. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#require_screen_lock AccessContextManagerAccessLevels#require_screen_lock}
        '''
        value = AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicy(
            allowed_device_management_levels=allowed_device_management_levels,
            allowed_encryption_statuses=allowed_encryption_statuses,
            os_constraints=os_constraints,
            require_admin_approval=require_admin_approval,
            require_corp_owned=require_corp_owned,
            require_screen_lock=require_screen_lock,
        )

        return typing.cast(None, jsii.invoke(self, "putDevicePolicy", [value]))

    @jsii.member(jsii_name="putVpcNetworkSources")
    def put_vpc_network_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b15527390b4b17751f6549343f771cb4cbc1c0ee9f35ca481b376cba6361b54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVpcNetworkSources", [value]))

    @jsii.member(jsii_name="resetDevicePolicy")
    def reset_device_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDevicePolicy", []))

    @jsii.member(jsii_name="resetIpSubnetworks")
    def reset_ip_subnetworks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpSubnetworks", []))

    @jsii.member(jsii_name="resetMembers")
    def reset_members(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMembers", []))

    @jsii.member(jsii_name="resetNegate")
    def reset_negate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegate", []))

    @jsii.member(jsii_name="resetRegions")
    def reset_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegions", []))

    @jsii.member(jsii_name="resetRequiredAccessLevels")
    def reset_required_access_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredAccessLevels", []))

    @jsii.member(jsii_name="resetVpcNetworkSources")
    def reset_vpc_network_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcNetworkSources", []))

    @builtins.property
    @jsii.member(jsii_name="devicePolicy")
    def device_policy(
        self,
    ) -> AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOutputReference:
        return typing.cast(AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOutputReference, jsii.get(self, "devicePolicy"))

    @builtins.property
    @jsii.member(jsii_name="vpcNetworkSources")
    def vpc_network_sources(
        self,
    ) -> "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesList":
        return typing.cast("AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesList", jsii.get(self, "vpcNetworkSources"))

    @builtins.property
    @jsii.member(jsii_name="devicePolicyInput")
    def device_policy_input(
        self,
    ) -> typing.Optional[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicy]:
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicy], jsii.get(self, "devicePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="ipSubnetworksInput")
    def ip_subnetworks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipSubnetworksInput"))

    @builtins.property
    @jsii.member(jsii_name="membersInput")
    def members_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "membersInput"))

    @builtins.property
    @jsii.member(jsii_name="negateInput")
    def negate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateInput"))

    @builtins.property
    @jsii.member(jsii_name="regionsInput")
    def regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "regionsInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredAccessLevelsInput")
    def required_access_levels_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "requiredAccessLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcNetworkSourcesInput")
    def vpc_network_sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources"]]], jsii.get(self, "vpcNetworkSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="ipSubnetworks")
    def ip_subnetworks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipSubnetworks"))

    @ip_subnetworks.setter
    def ip_subnetworks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d46859c9dcd8f70729ffe1bf7a6e7d94b4226a8bfe755e7b605a33677b8130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipSubnetworks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="members")
    def members(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "members"))

    @members.setter
    def members(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdde5178ab0bec4867e817543b210f037fb3bf14172997833c10a4d2ebbd5800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "members", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negate")
    def negate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negate"))

    @negate.setter
    def negate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac5c73fded29be391bb3635a7e6bc0662f3f95d33055254bf321b4cf623a3ff9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regions")
    def regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "regions"))

    @regions.setter
    def regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2031b5375c13563161cd383ffff12caa2e17d44eaa523a74a4d1f79b378913dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredAccessLevels")
    def required_access_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requiredAccessLevels"))

    @required_access_levels.setter
    def required_access_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6644383682af3908d6fd6305feb1b222ba54aff6ee6f7130e346f7795809d615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredAccessLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsAccessLevelsBasicConditions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsAccessLevelsBasicConditions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsAccessLevelsBasicConditions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bacd4cd0e9b4a6df9715fda4813f7438aa47b7428f5609924ccebec80363cac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources",
    jsii_struct_bases=[],
    name_mapping={"vpc_subnetwork": "vpcSubnetwork"},
)
class AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources:
    def __init__(
        self,
        *,
        vpc_subnetwork: typing.Optional[typing.Union["AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetwork", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param vpc_subnetwork: vpc_subnetwork block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#vpc_subnetwork AccessContextManagerAccessLevels#vpc_subnetwork}
        '''
        if isinstance(vpc_subnetwork, dict):
            vpc_subnetwork = AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetwork(**vpc_subnetwork)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10104a977879d1ae242a69099f1bfeb4846353532443fff8f2e29e864032bfee)
            check_type(argname="argument vpc_subnetwork", value=vpc_subnetwork, expected_type=type_hints["vpc_subnetwork"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if vpc_subnetwork is not None:
            self._values["vpc_subnetwork"] = vpc_subnetwork

    @builtins.property
    def vpc_subnetwork(
        self,
    ) -> typing.Optional["AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetwork"]:
        '''vpc_subnetwork block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#vpc_subnetwork AccessContextManagerAccessLevels#vpc_subnetwork}
        '''
        result = self._values.get("vpc_subnetwork")
        return typing.cast(typing.Optional["AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetwork"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f8ef188d2f243afaf226a986dc4ba2e9a9232b8e7de4bd03fa8c0c466a11055)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c06456717d6d9e254fdae7382b90413d2dc9e69eee04225f2ea4b47f1b3661a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81884678d8a0d6beb41d0e4e94fa6d478de5bba0b32e22e1af1e634d5c75a76e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b889887d6cd041199b9fd076208b0786beb4ff8c337558104e389a6cf573038)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09a3d78a5c11384cf664f6e544ab4334ade7a9803c75edd7b5cfba81f76caeb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4224f1cf3e7bd860f9bd6872325e97036364d4c5a769e00e377668f30afef716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cb17d476184f88bac57f8821b612bf46108a3052484e4a3a2299bf50e6ce9fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putVpcSubnetwork")
    def put_vpc_subnetwork(
        self,
        *,
        network: builtins.str,
        vpc_ip_subnetworks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param network: Required. Network name to be allowed by this Access Level. Networks of foreign organizations requires 'compute.network.get' permission to be granted to caller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#network AccessContextManagerAccessLevels#network}
        :param vpc_ip_subnetworks: CIDR block IP subnetwork specification. Must be IPv4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#vpc_ip_subnetworks AccessContextManagerAccessLevels#vpc_ip_subnetworks}
        '''
        value = AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetwork(
            network=network, vpc_ip_subnetworks=vpc_ip_subnetworks
        )

        return typing.cast(None, jsii.invoke(self, "putVpcSubnetwork", [value]))

    @jsii.member(jsii_name="resetVpcSubnetwork")
    def reset_vpc_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcSubnetwork", []))

    @builtins.property
    @jsii.member(jsii_name="vpcSubnetwork")
    def vpc_subnetwork(
        self,
    ) -> "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetworkOutputReference":
        return typing.cast("AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetworkOutputReference", jsii.get(self, "vpcSubnetwork"))

    @builtins.property
    @jsii.member(jsii_name="vpcSubnetworkInput")
    def vpc_subnetwork_input(
        self,
    ) -> typing.Optional["AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetwork"]:
        return typing.cast(typing.Optional["AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetwork"], jsii.get(self, "vpcSubnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58edcc69fefe594b9a36138727383bed98e0401fe228de4f0d513fc8d1ab64c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetwork",
    jsii_struct_bases=[],
    name_mapping={"network": "network", "vpc_ip_subnetworks": "vpcIpSubnetworks"},
)
class AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetwork:
    def __init__(
        self,
        *,
        network: builtins.str,
        vpc_ip_subnetworks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param network: Required. Network name to be allowed by this Access Level. Networks of foreign organizations requires 'compute.network.get' permission to be granted to caller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#network AccessContextManagerAccessLevels#network}
        :param vpc_ip_subnetworks: CIDR block IP subnetwork specification. Must be IPv4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#vpc_ip_subnetworks AccessContextManagerAccessLevels#vpc_ip_subnetworks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aa10cb6a1c266e6ba2d382226180e0cf7498acd40c963611444242745b13474)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument vpc_ip_subnetworks", value=vpc_ip_subnetworks, expected_type=type_hints["vpc_ip_subnetworks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network": network,
        }
        if vpc_ip_subnetworks is not None:
            self._values["vpc_ip_subnetworks"] = vpc_ip_subnetworks

    @builtins.property
    def network(self) -> builtins.str:
        '''Required.

        Network name to be allowed by this Access Level. Networks of foreign organizations requires 'compute.network.get' permission to be granted to caller.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#network AccessContextManagerAccessLevels#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_ip_subnetworks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''CIDR block IP subnetwork specification. Must be IPv4.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#vpc_ip_subnetworks AccessContextManagerAccessLevels#vpc_ip_subnetworks}
        '''
        result = self._values.get("vpc_ip_subnetworks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c02907181326c510620bb9212c34d3b119a1ea46aa3e2e6ba47f55b4f83a1eed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetVpcIpSubnetworks")
    def reset_vpc_ip_subnetworks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcIpSubnetworks", []))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIpSubnetworksInput")
    def vpc_ip_subnetworks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "vpcIpSubnetworksInput"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13fb3399b349558423bc719126a8688aea05495d136270f9b0c3ee9fe4d6934c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcIpSubnetworks")
    def vpc_ip_subnetworks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vpcIpSubnetworks"))

    @vpc_ip_subnetworks.setter
    def vpc_ip_subnetworks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fccc7d541cb9408448e5df1cbfeb30f8a1ff05432c1b07c464dec758221288c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcIpSubnetworks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetwork]:
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b2874b929c161fcb07e98b7f4ee343f328210fdb7f7d6f7486de6bfe6c42b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerAccessLevelsAccessLevelsBasicOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsBasicOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73bc58e9f83cef46b17315219517f249f91c6e0691e74d27f1b67844459f18b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelsAccessLevelsBasicConditions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0218e3370740d854dff41fde8d5e8e0312d78c76194378c03355a21c2ca66ddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="resetCombiningFunction")
    def reset_combining_function(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCombiningFunction", []))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(
        self,
    ) -> AccessContextManagerAccessLevelsAccessLevelsBasicConditionsList:
        return typing.cast(AccessContextManagerAccessLevelsAccessLevelsBasicConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="combiningFunctionInput")
    def combining_function_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "combiningFunctionInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevelsBasicConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevelsBasicConditions]]], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="combiningFunction")
    def combining_function(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "combiningFunction"))

    @combining_function.setter
    def combining_function(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49eb910740cd5cbd3d625fae65e9221d0552b4e148d2d21669008362fa360b8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "combiningFunction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerAccessLevelsAccessLevelsBasic]:
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelsAccessLevelsBasic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerAccessLevelsAccessLevelsBasic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b608425b07eb2bc34fde185593388169db08497075374f2867d1e7398243737e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsCustom",
    jsii_struct_bases=[],
    name_mapping={"expr": "expr"},
)
class AccessContextManagerAccessLevelsAccessLevelsCustom:
    def __init__(
        self,
        *,
        expr: typing.Union["AccessContextManagerAccessLevelsAccessLevelsCustomExpr", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param expr: expr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#expr AccessContextManagerAccessLevels#expr}
        '''
        if isinstance(expr, dict):
            expr = AccessContextManagerAccessLevelsAccessLevelsCustomExpr(**expr)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e09b6e9a59e5608aec4892a062a1c2de42ca2d8cb10e401ad7dfbf0a1c70a7c0)
            check_type(argname="argument expr", value=expr, expected_type=type_hints["expr"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expr": expr,
        }

    @builtins.property
    def expr(self) -> "AccessContextManagerAccessLevelsAccessLevelsCustomExpr":
        '''expr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#expr AccessContextManagerAccessLevels#expr}
        '''
        result = self._values.get("expr")
        assert result is not None, "Required property 'expr' is missing"
        return typing.cast("AccessContextManagerAccessLevelsAccessLevelsCustomExpr", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelsAccessLevelsCustom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsCustomExpr",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class AccessContextManagerAccessLevelsAccessLevelsCustomExpr:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#expression AccessContextManagerAccessLevels#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#description AccessContextManagerAccessLevels#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#location AccessContextManagerAccessLevels#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#title AccessContextManagerAccessLevels#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ccc443f46f9d46dc7ea12db892a67ba60ca520645c4824dd6ae0a05919d4bb4)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }
        if description is not None:
            self._values["description"] = description
        if location is not None:
            self._values["location"] = location
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def expression(self) -> builtins.str:
        '''Textual representation of an expression in Common Expression Language syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#expression AccessContextManagerAccessLevels#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#description AccessContextManagerAccessLevels#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#location AccessContextManagerAccessLevels#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#title AccessContextManagerAccessLevels#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelsAccessLevelsCustomExpr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerAccessLevelsAccessLevelsCustomExprOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsCustomExprOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__419aa1b0025c7209aaaf35f8ee6baef3dc49738986a323f3d54658b69c226f42)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__951a0b802411d5a56fc4ebdb4f80f83bdda5a744c39b9ca9a6f95ffcaa3bd246)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f76cb595c5f0be001b0f5dc8cc5f8bf3ee9beab567118fd68165dd203992963e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd0c23329a408045792a9d7f7ea6716cb9a170f2e3215834a74dec52bcedb5ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdc435b1a4659bf3bf3172a610182a4d58340b0e9ed7aafa9eefcf81c2b59567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerAccessLevelsAccessLevelsCustomExpr]:
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelsAccessLevelsCustomExpr], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerAccessLevelsAccessLevelsCustomExpr],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__596f0352373acc9df7f459a4daadbc23dbe6590e062b7f1a1c6e6a69634e9cce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerAccessLevelsAccessLevelsCustomOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsCustomOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__784fa797e1226fd615839dcf749b7f8d3f2b58b551ee3b19d213623ced217769)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExpr")
    def put_expr(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#expression AccessContextManagerAccessLevels#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#description AccessContextManagerAccessLevels#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#location AccessContextManagerAccessLevels#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#title AccessContextManagerAccessLevels#title}
        '''
        value = AccessContextManagerAccessLevelsAccessLevelsCustomExpr(
            expression=expression,
            description=description,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putExpr", [value]))

    @builtins.property
    @jsii.member(jsii_name="expr")
    def expr(
        self,
    ) -> AccessContextManagerAccessLevelsAccessLevelsCustomExprOutputReference:
        return typing.cast(AccessContextManagerAccessLevelsAccessLevelsCustomExprOutputReference, jsii.get(self, "expr"))

    @builtins.property
    @jsii.member(jsii_name="exprInput")
    def expr_input(
        self,
    ) -> typing.Optional[AccessContextManagerAccessLevelsAccessLevelsCustomExpr]:
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelsAccessLevelsCustomExpr], jsii.get(self, "exprInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerAccessLevelsAccessLevelsCustom]:
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelsAccessLevelsCustom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerAccessLevelsAccessLevelsCustom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a50f5dd8ce462f0f545043460487a946b7800897141005ed99b644f7438d7ccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerAccessLevelsAccessLevelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__128a614cb8390b6512e770e90fd2206abeb64c1178b8849f51825490083ed38e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerAccessLevelsAccessLevelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__280b84c277b4fa8cb32d1dc33b3578d960646c3368a87843cd8dff060544467d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerAccessLevelsAccessLevelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68de474fd9c982bc22a98df104064ccfa370319918f1d866c0a918bcc6f34a3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f48c3838e076269aca28286494fb55d9d006af748b9e8847a4aa92d5a2ceed47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aff40d6ca7205cf5f1a45d532f1de5f41e6a9e92366c0d1f03f4e54d08d7b7e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf190819f31da2d105c8648937353a0ec1cb38640f0808211afe2859ff3bffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerAccessLevelsAccessLevelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsAccessLevelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d343e5d233ff910a71d5ccba6f348d9eb6d9b9ad8457c29903d264a9c62bf35f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBasic")
    def put_basic(
        self,
        *,
        conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelsAccessLevelsBasicConditions, typing.Dict[builtins.str, typing.Any]]]],
        combining_function: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#conditions AccessContextManagerAccessLevels#conditions}
        :param combining_function: How the conditions list should be combined to determine if a request is granted this AccessLevel. If AND is used, each Condition in conditions must be satisfied for the AccessLevel to be applied. If OR is used, at least one Condition in conditions must be satisfied for the AccessLevel to be applied. Default value: "AND" Possible values: ["AND", "OR"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#combining_function AccessContextManagerAccessLevels#combining_function}
        '''
        value = AccessContextManagerAccessLevelsAccessLevelsBasic(
            conditions=conditions, combining_function=combining_function
        )

        return typing.cast(None, jsii.invoke(self, "putBasic", [value]))

    @jsii.member(jsii_name="putCustom")
    def put_custom(
        self,
        *,
        expr: typing.Union[AccessContextManagerAccessLevelsAccessLevelsCustomExpr, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param expr: expr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#expr AccessContextManagerAccessLevels#expr}
        '''
        value = AccessContextManagerAccessLevelsAccessLevelsCustom(expr=expr)

        return typing.cast(None, jsii.invoke(self, "putCustom", [value]))

    @jsii.member(jsii_name="resetBasic")
    def reset_basic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasic", []))

    @jsii.member(jsii_name="resetCustom")
    def reset_custom(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustom", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="basic")
    def basic(self) -> AccessContextManagerAccessLevelsAccessLevelsBasicOutputReference:
        return typing.cast(AccessContextManagerAccessLevelsAccessLevelsBasicOutputReference, jsii.get(self, "basic"))

    @builtins.property
    @jsii.member(jsii_name="custom")
    def custom(
        self,
    ) -> AccessContextManagerAccessLevelsAccessLevelsCustomOutputReference:
        return typing.cast(AccessContextManagerAccessLevelsAccessLevelsCustomOutputReference, jsii.get(self, "custom"))

    @builtins.property
    @jsii.member(jsii_name="basicInput")
    def basic_input(
        self,
    ) -> typing.Optional[AccessContextManagerAccessLevelsAccessLevelsBasic]:
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelsAccessLevelsBasic], jsii.get(self, "basicInput"))

    @builtins.property
    @jsii.member(jsii_name="customInput")
    def custom_input(
        self,
    ) -> typing.Optional[AccessContextManagerAccessLevelsAccessLevelsCustom]:
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelsAccessLevelsCustom], jsii.get(self, "customInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec0f1cea5a596db53a59410413427f77d161a08458f0e9bd1a4b6546543faf15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a2e5dc5d6c6740ef7b0099b5ab6fe737d9596c2b796e21c7f98c484df710d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4422cf227bc28ca26132f96013b5ea213a7dbdfa82c1fdbc3cbf325c5a0fa639)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsAccessLevels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsAccessLevels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsAccessLevels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f943b71ccc6ddcf21c380ed4283ccea188bcf22935ab7ccf15b29e0c4e70fd1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsConfig",
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
        "access_levels": "accessLevels",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class AccessContextManagerAccessLevelsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        access_levels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelsAccessLevels, typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerAccessLevelsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param parent: The AccessPolicy this AccessLevel lives in. Format: accessPolicies/{policy_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#parent AccessContextManagerAccessLevels#parent}
        :param access_levels: access_levels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#access_levels AccessContextManagerAccessLevels#access_levels}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#id AccessContextManagerAccessLevels#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#timeouts AccessContextManagerAccessLevels#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = AccessContextManagerAccessLevelsTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718af0acdf5d81d4ef81220c2b9b2796d6d04cfdf9abb0fa10ddbc16b95ea21c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument access_levels", value=access_levels, expected_type=type_hints["access_levels"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parent": parent,
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
        if access_levels is not None:
            self._values["access_levels"] = access_levels
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
        '''The AccessPolicy this AccessLevel lives in. Format: accessPolicies/{policy_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#parent AccessContextManagerAccessLevels#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_levels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevels]]]:
        '''access_levels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#access_levels AccessContextManagerAccessLevels#access_levels}
        '''
        result = self._values.get("access_levels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevels]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#id AccessContextManagerAccessLevels#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AccessContextManagerAccessLevelsTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#timeouts AccessContextManagerAccessLevels#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AccessContextManagerAccessLevelsTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class AccessContextManagerAccessLevelsTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#create AccessContextManagerAccessLevels#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#delete AccessContextManagerAccessLevels#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#update AccessContextManagerAccessLevels#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71c6ab78e15d7c4f9044833a9f3b29f3015205c4b6294e7df834a2dcc0c479bc)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#create AccessContextManagerAccessLevels#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#delete AccessContextManagerAccessLevels#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_levels#update AccessContextManagerAccessLevels#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelsTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerAccessLevelsTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevels.AccessContextManagerAccessLevelsTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78f9b4d15ec95197b2d9dd218428f8b04bf7c1f5f30cd5922561055952b6577c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f86e7bfaaa3d1d80ebc97e151ae753c955c3266886ed44ae9d357fb85762c6ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03292aa98428d6d3e380c87327951838ae30cbd2a01b5fb58a7e546a3cf05e91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a181e1ed310f8b4f3fa6bfef627d3416757e9ebec5a5d35a13877d4db3521285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eafddab90310441182345669242a168ef8065309f54f55975e8750b1581000e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AccessContextManagerAccessLevels",
    "AccessContextManagerAccessLevelsAccessLevels",
    "AccessContextManagerAccessLevelsAccessLevelsBasic",
    "AccessContextManagerAccessLevelsAccessLevelsBasicConditions",
    "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicy",
    "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints",
    "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraintsList",
    "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraintsOutputReference",
    "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOutputReference",
    "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsList",
    "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsOutputReference",
    "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources",
    "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesList",
    "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesOutputReference",
    "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetwork",
    "AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetworkOutputReference",
    "AccessContextManagerAccessLevelsAccessLevelsBasicOutputReference",
    "AccessContextManagerAccessLevelsAccessLevelsCustom",
    "AccessContextManagerAccessLevelsAccessLevelsCustomExpr",
    "AccessContextManagerAccessLevelsAccessLevelsCustomExprOutputReference",
    "AccessContextManagerAccessLevelsAccessLevelsCustomOutputReference",
    "AccessContextManagerAccessLevelsAccessLevelsList",
    "AccessContextManagerAccessLevelsAccessLevelsOutputReference",
    "AccessContextManagerAccessLevelsConfig",
    "AccessContextManagerAccessLevelsTimeouts",
    "AccessContextManagerAccessLevelsTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__99b3a3db400c571aa4c62cdba24572c96f8ca4ecba925f247dde68e20dc25d16(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    parent: builtins.str,
    access_levels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelsAccessLevels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerAccessLevelsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__0e6bbe6aaf11713dad54491c0ac7b3c12d5abd3599e007caa410723b1a462a72(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73bdc277ea7d716f5e8ad60c155e51d4389e24ac2c043eb1a71048aa5d92b6a1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelsAccessLevels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3be4aebbaf982691512e5b6c78c0d220ad531950b83678c0a727441ba29a924(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da7e7aff61159885dd64a37c47da8a78a437e74f54961f8dafef79e7d34c096b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76bb22e18234df1321f53e57d2458adaf99892cf1e52562e91a8bd07ce51ebe8(
    *,
    name: builtins.str,
    title: builtins.str,
    basic: typing.Optional[typing.Union[AccessContextManagerAccessLevelsAccessLevelsBasic, typing.Dict[builtins.str, typing.Any]]] = None,
    custom: typing.Optional[typing.Union[AccessContextManagerAccessLevelsAccessLevelsCustom, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d30a7af8c126611df03d587e1e2ff6bee8e5ad03111e54f69703b2904a487ad(
    *,
    conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelsAccessLevelsBasicConditions, typing.Dict[builtins.str, typing.Any]]]],
    combining_function: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f0f273e1ce59ed5bf2c29edce4a077d17bf5cbd333780a01d40ebbdb5a1dab1(
    *,
    device_policy: typing.Optional[typing.Union[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    ip_subnetworks: typing.Optional[typing.Sequence[builtins.str]] = None,
    members: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    required_access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_network_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f47594524f45e68da05fcf92ccd6a755368a88462b46af8611cbf192666d17(
    *,
    allowed_device_management_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_encryption_statuses: typing.Optional[typing.Sequence[builtins.str]] = None,
    os_constraints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    require_admin_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_corp_owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_screen_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de33b07e8e0f2d86321cb3831777e88e67abe351a28240496fdb19c917ded34(
    *,
    os_type: builtins.str,
    minimum_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ec9f5c339f85c1027c14e30c85917a4fbdbb87c0d6883e9e5b8a7ed62813be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c76683a09f297a4bdbc1dedeafaa4b48f75a4fafb0384ee5e20e32a65f7b2e5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c730bbf49a045c269db81fb285dd853f31d0717c848a95f8763d5cd982644637(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cfe5e9df109049d89da80f846b25a39b6bcf7c28b1be1b0d0b58ce289f66a20(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ecaf59eeef42f2c1a1db6d8d6bd5d87fa8ca807cce7c59e1ac06e6f4cf1b60a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ebb12333bf5b2835f15c75953de10bf41dc33129f185caf562f8b078098aa7d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a734af6cf91825bc43ee74e52da1a878bd92cb4494630f1514110fb4a67abf2c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7cfdf33bae963f9f712861c3618db28fb0ffb5e1bfd129f7c30e4b4cd83fae6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d256bee017a458e768b3142c3bc7449bc40b65cd5b10235d5f4ee8ec78b7e40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda12230b2246bb8eba488b20c18b73f6685a96e97e65d058955af9b6a9af541(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38198c55564dc81e5e427d008e31eef21c9d45f4ca2ec63439595c6ad60674f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d3cdd206dde21d0e9dcfdda494fee66b7586395cfe6eca4a22506d927fd18a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicyOsConstraints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fc11e679a6d68b0b037e7e0e7421cba009c3c92b9fe139eb4e8696393c54e9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__747c91de5454cc507ba59fa1302149540e3173ee4eae47349d019269f940c509(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c84a892fc1d197a344110f4184e54edc75a5d983bbd0926ea0debcacec369bab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db4b1070ecee7fe7a0f7461d8f2f630fead91d9d97c223a7c29786d86d924c7c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370dd1c0b921eb2b5b984a9bcfe3e4a36351659be3e195f7c6cf6b5a4dbc875f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9849113b5da926c00b672e40d36ad689cf74ff7bc1e2291e718c326b3df11d(
    value: typing.Optional[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsDevicePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6bc73d226e88d96890ecc2629bc93caa9ce437c51a694793cf6fb3e92cf4e7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d7c5858f31d5a0a857602b5058e0e5e52c93c8cd2dab87296cbbceba3d6890(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85afa213eb9f09e05f18db9cd0ac91679d3ae8053e28a356446d710a95d2654c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aae6d1579d904eee70e06df567033d263c6712e5f97d9b52b33a96a20451038(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de52c4f73444c679744c5e0bc10d3299042c1c506eca7a8ca7144be30cbbb36(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d680163a54ebaf8cab2bd9f62bf9a0f6a461490ddb8d70ddcf9df18c589e32(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevelsBasicConditions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9541b8410c5c2f8553c87be73d425844db2928c4055b90da348aa5b7ba4637d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b15527390b4b17751f6549343f771cb4cbc1c0ee9f35ca481b376cba6361b54(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d46859c9dcd8f70729ffe1bf7a6e7d94b4226a8bfe755e7b605a33677b8130(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdde5178ab0bec4867e817543b210f037fb3bf14172997833c10a4d2ebbd5800(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5c73fded29be391bb3635a7e6bc0662f3f95d33055254bf321b4cf623a3ff9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2031b5375c13563161cd383ffff12caa2e17d44eaa523a74a4d1f79b378913dd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6644383682af3908d6fd6305feb1b222ba54aff6ee6f7130e346f7795809d615(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bacd4cd0e9b4a6df9715fda4813f7438aa47b7428f5609924ccebec80363cac9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsAccessLevelsBasicConditions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10104a977879d1ae242a69099f1bfeb4846353532443fff8f2e29e864032bfee(
    *,
    vpc_subnetwork: typing.Optional[typing.Union[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetwork, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f8ef188d2f243afaf226a986dc4ba2e9a9232b8e7de4bd03fa8c0c466a11055(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c06456717d6d9e254fdae7382b90413d2dc9e69eee04225f2ea4b47f1b3661a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81884678d8a0d6beb41d0e4e94fa6d478de5bba0b32e22e1af1e634d5c75a76e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b889887d6cd041199b9fd076208b0786beb4ff8c337558104e389a6cf573038(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a3d78a5c11384cf664f6e544ab4334ade7a9803c75edd7b5cfba81f76caeb7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4224f1cf3e7bd860f9bd6872325e97036364d4c5a769e00e377668f30afef716(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb17d476184f88bac57f8821b612bf46108a3052484e4a3a2299bf50e6ce9fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58edcc69fefe594b9a36138727383bed98e0401fe228de4f0d513fc8d1ab64c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aa10cb6a1c266e6ba2d382226180e0cf7498acd40c963611444242745b13474(
    *,
    network: builtins.str,
    vpc_ip_subnetworks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c02907181326c510620bb9212c34d3b119a1ea46aa3e2e6ba47f55b4f83a1eed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13fb3399b349558423bc719126a8688aea05495d136270f9b0c3ee9fe4d6934c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fccc7d541cb9408448e5df1cbfeb30f8a1ff05432c1b07c464dec758221288c9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b2874b929c161fcb07e98b7f4ee343f328210fdb7f7d6f7486de6bfe6c42b3(
    value: typing.Optional[AccessContextManagerAccessLevelsAccessLevelsBasicConditionsVpcNetworkSourcesVpcSubnetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73bc58e9f83cef46b17315219517f249f91c6e0691e74d27f1b67844459f18b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0218e3370740d854dff41fde8d5e8e0312d78c76194378c03355a21c2ca66ddc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelsAccessLevelsBasicConditions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49eb910740cd5cbd3d625fae65e9221d0552b4e148d2d21669008362fa360b8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b608425b07eb2bc34fde185593388169db08497075374f2867d1e7398243737e(
    value: typing.Optional[AccessContextManagerAccessLevelsAccessLevelsBasic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09b6e9a59e5608aec4892a062a1c2de42ca2d8cb10e401ad7dfbf0a1c70a7c0(
    *,
    expr: typing.Union[AccessContextManagerAccessLevelsAccessLevelsCustomExpr, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ccc443f46f9d46dc7ea12db892a67ba60ca520645c4824dd6ae0a05919d4bb4(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__419aa1b0025c7209aaaf35f8ee6baef3dc49738986a323f3d54658b69c226f42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951a0b802411d5a56fc4ebdb4f80f83bdda5a744c39b9ca9a6f95ffcaa3bd246(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f76cb595c5f0be001b0f5dc8cc5f8bf3ee9beab567118fd68165dd203992963e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0c23329a408045792a9d7f7ea6716cb9a170f2e3215834a74dec52bcedb5ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdc435b1a4659bf3bf3172a610182a4d58340b0e9ed7aafa9eefcf81c2b59567(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__596f0352373acc9df7f459a4daadbc23dbe6590e062b7f1a1c6e6a69634e9cce(
    value: typing.Optional[AccessContextManagerAccessLevelsAccessLevelsCustomExpr],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__784fa797e1226fd615839dcf749b7f8d3f2b58b551ee3b19d213623ced217769(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50f5dd8ce462f0f545043460487a946b7800897141005ed99b644f7438d7ccf(
    value: typing.Optional[AccessContextManagerAccessLevelsAccessLevelsCustom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__128a614cb8390b6512e770e90fd2206abeb64c1178b8849f51825490083ed38e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__280b84c277b4fa8cb32d1dc33b3578d960646c3368a87843cd8dff060544467d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68de474fd9c982bc22a98df104064ccfa370319918f1d866c0a918bcc6f34a3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48c3838e076269aca28286494fb55d9d006af748b9e8847a4aa92d5a2ceed47(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff40d6ca7205cf5f1a45d532f1de5f41e6a9e92366c0d1f03f4e54d08d7b7e7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf190819f31da2d105c8648937353a0ec1cb38640f0808211afe2859ff3bffa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelsAccessLevels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d343e5d233ff910a71d5ccba6f348d9eb6d9b9ad8457c29903d264a9c62bf35f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec0f1cea5a596db53a59410413427f77d161a08458f0e9bd1a4b6546543faf15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a2e5dc5d6c6740ef7b0099b5ab6fe737d9596c2b796e21c7f98c484df710d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4422cf227bc28ca26132f96013b5ea213a7dbdfa82c1fdbc3cbf325c5a0fa639(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f943b71ccc6ddcf21c380ed4283ccea188bcf22935ab7ccf15b29e0c4e70fd1a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsAccessLevels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718af0acdf5d81d4ef81220c2b9b2796d6d04cfdf9abb0fa10ddbc16b95ea21c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parent: builtins.str,
    access_levels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelsAccessLevels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerAccessLevelsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c6ab78e15d7c4f9044833a9f3b29f3015205c4b6294e7df834a2dcc0c479bc(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f9b4d15ec95197b2d9dd218428f8b04bf7c1f5f30cd5922561055952b6577c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f86e7bfaaa3d1d80ebc97e151ae753c955c3266886ed44ae9d357fb85762c6ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03292aa98428d6d3e380c87327951838ae30cbd2a01b5fb58a7e546a3cf05e91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a181e1ed310f8b4f3fa6bfef627d3416757e9ebec5a5d35a13877d4db3521285(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eafddab90310441182345669242a168ef8065309f54f55975e8750b1581000e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelsTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

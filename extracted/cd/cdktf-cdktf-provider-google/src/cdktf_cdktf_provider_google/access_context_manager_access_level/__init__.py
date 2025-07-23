r'''
# `google_access_context_manager_access_level`

Refer to the Terraform Registry for docs: [`google_access_context_manager_access_level`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level).
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


class AccessContextManagerAccessLevel(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevel",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level google_access_context_manager_access_level}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        parent: builtins.str,
        title: builtins.str,
        basic: typing.Optional[typing.Union["AccessContextManagerAccessLevelBasic", typing.Dict[builtins.str, typing.Any]]] = None,
        custom: typing.Optional[typing.Union["AccessContextManagerAccessLevelCustom", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerAccessLevelTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level google_access_context_manager_access_level} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Resource name for the Access Level. The short_name component must begin with a letter and only include alphanumeric and '_'. Format: accessPolicies/{policy_id}/accessLevels/{short_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#name AccessContextManagerAccessLevel#name}
        :param parent: The AccessPolicy this AccessLevel lives in. Format: accessPolicies/{policy_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#parent AccessContextManagerAccessLevel#parent}
        :param title: Human readable title. Must be unique within the Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#title AccessContextManagerAccessLevel#title}
        :param basic: basic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#basic AccessContextManagerAccessLevel#basic}
        :param custom: custom block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#custom AccessContextManagerAccessLevel#custom}
        :param description: Description of the AccessLevel and its use. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#description AccessContextManagerAccessLevel#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#id AccessContextManagerAccessLevel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#timeouts AccessContextManagerAccessLevel#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6728517009e6c355f865ccd130744e116c2e4ec44d644403a47cab568a88170)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccessContextManagerAccessLevelConfig(
            name=name,
            parent=parent,
            title=title,
            basic=basic,
            custom=custom,
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
        '''Generates CDKTF code for importing a AccessContextManagerAccessLevel resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AccessContextManagerAccessLevel to import.
        :param import_from_id: The id of the existing AccessContextManagerAccessLevel that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AccessContextManagerAccessLevel to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b6fabf7d02a35aa880f4913a02c2a90bcad1889aa40bbe00d0296d9ef6aa93)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBasic")
    def put_basic(
        self,
        *,
        conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerAccessLevelBasicConditions", typing.Dict[builtins.str, typing.Any]]]],
        combining_function: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#conditions AccessContextManagerAccessLevel#conditions}
        :param combining_function: How the conditions list should be combined to determine if a request is granted this AccessLevel. If AND is used, each Condition in conditions must be satisfied for the AccessLevel to be applied. If OR is used, at least one Condition in conditions must be satisfied for the AccessLevel to be applied. Default value: "AND" Possible values: ["AND", "OR"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#combining_function AccessContextManagerAccessLevel#combining_function}
        '''
        value = AccessContextManagerAccessLevelBasic(
            conditions=conditions, combining_function=combining_function
        )

        return typing.cast(None, jsii.invoke(self, "putBasic", [value]))

    @jsii.member(jsii_name="putCustom")
    def put_custom(
        self,
        *,
        expr: typing.Union["AccessContextManagerAccessLevelCustomExpr", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param expr: expr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#expr AccessContextManagerAccessLevel#expr}
        '''
        value = AccessContextManagerAccessLevelCustom(expr=expr)

        return typing.cast(None, jsii.invoke(self, "putCustom", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#create AccessContextManagerAccessLevel#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#delete AccessContextManagerAccessLevel#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#update AccessContextManagerAccessLevel#update}.
        '''
        value = AccessContextManagerAccessLevelTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBasic")
    def reset_basic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasic", []))

    @jsii.member(jsii_name="resetCustom")
    def reset_custom(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustom", []))

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
    @jsii.member(jsii_name="basic")
    def basic(self) -> "AccessContextManagerAccessLevelBasicOutputReference":
        return typing.cast("AccessContextManagerAccessLevelBasicOutputReference", jsii.get(self, "basic"))

    @builtins.property
    @jsii.member(jsii_name="custom")
    def custom(self) -> "AccessContextManagerAccessLevelCustomOutputReference":
        return typing.cast("AccessContextManagerAccessLevelCustomOutputReference", jsii.get(self, "custom"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AccessContextManagerAccessLevelTimeoutsOutputReference":
        return typing.cast("AccessContextManagerAccessLevelTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="basicInput")
    def basic_input(self) -> typing.Optional["AccessContextManagerAccessLevelBasic"]:
        return typing.cast(typing.Optional["AccessContextManagerAccessLevelBasic"], jsii.get(self, "basicInput"))

    @builtins.property
    @jsii.member(jsii_name="customInput")
    def custom_input(self) -> typing.Optional["AccessContextManagerAccessLevelCustom"]:
        return typing.cast(typing.Optional["AccessContextManagerAccessLevelCustom"], jsii.get(self, "customInput"))

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
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["AccessContextManagerAccessLevelTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["AccessContextManagerAccessLevelTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9b9314e574cf19458d785bf6b619b00d4c22348622e276f807fe109fdb947ce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1eaacefaf04fca0359bf447580aa495bfab45b2d44405fa8b47344e3334b38b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc8d779f5c43551b7661ff88f80efca1bf3761606f9942598888d6d8513ee807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a510e8ae853672ef520d0f01c40be102e4ef9f233b33e5b1102bd8df98799d23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0465edc3e1c6b074f2d609bd59ddf8837998f98376346313588dbec2bfc18233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelBasic",
    jsii_struct_bases=[],
    name_mapping={
        "conditions": "conditions",
        "combining_function": "combiningFunction",
    },
)
class AccessContextManagerAccessLevelBasic:
    def __init__(
        self,
        *,
        conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerAccessLevelBasicConditions", typing.Dict[builtins.str, typing.Any]]]],
        combining_function: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#conditions AccessContextManagerAccessLevel#conditions}
        :param combining_function: How the conditions list should be combined to determine if a request is granted this AccessLevel. If AND is used, each Condition in conditions must be satisfied for the AccessLevel to be applied. If OR is used, at least one Condition in conditions must be satisfied for the AccessLevel to be applied. Default value: "AND" Possible values: ["AND", "OR"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#combining_function AccessContextManagerAccessLevel#combining_function}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bcc17ba8f569eda97338e52a0bff79ce67c7c17fb9b88d373674721ff821cf4)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelBasicConditions"]]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#conditions AccessContextManagerAccessLevel#conditions}
        '''
        result = self._values.get("conditions")
        assert result is not None, "Required property 'conditions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelBasicConditions"]], result)

    @builtins.property
    def combining_function(self) -> typing.Optional[builtins.str]:
        '''How the conditions list should be combined to determine if a request is granted this AccessLevel.

        If AND is used, each Condition in
        conditions must be satisfied for the AccessLevel to be applied. If
        OR is used, at least one Condition in conditions must be satisfied
        for the AccessLevel to be applied. Default value: "AND" Possible values: ["AND", "OR"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#combining_function AccessContextManagerAccessLevel#combining_function}
        '''
        result = self._values.get("combining_function")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelBasic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelBasicConditions",
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
class AccessContextManagerAccessLevelBasicConditions:
    def __init__(
        self,
        *,
        device_policy: typing.Optional[typing.Union["AccessContextManagerAccessLevelBasicConditionsDevicePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        ip_subnetworks: typing.Optional[typing.Sequence[builtins.str]] = None,
        members: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        required_access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_network_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param device_policy: device_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#device_policy AccessContextManagerAccessLevel#device_policy}
        :param ip_subnetworks: A list of CIDR block IP subnetwork specification. May be IPv4 or IPv6. Note that for a CIDR IP address block, the specified IP address portion must be properly truncated (i.e. all the host bits must be zero) or the input is considered malformed. For example, "192.0.2.0/24" is accepted but "192.0.2.1/24" is not. Similarly, for IPv6, "2001:db8::/32" is accepted whereas "2001:db8::1/32" is not. The originating IP of a request must be in one of the listed subnets in order for this Condition to be true. If empty, all IP addresses are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#ip_subnetworks AccessContextManagerAccessLevel#ip_subnetworks}
        :param members: An allowed list of members (users, service accounts). Using groups is not supported yet. The signed-in user originating the request must be a part of one of the provided members. If not specified, a request may come from any user (logged in/not logged in, not present in any groups, etc.). Formats: 'user:{emailid}', 'serviceAccount:{emailid}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#members AccessContextManagerAccessLevel#members}
        :param negate: Whether to negate the Condition. If true, the Condition becomes a NAND over its non-empty fields, each field must be false for the Condition overall to be satisfied. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#negate AccessContextManagerAccessLevel#negate}
        :param regions: The request must originate from one of the provided countries/regions. Format: A valid ISO 3166-1 alpha-2 code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#regions AccessContextManagerAccessLevel#regions}
        :param required_access_levels: A list of other access levels defined in the same Policy, referenced by resource name. Referencing an AccessLevel which does not exist is an error. All access levels listed must be granted for the Condition to be true. Format: accessPolicies/{policy_id}/accessLevels/{short_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#required_access_levels AccessContextManagerAccessLevel#required_access_levels}
        :param vpc_network_sources: vpc_network_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#vpc_network_sources AccessContextManagerAccessLevel#vpc_network_sources}
        '''
        if isinstance(device_policy, dict):
            device_policy = AccessContextManagerAccessLevelBasicConditionsDevicePolicy(**device_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eea1f5b3e29468e27559396f0c3d9343cda1e81e11bbf617c0099cb53d101b4)
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
    ) -> typing.Optional["AccessContextManagerAccessLevelBasicConditionsDevicePolicy"]:
        '''device_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#device_policy AccessContextManagerAccessLevel#device_policy}
        '''
        result = self._values.get("device_policy")
        return typing.cast(typing.Optional["AccessContextManagerAccessLevelBasicConditionsDevicePolicy"], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#ip_subnetworks AccessContextManagerAccessLevel#ip_subnetworks}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#members AccessContextManagerAccessLevel#members}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#negate AccessContextManagerAccessLevel#negate}
        '''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The request must originate from one of the provided countries/regions. Format: A valid ISO 3166-1 alpha-2 code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#regions AccessContextManagerAccessLevel#regions}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#required_access_levels AccessContextManagerAccessLevel#required_access_levels}
        '''
        result = self._values.get("required_access_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_network_sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources"]]]:
        '''vpc_network_sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#vpc_network_sources AccessContextManagerAccessLevel#vpc_network_sources}
        '''
        result = self._values.get("vpc_network_sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelBasicConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelBasicConditionsDevicePolicy",
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
class AccessContextManagerAccessLevelBasicConditionsDevicePolicy:
    def __init__(
        self,
        *,
        allowed_device_management_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_encryption_statuses: typing.Optional[typing.Sequence[builtins.str]] = None,
        os_constraints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        require_admin_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_corp_owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_screen_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_device_management_levels: A list of allowed device management levels. An empty list allows all management levels. Possible values: ["MANAGEMENT_UNSPECIFIED", "NONE", "BASIC", "COMPLETE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#allowed_device_management_levels AccessContextManagerAccessLevel#allowed_device_management_levels}
        :param allowed_encryption_statuses: A list of allowed encryptions statuses. An empty list allows all statuses. Possible values: ["ENCRYPTION_UNSPECIFIED", "ENCRYPTION_UNSUPPORTED", "UNENCRYPTED", "ENCRYPTED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#allowed_encryption_statuses AccessContextManagerAccessLevel#allowed_encryption_statuses}
        :param os_constraints: os_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#os_constraints AccessContextManagerAccessLevel#os_constraints}
        :param require_admin_approval: Whether the device needs to be approved by the customer admin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#require_admin_approval AccessContextManagerAccessLevel#require_admin_approval}
        :param require_corp_owned: Whether the device needs to be corp owned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#require_corp_owned AccessContextManagerAccessLevel#require_corp_owned}
        :param require_screen_lock: Whether or not screenlock is required for the DevicePolicy to be true. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#require_screen_lock AccessContextManagerAccessLevel#require_screen_lock}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a42f34c1c198950e7a1ae3b540e10105eaf07d78dc5db41b6457564479b7ca6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#allowed_device_management_levels AccessContextManagerAccessLevel#allowed_device_management_levels}
        '''
        result = self._values.get("allowed_device_management_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_encryption_statuses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of allowed encryptions statuses. An empty list allows all statuses. Possible values: ["ENCRYPTION_UNSPECIFIED", "ENCRYPTION_UNSUPPORTED", "UNENCRYPTED", "ENCRYPTED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#allowed_encryption_statuses AccessContextManagerAccessLevel#allowed_encryption_statuses}
        '''
        result = self._values.get("allowed_encryption_statuses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def os_constraints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints"]]]:
        '''os_constraints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#os_constraints AccessContextManagerAccessLevel#os_constraints}
        '''
        result = self._values.get("os_constraints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints"]]], result)

    @builtins.property
    def require_admin_approval(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the device needs to be approved by the customer admin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#require_admin_approval AccessContextManagerAccessLevel#require_admin_approval}
        '''
        result = self._values.get("require_admin_approval")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_corp_owned(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the device needs to be corp owned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#require_corp_owned AccessContextManagerAccessLevel#require_corp_owned}
        '''
        result = self._values.get("require_corp_owned")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_screen_lock(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not screenlock is required for the DevicePolicy to be true. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#require_screen_lock AccessContextManagerAccessLevel#require_screen_lock}
        '''
        result = self._values.get("require_screen_lock")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelBasicConditionsDevicePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints",
    jsii_struct_bases=[],
    name_mapping={
        "os_type": "osType",
        "minimum_version": "minimumVersion",
        "require_verified_chrome_os": "requireVerifiedChromeOs",
    },
)
class AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints:
    def __init__(
        self,
        *,
        os_type: builtins.str,
        minimum_version: typing.Optional[builtins.str] = None,
        require_verified_chrome_os: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param os_type: The operating system type of the device. Possible values: ["OS_UNSPECIFIED", "DESKTOP_MAC", "DESKTOP_WINDOWS", "DESKTOP_LINUX", "DESKTOP_CHROME_OS", "ANDROID", "IOS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#os_type AccessContextManagerAccessLevel#os_type}
        :param minimum_version: The minimum allowed OS version. If not set, any version of this OS satisfies the constraint. Format: "major.minor.patch" such as "10.5.301", "9.2.1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#minimum_version AccessContextManagerAccessLevel#minimum_version}
        :param require_verified_chrome_os: If you specify DESKTOP_CHROME_OS for osType, you can optionally include requireVerifiedChromeOs to require Chrome Verified Access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#require_verified_chrome_os AccessContextManagerAccessLevel#require_verified_chrome_os}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83df9030369d715d0ce0545b054fc53cf67434e59b7401f14e95c058b80bee1c)
            check_type(argname="argument os_type", value=os_type, expected_type=type_hints["os_type"])
            check_type(argname="argument minimum_version", value=minimum_version, expected_type=type_hints["minimum_version"])
            check_type(argname="argument require_verified_chrome_os", value=require_verified_chrome_os, expected_type=type_hints["require_verified_chrome_os"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "os_type": os_type,
        }
        if minimum_version is not None:
            self._values["minimum_version"] = minimum_version
        if require_verified_chrome_os is not None:
            self._values["require_verified_chrome_os"] = require_verified_chrome_os

    @builtins.property
    def os_type(self) -> builtins.str:
        '''The operating system type of the device. Possible values: ["OS_UNSPECIFIED", "DESKTOP_MAC", "DESKTOP_WINDOWS", "DESKTOP_LINUX", "DESKTOP_CHROME_OS", "ANDROID", "IOS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#os_type AccessContextManagerAccessLevel#os_type}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#minimum_version AccessContextManagerAccessLevel#minimum_version}
        '''
        result = self._values.get("minimum_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_verified_chrome_os(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If you specify DESKTOP_CHROME_OS for osType, you can optionally include requireVerifiedChromeOs to require Chrome Verified Access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#require_verified_chrome_os AccessContextManagerAccessLevel#require_verified_chrome_os}
        '''
        result = self._values.get("require_verified_chrome_os")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbc1a72d1f24a97ec889285fbc5a6203e25070cdee63e3d465e5818e0f06f90a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4c779dc849fac60c654642df4707eb9f29d1b9a8f29a3eeaf266d37e167e572)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9b854a869d6ae9ffd7d0ef761d702443d9aedf5a21bb7a03449d55afe2ef08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d617e0e18e1feb55ebebcecfbd6167ac460751ce16b43862a31e7908eb4139a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d40d680136995c39c7f8e4caeeeb36eb827fc334e21b985742aab996d05e75b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08569111194a740c41e3753a5441fae2144b34f62df0b935e204c7ca37de95e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b645a6996c954a81e4e373a223dcba083e652845f981d6f8978d6fd8276c2e07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMinimumVersion")
    def reset_minimum_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumVersion", []))

    @jsii.member(jsii_name="resetRequireVerifiedChromeOs")
    def reset_require_verified_chrome_os(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireVerifiedChromeOs", []))

    @builtins.property
    @jsii.member(jsii_name="minimumVersionInput")
    def minimum_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="osTypeInput")
    def os_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="requireVerifiedChromeOsInput")
    def require_verified_chrome_os_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireVerifiedChromeOsInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumVersion")
    def minimum_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumVersion"))

    @minimum_version.setter
    def minimum_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e15c231303f82452c029b1749909a7ff5ebe6f4d572d7ca64f78abc120c4bb36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @os_type.setter
    def os_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20fdda2faf9333573eca1a2573820aa5d82bb8d82c32a39779e2a987585bd199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireVerifiedChromeOs")
    def require_verified_chrome_os(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireVerifiedChromeOs"))

    @require_verified_chrome_os.setter
    def require_verified_chrome_os(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7946f93164483be6a3e04cf0ba9973433afc0011ac045e1f97bbdd0aedcb8eec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireVerifiedChromeOs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4412af7c66e47b7294861a3456d4575cda3f4ca282acc907b258d3f74285f6f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerAccessLevelBasicConditionsDevicePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelBasicConditionsDevicePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00c5d444863fba7c2b6aa7288595eb700b832ae8aabfcde48341d0ae86c79e02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOsConstraints")
    def put_os_constraints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b469b640868539cc3884cef843ba8d3191c4f59a768bf0de81790d1bd5754b95)
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
    ) -> AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraintsList:
        return typing.cast(AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraintsList, jsii.get(self, "osConstraints"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints]]], jsii.get(self, "osConstraintsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7ae357049324d33f56b491143a03011c3c1bf1e8536a071dcfec916e3dcd0b44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedDeviceManagementLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedEncryptionStatuses")
    def allowed_encryption_statuses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedEncryptionStatuses"))

    @allowed_encryption_statuses.setter
    def allowed_encryption_statuses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__562e2c763446cd1cda90c69ace7766dd4cb9bddbc204d17611a34ca645ed6913)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44addc768326fb35629ee7ff425d7dffe755a54272a4ac189a3a2bb53f2341ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d37f57680b7f12665be4239bea888a1988173206cfecd8ee26094f82a113e32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a12d49d5ed1e9c22c07fd526d23c4e5ff3433f54291af35afc95d18506faedd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireScreenLock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerAccessLevelBasicConditionsDevicePolicy]:
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelBasicConditionsDevicePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerAccessLevelBasicConditionsDevicePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51bc21f39b82149bd956c5c0a62b22bb02d64ae52f870a1884f6e82c59af4143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerAccessLevelBasicConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelBasicConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a564759365ebc86f5740a73af58f5f8e3d7c490e9db1ba06b499b58154593f98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerAccessLevelBasicConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d1ad5f8d8d0fb9edf4cd3971f28a56a5d671fb69d1c0581620a0a2921f45f3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerAccessLevelBasicConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0686fa06d336be3ba8d2235d36a2fef2e2b5b557c48e9d3718417d3c85a2729)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb6709a6b4f93aef5fdf1fbd9dff694e6ea33da391f8106af213e69d04c02ba8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__421ba8c392be8a1599bf1ce5ac7010d998a49b7f35a2ff49649375fa17ec227b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelBasicConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelBasicConditions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelBasicConditions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61d5d12c8902221dd12165b4dab824cc0e585fec80bae3b8efa51fe3a6ca72f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerAccessLevelBasicConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelBasicConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0ca1ecb1fa74dcd56282d20fff156aef31c02729897bd1e1b5604951470a8ed)
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
        os_constraints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints, typing.Dict[builtins.str, typing.Any]]]]] = None,
        require_admin_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_corp_owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_screen_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_device_management_levels: A list of allowed device management levels. An empty list allows all management levels. Possible values: ["MANAGEMENT_UNSPECIFIED", "NONE", "BASIC", "COMPLETE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#allowed_device_management_levels AccessContextManagerAccessLevel#allowed_device_management_levels}
        :param allowed_encryption_statuses: A list of allowed encryptions statuses. An empty list allows all statuses. Possible values: ["ENCRYPTION_UNSPECIFIED", "ENCRYPTION_UNSUPPORTED", "UNENCRYPTED", "ENCRYPTED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#allowed_encryption_statuses AccessContextManagerAccessLevel#allowed_encryption_statuses}
        :param os_constraints: os_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#os_constraints AccessContextManagerAccessLevel#os_constraints}
        :param require_admin_approval: Whether the device needs to be approved by the customer admin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#require_admin_approval AccessContextManagerAccessLevel#require_admin_approval}
        :param require_corp_owned: Whether the device needs to be corp owned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#require_corp_owned AccessContextManagerAccessLevel#require_corp_owned}
        :param require_screen_lock: Whether or not screenlock is required for the DevicePolicy to be true. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#require_screen_lock AccessContextManagerAccessLevel#require_screen_lock}
        '''
        value = AccessContextManagerAccessLevelBasicConditionsDevicePolicy(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02472ff1244a42da5a31348fa351fc200bd03e864b67fd7745e129278f8ddf61)
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
    ) -> AccessContextManagerAccessLevelBasicConditionsDevicePolicyOutputReference:
        return typing.cast(AccessContextManagerAccessLevelBasicConditionsDevicePolicyOutputReference, jsii.get(self, "devicePolicy"))

    @builtins.property
    @jsii.member(jsii_name="vpcNetworkSources")
    def vpc_network_sources(
        self,
    ) -> "AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesList":
        return typing.cast("AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesList", jsii.get(self, "vpcNetworkSources"))

    @builtins.property
    @jsii.member(jsii_name="devicePolicyInput")
    def device_policy_input(
        self,
    ) -> typing.Optional[AccessContextManagerAccessLevelBasicConditionsDevicePolicy]:
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelBasicConditionsDevicePolicy], jsii.get(self, "devicePolicyInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources"]]], jsii.get(self, "vpcNetworkSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="ipSubnetworks")
    def ip_subnetworks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipSubnetworks"))

    @ip_subnetworks.setter
    def ip_subnetworks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93aafdb96f8b1c57e6ab2d01e16022d93d4baae25bd4a9da2cc78c524a191c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipSubnetworks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="members")
    def members(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "members"))

    @members.setter
    def members(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32cd0473be1dcabcffc6c1d2a2a07d81c67774b79ece666c9451a6010342c0ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c4e4994454d4b549c0fab02a0bcce10f030d1b938a2ab6b6737657b6a08568c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regions")
    def regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "regions"))

    @regions.setter
    def regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a7c726fcec9ec056ec1eaa644f26b2406bcc010c3c83f5ec5cd325048fc09c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredAccessLevels")
    def required_access_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requiredAccessLevels"))

    @required_access_levels.setter
    def required_access_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c3ea95e4fcfe6aa80c762e7c807c401e93279f2ab8c7735aa4b03ff721cf418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredAccessLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelBasicConditions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelBasicConditions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelBasicConditions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1509bd5c00e9e2eec4e7ef6fbf9975b47766a27c32b8453acaaca12015c9fb0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources",
    jsii_struct_bases=[],
    name_mapping={"vpc_subnetwork": "vpcSubnetwork"},
)
class AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources:
    def __init__(
        self,
        *,
        vpc_subnetwork: typing.Optional[typing.Union["AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetwork", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param vpc_subnetwork: vpc_subnetwork block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#vpc_subnetwork AccessContextManagerAccessLevel#vpc_subnetwork}
        '''
        if isinstance(vpc_subnetwork, dict):
            vpc_subnetwork = AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetwork(**vpc_subnetwork)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20370d481843ce1196e9746c78d3ecf606c90cb133cf072288aeaff8709a60bb)
            check_type(argname="argument vpc_subnetwork", value=vpc_subnetwork, expected_type=type_hints["vpc_subnetwork"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if vpc_subnetwork is not None:
            self._values["vpc_subnetwork"] = vpc_subnetwork

    @builtins.property
    def vpc_subnetwork(
        self,
    ) -> typing.Optional["AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetwork"]:
        '''vpc_subnetwork block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#vpc_subnetwork AccessContextManagerAccessLevel#vpc_subnetwork}
        '''
        result = self._values.get("vpc_subnetwork")
        return typing.cast(typing.Optional["AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetwork"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__067e345b8ab0fff3ae366bbe77a1668aa24b15a09ff21d477321916a6ace643f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c084d863b92fee55c684fd8cc2674d7518054384c0113bce79c8254f078cfdd2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__803b77a5a16226c39c91e1800b7f9c8011c82a3ff257ddc86301e6b9174106a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5eecf081fbdc88eebd70eeeb8195d80454d7bdef5feb1f8a03cce33c65a6039)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1638a49f263a3e4adbad3964972dcf800b2e3581382eac10b41fd6b1d213890b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bba83f1d70143759823e013ff098161c1dc75c2349d945cea72b53c347d00c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1367e195098282823d8828284a90322f29c85b348edb44beba17ca0e6d0cf7f8)
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
        :param network: Required. Network name to be allowed by this Access Level. Networks of foreign organizations requires 'compute.network.get' permission to be granted to caller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#network AccessContextManagerAccessLevel#network}
        :param vpc_ip_subnetworks: A list of CIDR block IP subnetwork specification. Must be IPv4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#vpc_ip_subnetworks AccessContextManagerAccessLevel#vpc_ip_subnetworks}
        '''
        value = AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetwork(
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
    ) -> "AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetworkOutputReference":
        return typing.cast("AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetworkOutputReference", jsii.get(self, "vpcSubnetwork"))

    @builtins.property
    @jsii.member(jsii_name="vpcSubnetworkInput")
    def vpc_subnetwork_input(
        self,
    ) -> typing.Optional["AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetwork"]:
        return typing.cast(typing.Optional["AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetwork"], jsii.get(self, "vpcSubnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286a0be872674428f750ea952fc8c3b40c2a1b3a256fdc228bc1f2a2f990f9ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetwork",
    jsii_struct_bases=[],
    name_mapping={"network": "network", "vpc_ip_subnetworks": "vpcIpSubnetworks"},
)
class AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetwork:
    def __init__(
        self,
        *,
        network: builtins.str,
        vpc_ip_subnetworks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param network: Required. Network name to be allowed by this Access Level. Networks of foreign organizations requires 'compute.network.get' permission to be granted to caller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#network AccessContextManagerAccessLevel#network}
        :param vpc_ip_subnetworks: A list of CIDR block IP subnetwork specification. Must be IPv4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#vpc_ip_subnetworks AccessContextManagerAccessLevel#vpc_ip_subnetworks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b01a65f98ccc24344422688f6ab6527e0811e323a7da0906dd15c120366b7896)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#network AccessContextManagerAccessLevel#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_ip_subnetworks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of CIDR block IP subnetwork specification. Must be IPv4.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#vpc_ip_subnetworks AccessContextManagerAccessLevel#vpc_ip_subnetworks}
        '''
        result = self._values.get("vpc_ip_subnetworks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a122f3e15ea0bc370db7957ac1e4976f36c6226311aca1a87aea5a2611a20939)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec8ffd48af95193a11c4ce996998c37e61f71ba0035c968299976857d0947e00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcIpSubnetworks")
    def vpc_ip_subnetworks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vpcIpSubnetworks"))

    @vpc_ip_subnetworks.setter
    def vpc_ip_subnetworks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__737fc0f9697e8aa4acd0ed922313874eac5340b27ddcd4f80c6da32a1c7f6f24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcIpSubnetworks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetwork]:
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__202115f1ceaffcfd40efa9a4dc7be796bc3e9bf07fcffae115c964ea0ebd8436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerAccessLevelBasicOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelBasicOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9299aef5a2ac73aef689eb6d8d1accab296dedf67dba5c4ff0eb2ebf7a608d44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelBasicConditions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c359c21d74ae66c4be234aacae158e8ce39115dc5ab8273df0ab8461e419046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="resetCombiningFunction")
    def reset_combining_function(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCombiningFunction", []))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> AccessContextManagerAccessLevelBasicConditionsList:
        return typing.cast(AccessContextManagerAccessLevelBasicConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="combiningFunctionInput")
    def combining_function_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "combiningFunctionInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelBasicConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelBasicConditions]]], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="combiningFunction")
    def combining_function(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "combiningFunction"))

    @combining_function.setter
    def combining_function(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b2d30d767f91f32864d80e56eae96d51338da818cac1368eaa04d08c36c804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "combiningFunction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AccessContextManagerAccessLevelBasic]:
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelBasic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerAccessLevelBasic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7caf2d527661f98c694dd3ee8b67ba0d81d386282f82c954cf4eec1055bdb428)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelConfig",
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
        "parent": "parent",
        "title": "title",
        "basic": "basic",
        "custom": "custom",
        "description": "description",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class AccessContextManagerAccessLevelConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        parent: builtins.str,
        title: builtins.str,
        basic: typing.Optional[typing.Union[AccessContextManagerAccessLevelBasic, typing.Dict[builtins.str, typing.Any]]] = None,
        custom: typing.Optional[typing.Union["AccessContextManagerAccessLevelCustom", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerAccessLevelTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Resource name for the Access Level. The short_name component must begin with a letter and only include alphanumeric and '_'. Format: accessPolicies/{policy_id}/accessLevels/{short_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#name AccessContextManagerAccessLevel#name}
        :param parent: The AccessPolicy this AccessLevel lives in. Format: accessPolicies/{policy_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#parent AccessContextManagerAccessLevel#parent}
        :param title: Human readable title. Must be unique within the Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#title AccessContextManagerAccessLevel#title}
        :param basic: basic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#basic AccessContextManagerAccessLevel#basic}
        :param custom: custom block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#custom AccessContextManagerAccessLevel#custom}
        :param description: Description of the AccessLevel and its use. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#description AccessContextManagerAccessLevel#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#id AccessContextManagerAccessLevel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#timeouts AccessContextManagerAccessLevel#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(basic, dict):
            basic = AccessContextManagerAccessLevelBasic(**basic)
        if isinstance(custom, dict):
            custom = AccessContextManagerAccessLevelCustom(**custom)
        if isinstance(timeouts, dict):
            timeouts = AccessContextManagerAccessLevelTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552ee6c7cb7fc9d1d5e28f6da0ccb425d44b8c3b9ca810d8846cc2fcfcb0f245)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument basic", value=basic, expected_type=type_hints["basic"])
            check_type(argname="argument custom", value=custom, expected_type=type_hints["custom"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "parent": parent,
            "title": title,
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
        if basic is not None:
            self._values["basic"] = basic
        if custom is not None:
            self._values["custom"] = custom
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
    def name(self) -> builtins.str:
        '''Resource name for the Access Level.

        The short_name component must begin
        with a letter and only include alphanumeric and '_'.
        Format: accessPolicies/{policy_id}/accessLevels/{short_name}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#name AccessContextManagerAccessLevel#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''The AccessPolicy this AccessLevel lives in. Format: accessPolicies/{policy_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#parent AccessContextManagerAccessLevel#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Human readable title. Must be unique within the Policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#title AccessContextManagerAccessLevel#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def basic(self) -> typing.Optional[AccessContextManagerAccessLevelBasic]:
        '''basic block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#basic AccessContextManagerAccessLevel#basic}
        '''
        result = self._values.get("basic")
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelBasic], result)

    @builtins.property
    def custom(self) -> typing.Optional["AccessContextManagerAccessLevelCustom"]:
        '''custom block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#custom AccessContextManagerAccessLevel#custom}
        '''
        result = self._values.get("custom")
        return typing.cast(typing.Optional["AccessContextManagerAccessLevelCustom"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the AccessLevel and its use. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#description AccessContextManagerAccessLevel#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#id AccessContextManagerAccessLevel#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AccessContextManagerAccessLevelTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#timeouts AccessContextManagerAccessLevel#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AccessContextManagerAccessLevelTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelCustom",
    jsii_struct_bases=[],
    name_mapping={"expr": "expr"},
)
class AccessContextManagerAccessLevelCustom:
    def __init__(
        self,
        *,
        expr: typing.Union["AccessContextManagerAccessLevelCustomExpr", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param expr: expr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#expr AccessContextManagerAccessLevel#expr}
        '''
        if isinstance(expr, dict):
            expr = AccessContextManagerAccessLevelCustomExpr(**expr)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c361bf399276b55082af9ca9920ae51bc990e6268f4a421e087aa7686a8e07b)
            check_type(argname="argument expr", value=expr, expected_type=type_hints["expr"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expr": expr,
        }

    @builtins.property
    def expr(self) -> "AccessContextManagerAccessLevelCustomExpr":
        '''expr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#expr AccessContextManagerAccessLevel#expr}
        '''
        result = self._values.get("expr")
        assert result is not None, "Required property 'expr' is missing"
        return typing.cast("AccessContextManagerAccessLevelCustomExpr", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelCustom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelCustomExpr",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class AccessContextManagerAccessLevelCustomExpr:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#expression AccessContextManagerAccessLevel#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#description AccessContextManagerAccessLevel#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#location AccessContextManagerAccessLevel#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#title AccessContextManagerAccessLevel#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10d52c704dc0ae648b523b29e7f80ec8ece5e55f5418d6056a40c3929898db3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#expression AccessContextManagerAccessLevel#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#description AccessContextManagerAccessLevel#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#location AccessContextManagerAccessLevel#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#title AccessContextManagerAccessLevel#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelCustomExpr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerAccessLevelCustomExprOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelCustomExprOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa9bc41165b161829a4df7515f09d5a832e4be2f03139db85d8755ed84321e6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9d2f7225cca9f45312a08d288a8503a22e2395f98254e8bff9e371879acbf1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3cf27ccf99552bd3f55a8ae91c9437fe02b58c0b5efadd4743eca9c30a9a75f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b138830f838964093848fc15647edba09b8199133c4c550ccf90af1e55d6635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab55f921819bedc8d2c356a6f093149c69ee8e7a2e9eeaf40e2d0b1edfee7fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerAccessLevelCustomExpr]:
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelCustomExpr], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerAccessLevelCustomExpr],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb18e30425d361d2c2c06f5202550beba32ac760b13582f5acd684d297669b10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerAccessLevelCustomOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelCustomOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce8664bcbc9989a2833e8cfaf29ae2d080658f694bd6bbef5d62a4cc11657ebc)
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
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#expression AccessContextManagerAccessLevel#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#description AccessContextManagerAccessLevel#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#location AccessContextManagerAccessLevel#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#title AccessContextManagerAccessLevel#title}
        '''
        value = AccessContextManagerAccessLevelCustomExpr(
            expression=expression,
            description=description,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putExpr", [value]))

    @builtins.property
    @jsii.member(jsii_name="expr")
    def expr(self) -> AccessContextManagerAccessLevelCustomExprOutputReference:
        return typing.cast(AccessContextManagerAccessLevelCustomExprOutputReference, jsii.get(self, "expr"))

    @builtins.property
    @jsii.member(jsii_name="exprInput")
    def expr_input(self) -> typing.Optional[AccessContextManagerAccessLevelCustomExpr]:
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelCustomExpr], jsii.get(self, "exprInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AccessContextManagerAccessLevelCustom]:
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelCustom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerAccessLevelCustom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b46adbd198106139daba674ad07918ab72ab90748a4413802093c2511816c5c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class AccessContextManagerAccessLevelTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#create AccessContextManagerAccessLevel#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#delete AccessContextManagerAccessLevel#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#update AccessContextManagerAccessLevel#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fda5b7ac16028a7c17af3374cafc84c56ddbdc2c2180bcc68d171e8b5da93182)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#create AccessContextManagerAccessLevel#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#delete AccessContextManagerAccessLevel#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_access_level#update AccessContextManagerAccessLevel#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerAccessLevelTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevel.AccessContextManagerAccessLevelTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__567fce5b78f55750f70795ccdb7cd41a93d4f5d808462b77ca499cbae189aa2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24c8ad669fdfd35d42f508d485876e450fa2a442d78395580b7dc86365e478d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9153322e86e9b23f189c5e1eab76231c8613a2682681c077c4eb2679400e1651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e0e5ccac09cb6ebe29871f5abd1a8782ea85f33f96f25b5fa1c7e7ef8aef6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessContextManagerAccessLevelTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessContextManagerAccessLevelTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessContextManagerAccessLevelTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e9bf44e0ad8000ab9b16a1e0e28690d9d4c750397762bdff334177360a4ff94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AccessContextManagerAccessLevel",
    "AccessContextManagerAccessLevelBasic",
    "AccessContextManagerAccessLevelBasicConditions",
    "AccessContextManagerAccessLevelBasicConditionsDevicePolicy",
    "AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints",
    "AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraintsList",
    "AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraintsOutputReference",
    "AccessContextManagerAccessLevelBasicConditionsDevicePolicyOutputReference",
    "AccessContextManagerAccessLevelBasicConditionsList",
    "AccessContextManagerAccessLevelBasicConditionsOutputReference",
    "AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources",
    "AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesList",
    "AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesOutputReference",
    "AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetwork",
    "AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetworkOutputReference",
    "AccessContextManagerAccessLevelBasicOutputReference",
    "AccessContextManagerAccessLevelConfig",
    "AccessContextManagerAccessLevelCustom",
    "AccessContextManagerAccessLevelCustomExpr",
    "AccessContextManagerAccessLevelCustomExprOutputReference",
    "AccessContextManagerAccessLevelCustomOutputReference",
    "AccessContextManagerAccessLevelTimeouts",
    "AccessContextManagerAccessLevelTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f6728517009e6c355f865ccd130744e116c2e4ec44d644403a47cab568a88170(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    parent: builtins.str,
    title: builtins.str,
    basic: typing.Optional[typing.Union[AccessContextManagerAccessLevelBasic, typing.Dict[builtins.str, typing.Any]]] = None,
    custom: typing.Optional[typing.Union[AccessContextManagerAccessLevelCustom, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerAccessLevelTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c9b6fabf7d02a35aa880f4913a02c2a90bcad1889aa40bbe00d0296d9ef6aa93(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b9314e574cf19458d785bf6b619b00d4c22348622e276f807fe109fdb947ce3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1eaacefaf04fca0359bf447580aa495bfab45b2d44405fa8b47344e3334b38b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8d779f5c43551b7661ff88f80efca1bf3761606f9942598888d6d8513ee807(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a510e8ae853672ef520d0f01c40be102e4ef9f233b33e5b1102bd8df98799d23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0465edc3e1c6b074f2d609bd59ddf8837998f98376346313588dbec2bfc18233(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bcc17ba8f569eda97338e52a0bff79ce67c7c17fb9b88d373674721ff821cf4(
    *,
    conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelBasicConditions, typing.Dict[builtins.str, typing.Any]]]],
    combining_function: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eea1f5b3e29468e27559396f0c3d9343cda1e81e11bbf617c0099cb53d101b4(
    *,
    device_policy: typing.Optional[typing.Union[AccessContextManagerAccessLevelBasicConditionsDevicePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    ip_subnetworks: typing.Optional[typing.Sequence[builtins.str]] = None,
    members: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    required_access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_network_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a42f34c1c198950e7a1ae3b540e10105eaf07d78dc5db41b6457564479b7ca6(
    *,
    allowed_device_management_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_encryption_statuses: typing.Optional[typing.Sequence[builtins.str]] = None,
    os_constraints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    require_admin_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_corp_owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_screen_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83df9030369d715d0ce0545b054fc53cf67434e59b7401f14e95c058b80bee1c(
    *,
    os_type: builtins.str,
    minimum_version: typing.Optional[builtins.str] = None,
    require_verified_chrome_os: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc1a72d1f24a97ec889285fbc5a6203e25070cdee63e3d465e5818e0f06f90a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4c779dc849fac60c654642df4707eb9f29d1b9a8f29a3eeaf266d37e167e572(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9b854a869d6ae9ffd7d0ef761d702443d9aedf5a21bb7a03449d55afe2ef08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d617e0e18e1feb55ebebcecfbd6167ac460751ce16b43862a31e7908eb4139a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d40d680136995c39c7f8e4caeeeb36eb827fc334e21b985742aab996d05e75b6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08569111194a740c41e3753a5441fae2144b34f62df0b935e204c7ca37de95e4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b645a6996c954a81e4e373a223dcba083e652845f981d6f8978d6fd8276c2e07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15c231303f82452c029b1749909a7ff5ebe6f4d572d7ca64f78abc120c4bb36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fdda2faf9333573eca1a2573820aa5d82bb8d82c32a39779e2a987585bd199(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7946f93164483be6a3e04cf0ba9973433afc0011ac045e1f97bbdd0aedcb8eec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4412af7c66e47b7294861a3456d4575cda3f4ca282acc907b258d3f74285f6f8(
    value: typing.Optional[typing.Union[AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c5d444863fba7c2b6aa7288595eb700b832ae8aabfcde48341d0ae86c79e02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b469b640868539cc3884cef843ba8d3191c4f59a768bf0de81790d1bd5754b95(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelBasicConditionsDevicePolicyOsConstraints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae357049324d33f56b491143a03011c3c1bf1e8536a071dcfec916e3dcd0b44(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562e2c763446cd1cda90c69ace7766dd4cb9bddbc204d17611a34ca645ed6913(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44addc768326fb35629ee7ff425d7dffe755a54272a4ac189a3a2bb53f2341ee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d37f57680b7f12665be4239bea888a1988173206cfecd8ee26094f82a113e32(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a12d49d5ed1e9c22c07fd526d23c4e5ff3433f54291af35afc95d18506faedd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51bc21f39b82149bd956c5c0a62b22bb02d64ae52f870a1884f6e82c59af4143(
    value: typing.Optional[AccessContextManagerAccessLevelBasicConditionsDevicePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a564759365ebc86f5740a73af58f5f8e3d7c490e9db1ba06b499b58154593f98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d1ad5f8d8d0fb9edf4cd3971f28a56a5d671fb69d1c0581620a0a2921f45f3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0686fa06d336be3ba8d2235d36a2fef2e2b5b557c48e9d3718417d3c85a2729(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6709a6b4f93aef5fdf1fbd9dff694e6ea33da391f8106af213e69d04c02ba8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421ba8c392be8a1599bf1ce5ac7010d998a49b7f35a2ff49649375fa17ec227b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61d5d12c8902221dd12165b4dab824cc0e585fec80bae3b8efa51fe3a6ca72f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelBasicConditions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ca1ecb1fa74dcd56282d20fff156aef31c02729897bd1e1b5604951470a8ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02472ff1244a42da5a31348fa351fc200bd03e864b67fd7745e129278f8ddf61(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93aafdb96f8b1c57e6ab2d01e16022d93d4baae25bd4a9da2cc78c524a191c09(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32cd0473be1dcabcffc6c1d2a2a07d81c67774b79ece666c9451a6010342c0ed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c4e4994454d4b549c0fab02a0bcce10f030d1b938a2ab6b6737657b6a08568c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7c726fcec9ec056ec1eaa644f26b2406bcc010c3c83f5ec5cd325048fc09c1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3ea95e4fcfe6aa80c762e7c807c401e93279f2ab8c7735aa4b03ff721cf418(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1509bd5c00e9e2eec4e7ef6fbf9975b47766a27c32b8453acaaca12015c9fb0c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelBasicConditions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20370d481843ce1196e9746c78d3ecf606c90cb133cf072288aeaff8709a60bb(
    *,
    vpc_subnetwork: typing.Optional[typing.Union[AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetwork, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067e345b8ab0fff3ae366bbe77a1668aa24b15a09ff21d477321916a6ace643f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c084d863b92fee55c684fd8cc2674d7518054384c0113bce79c8254f078cfdd2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__803b77a5a16226c39c91e1800b7f9c8011c82a3ff257ddc86301e6b9174106a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5eecf081fbdc88eebd70eeeb8195d80454d7bdef5feb1f8a03cce33c65a6039(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1638a49f263a3e4adbad3964972dcf800b2e3581382eac10b41fd6b1d213890b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bba83f1d70143759823e013ff098161c1dc75c2349d945cea72b53c347d00c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1367e195098282823d8828284a90322f29c85b348edb44beba17ca0e6d0cf7f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286a0be872674428f750ea952fc8c3b40c2a1b3a256fdc228bc1f2a2f990f9ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAccessLevelBasicConditionsVpcNetworkSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01a65f98ccc24344422688f6ab6527e0811e323a7da0906dd15c120366b7896(
    *,
    network: builtins.str,
    vpc_ip_subnetworks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a122f3e15ea0bc370db7957ac1e4976f36c6226311aca1a87aea5a2611a20939(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec8ffd48af95193a11c4ce996998c37e61f71ba0035c968299976857d0947e00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737fc0f9697e8aa4acd0ed922313874eac5340b27ddcd4f80c6da32a1c7f6f24(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__202115f1ceaffcfd40efa9a4dc7be796bc3e9bf07fcffae115c964ea0ebd8436(
    value: typing.Optional[AccessContextManagerAccessLevelBasicConditionsVpcNetworkSourcesVpcSubnetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9299aef5a2ac73aef689eb6d8d1accab296dedf67dba5c4ff0eb2ebf7a608d44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c359c21d74ae66c4be234aacae158e8ce39115dc5ab8273df0ab8461e419046(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelBasicConditions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b2d30d767f91f32864d80e56eae96d51338da818cac1368eaa04d08c36c804(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7caf2d527661f98c694dd3ee8b67ba0d81d386282f82c954cf4eec1055bdb428(
    value: typing.Optional[AccessContextManagerAccessLevelBasic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552ee6c7cb7fc9d1d5e28f6da0ccb425d44b8c3b9ca810d8846cc2fcfcb0f245(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    parent: builtins.str,
    title: builtins.str,
    basic: typing.Optional[typing.Union[AccessContextManagerAccessLevelBasic, typing.Dict[builtins.str, typing.Any]]] = None,
    custom: typing.Optional[typing.Union[AccessContextManagerAccessLevelCustom, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerAccessLevelTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c361bf399276b55082af9ca9920ae51bc990e6268f4a421e087aa7686a8e07b(
    *,
    expr: typing.Union[AccessContextManagerAccessLevelCustomExpr, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10d52c704dc0ae648b523b29e7f80ec8ece5e55f5418d6056a40c3929898db3(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9bc41165b161829a4df7515f09d5a832e4be2f03139db85d8755ed84321e6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d2f7225cca9f45312a08d288a8503a22e2395f98254e8bff9e371879acbf1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3cf27ccf99552bd3f55a8ae91c9437fe02b58c0b5efadd4743eca9c30a9a75f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b138830f838964093848fc15647edba09b8199133c4c550ccf90af1e55d6635(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab55f921819bedc8d2c356a6f093149c69ee8e7a2e9eeaf40e2d0b1edfee7fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb18e30425d361d2c2c06f5202550beba32ac760b13582f5acd684d297669b10(
    value: typing.Optional[AccessContextManagerAccessLevelCustomExpr],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce8664bcbc9989a2833e8cfaf29ae2d080658f694bd6bbef5d62a4cc11657ebc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46adbd198106139daba674ad07918ab72ab90748a4413802093c2511816c5c6(
    value: typing.Optional[AccessContextManagerAccessLevelCustom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda5b7ac16028a7c17af3374cafc84c56ddbdc2c2180bcc68d171e8b5da93182(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567fce5b78f55750f70795ccdb7cd41a93d4f5d808462b77ca499cbae189aa2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c8ad669fdfd35d42f508d485876e450fa2a442d78395580b7dc86365e478d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9153322e86e9b23f189c5e1eab76231c8613a2682681c077c4eb2679400e1651(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e0e5ccac09cb6ebe29871f5abd1a8782ea85f33f96f25b5fa1c7e7ef8aef6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9bf44e0ad8000ab9b16a1e0e28690d9d4c750397762bdff334177360a4ff94(
    value: typing.Optional[typing.Union[AccessContextManagerAccessLevelTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

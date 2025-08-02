r'''
# `opentelekomcloud_waf_dedicated_cc_rule_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_waf_dedicated_cc_rule_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1).
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


class WafDedicatedCcRuleV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedCcRuleV1.WafDedicatedCcRuleV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1 opentelekomcloud_waf_dedicated_cc_rule_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDedicatedCcRuleV1Action", typing.Dict[builtins.str, typing.Any]]]],
        limit_num: jsii.Number,
        limit_period: jsii.Number,
        mode: jsii.Number,
        policy_id: builtins.str,
        tag_type: builtins.str,
        url: builtins.str,
        conditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDedicatedCcRuleV1Conditions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lock_time: typing.Optional[jsii.Number] = None,
        tag_category: typing.Optional[builtins.str] = None,
        tag_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_index: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["WafDedicatedCcRuleV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        unlock_num: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1 opentelekomcloud_waf_dedicated_cc_rule_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#action WafDedicatedCcRuleV1#action}
        :param limit_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#limit_num WafDedicatedCcRuleV1#limit_num}.
        :param limit_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#limit_period WafDedicatedCcRuleV1#limit_period}.
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#mode WafDedicatedCcRuleV1#mode}.
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#policy_id WafDedicatedCcRuleV1#policy_id}.
        :param tag_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#tag_type WafDedicatedCcRuleV1#tag_type}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#url WafDedicatedCcRuleV1#url}.
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#conditions WafDedicatedCcRuleV1#conditions}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#description WafDedicatedCcRuleV1#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#id WafDedicatedCcRuleV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lock_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#lock_time WafDedicatedCcRuleV1#lock_time}.
        :param tag_category: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#tag_category WafDedicatedCcRuleV1#tag_category}.
        :param tag_contents: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#tag_contents WafDedicatedCcRuleV1#tag_contents}.
        :param tag_index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#tag_index WafDedicatedCcRuleV1#tag_index}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#timeouts WafDedicatedCcRuleV1#timeouts}
        :param unlock_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#unlock_num WafDedicatedCcRuleV1#unlock_num}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a9ade86593d86eb0367ac15d2cfe1fca78376221a7db38c1be34391fc2d732)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WafDedicatedCcRuleV1Config(
            action=action,
            limit_num=limit_num,
            limit_period=limit_period,
            mode=mode,
            policy_id=policy_id,
            tag_type=tag_type,
            url=url,
            conditions=conditions,
            description=description,
            id=id,
            lock_time=lock_time,
            tag_category=tag_category,
            tag_contents=tag_contents,
            tag_index=tag_index,
            timeouts=timeouts,
            unlock_num=unlock_num,
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
        '''Generates CDKTF code for importing a WafDedicatedCcRuleV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WafDedicatedCcRuleV1 to import.
        :param import_from_id: The id of the existing WafDedicatedCcRuleV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WafDedicatedCcRuleV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd1b8e344915720d45665d64784a8573f770a35d4cf2bae69900f11f7153df49)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDedicatedCcRuleV1Action", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe13102638dcc9ea87f66d4fa23ba49642289ee09d1fae0777b06b388cce6264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDedicatedCcRuleV1Conditions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c140effca040127547700a2670cac60f6e507d6f8672215cc68b80b5fce08f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#create WafDedicatedCcRuleV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#delete WafDedicatedCcRuleV1#delete}.
        '''
        value = WafDedicatedCcRuleV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetConditions")
    def reset_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditions", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLockTime")
    def reset_lock_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLockTime", []))

    @jsii.member(jsii_name="resetTagCategory")
    def reset_tag_category(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagCategory", []))

    @jsii.member(jsii_name="resetTagContents")
    def reset_tag_contents(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagContents", []))

    @jsii.member(jsii_name="resetTagIndex")
    def reset_tag_index(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagIndex", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUnlockNum")
    def reset_unlock_num(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnlockNum", []))

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
    @jsii.member(jsii_name="action")
    def action(self) -> "WafDedicatedCcRuleV1ActionList":
        return typing.cast("WafDedicatedCcRuleV1ActionList", jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> "WafDedicatedCcRuleV1ConditionsList":
        return typing.cast("WafDedicatedCcRuleV1ConditionsList", jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "WafDedicatedCcRuleV1TimeoutsOutputReference":
        return typing.cast("WafDedicatedCcRuleV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedCcRuleV1Action"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedCcRuleV1Action"]]], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedCcRuleV1Conditions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedCcRuleV1Conditions"]]], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="limitNumInput")
    def limit_num_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "limitNumInput"))

    @builtins.property
    @jsii.member(jsii_name="limitPeriodInput")
    def limit_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "limitPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="lockTimeInput")
    def lock_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lockTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagCategoryInput")
    def tag_category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagCategoryInput"))

    @builtins.property
    @jsii.member(jsii_name="tagContentsInput")
    def tag_contents_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagContentsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagIndexInput")
    def tag_index_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="tagTypeInput")
    def tag_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WafDedicatedCcRuleV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WafDedicatedCcRuleV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="unlockNumInput")
    def unlock_num_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unlockNumInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__781e04c4530faad1fb5c6ebf291d117e4c02daba0d471a649ee16eeeffd8c896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a3ecb1835a9492d8c519f0b1db7ddb7a6529e84f888a4dd90667da9e7cf0c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limitNum")
    def limit_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limitNum"))

    @limit_num.setter
    def limit_num(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7103a62078cfe10087d08496b0d8829075f33b3477500c1bf9428edd0041b134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limitNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limitPeriod")
    def limit_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limitPeriod"))

    @limit_period.setter
    def limit_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42fd081b8194f8884e99e0d39a9ec44623520b101b93d3cc80fade1370d4e015)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limitPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lockTime")
    def lock_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lockTime"))

    @lock_time.setter
    def lock_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e467ff97d5ff15862b547dbc93e0019fa33d006c5ec65669afc2c03a15c2bfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lockTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfe78e295f7678e536e51d787664b1ab25aa048e760e762d9f7475bf39dab545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfbe3124a0b069076f0acab5329de1c21c6eac9e5b8613cb1536650869e6b14c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagCategory")
    def tag_category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagCategory"))

    @tag_category.setter
    def tag_category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be2a41a90f9543d0dc6d79d3531f6f6e79552741ad811a358b1c8931f99fbae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagCategory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagContents")
    def tag_contents(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tagContents"))

    @tag_contents.setter
    def tag_contents(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d4e9a2365ac0d64d3941fc9ae93cfe7b80c234598ad2f02205f8ade89d5fa71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagContents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagIndex")
    def tag_index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagIndex"))

    @tag_index.setter
    def tag_index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__623f36ceb979cd1a775da1766cdb8d2030cac3ad99be38c58c961f8cf4e66adc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagType")
    def tag_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagType"))

    @tag_type.setter
    def tag_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffcd8e0f55e896d97bc58eb88d81c0467087d414d42a4c1510c9a271e7d898e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unlockNum")
    def unlock_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unlockNum"))

    @unlock_num.setter
    def unlock_num(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dee6f1d7bfe4e263d377d90355038a8700fc74c399748d77f2aaa749c8dea43f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unlockNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60841a9fe799c23731e4e22f7ab0c55e2fcc7471d762326b39ec98f1395c8b12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedCcRuleV1.WafDedicatedCcRuleV1Action",
    jsii_struct_bases=[],
    name_mapping={
        "category": "category",
        "content": "content",
        "content_type": "contentType",
    },
)
class WafDedicatedCcRuleV1Action:
    def __init__(
        self,
        *,
        category: builtins.str,
        content: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param category: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#category WafDedicatedCcRuleV1#category}.
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#content WafDedicatedCcRuleV1#content}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#content_type WafDedicatedCcRuleV1#content_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__023f9df29e363d9f051ee896637a37f9f475d43bd0fbbc9b98e5894c7fc111d1)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "category": category,
        }
        if content is not None:
            self._values["content"] = content
        if content_type is not None:
            self._values["content_type"] = content_type

    @builtins.property
    def category(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#category WafDedicatedCcRuleV1#category}.'''
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#content WafDedicatedCcRuleV1#content}.'''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#content_type WafDedicatedCcRuleV1#content_type}.'''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedCcRuleV1Action(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDedicatedCcRuleV1ActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedCcRuleV1.WafDedicatedCcRuleV1ActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d48360884c67ce08b198cce6ad090ae5cf25f04b3ebf2f320d1ec31ab3f2c0a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "WafDedicatedCcRuleV1ActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bac9e2282f1ad6423d38dd7deb63fa51c035b144bb4e8fc230554f08313014d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WafDedicatedCcRuleV1ActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9409f0d549ec9ddc4e1d7f66bafecc06c315fca40a075dbc33e2bdbe51bb2006)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95d268a1ceb04fdd6b11613f65656ab8edc85703f6e2580d5cd64f9bb97aee3b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e48ea57a7fefadab8f27ff606ed32414686cc736e31dfed98d78d07f527f5bfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedCcRuleV1Action]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedCcRuleV1Action]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedCcRuleV1Action]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1b73d120865a706189b07b5e4ec28b904dc85683b885b46e8f353377b4200a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WafDedicatedCcRuleV1ActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedCcRuleV1.WafDedicatedCcRuleV1ActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6350badef32b07293273972af6a1242b96da7ccced19bccd039f63a34bb19570)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContent")
    def reset_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContent", []))

    @jsii.member(jsii_name="resetContentType")
    def reset_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentType", []))

    @builtins.property
    @jsii.member(jsii_name="categoryInput")
    def category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "categoryInput"))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @category.setter
    def category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0af93beb2a9851afaf5d7b73089fc6ab7301b4c4af0bc59b9ce48c84bd30b828)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "category", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f263d1f4b0a7150261de94f1229f150bc2f6f89e5be813957bfe019bf2b65dd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc756298fbbe1a5733b622e7dfe204cc19b46dcb0505d49869d90e29ab0a97af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedCcRuleV1Action]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedCcRuleV1Action]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedCcRuleV1Action]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6a1249596c81ed4d5464aabc4b603b6a886ed36ffc3e49ceda9a09d7c46158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedCcRuleV1.WafDedicatedCcRuleV1Conditions",
    jsii_struct_bases=[],
    name_mapping={
        "category": "category",
        "logic_operation": "logicOperation",
        "contents": "contents",
        "index": "index",
        "value_list_id": "valueListId",
    },
)
class WafDedicatedCcRuleV1Conditions:
    def __init__(
        self,
        *,
        category: builtins.str,
        logic_operation: builtins.str,
        contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        index: typing.Optional[builtins.str] = None,
        value_list_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param category: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#category WafDedicatedCcRuleV1#category}.
        :param logic_operation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#logic_operation WafDedicatedCcRuleV1#logic_operation}.
        :param contents: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#contents WafDedicatedCcRuleV1#contents}.
        :param index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#index WafDedicatedCcRuleV1#index}.
        :param value_list_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#value_list_id WafDedicatedCcRuleV1#value_list_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d95d499e07afa1f349cd9852f07c2a0860c3117fad933a18758ef4e197da4da)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument logic_operation", value=logic_operation, expected_type=type_hints["logic_operation"])
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument value_list_id", value=value_list_id, expected_type=type_hints["value_list_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "category": category,
            "logic_operation": logic_operation,
        }
        if contents is not None:
            self._values["contents"] = contents
        if index is not None:
            self._values["index"] = index
        if value_list_id is not None:
            self._values["value_list_id"] = value_list_id

    @builtins.property
    def category(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#category WafDedicatedCcRuleV1#category}.'''
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def logic_operation(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#logic_operation WafDedicatedCcRuleV1#logic_operation}.'''
        result = self._values.get("logic_operation")
        assert result is not None, "Required property 'logic_operation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def contents(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#contents WafDedicatedCcRuleV1#contents}.'''
        result = self._values.get("contents")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def index(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#index WafDedicatedCcRuleV1#index}.'''
        result = self._values.get("index")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_list_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#value_list_id WafDedicatedCcRuleV1#value_list_id}.'''
        result = self._values.get("value_list_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedCcRuleV1Conditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDedicatedCcRuleV1ConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedCcRuleV1.WafDedicatedCcRuleV1ConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ece2d147965b3f34e975da4fb874188b8c63e08fd4331412e49f056450884f69)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WafDedicatedCcRuleV1ConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fafe7aba5f7bc328639cf62c027dc44e9b58f1fbd451c5f28c3ac23b999170e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WafDedicatedCcRuleV1ConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fd3bdbe9cc68031463c8948ea0ada523d0d7617b45407751658e7461e226d1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51f7825cb197b8a02e1e43d5a87b789d1df55184cda4827abcb3022c092c0063)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d23cf9be0a80e83ff95f8040f80547245d34912d3a5f3f3c09765fcdcd1f038c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedCcRuleV1Conditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedCcRuleV1Conditions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedCcRuleV1Conditions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a91f08a57e4a776b3000fff06d5791af795833f16bd02a348beb72344dcaa10e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WafDedicatedCcRuleV1ConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedCcRuleV1.WafDedicatedCcRuleV1ConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__499b3fde0dbef8e0406fc5dd3498b3e0096dd0ce2a40ee8ad4e7e3643f06e23a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContents")
    def reset_contents(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContents", []))

    @jsii.member(jsii_name="resetIndex")
    def reset_index(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndex", []))

    @jsii.member(jsii_name="resetValueListId")
    def reset_value_list_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueListId", []))

    @builtins.property
    @jsii.member(jsii_name="categoryInput")
    def category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "categoryInput"))

    @builtins.property
    @jsii.member(jsii_name="contentsInput")
    def contents_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "contentsInput"))

    @builtins.property
    @jsii.member(jsii_name="indexInput")
    def index_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexInput"))

    @builtins.property
    @jsii.member(jsii_name="logicOperationInput")
    def logic_operation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logicOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="valueListIdInput")
    def value_list_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueListIdInput"))

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @category.setter
    def category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d65295c02a9b1a29c8e9de0e625f666dc6ab1378740f49516d91c5aec739681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "category", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contents")
    def contents(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "contents"))

    @contents.setter
    def contents(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74bc9a873f03ea600e0baf294a7e3e5da43e5ef49a165f2445b0b7be1eb6ee1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "index"))

    @index.setter
    def index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f7fbae7b473b7ed457477645cb5f749290b82737d3ff95e4dad1f663cffef55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "index", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logicOperation")
    def logic_operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logicOperation"))

    @logic_operation.setter
    def logic_operation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7582841bfb59042b22ccf9ba72df25cd5a985de9eff5d4b4d19a1174db86e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logicOperation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueListId")
    def value_list_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueListId"))

    @value_list_id.setter
    def value_list_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94fff43f5c5d7df05657d5dc0642636667e175fdb861c8c704b6f87c95d2d2cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueListId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedCcRuleV1Conditions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedCcRuleV1Conditions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedCcRuleV1Conditions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20c006cc924a139f123b4fde2bd7756495383250eabf0ef3bf08825e697e849f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedCcRuleV1.WafDedicatedCcRuleV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "action": "action",
        "limit_num": "limitNum",
        "limit_period": "limitPeriod",
        "mode": "mode",
        "policy_id": "policyId",
        "tag_type": "tagType",
        "url": "url",
        "conditions": "conditions",
        "description": "description",
        "id": "id",
        "lock_time": "lockTime",
        "tag_category": "tagCategory",
        "tag_contents": "tagContents",
        "tag_index": "tagIndex",
        "timeouts": "timeouts",
        "unlock_num": "unlockNum",
    },
)
class WafDedicatedCcRuleV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedCcRuleV1Action, typing.Dict[builtins.str, typing.Any]]]],
        limit_num: jsii.Number,
        limit_period: jsii.Number,
        mode: jsii.Number,
        policy_id: builtins.str,
        tag_type: builtins.str,
        url: builtins.str,
        conditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedCcRuleV1Conditions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lock_time: typing.Optional[jsii.Number] = None,
        tag_category: typing.Optional[builtins.str] = None,
        tag_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_index: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["WafDedicatedCcRuleV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        unlock_num: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#action WafDedicatedCcRuleV1#action}
        :param limit_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#limit_num WafDedicatedCcRuleV1#limit_num}.
        :param limit_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#limit_period WafDedicatedCcRuleV1#limit_period}.
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#mode WafDedicatedCcRuleV1#mode}.
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#policy_id WafDedicatedCcRuleV1#policy_id}.
        :param tag_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#tag_type WafDedicatedCcRuleV1#tag_type}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#url WafDedicatedCcRuleV1#url}.
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#conditions WafDedicatedCcRuleV1#conditions}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#description WafDedicatedCcRuleV1#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#id WafDedicatedCcRuleV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lock_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#lock_time WafDedicatedCcRuleV1#lock_time}.
        :param tag_category: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#tag_category WafDedicatedCcRuleV1#tag_category}.
        :param tag_contents: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#tag_contents WafDedicatedCcRuleV1#tag_contents}.
        :param tag_index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#tag_index WafDedicatedCcRuleV1#tag_index}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#timeouts WafDedicatedCcRuleV1#timeouts}
        :param unlock_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#unlock_num WafDedicatedCcRuleV1#unlock_num}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = WafDedicatedCcRuleV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9622c99f63703303c6967b7389590dcdc4cfc3e24731c8fffe67414d9123e3b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument limit_num", value=limit_num, expected_type=type_hints["limit_num"])
            check_type(argname="argument limit_period", value=limit_period, expected_type=type_hints["limit_period"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument tag_type", value=tag_type, expected_type=type_hints["tag_type"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lock_time", value=lock_time, expected_type=type_hints["lock_time"])
            check_type(argname="argument tag_category", value=tag_category, expected_type=type_hints["tag_category"])
            check_type(argname="argument tag_contents", value=tag_contents, expected_type=type_hints["tag_contents"])
            check_type(argname="argument tag_index", value=tag_index, expected_type=type_hints["tag_index"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument unlock_num", value=unlock_num, expected_type=type_hints["unlock_num"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "limit_num": limit_num,
            "limit_period": limit_period,
            "mode": mode,
            "policy_id": policy_id,
            "tag_type": tag_type,
            "url": url,
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
        if conditions is not None:
            self._values["conditions"] = conditions
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if lock_time is not None:
            self._values["lock_time"] = lock_time
        if tag_category is not None:
            self._values["tag_category"] = tag_category
        if tag_contents is not None:
            self._values["tag_contents"] = tag_contents
        if tag_index is not None:
            self._values["tag_index"] = tag_index
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if unlock_num is not None:
            self._values["unlock_num"] = unlock_num

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
    def action(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedCcRuleV1Action]]:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#action WafDedicatedCcRuleV1#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedCcRuleV1Action]], result)

    @builtins.property
    def limit_num(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#limit_num WafDedicatedCcRuleV1#limit_num}.'''
        result = self._values.get("limit_num")
        assert result is not None, "Required property 'limit_num' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def limit_period(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#limit_period WafDedicatedCcRuleV1#limit_period}.'''
        result = self._values.get("limit_period")
        assert result is not None, "Required property 'limit_period' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def mode(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#mode WafDedicatedCcRuleV1#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#policy_id WafDedicatedCcRuleV1#policy_id}.'''
        result = self._values.get("policy_id")
        assert result is not None, "Required property 'policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#tag_type WafDedicatedCcRuleV1#tag_type}.'''
        result = self._values.get("tag_type")
        assert result is not None, "Required property 'tag_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#url WafDedicatedCcRuleV1#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def conditions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedCcRuleV1Conditions]]]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#conditions WafDedicatedCcRuleV1#conditions}
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedCcRuleV1Conditions]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#description WafDedicatedCcRuleV1#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#id WafDedicatedCcRuleV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lock_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#lock_time WafDedicatedCcRuleV1#lock_time}.'''
        result = self._values.get("lock_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_category(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#tag_category WafDedicatedCcRuleV1#tag_category}.'''
        result = self._values.get("tag_category")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_contents(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#tag_contents WafDedicatedCcRuleV1#tag_contents}.'''
        result = self._values.get("tag_contents")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_index(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#tag_index WafDedicatedCcRuleV1#tag_index}.'''
        result = self._values.get("tag_index")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["WafDedicatedCcRuleV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#timeouts WafDedicatedCcRuleV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["WafDedicatedCcRuleV1Timeouts"], result)

    @builtins.property
    def unlock_num(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#unlock_num WafDedicatedCcRuleV1#unlock_num}.'''
        result = self._values.get("unlock_num")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedCcRuleV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedCcRuleV1.WafDedicatedCcRuleV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class WafDedicatedCcRuleV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#create WafDedicatedCcRuleV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#delete WafDedicatedCcRuleV1#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07c1f71e23c5c71b5deb5146326c8d4b0e87777a7abf35a431f28e5d981527c)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#create WafDedicatedCcRuleV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_cc_rule_v1#delete WafDedicatedCcRuleV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedCcRuleV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDedicatedCcRuleV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedCcRuleV1.WafDedicatedCcRuleV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a93f82a23a64373cd0836b390091ebe817e72d1d7fdd2a66fdc29dfe0c14285)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31cf0a49b1e123e83db517ad75ae5e24040e1fb509e39b97ed98cfef8cd5575d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a21eb2cde7d117e44f9c3317f4251b721e8be44bd592140c1ea5a2ef8267f8f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedCcRuleV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedCcRuleV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedCcRuleV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5344ca22198781ee58616ca07b27080c319cfaf8d05fff30403f6793baa61ebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WafDedicatedCcRuleV1",
    "WafDedicatedCcRuleV1Action",
    "WafDedicatedCcRuleV1ActionList",
    "WafDedicatedCcRuleV1ActionOutputReference",
    "WafDedicatedCcRuleV1Conditions",
    "WafDedicatedCcRuleV1ConditionsList",
    "WafDedicatedCcRuleV1ConditionsOutputReference",
    "WafDedicatedCcRuleV1Config",
    "WafDedicatedCcRuleV1Timeouts",
    "WafDedicatedCcRuleV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__75a9ade86593d86eb0367ac15d2cfe1fca78376221a7db38c1be34391fc2d732(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedCcRuleV1Action, typing.Dict[builtins.str, typing.Any]]]],
    limit_num: jsii.Number,
    limit_period: jsii.Number,
    mode: jsii.Number,
    policy_id: builtins.str,
    tag_type: builtins.str,
    url: builtins.str,
    conditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedCcRuleV1Conditions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lock_time: typing.Optional[jsii.Number] = None,
    tag_category: typing.Optional[builtins.str] = None,
    tag_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_index: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[WafDedicatedCcRuleV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    unlock_num: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__fd1b8e344915720d45665d64784a8573f770a35d4cf2bae69900f11f7153df49(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe13102638dcc9ea87f66d4fa23ba49642289ee09d1fae0777b06b388cce6264(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedCcRuleV1Action, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c140effca040127547700a2670cac60f6e507d6f8672215cc68b80b5fce08f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedCcRuleV1Conditions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__781e04c4530faad1fb5c6ebf291d117e4c02daba0d471a649ee16eeeffd8c896(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a3ecb1835a9492d8c519f0b1db7ddb7a6529e84f888a4dd90667da9e7cf0c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7103a62078cfe10087d08496b0d8829075f33b3477500c1bf9428edd0041b134(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42fd081b8194f8884e99e0d39a9ec44623520b101b93d3cc80fade1370d4e015(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e467ff97d5ff15862b547dbc93e0019fa33d006c5ec65669afc2c03a15c2bfe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe78e295f7678e536e51d787664b1ab25aa048e760e762d9f7475bf39dab545(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfbe3124a0b069076f0acab5329de1c21c6eac9e5b8613cb1536650869e6b14c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be2a41a90f9543d0dc6d79d3531f6f6e79552741ad811a358b1c8931f99fbae7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d4e9a2365ac0d64d3941fc9ae93cfe7b80c234598ad2f02205f8ade89d5fa71(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__623f36ceb979cd1a775da1766cdb8d2030cac3ad99be38c58c961f8cf4e66adc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffcd8e0f55e896d97bc58eb88d81c0467087d414d42a4c1510c9a271e7d898e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee6f1d7bfe4e263d377d90355038a8700fc74c399748d77f2aaa749c8dea43f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60841a9fe799c23731e4e22f7ab0c55e2fcc7471d762326b39ec98f1395c8b12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__023f9df29e363d9f051ee896637a37f9f475d43bd0fbbc9b98e5894c7fc111d1(
    *,
    category: builtins.str,
    content: typing.Optional[builtins.str] = None,
    content_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d48360884c67ce08b198cce6ad090ae5cf25f04b3ebf2f320d1ec31ab3f2c0a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bac9e2282f1ad6423d38dd7deb63fa51c035b144bb4e8fc230554f08313014d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9409f0d549ec9ddc4e1d7f66bafecc06c315fca40a075dbc33e2bdbe51bb2006(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d268a1ceb04fdd6b11613f65656ab8edc85703f6e2580d5cd64f9bb97aee3b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48ea57a7fefadab8f27ff606ed32414686cc736e31dfed98d78d07f527f5bfc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1b73d120865a706189b07b5e4ec28b904dc85683b885b46e8f353377b4200a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedCcRuleV1Action]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6350badef32b07293273972af6a1242b96da7ccced19bccd039f63a34bb19570(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0af93beb2a9851afaf5d7b73089fc6ab7301b4c4af0bc59b9ce48c84bd30b828(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f263d1f4b0a7150261de94f1229f150bc2f6f89e5be813957bfe019bf2b65dd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc756298fbbe1a5733b622e7dfe204cc19b46dcb0505d49869d90e29ab0a97af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6a1249596c81ed4d5464aabc4b603b6a886ed36ffc3e49ceda9a09d7c46158(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedCcRuleV1Action]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d95d499e07afa1f349cd9852f07c2a0860c3117fad933a18758ef4e197da4da(
    *,
    category: builtins.str,
    logic_operation: builtins.str,
    contents: typing.Optional[typing.Sequence[builtins.str]] = None,
    index: typing.Optional[builtins.str] = None,
    value_list_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece2d147965b3f34e975da4fb874188b8c63e08fd4331412e49f056450884f69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fafe7aba5f7bc328639cf62c027dc44e9b58f1fbd451c5f28c3ac23b999170e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd3bdbe9cc68031463c8948ea0ada523d0d7617b45407751658e7461e226d1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f7825cb197b8a02e1e43d5a87b789d1df55184cda4827abcb3022c092c0063(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23cf9be0a80e83ff95f8040f80547245d34912d3a5f3f3c09765fcdcd1f038c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91f08a57e4a776b3000fff06d5791af795833f16bd02a348beb72344dcaa10e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedCcRuleV1Conditions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499b3fde0dbef8e0406fc5dd3498b3e0096dd0ce2a40ee8ad4e7e3643f06e23a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d65295c02a9b1a29c8e9de0e625f666dc6ab1378740f49516d91c5aec739681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74bc9a873f03ea600e0baf294a7e3e5da43e5ef49a165f2445b0b7be1eb6ee1b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f7fbae7b473b7ed457477645cb5f749290b82737d3ff95e4dad1f663cffef55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7582841bfb59042b22ccf9ba72df25cd5a985de9eff5d4b4d19a1174db86e38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94fff43f5c5d7df05657d5dc0642636667e175fdb861c8c704b6f87c95d2d2cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c006cc924a139f123b4fde2bd7756495383250eabf0ef3bf08825e697e849f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedCcRuleV1Conditions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9622c99f63703303c6967b7389590dcdc4cfc3e24731c8fffe67414d9123e3b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedCcRuleV1Action, typing.Dict[builtins.str, typing.Any]]]],
    limit_num: jsii.Number,
    limit_period: jsii.Number,
    mode: jsii.Number,
    policy_id: builtins.str,
    tag_type: builtins.str,
    url: builtins.str,
    conditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedCcRuleV1Conditions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lock_time: typing.Optional[jsii.Number] = None,
    tag_category: typing.Optional[builtins.str] = None,
    tag_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_index: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[WafDedicatedCcRuleV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    unlock_num: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07c1f71e23c5c71b5deb5146326c8d4b0e87777a7abf35a431f28e5d981527c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a93f82a23a64373cd0836b390091ebe817e72d1d7fdd2a66fdc29dfe0c14285(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31cf0a49b1e123e83db517ad75ae5e24040e1fb509e39b97ed98cfef8cd5575d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21eb2cde7d117e44f9c3317f4251b721e8be44bd592140c1ea5a2ef8267f8f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5344ca22198781ee58616ca07b27080c319cfaf8d05fff30403f6793baa61ebb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedCcRuleV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

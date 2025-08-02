r'''
# `opentelekomcloud_waf_ccattackprotection_rule_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_waf_ccattackprotection_rule_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1).
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


class WafCcattackprotectionRuleV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafCcattackprotectionRuleV1.WafCcattackprotectionRuleV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1 opentelekomcloud_waf_ccattackprotection_rule_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action_category: builtins.str,
        limit_num: jsii.Number,
        limit_period: jsii.Number,
        policy_id: builtins.str,
        tag_type: builtins.str,
        url: builtins.str,
        block_content: typing.Optional[builtins.str] = None,
        block_content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lock_time: typing.Optional[jsii.Number] = None,
        tag_category: typing.Optional[builtins.str] = None,
        tag_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_index: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["WafCcattackprotectionRuleV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1 opentelekomcloud_waf_ccattackprotection_rule_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action_category: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#action_category WafCcattackprotectionRuleV1#action_category}.
        :param limit_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#limit_num WafCcattackprotectionRuleV1#limit_num}.
        :param limit_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#limit_period WafCcattackprotectionRuleV1#limit_period}.
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#policy_id WafCcattackprotectionRuleV1#policy_id}.
        :param tag_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#tag_type WafCcattackprotectionRuleV1#tag_type}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#url WafCcattackprotectionRuleV1#url}.
        :param block_content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#block_content WafCcattackprotectionRuleV1#block_content}.
        :param block_content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#block_content_type WafCcattackprotectionRuleV1#block_content_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#id WafCcattackprotectionRuleV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lock_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#lock_time WafCcattackprotectionRuleV1#lock_time}.
        :param tag_category: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#tag_category WafCcattackprotectionRuleV1#tag_category}.
        :param tag_contents: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#tag_contents WafCcattackprotectionRuleV1#tag_contents}.
        :param tag_index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#tag_index WafCcattackprotectionRuleV1#tag_index}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#timeouts WafCcattackprotectionRuleV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b32aafd66abaf894901761fc96e03d1d1e78e9cce3379f52fc2a908a79e9d8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WafCcattackprotectionRuleV1Config(
            action_category=action_category,
            limit_num=limit_num,
            limit_period=limit_period,
            policy_id=policy_id,
            tag_type=tag_type,
            url=url,
            block_content=block_content,
            block_content_type=block_content_type,
            id=id,
            lock_time=lock_time,
            tag_category=tag_category,
            tag_contents=tag_contents,
            tag_index=tag_index,
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
        '''Generates CDKTF code for importing a WafCcattackprotectionRuleV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WafCcattackprotectionRuleV1 to import.
        :param import_from_id: The id of the existing WafCcattackprotectionRuleV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WafCcattackprotectionRuleV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6efd5ce970fe8f8e905ec1775cd2c24635431c6f50d85f927289e84ccf598c64)
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
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#create WafCcattackprotectionRuleV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#delete WafCcattackprotectionRuleV1#delete}.
        '''
        value = WafCcattackprotectionRuleV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBlockContent")
    def reset_block_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockContent", []))

    @jsii.member(jsii_name="resetBlockContentType")
    def reset_block_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockContentType", []))

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
    @jsii.member(jsii_name="default")
    def default(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "WafCcattackprotectionRuleV1TimeoutsOutputReference":
        return typing.cast("WafCcattackprotectionRuleV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionCategoryInput")
    def action_category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionCategoryInput"))

    @builtins.property
    @jsii.member(jsii_name="blockContentInput")
    def block_content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockContentInput"))

    @builtins.property
    @jsii.member(jsii_name="blockContentTypeInput")
    def block_content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockContentTypeInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WafCcattackprotectionRuleV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WafCcattackprotectionRuleV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="actionCategory")
    def action_category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionCategory"))

    @action_category.setter
    def action_category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdacfba875fa941570857d58d25338d89c9f544bc7294eabb3d7900edc2d6b35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionCategory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="blockContent")
    def block_content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blockContent"))

    @block_content.setter
    def block_content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beba9f67bc6b5a5adf0b9e22d8ac44f14f9d93b076ae5d19eb53730b7878b78d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockContent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="blockContentType")
    def block_content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blockContentType"))

    @block_content_type.setter
    def block_content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b538594c04696b83c212a71b2373179b03b2e75e2a6cbafbc863ee4f2bd8bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockContentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d32e7ae76b89a250b7066b9c26ab98f38ad602c88eaddde1de8dc5af85c33d6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limitNum")
    def limit_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limitNum"))

    @limit_num.setter
    def limit_num(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ba885bf65cf0b7c7ec83ea62f8caf45d6824d0d0052e69e00eb8132bea944dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limitNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limitPeriod")
    def limit_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limitPeriod"))

    @limit_period.setter
    def limit_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a3f90f8f9117fc31aa49aa6b4272ac614c420d5f74bf225c9b6148afa609a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limitPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lockTime")
    def lock_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lockTime"))

    @lock_time.setter
    def lock_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e61302c01538871916c2a2fdd7a3a6b635a463941bab4a2b48ae717f6c9842b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lockTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81a44beb18a9b563e034db426b42a8f60399fac9d6b487cb63b38e951d5322b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagCategory")
    def tag_category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagCategory"))

    @tag_category.setter
    def tag_category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__121ef07d3a8dbd5cf4b90bd14361fbfdb96719a3c781df167c71410a9dda3522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagCategory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagContents")
    def tag_contents(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tagContents"))

    @tag_contents.setter
    def tag_contents(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b303880ffa9488cd321532b26c49e23315e9df42cffd1f8e8e91bff47041c998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagContents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagIndex")
    def tag_index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagIndex"))

    @tag_index.setter
    def tag_index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2146a7711f29d2d8973258e8d6b74057c2a7b60796d22ed9917e70ac6d2df4fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagType")
    def tag_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagType"))

    @tag_type.setter
    def tag_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__891d743a5f82d6f5ff5f3ec1eed582e17c932e798ca5cd92c5a7da0567fb8746)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0817cef61d2622a561725b1c04ab8f2c4f84ffc0ad975e85254ec5b85d03acab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafCcattackprotectionRuleV1.WafCcattackprotectionRuleV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "action_category": "actionCategory",
        "limit_num": "limitNum",
        "limit_period": "limitPeriod",
        "policy_id": "policyId",
        "tag_type": "tagType",
        "url": "url",
        "block_content": "blockContent",
        "block_content_type": "blockContentType",
        "id": "id",
        "lock_time": "lockTime",
        "tag_category": "tagCategory",
        "tag_contents": "tagContents",
        "tag_index": "tagIndex",
        "timeouts": "timeouts",
    },
)
class WafCcattackprotectionRuleV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        action_category: builtins.str,
        limit_num: jsii.Number,
        limit_period: jsii.Number,
        policy_id: builtins.str,
        tag_type: builtins.str,
        url: builtins.str,
        block_content: typing.Optional[builtins.str] = None,
        block_content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lock_time: typing.Optional[jsii.Number] = None,
        tag_category: typing.Optional[builtins.str] = None,
        tag_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_index: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["WafCcattackprotectionRuleV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action_category: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#action_category WafCcattackprotectionRuleV1#action_category}.
        :param limit_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#limit_num WafCcattackprotectionRuleV1#limit_num}.
        :param limit_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#limit_period WafCcattackprotectionRuleV1#limit_period}.
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#policy_id WafCcattackprotectionRuleV1#policy_id}.
        :param tag_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#tag_type WafCcattackprotectionRuleV1#tag_type}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#url WafCcattackprotectionRuleV1#url}.
        :param block_content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#block_content WafCcattackprotectionRuleV1#block_content}.
        :param block_content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#block_content_type WafCcattackprotectionRuleV1#block_content_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#id WafCcattackprotectionRuleV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lock_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#lock_time WafCcattackprotectionRuleV1#lock_time}.
        :param tag_category: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#tag_category WafCcattackprotectionRuleV1#tag_category}.
        :param tag_contents: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#tag_contents WafCcattackprotectionRuleV1#tag_contents}.
        :param tag_index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#tag_index WafCcattackprotectionRuleV1#tag_index}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#timeouts WafCcattackprotectionRuleV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = WafCcattackprotectionRuleV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe946aecf5ddb09686a60058d7471e74c9211462ea920f5066426316336f7399)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action_category", value=action_category, expected_type=type_hints["action_category"])
            check_type(argname="argument limit_num", value=limit_num, expected_type=type_hints["limit_num"])
            check_type(argname="argument limit_period", value=limit_period, expected_type=type_hints["limit_period"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument tag_type", value=tag_type, expected_type=type_hints["tag_type"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument block_content", value=block_content, expected_type=type_hints["block_content"])
            check_type(argname="argument block_content_type", value=block_content_type, expected_type=type_hints["block_content_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lock_time", value=lock_time, expected_type=type_hints["lock_time"])
            check_type(argname="argument tag_category", value=tag_category, expected_type=type_hints["tag_category"])
            check_type(argname="argument tag_contents", value=tag_contents, expected_type=type_hints["tag_contents"])
            check_type(argname="argument tag_index", value=tag_index, expected_type=type_hints["tag_index"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_category": action_category,
            "limit_num": limit_num,
            "limit_period": limit_period,
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
        if block_content is not None:
            self._values["block_content"] = block_content
        if block_content_type is not None:
            self._values["block_content_type"] = block_content_type
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
    def action_category(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#action_category WafCcattackprotectionRuleV1#action_category}.'''
        result = self._values.get("action_category")
        assert result is not None, "Required property 'action_category' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def limit_num(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#limit_num WafCcattackprotectionRuleV1#limit_num}.'''
        result = self._values.get("limit_num")
        assert result is not None, "Required property 'limit_num' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def limit_period(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#limit_period WafCcattackprotectionRuleV1#limit_period}.'''
        result = self._values.get("limit_period")
        assert result is not None, "Required property 'limit_period' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#policy_id WafCcattackprotectionRuleV1#policy_id}.'''
        result = self._values.get("policy_id")
        assert result is not None, "Required property 'policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#tag_type WafCcattackprotectionRuleV1#tag_type}.'''
        result = self._values.get("tag_type")
        assert result is not None, "Required property 'tag_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#url WafCcattackprotectionRuleV1#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def block_content(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#block_content WafCcattackprotectionRuleV1#block_content}.'''
        result = self._values.get("block_content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def block_content_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#block_content_type WafCcattackprotectionRuleV1#block_content_type}.'''
        result = self._values.get("block_content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#id WafCcattackprotectionRuleV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lock_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#lock_time WafCcattackprotectionRuleV1#lock_time}.'''
        result = self._values.get("lock_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_category(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#tag_category WafCcattackprotectionRuleV1#tag_category}.'''
        result = self._values.get("tag_category")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_contents(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#tag_contents WafCcattackprotectionRuleV1#tag_contents}.'''
        result = self._values.get("tag_contents")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_index(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#tag_index WafCcattackprotectionRuleV1#tag_index}.'''
        result = self._values.get("tag_index")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["WafCcattackprotectionRuleV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#timeouts WafCcattackprotectionRuleV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["WafCcattackprotectionRuleV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafCcattackprotectionRuleV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafCcattackprotectionRuleV1.WafCcattackprotectionRuleV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class WafCcattackprotectionRuleV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#create WafCcattackprotectionRuleV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#delete WafCcattackprotectionRuleV1#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7acb56bb4c66fc86ceb2fe311fb5947a91a94b6e4396535821f98491d9c1e016)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#create WafCcattackprotectionRuleV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_ccattackprotection_rule_v1#delete WafCcattackprotectionRuleV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafCcattackprotectionRuleV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafCcattackprotectionRuleV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafCcattackprotectionRuleV1.WafCcattackprotectionRuleV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3c68ea007e358f99d95c124e6b9979b3eb9bd0191a46a260175827d653993bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b4226e8243f1543307dff1ced9e484af43cf27b393e3277361f7bc1330a09db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__669bbb2d2703d5e45613c656e7b29b414b2e85cb526374516ded5b761e8ef115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafCcattackprotectionRuleV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafCcattackprotectionRuleV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafCcattackprotectionRuleV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bb958c935008442feb9649b055c235a2dbe4f9da292784e6ec45997735f67e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WafCcattackprotectionRuleV1",
    "WafCcattackprotectionRuleV1Config",
    "WafCcattackprotectionRuleV1Timeouts",
    "WafCcattackprotectionRuleV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b6b32aafd66abaf894901761fc96e03d1d1e78e9cce3379f52fc2a908a79e9d8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action_category: builtins.str,
    limit_num: jsii.Number,
    limit_period: jsii.Number,
    policy_id: builtins.str,
    tag_type: builtins.str,
    url: builtins.str,
    block_content: typing.Optional[builtins.str] = None,
    block_content_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lock_time: typing.Optional[jsii.Number] = None,
    tag_category: typing.Optional[builtins.str] = None,
    tag_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_index: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[WafCcattackprotectionRuleV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6efd5ce970fe8f8e905ec1775cd2c24635431c6f50d85f927289e84ccf598c64(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdacfba875fa941570857d58d25338d89c9f544bc7294eabb3d7900edc2d6b35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beba9f67bc6b5a5adf0b9e22d8ac44f14f9d93b076ae5d19eb53730b7878b78d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b538594c04696b83c212a71b2373179b03b2e75e2a6cbafbc863ee4f2bd8bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d32e7ae76b89a250b7066b9c26ab98f38ad602c88eaddde1de8dc5af85c33d6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba885bf65cf0b7c7ec83ea62f8caf45d6824d0d0052e69e00eb8132bea944dd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a3f90f8f9117fc31aa49aa6b4272ac614c420d5f74bf225c9b6148afa609a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e61302c01538871916c2a2fdd7a3a6b635a463941bab4a2b48ae717f6c9842b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a44beb18a9b563e034db426b42a8f60399fac9d6b487cb63b38e951d5322b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__121ef07d3a8dbd5cf4b90bd14361fbfdb96719a3c781df167c71410a9dda3522(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b303880ffa9488cd321532b26c49e23315e9df42cffd1f8e8e91bff47041c998(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2146a7711f29d2d8973258e8d6b74057c2a7b60796d22ed9917e70ac6d2df4fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891d743a5f82d6f5ff5f3ec1eed582e17c932e798ca5cd92c5a7da0567fb8746(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0817cef61d2622a561725b1c04ab8f2c4f84ffc0ad975e85254ec5b85d03acab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe946aecf5ddb09686a60058d7471e74c9211462ea920f5066426316336f7399(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action_category: builtins.str,
    limit_num: jsii.Number,
    limit_period: jsii.Number,
    policy_id: builtins.str,
    tag_type: builtins.str,
    url: builtins.str,
    block_content: typing.Optional[builtins.str] = None,
    block_content_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lock_time: typing.Optional[jsii.Number] = None,
    tag_category: typing.Optional[builtins.str] = None,
    tag_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_index: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[WafCcattackprotectionRuleV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7acb56bb4c66fc86ceb2fe311fb5947a91a94b6e4396535821f98491d9c1e016(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3c68ea007e358f99d95c124e6b9979b3eb9bd0191a46a260175827d653993bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b4226e8243f1543307dff1ced9e484af43cf27b393e3277361f7bc1330a09db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__669bbb2d2703d5e45613c656e7b29b414b2e85cb526374516ded5b761e8ef115(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb958c935008442feb9649b055c235a2dbe4f9da292784e6ec45997735f67e2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafCcattackprotectionRuleV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

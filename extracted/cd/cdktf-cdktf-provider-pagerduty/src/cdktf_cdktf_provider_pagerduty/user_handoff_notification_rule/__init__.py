r'''
# `pagerduty_user_handoff_notification_rule`

Refer to the Terraform Registry for docs: [`pagerduty_user_handoff_notification_rule`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule).
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


class UserHandoffNotificationRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.userHandoffNotificationRule.UserHandoffNotificationRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule pagerduty_user_handoff_notification_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        notify_advance_in_minutes: jsii.Number,
        user_id: builtins.str,
        contact_method: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["UserHandoffNotificationRuleContactMethod", typing.Dict[builtins.str, typing.Any]]]]] = None,
        handoff_type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule pagerduty_user_handoff_notification_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param notify_advance_in_minutes: The number of minutes before the handoff to notify the user. Must be greater than or equal to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule#notify_advance_in_minutes UserHandoffNotificationRule#notify_advance_in_minutes}
        :param user_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule#user_id UserHandoffNotificationRule#user_id}.
        :param contact_method: contact_method block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule#contact_method UserHandoffNotificationRule#contact_method}
        :param handoff_type: The type of handoff to notify for. Possible values are 'both', 'oncall', 'offcall'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule#handoff_type UserHandoffNotificationRule#handoff_type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be9acd4a984e42a30c25cdd5055a79e999fb4f793aa08a819c51f1d42809afe6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = UserHandoffNotificationRuleConfig(
            notify_advance_in_minutes=notify_advance_in_minutes,
            user_id=user_id,
            contact_method=contact_method,
            handoff_type=handoff_type,
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
        '''Generates CDKTF code for importing a UserHandoffNotificationRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the UserHandoffNotificationRule to import.
        :param import_from_id: The id of the existing UserHandoffNotificationRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the UserHandoffNotificationRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b0d37f39fb73652cf0aeb9ddeb18edafc9c99d6049eb722086ffdae7567526)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putContactMethod")
    def put_contact_method(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["UserHandoffNotificationRuleContactMethod", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e949bd3b71b3b794588cfd6b6a299c2d970ed7655d23c8efabc847a2949c85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContactMethod", [value]))

    @jsii.member(jsii_name="resetContactMethod")
    def reset_contact_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContactMethod", []))

    @jsii.member(jsii_name="resetHandoffType")
    def reset_handoff_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHandoffType", []))

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
    @jsii.member(jsii_name="contactMethod")
    def contact_method(self) -> "UserHandoffNotificationRuleContactMethodList":
        return typing.cast("UserHandoffNotificationRuleContactMethodList", jsii.get(self, "contactMethod"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="contactMethodInput")
    def contact_method_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["UserHandoffNotificationRuleContactMethod"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["UserHandoffNotificationRuleContactMethod"]]], jsii.get(self, "contactMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="handoffTypeInput")
    def handoff_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "handoffTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyAdvanceInMinutesInput")
    def notify_advance_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "notifyAdvanceInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdInput")
    def user_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userIdInput"))

    @builtins.property
    @jsii.member(jsii_name="handoffType")
    def handoff_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "handoffType"))

    @handoff_type.setter
    def handoff_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3ec3c84ae7dd7ff7d4cca10e5dae208610ad74d7454591eabd0dfadfc17f130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "handoffType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notifyAdvanceInMinutes")
    def notify_advance_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "notifyAdvanceInMinutes"))

    @notify_advance_in_minutes.setter
    def notify_advance_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e20e10a8292a6699876390c0f40c82e2527eb97b34eb441f3bfa9798e495ffe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyAdvanceInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @user_id.setter
    def user_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__917c697e12d1b43b4dd1f61ecf48bb24f2534a62d533956a0394406476cca618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.userHandoffNotificationRule.UserHandoffNotificationRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "notify_advance_in_minutes": "notifyAdvanceInMinutes",
        "user_id": "userId",
        "contact_method": "contactMethod",
        "handoff_type": "handoffType",
    },
)
class UserHandoffNotificationRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        notify_advance_in_minutes: jsii.Number,
        user_id: builtins.str,
        contact_method: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["UserHandoffNotificationRuleContactMethod", typing.Dict[builtins.str, typing.Any]]]]] = None,
        handoff_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param notify_advance_in_minutes: The number of minutes before the handoff to notify the user. Must be greater than or equal to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule#notify_advance_in_minutes UserHandoffNotificationRule#notify_advance_in_minutes}
        :param user_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule#user_id UserHandoffNotificationRule#user_id}.
        :param contact_method: contact_method block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule#contact_method UserHandoffNotificationRule#contact_method}
        :param handoff_type: The type of handoff to notify for. Possible values are 'both', 'oncall', 'offcall'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule#handoff_type UserHandoffNotificationRule#handoff_type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bbe373c32f6cbdffe57eb37b36993d10e59b22df145b4a039c917de7e499889)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument notify_advance_in_minutes", value=notify_advance_in_minutes, expected_type=type_hints["notify_advance_in_minutes"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            check_type(argname="argument contact_method", value=contact_method, expected_type=type_hints["contact_method"])
            check_type(argname="argument handoff_type", value=handoff_type, expected_type=type_hints["handoff_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "notify_advance_in_minutes": notify_advance_in_minutes,
            "user_id": user_id,
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
        if contact_method is not None:
            self._values["contact_method"] = contact_method
        if handoff_type is not None:
            self._values["handoff_type"] = handoff_type

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
    def notify_advance_in_minutes(self) -> jsii.Number:
        '''The number of minutes before the handoff to notify the user. Must be greater than or equal to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule#notify_advance_in_minutes UserHandoffNotificationRule#notify_advance_in_minutes}
        '''
        result = self._values.get("notify_advance_in_minutes")
        assert result is not None, "Required property 'notify_advance_in_minutes' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def user_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule#user_id UserHandoffNotificationRule#user_id}.'''
        result = self._values.get("user_id")
        assert result is not None, "Required property 'user_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def contact_method(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["UserHandoffNotificationRuleContactMethod"]]]:
        '''contact_method block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule#contact_method UserHandoffNotificationRule#contact_method}
        '''
        result = self._values.get("contact_method")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["UserHandoffNotificationRuleContactMethod"]]], result)

    @builtins.property
    def handoff_type(self) -> typing.Optional[builtins.str]:
        '''The type of handoff to notify for. Possible values are 'both', 'oncall', 'offcall'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule#handoff_type UserHandoffNotificationRule#handoff_type}
        '''
        result = self._values.get("handoff_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserHandoffNotificationRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.userHandoffNotificationRule.UserHandoffNotificationRuleContactMethod",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "type": "type"},
)
class UserHandoffNotificationRuleContactMethod:
    def __init__(self, *, id: builtins.str, type: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule#id UserHandoffNotificationRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param type: The type of contact method to notify for. Possible values are 'email_contact_method', 'email_contact_method_reference', 'phone_contact_method', 'phone_contact_method_reference', 'push_notification_contact_method', 'push_notification_contact_method_reference', 'sms_contact_method', 'sms_contact_method_reference'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule#type UserHandoffNotificationRule#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f45730d10d147bf610802d9b207c8dee3709fd964cc69a6f239033cf5f4b94)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "type": type,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule#id UserHandoffNotificationRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of contact method to notify for. Possible values are 'email_contact_method', 'email_contact_method_reference', 'phone_contact_method', 'phone_contact_method_reference', 'push_notification_contact_method', 'push_notification_contact_method_reference', 'sms_contact_method', 'sms_contact_method_reference'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/user_handoff_notification_rule#type UserHandoffNotificationRule#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserHandoffNotificationRuleContactMethod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserHandoffNotificationRuleContactMethodList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.userHandoffNotificationRule.UserHandoffNotificationRuleContactMethodList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4811b94bbd68dad081282eb73d7db8a815690201b6977cf5453b6000c11097a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserHandoffNotificationRuleContactMethodOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f6efd518eedd846d92aba1f941a00a93aa8fd8ebdf412ff81dce72fda692b8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserHandoffNotificationRuleContactMethodOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d1f26c60a6eeda94350f8be26a5e8f7445aee4edc7a2e73dc187f4b4230623f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__142ba1a23c7b87dcc7e11521a0557c970d63c24e34328ebc7ebfc07c52b830ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3ba3e8c0f5bbbd6de0b24b08db51e7512e25f6b75a0b9d1b9f4665413eee51a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserHandoffNotificationRuleContactMethod]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserHandoffNotificationRuleContactMethod]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserHandoffNotificationRuleContactMethod]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93420676e84948a63d57f975487f4a460e17a01cea890be6b12905451eb8805d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class UserHandoffNotificationRuleContactMethodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.userHandoffNotificationRule.UserHandoffNotificationRuleContactMethodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b6bb51d1279cb5c60cccc4a9219d4bed443d90cb56b66de88fe481d8c312935)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__644eecdd727407bebee3e24945b9753f43139b1af1bf7783263cb133de3c653f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d40db1d3d4363a0c1c5de7f6499b554edb787c7fd9f2329dbcfa914e9f11859d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, UserHandoffNotificationRuleContactMethod]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, UserHandoffNotificationRuleContactMethod]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, UserHandoffNotificationRuleContactMethod]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__442eb9f24397853d6af24d4e85501fc83549c4ed5144b41b5d8b26d10c0e0775)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "UserHandoffNotificationRule",
    "UserHandoffNotificationRuleConfig",
    "UserHandoffNotificationRuleContactMethod",
    "UserHandoffNotificationRuleContactMethodList",
    "UserHandoffNotificationRuleContactMethodOutputReference",
]

publication.publish()

def _typecheckingstub__be9acd4a984e42a30c25cdd5055a79e999fb4f793aa08a819c51f1d42809afe6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    notify_advance_in_minutes: jsii.Number,
    user_id: builtins.str,
    contact_method: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[UserHandoffNotificationRuleContactMethod, typing.Dict[builtins.str, typing.Any]]]]] = None,
    handoff_type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__39b0d37f39fb73652cf0aeb9ddeb18edafc9c99d6049eb722086ffdae7567526(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e949bd3b71b3b794588cfd6b6a299c2d970ed7655d23c8efabc847a2949c85(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[UserHandoffNotificationRuleContactMethod, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ec3c84ae7dd7ff7d4cca10e5dae208610ad74d7454591eabd0dfadfc17f130(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e20e10a8292a6699876390c0f40c82e2527eb97b34eb441f3bfa9798e495ffe7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917c697e12d1b43b4dd1f61ecf48bb24f2534a62d533956a0394406476cca618(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bbe373c32f6cbdffe57eb37b36993d10e59b22df145b4a039c917de7e499889(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    notify_advance_in_minutes: jsii.Number,
    user_id: builtins.str,
    contact_method: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[UserHandoffNotificationRuleContactMethod, typing.Dict[builtins.str, typing.Any]]]]] = None,
    handoff_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f45730d10d147bf610802d9b207c8dee3709fd964cc69a6f239033cf5f4b94(
    *,
    id: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4811b94bbd68dad081282eb73d7db8a815690201b6977cf5453b6000c11097a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f6efd518eedd846d92aba1f941a00a93aa8fd8ebdf412ff81dce72fda692b8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d1f26c60a6eeda94350f8be26a5e8f7445aee4edc7a2e73dc187f4b4230623f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142ba1a23c7b87dcc7e11521a0557c970d63c24e34328ebc7ebfc07c52b830ea(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3ba3e8c0f5bbbd6de0b24b08db51e7512e25f6b75a0b9d1b9f4665413eee51a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93420676e84948a63d57f975487f4a460e17a01cea890be6b12905451eb8805d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserHandoffNotificationRuleContactMethod]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6bb51d1279cb5c60cccc4a9219d4bed443d90cb56b66de88fe481d8c312935(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644eecdd727407bebee3e24945b9753f43139b1af1bf7783263cb133de3c653f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d40db1d3d4363a0c1c5de7f6499b554edb787c7fd9f2329dbcfa914e9f11859d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__442eb9f24397853d6af24d4e85501fc83549c4ed5144b41b5d8b26d10c0e0775(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, UserHandoffNotificationRuleContactMethod]],
) -> None:
    """Type checking stubs"""
    pass

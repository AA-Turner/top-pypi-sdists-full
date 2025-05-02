r'''
# `aws_cognito_risk_configuration`

Refer to the Terraform Registry for docs: [`aws_cognito_risk_configuration`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration).
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


class CognitoRiskConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration aws_cognito_risk_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        user_pool_id: builtins.str,
        account_takeover_risk_configuration: typing.Optional[typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        client_id: typing.Optional[builtins.str] = None,
        compromised_credentials_risk_configuration: typing.Optional[typing.Union["CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        risk_exception_configuration: typing.Optional[typing.Union["CognitoRiskConfigurationRiskExceptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration aws_cognito_risk_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param user_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#user_pool_id CognitoRiskConfiguration#user_pool_id}.
        :param account_takeover_risk_configuration: account_takeover_risk_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#account_takeover_risk_configuration CognitoRiskConfiguration#account_takeover_risk_configuration}
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#client_id CognitoRiskConfiguration#client_id}.
        :param compromised_credentials_risk_configuration: compromised_credentials_risk_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#compromised_credentials_risk_configuration CognitoRiskConfiguration#compromised_credentials_risk_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#id CognitoRiskConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param risk_exception_configuration: risk_exception_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#risk_exception_configuration CognitoRiskConfiguration#risk_exception_configuration}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee5bd88f254a14a346bc366ba5e420a19bd04c9f76e02911ff52d9371013c256)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CognitoRiskConfigurationConfig(
            user_pool_id=user_pool_id,
            account_takeover_risk_configuration=account_takeover_risk_configuration,
            client_id=client_id,
            compromised_credentials_risk_configuration=compromised_credentials_risk_configuration,
            id=id,
            risk_exception_configuration=risk_exception_configuration,
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
        '''Generates CDKTF code for importing a CognitoRiskConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CognitoRiskConfiguration to import.
        :param import_from_id: The id of the existing CognitoRiskConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CognitoRiskConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f1aa037e15e2a7e95575d2e8af3ae22995cc187ed239a699c37f9f2ca721a4f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccountTakeoverRiskConfiguration")
    def put_account_takeover_risk_configuration(
        self,
        *,
        actions: typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions", typing.Dict[builtins.str, typing.Any]],
        notify_configuration: typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#actions CognitoRiskConfiguration#actions}
        :param notify_configuration: notify_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#notify_configuration CognitoRiskConfiguration#notify_configuration}
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfiguration(
            actions=actions, notify_configuration=notify_configuration
        )

        return typing.cast(None, jsii.invoke(self, "putAccountTakeoverRiskConfiguration", [value]))

    @jsii.member(jsii_name="putCompromisedCredentialsRiskConfiguration")
    def put_compromised_credentials_risk_configuration(
        self,
        *,
        actions: typing.Union["CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions", typing.Dict[builtins.str, typing.Any]],
        event_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#actions CognitoRiskConfiguration#actions}
        :param event_filter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#event_filter CognitoRiskConfiguration#event_filter}.
        '''
        value = CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration(
            actions=actions, event_filter=event_filter
        )

        return typing.cast(None, jsii.invoke(self, "putCompromisedCredentialsRiskConfiguration", [value]))

    @jsii.member(jsii_name="putRiskExceptionConfiguration")
    def put_risk_exception_configuration(
        self,
        *,
        blocked_ip_range_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        skipped_ip_range_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param blocked_ip_range_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#blocked_ip_range_list CognitoRiskConfiguration#blocked_ip_range_list}.
        :param skipped_ip_range_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#skipped_ip_range_list CognitoRiskConfiguration#skipped_ip_range_list}.
        '''
        value = CognitoRiskConfigurationRiskExceptionConfiguration(
            blocked_ip_range_list=blocked_ip_range_list,
            skipped_ip_range_list=skipped_ip_range_list,
        )

        return typing.cast(None, jsii.invoke(self, "putRiskExceptionConfiguration", [value]))

    @jsii.member(jsii_name="resetAccountTakeoverRiskConfiguration")
    def reset_account_takeover_risk_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountTakeoverRiskConfiguration", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetCompromisedCredentialsRiskConfiguration")
    def reset_compromised_credentials_risk_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompromisedCredentialsRiskConfiguration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRiskExceptionConfiguration")
    def reset_risk_exception_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRiskExceptionConfiguration", []))

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
    @jsii.member(jsii_name="accountTakeoverRiskConfiguration")
    def account_takeover_risk_configuration(
        self,
    ) -> "CognitoRiskConfigurationAccountTakeoverRiskConfigurationOutputReference":
        return typing.cast("CognitoRiskConfigurationAccountTakeoverRiskConfigurationOutputReference", jsii.get(self, "accountTakeoverRiskConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="compromisedCredentialsRiskConfiguration")
    def compromised_credentials_risk_configuration(
        self,
    ) -> "CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationOutputReference":
        return typing.cast("CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationOutputReference", jsii.get(self, "compromisedCredentialsRiskConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="riskExceptionConfiguration")
    def risk_exception_configuration(
        self,
    ) -> "CognitoRiskConfigurationRiskExceptionConfigurationOutputReference":
        return typing.cast("CognitoRiskConfigurationRiskExceptionConfigurationOutputReference", jsii.get(self, "riskExceptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="accountTakeoverRiskConfigurationInput")
    def account_takeover_risk_configuration_input(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfiguration"]:
        return typing.cast(typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfiguration"], jsii.get(self, "accountTakeoverRiskConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="compromisedCredentialsRiskConfigurationInput")
    def compromised_credentials_risk_configuration_input(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration"]:
        return typing.cast(typing.Optional["CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration"], jsii.get(self, "compromisedCredentialsRiskConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="riskExceptionConfigurationInput")
    def risk_exception_configuration_input(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationRiskExceptionConfiguration"]:
        return typing.cast(typing.Optional["CognitoRiskConfigurationRiskExceptionConfiguration"], jsii.get(self, "riskExceptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="userPoolIdInput")
    def user_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afefc8dbc8d87b39c7578bf0dbf8ded92bad6a3e270164583bfe50e3796caf71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8edfcdfc624e7fece40b71bff9552296632679337afeebd790e11163175f2b51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPoolId"))

    @user_pool_id.setter
    def user_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c3dea987d5ccffe22b903f662cbc1cc6bc9d308681e3b74fbc6a00b2284d57d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPoolId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfiguration",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions", "notify_configuration": "notifyConfiguration"},
)
class CognitoRiskConfigurationAccountTakeoverRiskConfiguration:
    def __init__(
        self,
        *,
        actions: typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions", typing.Dict[builtins.str, typing.Any]],
        notify_configuration: typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#actions CognitoRiskConfiguration#actions}
        :param notify_configuration: notify_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#notify_configuration CognitoRiskConfiguration#notify_configuration}
        '''
        if isinstance(actions, dict):
            actions = CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions(**actions)
        if isinstance(notify_configuration, dict):
            notify_configuration = CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration(**notify_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b936500b484783e7891ed8e6190e5e59924fe5b267a63960f1b4b2073ee3cf45)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument notify_configuration", value=notify_configuration, expected_type=type_hints["notify_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "notify_configuration": notify_configuration,
        }

    @builtins.property
    def actions(
        self,
    ) -> "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions":
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#actions CognitoRiskConfiguration#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast("CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions", result)

    @builtins.property
    def notify_configuration(
        self,
    ) -> "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration":
        '''notify_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#notify_configuration CognitoRiskConfiguration#notify_configuration}
        '''
        result = self._values.get("notify_configuration")
        assert result is not None, "Required property 'notify_configuration' is missing"
        return typing.cast("CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions",
    jsii_struct_bases=[],
    name_mapping={
        "high_action": "highAction",
        "low_action": "lowAction",
        "medium_action": "mediumAction",
    },
)
class CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions:
    def __init__(
        self,
        *,
        high_action: typing.Optional[typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction", typing.Dict[builtins.str, typing.Any]]] = None,
        low_action: typing.Optional[typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction", typing.Dict[builtins.str, typing.Any]]] = None,
        medium_action: typing.Optional[typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param high_action: high_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#high_action CognitoRiskConfiguration#high_action}
        :param low_action: low_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#low_action CognitoRiskConfiguration#low_action}
        :param medium_action: medium_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#medium_action CognitoRiskConfiguration#medium_action}
        '''
        if isinstance(high_action, dict):
            high_action = CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction(**high_action)
        if isinstance(low_action, dict):
            low_action = CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction(**low_action)
        if isinstance(medium_action, dict):
            medium_action = CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction(**medium_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dfcb874bc66fbb3c7df2b3883a2699c36736596d92b2b73b7e2c702a7a444a6)
            check_type(argname="argument high_action", value=high_action, expected_type=type_hints["high_action"])
            check_type(argname="argument low_action", value=low_action, expected_type=type_hints["low_action"])
            check_type(argname="argument medium_action", value=medium_action, expected_type=type_hints["medium_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if high_action is not None:
            self._values["high_action"] = high_action
        if low_action is not None:
            self._values["low_action"] = low_action
        if medium_action is not None:
            self._values["medium_action"] = medium_action

    @builtins.property
    def high_action(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction"]:
        '''high_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#high_action CognitoRiskConfiguration#high_action}
        '''
        result = self._values.get("high_action")
        return typing.cast(typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction"], result)

    @builtins.property
    def low_action(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction"]:
        '''low_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#low_action CognitoRiskConfiguration#low_action}
        '''
        result = self._values.get("low_action")
        return typing.cast(typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction"], result)

    @builtins.property
    def medium_action(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction"]:
        '''medium_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#medium_action CognitoRiskConfiguration#medium_action}
        '''
        result = self._values.get("medium_action")
        return typing.cast(typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction",
    jsii_struct_bases=[],
    name_mapping={"event_action": "eventAction", "notify": "notify"},
)
class CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction:
    def __init__(
        self,
        *,
        event_action: builtins.str,
        notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.
        :param notify: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b96249ffb69c4af97b84817009550b8d2a94f30fb30bef0a64d198fbff2635)
            check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
            check_type(argname="argument notify", value=notify, expected_type=type_hints["notify"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_action": event_action,
            "notify": notify,
        }

    @builtins.property
    def event_action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.'''
        result = self._values.get("event_action")
        assert result is not None, "Required property 'event_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.'''
        result = self._values.get("notify")
        assert result is not None, "Required property 'notify' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cf9f6101438aeb384b6741fe2e1fde66a53bbd5147a0d733ce58e4e8c5ad7d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="eventActionInput")
    def event_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventActionInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyInput")
    def notify_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "notifyInput"))

    @builtins.property
    @jsii.member(jsii_name="eventAction")
    def event_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventAction"))

    @event_action.setter
    def event_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7fe5ec6320de050a142ffbd7201dce99f86237d8bfcdba422205fd4aa74270d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notify")
    def notify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "notify"))

    @notify.setter
    def notify(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__548b5c1ba4215a43bc19778da679d7b82a15be390449d66646ae89aa9aad91f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notify", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__147abb3c09a4693a271a6fbc0855f1f3cc2a5dc0cf9a667f28c3e8fd490ae34c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction",
    jsii_struct_bases=[],
    name_mapping={"event_action": "eventAction", "notify": "notify"},
)
class CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction:
    def __init__(
        self,
        *,
        event_action: builtins.str,
        notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.
        :param notify: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3060780a98e92533bc35623f9e28da0c3311eb650637cefddc7c462a2641e26)
            check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
            check_type(argname="argument notify", value=notify, expected_type=type_hints["notify"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_action": event_action,
            "notify": notify,
        }

    @builtins.property
    def event_action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.'''
        result = self._values.get("event_action")
        assert result is not None, "Required property 'event_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.'''
        result = self._values.get("notify")
        assert result is not None, "Required property 'notify' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40cd994d4f503501f9166fdc4bcc1c543827e49bec9b4c195dafeea91417cac0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="eventActionInput")
    def event_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventActionInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyInput")
    def notify_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "notifyInput"))

    @builtins.property
    @jsii.member(jsii_name="eventAction")
    def event_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventAction"))

    @event_action.setter
    def event_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__845d8484ccd896dd64949e78d4525ff669a58e794dcd9fe66f6228f1c3b0cfbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notify")
    def notify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "notify"))

    @notify.setter
    def notify(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b37e21d2f5cac7b7bea27f68984c370ae696f01e70185cb8821cbf03d892728d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notify", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1c1cadf3ac5790d94ff18861bb6d3acd27ee6623a4c0735953842b0f675d6e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction",
    jsii_struct_bases=[],
    name_mapping={"event_action": "eventAction", "notify": "notify"},
)
class CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction:
    def __init__(
        self,
        *,
        event_action: builtins.str,
        notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.
        :param notify: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72f53ca822b914868f1f1ade682bf4ab5d3db982780f80985c7c990a8e7ead67)
            check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
            check_type(argname="argument notify", value=notify, expected_type=type_hints["notify"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_action": event_action,
            "notify": notify,
        }

    @builtins.property
    def event_action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.'''
        result = self._values.get("event_action")
        assert result is not None, "Required property 'event_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.'''
        result = self._values.get("notify")
        assert result is not None, "Required property 'notify' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bdc32357163bb5dd400f1f24df05e501237cae861807e03381a2e3f38f30f2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="eventActionInput")
    def event_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventActionInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyInput")
    def notify_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "notifyInput"))

    @builtins.property
    @jsii.member(jsii_name="eventAction")
    def event_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventAction"))

    @event_action.setter
    def event_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__843431b66cdb41bbd96344822f740527555469e97afe671428aa432b2415113e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notify")
    def notify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "notify"))

    @notify.setter
    def notify(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2110da51e73200c534da27edc84d34bfcfdb65f8e11a1f3c01230f1bcf4fa14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notify", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381fe0979769aba2f2d166f864112d4488d5ba5b7c72c2637a862b9b000d7917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cead3c98a521f9065331febe28cd31294c33c99ecdaaf184bbedf031e00db999)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHighAction")
    def put_high_action(
        self,
        *,
        event_action: builtins.str,
        notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.
        :param notify: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction(
            event_action=event_action, notify=notify
        )

        return typing.cast(None, jsii.invoke(self, "putHighAction", [value]))

    @jsii.member(jsii_name="putLowAction")
    def put_low_action(
        self,
        *,
        event_action: builtins.str,
        notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.
        :param notify: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction(
            event_action=event_action, notify=notify
        )

        return typing.cast(None, jsii.invoke(self, "putLowAction", [value]))

    @jsii.member(jsii_name="putMediumAction")
    def put_medium_action(
        self,
        *,
        event_action: builtins.str,
        notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.
        :param notify: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction(
            event_action=event_action, notify=notify
        )

        return typing.cast(None, jsii.invoke(self, "putMediumAction", [value]))

    @jsii.member(jsii_name="resetHighAction")
    def reset_high_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHighAction", []))

    @jsii.member(jsii_name="resetLowAction")
    def reset_low_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLowAction", []))

    @jsii.member(jsii_name="resetMediumAction")
    def reset_medium_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMediumAction", []))

    @builtins.property
    @jsii.member(jsii_name="highAction")
    def high_action(
        self,
    ) -> CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighActionOutputReference:
        return typing.cast(CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighActionOutputReference, jsii.get(self, "highAction"))

    @builtins.property
    @jsii.member(jsii_name="lowAction")
    def low_action(
        self,
    ) -> CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowActionOutputReference:
        return typing.cast(CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowActionOutputReference, jsii.get(self, "lowAction"))

    @builtins.property
    @jsii.member(jsii_name="mediumAction")
    def medium_action(
        self,
    ) -> CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumActionOutputReference:
        return typing.cast(CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumActionOutputReference, jsii.get(self, "mediumAction"))

    @builtins.property
    @jsii.member(jsii_name="highActionInput")
    def high_action_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction], jsii.get(self, "highActionInput"))

    @builtins.property
    @jsii.member(jsii_name="lowActionInput")
    def low_action_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction], jsii.get(self, "lowActionInput"))

    @builtins.property
    @jsii.member(jsii_name="mediumActionInput")
    def medium_action_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction], jsii.get(self, "mediumActionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b33a6361e8cd9c19ee42e0e50648ab343428b04ae21714b8a311470e645192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "source_arn": "sourceArn",
        "block_email": "blockEmail",
        "from_": "from",
        "mfa_email": "mfaEmail",
        "no_action_email": "noActionEmail",
        "reply_to": "replyTo",
    },
)
class CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration:
    def __init__(
        self,
        *,
        source_arn: builtins.str,
        block_email: typing.Optional[typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail", typing.Dict[builtins.str, typing.Any]]] = None,
        from_: typing.Optional[builtins.str] = None,
        mfa_email: typing.Optional[typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail", typing.Dict[builtins.str, typing.Any]]] = None,
        no_action_email: typing.Optional[typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail", typing.Dict[builtins.str, typing.Any]]] = None,
        reply_to: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#source_arn CognitoRiskConfiguration#source_arn}.
        :param block_email: block_email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#block_email CognitoRiskConfiguration#block_email}
        :param from_: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#from CognitoRiskConfiguration#from}.
        :param mfa_email: mfa_email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#mfa_email CognitoRiskConfiguration#mfa_email}
        :param no_action_email: no_action_email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#no_action_email CognitoRiskConfiguration#no_action_email}
        :param reply_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#reply_to CognitoRiskConfiguration#reply_to}.
        '''
        if isinstance(block_email, dict):
            block_email = CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail(**block_email)
        if isinstance(mfa_email, dict):
            mfa_email = CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail(**mfa_email)
        if isinstance(no_action_email, dict):
            no_action_email = CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail(**no_action_email)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd425bfe3a42f5e22aad397f250cb842e888b159f5fd4dd5b88873c05475f77)
            check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
            check_type(argname="argument block_email", value=block_email, expected_type=type_hints["block_email"])
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument mfa_email", value=mfa_email, expected_type=type_hints["mfa_email"])
            check_type(argname="argument no_action_email", value=no_action_email, expected_type=type_hints["no_action_email"])
            check_type(argname="argument reply_to", value=reply_to, expected_type=type_hints["reply_to"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_arn": source_arn,
        }
        if block_email is not None:
            self._values["block_email"] = block_email
        if from_ is not None:
            self._values["from_"] = from_
        if mfa_email is not None:
            self._values["mfa_email"] = mfa_email
        if no_action_email is not None:
            self._values["no_action_email"] = no_action_email
        if reply_to is not None:
            self._values["reply_to"] = reply_to

    @builtins.property
    def source_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#source_arn CognitoRiskConfiguration#source_arn}.'''
        result = self._values.get("source_arn")
        assert result is not None, "Required property 'source_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def block_email(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail"]:
        '''block_email block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#block_email CognitoRiskConfiguration#block_email}
        '''
        result = self._values.get("block_email")
        return typing.cast(typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail"], result)

    @builtins.property
    def from_(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#from CognitoRiskConfiguration#from}.'''
        result = self._values.get("from_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mfa_email(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail"]:
        '''mfa_email block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#mfa_email CognitoRiskConfiguration#mfa_email}
        '''
        result = self._values.get("mfa_email")
        return typing.cast(typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail"], result)

    @builtins.property
    def no_action_email(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail"]:
        '''no_action_email block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#no_action_email CognitoRiskConfiguration#no_action_email}
        '''
        result = self._values.get("no_action_email")
        return typing.cast(typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail"], result)

    @builtins.property
    def reply_to(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#reply_to CognitoRiskConfiguration#reply_to}.'''
        result = self._values.get("reply_to")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail",
    jsii_struct_bases=[],
    name_mapping={
        "html_body": "htmlBody",
        "subject": "subject",
        "text_body": "textBody",
    },
)
class CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail:
    def __init__(
        self,
        *,
        html_body: builtins.str,
        subject: builtins.str,
        text_body: builtins.str,
    ) -> None:
        '''
        :param html_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.
        :param subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.
        :param text_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c258d70c2016eb73d284c0e1b85dd84ee314fb28d2825e768fa8fc44b97bb283)
            check_type(argname="argument html_body", value=html_body, expected_type=type_hints["html_body"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument text_body", value=text_body, expected_type=type_hints["text_body"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "html_body": html_body,
            "subject": subject,
            "text_body": text_body,
        }

    @builtins.property
    def html_body(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.'''
        result = self._values.get("html_body")
        assert result is not None, "Required property 'html_body' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.'''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def text_body(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.'''
        result = self._values.get("text_body")
        assert result is not None, "Required property 'text_body' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3f31a5b94a3f0a39c710a0aba0050f2d177c106c6047c03a6759307f8b00fe5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="htmlBodyInput")
    def html_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "htmlBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="textBodyInput")
    def text_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="htmlBody")
    def html_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "htmlBody"))

    @html_body.setter
    def html_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68a363d31ab5dbd01f693478db2f6b7b55d5573d4f377f07f23431ddf2538593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "htmlBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @subject.setter
    def subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63ebc2584af449da7ef36b320e52eca70873672597015ee8880bcd207af8170a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="textBody")
    def text_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "textBody"))

    @text_body.setter
    def text_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b3a65c1e48fa68f59a09b4bf1375dc8494cdf2bacc06137b2578fbee356c41e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "textBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d00548e66055e83745e673c40e4797d7348cd1ece9511b518c8c9502a1410f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail",
    jsii_struct_bases=[],
    name_mapping={
        "html_body": "htmlBody",
        "subject": "subject",
        "text_body": "textBody",
    },
)
class CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail:
    def __init__(
        self,
        *,
        html_body: builtins.str,
        subject: builtins.str,
        text_body: builtins.str,
    ) -> None:
        '''
        :param html_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.
        :param subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.
        :param text_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56658e61bacc6135d5731085b88856093a1a5cbcaa6826a9191b7b1619ae9e43)
            check_type(argname="argument html_body", value=html_body, expected_type=type_hints["html_body"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument text_body", value=text_body, expected_type=type_hints["text_body"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "html_body": html_body,
            "subject": subject,
            "text_body": text_body,
        }

    @builtins.property
    def html_body(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.'''
        result = self._values.get("html_body")
        assert result is not None, "Required property 'html_body' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.'''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def text_body(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.'''
        result = self._values.get("text_body")
        assert result is not None, "Required property 'text_body' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__910352b1cb0a6355809c8a86987f4bded5c205a564cb05505d55ebe494a10575)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="htmlBodyInput")
    def html_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "htmlBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="textBodyInput")
    def text_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="htmlBody")
    def html_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "htmlBody"))

    @html_body.setter
    def html_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d7ca936e90990ab3a5130f6a1300a114f428f70e6351f09d3ecaaed4d066cef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "htmlBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @subject.setter
    def subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fb20e836b8aa231fe34915b9a6e6c0743e4ec11c0e8f492632693381cf951f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="textBody")
    def text_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "textBody"))

    @text_body.setter
    def text_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d7605ba11242a116a8f334911ec2d7abce063888a232d7ac666ada47606d87f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "textBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f49a40ccd70da78890db9740afe76c73cc57fce43d2bb1e331b26b2a808161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail",
    jsii_struct_bases=[],
    name_mapping={
        "html_body": "htmlBody",
        "subject": "subject",
        "text_body": "textBody",
    },
)
class CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail:
    def __init__(
        self,
        *,
        html_body: builtins.str,
        subject: builtins.str,
        text_body: builtins.str,
    ) -> None:
        '''
        :param html_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.
        :param subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.
        :param text_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f5413fa4bf4157612bed4eb26667d6d42093fffef80a03d834d9c4b5c19c03d)
            check_type(argname="argument html_body", value=html_body, expected_type=type_hints["html_body"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument text_body", value=text_body, expected_type=type_hints["text_body"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "html_body": html_body,
            "subject": subject,
            "text_body": text_body,
        }

    @builtins.property
    def html_body(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.'''
        result = self._values.get("html_body")
        assert result is not None, "Required property 'html_body' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.'''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def text_body(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.'''
        result = self._values.get("text_body")
        assert result is not None, "Required property 'text_body' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5775d6f2f23acf0e30b14046a452c0a87f7bd2fc28cc36c73f32bc8e7ee56aa0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="htmlBodyInput")
    def html_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "htmlBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="textBodyInput")
    def text_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="htmlBody")
    def html_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "htmlBody"))

    @html_body.setter
    def html_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e8746e4b40953201efcd826c42b89639dc4f60144bcf89738749db3077ec679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "htmlBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @subject.setter
    def subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668091476da642997a2377a7f31f805f76a6af6154118b223f912fdf0cc1966f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="textBody")
    def text_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "textBody"))

    @text_body.setter
    def text_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c47bacfc54d9e456fe3c097a6a2395ec87314c9acb6d81ba446573482a55996)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "textBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d405ebbdd704ab160a46625b467bd16cb7461666c278990432530127147bae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24a22374e6787f00e616a38163552857ea6a1cda1e190e25dfb5cbf8d392dc77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBlockEmail")
    def put_block_email(
        self,
        *,
        html_body: builtins.str,
        subject: builtins.str,
        text_body: builtins.str,
    ) -> None:
        '''
        :param html_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.
        :param subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.
        :param text_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail(
            html_body=html_body, subject=subject, text_body=text_body
        )

        return typing.cast(None, jsii.invoke(self, "putBlockEmail", [value]))

    @jsii.member(jsii_name="putMfaEmail")
    def put_mfa_email(
        self,
        *,
        html_body: builtins.str,
        subject: builtins.str,
        text_body: builtins.str,
    ) -> None:
        '''
        :param html_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.
        :param subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.
        :param text_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail(
            html_body=html_body, subject=subject, text_body=text_body
        )

        return typing.cast(None, jsii.invoke(self, "putMfaEmail", [value]))

    @jsii.member(jsii_name="putNoActionEmail")
    def put_no_action_email(
        self,
        *,
        html_body: builtins.str,
        subject: builtins.str,
        text_body: builtins.str,
    ) -> None:
        '''
        :param html_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.
        :param subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.
        :param text_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail(
            html_body=html_body, subject=subject, text_body=text_body
        )

        return typing.cast(None, jsii.invoke(self, "putNoActionEmail", [value]))

    @jsii.member(jsii_name="resetBlockEmail")
    def reset_block_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockEmail", []))

    @jsii.member(jsii_name="resetFrom")
    def reset_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrom", []))

    @jsii.member(jsii_name="resetMfaEmail")
    def reset_mfa_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMfaEmail", []))

    @jsii.member(jsii_name="resetNoActionEmail")
    def reset_no_action_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoActionEmail", []))

    @jsii.member(jsii_name="resetReplyTo")
    def reset_reply_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplyTo", []))

    @builtins.property
    @jsii.member(jsii_name="blockEmail")
    def block_email(
        self,
    ) -> CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmailOutputReference:
        return typing.cast(CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmailOutputReference, jsii.get(self, "blockEmail"))

    @builtins.property
    @jsii.member(jsii_name="mfaEmail")
    def mfa_email(
        self,
    ) -> CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmailOutputReference:
        return typing.cast(CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmailOutputReference, jsii.get(self, "mfaEmail"))

    @builtins.property
    @jsii.member(jsii_name="noActionEmail")
    def no_action_email(
        self,
    ) -> CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmailOutputReference:
        return typing.cast(CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmailOutputReference, jsii.get(self, "noActionEmail"))

    @builtins.property
    @jsii.member(jsii_name="blockEmailInput")
    def block_email_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail], jsii.get(self, "blockEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="fromInput")
    def from_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fromInput"))

    @builtins.property
    @jsii.member(jsii_name="mfaEmailInput")
    def mfa_email_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail], jsii.get(self, "mfaEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="noActionEmailInput")
    def no_action_email_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail], jsii.get(self, "noActionEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="replyToInput")
    def reply_to_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replyToInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceArnInput")
    def source_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="from")
    def from_(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "from"))

    @from_.setter
    def from_(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05adc26c389f4b797399a368940f62ee1359031e7812bd123769b7efd1048765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "from", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replyTo")
    def reply_to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replyTo"))

    @reply_to.setter
    def reply_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afefcb374fd9a14027b3a1ee991d8c7fd7bd37fc46308716b1cf836dcc5e5ba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replyTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceArn")
    def source_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceArn"))

    @source_arn.setter
    def source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560e5a61324494cc1b2c7a8e70aa5b239a64d2568c1f53b7bfff4e57e843002f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df21387368b326f7b13853a378a2498066038b961666eb4086b3038005c71394)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7f2866030b93f0e7ecf5721b4786f980a0b98023aec972ce3c442e1f9c01c4c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        *,
        high_action: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction, typing.Dict[builtins.str, typing.Any]]] = None,
        low_action: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction, typing.Dict[builtins.str, typing.Any]]] = None,
        medium_action: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param high_action: high_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#high_action CognitoRiskConfiguration#high_action}
        :param low_action: low_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#low_action CognitoRiskConfiguration#low_action}
        :param medium_action: medium_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#medium_action CognitoRiskConfiguration#medium_action}
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions(
            high_action=high_action, low_action=low_action, medium_action=medium_action
        )

        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putNotifyConfiguration")
    def put_notify_configuration(
        self,
        *,
        source_arn: builtins.str,
        block_email: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail, typing.Dict[builtins.str, typing.Any]]] = None,
        from_: typing.Optional[builtins.str] = None,
        mfa_email: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail, typing.Dict[builtins.str, typing.Any]]] = None,
        no_action_email: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail, typing.Dict[builtins.str, typing.Any]]] = None,
        reply_to: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#source_arn CognitoRiskConfiguration#source_arn}.
        :param block_email: block_email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#block_email CognitoRiskConfiguration#block_email}
        :param from_: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#from CognitoRiskConfiguration#from}.
        :param mfa_email: mfa_email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#mfa_email CognitoRiskConfiguration#mfa_email}
        :param no_action_email: no_action_email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#no_action_email CognitoRiskConfiguration#no_action_email}
        :param reply_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#reply_to CognitoRiskConfiguration#reply_to}.
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration(
            source_arn=source_arn,
            block_email=block_email,
            from_=from_,
            mfa_email=mfa_email,
            no_action_email=no_action_email,
            reply_to=reply_to,
        )

        return typing.cast(None, jsii.invoke(self, "putNotifyConfiguration", [value]))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(
        self,
    ) -> CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsOutputReference:
        return typing.cast(CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsOutputReference, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="notifyConfiguration")
    def notify_configuration(
        self,
    ) -> CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationOutputReference:
        return typing.cast(CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationOutputReference, jsii.get(self, "notifyConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyConfigurationInput")
    def notify_configuration_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration], jsii.get(self, "notifyConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfiguration]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3369d16651fb04acf1f03d6b79f627e822bb4af2c5eb8b018bbd535909efc3d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions", "event_filter": "eventFilter"},
)
class CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration:
    def __init__(
        self,
        *,
        actions: typing.Union["CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions", typing.Dict[builtins.str, typing.Any]],
        event_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#actions CognitoRiskConfiguration#actions}
        :param event_filter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#event_filter CognitoRiskConfiguration#event_filter}.
        '''
        if isinstance(actions, dict):
            actions = CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions(**actions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd081efb8e17aa557e5061533b26fd057cb084f3c14475915899cc8db025f1f9)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument event_filter", value=event_filter, expected_type=type_hints["event_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
        }
        if event_filter is not None:
            self._values["event_filter"] = event_filter

    @builtins.property
    def actions(
        self,
    ) -> "CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions":
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#actions CognitoRiskConfiguration#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast("CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions", result)

    @builtins.property
    def event_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#event_filter CognitoRiskConfiguration#event_filter}.'''
        result = self._values.get("event_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions",
    jsii_struct_bases=[],
    name_mapping={"event_action": "eventAction"},
)
class CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions:
    def __init__(self, *, event_action: builtins.str) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19e77f654fb2822acf19c27decf53f9095fee2080f746743ba2063f0a3e390c4)
            check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_action": event_action,
        }

    @builtins.property
    def event_action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.'''
        result = self._values.get("event_action")
        assert result is not None, "Required property 'event_action' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__551a1fc713394013c5249acabfc27855bd286b606817bda78be5f62f1aac61ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="eventActionInput")
    def event_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventActionInput"))

    @builtins.property
    @jsii.member(jsii_name="eventAction")
    def event_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventAction"))

    @event_action.setter
    def event_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52aee80a9391f2ec9327f0e29f7db792fe25dda25f56a8d86626d7bdc3f75b65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6931ed61c0b45eefeb6cdf9223c39359d0cef098031f84a1f0311c30bf592c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f66dc9af53729e740de095761645f7f4013c146c5295309c073fcedc33410d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActions")
    def put_actions(self, *, event_action: builtins.str) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.
        '''
        value = CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions(
            event_action=event_action
        )

        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="resetEventFilter")
    def reset_event_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventFilter", []))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(
        self,
    ) -> CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActionsOutputReference:
        return typing.cast(CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActionsOutputReference, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="eventFilterInput")
    def event_filter_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "eventFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="eventFilter")
    def event_filter(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "eventFilter"))

    @event_filter.setter
    def event_filter(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc9c74678d97df8eb7fbb878f00114e2a2aa505aaec422c2c862d5e1c6cb600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ec25e45dc44de1d7922abcebb1c084d516878cf174f4b5cf333d48b16ac770f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "user_pool_id": "userPoolId",
        "account_takeover_risk_configuration": "accountTakeoverRiskConfiguration",
        "client_id": "clientId",
        "compromised_credentials_risk_configuration": "compromisedCredentialsRiskConfiguration",
        "id": "id",
        "risk_exception_configuration": "riskExceptionConfiguration",
    },
)
class CognitoRiskConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        user_pool_id: builtins.str,
        account_takeover_risk_configuration: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        client_id: typing.Optional[builtins.str] = None,
        compromised_credentials_risk_configuration: typing.Optional[typing.Union[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        risk_exception_configuration: typing.Optional[typing.Union["CognitoRiskConfigurationRiskExceptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param user_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#user_pool_id CognitoRiskConfiguration#user_pool_id}.
        :param account_takeover_risk_configuration: account_takeover_risk_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#account_takeover_risk_configuration CognitoRiskConfiguration#account_takeover_risk_configuration}
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#client_id CognitoRiskConfiguration#client_id}.
        :param compromised_credentials_risk_configuration: compromised_credentials_risk_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#compromised_credentials_risk_configuration CognitoRiskConfiguration#compromised_credentials_risk_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#id CognitoRiskConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param risk_exception_configuration: risk_exception_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#risk_exception_configuration CognitoRiskConfiguration#risk_exception_configuration}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(account_takeover_risk_configuration, dict):
            account_takeover_risk_configuration = CognitoRiskConfigurationAccountTakeoverRiskConfiguration(**account_takeover_risk_configuration)
        if isinstance(compromised_credentials_risk_configuration, dict):
            compromised_credentials_risk_configuration = CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration(**compromised_credentials_risk_configuration)
        if isinstance(risk_exception_configuration, dict):
            risk_exception_configuration = CognitoRiskConfigurationRiskExceptionConfiguration(**risk_exception_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b175e8b1fc2cf6c5c38c59d3f274d7546507374c351da80fb46d0d99607d70b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
            check_type(argname="argument account_takeover_risk_configuration", value=account_takeover_risk_configuration, expected_type=type_hints["account_takeover_risk_configuration"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument compromised_credentials_risk_configuration", value=compromised_credentials_risk_configuration, expected_type=type_hints["compromised_credentials_risk_configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument risk_exception_configuration", value=risk_exception_configuration, expected_type=type_hints["risk_exception_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_pool_id": user_pool_id,
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
        if account_takeover_risk_configuration is not None:
            self._values["account_takeover_risk_configuration"] = account_takeover_risk_configuration
        if client_id is not None:
            self._values["client_id"] = client_id
        if compromised_credentials_risk_configuration is not None:
            self._values["compromised_credentials_risk_configuration"] = compromised_credentials_risk_configuration
        if id is not None:
            self._values["id"] = id
        if risk_exception_configuration is not None:
            self._values["risk_exception_configuration"] = risk_exception_configuration

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
    def user_pool_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#user_pool_id CognitoRiskConfiguration#user_pool_id}.'''
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_takeover_risk_configuration(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfiguration]:
        '''account_takeover_risk_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#account_takeover_risk_configuration CognitoRiskConfiguration#account_takeover_risk_configuration}
        '''
        result = self._values.get("account_takeover_risk_configuration")
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfiguration], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#client_id CognitoRiskConfiguration#client_id}.'''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compromised_credentials_risk_configuration(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration]:
        '''compromised_credentials_risk_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#compromised_credentials_risk_configuration CognitoRiskConfiguration#compromised_credentials_risk_configuration}
        '''
        result = self._values.get("compromised_credentials_risk_configuration")
        return typing.cast(typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#id CognitoRiskConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def risk_exception_configuration(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationRiskExceptionConfiguration"]:
        '''risk_exception_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#risk_exception_configuration CognitoRiskConfiguration#risk_exception_configuration}
        '''
        result = self._values.get("risk_exception_configuration")
        return typing.cast(typing.Optional["CognitoRiskConfigurationRiskExceptionConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationRiskExceptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "blocked_ip_range_list": "blockedIpRangeList",
        "skipped_ip_range_list": "skippedIpRangeList",
    },
)
class CognitoRiskConfigurationRiskExceptionConfiguration:
    def __init__(
        self,
        *,
        blocked_ip_range_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        skipped_ip_range_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param blocked_ip_range_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#blocked_ip_range_list CognitoRiskConfiguration#blocked_ip_range_list}.
        :param skipped_ip_range_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#skipped_ip_range_list CognitoRiskConfiguration#skipped_ip_range_list}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8c11f66fabde722913d14844ab57c05188ea76d443715a197c70f9293fc57e8)
            check_type(argname="argument blocked_ip_range_list", value=blocked_ip_range_list, expected_type=type_hints["blocked_ip_range_list"])
            check_type(argname="argument skipped_ip_range_list", value=skipped_ip_range_list, expected_type=type_hints["skipped_ip_range_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if blocked_ip_range_list is not None:
            self._values["blocked_ip_range_list"] = blocked_ip_range_list
        if skipped_ip_range_list is not None:
            self._values["skipped_ip_range_list"] = skipped_ip_range_list

    @builtins.property
    def blocked_ip_range_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#blocked_ip_range_list CognitoRiskConfiguration#blocked_ip_range_list}.'''
        result = self._values.get("blocked_ip_range_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def skipped_ip_range_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cognito_risk_configuration#skipped_ip_range_list CognitoRiskConfiguration#skipped_ip_range_list}.'''
        result = self._values.get("skipped_ip_range_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationRiskExceptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoRiskConfigurationRiskExceptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationRiskExceptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4d6a756fdc89f665909ee2fbf24f2fd17a784cbade53001e61c8ca2a06d0a68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBlockedIpRangeList")
    def reset_blocked_ip_range_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockedIpRangeList", []))

    @jsii.member(jsii_name="resetSkippedIpRangeList")
    def reset_skipped_ip_range_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkippedIpRangeList", []))

    @builtins.property
    @jsii.member(jsii_name="blockedIpRangeListInput")
    def blocked_ip_range_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "blockedIpRangeListInput"))

    @builtins.property
    @jsii.member(jsii_name="skippedIpRangeListInput")
    def skipped_ip_range_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "skippedIpRangeListInput"))

    @builtins.property
    @jsii.member(jsii_name="blockedIpRangeList")
    def blocked_ip_range_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "blockedIpRangeList"))

    @blocked_ip_range_list.setter
    def blocked_ip_range_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f547cc63d8caec2858faaae4d8c9c75ed2911611b9d917eb9ad043b987e2eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockedIpRangeList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skippedIpRangeList")
    def skipped_ip_range_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "skippedIpRangeList"))

    @skipped_ip_range_list.setter
    def skipped_ip_range_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5694be02382bac314bef9fa3fc2a9bc436e95db44fc5de95e10635f6ba4dc73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skippedIpRangeList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationRiskExceptionConfiguration]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationRiskExceptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationRiskExceptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f1cd05e140e118587da8404f8274f2beee906edfba68f342fb6d0cddb2f979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CognitoRiskConfiguration",
    "CognitoRiskConfigurationAccountTakeoverRiskConfiguration",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighActionOutputReference",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowActionOutputReference",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumActionOutputReference",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsOutputReference",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmailOutputReference",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmailOutputReference",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmailOutputReference",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationOutputReference",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationOutputReference",
    "CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration",
    "CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions",
    "CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActionsOutputReference",
    "CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationOutputReference",
    "CognitoRiskConfigurationConfig",
    "CognitoRiskConfigurationRiskExceptionConfiguration",
    "CognitoRiskConfigurationRiskExceptionConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__ee5bd88f254a14a346bc366ba5e420a19bd04c9f76e02911ff52d9371013c256(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    user_pool_id: builtins.str,
    account_takeover_risk_configuration: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    client_id: typing.Optional[builtins.str] = None,
    compromised_credentials_risk_configuration: typing.Optional[typing.Union[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    risk_exception_configuration: typing.Optional[typing.Union[CognitoRiskConfigurationRiskExceptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7f1aa037e15e2a7e95575d2e8af3ae22995cc187ed239a699c37f9f2ca721a4f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afefc8dbc8d87b39c7578bf0dbf8ded92bad6a3e270164583bfe50e3796caf71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8edfcdfc624e7fece40b71bff9552296632679337afeebd790e11163175f2b51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3dea987d5ccffe22b903f662cbc1cc6bc9d308681e3b74fbc6a00b2284d57d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b936500b484783e7891ed8e6190e5e59924fe5b267a63960f1b4b2073ee3cf45(
    *,
    actions: typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions, typing.Dict[builtins.str, typing.Any]],
    notify_configuration: typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dfcb874bc66fbb3c7df2b3883a2699c36736596d92b2b73b7e2c702a7a444a6(
    *,
    high_action: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction, typing.Dict[builtins.str, typing.Any]]] = None,
    low_action: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction, typing.Dict[builtins.str, typing.Any]]] = None,
    medium_action: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b96249ffb69c4af97b84817009550b8d2a94f30fb30bef0a64d198fbff2635(
    *,
    event_action: builtins.str,
    notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf9f6101438aeb384b6741fe2e1fde66a53bbd5147a0d733ce58e4e8c5ad7d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fe5ec6320de050a142ffbd7201dce99f86237d8bfcdba422205fd4aa74270d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__548b5c1ba4215a43bc19778da679d7b82a15be390449d66646ae89aa9aad91f6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__147abb3c09a4693a271a6fbc0855f1f3cc2a5dc0cf9a667f28c3e8fd490ae34c(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3060780a98e92533bc35623f9e28da0c3311eb650637cefddc7c462a2641e26(
    *,
    event_action: builtins.str,
    notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40cd994d4f503501f9166fdc4bcc1c543827e49bec9b4c195dafeea91417cac0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__845d8484ccd896dd64949e78d4525ff669a58e794dcd9fe66f6228f1c3b0cfbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37e21d2f5cac7b7bea27f68984c370ae696f01e70185cb8821cbf03d892728d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1c1cadf3ac5790d94ff18861bb6d3acd27ee6623a4c0735953842b0f675d6e9(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f53ca822b914868f1f1ade682bf4ab5d3db982780f80985c7c990a8e7ead67(
    *,
    event_action: builtins.str,
    notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bdc32357163bb5dd400f1f24df05e501237cae861807e03381a2e3f38f30f2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__843431b66cdb41bbd96344822f740527555469e97afe671428aa432b2415113e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2110da51e73200c534da27edc84d34bfcfdb65f8e11a1f3c01230f1bcf4fa14(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381fe0979769aba2f2d166f864112d4488d5ba5b7c72c2637a862b9b000d7917(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cead3c98a521f9065331febe28cd31294c33c99ecdaaf184bbedf031e00db999(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b33a6361e8cd9c19ee42e0e50648ab343428b04ae21714b8a311470e645192(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd425bfe3a42f5e22aad397f250cb842e888b159f5fd4dd5b88873c05475f77(
    *,
    source_arn: builtins.str,
    block_email: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail, typing.Dict[builtins.str, typing.Any]]] = None,
    from_: typing.Optional[builtins.str] = None,
    mfa_email: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail, typing.Dict[builtins.str, typing.Any]]] = None,
    no_action_email: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail, typing.Dict[builtins.str, typing.Any]]] = None,
    reply_to: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c258d70c2016eb73d284c0e1b85dd84ee314fb28d2825e768fa8fc44b97bb283(
    *,
    html_body: builtins.str,
    subject: builtins.str,
    text_body: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f31a5b94a3f0a39c710a0aba0050f2d177c106c6047c03a6759307f8b00fe5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a363d31ab5dbd01f693478db2f6b7b55d5573d4f377f07f23431ddf2538593(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ebc2584af449da7ef36b320e52eca70873672597015ee8880bcd207af8170a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3a65c1e48fa68f59a09b4bf1375dc8494cdf2bacc06137b2578fbee356c41e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d00548e66055e83745e673c40e4797d7348cd1ece9511b518c8c9502a1410f4(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56658e61bacc6135d5731085b88856093a1a5cbcaa6826a9191b7b1619ae9e43(
    *,
    html_body: builtins.str,
    subject: builtins.str,
    text_body: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__910352b1cb0a6355809c8a86987f4bded5c205a564cb05505d55ebe494a10575(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d7ca936e90990ab3a5130f6a1300a114f428f70e6351f09d3ecaaed4d066cef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fb20e836b8aa231fe34915b9a6e6c0743e4ec11c0e8f492632693381cf951f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d7605ba11242a116a8f334911ec2d7abce063888a232d7ac666ada47606d87f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f49a40ccd70da78890db9740afe76c73cc57fce43d2bb1e331b26b2a808161(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f5413fa4bf4157612bed4eb26667d6d42093fffef80a03d834d9c4b5c19c03d(
    *,
    html_body: builtins.str,
    subject: builtins.str,
    text_body: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5775d6f2f23acf0e30b14046a452c0a87f7bd2fc28cc36c73f32bc8e7ee56aa0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8746e4b40953201efcd826c42b89639dc4f60144bcf89738749db3077ec679(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668091476da642997a2377a7f31f805f76a6af6154118b223f912fdf0cc1966f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c47bacfc54d9e456fe3c097a6a2395ec87314c9acb6d81ba446573482a55996(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d405ebbdd704ab160a46625b467bd16cb7461666c278990432530127147bae8(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a22374e6787f00e616a38163552857ea6a1cda1e190e25dfb5cbf8d392dc77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05adc26c389f4b797399a368940f62ee1359031e7812bd123769b7efd1048765(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afefcb374fd9a14027b3a1ee991d8c7fd7bd37fc46308716b1cf836dcc5e5ba8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560e5a61324494cc1b2c7a8e70aa5b239a64d2568c1f53b7bfff4e57e843002f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df21387368b326f7b13853a378a2498066038b961666eb4086b3038005c71394(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f2866030b93f0e7ecf5721b4786f980a0b98023aec972ce3c442e1f9c01c4c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3369d16651fb04acf1f03d6b79f627e822bb4af2c5eb8b018bbd535909efc3d9(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd081efb8e17aa557e5061533b26fd057cb084f3c14475915899cc8db025f1f9(
    *,
    actions: typing.Union[CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions, typing.Dict[builtins.str, typing.Any]],
    event_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e77f654fb2822acf19c27decf53f9095fee2080f746743ba2063f0a3e390c4(
    *,
    event_action: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551a1fc713394013c5249acabfc27855bd286b606817bda78be5f62f1aac61ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52aee80a9391f2ec9327f0e29f7db792fe25dda25f56a8d86626d7bdc3f75b65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6931ed61c0b45eefeb6cdf9223c39359d0cef098031f84a1f0311c30bf592c6(
    value: typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f66dc9af53729e740de095761645f7f4013c146c5295309c073fcedc33410d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc9c74678d97df8eb7fbb878f00114e2a2aa505aaec422c2c862d5e1c6cb600(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ec25e45dc44de1d7922abcebb1c084d516878cf174f4b5cf333d48b16ac770f(
    value: typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b175e8b1fc2cf6c5c38c59d3f274d7546507374c351da80fb46d0d99607d70b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    user_pool_id: builtins.str,
    account_takeover_risk_configuration: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    client_id: typing.Optional[builtins.str] = None,
    compromised_credentials_risk_configuration: typing.Optional[typing.Union[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    risk_exception_configuration: typing.Optional[typing.Union[CognitoRiskConfigurationRiskExceptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8c11f66fabde722913d14844ab57c05188ea76d443715a197c70f9293fc57e8(
    *,
    blocked_ip_range_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    skipped_ip_range_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4d6a756fdc89f665909ee2fbf24f2fd17a784cbade53001e61c8ca2a06d0a68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f547cc63d8caec2858faaae4d8c9c75ed2911611b9d917eb9ad043b987e2eb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5694be02382bac314bef9fa3fc2a9bc436e95db44fc5de95e10635f6ba4dc73(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f1cd05e140e118587da8404f8274f2beee906edfba68f342fb6d0cddb2f979(
    value: typing.Optional[CognitoRiskConfigurationRiskExceptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

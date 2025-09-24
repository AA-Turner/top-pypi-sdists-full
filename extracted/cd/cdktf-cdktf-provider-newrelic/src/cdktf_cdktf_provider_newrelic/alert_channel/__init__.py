r'''
# `newrelic_alert_channel`

Refer to the Terraform Registry for docs: [`newrelic_alert_channel`](https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel).
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


class AlertChannel(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.alertChannel.AlertChannel",
):
    '''Represents a {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel newrelic_alert_channel}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        type: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
        config: typing.Optional[typing.Union["AlertChannelConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel newrelic_alert_channel} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: (Required) The name of the channel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#name AlertChannel#name}
        :param type: (Required) The type of channel. One of: (slack, user, victorops, webhook, email, opsgenie, pagerduty). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#type AlertChannel#type}
        :param account_id: The New Relic account ID where you want to create alert channels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#account_id AlertChannel#account_id}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#config AlertChannel#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#id AlertChannel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3b5e862284375f0c9eeda12c697cfa2d0486129cf845d45fc465978d8999796)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = AlertChannelConfig(
            name=name,
            type=type,
            account_id=account_id,
            config=config,
            id=id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config_])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a AlertChannel resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AlertChannel to import.
        :param import_from_id: The id of the existing AlertChannel that should be imported. Refer to the {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AlertChannel to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc6d91d206bcd102f9b61178ed587b26ec7d61d95ba6ac505dc4946f9e384e9e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        api_key: typing.Optional[builtins.str] = None,
        auth_password: typing.Optional[builtins.str] = None,
        auth_type: typing.Optional[builtins.str] = None,
        auth_username: typing.Optional[builtins.str] = None,
        base_url: typing.Optional[builtins.str] = None,
        channel: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        headers_string: typing.Optional[builtins.str] = None,
        include_json_attachment: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        payload: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        payload_string: typing.Optional[builtins.str] = None,
        payload_type: typing.Optional[builtins.str] = None,
        recipients: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        route_key: typing.Optional[builtins.str] = None,
        service_key: typing.Optional[builtins.str] = None,
        tags: typing.Optional[builtins.str] = None,
        teams: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
        user_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_key: The API key for integrating with OpsGenie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#api_key AlertChannel#api_key}
        :param auth_password: Specifies an authentication password for use with a channel. Supported by the webhook channel type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#auth_password AlertChannel#auth_password}
        :param auth_type: Specifies an authentication method for use with a channel. Supported by the webhook channel type. Only HTTP basic authentication is currently supported via the value BASIC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#auth_type AlertChannel#auth_type}
        :param auth_username: Specifies an authentication username for use with a channel. Supported by the webhook channel type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#auth_username AlertChannel#auth_username}
        :param base_url: The base URL of the webhook destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#base_url AlertChannel#base_url}
        :param channel: The Slack channel to send notifications to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#channel AlertChannel#channel}
        :param headers: A map of key/value pairs that represents extra HTTP headers to be sent along with the webhook payload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#headers AlertChannel#headers}
        :param headers_string: Use instead of headers if the desired payload is more complex than a list of key/value pairs (e.g. a set of headers that makes use of nested objects). The value provided should be a valid JSON string with escaped double quotes. Conflicts with headers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#headers_string AlertChannel#headers_string}
        :param include_json_attachment: true or false. Flag for whether or not to attach a JSON document containing information about the associated alert to the email that is sent to recipients. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#include_json_attachment AlertChannel#include_json_attachment}
        :param key: The key for integrating with VictorOps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#key AlertChannel#key}
        :param payload: A map of key/value pairs that represents the webhook payload. Must provide payload_type if setting this argument. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#payload AlertChannel#payload}
        :param payload_string: Use instead of payload if the desired payload is more complex than a list of key/value pairs (e.g. a payload that makes use of nested objects). The value provided should be a valid JSON string with escaped double quotes. Conflicts with payload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#payload_string AlertChannel#payload_string}
        :param payload_type: Can either be application/json or application/x-www-form-urlencoded. The payload_type argument is required if payload is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#payload_type AlertChannel#payload_type}
        :param recipients: A set of recipients for targeting notifications. Multiple values are comma separated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#recipients AlertChannel#recipients}
        :param region: The data center region to store your data. Valid values are US and EU. Default is US. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#region AlertChannel#region}
        :param route_key: The route key for integrating with VictorOps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#route_key AlertChannel#route_key}
        :param service_key: Specifies the service key for integrating with Pagerduty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#service_key AlertChannel#service_key}
        :param tags: A set of tags for targeting notifications. Multiple values are comma separated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#tags AlertChannel#tags}
        :param teams: A set of teams for targeting notifications. Multiple values are comma separated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#teams AlertChannel#teams}
        :param url: Your organization's Slack URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#url AlertChannel#url}
        :param user_id: The user ID for use with the user channel type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#user_id AlertChannel#user_id}
        '''
        value = AlertChannelConfigA(
            api_key=api_key,
            auth_password=auth_password,
            auth_type=auth_type,
            auth_username=auth_username,
            base_url=base_url,
            channel=channel,
            headers=headers,
            headers_string=headers_string,
            include_json_attachment=include_json_attachment,
            key=key,
            payload=payload,
            payload_string=payload_string,
            payload_type=payload_type,
            recipients=recipients,
            region=region,
            route_key=route_key,
            service_key=service_key,
            tags=tags,
            teams=teams,
            url=url,
            user_id=user_id,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="config")
    def config(self) -> "AlertChannelConfigAOutputReference":
        return typing.cast("AlertChannelConfigAOutputReference", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["AlertChannelConfigA"]:
        return typing.cast(typing.Optional["AlertChannelConfigA"], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2602e1a557b92db237ff56526a2074a4d08c4c52e1ec16d8991f6b396aef44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec32047e15d776161464c7ed35f041eb0ef78bb4e3ec19cba47763fa8fef872e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc768690c0ba5ada78e2d647a4b0fe30720ce6c7c972c945049bc78e6c28eaf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5059f889661ed85ad809dff3447a9ca120537cb8cb78b7f01b8895147c4b3bea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.alertChannel.AlertChannelConfig",
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
        "type": "type",
        "account_id": "accountId",
        "config": "config",
        "id": "id",
    },
)
class AlertChannelConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        type: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
        config: typing.Optional[typing.Union["AlertChannelConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: (Required) The name of the channel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#name AlertChannel#name}
        :param type: (Required) The type of channel. One of: (slack, user, victorops, webhook, email, opsgenie, pagerduty). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#type AlertChannel#type}
        :param account_id: The New Relic account ID where you want to create alert channels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#account_id AlertChannel#account_id}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#config AlertChannel#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#id AlertChannel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config, dict):
            config = AlertChannelConfigA(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6cce12699578e3926be59f1dd9391597286d8af92e8e3e0ffd74d2b6cbe6b36)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if config is not None:
            self._values["config"] = config
        if id is not None:
            self._values["id"] = id

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
        '''(Required) The name of the channel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#name AlertChannel#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''(Required) The type of channel. One of: (slack, user, victorops, webhook, email, opsgenie, pagerduty).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#type AlertChannel#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The New Relic account ID where you want to create alert channels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#account_id AlertChannel#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def config(self) -> typing.Optional["AlertChannelConfigA"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#config AlertChannel#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["AlertChannelConfigA"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#id AlertChannel#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlertChannelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.alertChannel.AlertChannelConfigA",
    jsii_struct_bases=[],
    name_mapping={
        "api_key": "apiKey",
        "auth_password": "authPassword",
        "auth_type": "authType",
        "auth_username": "authUsername",
        "base_url": "baseUrl",
        "channel": "channel",
        "headers": "headers",
        "headers_string": "headersString",
        "include_json_attachment": "includeJsonAttachment",
        "key": "key",
        "payload": "payload",
        "payload_string": "payloadString",
        "payload_type": "payloadType",
        "recipients": "recipients",
        "region": "region",
        "route_key": "routeKey",
        "service_key": "serviceKey",
        "tags": "tags",
        "teams": "teams",
        "url": "url",
        "user_id": "userId",
    },
)
class AlertChannelConfigA:
    def __init__(
        self,
        *,
        api_key: typing.Optional[builtins.str] = None,
        auth_password: typing.Optional[builtins.str] = None,
        auth_type: typing.Optional[builtins.str] = None,
        auth_username: typing.Optional[builtins.str] = None,
        base_url: typing.Optional[builtins.str] = None,
        channel: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        headers_string: typing.Optional[builtins.str] = None,
        include_json_attachment: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        payload: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        payload_string: typing.Optional[builtins.str] = None,
        payload_type: typing.Optional[builtins.str] = None,
        recipients: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        route_key: typing.Optional[builtins.str] = None,
        service_key: typing.Optional[builtins.str] = None,
        tags: typing.Optional[builtins.str] = None,
        teams: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
        user_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_key: The API key for integrating with OpsGenie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#api_key AlertChannel#api_key}
        :param auth_password: Specifies an authentication password for use with a channel. Supported by the webhook channel type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#auth_password AlertChannel#auth_password}
        :param auth_type: Specifies an authentication method for use with a channel. Supported by the webhook channel type. Only HTTP basic authentication is currently supported via the value BASIC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#auth_type AlertChannel#auth_type}
        :param auth_username: Specifies an authentication username for use with a channel. Supported by the webhook channel type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#auth_username AlertChannel#auth_username}
        :param base_url: The base URL of the webhook destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#base_url AlertChannel#base_url}
        :param channel: The Slack channel to send notifications to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#channel AlertChannel#channel}
        :param headers: A map of key/value pairs that represents extra HTTP headers to be sent along with the webhook payload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#headers AlertChannel#headers}
        :param headers_string: Use instead of headers if the desired payload is more complex than a list of key/value pairs (e.g. a set of headers that makes use of nested objects). The value provided should be a valid JSON string with escaped double quotes. Conflicts with headers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#headers_string AlertChannel#headers_string}
        :param include_json_attachment: true or false. Flag for whether or not to attach a JSON document containing information about the associated alert to the email that is sent to recipients. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#include_json_attachment AlertChannel#include_json_attachment}
        :param key: The key for integrating with VictorOps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#key AlertChannel#key}
        :param payload: A map of key/value pairs that represents the webhook payload. Must provide payload_type if setting this argument. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#payload AlertChannel#payload}
        :param payload_string: Use instead of payload if the desired payload is more complex than a list of key/value pairs (e.g. a payload that makes use of nested objects). The value provided should be a valid JSON string with escaped double quotes. Conflicts with payload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#payload_string AlertChannel#payload_string}
        :param payload_type: Can either be application/json or application/x-www-form-urlencoded. The payload_type argument is required if payload is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#payload_type AlertChannel#payload_type}
        :param recipients: A set of recipients for targeting notifications. Multiple values are comma separated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#recipients AlertChannel#recipients}
        :param region: The data center region to store your data. Valid values are US and EU. Default is US. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#region AlertChannel#region}
        :param route_key: The route key for integrating with VictorOps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#route_key AlertChannel#route_key}
        :param service_key: Specifies the service key for integrating with Pagerduty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#service_key AlertChannel#service_key}
        :param tags: A set of tags for targeting notifications. Multiple values are comma separated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#tags AlertChannel#tags}
        :param teams: A set of teams for targeting notifications. Multiple values are comma separated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#teams AlertChannel#teams}
        :param url: Your organization's Slack URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#url AlertChannel#url}
        :param user_id: The user ID for use with the user channel type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#user_id AlertChannel#user_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a5746c2e9e52df5745afb5ecc8360d8898afc597685bae990ef615f1dc9e0a)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument auth_password", value=auth_password, expected_type=type_hints["auth_password"])
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument auth_username", value=auth_username, expected_type=type_hints["auth_username"])
            check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument headers_string", value=headers_string, expected_type=type_hints["headers_string"])
            check_type(argname="argument include_json_attachment", value=include_json_attachment, expected_type=type_hints["include_json_attachment"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            check_type(argname="argument payload_string", value=payload_string, expected_type=type_hints["payload_string"])
            check_type(argname="argument payload_type", value=payload_type, expected_type=type_hints["payload_type"])
            check_type(argname="argument recipients", value=recipients, expected_type=type_hints["recipients"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument route_key", value=route_key, expected_type=type_hints["route_key"])
            check_type(argname="argument service_key", value=service_key, expected_type=type_hints["service_key"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument teams", value=teams, expected_type=type_hints["teams"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_key is not None:
            self._values["api_key"] = api_key
        if auth_password is not None:
            self._values["auth_password"] = auth_password
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if auth_username is not None:
            self._values["auth_username"] = auth_username
        if base_url is not None:
            self._values["base_url"] = base_url
        if channel is not None:
            self._values["channel"] = channel
        if headers is not None:
            self._values["headers"] = headers
        if headers_string is not None:
            self._values["headers_string"] = headers_string
        if include_json_attachment is not None:
            self._values["include_json_attachment"] = include_json_attachment
        if key is not None:
            self._values["key"] = key
        if payload is not None:
            self._values["payload"] = payload
        if payload_string is not None:
            self._values["payload_string"] = payload_string
        if payload_type is not None:
            self._values["payload_type"] = payload_type
        if recipients is not None:
            self._values["recipients"] = recipients
        if region is not None:
            self._values["region"] = region
        if route_key is not None:
            self._values["route_key"] = route_key
        if service_key is not None:
            self._values["service_key"] = service_key
        if tags is not None:
            self._values["tags"] = tags
        if teams is not None:
            self._values["teams"] = teams
        if url is not None:
            self._values["url"] = url
        if user_id is not None:
            self._values["user_id"] = user_id

    @builtins.property
    def api_key(self) -> typing.Optional[builtins.str]:
        '''The API key for integrating with OpsGenie.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#api_key AlertChannel#api_key}
        '''
        result = self._values.get("api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_password(self) -> typing.Optional[builtins.str]:
        '''Specifies an authentication password for use with a channel. Supported by the webhook channel type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#auth_password AlertChannel#auth_password}
        '''
        result = self._values.get("auth_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''Specifies an authentication method for use with a channel.

        Supported by the webhook channel type. Only HTTP basic authentication is currently supported via the value BASIC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#auth_type AlertChannel#auth_type}
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_username(self) -> typing.Optional[builtins.str]:
        '''Specifies an authentication username for use with a channel. Supported by the webhook channel type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#auth_username AlertChannel#auth_username}
        '''
        result = self._values.get("auth_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def base_url(self) -> typing.Optional[builtins.str]:
        '''The base URL of the webhook destination.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#base_url AlertChannel#base_url}
        '''
        result = self._values.get("base_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def channel(self) -> typing.Optional[builtins.str]:
        '''The Slack channel to send notifications to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#channel AlertChannel#channel}
        '''
        result = self._values.get("channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def headers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of key/value pairs that represents extra HTTP headers to be sent along with the webhook payload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#headers AlertChannel#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def headers_string(self) -> typing.Optional[builtins.str]:
        '''Use instead of headers if the desired payload is more complex than a list of key/value pairs (e.g. a set of headers that makes use of nested objects). The value provided should be a valid JSON string with escaped double quotes. Conflicts with headers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#headers_string AlertChannel#headers_string}
        '''
        result = self._values.get("headers_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_json_attachment(self) -> typing.Optional[builtins.str]:
        '''true or false.

        Flag for whether or not to attach a JSON document containing information about the associated alert to the email that is sent to recipients.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#include_json_attachment AlertChannel#include_json_attachment}
        '''
        result = self._values.get("include_json_attachment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''The key for integrating with VictorOps.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#key AlertChannel#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def payload(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of key/value pairs that represents the webhook payload. Must provide payload_type if setting this argument.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#payload AlertChannel#payload}
        '''
        result = self._values.get("payload")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def payload_string(self) -> typing.Optional[builtins.str]:
        '''Use instead of payload if the desired payload is more complex than a list of key/value pairs (e.g. a payload that makes use of nested objects). The value provided should be a valid JSON string with escaped double quotes. Conflicts with payload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#payload_string AlertChannel#payload_string}
        '''
        result = self._values.get("payload_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def payload_type(self) -> typing.Optional[builtins.str]:
        '''Can either be application/json or application/x-www-form-urlencoded. The payload_type argument is required if payload is set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#payload_type AlertChannel#payload_type}
        '''
        result = self._values.get("payload_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recipients(self) -> typing.Optional[builtins.str]:
        '''A set of recipients for targeting notifications. Multiple values are comma separated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#recipients AlertChannel#recipients}
        '''
        result = self._values.get("recipients")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The data center region to store your data. Valid values are US and EU. Default is US.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#region AlertChannel#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_key(self) -> typing.Optional[builtins.str]:
        '''The route key for integrating with VictorOps.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#route_key AlertChannel#route_key}
        '''
        result = self._values.get("route_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_key(self) -> typing.Optional[builtins.str]:
        '''Specifies the service key for integrating with Pagerduty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#service_key AlertChannel#service_key}
        '''
        result = self._values.get("service_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[builtins.str]:
        '''A set of tags for targeting notifications. Multiple values are comma separated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#tags AlertChannel#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def teams(self) -> typing.Optional[builtins.str]:
        '''A set of teams for targeting notifications. Multiple values are comma separated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#teams AlertChannel#teams}
        '''
        result = self._values.get("teams")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Your organization's Slack URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#url AlertChannel#url}
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_id(self) -> typing.Optional[builtins.str]:
        '''The user ID for use with the user channel type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_channel#user_id AlertChannel#user_id}
        '''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlertChannelConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlertChannelConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.alertChannel.AlertChannelConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9058079087f009af2e64d8a419d2afd13903e53e686000fa5e5a1eecf3dfa5ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetApiKey")
    def reset_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiKey", []))

    @jsii.member(jsii_name="resetAuthPassword")
    def reset_auth_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthPassword", []))

    @jsii.member(jsii_name="resetAuthType")
    def reset_auth_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthType", []))

    @jsii.member(jsii_name="resetAuthUsername")
    def reset_auth_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthUsername", []))

    @jsii.member(jsii_name="resetBaseUrl")
    def reset_base_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseUrl", []))

    @jsii.member(jsii_name="resetChannel")
    def reset_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChannel", []))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetHeadersString")
    def reset_headers_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeadersString", []))

    @jsii.member(jsii_name="resetIncludeJsonAttachment")
    def reset_include_json_attachment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeJsonAttachment", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetPayload")
    def reset_payload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPayload", []))

    @jsii.member(jsii_name="resetPayloadString")
    def reset_payload_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPayloadString", []))

    @jsii.member(jsii_name="resetPayloadType")
    def reset_payload_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPayloadType", []))

    @jsii.member(jsii_name="resetRecipients")
    def reset_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecipients", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRouteKey")
    def reset_route_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteKey", []))

    @jsii.member(jsii_name="resetServiceKey")
    def reset_service_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceKey", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTeams")
    def reset_teams(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeams", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @jsii.member(jsii_name="resetUserId")
    def reset_user_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserId", []))

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="authPasswordInput")
    def auth_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="authTypeInput")
    def auth_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="authUsernameInput")
    def auth_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="baseUrlInput")
    def base_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="channelInput")
    def channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelInput"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="headersStringInput")
    def headers_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headersStringInput"))

    @builtins.property
    @jsii.member(jsii_name="includeJsonAttachmentInput")
    def include_json_attachment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "includeJsonAttachmentInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadInput")
    def payload_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "payloadInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadStringInput")
    def payload_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadStringInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadTypeInput")
    def payload_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="recipientsInput")
    def recipients_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="routeKeyInput")
    def route_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceKeyInput")
    def service_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="teamsInput")
    def teams_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamsInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdInput")
    def user_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userIdInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f197ad04f11cf11107a4143746bddf9ba732c917f4f99059e6ef2714c863892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authPassword")
    def auth_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authPassword"))

    @auth_password.setter
    def auth_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81a020a6dcf312a7cfc359cc584a1d0ff88d1d4230fda7077b8abe9b2ba66ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b63a571f032fc792aaab47c106ea11693c77c652872c88ed6a318325c241463d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authUsername")
    def auth_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authUsername"))

    @auth_username.setter
    def auth_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e44e05dc893d787b1374baf9471c27bba1cf7787f8c3476b417a9b242640e67e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseUrl"))

    @base_url.setter
    def base_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ec76ba92b092dd4dfa0959bfcb859fcf5a34603b6b9b8f76c58e4cef2c8fa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="channel")
    def channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channel"))

    @channel.setter
    def channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__634d25aef3b6a04acf4330126b02a0276fb085b4e0066cabbefaa5a254561cf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "headers"))

    @headers.setter
    def headers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f8de627fc56cc5270d19871970a0f9c7b43cc18be32098dbc5e23e3bdc2ac06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headersString")
    def headers_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headersString"))

    @headers_string.setter
    def headers_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2dcda80437e8391fd60099caf17c722b98f33694c6145273968151d9c0524ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headersString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeJsonAttachment")
    def include_json_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "includeJsonAttachment"))

    @include_json_attachment.setter
    def include_json_attachment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3112b51d2163b389e47cd5afef5e9e6480489e8fbf50270dbc891195ada87dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeJsonAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a12dc68bd75ee06cc2169d2285bd082061ef0291ab19489ef358c0020ef233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payload")
    def payload(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "payload"))

    @payload.setter
    def payload(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a7c87b3ec47c531c58cdbd80f77e3f3a2149abe28eab341b2ceb3c9ed5a08f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payloadString")
    def payload_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payloadString"))

    @payload_string.setter
    def payload_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020e25b17087ce5084606fbc1170bbd7398b89f61d49a08629f3f0fbafe8aa12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payloadType")
    def payload_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payloadType"))

    @payload_type.setter
    def payload_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5204979af217aa94ad99eb487c15a2bf9c209b76c5805a5175d980b8d709ff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recipients")
    def recipients(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recipients"))

    @recipients.setter
    def recipients(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d080dc1b2ba704c117db222f57d78afac955b0d4a7e3124d509b722bf7a4b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9576be1617d0a9328085d18a5afda882394c8e7b98fbfe28bd1ce5df0516966d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeKey")
    def route_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeKey"))

    @route_key.setter
    def route_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__301e9746a24d17aadf928abdb4160dc3a145e94c535dd9be09b9facb3a92a633)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceKey")
    def service_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceKey"))

    @service_key.setter
    def service_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__824e0328ac2852d58b6cab74417d7a47ea849947e5c00573047d2060e7a9be67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f30bd5b486ab640effe6e121a177b32e3b4b193c5ad76865f1c19365a00e17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="teams")
    def teams(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "teams"))

    @teams.setter
    def teams(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a951e172c747f5676ddcf24e036b39dcdbe82345808f7390c271ca9a3558185d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8634f51912c98eff6b5c3585f589dbe9644817f3519a547325a5a6dd7008746b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @user_id.setter
    def user_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__478b9589f7f032c4988dc001507992dfc277cb42e9dc6eedbc52ec44c8262e58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlertChannelConfigA]:
        return typing.cast(typing.Optional[AlertChannelConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AlertChannelConfigA]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__078d47bb0b8298d3f3c7879591580f96fc5873696118707aa8cd85007d94e2fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AlertChannel",
    "AlertChannelConfig",
    "AlertChannelConfigA",
    "AlertChannelConfigAOutputReference",
]

publication.publish()

def _typecheckingstub__e3b5e862284375f0c9eeda12c697cfa2d0486129cf845d45fc465978d8999796(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    type: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
    config: typing.Optional[typing.Union[AlertChannelConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__bc6d91d206bcd102f9b61178ed587b26ec7d61d95ba6ac505dc4946f9e384e9e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2602e1a557b92db237ff56526a2074a4d08c4c52e1ec16d8991f6b396aef44(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec32047e15d776161464c7ed35f041eb0ef78bb4e3ec19cba47763fa8fef872e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc768690c0ba5ada78e2d647a4b0fe30720ce6c7c972c945049bc78e6c28eaf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5059f889661ed85ad809dff3447a9ca120537cb8cb78b7f01b8895147c4b3bea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6cce12699578e3926be59f1dd9391597286d8af92e8e3e0ffd74d2b6cbe6b36(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    type: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
    config: typing.Optional[typing.Union[AlertChannelConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a5746c2e9e52df5745afb5ecc8360d8898afc597685bae990ef615f1dc9e0a(
    *,
    api_key: typing.Optional[builtins.str] = None,
    auth_password: typing.Optional[builtins.str] = None,
    auth_type: typing.Optional[builtins.str] = None,
    auth_username: typing.Optional[builtins.str] = None,
    base_url: typing.Optional[builtins.str] = None,
    channel: typing.Optional[builtins.str] = None,
    headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    headers_string: typing.Optional[builtins.str] = None,
    include_json_attachment: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    payload: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    payload_string: typing.Optional[builtins.str] = None,
    payload_type: typing.Optional[builtins.str] = None,
    recipients: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    route_key: typing.Optional[builtins.str] = None,
    service_key: typing.Optional[builtins.str] = None,
    tags: typing.Optional[builtins.str] = None,
    teams: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
    user_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9058079087f009af2e64d8a419d2afd13903e53e686000fa5e5a1eecf3dfa5ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f197ad04f11cf11107a4143746bddf9ba732c917f4f99059e6ef2714c863892(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a020a6dcf312a7cfc359cc584a1d0ff88d1d4230fda7077b8abe9b2ba66ce7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b63a571f032fc792aaab47c106ea11693c77c652872c88ed6a318325c241463d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44e05dc893d787b1374baf9471c27bba1cf7787f8c3476b417a9b242640e67e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ec76ba92b092dd4dfa0959bfcb859fcf5a34603b6b9b8f76c58e4cef2c8fa0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__634d25aef3b6a04acf4330126b02a0276fb085b4e0066cabbefaa5a254561cf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8de627fc56cc5270d19871970a0f9c7b43cc18be32098dbc5e23e3bdc2ac06(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2dcda80437e8391fd60099caf17c722b98f33694c6145273968151d9c0524ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3112b51d2163b389e47cd5afef5e9e6480489e8fbf50270dbc891195ada87dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a12dc68bd75ee06cc2169d2285bd082061ef0291ab19489ef358c0020ef233(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7c87b3ec47c531c58cdbd80f77e3f3a2149abe28eab341b2ceb3c9ed5a08f9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020e25b17087ce5084606fbc1170bbd7398b89f61d49a08629f3f0fbafe8aa12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5204979af217aa94ad99eb487c15a2bf9c209b76c5805a5175d980b8d709ff6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d080dc1b2ba704c117db222f57d78afac955b0d4a7e3124d509b722bf7a4b1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9576be1617d0a9328085d18a5afda882394c8e7b98fbfe28bd1ce5df0516966d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301e9746a24d17aadf928abdb4160dc3a145e94c535dd9be09b9facb3a92a633(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824e0328ac2852d58b6cab74417d7a47ea849947e5c00573047d2060e7a9be67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f30bd5b486ab640effe6e121a177b32e3b4b193c5ad76865f1c19365a00e17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a951e172c747f5676ddcf24e036b39dcdbe82345808f7390c271ca9a3558185d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8634f51912c98eff6b5c3585f589dbe9644817f3519a547325a5a6dd7008746b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478b9589f7f032c4988dc001507992dfc277cb42e9dc6eedbc52ec44c8262e58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078d47bb0b8298d3f3c7879591580f96fc5873696118707aa8cd85007d94e2fd(
    value: typing.Optional[AlertChannelConfigA],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `pagerduty_webhook_subscription`

Refer to the Terraform Registry for docs: [`pagerduty_webhook_subscription`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription).
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


class WebhookSubscription(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.webhookSubscription.WebhookSubscription",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription pagerduty_webhook_subscription}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        delivery_method: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebhookSubscriptionDeliveryMethod", typing.Dict[builtins.str, typing.Any]]]],
        events: typing.Sequence[builtins.str],
        filter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebhookSubscriptionFilter", typing.Dict[builtins.str, typing.Any]]]],
        active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription pagerduty_webhook_subscription} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param delivery_method: delivery_method block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#delivery_method WebhookSubscription#delivery_method}
        :param events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#events WebhookSubscription#events}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#filter WebhookSubscription#filter}
        :param active: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#active WebhookSubscription#active}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#description WebhookSubscription#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#id WebhookSubscription#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#type WebhookSubscription#type}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ef75b6c5bb5abb815c29c9193b8184bb7dcaa1ba8a99eb8d5193ad22eab6cba)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WebhookSubscriptionConfig(
            delivery_method=delivery_method,
            events=events,
            filter=filter,
            active=active,
            description=description,
            id=id,
            type=type,
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
        '''Generates CDKTF code for importing a WebhookSubscription resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WebhookSubscription to import.
        :param import_from_id: The id of the existing WebhookSubscription that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WebhookSubscription to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__368b0ede03c1131f76c721c23ccf8f5e79cfb4a4439e3670f73f383587aa33a3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDeliveryMethod")
    def put_delivery_method(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebhookSubscriptionDeliveryMethod", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee3e44cce95d4ff5c666ea9fcf92ee6834ec32d6207487e4e649f63acb01619a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeliveryMethod", [value]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebhookSubscriptionFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ed1057a850977ce864143f3950cf59b923dc55531094708642336d15180643)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="resetActive")
    def reset_active(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActive", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
    @jsii.member(jsii_name="deliveryMethod")
    def delivery_method(self) -> "WebhookSubscriptionDeliveryMethodList":
        return typing.cast("WebhookSubscriptionDeliveryMethodList", jsii.get(self, "deliveryMethod"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> "WebhookSubscriptionFilterList":
        return typing.cast("WebhookSubscriptionFilterList", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="activeInput")
    def active_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "activeInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryMethodInput")
    def delivery_method_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebhookSubscriptionDeliveryMethod"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebhookSubscriptionDeliveryMethod"]]], jsii.get(self, "deliveryMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="eventsInput")
    def events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "eventsInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebhookSubscriptionFilter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebhookSubscriptionFilter"]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="active")
    def active(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "active"))

    @active.setter
    def active(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f778528001fccd005b99749b7a2f2aacfd396037f27d9ebd56a03e3a138345)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "active", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__813e3c16b77b2173f6f3db072392384d85ba6e9592afc032c9042e25450b3a14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="events")
    def events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "events"))

    @events.setter
    def events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0db5e418d1ffbb5bd863d22cdb05a6440356f845adef2566b618b3c0c6c4ab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "events", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa04073ccae4722496e7d2f2af8ff1e9d2a569729178f8b5febadb3ed4e8d853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e1a10bb388d069882110dd98bf019fd5689fe5185f053457f38cf65229cd8b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.webhookSubscription.WebhookSubscriptionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "delivery_method": "deliveryMethod",
        "events": "events",
        "filter": "filter",
        "active": "active",
        "description": "description",
        "id": "id",
        "type": "type",
    },
)
class WebhookSubscriptionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        delivery_method: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebhookSubscriptionDeliveryMethod", typing.Dict[builtins.str, typing.Any]]]],
        events: typing.Sequence[builtins.str],
        filter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebhookSubscriptionFilter", typing.Dict[builtins.str, typing.Any]]]],
        active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param delivery_method: delivery_method block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#delivery_method WebhookSubscription#delivery_method}
        :param events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#events WebhookSubscription#events}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#filter WebhookSubscription#filter}
        :param active: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#active WebhookSubscription#active}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#description WebhookSubscription#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#id WebhookSubscription#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#type WebhookSubscription#type}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f25001c1e52d31068a41294bd885585ad41cc7218e54f7b58b6aa0c87a8c1b9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument delivery_method", value=delivery_method, expected_type=type_hints["delivery_method"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument active", value=active, expected_type=type_hints["active"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delivery_method": delivery_method,
            "events": events,
            "filter": filter,
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
        if active is not None:
            self._values["active"] = active
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if type is not None:
            self._values["type"] = type

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
    def delivery_method(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebhookSubscriptionDeliveryMethod"]]:
        '''delivery_method block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#delivery_method WebhookSubscription#delivery_method}
        '''
        result = self._values.get("delivery_method")
        assert result is not None, "Required property 'delivery_method' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebhookSubscriptionDeliveryMethod"]], result)

    @builtins.property
    def events(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#events WebhookSubscription#events}.'''
        result = self._values.get("events")
        assert result is not None, "Required property 'events' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebhookSubscriptionFilter"]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#filter WebhookSubscription#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebhookSubscriptionFilter"]], result)

    @builtins.property
    def active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#active WebhookSubscription#active}.'''
        result = self._values.get("active")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#description WebhookSubscription#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#id WebhookSubscription#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#type WebhookSubscription#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebhookSubscriptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.webhookSubscription.WebhookSubscriptionDeliveryMethod",
    jsii_struct_bases=[],
    name_mapping={
        "custom_header": "customHeader",
        "temporarily_disabled": "temporarilyDisabled",
        "type": "type",
        "url": "url",
    },
)
class WebhookSubscriptionDeliveryMethod:
    def __init__(
        self,
        *,
        custom_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebhookSubscriptionDeliveryMethodCustomHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        temporarily_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        type: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_header: custom_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#custom_header WebhookSubscription#custom_header}
        :param temporarily_disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#temporarily_disabled WebhookSubscription#temporarily_disabled}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#type WebhookSubscription#type}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#url WebhookSubscription#url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e7a45bc42a2805ca32f742ca5e2d518fd3e8aba1e27b34772fe39677792983)
            check_type(argname="argument custom_header", value=custom_header, expected_type=type_hints["custom_header"])
            check_type(argname="argument temporarily_disabled", value=temporarily_disabled, expected_type=type_hints["temporarily_disabled"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_header is not None:
            self._values["custom_header"] = custom_header
        if temporarily_disabled is not None:
            self._values["temporarily_disabled"] = temporarily_disabled
        if type is not None:
            self._values["type"] = type
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def custom_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebhookSubscriptionDeliveryMethodCustomHeader"]]]:
        '''custom_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#custom_header WebhookSubscription#custom_header}
        '''
        result = self._values.get("custom_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebhookSubscriptionDeliveryMethodCustomHeader"]]], result)

    @builtins.property
    def temporarily_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#temporarily_disabled WebhookSubscription#temporarily_disabled}.'''
        result = self._values.get("temporarily_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#type WebhookSubscription#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#url WebhookSubscription#url}.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebhookSubscriptionDeliveryMethod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.webhookSubscription.WebhookSubscriptionDeliveryMethodCustomHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class WebhookSubscriptionDeliveryMethodCustomHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#name WebhookSubscription#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#value WebhookSubscription#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__593368252c0d8b4539f368e5046d6b298c107f7bbcc061679642df6e5b6f7db0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#name WebhookSubscription#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#value WebhookSubscription#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebhookSubscriptionDeliveryMethodCustomHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebhookSubscriptionDeliveryMethodCustomHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.webhookSubscription.WebhookSubscriptionDeliveryMethodCustomHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df34d55b3639813ef7c751bde574ac174d82397fcc199f9a2c8149e4cbb3ca9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WebhookSubscriptionDeliveryMethodCustomHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57fa4435f9ccd1f1de6c054e062ad9d7c48f782b82364609a1f11ea06f782396)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WebhookSubscriptionDeliveryMethodCustomHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71baed10d00d6ddf589aea177c5832d25a734151e0fe432a1c87dbe094a8e710)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5cb4a7f9dd9aa83a976ae7c3924f4fb45a44ae933c0e9b71c6b1cdf754a5187)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e236401298a3aef14991c6a6aeb4061f3e6bdce244d31b3c09bd20ca1b1c28e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebhookSubscriptionDeliveryMethodCustomHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebhookSubscriptionDeliveryMethodCustomHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebhookSubscriptionDeliveryMethodCustomHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d07de71b7da2a89cf247f39b0aa78076e9fae320826c8b66ab7f91811896e90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WebhookSubscriptionDeliveryMethodCustomHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.webhookSubscription.WebhookSubscriptionDeliveryMethodCustomHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6606ace2dc835e8c21f1aa75150993335db7783ec5e1cf0a8a74a16bbbf9a14b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__743d12724de4365cce919bab46324bbca434304c27432edf4e720bc4c995ba77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d12a0a3bd998c6ddaefb5916bca1e0c7d839b6986c92a75d9167859f074e4ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebhookSubscriptionDeliveryMethodCustomHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebhookSubscriptionDeliveryMethodCustomHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebhookSubscriptionDeliveryMethodCustomHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a36f66b58542029c13d82ff49dcc28bdbe52866892c00d79d1f7674ce850d835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WebhookSubscriptionDeliveryMethodList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.webhookSubscription.WebhookSubscriptionDeliveryMethodList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14a58159e41394bd866ac95548c9086571628b99a435019f0c22fd0fde71e3c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WebhookSubscriptionDeliveryMethodOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec12dc232dc19ca8b464512c6a778832393b01f607c63647050bd20ddd1b5084)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WebhookSubscriptionDeliveryMethodOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc804a3bc85d8757604c80a0e6dbe1f04de62c25c36607896e011c2ec8e7c61)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7937ae36275c2d1965e4811fc1ede6c17ff3015a3fafc9a75981c8d756ab5232)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a3e3a4415e3f289640946751d94d56eb6bf80f99fe4e31061c016684276c5ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebhookSubscriptionDeliveryMethod]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebhookSubscriptionDeliveryMethod]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebhookSubscriptionDeliveryMethod]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae8e8da4f22077faadac555c002108d6610b9bacc06cf4a578ec5ed5b8917ca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WebhookSubscriptionDeliveryMethodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.webhookSubscription.WebhookSubscriptionDeliveryMethodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b70c8e7fa52f1ccee3f8cd3c6d6f5880417c13668e07f50004667764dc062f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCustomHeader")
    def put_custom_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebhookSubscriptionDeliveryMethodCustomHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43f1db1eb5e0cd01e385fb940d4a53880842cf531857a841d6154a4c62eea25c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomHeader", [value]))

    @jsii.member(jsii_name="resetCustomHeader")
    def reset_custom_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomHeader", []))

    @jsii.member(jsii_name="resetTemporarilyDisabled")
    def reset_temporarily_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemporarilyDisabled", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="customHeader")
    def custom_header(self) -> WebhookSubscriptionDeliveryMethodCustomHeaderList:
        return typing.cast(WebhookSubscriptionDeliveryMethodCustomHeaderList, jsii.get(self, "customHeader"))

    @builtins.property
    @jsii.member(jsii_name="customHeaderInput")
    def custom_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebhookSubscriptionDeliveryMethodCustomHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebhookSubscriptionDeliveryMethodCustomHeader]]], jsii.get(self, "customHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="temporarilyDisabledInput")
    def temporarily_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "temporarilyDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="temporarilyDisabled")
    def temporarily_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "temporarilyDisabled"))

    @temporarily_disabled.setter
    def temporarily_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e778e4977dec23d09df1a50d37e711517e83c1d5f9bf8f2489d6bf4e85172268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "temporarilyDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a6aa83a8dab71c8afe7722795848a80ec828ef369dbb4238f2862559d5bf80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdb258ec241c13c404bae7dc6649b9ba0a330c262ba85d3f5848383bf026ca9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebhookSubscriptionDeliveryMethod]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebhookSubscriptionDeliveryMethod]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebhookSubscriptionDeliveryMethod]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07f53967ccbc8f39d6fd861f25674f44d1a504540b224f823dcc709907bada10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.webhookSubscription.WebhookSubscriptionFilter",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "id": "id"},
)
class WebhookSubscriptionFilter:
    def __init__(
        self,
        *,
        type: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#type WebhookSubscription#type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#id WebhookSubscription#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ff36254a3c3294ace7139c9ce87b778a5befdf019ec44426a1c95100cb4719)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#type WebhookSubscription#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/webhook_subscription#id WebhookSubscription#id}.

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
        return "WebhookSubscriptionFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebhookSubscriptionFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.webhookSubscription.WebhookSubscriptionFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce83c26a48f96746362307051cf5eefe815ff5c586760b1c260c16a07ec7ed1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "WebhookSubscriptionFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0738245c408863a7ee6061c934e0b82a0b4b64949e4eeee1557813efe555c652)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WebhookSubscriptionFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd33e9e914e236b6aa03b0bb4c2e8d122d50a43113397a4b2d1f214d5576f64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da005a2f13855e487e99677a5a3a44947fb0c4d4943e28f18aa98eb93bc42d78)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11eb218aba26f6a91dd7050b5b3f1fd5419a801e6bb025436eb646b3a89d86c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebhookSubscriptionFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebhookSubscriptionFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebhookSubscriptionFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515e8b8abb8c443e3b87674840fd839c0c7a6ac0207ac97a9059ea7c9edf7d87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WebhookSubscriptionFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.webhookSubscription.WebhookSubscriptionFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a9a02086f880245469c3b6ae0d864061c80753d6f29e6b732122647027c48ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fe85ebbadd6c02dc3c4e213a4d156bc81ff907e403008bf1f9c6130bed877eb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e84609ba169ac295ad180bd34f48a4f38cdb7f0b1289f7bed94153003599d01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebhookSubscriptionFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebhookSubscriptionFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebhookSubscriptionFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8047237d1af935d185cb000a52fa3481e28a20f0b3d50257b045508a7c1e276)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WebhookSubscription",
    "WebhookSubscriptionConfig",
    "WebhookSubscriptionDeliveryMethod",
    "WebhookSubscriptionDeliveryMethodCustomHeader",
    "WebhookSubscriptionDeliveryMethodCustomHeaderList",
    "WebhookSubscriptionDeliveryMethodCustomHeaderOutputReference",
    "WebhookSubscriptionDeliveryMethodList",
    "WebhookSubscriptionDeliveryMethodOutputReference",
    "WebhookSubscriptionFilter",
    "WebhookSubscriptionFilterList",
    "WebhookSubscriptionFilterOutputReference",
]

publication.publish()

def _typecheckingstub__1ef75b6c5bb5abb815c29c9193b8184bb7dcaa1ba8a99eb8d5193ad22eab6cba(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    delivery_method: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebhookSubscriptionDeliveryMethod, typing.Dict[builtins.str, typing.Any]]]],
    events: typing.Sequence[builtins.str],
    filter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebhookSubscriptionFilter, typing.Dict[builtins.str, typing.Any]]]],
    active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__368b0ede03c1131f76c721c23ccf8f5e79cfb4a4439e3670f73f383587aa33a3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee3e44cce95d4ff5c666ea9fcf92ee6834ec32d6207487e4e649f63acb01619a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebhookSubscriptionDeliveryMethod, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ed1057a850977ce864143f3950cf59b923dc55531094708642336d15180643(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebhookSubscriptionFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f778528001fccd005b99749b7a2f2aacfd396037f27d9ebd56a03e3a138345(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813e3c16b77b2173f6f3db072392384d85ba6e9592afc032c9042e25450b3a14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0db5e418d1ffbb5bd863d22cdb05a6440356f845adef2566b618b3c0c6c4ab0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa04073ccae4722496e7d2f2af8ff1e9d2a569729178f8b5febadb3ed4e8d853(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1a10bb388d069882110dd98bf019fd5689fe5185f053457f38cf65229cd8b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f25001c1e52d31068a41294bd885585ad41cc7218e54f7b58b6aa0c87a8c1b9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    delivery_method: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebhookSubscriptionDeliveryMethod, typing.Dict[builtins.str, typing.Any]]]],
    events: typing.Sequence[builtins.str],
    filter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebhookSubscriptionFilter, typing.Dict[builtins.str, typing.Any]]]],
    active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e7a45bc42a2805ca32f742ca5e2d518fd3e8aba1e27b34772fe39677792983(
    *,
    custom_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebhookSubscriptionDeliveryMethodCustomHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    temporarily_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__593368252c0d8b4539f368e5046d6b298c107f7bbcc061679642df6e5b6f7db0(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df34d55b3639813ef7c751bde574ac174d82397fcc199f9a2c8149e4cbb3ca9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57fa4435f9ccd1f1de6c054e062ad9d7c48f782b82364609a1f11ea06f782396(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71baed10d00d6ddf589aea177c5832d25a734151e0fe432a1c87dbe094a8e710(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5cb4a7f9dd9aa83a976ae7c3924f4fb45a44ae933c0e9b71c6b1cdf754a5187(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e236401298a3aef14991c6a6aeb4061f3e6bdce244d31b3c09bd20ca1b1c28e6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d07de71b7da2a89cf247f39b0aa78076e9fae320826c8b66ab7f91811896e90(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebhookSubscriptionDeliveryMethodCustomHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6606ace2dc835e8c21f1aa75150993335db7783ec5e1cf0a8a74a16bbbf9a14b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743d12724de4365cce919bab46324bbca434304c27432edf4e720bc4c995ba77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d12a0a3bd998c6ddaefb5916bca1e0c7d839b6986c92a75d9167859f074e4ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a36f66b58542029c13d82ff49dcc28bdbe52866892c00d79d1f7674ce850d835(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebhookSubscriptionDeliveryMethodCustomHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a58159e41394bd866ac95548c9086571628b99a435019f0c22fd0fde71e3c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec12dc232dc19ca8b464512c6a778832393b01f607c63647050bd20ddd1b5084(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc804a3bc85d8757604c80a0e6dbe1f04de62c25c36607896e011c2ec8e7c61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7937ae36275c2d1965e4811fc1ede6c17ff3015a3fafc9a75981c8d756ab5232(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3e3a4415e3f289640946751d94d56eb6bf80f99fe4e31061c016684276c5ed(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8e8da4f22077faadac555c002108d6610b9bacc06cf4a578ec5ed5b8917ca0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebhookSubscriptionDeliveryMethod]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b70c8e7fa52f1ccee3f8cd3c6d6f5880417c13668e07f50004667764dc062f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f1db1eb5e0cd01e385fb940d4a53880842cf531857a841d6154a4c62eea25c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebhookSubscriptionDeliveryMethodCustomHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e778e4977dec23d09df1a50d37e711517e83c1d5f9bf8f2489d6bf4e85172268(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a6aa83a8dab71c8afe7722795848a80ec828ef369dbb4238f2862559d5bf80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb258ec241c13c404bae7dc6649b9ba0a330c262ba85d3f5848383bf026ca9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f53967ccbc8f39d6fd861f25674f44d1a504540b224f823dcc709907bada10(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebhookSubscriptionDeliveryMethod]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ff36254a3c3294ace7139c9ce87b778a5befdf019ec44426a1c95100cb4719(
    *,
    type: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce83c26a48f96746362307051cf5eefe815ff5c586760b1c260c16a07ec7ed1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0738245c408863a7ee6061c934e0b82a0b4b64949e4eeee1557813efe555c652(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd33e9e914e236b6aa03b0bb4c2e8d122d50a43113397a4b2d1f214d5576f64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da005a2f13855e487e99677a5a3a44947fb0c4d4943e28f18aa98eb93bc42d78(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11eb218aba26f6a91dd7050b5b3f1fd5419a801e6bb025436eb646b3a89d86c4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515e8b8abb8c443e3b87674840fd839c0c7a6ac0207ac97a9059ea7c9edf7d87(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebhookSubscriptionFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9a02086f880245469c3b6ae0d864061c80753d6f29e6b732122647027c48ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe85ebbadd6c02dc3c4e213a4d156bc81ff907e403008bf1f9c6130bed877eb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e84609ba169ac295ad180bd34f48a4f38cdb7f0b1289f7bed94153003599d01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8047237d1af935d185cb000a52fa3481e28a20f0b3d50257b045508a7c1e276(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebhookSubscriptionFilter]],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `opentelekomcloud_cts_event_notification_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_cts_event_notification_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3).
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


class CtsEventNotificationV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ctsEventNotificationV3.CtsEventNotificationV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3 opentelekomcloud_cts_event_notification_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        notification_name: builtins.str,
        operation_type: builtins.str,
        filter: typing.Optional[typing.Union["CtsEventNotificationV3Filter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        notify_user_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CtsEventNotificationV3NotifyUserListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CtsEventNotificationV3Operations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        status: typing.Optional[builtins.str] = None,
        topic_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3 opentelekomcloud_cts_event_notification_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param notification_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#notification_name CtsEventNotificationV3#notification_name}.
        :param operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#operation_type CtsEventNotificationV3#operation_type}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#filter CtsEventNotificationV3#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#id CtsEventNotificationV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notify_user_list: notify_user_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#notify_user_list CtsEventNotificationV3#notify_user_list}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#operations CtsEventNotificationV3#operations}
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#status CtsEventNotificationV3#status}.
        :param topic_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#topic_id CtsEventNotificationV3#topic_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e0659ea3793cba43b0f068265bdf1f4efd10465510ad718d97c50e06a92093)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CtsEventNotificationV3Config(
            notification_name=notification_name,
            operation_type=operation_type,
            filter=filter,
            id=id,
            notify_user_list=notify_user_list,
            operations=operations,
            status=status,
            topic_id=topic_id,
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
        '''Generates CDKTF code for importing a CtsEventNotificationV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CtsEventNotificationV3 to import.
        :param import_from_id: The id of the existing CtsEventNotificationV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CtsEventNotificationV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c900959e1fb7dd67fc633de912f5e1c214589a83447c8dff316c2a847a4b511)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        *,
        condition: builtins.str,
        rule: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#condition CtsEventNotificationV3#condition}.
        :param rule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#rule CtsEventNotificationV3#rule}.
        '''
        value = CtsEventNotificationV3Filter(condition=condition, rule=rule)

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putNotifyUserList")
    def put_notify_user_list(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CtsEventNotificationV3NotifyUserListStruct", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515742389e6e0d3b160f7c35381e0059ec59c80b29f063f6f7e628a45d529707)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNotifyUserList", [value]))

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CtsEventNotificationV3Operations", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8816c649223500b48221af41e666c18c25c04c8132c1e3ba5899c001a4cdc80f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperations", [value]))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNotifyUserList")
    def reset_notify_user_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifyUserList", []))

    @jsii.member(jsii_name="resetOperations")
    def reset_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperations", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTopicId")
    def reset_topic_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopicId", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> "CtsEventNotificationV3FilterOutputReference":
        return typing.cast("CtsEventNotificationV3FilterOutputReference", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="notificationId")
    def notification_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationId"))

    @builtins.property
    @jsii.member(jsii_name="notificationType")
    def notification_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationType"))

    @builtins.property
    @jsii.member(jsii_name="notifyUserList")
    def notify_user_list(self) -> "CtsEventNotificationV3NotifyUserListStructList":
        return typing.cast("CtsEventNotificationV3NotifyUserListStructList", jsii.get(self, "notifyUserList"))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(self) -> "CtsEventNotificationV3OperationsList":
        return typing.cast("CtsEventNotificationV3OperationsList", jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional["CtsEventNotificationV3Filter"]:
        return typing.cast(typing.Optional["CtsEventNotificationV3Filter"], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationNameInput")
    def notification_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyUserListInput")
    def notify_user_list_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CtsEventNotificationV3NotifyUserListStruct"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CtsEventNotificationV3NotifyUserListStruct"]]], jsii.get(self, "notifyUserListInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CtsEventNotificationV3Operations"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CtsEventNotificationV3Operations"]]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="operationTypeInput")
    def operation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="topicIdInput")
    def topic_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30aa21c7bee5f0c769ada674a6d49fb36c40685c2423df66610d19c018ba9441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationName")
    def notification_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationName"))

    @notification_name.setter
    def notification_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd8c43e8e10c4566107a3b9b57cef577e321050d194eea2dc52a17679e286b60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operationType")
    def operation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationType"))

    @operation_type.setter
    def operation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__884db3ccbb2d1f0cec9992f19a8e3ed77699a8199942cacab60e97130125937b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0424c9a23339c19e282cf434ee472e6b7f86182d83f1dcee48aca8cc73b8ee76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topicId")
    def topic_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topicId"))

    @topic_id.setter
    def topic_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b86bb5a5499428b0e3a628a35c5d0aa7a4b68a69b1f38b0e4d8fc8e324c414b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ctsEventNotificationV3.CtsEventNotificationV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "notification_name": "notificationName",
        "operation_type": "operationType",
        "filter": "filter",
        "id": "id",
        "notify_user_list": "notifyUserList",
        "operations": "operations",
        "status": "status",
        "topic_id": "topicId",
    },
)
class CtsEventNotificationV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        notification_name: builtins.str,
        operation_type: builtins.str,
        filter: typing.Optional[typing.Union["CtsEventNotificationV3Filter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        notify_user_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CtsEventNotificationV3NotifyUserListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CtsEventNotificationV3Operations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        status: typing.Optional[builtins.str] = None,
        topic_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param notification_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#notification_name CtsEventNotificationV3#notification_name}.
        :param operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#operation_type CtsEventNotificationV3#operation_type}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#filter CtsEventNotificationV3#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#id CtsEventNotificationV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notify_user_list: notify_user_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#notify_user_list CtsEventNotificationV3#notify_user_list}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#operations CtsEventNotificationV3#operations}
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#status CtsEventNotificationV3#status}.
        :param topic_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#topic_id CtsEventNotificationV3#topic_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(filter, dict):
            filter = CtsEventNotificationV3Filter(**filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfeb92d1c00e028e21a4db710bd4ce485c63f6f7bd304a3f2d1f92d41f286c26)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument notification_name", value=notification_name, expected_type=type_hints["notification_name"])
            check_type(argname="argument operation_type", value=operation_type, expected_type=type_hints["operation_type"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notify_user_list", value=notify_user_list, expected_type=type_hints["notify_user_list"])
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument topic_id", value=topic_id, expected_type=type_hints["topic_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "notification_name": notification_name,
            "operation_type": operation_type,
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
        if filter is not None:
            self._values["filter"] = filter
        if id is not None:
            self._values["id"] = id
        if notify_user_list is not None:
            self._values["notify_user_list"] = notify_user_list
        if operations is not None:
            self._values["operations"] = operations
        if status is not None:
            self._values["status"] = status
        if topic_id is not None:
            self._values["topic_id"] = topic_id

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
    def notification_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#notification_name CtsEventNotificationV3#notification_name}.'''
        result = self._values.get("notification_name")
        assert result is not None, "Required property 'notification_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operation_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#operation_type CtsEventNotificationV3#operation_type}.'''
        result = self._values.get("operation_type")
        assert result is not None, "Required property 'operation_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(self) -> typing.Optional["CtsEventNotificationV3Filter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#filter CtsEventNotificationV3#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional["CtsEventNotificationV3Filter"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#id CtsEventNotificationV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notify_user_list(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CtsEventNotificationV3NotifyUserListStruct"]]]:
        '''notify_user_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#notify_user_list CtsEventNotificationV3#notify_user_list}
        '''
        result = self._values.get("notify_user_list")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CtsEventNotificationV3NotifyUserListStruct"]]], result)

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CtsEventNotificationV3Operations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#operations CtsEventNotificationV3#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CtsEventNotificationV3Operations"]]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#status CtsEventNotificationV3#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#topic_id CtsEventNotificationV3#topic_id}.'''
        result = self._values.get("topic_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CtsEventNotificationV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ctsEventNotificationV3.CtsEventNotificationV3Filter",
    jsii_struct_bases=[],
    name_mapping={"condition": "condition", "rule": "rule"},
)
class CtsEventNotificationV3Filter:
    def __init__(
        self,
        *,
        condition: builtins.str,
        rule: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#condition CtsEventNotificationV3#condition}.
        :param rule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#rule CtsEventNotificationV3#rule}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f267a43355e799ea0f6fcaaad77af447d19886d3e8999d69ace98ce2f0561868)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "condition": condition,
            "rule": rule,
        }

    @builtins.property
    def condition(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#condition CtsEventNotificationV3#condition}.'''
        result = self._values.get("condition")
        assert result is not None, "Required property 'condition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#rule CtsEventNotificationV3#rule}.'''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CtsEventNotificationV3Filter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CtsEventNotificationV3FilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ctsEventNotificationV3.CtsEventNotificationV3FilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b6130788db108c5dd15858a2328f43d0e74ed7935fe787447f8593b366cc4bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @condition.setter
    def condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5afc3a11121e0892fc84af9a8dcae671ce785ea7b7e230d70a6fea9de53b0aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "condition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rule"))

    @rule.setter
    def rule(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b238b64f921fab69490508537643f2cb66f08e80c83e272188437aaaf6d7ecb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CtsEventNotificationV3Filter]:
        return typing.cast(typing.Optional[CtsEventNotificationV3Filter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CtsEventNotificationV3Filter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ff62c7e297a7fcf4d0310bdd99181413532a84593132f1d4a9ef7ada267500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ctsEventNotificationV3.CtsEventNotificationV3NotifyUserListStruct",
    jsii_struct_bases=[],
    name_mapping={"user_group": "userGroup", "user_list": "userList"},
)
class CtsEventNotificationV3NotifyUserListStruct:
    def __init__(
        self,
        *,
        user_group: builtins.str,
        user_list: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param user_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#user_group CtsEventNotificationV3#user_group}.
        :param user_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#user_list CtsEventNotificationV3#user_list}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3df5f50764e847b22c5300ab7eb728da64cfadec66b07150270a299ecabf2259)
            check_type(argname="argument user_group", value=user_group, expected_type=type_hints["user_group"])
            check_type(argname="argument user_list", value=user_list, expected_type=type_hints["user_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_group": user_group,
            "user_list": user_list,
        }

    @builtins.property
    def user_group(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#user_group CtsEventNotificationV3#user_group}.'''
        result = self._values.get("user_group")
        assert result is not None, "Required property 'user_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_list(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#user_list CtsEventNotificationV3#user_list}.'''
        result = self._values.get("user_list")
        assert result is not None, "Required property 'user_list' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CtsEventNotificationV3NotifyUserListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CtsEventNotificationV3NotifyUserListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ctsEventNotificationV3.CtsEventNotificationV3NotifyUserListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b0273b8808f795887388f43813d8aba581ae494d4673c0d744cfbdfd9685699)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CtsEventNotificationV3NotifyUserListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd78ed4507e1cec6ef27496e6ba235c8b86bb060e8f86073dc5f4ec6a94420b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CtsEventNotificationV3NotifyUserListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae20464f860b34e19b9396891488d79eee6d699afc3dd3ddf4d37f7abcc738ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42b01f50d8f36c3fae2be60a2d479fc10310435e272038f63d999bc39d418fc6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a237762f7884318b1cac3003eca7bb16c9722fd1288f726ddcb35e2690cb806)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CtsEventNotificationV3NotifyUserListStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CtsEventNotificationV3NotifyUserListStruct]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CtsEventNotificationV3NotifyUserListStruct]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b270221800f4e373df66c08454a9b1d454122fa9cae90218faf45c119ba53e9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CtsEventNotificationV3NotifyUserListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ctsEventNotificationV3.CtsEventNotificationV3NotifyUserListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__529a9aadd8e4121e86b6d943b7d7c5a55ed509a12a3304780ac446ca8e1738a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="userGroupInput")
    def user_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="userListInput")
    def user_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userListInput"))

    @builtins.property
    @jsii.member(jsii_name="userGroup")
    def user_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userGroup"))

    @user_group.setter
    def user_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bca48c75587643c3fdd18c73109c436d1d0ea028149690b92c20463d8b45804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userList")
    def user_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userList"))

    @user_list.setter
    def user_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3f614be2069f340526497f3e264be9149b395517722be8718b0385b9132e7de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CtsEventNotificationV3NotifyUserListStruct]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CtsEventNotificationV3NotifyUserListStruct]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CtsEventNotificationV3NotifyUserListStruct]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145826e2af5bcc342b49de771ab0b62b8c36ae514bc9030cc183c38271fa3468)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ctsEventNotificationV3.CtsEventNotificationV3Operations",
    jsii_struct_bases=[],
    name_mapping={
        "resource_type": "resourceType",
        "service_type": "serviceType",
        "trace_names": "traceNames",
    },
)
class CtsEventNotificationV3Operations:
    def __init__(
        self,
        *,
        resource_type: builtins.str,
        service_type: builtins.str,
        trace_names: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#resource_type CtsEventNotificationV3#resource_type}.
        :param service_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#service_type CtsEventNotificationV3#service_type}.
        :param trace_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#trace_names CtsEventNotificationV3#trace_names}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb6ad64ad39a2bbb6be046a69b60daaff4e0f20c36ca594f4b48d4c7cc0099b2)
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument service_type", value=service_type, expected_type=type_hints["service_type"])
            check_type(argname="argument trace_names", value=trace_names, expected_type=type_hints["trace_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_type": resource_type,
            "service_type": service_type,
            "trace_names": trace_names,
        }

    @builtins.property
    def resource_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#resource_type CtsEventNotificationV3#resource_type}.'''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#service_type CtsEventNotificationV3#service_type}.'''
        result = self._values.get("service_type")
        assert result is not None, "Required property 'service_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trace_names(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cts_event_notification_v3#trace_names CtsEventNotificationV3#trace_names}.'''
        result = self._values.get("trace_names")
        assert result is not None, "Required property 'trace_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CtsEventNotificationV3Operations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CtsEventNotificationV3OperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ctsEventNotificationV3.CtsEventNotificationV3OperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1a0dc8783c99441f8780f16ae947ef28960b2ac02e85bb78e2a019efa0d91d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CtsEventNotificationV3OperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d583be3c0af45b1ccde5aba9b50e5fc08cbfdea6511a27e1dbfea5c5b9b98346)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CtsEventNotificationV3OperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d2e713d71adcc8a2e10aa4b14c7efa21411ccb4e36f4ac0223bf5d843bae53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8efe4e8c16fbafc0a3caef935abe0103d6e3060ce05789eccb8b70138e56315b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26af040bcdc09b7a13daba4802a08e5236986e09a6b682ccd4286414227125ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CtsEventNotificationV3Operations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CtsEventNotificationV3Operations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CtsEventNotificationV3Operations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1560bd68e9af33bdc4b4c0d8f70f87dcb8d21b4ff92c6851352ca1e51f94070a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CtsEventNotificationV3OperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ctsEventNotificationV3.CtsEventNotificationV3OperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a831d2f21c995d2251fc1948081bd29cf9779f302c5969296dbf2e8da91fca8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceTypeInput")
    def service_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="traceNamesInput")
    def trace_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "traceNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125cf956ff8e4f9511bc773b117006ca0e305b5133ea35652381049bb6810118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceType")
    def service_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceType"))

    @service_type.setter
    def service_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a25a59d9a3423e8bb4f56e9013b411d48083e60e3ff8052531ebf078c15aee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="traceNames")
    def trace_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "traceNames"))

    @trace_names.setter
    def trace_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__906c93abb364578d113cadf7bc816049cd9a05042e2e299b9cbac7a30446b978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "traceNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CtsEventNotificationV3Operations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CtsEventNotificationV3Operations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CtsEventNotificationV3Operations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44407da81d42d54838863c113192419c94fc463597d240fd2354e441082fc210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CtsEventNotificationV3",
    "CtsEventNotificationV3Config",
    "CtsEventNotificationV3Filter",
    "CtsEventNotificationV3FilterOutputReference",
    "CtsEventNotificationV3NotifyUserListStruct",
    "CtsEventNotificationV3NotifyUserListStructList",
    "CtsEventNotificationV3NotifyUserListStructOutputReference",
    "CtsEventNotificationV3Operations",
    "CtsEventNotificationV3OperationsList",
    "CtsEventNotificationV3OperationsOutputReference",
]

publication.publish()

def _typecheckingstub__d1e0659ea3793cba43b0f068265bdf1f4efd10465510ad718d97c50e06a92093(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    notification_name: builtins.str,
    operation_type: builtins.str,
    filter: typing.Optional[typing.Union[CtsEventNotificationV3Filter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    notify_user_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CtsEventNotificationV3NotifyUserListStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CtsEventNotificationV3Operations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    status: typing.Optional[builtins.str] = None,
    topic_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__8c900959e1fb7dd67fc633de912f5e1c214589a83447c8dff316c2a847a4b511(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515742389e6e0d3b160f7c35381e0059ec59c80b29f063f6f7e628a45d529707(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CtsEventNotificationV3NotifyUserListStruct, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8816c649223500b48221af41e666c18c25c04c8132c1e3ba5899c001a4cdc80f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CtsEventNotificationV3Operations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30aa21c7bee5f0c769ada674a6d49fb36c40685c2423df66610d19c018ba9441(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8c43e8e10c4566107a3b9b57cef577e321050d194eea2dc52a17679e286b60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__884db3ccbb2d1f0cec9992f19a8e3ed77699a8199942cacab60e97130125937b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0424c9a23339c19e282cf434ee472e6b7f86182d83f1dcee48aca8cc73b8ee76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b86bb5a5499428b0e3a628a35c5d0aa7a4b68a69b1f38b0e4d8fc8e324c414b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfeb92d1c00e028e21a4db710bd4ce485c63f6f7bd304a3f2d1f92d41f286c26(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    notification_name: builtins.str,
    operation_type: builtins.str,
    filter: typing.Optional[typing.Union[CtsEventNotificationV3Filter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    notify_user_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CtsEventNotificationV3NotifyUserListStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CtsEventNotificationV3Operations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    status: typing.Optional[builtins.str] = None,
    topic_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f267a43355e799ea0f6fcaaad77af447d19886d3e8999d69ace98ce2f0561868(
    *,
    condition: builtins.str,
    rule: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6130788db108c5dd15858a2328f43d0e74ed7935fe787447f8593b366cc4bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5afc3a11121e0892fc84af9a8dcae671ce785ea7b7e230d70a6fea9de53b0aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b238b64f921fab69490508537643f2cb66f08e80c83e272188437aaaf6d7ecb9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ff62c7e297a7fcf4d0310bdd99181413532a84593132f1d4a9ef7ada267500(
    value: typing.Optional[CtsEventNotificationV3Filter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df5f50764e847b22c5300ab7eb728da64cfadec66b07150270a299ecabf2259(
    *,
    user_group: builtins.str,
    user_list: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0273b8808f795887388f43813d8aba581ae494d4673c0d744cfbdfd9685699(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd78ed4507e1cec6ef27496e6ba235c8b86bb060e8f86073dc5f4ec6a94420b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae20464f860b34e19b9396891488d79eee6d699afc3dd3ddf4d37f7abcc738ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b01f50d8f36c3fae2be60a2d479fc10310435e272038f63d999bc39d418fc6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a237762f7884318b1cac3003eca7bb16c9722fd1288f726ddcb35e2690cb806(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b270221800f4e373df66c08454a9b1d454122fa9cae90218faf45c119ba53e9c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CtsEventNotificationV3NotifyUserListStruct]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__529a9aadd8e4121e86b6d943b7d7c5a55ed509a12a3304780ac446ca8e1738a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bca48c75587643c3fdd18c73109c436d1d0ea028149690b92c20463d8b45804(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f614be2069f340526497f3e264be9149b395517722be8718b0385b9132e7de(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145826e2af5bcc342b49de771ab0b62b8c36ae514bc9030cc183c38271fa3468(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CtsEventNotificationV3NotifyUserListStruct]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6ad64ad39a2bbb6be046a69b60daaff4e0f20c36ca594f4b48d4c7cc0099b2(
    *,
    resource_type: builtins.str,
    service_type: builtins.str,
    trace_names: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1a0dc8783c99441f8780f16ae947ef28960b2ac02e85bb78e2a019efa0d91d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d583be3c0af45b1ccde5aba9b50e5fc08cbfdea6511a27e1dbfea5c5b9b98346(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d2e713d71adcc8a2e10aa4b14c7efa21411ccb4e36f4ac0223bf5d843bae53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8efe4e8c16fbafc0a3caef935abe0103d6e3060ce05789eccb8b70138e56315b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26af040bcdc09b7a13daba4802a08e5236986e09a6b682ccd4286414227125ad(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1560bd68e9af33bdc4b4c0d8f70f87dcb8d21b4ff92c6851352ca1e51f94070a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CtsEventNotificationV3Operations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a831d2f21c995d2251fc1948081bd29cf9779f302c5969296dbf2e8da91fca8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125cf956ff8e4f9511bc773b117006ca0e305b5133ea35652381049bb6810118(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a25a59d9a3423e8bb4f56e9013b411d48083e60e3ff8052531ebf078c15aee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906c93abb364578d113cadf7bc816049cd9a05042e2e299b9cbac7a30446b978(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44407da81d42d54838863c113192419c94fc463597d240fd2354e441082fc210(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CtsEventNotificationV3Operations]],
) -> None:
    """Type checking stubs"""
    pass

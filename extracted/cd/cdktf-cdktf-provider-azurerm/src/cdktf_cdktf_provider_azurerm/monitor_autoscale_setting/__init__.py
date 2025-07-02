r'''
# `azurerm_monitor_autoscale_setting`

Refer to the Terraform Registry for docs: [`azurerm_monitor_autoscale_setting`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting).
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


class MonitorAutoscaleSetting(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSetting",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting azurerm_monitor_autoscale_setting}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        profile: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAutoscaleSettingProfile", typing.Dict[builtins.str, typing.Any]]]],
        resource_group_name: builtins.str,
        target_resource_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        notification: typing.Optional[typing.Union["MonitorAutoscaleSettingNotification", typing.Dict[builtins.str, typing.Any]]] = None,
        predictive: typing.Optional[typing.Union["MonitorAutoscaleSettingPredictive", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorAutoscaleSettingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting azurerm_monitor_autoscale_setting} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#location MonitorAutoscaleSetting#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#name MonitorAutoscaleSetting#name}.
        :param profile: profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#profile MonitorAutoscaleSetting#profile}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#resource_group_name MonitorAutoscaleSetting#resource_group_name}.
        :param target_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#target_resource_id MonitorAutoscaleSetting#target_resource_id}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#enabled MonitorAutoscaleSetting#enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#id MonitorAutoscaleSetting#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification: notification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#notification MonitorAutoscaleSetting#notification}
        :param predictive: predictive block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#predictive MonitorAutoscaleSetting#predictive}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#tags MonitorAutoscaleSetting#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#timeouts MonitorAutoscaleSetting#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cada1144558e56fb576fa1040ab6319ba3a3c45878bbd8e10fdcaf3de194c74)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitorAutoscaleSettingConfig(
            location=location,
            name=name,
            profile=profile,
            resource_group_name=resource_group_name,
            target_resource_id=target_resource_id,
            enabled=enabled,
            id=id,
            notification=notification,
            predictive=predictive,
            tags=tags,
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
        '''Generates CDKTF code for importing a MonitorAutoscaleSetting resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MonitorAutoscaleSetting to import.
        :param import_from_id: The id of the existing MonitorAutoscaleSetting that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MonitorAutoscaleSetting to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba9d048938a97443edec8355ba5b6a08db743921f09d36808052ce21a92e9df)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putNotification")
    def put_notification(
        self,
        *,
        email: typing.Optional[typing.Union["MonitorAutoscaleSettingNotificationEmail", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAutoscaleSettingNotificationWebhook", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param email: email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#email MonitorAutoscaleSetting#email}
        :param webhook: webhook block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#webhook MonitorAutoscaleSetting#webhook}
        '''
        value = MonitorAutoscaleSettingNotification(email=email, webhook=webhook)

        return typing.cast(None, jsii.invoke(self, "putNotification", [value]))

    @jsii.member(jsii_name="putPredictive")
    def put_predictive(
        self,
        *,
        scale_mode: builtins.str,
        look_ahead_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scale_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#scale_mode MonitorAutoscaleSetting#scale_mode}.
        :param look_ahead_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#look_ahead_time MonitorAutoscaleSetting#look_ahead_time}.
        '''
        value = MonitorAutoscaleSettingPredictive(
            scale_mode=scale_mode, look_ahead_time=look_ahead_time
        )

        return typing.cast(None, jsii.invoke(self, "putPredictive", [value]))

    @jsii.member(jsii_name="putProfile")
    def put_profile(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAutoscaleSettingProfile", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f8449b88de799518113c522dfca37f629da470c3f20074bff615191e339176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProfile", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#create MonitorAutoscaleSetting#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#delete MonitorAutoscaleSetting#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#read MonitorAutoscaleSetting#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#update MonitorAutoscaleSetting#update}.
        '''
        value = MonitorAutoscaleSettingTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNotification")
    def reset_notification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotification", []))

    @jsii.member(jsii_name="resetPredictive")
    def reset_predictive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredictive", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="notification")
    def notification(self) -> "MonitorAutoscaleSettingNotificationOutputReference":
        return typing.cast("MonitorAutoscaleSettingNotificationOutputReference", jsii.get(self, "notification"))

    @builtins.property
    @jsii.member(jsii_name="predictive")
    def predictive(self) -> "MonitorAutoscaleSettingPredictiveOutputReference":
        return typing.cast("MonitorAutoscaleSettingPredictiveOutputReference", jsii.get(self, "predictive"))

    @builtins.property
    @jsii.member(jsii_name="profile")
    def profile(self) -> "MonitorAutoscaleSettingProfileList":
        return typing.cast("MonitorAutoscaleSettingProfileList", jsii.get(self, "profile"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MonitorAutoscaleSettingTimeoutsOutputReference":
        return typing.cast("MonitorAutoscaleSettingTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationInput")
    def notification_input(
        self,
    ) -> typing.Optional["MonitorAutoscaleSettingNotification"]:
        return typing.cast(typing.Optional["MonitorAutoscaleSettingNotification"], jsii.get(self, "notificationInput"))

    @builtins.property
    @jsii.member(jsii_name="predictiveInput")
    def predictive_input(self) -> typing.Optional["MonitorAutoscaleSettingPredictive"]:
        return typing.cast(typing.Optional["MonitorAutoscaleSettingPredictive"], jsii.get(self, "predictiveInput"))

    @builtins.property
    @jsii.member(jsii_name="profileInput")
    def profile_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAutoscaleSettingProfile"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAutoscaleSettingProfile"]]], jsii.get(self, "profileInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceIdInput")
    def target_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitorAutoscaleSettingTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitorAutoscaleSettingTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d56c27af2c5381ed869b1e548fe041fbfa887d38e616f0981cd48fbc243716e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b17d893e74a278fdc71617f56f673e8a0a3af35db4966366c931afa2df916c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ffef7bb1a348c6251260e4c8f169092a0764b23168682c82729af580327b1b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c97d935f959c874a5796c815e09d510edf62c2f52eee02d45b6b1eb189c53db0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e355bdf59272d33e23c4cc78f02836f36c4a8458ee272c562fa1b68680aac3a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc5ca1503f7a2407db12984723e5bfc00cb5942b0b6ed81ebce2033ee9182a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetResourceId")
    def target_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetResourceId"))

    @target_resource_id.setter
    def target_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bd0365c72d5d8c1ce83a3c53d4878062c0fbb383fecb7cc028f3fe452b6bc66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetResourceId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "profile": "profile",
        "resource_group_name": "resourceGroupName",
        "target_resource_id": "targetResourceId",
        "enabled": "enabled",
        "id": "id",
        "notification": "notification",
        "predictive": "predictive",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class MonitorAutoscaleSettingConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        profile: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAutoscaleSettingProfile", typing.Dict[builtins.str, typing.Any]]]],
        resource_group_name: builtins.str,
        target_resource_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        notification: typing.Optional[typing.Union["MonitorAutoscaleSettingNotification", typing.Dict[builtins.str, typing.Any]]] = None,
        predictive: typing.Optional[typing.Union["MonitorAutoscaleSettingPredictive", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorAutoscaleSettingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#location MonitorAutoscaleSetting#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#name MonitorAutoscaleSetting#name}.
        :param profile: profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#profile MonitorAutoscaleSetting#profile}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#resource_group_name MonitorAutoscaleSetting#resource_group_name}.
        :param target_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#target_resource_id MonitorAutoscaleSetting#target_resource_id}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#enabled MonitorAutoscaleSetting#enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#id MonitorAutoscaleSetting#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification: notification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#notification MonitorAutoscaleSetting#notification}
        :param predictive: predictive block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#predictive MonitorAutoscaleSetting#predictive}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#tags MonitorAutoscaleSetting#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#timeouts MonitorAutoscaleSetting#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(notification, dict):
            notification = MonitorAutoscaleSettingNotification(**notification)
        if isinstance(predictive, dict):
            predictive = MonitorAutoscaleSettingPredictive(**predictive)
        if isinstance(timeouts, dict):
            timeouts = MonitorAutoscaleSettingTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba6f8f649513c00b098b7661fe7b0a268c9301fcae4f90777ae07a6dd3643675)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument target_resource_id", value=target_resource_id, expected_type=type_hints["target_resource_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notification", value=notification, expected_type=type_hints["notification"])
            check_type(argname="argument predictive", value=predictive, expected_type=type_hints["predictive"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "profile": profile,
            "resource_group_name": resource_group_name,
            "target_resource_id": target_resource_id,
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
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if notification is not None:
            self._values["notification"] = notification
        if predictive is not None:
            self._values["predictive"] = predictive
        if tags is not None:
            self._values["tags"] = tags
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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#location MonitorAutoscaleSetting#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#name MonitorAutoscaleSetting#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def profile(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAutoscaleSettingProfile"]]:
        '''profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#profile MonitorAutoscaleSetting#profile}
        '''
        result = self._values.get("profile")
        assert result is not None, "Required property 'profile' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAutoscaleSettingProfile"]], result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#resource_group_name MonitorAutoscaleSetting#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#target_resource_id MonitorAutoscaleSetting#target_resource_id}.'''
        result = self._values.get("target_resource_id")
        assert result is not None, "Required property 'target_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#enabled MonitorAutoscaleSetting#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#id MonitorAutoscaleSetting#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification(self) -> typing.Optional["MonitorAutoscaleSettingNotification"]:
        '''notification block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#notification MonitorAutoscaleSetting#notification}
        '''
        result = self._values.get("notification")
        return typing.cast(typing.Optional["MonitorAutoscaleSettingNotification"], result)

    @builtins.property
    def predictive(self) -> typing.Optional["MonitorAutoscaleSettingPredictive"]:
        '''predictive block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#predictive MonitorAutoscaleSetting#predictive}
        '''
        result = self._values.get("predictive")
        return typing.cast(typing.Optional["MonitorAutoscaleSettingPredictive"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#tags MonitorAutoscaleSetting#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MonitorAutoscaleSettingTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#timeouts MonitorAutoscaleSetting#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MonitorAutoscaleSettingTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAutoscaleSettingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingNotification",
    jsii_struct_bases=[],
    name_mapping={"email": "email", "webhook": "webhook"},
)
class MonitorAutoscaleSettingNotification:
    def __init__(
        self,
        *,
        email: typing.Optional[typing.Union["MonitorAutoscaleSettingNotificationEmail", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAutoscaleSettingNotificationWebhook", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param email: email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#email MonitorAutoscaleSetting#email}
        :param webhook: webhook block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#webhook MonitorAutoscaleSetting#webhook}
        '''
        if isinstance(email, dict):
            email = MonitorAutoscaleSettingNotificationEmail(**email)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f29e1bf3ae76f88e2f0d989ffb6ca9127827a82569d254b7fbf938865297c8)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument webhook", value=webhook, expected_type=type_hints["webhook"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if email is not None:
            self._values["email"] = email
        if webhook is not None:
            self._values["webhook"] = webhook

    @builtins.property
    def email(self) -> typing.Optional["MonitorAutoscaleSettingNotificationEmail"]:
        '''email block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#email MonitorAutoscaleSetting#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional["MonitorAutoscaleSettingNotificationEmail"], result)

    @builtins.property
    def webhook(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAutoscaleSettingNotificationWebhook"]]]:
        '''webhook block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#webhook MonitorAutoscaleSetting#webhook}
        '''
        result = self._values.get("webhook")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAutoscaleSettingNotificationWebhook"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAutoscaleSettingNotification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingNotificationEmail",
    jsii_struct_bases=[],
    name_mapping={
        "custom_emails": "customEmails",
        "send_to_subscription_administrator": "sendToSubscriptionAdministrator",
        "send_to_subscription_co_administrator": "sendToSubscriptionCoAdministrator",
    },
)
class MonitorAutoscaleSettingNotificationEmail:
    def __init__(
        self,
        *,
        custom_emails: typing.Optional[typing.Sequence[builtins.str]] = None,
        send_to_subscription_administrator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_to_subscription_co_administrator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param custom_emails: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#custom_emails MonitorAutoscaleSetting#custom_emails}.
        :param send_to_subscription_administrator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#send_to_subscription_administrator MonitorAutoscaleSetting#send_to_subscription_administrator}.
        :param send_to_subscription_co_administrator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#send_to_subscription_co_administrator MonitorAutoscaleSetting#send_to_subscription_co_administrator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d530e04ba0ea7dce527b0011bb44a3f818fd6138f351a569da3a593f7311ad71)
            check_type(argname="argument custom_emails", value=custom_emails, expected_type=type_hints["custom_emails"])
            check_type(argname="argument send_to_subscription_administrator", value=send_to_subscription_administrator, expected_type=type_hints["send_to_subscription_administrator"])
            check_type(argname="argument send_to_subscription_co_administrator", value=send_to_subscription_co_administrator, expected_type=type_hints["send_to_subscription_co_administrator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_emails is not None:
            self._values["custom_emails"] = custom_emails
        if send_to_subscription_administrator is not None:
            self._values["send_to_subscription_administrator"] = send_to_subscription_administrator
        if send_to_subscription_co_administrator is not None:
            self._values["send_to_subscription_co_administrator"] = send_to_subscription_co_administrator

    @builtins.property
    def custom_emails(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#custom_emails MonitorAutoscaleSetting#custom_emails}.'''
        result = self._values.get("custom_emails")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def send_to_subscription_administrator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#send_to_subscription_administrator MonitorAutoscaleSetting#send_to_subscription_administrator}.'''
        result = self._values.get("send_to_subscription_administrator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def send_to_subscription_co_administrator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#send_to_subscription_co_administrator MonitorAutoscaleSetting#send_to_subscription_co_administrator}.'''
        result = self._values.get("send_to_subscription_co_administrator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAutoscaleSettingNotificationEmail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAutoscaleSettingNotificationEmailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingNotificationEmailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47e3e729081b59e77708e75c1f190f5b555a2b9990d81c17b3f7b1450d0ced32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCustomEmails")
    def reset_custom_emails(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomEmails", []))

    @jsii.member(jsii_name="resetSendToSubscriptionAdministrator")
    def reset_send_to_subscription_administrator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendToSubscriptionAdministrator", []))

    @jsii.member(jsii_name="resetSendToSubscriptionCoAdministrator")
    def reset_send_to_subscription_co_administrator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendToSubscriptionCoAdministrator", []))

    @builtins.property
    @jsii.member(jsii_name="customEmailsInput")
    def custom_emails_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "customEmailsInput"))

    @builtins.property
    @jsii.member(jsii_name="sendToSubscriptionAdministratorInput")
    def send_to_subscription_administrator_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendToSubscriptionAdministratorInput"))

    @builtins.property
    @jsii.member(jsii_name="sendToSubscriptionCoAdministratorInput")
    def send_to_subscription_co_administrator_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendToSubscriptionCoAdministratorInput"))

    @builtins.property
    @jsii.member(jsii_name="customEmails")
    def custom_emails(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customEmails"))

    @custom_emails.setter
    def custom_emails(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13aff88deaed3da03c27c691d73cb2f0c053abd5575011c04d2aec84a7570aa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customEmails", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendToSubscriptionAdministrator")
    def send_to_subscription_administrator(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendToSubscriptionAdministrator"))

    @send_to_subscription_administrator.setter
    def send_to_subscription_administrator(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcdd842650158dca19d684b8404729d221f5392da7f4b0225732e14e9973069d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendToSubscriptionAdministrator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendToSubscriptionCoAdministrator")
    def send_to_subscription_co_administrator(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendToSubscriptionCoAdministrator"))

    @send_to_subscription_co_administrator.setter
    def send_to_subscription_co_administrator(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea7fc9c7c4c817c6295ab8923a05b380f4eef24a3beacffdba88641a80c70200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendToSubscriptionCoAdministrator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAutoscaleSettingNotificationEmail]:
        return typing.cast(typing.Optional[MonitorAutoscaleSettingNotificationEmail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAutoscaleSettingNotificationEmail],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e4a599c80a492d30987c67cbabe77367563c40905907f53b105c4805358b903)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAutoscaleSettingNotificationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingNotificationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__611975ff4747917ce61e02fc27cb1bd46051b43a814ce989282af771525f1d55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEmail")
    def put_email(
        self,
        *,
        custom_emails: typing.Optional[typing.Sequence[builtins.str]] = None,
        send_to_subscription_administrator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_to_subscription_co_administrator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param custom_emails: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#custom_emails MonitorAutoscaleSetting#custom_emails}.
        :param send_to_subscription_administrator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#send_to_subscription_administrator MonitorAutoscaleSetting#send_to_subscription_administrator}.
        :param send_to_subscription_co_administrator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#send_to_subscription_co_administrator MonitorAutoscaleSetting#send_to_subscription_co_administrator}.
        '''
        value = MonitorAutoscaleSettingNotificationEmail(
            custom_emails=custom_emails,
            send_to_subscription_administrator=send_to_subscription_administrator,
            send_to_subscription_co_administrator=send_to_subscription_co_administrator,
        )

        return typing.cast(None, jsii.invoke(self, "putEmail", [value]))

    @jsii.member(jsii_name="putWebhook")
    def put_webhook(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAutoscaleSettingNotificationWebhook", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d906d75eaa006434b5e73806896a51b2bd989952771832584188fbfc8045a9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWebhook", [value]))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetWebhook")
    def reset_webhook(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebhook", []))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> MonitorAutoscaleSettingNotificationEmailOutputReference:
        return typing.cast(MonitorAutoscaleSettingNotificationEmailOutputReference, jsii.get(self, "email"))

    @builtins.property
    @jsii.member(jsii_name="webhook")
    def webhook(self) -> "MonitorAutoscaleSettingNotificationWebhookList":
        return typing.cast("MonitorAutoscaleSettingNotificationWebhookList", jsii.get(self, "webhook"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[MonitorAutoscaleSettingNotificationEmail]:
        return typing.cast(typing.Optional[MonitorAutoscaleSettingNotificationEmail], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookInput")
    def webhook_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAutoscaleSettingNotificationWebhook"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAutoscaleSettingNotificationWebhook"]]], jsii.get(self, "webhookInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorAutoscaleSettingNotification]:
        return typing.cast(typing.Optional[MonitorAutoscaleSettingNotification], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAutoscaleSettingNotification],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf0edf49d31192c6f0de45469af50190627c1253729901f4668cfb05258990b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingNotificationWebhook",
    jsii_struct_bases=[],
    name_mapping={"service_uri": "serviceUri", "properties": "properties"},
)
class MonitorAutoscaleSettingNotificationWebhook:
    def __init__(
        self,
        *,
        service_uri: builtins.str,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param service_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#service_uri MonitorAutoscaleSetting#service_uri}.
        :param properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#properties MonitorAutoscaleSetting#properties}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd285622b27a1a14a64808fda0ad6f288f996003e332189d56514c8e912256a)
            check_type(argname="argument service_uri", value=service_uri, expected_type=type_hints["service_uri"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_uri": service_uri,
        }
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def service_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#service_uri MonitorAutoscaleSetting#service_uri}.'''
        result = self._values.get("service_uri")
        assert result is not None, "Required property 'service_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#properties MonitorAutoscaleSetting#properties}.'''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAutoscaleSettingNotificationWebhook(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAutoscaleSettingNotificationWebhookList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingNotificationWebhookList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92a3f1f1acc48439e6c2394749a8b9a641c1ee6cdb63bd921993f2d71281a4e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorAutoscaleSettingNotificationWebhookOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb337218f90ec68c86ac5abe4edae23cf0e971ce83b3e35b0604d9537ee828f2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorAutoscaleSettingNotificationWebhookOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3126c7a6b466397e9b48e2ce29d327e20935796f47051d484f4ab5c929cfcc0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cdee6b31f122518f7719b6493dcf6d058a822ef62b9565fc1a4ce3d848e5df0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf143c1a374b29373c547d597547106278e3dfa3a7abd35782c05cb12a131fa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingNotificationWebhook]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingNotificationWebhook]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingNotificationWebhook]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e948a22f395589e18828f60df3e6958ff2768e4391dd561157c8e3801fe0acd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAutoscaleSettingNotificationWebhookOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingNotificationWebhookOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cd9193960f4ed68448b56b09c6ef7821486507fde4703c8b8e933ee1e72e3e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceUriInput")
    def service_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceUriInput"))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714a02bd9d8686b00a0c2dbe6a14dbb9480f46fa62d6eaa43b94b3a45d06b6a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceUri")
    def service_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceUri"))

    @service_uri.setter
    def service_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93310abfe2272809dd5db064a742696a4746bf7943dd144b4fb79f0b7219e58c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingNotificationWebhook]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingNotificationWebhook]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingNotificationWebhook]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a69fbdd3784abb6689e8a4a0196ceb2a28d256e882e8595bbf6c47f9ffb33732)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingPredictive",
    jsii_struct_bases=[],
    name_mapping={"scale_mode": "scaleMode", "look_ahead_time": "lookAheadTime"},
)
class MonitorAutoscaleSettingPredictive:
    def __init__(
        self,
        *,
        scale_mode: builtins.str,
        look_ahead_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scale_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#scale_mode MonitorAutoscaleSetting#scale_mode}.
        :param look_ahead_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#look_ahead_time MonitorAutoscaleSetting#look_ahead_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7068cc9f58a218b0d4885d7e18c0d7c21c86cd1235356d878e729e7661136c32)
            check_type(argname="argument scale_mode", value=scale_mode, expected_type=type_hints["scale_mode"])
            check_type(argname="argument look_ahead_time", value=look_ahead_time, expected_type=type_hints["look_ahead_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scale_mode": scale_mode,
        }
        if look_ahead_time is not None:
            self._values["look_ahead_time"] = look_ahead_time

    @builtins.property
    def scale_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#scale_mode MonitorAutoscaleSetting#scale_mode}.'''
        result = self._values.get("scale_mode")
        assert result is not None, "Required property 'scale_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def look_ahead_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#look_ahead_time MonitorAutoscaleSetting#look_ahead_time}.'''
        result = self._values.get("look_ahead_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAutoscaleSettingPredictive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAutoscaleSettingPredictiveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingPredictiveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bdf1b219aed0251146b134a0d4f6e5a743869e2811b845b71bce2179d6350e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLookAheadTime")
    def reset_look_ahead_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLookAheadTime", []))

    @builtins.property
    @jsii.member(jsii_name="lookAheadTimeInput")
    def look_ahead_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lookAheadTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleModeInput")
    def scale_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scaleModeInput"))

    @builtins.property
    @jsii.member(jsii_name="lookAheadTime")
    def look_ahead_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lookAheadTime"))

    @look_ahead_time.setter
    def look_ahead_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5240c411b9f420519b4559049de7ba3d1b05a39f2f59be6b589b7098b3f7847e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lookAheadTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleMode")
    def scale_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scaleMode"))

    @scale_mode.setter
    def scale_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b6775345c924c92e70897254d160dea0974d47f1d6d4731d3a35c9b6f3420d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorAutoscaleSettingPredictive]:
        return typing.cast(typing.Optional[MonitorAutoscaleSettingPredictive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAutoscaleSettingPredictive],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a0e555f5e5f9bb486a5881a984f414bdcab6e266d976a508109fcc78e21a9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfile",
    jsii_struct_bases=[],
    name_mapping={
        "capacity": "capacity",
        "name": "name",
        "fixed_date": "fixedDate",
        "recurrence": "recurrence",
        "rule": "rule",
    },
)
class MonitorAutoscaleSettingProfile:
    def __init__(
        self,
        *,
        capacity: typing.Union["MonitorAutoscaleSettingProfileCapacity", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        fixed_date: typing.Optional[typing.Union["MonitorAutoscaleSettingProfileFixedDate", typing.Dict[builtins.str, typing.Any]]] = None,
        recurrence: typing.Optional[typing.Union["MonitorAutoscaleSettingProfileRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAutoscaleSettingProfileRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param capacity: capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#capacity MonitorAutoscaleSetting#capacity}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#name MonitorAutoscaleSetting#name}.
        :param fixed_date: fixed_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#fixed_date MonitorAutoscaleSetting#fixed_date}
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#recurrence MonitorAutoscaleSetting#recurrence}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#rule MonitorAutoscaleSetting#rule}
        '''
        if isinstance(capacity, dict):
            capacity = MonitorAutoscaleSettingProfileCapacity(**capacity)
        if isinstance(fixed_date, dict):
            fixed_date = MonitorAutoscaleSettingProfileFixedDate(**fixed_date)
        if isinstance(recurrence, dict):
            recurrence = MonitorAutoscaleSettingProfileRecurrence(**recurrence)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a57d1292707572659d398bae1d5da0d88d06cbb2beff833979e8326c12e5de1)
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument fixed_date", value=fixed_date, expected_type=type_hints["fixed_date"])
            check_type(argname="argument recurrence", value=recurrence, expected_type=type_hints["recurrence"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity": capacity,
            "name": name,
        }
        if fixed_date is not None:
            self._values["fixed_date"] = fixed_date
        if recurrence is not None:
            self._values["recurrence"] = recurrence
        if rule is not None:
            self._values["rule"] = rule

    @builtins.property
    def capacity(self) -> "MonitorAutoscaleSettingProfileCapacity":
        '''capacity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#capacity MonitorAutoscaleSetting#capacity}
        '''
        result = self._values.get("capacity")
        assert result is not None, "Required property 'capacity' is missing"
        return typing.cast("MonitorAutoscaleSettingProfileCapacity", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#name MonitorAutoscaleSetting#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fixed_date(self) -> typing.Optional["MonitorAutoscaleSettingProfileFixedDate"]:
        '''fixed_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#fixed_date MonitorAutoscaleSetting#fixed_date}
        '''
        result = self._values.get("fixed_date")
        return typing.cast(typing.Optional["MonitorAutoscaleSettingProfileFixedDate"], result)

    @builtins.property
    def recurrence(self) -> typing.Optional["MonitorAutoscaleSettingProfileRecurrence"]:
        '''recurrence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#recurrence MonitorAutoscaleSetting#recurrence}
        '''
        result = self._values.get("recurrence")
        return typing.cast(typing.Optional["MonitorAutoscaleSettingProfileRecurrence"], result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAutoscaleSettingProfileRule"]]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#rule MonitorAutoscaleSetting#rule}
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAutoscaleSettingProfileRule"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAutoscaleSettingProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileCapacity",
    jsii_struct_bases=[],
    name_mapping={"default": "default", "maximum": "maximum", "minimum": "minimum"},
)
class MonitorAutoscaleSettingProfileCapacity:
    def __init__(
        self,
        *,
        default: jsii.Number,
        maximum: jsii.Number,
        minimum: jsii.Number,
    ) -> None:
        '''
        :param default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#default MonitorAutoscaleSetting#default}.
        :param maximum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#maximum MonitorAutoscaleSetting#maximum}.
        :param minimum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#minimum MonitorAutoscaleSetting#minimum}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a99e21a7e2fb7ca810ac0d4edfbfc2152a46e12e8fea753b610110e95a1858)
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument maximum", value=maximum, expected_type=type_hints["maximum"])
            check_type(argname="argument minimum", value=minimum, expected_type=type_hints["minimum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default": default,
            "maximum": maximum,
            "minimum": minimum,
        }

    @builtins.property
    def default(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#default MonitorAutoscaleSetting#default}.'''
        result = self._values.get("default")
        assert result is not None, "Required property 'default' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def maximum(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#maximum MonitorAutoscaleSetting#maximum}.'''
        result = self._values.get("maximum")
        assert result is not None, "Required property 'maximum' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def minimum(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#minimum MonitorAutoscaleSetting#minimum}.'''
        result = self._values.get("minimum")
        assert result is not None, "Required property 'minimum' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAutoscaleSettingProfileCapacity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAutoscaleSettingProfileCapacityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileCapacityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e15e4f793b5a0dee029a3704559eb578d5a96277b7922f522ca4335d551a77c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="defaultInput")
    def default_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumInput")
    def maximum_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumInput")
    def minimum_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumInput"))

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "default"))

    @default.setter
    def default(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4074a26340f56b25b2a22a4c5056498ddf8c5e9a88aa1535df2a4d67c4abcc82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximum")
    def maximum(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximum"))

    @maximum.setter
    def maximum(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e4cfac50b8771693e2e22eadc140ac63de68245d4d6cdf9f00119431556e96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimum")
    def minimum(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimum"))

    @minimum.setter
    def minimum(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3bccad7f3a5f1b59a74b6801380b1313d02ffe92f6e033b0210c1adbd03392a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorAutoscaleSettingProfileCapacity]:
        return typing.cast(typing.Optional[MonitorAutoscaleSettingProfileCapacity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAutoscaleSettingProfileCapacity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f8828348e594481dc9605e2a3402d054621dc4594a15832db6bc5c3d18f63c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileFixedDate",
    jsii_struct_bases=[],
    name_mapping={"end": "end", "start": "start", "timezone": "timezone"},
)
class MonitorAutoscaleSettingProfileFixedDate:
    def __init__(
        self,
        *,
        end: builtins.str,
        start: builtins.str,
        timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#end MonitorAutoscaleSetting#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#start MonitorAutoscaleSetting#start}.
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#timezone MonitorAutoscaleSetting#timezone}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46ca0496f35d4e01fd3f277958400d2648af69fbe89623f3eac04d949f5b08f3)
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end": end,
            "start": start,
        }
        if timezone is not None:
            self._values["timezone"] = timezone

    @builtins.property
    def end(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#end MonitorAutoscaleSetting#end}.'''
        result = self._values.get("end")
        assert result is not None, "Required property 'end' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#start MonitorAutoscaleSetting#start}.'''
        result = self._values.get("start")
        assert result is not None, "Required property 'start' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#timezone MonitorAutoscaleSetting#timezone}.'''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAutoscaleSettingProfileFixedDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAutoscaleSettingProfileFixedDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileFixedDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47dfd3eb329c77d28f634dac91a7e4404c1aae7b6efbda6445814fa53368ef77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTimezone")
    def reset_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimezone", []))

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "end"))

    @end.setter
    def end(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af5a9f5c0062e8930c0e7120cce35cb02b9a68fa85468ad715f5852469a43b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "start"))

    @start.setter
    def start(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e47781c9655ee9b935fecd89227b8131d44f6e6f2b5ec781879a45a464b6b24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17ca49a80230a8d1c3dee72dea1d6312d076274cedd933deb53367994e69db8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAutoscaleSettingProfileFixedDate]:
        return typing.cast(typing.Optional[MonitorAutoscaleSettingProfileFixedDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAutoscaleSettingProfileFixedDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db234def3350de20022235a1c38476466fd5619aa1b1c3b7ec070759d1ba297)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAutoscaleSettingProfileList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5240ceec3dd596fc0d566b7880203624d23ffdb15cf368b8d152a7563d3979aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorAutoscaleSettingProfileOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67841c686f3360913f44941458734bd699abbd82cabb8c6f630b6ab60d1cb16d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorAutoscaleSettingProfileOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56d1114faf78a08ff5462bc9cfd71b26dc6c6a806332ba3fd897db3ca8950bc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9a3d595197461f461605a0c476754625252a2e2d5033d844abef4057e1741eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f33e19de35fa1627360b95df19e75c29f0aad7c5f9a94b2eea7eb2b6ad762be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingProfile]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingProfile]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingProfile]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b3fc753e209ce9c1ded56367ae08e88e0e49585ae6e92b84645c022e7864ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAutoscaleSettingProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a901af2175f84c9fa2f5b8f67cc9faf631d0cbd7cb3cb4665c8aaa7823586121)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCapacity")
    def put_capacity(
        self,
        *,
        default: jsii.Number,
        maximum: jsii.Number,
        minimum: jsii.Number,
    ) -> None:
        '''
        :param default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#default MonitorAutoscaleSetting#default}.
        :param maximum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#maximum MonitorAutoscaleSetting#maximum}.
        :param minimum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#minimum MonitorAutoscaleSetting#minimum}.
        '''
        value = MonitorAutoscaleSettingProfileCapacity(
            default=default, maximum=maximum, minimum=minimum
        )

        return typing.cast(None, jsii.invoke(self, "putCapacity", [value]))

    @jsii.member(jsii_name="putFixedDate")
    def put_fixed_date(
        self,
        *,
        end: builtins.str,
        start: builtins.str,
        timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#end MonitorAutoscaleSetting#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#start MonitorAutoscaleSetting#start}.
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#timezone MonitorAutoscaleSetting#timezone}.
        '''
        value = MonitorAutoscaleSettingProfileFixedDate(
            end=end, start=start, timezone=timezone
        )

        return typing.cast(None, jsii.invoke(self, "putFixedDate", [value]))

    @jsii.member(jsii_name="putRecurrence")
    def put_recurrence(
        self,
        *,
        days: typing.Sequence[builtins.str],
        hours: typing.Sequence[jsii.Number],
        minutes: typing.Sequence[jsii.Number],
        timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#days MonitorAutoscaleSetting#days}.
        :param hours: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#hours MonitorAutoscaleSetting#hours}.
        :param minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#minutes MonitorAutoscaleSetting#minutes}.
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#timezone MonitorAutoscaleSetting#timezone}.
        '''
        value = MonitorAutoscaleSettingProfileRecurrence(
            days=days, hours=hours, minutes=minutes, timezone=timezone
        )

        return typing.cast(None, jsii.invoke(self, "putRecurrence", [value]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAutoscaleSettingProfileRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05b90bcbc3c4dbc88d6538af57987d3e8558f51cb55a17eb04289b02a349e0d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="resetFixedDate")
    def reset_fixed_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedDate", []))

    @jsii.member(jsii_name="resetRecurrence")
    def reset_recurrence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurrence", []))

    @jsii.member(jsii_name="resetRule")
    def reset_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRule", []))

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> MonitorAutoscaleSettingProfileCapacityOutputReference:
        return typing.cast(MonitorAutoscaleSettingProfileCapacityOutputReference, jsii.get(self, "capacity"))

    @builtins.property
    @jsii.member(jsii_name="fixedDate")
    def fixed_date(self) -> MonitorAutoscaleSettingProfileFixedDateOutputReference:
        return typing.cast(MonitorAutoscaleSettingProfileFixedDateOutputReference, jsii.get(self, "fixedDate"))

    @builtins.property
    @jsii.member(jsii_name="recurrence")
    def recurrence(self) -> "MonitorAutoscaleSettingProfileRecurrenceOutputReference":
        return typing.cast("MonitorAutoscaleSettingProfileRecurrenceOutputReference", jsii.get(self, "recurrence"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "MonitorAutoscaleSettingProfileRuleList":
        return typing.cast("MonitorAutoscaleSettingProfileRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="capacityInput")
    def capacity_input(self) -> typing.Optional[MonitorAutoscaleSettingProfileCapacity]:
        return typing.cast(typing.Optional[MonitorAutoscaleSettingProfileCapacity], jsii.get(self, "capacityInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedDateInput")
    def fixed_date_input(
        self,
    ) -> typing.Optional[MonitorAutoscaleSettingProfileFixedDate]:
        return typing.cast(typing.Optional[MonitorAutoscaleSettingProfileFixedDate], jsii.get(self, "fixedDateInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceInput")
    def recurrence_input(
        self,
    ) -> typing.Optional["MonitorAutoscaleSettingProfileRecurrence"]:
        return typing.cast(typing.Optional["MonitorAutoscaleSettingProfileRecurrence"], jsii.get(self, "recurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAutoscaleSettingProfileRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAutoscaleSettingProfileRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80b1abfec104f0aadbc103ae847e54e87b8e760a5f42c62ef3777a18845de3b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingProfile]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingProfile]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingProfile]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25062f4916f283d1baee6b756359b33264cc676efb1f5759b56edbac9865bee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileRecurrence",
    jsii_struct_bases=[],
    name_mapping={
        "days": "days",
        "hours": "hours",
        "minutes": "minutes",
        "timezone": "timezone",
    },
)
class MonitorAutoscaleSettingProfileRecurrence:
    def __init__(
        self,
        *,
        days: typing.Sequence[builtins.str],
        hours: typing.Sequence[jsii.Number],
        minutes: typing.Sequence[jsii.Number],
        timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#days MonitorAutoscaleSetting#days}.
        :param hours: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#hours MonitorAutoscaleSetting#hours}.
        :param minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#minutes MonitorAutoscaleSetting#minutes}.
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#timezone MonitorAutoscaleSetting#timezone}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a964007bdfbc0da528db358744eb522a80df346ee3edb51da6482e7e4f41f4f8)
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "days": days,
            "hours": hours,
            "minutes": minutes,
        }
        if timezone is not None:
            self._values["timezone"] = timezone

    @builtins.property
    def days(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#days MonitorAutoscaleSetting#days}.'''
        result = self._values.get("days")
        assert result is not None, "Required property 'days' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def hours(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#hours MonitorAutoscaleSetting#hours}.'''
        result = self._values.get("hours")
        assert result is not None, "Required property 'hours' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#minutes MonitorAutoscaleSetting#minutes}.'''
        result = self._values.get("minutes")
        assert result is not None, "Required property 'minutes' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#timezone MonitorAutoscaleSetting#timezone}.'''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAutoscaleSettingProfileRecurrence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAutoscaleSettingProfileRecurrenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileRecurrenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__838227319e37097287e95b043052bbc36dc479824013f272bb894929f91f4760)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTimezone")
    def reset_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimezone", []))

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "days"))

    @days.setter
    def days(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa1786c051f8f8988594c9f428d17dbff6d7ae5f1e05d5e106af8ff30b92564d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a856f1d8ff950e5dbf3474416e88f09e1283460dac90fd5fe8a260856f5e1b2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aeb432b846e8a3258e862f660cef9a5193005e4ff9e595a673000e857c1a4c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8616263dfeabf851d684e7d59f268aacd91ecb2eb049fff39a258ef8e61beeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAutoscaleSettingProfileRecurrence]:
        return typing.cast(typing.Optional[MonitorAutoscaleSettingProfileRecurrence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAutoscaleSettingProfileRecurrence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3664ed3c63743ea6845e130759cf74d989124386c15d0e282163a1a67583f97c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileRule",
    jsii_struct_bases=[],
    name_mapping={"metric_trigger": "metricTrigger", "scale_action": "scaleAction"},
)
class MonitorAutoscaleSettingProfileRule:
    def __init__(
        self,
        *,
        metric_trigger: typing.Union["MonitorAutoscaleSettingProfileRuleMetricTrigger", typing.Dict[builtins.str, typing.Any]],
        scale_action: typing.Union["MonitorAutoscaleSettingProfileRuleScaleAction", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param metric_trigger: metric_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#metric_trigger MonitorAutoscaleSetting#metric_trigger}
        :param scale_action: scale_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#scale_action MonitorAutoscaleSetting#scale_action}
        '''
        if isinstance(metric_trigger, dict):
            metric_trigger = MonitorAutoscaleSettingProfileRuleMetricTrigger(**metric_trigger)
        if isinstance(scale_action, dict):
            scale_action = MonitorAutoscaleSettingProfileRuleScaleAction(**scale_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c591b99d23ec1bb33779813eab54a9e14146b7765b76b5e22f76a0f7121f72c)
            check_type(argname="argument metric_trigger", value=metric_trigger, expected_type=type_hints["metric_trigger"])
            check_type(argname="argument scale_action", value=scale_action, expected_type=type_hints["scale_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_trigger": metric_trigger,
            "scale_action": scale_action,
        }

    @builtins.property
    def metric_trigger(self) -> "MonitorAutoscaleSettingProfileRuleMetricTrigger":
        '''metric_trigger block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#metric_trigger MonitorAutoscaleSetting#metric_trigger}
        '''
        result = self._values.get("metric_trigger")
        assert result is not None, "Required property 'metric_trigger' is missing"
        return typing.cast("MonitorAutoscaleSettingProfileRuleMetricTrigger", result)

    @builtins.property
    def scale_action(self) -> "MonitorAutoscaleSettingProfileRuleScaleAction":
        '''scale_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#scale_action MonitorAutoscaleSetting#scale_action}
        '''
        result = self._values.get("scale_action")
        assert result is not None, "Required property 'scale_action' is missing"
        return typing.cast("MonitorAutoscaleSettingProfileRuleScaleAction", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAutoscaleSettingProfileRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAutoscaleSettingProfileRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d6870723df644600236c8df85f78a20d6a7249d929220a302ae43f8f8720f30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorAutoscaleSettingProfileRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e642e0209e67fb2fee2b68d8a157e4a5aae54099fd140839773a7a265ca3f82)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorAutoscaleSettingProfileRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a52a8918c2f2e37eab589c30e94e1cf9cf768e87f65ce4713911406e7784bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8580e5c595032beafe2c8226e989e5e2c8935186b11576bd77a4ecf36a22b79f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa96dc02abee8ab3d997e7bd6441acb7d1c5dd7bd054cba066961850d12e83a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingProfileRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingProfileRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingProfileRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b2268afb79b27130cbf382b02a7a2421073b8714b3898a2b7e9cb37f3d515dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileRuleMetricTrigger",
    jsii_struct_bases=[],
    name_mapping={
        "metric_name": "metricName",
        "metric_resource_id": "metricResourceId",
        "operator": "operator",
        "statistic": "statistic",
        "threshold": "threshold",
        "time_aggregation": "timeAggregation",
        "time_grain": "timeGrain",
        "time_window": "timeWindow",
        "dimensions": "dimensions",
        "divide_by_instance_count": "divideByInstanceCount",
        "metric_namespace": "metricNamespace",
    },
)
class MonitorAutoscaleSettingProfileRuleMetricTrigger:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        metric_resource_id: builtins.str,
        operator: builtins.str,
        statistic: builtins.str,
        threshold: jsii.Number,
        time_aggregation: builtins.str,
        time_grain: builtins.str,
        time_window: builtins.str,
        dimensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        divide_by_instance_count: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metric_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#metric_name MonitorAutoscaleSetting#metric_name}.
        :param metric_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#metric_resource_id MonitorAutoscaleSetting#metric_resource_id}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#operator MonitorAutoscaleSetting#operator}.
        :param statistic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#statistic MonitorAutoscaleSetting#statistic}.
        :param threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#threshold MonitorAutoscaleSetting#threshold}.
        :param time_aggregation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#time_aggregation MonitorAutoscaleSetting#time_aggregation}.
        :param time_grain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#time_grain MonitorAutoscaleSetting#time_grain}.
        :param time_window: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#time_window MonitorAutoscaleSetting#time_window}.
        :param dimensions: dimensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#dimensions MonitorAutoscaleSetting#dimensions}
        :param divide_by_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#divide_by_instance_count MonitorAutoscaleSetting#divide_by_instance_count}.
        :param metric_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#metric_namespace MonitorAutoscaleSetting#metric_namespace}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b4a759ad7e6303a7f4bbb03db20592033bacf8f294b5997c245af26b5658ded)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metric_resource_id", value=metric_resource_id, expected_type=type_hints["metric_resource_id"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument time_aggregation", value=time_aggregation, expected_type=type_hints["time_aggregation"])
            check_type(argname="argument time_grain", value=time_grain, expected_type=type_hints["time_grain"])
            check_type(argname="argument time_window", value=time_window, expected_type=type_hints["time_window"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument divide_by_instance_count", value=divide_by_instance_count, expected_type=type_hints["divide_by_instance_count"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_name": metric_name,
            "metric_resource_id": metric_resource_id,
            "operator": operator,
            "statistic": statistic,
            "threshold": threshold,
            "time_aggregation": time_aggregation,
            "time_grain": time_grain,
            "time_window": time_window,
        }
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if divide_by_instance_count is not None:
            self._values["divide_by_instance_count"] = divide_by_instance_count
        if metric_namespace is not None:
            self._values["metric_namespace"] = metric_namespace

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#metric_name MonitorAutoscaleSetting#metric_name}.'''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#metric_resource_id MonitorAutoscaleSetting#metric_resource_id}.'''
        result = self._values.get("metric_resource_id")
        assert result is not None, "Required property 'metric_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#operator MonitorAutoscaleSetting#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def statistic(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#statistic MonitorAutoscaleSetting#statistic}.'''
        result = self._values.get("statistic")
        assert result is not None, "Required property 'statistic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#threshold MonitorAutoscaleSetting#threshold}.'''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def time_aggregation(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#time_aggregation MonitorAutoscaleSetting#time_aggregation}.'''
        result = self._values.get("time_aggregation")
        assert result is not None, "Required property 'time_aggregation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_grain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#time_grain MonitorAutoscaleSetting#time_grain}.'''
        result = self._values.get("time_grain")
        assert result is not None, "Required property 'time_grain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_window(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#time_window MonitorAutoscaleSetting#time_window}.'''
        result = self._values.get("time_window")
        assert result is not None, "Required property 'time_window' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions"]]]:
        '''dimensions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#dimensions MonitorAutoscaleSetting#dimensions}
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions"]]], result)

    @builtins.property
    def divide_by_instance_count(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#divide_by_instance_count MonitorAutoscaleSetting#divide_by_instance_count}.'''
        result = self._values.get("divide_by_instance_count")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metric_namespace(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#metric_namespace MonitorAutoscaleSetting#metric_namespace}.'''
        result = self._values.get("metric_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAutoscaleSettingProfileRuleMetricTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "operator": "operator", "values": "values"},
)
class MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions:
    def __init__(
        self,
        *,
        name: builtins.str,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#name MonitorAutoscaleSetting#name}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#operator MonitorAutoscaleSetting#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#values MonitorAutoscaleSetting#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77b58b4ee3c06b161be75d3f8d0f753a0f6343440b268b561c4dd055f4ce425f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#name MonitorAutoscaleSetting#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#operator MonitorAutoscaleSetting#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#values MonitorAutoscaleSetting#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAutoscaleSettingProfileRuleMetricTriggerDimensionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileRuleMetricTriggerDimensionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ad81d8ddaa7b477973741e346768198bbbf724c61193d3f119b4b3a69b6ffc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorAutoscaleSettingProfileRuleMetricTriggerDimensionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e809ed34552090baac35ebc8fcee842ad66ffc6962ca28ebc97255fb04d00d50)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorAutoscaleSettingProfileRuleMetricTriggerDimensionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ccdd195c49ded73dc4b8e99ef1e3005e7f63ac8bf765dbeeb38468d60590d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f447b7dd04a81564f1b0f430ef0f89a1445c96f24e816b505d533f7ba8ae7de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4493d5cc4942c97a39d78ec4821dfc677d8fe488785e18ba9d5475b42c15635a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__370c16c3e48a849d0bd61d500d28f87e2d6fac1f74abe0d4222177cfa3df4e5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAutoscaleSettingProfileRuleMetricTriggerDimensionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileRuleMetricTriggerDimensionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0f1784d5e57ca4d267ecb5b1630f3266c18ea218bafcb091852e24165472793)
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
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__386de52c730c08bb8eb603fe0973ae3e1b5c4c7b64457aafe188ddb1f9da3693)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55bdf55b9e0fa479f3354cbab8b41a9e62ebdf4e17d7e471e893aa6e5412c3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0c7af19b7b38bdfff908b017e61cfec99c8f9b97c835be3f203d79bd2d71e80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c94703c3a55a9ec857d7ec26ad5032addd1eb605337ce4edc3e31a1308a5f4f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAutoscaleSettingProfileRuleMetricTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileRuleMetricTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3eb68d99304039a7f3bf696b983247059338f8ed26d4596416c3b13cab8aeb40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDimensions")
    def put_dimensions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__609c7c792a092c8a3b91cf1af119fc3e5156eb319a531036c7ea384eaafb061e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDimensions", [value]))

    @jsii.member(jsii_name="resetDimensions")
    def reset_dimensions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimensions", []))

    @jsii.member(jsii_name="resetDivideByInstanceCount")
    def reset_divide_by_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDivideByInstanceCount", []))

    @jsii.member(jsii_name="resetMetricNamespace")
    def reset_metric_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricNamespace", []))

    @builtins.property
    @jsii.member(jsii_name="dimensions")
    def dimensions(
        self,
    ) -> MonitorAutoscaleSettingProfileRuleMetricTriggerDimensionsList:
        return typing.cast(MonitorAutoscaleSettingProfileRuleMetricTriggerDimensionsList, jsii.get(self, "dimensions"))

    @builtins.property
    @jsii.member(jsii_name="dimensionsInput")
    def dimensions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions]]], jsii.get(self, "dimensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="divideByInstanceCountInput")
    def divide_by_instance_count_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "divideByInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="metricNameInput")
    def metric_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNameInput"))

    @builtins.property
    @jsii.member(jsii_name="metricNamespaceInput")
    def metric_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="metricResourceIdInput")
    def metric_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="statisticInput")
    def statistic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statisticInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdInput")
    def threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeAggregationInput")
    def time_aggregation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeAggregationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeGrainInput")
    def time_grain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeGrainInput"))

    @builtins.property
    @jsii.member(jsii_name="timeWindowInput")
    def time_window_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="divideByInstanceCount")
    def divide_by_instance_count(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "divideByInstanceCount"))

    @divide_by_instance_count.setter
    def divide_by_instance_count(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed3d7b0b61e5e1f8ce3043ec94060e9ed873a529fc3406135e5897242d747285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "divideByInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb54361d8cb949000cfecabf6615cfc01e99d94ea8d30a670ff380a701a1d95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricNamespace")
    def metric_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricNamespace"))

    @metric_namespace.setter
    def metric_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c516f79b03655a4df5864c1dbcdf80e18f57380fab882c9c3d5aec940e5663af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricResourceId")
    def metric_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricResourceId"))

    @metric_resource_id.setter
    def metric_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4502f992ceafcf4377c7d30c4d22651b04379fe7ad64ee3dc6be797735cd5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec64cf8ce368161dcb8cfad6732bc8847ed558545db145105df56a5c18c1ffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statistic")
    def statistic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statistic"))

    @statistic.setter
    def statistic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0615a4fa318a8fde888b0db09593027fe42916ef4bf83d8a111640968005f3b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statistic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b7955ec6b687339e79f975e36bae71956d421ce547903bcfb480a7de5707574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeAggregation")
    def time_aggregation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeAggregation"))

    @time_aggregation.setter
    def time_aggregation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b09fe1d2c7a7c1adcc7e0dcefb5746c08c30e5d445b0c19f4a3df0dea3a7ed35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeAggregation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeGrain")
    def time_grain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeGrain"))

    @time_grain.setter
    def time_grain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85c185f9b38ecefd716bc8c5ace082c12c5f554ba86eabc04b131361a0ac5c4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeGrain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeWindow")
    def time_window(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeWindow"))

    @time_window.setter
    def time_window(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9f4680becb28b4114776b9b6c8fcd96562328a793c9d63d74317d031d3b8d0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeWindow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAutoscaleSettingProfileRuleMetricTrigger]:
        return typing.cast(typing.Optional[MonitorAutoscaleSettingProfileRuleMetricTrigger], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAutoscaleSettingProfileRuleMetricTrigger],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__affb6df986ee951633619990b161f5ecf166b0e84602bb8e1d12f07d694ccd8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAutoscaleSettingProfileRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de83e8a85de73aca12d83cc4d7dfaed523f2cd70dba35ad548bf482aaf736109)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMetricTrigger")
    def put_metric_trigger(
        self,
        *,
        metric_name: builtins.str,
        metric_resource_id: builtins.str,
        operator: builtins.str,
        statistic: builtins.str,
        threshold: jsii.Number,
        time_aggregation: builtins.str,
        time_grain: builtins.str,
        time_window: builtins.str,
        dimensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        divide_by_instance_count: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metric_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#metric_name MonitorAutoscaleSetting#metric_name}.
        :param metric_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#metric_resource_id MonitorAutoscaleSetting#metric_resource_id}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#operator MonitorAutoscaleSetting#operator}.
        :param statistic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#statistic MonitorAutoscaleSetting#statistic}.
        :param threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#threshold MonitorAutoscaleSetting#threshold}.
        :param time_aggregation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#time_aggregation MonitorAutoscaleSetting#time_aggregation}.
        :param time_grain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#time_grain MonitorAutoscaleSetting#time_grain}.
        :param time_window: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#time_window MonitorAutoscaleSetting#time_window}.
        :param dimensions: dimensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#dimensions MonitorAutoscaleSetting#dimensions}
        :param divide_by_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#divide_by_instance_count MonitorAutoscaleSetting#divide_by_instance_count}.
        :param metric_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#metric_namespace MonitorAutoscaleSetting#metric_namespace}.
        '''
        value = MonitorAutoscaleSettingProfileRuleMetricTrigger(
            metric_name=metric_name,
            metric_resource_id=metric_resource_id,
            operator=operator,
            statistic=statistic,
            threshold=threshold,
            time_aggregation=time_aggregation,
            time_grain=time_grain,
            time_window=time_window,
            dimensions=dimensions,
            divide_by_instance_count=divide_by_instance_count,
            metric_namespace=metric_namespace,
        )

        return typing.cast(None, jsii.invoke(self, "putMetricTrigger", [value]))

    @jsii.member(jsii_name="putScaleAction")
    def put_scale_action(
        self,
        *,
        cooldown: builtins.str,
        direction: builtins.str,
        type: builtins.str,
        value: jsii.Number,
    ) -> None:
        '''
        :param cooldown: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#cooldown MonitorAutoscaleSetting#cooldown}.
        :param direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#direction MonitorAutoscaleSetting#direction}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#type MonitorAutoscaleSetting#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#value MonitorAutoscaleSetting#value}.
        '''
        value_ = MonitorAutoscaleSettingProfileRuleScaleAction(
            cooldown=cooldown, direction=direction, type=type, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putScaleAction", [value_]))

    @builtins.property
    @jsii.member(jsii_name="metricTrigger")
    def metric_trigger(
        self,
    ) -> MonitorAutoscaleSettingProfileRuleMetricTriggerOutputReference:
        return typing.cast(MonitorAutoscaleSettingProfileRuleMetricTriggerOutputReference, jsii.get(self, "metricTrigger"))

    @builtins.property
    @jsii.member(jsii_name="scaleAction")
    def scale_action(
        self,
    ) -> "MonitorAutoscaleSettingProfileRuleScaleActionOutputReference":
        return typing.cast("MonitorAutoscaleSettingProfileRuleScaleActionOutputReference", jsii.get(self, "scaleAction"))

    @builtins.property
    @jsii.member(jsii_name="metricTriggerInput")
    def metric_trigger_input(
        self,
    ) -> typing.Optional[MonitorAutoscaleSettingProfileRuleMetricTrigger]:
        return typing.cast(typing.Optional[MonitorAutoscaleSettingProfileRuleMetricTrigger], jsii.get(self, "metricTriggerInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleActionInput")
    def scale_action_input(
        self,
    ) -> typing.Optional["MonitorAutoscaleSettingProfileRuleScaleAction"]:
        return typing.cast(typing.Optional["MonitorAutoscaleSettingProfileRuleScaleAction"], jsii.get(self, "scaleActionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingProfileRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingProfileRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingProfileRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a0b3c1c8dfb54d2b3545cac2d8867254d02abd39909ea6a0ae4e518a277be2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileRuleScaleAction",
    jsii_struct_bases=[],
    name_mapping={
        "cooldown": "cooldown",
        "direction": "direction",
        "type": "type",
        "value": "value",
    },
)
class MonitorAutoscaleSettingProfileRuleScaleAction:
    def __init__(
        self,
        *,
        cooldown: builtins.str,
        direction: builtins.str,
        type: builtins.str,
        value: jsii.Number,
    ) -> None:
        '''
        :param cooldown: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#cooldown MonitorAutoscaleSetting#cooldown}.
        :param direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#direction MonitorAutoscaleSetting#direction}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#type MonitorAutoscaleSetting#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#value MonitorAutoscaleSetting#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cac19478f9e74dacfdd15a92afac691e83fa8d341de04cda74fc8d8942d908f2)
            check_type(argname="argument cooldown", value=cooldown, expected_type=type_hints["cooldown"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cooldown": cooldown,
            "direction": direction,
            "type": type,
            "value": value,
        }

    @builtins.property
    def cooldown(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#cooldown MonitorAutoscaleSetting#cooldown}.'''
        result = self._values.get("cooldown")
        assert result is not None, "Required property 'cooldown' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def direction(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#direction MonitorAutoscaleSetting#direction}.'''
        result = self._values.get("direction")
        assert result is not None, "Required property 'direction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#type MonitorAutoscaleSetting#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#value MonitorAutoscaleSetting#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAutoscaleSettingProfileRuleScaleAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAutoscaleSettingProfileRuleScaleActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingProfileRuleScaleActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd012e0d7e5f864de3fadca7a29b0d52469248f059892e431a30cac319f43588)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="cooldownInput")
    def cooldown_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cooldownInput"))

    @builtins.property
    @jsii.member(jsii_name="directionInput")
    def direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directionInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="cooldown")
    def cooldown(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cooldown"))

    @cooldown.setter
    def cooldown(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3fdd354a26564874072646776a8c5e362f23c7adc9f0da9db7599803a6b2b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cooldown", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63aef7d4c6304ba2c9f866407d2e14d419cb1c768b836a144bd606a532b8a69c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "direction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690ef894ac96600f76ddf3a6ace39cd4c6c3970bc3c0d36445174ddcf8054267)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e330e03183001dd393f0969456af46384cac9c918dfab0fca18136108af9ab87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAutoscaleSettingProfileRuleScaleAction]:
        return typing.cast(typing.Optional[MonitorAutoscaleSettingProfileRuleScaleAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAutoscaleSettingProfileRuleScaleAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c71c4f9e1f08b550db50482c83fa9c27c951a5e785e26ccf0d91ddd85cfc4bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MonitorAutoscaleSettingTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#create MonitorAutoscaleSetting#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#delete MonitorAutoscaleSetting#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#read MonitorAutoscaleSetting#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#update MonitorAutoscaleSetting#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__633092864132ac9cfe176ced6e2f54ebc472883251086e8e278f7297603f7773)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#create MonitorAutoscaleSetting#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#delete MonitorAutoscaleSetting#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#read MonitorAutoscaleSetting#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_autoscale_setting#update MonitorAutoscaleSetting#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAutoscaleSettingTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAutoscaleSettingTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAutoscaleSetting.MonitorAutoscaleSettingTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8716b91a011e4dc995d8e45c318db5f558a63b368516cafa3f34d5848a418d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__866d38b7076ec1082b1b5ba7b44ba0874b80ca7bbb47660b8042d0fdf72c3f54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a1801da71c6ea21a063df9d0a9b15e4dc100c383da4825229233ae8e571b411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241d5a549aeccd56e0491b7bd546d8d1546a873695f2aa69c8de61a8d3427848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b50886682b6abf78f130b069421790796081afb765e989471243778c6c5706b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf769721ef3d2683ac7b57e53c86ace30a152954433f570d6fb0c7097481f7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MonitorAutoscaleSetting",
    "MonitorAutoscaleSettingConfig",
    "MonitorAutoscaleSettingNotification",
    "MonitorAutoscaleSettingNotificationEmail",
    "MonitorAutoscaleSettingNotificationEmailOutputReference",
    "MonitorAutoscaleSettingNotificationOutputReference",
    "MonitorAutoscaleSettingNotificationWebhook",
    "MonitorAutoscaleSettingNotificationWebhookList",
    "MonitorAutoscaleSettingNotificationWebhookOutputReference",
    "MonitorAutoscaleSettingPredictive",
    "MonitorAutoscaleSettingPredictiveOutputReference",
    "MonitorAutoscaleSettingProfile",
    "MonitorAutoscaleSettingProfileCapacity",
    "MonitorAutoscaleSettingProfileCapacityOutputReference",
    "MonitorAutoscaleSettingProfileFixedDate",
    "MonitorAutoscaleSettingProfileFixedDateOutputReference",
    "MonitorAutoscaleSettingProfileList",
    "MonitorAutoscaleSettingProfileOutputReference",
    "MonitorAutoscaleSettingProfileRecurrence",
    "MonitorAutoscaleSettingProfileRecurrenceOutputReference",
    "MonitorAutoscaleSettingProfileRule",
    "MonitorAutoscaleSettingProfileRuleList",
    "MonitorAutoscaleSettingProfileRuleMetricTrigger",
    "MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions",
    "MonitorAutoscaleSettingProfileRuleMetricTriggerDimensionsList",
    "MonitorAutoscaleSettingProfileRuleMetricTriggerDimensionsOutputReference",
    "MonitorAutoscaleSettingProfileRuleMetricTriggerOutputReference",
    "MonitorAutoscaleSettingProfileRuleOutputReference",
    "MonitorAutoscaleSettingProfileRuleScaleAction",
    "MonitorAutoscaleSettingProfileRuleScaleActionOutputReference",
    "MonitorAutoscaleSettingTimeouts",
    "MonitorAutoscaleSettingTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4cada1144558e56fb576fa1040ab6319ba3a3c45878bbd8e10fdcaf3de194c74(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    profile: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAutoscaleSettingProfile, typing.Dict[builtins.str, typing.Any]]]],
    resource_group_name: builtins.str,
    target_resource_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    notification: typing.Optional[typing.Union[MonitorAutoscaleSettingNotification, typing.Dict[builtins.str, typing.Any]]] = None,
    predictive: typing.Optional[typing.Union[MonitorAutoscaleSettingPredictive, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorAutoscaleSettingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8ba9d048938a97443edec8355ba5b6a08db743921f09d36808052ce21a92e9df(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f8449b88de799518113c522dfca37f629da470c3f20074bff615191e339176(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAutoscaleSettingProfile, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d56c27af2c5381ed869b1e548fe041fbfa887d38e616f0981cd48fbc243716e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b17d893e74a278fdc71617f56f673e8a0a3af35db4966366c931afa2df916c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ffef7bb1a348c6251260e4c8f169092a0764b23168682c82729af580327b1b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c97d935f959c874a5796c815e09d510edf62c2f52eee02d45b6b1eb189c53db0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e355bdf59272d33e23c4cc78f02836f36c4a8458ee272c562fa1b68680aac3a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc5ca1503f7a2407db12984723e5bfc00cb5942b0b6ed81ebce2033ee9182a0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bd0365c72d5d8c1ce83a3c53d4878062c0fbb383fecb7cc028f3fe452b6bc66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6f8f649513c00b098b7661fe7b0a268c9301fcae4f90777ae07a6dd3643675(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    profile: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAutoscaleSettingProfile, typing.Dict[builtins.str, typing.Any]]]],
    resource_group_name: builtins.str,
    target_resource_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    notification: typing.Optional[typing.Union[MonitorAutoscaleSettingNotification, typing.Dict[builtins.str, typing.Any]]] = None,
    predictive: typing.Optional[typing.Union[MonitorAutoscaleSettingPredictive, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorAutoscaleSettingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f29e1bf3ae76f88e2f0d989ffb6ca9127827a82569d254b7fbf938865297c8(
    *,
    email: typing.Optional[typing.Union[MonitorAutoscaleSettingNotificationEmail, typing.Dict[builtins.str, typing.Any]]] = None,
    webhook: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAutoscaleSettingNotificationWebhook, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d530e04ba0ea7dce527b0011bb44a3f818fd6138f351a569da3a593f7311ad71(
    *,
    custom_emails: typing.Optional[typing.Sequence[builtins.str]] = None,
    send_to_subscription_administrator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_to_subscription_co_administrator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e3e729081b59e77708e75c1f190f5b555a2b9990d81c17b3f7b1450d0ced32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13aff88deaed3da03c27c691d73cb2f0c053abd5575011c04d2aec84a7570aa5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcdd842650158dca19d684b8404729d221f5392da7f4b0225732e14e9973069d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7fc9c7c4c817c6295ab8923a05b380f4eef24a3beacffdba88641a80c70200(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4a599c80a492d30987c67cbabe77367563c40905907f53b105c4805358b903(
    value: typing.Optional[MonitorAutoscaleSettingNotificationEmail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611975ff4747917ce61e02fc27cb1bd46051b43a814ce989282af771525f1d55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d906d75eaa006434b5e73806896a51b2bd989952771832584188fbfc8045a9d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAutoscaleSettingNotificationWebhook, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0edf49d31192c6f0de45469af50190627c1253729901f4668cfb05258990b1(
    value: typing.Optional[MonitorAutoscaleSettingNotification],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd285622b27a1a14a64808fda0ad6f288f996003e332189d56514c8e912256a(
    *,
    service_uri: builtins.str,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a3f1f1acc48439e6c2394749a8b9a641c1ee6cdb63bd921993f2d71281a4e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb337218f90ec68c86ac5abe4edae23cf0e971ce83b3e35b0604d9537ee828f2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3126c7a6b466397e9b48e2ce29d327e20935796f47051d484f4ab5c929cfcc0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdee6b31f122518f7719b6493dcf6d058a822ef62b9565fc1a4ce3d848e5df0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf143c1a374b29373c547d597547106278e3dfa3a7abd35782c05cb12a131fa0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e948a22f395589e18828f60df3e6958ff2768e4391dd561157c8e3801fe0acd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingNotificationWebhook]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd9193960f4ed68448b56b09c6ef7821486507fde4703c8b8e933ee1e72e3e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714a02bd9d8686b00a0c2dbe6a14dbb9480f46fa62d6eaa43b94b3a45d06b6a7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93310abfe2272809dd5db064a742696a4746bf7943dd144b4fb79f0b7219e58c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69fbdd3784abb6689e8a4a0196ceb2a28d256e882e8595bbf6c47f9ffb33732(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingNotificationWebhook]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7068cc9f58a218b0d4885d7e18c0d7c21c86cd1235356d878e729e7661136c32(
    *,
    scale_mode: builtins.str,
    look_ahead_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bdf1b219aed0251146b134a0d4f6e5a743869e2811b845b71bce2179d6350e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5240c411b9f420519b4559049de7ba3d1b05a39f2f59be6b589b7098b3f7847e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b6775345c924c92e70897254d160dea0974d47f1d6d4731d3a35c9b6f3420d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a0e555f5e5f9bb486a5881a984f414bdcab6e266d976a508109fcc78e21a9a(
    value: typing.Optional[MonitorAutoscaleSettingPredictive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a57d1292707572659d398bae1d5da0d88d06cbb2beff833979e8326c12e5de1(
    *,
    capacity: typing.Union[MonitorAutoscaleSettingProfileCapacity, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    fixed_date: typing.Optional[typing.Union[MonitorAutoscaleSettingProfileFixedDate, typing.Dict[builtins.str, typing.Any]]] = None,
    recurrence: typing.Optional[typing.Union[MonitorAutoscaleSettingProfileRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAutoscaleSettingProfileRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a99e21a7e2fb7ca810ac0d4edfbfc2152a46e12e8fea753b610110e95a1858(
    *,
    default: jsii.Number,
    maximum: jsii.Number,
    minimum: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e15e4f793b5a0dee029a3704559eb578d5a96277b7922f522ca4335d551a77c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4074a26340f56b25b2a22a4c5056498ddf8c5e9a88aa1535df2a4d67c4abcc82(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e4cfac50b8771693e2e22eadc140ac63de68245d4d6cdf9f00119431556e96(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3bccad7f3a5f1b59a74b6801380b1313d02ffe92f6e033b0210c1adbd03392a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f8828348e594481dc9605e2a3402d054621dc4594a15832db6bc5c3d18f63c(
    value: typing.Optional[MonitorAutoscaleSettingProfileCapacity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ca0496f35d4e01fd3f277958400d2648af69fbe89623f3eac04d949f5b08f3(
    *,
    end: builtins.str,
    start: builtins.str,
    timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47dfd3eb329c77d28f634dac91a7e4404c1aae7b6efbda6445814fa53368ef77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af5a9f5c0062e8930c0e7120cce35cb02b9a68fa85468ad715f5852469a43b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e47781c9655ee9b935fecd89227b8131d44f6e6f2b5ec781879a45a464b6b24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ca49a80230a8d1c3dee72dea1d6312d076274cedd933deb53367994e69db8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db234def3350de20022235a1c38476466fd5619aa1b1c3b7ec070759d1ba297(
    value: typing.Optional[MonitorAutoscaleSettingProfileFixedDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5240ceec3dd596fc0d566b7880203624d23ffdb15cf368b8d152a7563d3979aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67841c686f3360913f44941458734bd699abbd82cabb8c6f630b6ab60d1cb16d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d1114faf78a08ff5462bc9cfd71b26dc6c6a806332ba3fd897db3ca8950bc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a3d595197461f461605a0c476754625252a2e2d5033d844abef4057e1741eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f33e19de35fa1627360b95df19e75c29f0aad7c5f9a94b2eea7eb2b6ad762be(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b3fc753e209ce9c1ded56367ae08e88e0e49585ae6e92b84645c022e7864ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingProfile]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a901af2175f84c9fa2f5b8f67cc9faf631d0cbd7cb3cb4665c8aaa7823586121(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05b90bcbc3c4dbc88d6538af57987d3e8558f51cb55a17eb04289b02a349e0d5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAutoscaleSettingProfileRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b1abfec104f0aadbc103ae847e54e87b8e760a5f42c62ef3777a18845de3b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25062f4916f283d1baee6b756359b33264cc676efb1f5759b56edbac9865bee0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingProfile]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a964007bdfbc0da528db358744eb522a80df346ee3edb51da6482e7e4f41f4f8(
    *,
    days: typing.Sequence[builtins.str],
    hours: typing.Sequence[jsii.Number],
    minutes: typing.Sequence[jsii.Number],
    timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838227319e37097287e95b043052bbc36dc479824013f272bb894929f91f4760(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1786c051f8f8988594c9f428d17dbff6d7ae5f1e05d5e106af8ff30b92564d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a856f1d8ff950e5dbf3474416e88f09e1283460dac90fd5fe8a260856f5e1b2a(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aeb432b846e8a3258e862f660cef9a5193005e4ff9e595a673000e857c1a4c0(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8616263dfeabf851d684e7d59f268aacd91ecb2eb049fff39a258ef8e61beeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3664ed3c63743ea6845e130759cf74d989124386c15d0e282163a1a67583f97c(
    value: typing.Optional[MonitorAutoscaleSettingProfileRecurrence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c591b99d23ec1bb33779813eab54a9e14146b7765b76b5e22f76a0f7121f72c(
    *,
    metric_trigger: typing.Union[MonitorAutoscaleSettingProfileRuleMetricTrigger, typing.Dict[builtins.str, typing.Any]],
    scale_action: typing.Union[MonitorAutoscaleSettingProfileRuleScaleAction, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6870723df644600236c8df85f78a20d6a7249d929220a302ae43f8f8720f30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e642e0209e67fb2fee2b68d8a157e4a5aae54099fd140839773a7a265ca3f82(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a52a8918c2f2e37eab589c30e94e1cf9cf768e87f65ce4713911406e7784bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8580e5c595032beafe2c8226e989e5e2c8935186b11576bd77a4ecf36a22b79f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa96dc02abee8ab3d997e7bd6441acb7d1c5dd7bd054cba066961850d12e83a5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b2268afb79b27130cbf382b02a7a2421073b8714b3898a2b7e9cb37f3d515dc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingProfileRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b4a759ad7e6303a7f4bbb03db20592033bacf8f294b5997c245af26b5658ded(
    *,
    metric_name: builtins.str,
    metric_resource_id: builtins.str,
    operator: builtins.str,
    statistic: builtins.str,
    threshold: jsii.Number,
    time_aggregation: builtins.str,
    time_grain: builtins.str,
    time_window: builtins.str,
    dimensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    divide_by_instance_count: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metric_namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b58b4ee3c06b161be75d3f8d0f753a0f6343440b268b561c4dd055f4ce425f(
    *,
    name: builtins.str,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad81d8ddaa7b477973741e346768198bbbf724c61193d3f119b4b3a69b6ffc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e809ed34552090baac35ebc8fcee842ad66ffc6962ca28ebc97255fb04d00d50(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ccdd195c49ded73dc4b8e99ef1e3005e7f63ac8bf765dbeeb38468d60590d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f447b7dd04a81564f1b0f430ef0f89a1445c96f24e816b505d533f7ba8ae7de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4493d5cc4942c97a39d78ec4821dfc677d8fe488785e18ba9d5475b42c15635a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370c16c3e48a849d0bd61d500d28f87e2d6fac1f74abe0d4222177cfa3df4e5b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f1784d5e57ca4d267ecb5b1630f3266c18ea218bafcb091852e24165472793(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__386de52c730c08bb8eb603fe0973ae3e1b5c4c7b64457aafe188ddb1f9da3693(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55bdf55b9e0fa479f3354cbab8b41a9e62ebdf4e17d7e471e893aa6e5412c3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c7af19b7b38bdfff908b017e61cfec99c8f9b97c835be3f203d79bd2d71e80(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c94703c3a55a9ec857d7ec26ad5032addd1eb605337ce4edc3e31a1308a5f4f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb68d99304039a7f3bf696b983247059338f8ed26d4596416c3b13cab8aeb40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__609c7c792a092c8a3b91cf1af119fc3e5156eb319a531036c7ea384eaafb061e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAutoscaleSettingProfileRuleMetricTriggerDimensions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3d7b0b61e5e1f8ce3043ec94060e9ed873a529fc3406135e5897242d747285(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb54361d8cb949000cfecabf6615cfc01e99d94ea8d30a670ff380a701a1d95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c516f79b03655a4df5864c1dbcdf80e18f57380fab882c9c3d5aec940e5663af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4502f992ceafcf4377c7d30c4d22651b04379fe7ad64ee3dc6be797735cd5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec64cf8ce368161dcb8cfad6732bc8847ed558545db145105df56a5c18c1ffb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0615a4fa318a8fde888b0db09593027fe42916ef4bf83d8a111640968005f3b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b7955ec6b687339e79f975e36bae71956d421ce547903bcfb480a7de5707574(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b09fe1d2c7a7c1adcc7e0dcefb5746c08c30e5d445b0c19f4a3df0dea3a7ed35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c185f9b38ecefd716bc8c5ace082c12c5f554ba86eabc04b131361a0ac5c4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f4680becb28b4114776b9b6c8fcd96562328a793c9d63d74317d031d3b8d0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__affb6df986ee951633619990b161f5ecf166b0e84602bb8e1d12f07d694ccd8a(
    value: typing.Optional[MonitorAutoscaleSettingProfileRuleMetricTrigger],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de83e8a85de73aca12d83cc4d7dfaed523f2cd70dba35ad548bf482aaf736109(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0b3c1c8dfb54d2b3545cac2d8867254d02abd39909ea6a0ae4e518a277be2f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingProfileRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac19478f9e74dacfdd15a92afac691e83fa8d341de04cda74fc8d8942d908f2(
    *,
    cooldown: builtins.str,
    direction: builtins.str,
    type: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd012e0d7e5f864de3fadca7a29b0d52469248f059892e431a30cac319f43588(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3fdd354a26564874072646776a8c5e362f23c7adc9f0da9db7599803a6b2b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63aef7d4c6304ba2c9f866407d2e14d419cb1c768b836a144bd606a532b8a69c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690ef894ac96600f76ddf3a6ace39cd4c6c3970bc3c0d36445174ddcf8054267(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e330e03183001dd393f0969456af46384cac9c918dfab0fca18136108af9ab87(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c71c4f9e1f08b550db50482c83fa9c27c951a5e785e26ccf0d91ddd85cfc4bb4(
    value: typing.Optional[MonitorAutoscaleSettingProfileRuleScaleAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633092864132ac9cfe176ced6e2f54ebc472883251086e8e278f7297603f7773(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8716b91a011e4dc995d8e45c318db5f558a63b368516cafa3f34d5848a418d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866d38b7076ec1082b1b5ba7b44ba0874b80ca7bbb47660b8042d0fdf72c3f54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1801da71c6ea21a063df9d0a9b15e4dc100c383da4825229233ae8e571b411(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241d5a549aeccd56e0491b7bd546d8d1546a873695f2aa69c8de61a8d3427848(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b50886682b6abf78f130b069421790796081afb765e989471243778c6c5706b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf769721ef3d2683ac7b57e53c86ace30a152954433f570d6fb0c7097481f7d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAutoscaleSettingTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `data_opentelekomcloud_hss_intrusion_events_v5`

Refer to the Terraform Registry for docs: [`data_opentelekomcloud_hss_intrusion_events_v5`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5).
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


class DataOpentelekomcloudHssIntrusionEventsV5(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5 opentelekomcloud_hss_intrusion_events_v5}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        category: builtins.str,
        begin_time: typing.Optional[builtins.str] = None,
        container_name: typing.Optional[builtins.str] = None,
        days: typing.Optional[jsii.Number] = None,
        end_time: typing.Optional[builtins.str] = None,
        enterprise_project_id: typing.Optional[builtins.str] = None,
        event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        handle_status: typing.Optional[builtins.str] = None,
        host_id: typing.Optional[builtins.str] = None,
        host_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        private_ip: typing.Optional[builtins.str] = None,
        severity: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5 opentelekomcloud_hss_intrusion_events_v5} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param category: Event category. Its value can be: host (host security event) or container (container security event). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#category DataOpentelekomcloudHssIntrusionEventsV5#category}
        :param begin_time: Customized start time of a segment. The timestamp is accurate to seconds. The begin_time should be no more than two days earlier than the end_time. This parameter is mutually exclusive with the queried duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#begin_time DataOpentelekomcloudHssIntrusionEventsV5#begin_time}
        :param container_name: Container instance name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#container_name DataOpentelekomcloudHssIntrusionEventsV5#container_name}
        :param days: Number of days to be queried. This parameter is mutually exclusive with begin_time and end_time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#days DataOpentelekomcloudHssIntrusionEventsV5#days}
        :param end_time: Customized end time of a segment. The timestamp is accurate to seconds. The begin_time should be no more than two days earlier than the end_time. This parameter is mutually exclusive with the queried duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#end_time DataOpentelekomcloudHssIntrusionEventsV5#end_time}
        :param enterprise_project_id: Enterprise project ID. The value 0 indicates the default enterprise project. To query all enterprise projects, set this parameter to all_granted_eps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#enterprise_project_id DataOpentelekomcloudHssIntrusionEventsV5#enterprise_project_id}
        :param event_types: Intrusion types. Possible values include: 1001: Malware 1010: Rootkit 1011: Ransomware 1015: Web shell 1017: Reverse shell 2001: Common vulnerability exploit 3002: File privilege escalation 3003: Process privilege escalation 3004: Important file change 3005: File/Directory change 3007: Abnormal process behavior 3015: High-risk command execution 3018: Abnormal shell 3027: Suspicious crontab tasks 4002: Brute-force attack 4004: Abnormal login 4006: Invalid system account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#event_types DataOpentelekomcloudHssIntrusionEventsV5#event_types}
        :param handle_status: Status. Possible values: unhandled, handled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#handle_status DataOpentelekomcloudHssIntrusionEventsV5#handle_status}
        :param host_id: Host ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#host_id DataOpentelekomcloudHssIntrusionEventsV5#host_id}
        :param host_name: Server name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#host_name DataOpentelekomcloudHssIntrusionEventsV5#host_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#id DataOpentelekomcloudHssIntrusionEventsV5#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param private_ip: Server IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#private_ip DataOpentelekomcloudHssIntrusionEventsV5#private_ip}
        :param severity: Threat level. Possible values: Security, Low, Medium, High, Critical. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#severity DataOpentelekomcloudHssIntrusionEventsV5#severity}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec037a6643da042fe70b8069d69295d545d2630b55d6ef133122931ad2f64cc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpentelekomcloudHssIntrusionEventsV5Config(
            category=category,
            begin_time=begin_time,
            container_name=container_name,
            days=days,
            end_time=end_time,
            enterprise_project_id=enterprise_project_id,
            event_types=event_types,
            handle_status=handle_status,
            host_id=host_id,
            host_name=host_name,
            id=id,
            private_ip=private_ip,
            severity=severity,
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
        '''Generates CDKTF code for importing a DataOpentelekomcloudHssIntrusionEventsV5 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpentelekomcloudHssIntrusionEventsV5 to import.
        :param import_from_id: The id of the existing DataOpentelekomcloudHssIntrusionEventsV5 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpentelekomcloudHssIntrusionEventsV5 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dfab62fcd4d48a74946b28b16b0b488ac19147b35e3155f356b9befad24cd59)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetBeginTime")
    def reset_begin_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBeginTime", []))

    @jsii.member(jsii_name="resetContainerName")
    def reset_container_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerName", []))

    @jsii.member(jsii_name="resetDays")
    def reset_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDays", []))

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetEnterpriseProjectId")
    def reset_enterprise_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnterpriseProjectId", []))

    @jsii.member(jsii_name="resetEventTypes")
    def reset_event_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventTypes", []))

    @jsii.member(jsii_name="resetHandleStatus")
    def reset_handle_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHandleStatus", []))

    @jsii.member(jsii_name="resetHostId")
    def reset_host_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostId", []))

    @jsii.member(jsii_name="resetHostName")
    def reset_host_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPrivateIp")
    def reset_private_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIp", []))

    @jsii.member(jsii_name="resetSeverity")
    def reset_severity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverity", []))

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
    @jsii.member(jsii_name="events")
    def events(self) -> "DataOpentelekomcloudHssIntrusionEventsV5EventsList":
        return typing.cast("DataOpentelekomcloudHssIntrusionEventsV5EventsList", jsii.get(self, "events"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="beginTimeInput")
    def begin_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "beginTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="categoryInput")
    def category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "categoryInput"))

    @builtins.property
    @jsii.member(jsii_name="containerNameInput")
    def container_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="enterpriseProjectIdInput")
    def enterprise_project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enterpriseProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="eventTypesInput")
    def event_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "eventTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="handleStatusInput")
    def handle_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "handleStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="hostIdInput")
    def host_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostIdInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpInput")
    def private_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="beginTime")
    def begin_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "beginTime"))

    @begin_time.setter
    def begin_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2267450b9ec54ecf5e33716b77f88614a1d0a9fbd9091c7ce89bbe1f9469ba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "beginTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @category.setter
    def category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__065ce650bb4b0258c4d1f156d976006b8ad4928c1cf22cb514e36c2dd87a4613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "category", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerName")
    def container_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerName"))

    @container_name.setter
    def container_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4f6d2d20f1b0d5bad913a1dd362fdedf30640ef5ada357d34d13d06c8cc8ccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "days"))

    @days.setter
    def days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee20c71068fedbdfad0e0950441df2a2d487a96abe559262b3b56bbc90e7502c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__427fd02d02e2fb6a8e8b32a7623ed041f0bf1f3b0da82479c2974c05b57760be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enterpriseProjectId")
    def enterprise_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enterpriseProjectId"))

    @enterprise_project_id.setter
    def enterprise_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab0b9b989fc38161d6b59207540c295eb09dcce09d0eca7fee716956e8aa4a3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enterpriseProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventTypes")
    def event_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "eventTypes"))

    @event_types.setter
    def event_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b2b615f3ed2fe8ad2cd0c73f70056736c0ad84f992d15a3e321129913c0793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="handleStatus")
    def handle_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "handleStatus"))

    @handle_status.setter
    def handle_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbf182bbb5a7118a11775fc4badc52ea3bd9a6f50791a975ae488a71bb29e4a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "handleStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostId")
    def host_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostId"))

    @host_id.setter
    def host_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a85b7d4b1d7b6fb3dc88059a2994f4dcb7d903d216b428b721c43c9c0495631e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8424f3a372f28762003ec8093c2622e35e3b43b71e34817527a17d36d190d23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eba90ce5b174ecfd7910486148d9fc2dd4fdd549fe115f685062b88ae69fb327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @private_ip.setter
    def private_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1342816a9326a9f4cad167f16d513088d55bc920a8b12c7d0f2b93890608e5d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__675dc4d63c5d0f7085c816a6d56c3fc3900085e382c4772500782f71188d49eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "category": "category",
        "begin_time": "beginTime",
        "container_name": "containerName",
        "days": "days",
        "end_time": "endTime",
        "enterprise_project_id": "enterpriseProjectId",
        "event_types": "eventTypes",
        "handle_status": "handleStatus",
        "host_id": "hostId",
        "host_name": "hostName",
        "id": "id",
        "private_ip": "privateIp",
        "severity": "severity",
    },
)
class DataOpentelekomcloudHssIntrusionEventsV5Config(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        category: builtins.str,
        begin_time: typing.Optional[builtins.str] = None,
        container_name: typing.Optional[builtins.str] = None,
        days: typing.Optional[jsii.Number] = None,
        end_time: typing.Optional[builtins.str] = None,
        enterprise_project_id: typing.Optional[builtins.str] = None,
        event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        handle_status: typing.Optional[builtins.str] = None,
        host_id: typing.Optional[builtins.str] = None,
        host_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        private_ip: typing.Optional[builtins.str] = None,
        severity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param category: Event category. Its value can be: host (host security event) or container (container security event). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#category DataOpentelekomcloudHssIntrusionEventsV5#category}
        :param begin_time: Customized start time of a segment. The timestamp is accurate to seconds. The begin_time should be no more than two days earlier than the end_time. This parameter is mutually exclusive with the queried duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#begin_time DataOpentelekomcloudHssIntrusionEventsV5#begin_time}
        :param container_name: Container instance name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#container_name DataOpentelekomcloudHssIntrusionEventsV5#container_name}
        :param days: Number of days to be queried. This parameter is mutually exclusive with begin_time and end_time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#days DataOpentelekomcloudHssIntrusionEventsV5#days}
        :param end_time: Customized end time of a segment. The timestamp is accurate to seconds. The begin_time should be no more than two days earlier than the end_time. This parameter is mutually exclusive with the queried duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#end_time DataOpentelekomcloudHssIntrusionEventsV5#end_time}
        :param enterprise_project_id: Enterprise project ID. The value 0 indicates the default enterprise project. To query all enterprise projects, set this parameter to all_granted_eps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#enterprise_project_id DataOpentelekomcloudHssIntrusionEventsV5#enterprise_project_id}
        :param event_types: Intrusion types. Possible values include: 1001: Malware 1010: Rootkit 1011: Ransomware 1015: Web shell 1017: Reverse shell 2001: Common vulnerability exploit 3002: File privilege escalation 3003: Process privilege escalation 3004: Important file change 3005: File/Directory change 3007: Abnormal process behavior 3015: High-risk command execution 3018: Abnormal shell 3027: Suspicious crontab tasks 4002: Brute-force attack 4004: Abnormal login 4006: Invalid system account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#event_types DataOpentelekomcloudHssIntrusionEventsV5#event_types}
        :param handle_status: Status. Possible values: unhandled, handled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#handle_status DataOpentelekomcloudHssIntrusionEventsV5#handle_status}
        :param host_id: Host ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#host_id DataOpentelekomcloudHssIntrusionEventsV5#host_id}
        :param host_name: Server name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#host_name DataOpentelekomcloudHssIntrusionEventsV5#host_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#id DataOpentelekomcloudHssIntrusionEventsV5#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param private_ip: Server IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#private_ip DataOpentelekomcloudHssIntrusionEventsV5#private_ip}
        :param severity: Threat level. Possible values: Security, Low, Medium, High, Critical. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#severity DataOpentelekomcloudHssIntrusionEventsV5#severity}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__194804d25d8b8cffa92733fe86f29adfdfb7253683ae88d4dbca58d8ab963877)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument begin_time", value=begin_time, expected_type=type_hints["begin_time"])
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument enterprise_project_id", value=enterprise_project_id, expected_type=type_hints["enterprise_project_id"])
            check_type(argname="argument event_types", value=event_types, expected_type=type_hints["event_types"])
            check_type(argname="argument handle_status", value=handle_status, expected_type=type_hints["handle_status"])
            check_type(argname="argument host_id", value=host_id, expected_type=type_hints["host_id"])
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument private_ip", value=private_ip, expected_type=type_hints["private_ip"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "category": category,
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
        if begin_time is not None:
            self._values["begin_time"] = begin_time
        if container_name is not None:
            self._values["container_name"] = container_name
        if days is not None:
            self._values["days"] = days
        if end_time is not None:
            self._values["end_time"] = end_time
        if enterprise_project_id is not None:
            self._values["enterprise_project_id"] = enterprise_project_id
        if event_types is not None:
            self._values["event_types"] = event_types
        if handle_status is not None:
            self._values["handle_status"] = handle_status
        if host_id is not None:
            self._values["host_id"] = host_id
        if host_name is not None:
            self._values["host_name"] = host_name
        if id is not None:
            self._values["id"] = id
        if private_ip is not None:
            self._values["private_ip"] = private_ip
        if severity is not None:
            self._values["severity"] = severity

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
    def category(self) -> builtins.str:
        '''Event category. Its value can be: host (host security event) or container (container security event).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#category DataOpentelekomcloudHssIntrusionEventsV5#category}
        '''
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def begin_time(self) -> typing.Optional[builtins.str]:
        '''Customized start time of a segment.

        The timestamp is accurate to seconds. The begin_time should be no more than two days earlier than the end_time. This parameter is mutually exclusive with the queried duration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#begin_time DataOpentelekomcloudHssIntrusionEventsV5#begin_time}
        '''
        result = self._values.get("begin_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_name(self) -> typing.Optional[builtins.str]:
        '''Container instance name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#container_name DataOpentelekomcloudHssIntrusionEventsV5#container_name}
        '''
        result = self._values.get("container_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def days(self) -> typing.Optional[jsii.Number]:
        '''Number of days to be queried. This parameter is mutually exclusive with begin_time and end_time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#days DataOpentelekomcloudHssIntrusionEventsV5#days}
        '''
        result = self._values.get("days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''Customized end time of a segment.

        The timestamp is accurate to seconds. The begin_time should be no more than two days earlier than the end_time. This parameter is mutually exclusive with the queried duration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#end_time DataOpentelekomcloudHssIntrusionEventsV5#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enterprise_project_id(self) -> typing.Optional[builtins.str]:
        '''Enterprise project ID.

        The value 0 indicates the default enterprise project. To query all enterprise projects, set this parameter to all_granted_eps.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#enterprise_project_id DataOpentelekomcloudHssIntrusionEventsV5#enterprise_project_id}
        '''
        result = self._values.get("enterprise_project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Intrusion types.

        Possible values include:
        1001: Malware
        1010: Rootkit
        1011: Ransomware
        1015: Web shell
        1017: Reverse shell
        2001: Common vulnerability exploit
        3002: File privilege escalation
        3003: Process privilege escalation
        3004: Important file change
        3005: File/Directory change
        3007: Abnormal process behavior
        3015: High-risk command execution
        3018: Abnormal shell
        3027: Suspicious crontab tasks
        4002: Brute-force attack
        4004: Abnormal login
        4006: Invalid system account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#event_types DataOpentelekomcloudHssIntrusionEventsV5#event_types}
        '''
        result = self._values.get("event_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def handle_status(self) -> typing.Optional[builtins.str]:
        '''Status. Possible values: unhandled, handled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#handle_status DataOpentelekomcloudHssIntrusionEventsV5#handle_status}
        '''
        result = self._values.get("handle_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_id(self) -> typing.Optional[builtins.str]:
        '''Host ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#host_id DataOpentelekomcloudHssIntrusionEventsV5#host_id}
        '''
        result = self._values.get("host_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_name(self) -> typing.Optional[builtins.str]:
        '''Server name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#host_name DataOpentelekomcloudHssIntrusionEventsV5#host_name}
        '''
        result = self._values.get("host_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#id DataOpentelekomcloudHssIntrusionEventsV5#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip(self) -> typing.Optional[builtins.str]:
        '''Server IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#private_ip DataOpentelekomcloudHssIntrusionEventsV5#private_ip}
        '''
        result = self._values.get("private_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def severity(self) -> typing.Optional[builtins.str]:
        '''Threat level. Possible values: Security, Low, Medium, High, Critical.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/hss_intrusion_events_v5#severity DataOpentelekomcloudHssIntrusionEventsV5#severity}
        '''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudHssIntrusionEventsV5Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5Events",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudHssIntrusionEventsV5Events:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudHssIntrusionEventsV5Events(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c099f4e336d85ab4d9400360d1944776f34b42e205df2379e35cf5b8eb20188c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b3073678d4009b1d6c16a83ae74b35937b54ab82af8f9a9da7ec87f9b5e814a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d40fb4e9482f7c9352a15545de11a2e8bb008bc77aecd2252bb49ac1309061)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b90f0d0839c2c44e2df801daddcf5ded7053e8e18555b4ffaede1520c4eaef90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d54876e928c9231c7f665422439f277dfbd2d4ce0bd3920b12820cf6897f5083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__070c16e8051612bbe49c02bd55563a85dee5207aeb1a85148492a83927092f6c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="fdCount")
    def fd_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fdCount"))

    @builtins.property
    @jsii.member(jsii_name="fdInfo")
    def fd_info(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fdInfo"))

    @builtins.property
    @jsii.member(jsii_name="fileAction")
    def file_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileAction"))

    @builtins.property
    @jsii.member(jsii_name="fileAlias")
    def file_alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileAlias"))

    @builtins.property
    @jsii.member(jsii_name="fileAtime")
    def file_atime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileAtime"))

    @builtins.property
    @jsii.member(jsii_name="fileAttr")
    def file_attr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileAttr"))

    @builtins.property
    @jsii.member(jsii_name="fileChangeAttr")
    def file_change_attr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileChangeAttr"))

    @builtins.property
    @jsii.member(jsii_name="fileContent")
    def file_content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileContent"))

    @builtins.property
    @jsii.member(jsii_name="fileCtime")
    def file_ctime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileCtime"))

    @builtins.property
    @jsii.member(jsii_name="fileDesc")
    def file_desc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileDesc"))

    @builtins.property
    @jsii.member(jsii_name="fileHash")
    def file_hash(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileHash"))

    @builtins.property
    @jsii.member(jsii_name="fileKeyWord")
    def file_key_word(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileKeyWord"))

    @builtins.property
    @jsii.member(jsii_name="fileMd5")
    def file_md5(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileMd5"))

    @builtins.property
    @jsii.member(jsii_name="fileMtime")
    def file_mtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileMtime"))

    @builtins.property
    @jsii.member(jsii_name="fileNewPath")
    def file_new_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileNewPath"))

    @builtins.property
    @jsii.member(jsii_name="fileOperation")
    def file_operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileOperation"))

    @builtins.property
    @jsii.member(jsii_name="filePath")
    def file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filePath"))

    @builtins.property
    @jsii.member(jsii_name="fileSha256")
    def file_sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileSha256"))

    @builtins.property
    @jsii.member(jsii_name="fileSize")
    def file_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fileSize"))

    @builtins.property
    @jsii.member(jsii_name="fileType")
    def file_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileType"))

    @builtins.property
    @jsii.member(jsii_name="isDir")
    def is_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isDir"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStruct]:
        return typing.cast(typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74ec1372630fe23049e8a80ef7f4a873b1b016206b1d7b56d525bb6ff8ee1a9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudHssIntrusionEventsV5EventsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5EventsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__356d912d909c1b0fc16e9f103c539c5c291e33ca44f18cc95a0fd06280604422)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudHssIntrusionEventsV5EventsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e8f21a9c69efd9d0cd4ea84fa3b6351c5bb28f85f68621ab8822e89531e3d33)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudHssIntrusionEventsV5EventsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__822dbe9d35cccab6af0248eeee138492be6c535c85871619334d42676070f531)
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
            type_hints = typing.get_type_hints(_typecheckingstub__967df065b768bd8ef4d57ebdd26c6ca7e0140078924604877c3248fbc4c90847)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b30cc2a636d3cf24072a91b5ee208d562af24c6bbfb19d0167c723cd11101fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26b5f0a5159748b141ad2fff7f545223e811d474b6865a4069addaa7669afd9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dc0608d3543bca4af20ecc6eef0d769e11e6699633358505f25f734d18c14c8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__278d4a08059abf717a08b3a54fd2ccea29993d31be28026e6d89fdaeced3e7a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de8047158efba7bc94d5b38c2e29c9d860d49a9a4ea4704699b78fb4e01a982e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cce09e55701caa0794a35a3676d8e428273be569b35ba3a0e7b769ad3acba12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66b7e6e7a4be151e65721357d98dc348570f215a548ea5b7d1877b6e85b90cb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="agentId")
    def agent_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentId"))

    @builtins.property
    @jsii.member(jsii_name="fileAttr")
    def file_attr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileAttr"))

    @builtins.property
    @jsii.member(jsii_name="fileHash")
    def file_hash(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileHash"))

    @builtins.property
    @jsii.member(jsii_name="filePath")
    def file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filePath"))

    @builtins.property
    @jsii.member(jsii_name="hash")
    def hash(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hash"))

    @builtins.property
    @jsii.member(jsii_name="isParent")
    def is_parent(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isParent"))

    @builtins.property
    @jsii.member(jsii_name="keyword")
    def keyword(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyword"))

    @builtins.property
    @jsii.member(jsii_name="loginIp")
    def login_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginIp"))

    @builtins.property
    @jsii.member(jsii_name="loginUserName")
    def login_user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginUserName"))

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @builtins.property
    @jsii.member(jsii_name="processPid")
    def process_pid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "processPid"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStruct]:
        return typing.cast(typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bb2a3dac7330b93543ee728cc97b35b5aed3d6a63ee88742c87fd6bacd2aaf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudHssIntrusionEventsV5EventsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5EventsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3aeeb79f0e0f36e889f9074b765263d231d319739a6a753c802e8d295c04ef76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="agentStatus")
    def agent_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentStatus"))

    @builtins.property
    @jsii.member(jsii_name="assetValue")
    def asset_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assetValue"))

    @builtins.property
    @jsii.member(jsii_name="attackPhase")
    def attack_phase(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attackPhase"))

    @builtins.property
    @jsii.member(jsii_name="attackTag")
    def attack_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attackTag"))

    @builtins.property
    @jsii.member(jsii_name="containerName")
    def container_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerName"))

    @builtins.property
    @jsii.member(jsii_name="eventClassId")
    def event_class_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventClassId"))

    @builtins.property
    @jsii.member(jsii_name="eventDetails")
    def event_details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventDetails"))

    @builtins.property
    @jsii.member(jsii_name="eventName")
    def event_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventName"))

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "eventType"))

    @builtins.property
    @jsii.member(jsii_name="fileInfoList")
    def file_info_list(
        self,
    ) -> DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStructList:
        return typing.cast(DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStructList, jsii.get(self, "fileInfoList"))

    @builtins.property
    @jsii.member(jsii_name="handleMethod")
    def handle_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "handleMethod"))

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "handler"))

    @builtins.property
    @jsii.member(jsii_name="handleStatus")
    def handle_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "handleStatus"))

    @builtins.property
    @jsii.member(jsii_name="handleTime")
    def handle_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "handleTime"))

    @builtins.property
    @jsii.member(jsii_name="hostId")
    def host_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostId"))

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @builtins.property
    @jsii.member(jsii_name="hostStatus")
    def host_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostStatus"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @builtins.property
    @jsii.member(jsii_name="occurTime")
    def occur_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "occurTime"))

    @builtins.property
    @jsii.member(jsii_name="operateAcceptList")
    def operate_accept_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "operateAcceptList"))

    @builtins.property
    @jsii.member(jsii_name="operateDetailList")
    def operate_detail_list(
        self,
    ) -> DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStructList:
        return typing.cast(DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStructList, jsii.get(self, "operateDetailList"))

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @builtins.property
    @jsii.member(jsii_name="processInfoList")
    def process_info_list(
        self,
    ) -> "DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStructList":
        return typing.cast("DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStructList", jsii.get(self, "processInfoList"))

    @builtins.property
    @jsii.member(jsii_name="protectStatus")
    def protect_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectStatus"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="recommendation")
    def recommendation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recommendation"))

    @builtins.property
    @jsii.member(jsii_name="resourceInfo")
    def resource_info(
        self,
    ) -> "DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfoList":
        return typing.cast("DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfoList", jsii.get(self, "resourceInfo"))

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @builtins.property
    @jsii.member(jsii_name="userInfoList")
    def user_info_list(
        self,
    ) -> "DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStructList":
        return typing.cast("DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStructList", jsii.get(self, "userInfoList"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5Events]:
        return typing.cast(typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5Events], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5Events],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__defc2711d1dfb845d7b1f20dbdb68124849587c12f51cbc1640a5f5a76baa3b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff37d312971874e72f8c283220815dd3cf1f513d4b9665f3293981480fc0d271)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07782a3a738cbf7144e58b7b91a614027b5907e32f757f85729212bcf3f7c918)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__073c9f87ddfb42c6e147248ea93109ad9291a7803148f781461dfa0a39af0d49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36c88f4bb07be8cdc10bcbcc90a10117f564e48761447d7cbcdf6b9f00896de7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__04d8a8064ca44d8cc495efffc53d5ecc3129eff625e276746843a196a8953258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d843727bd0b19c8450c8eec52b4509956f2cc19c89a50d9d8e0f2592df4c296)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="childProcessCmdline")
    def child_process_cmdline(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "childProcessCmdline"))

    @builtins.property
    @jsii.member(jsii_name="childProcessEgid")
    def child_process_egid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "childProcessEgid"))

    @builtins.property
    @jsii.member(jsii_name="childProcessEuid")
    def child_process_euid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "childProcessEuid"))

    @builtins.property
    @jsii.member(jsii_name="childProcessFilename")
    def child_process_filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "childProcessFilename"))

    @builtins.property
    @jsii.member(jsii_name="childProcessGid")
    def child_process_gid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "childProcessGid"))

    @builtins.property
    @jsii.member(jsii_name="childProcessName")
    def child_process_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "childProcessName"))

    @builtins.property
    @jsii.member(jsii_name="childProcessPath")
    def child_process_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "childProcessPath"))

    @builtins.property
    @jsii.member(jsii_name="childProcessPid")
    def child_process_pid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "childProcessPid"))

    @builtins.property
    @jsii.member(jsii_name="childProcessStartTime")
    def child_process_start_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "childProcessStartTime"))

    @builtins.property
    @jsii.member(jsii_name="childProcessUid")
    def child_process_uid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "childProcessUid"))

    @builtins.property
    @jsii.member(jsii_name="escapeCmd")
    def escape_cmd(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "escapeCmd"))

    @builtins.property
    @jsii.member(jsii_name="escapeMode")
    def escape_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "escapeMode"))

    @builtins.property
    @jsii.member(jsii_name="parentProcessCmdline")
    def parent_process_cmdline(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentProcessCmdline"))

    @builtins.property
    @jsii.member(jsii_name="parentProcessEgid")
    def parent_process_egid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parentProcessEgid"))

    @builtins.property
    @jsii.member(jsii_name="parentProcessEuid")
    def parent_process_euid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parentProcessEuid"))

    @builtins.property
    @jsii.member(jsii_name="parentProcessFilename")
    def parent_process_filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentProcessFilename"))

    @builtins.property
    @jsii.member(jsii_name="parentProcessGid")
    def parent_process_gid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parentProcessGid"))

    @builtins.property
    @jsii.member(jsii_name="parentProcessName")
    def parent_process_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentProcessName"))

    @builtins.property
    @jsii.member(jsii_name="parentProcessPath")
    def parent_process_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentProcessPath"))

    @builtins.property
    @jsii.member(jsii_name="parentProcessPid")
    def parent_process_pid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parentProcessPid"))

    @builtins.property
    @jsii.member(jsii_name="parentProcessStartTime")
    def parent_process_start_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parentProcessStartTime"))

    @builtins.property
    @jsii.member(jsii_name="parentProcessUid")
    def parent_process_uid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parentProcessUid"))

    @builtins.property
    @jsii.member(jsii_name="processCmdline")
    def process_cmdline(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processCmdline"))

    @builtins.property
    @jsii.member(jsii_name="processEgid")
    def process_egid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "processEgid"))

    @builtins.property
    @jsii.member(jsii_name="processEuid")
    def process_euid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "processEuid"))

    @builtins.property
    @jsii.member(jsii_name="processFilename")
    def process_filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processFilename"))

    @builtins.property
    @jsii.member(jsii_name="processGid")
    def process_gid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "processGid"))

    @builtins.property
    @jsii.member(jsii_name="processHash")
    def process_hash(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processHash"))

    @builtins.property
    @jsii.member(jsii_name="processName")
    def process_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processName"))

    @builtins.property
    @jsii.member(jsii_name="processPath")
    def process_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processPath"))

    @builtins.property
    @jsii.member(jsii_name="processPid")
    def process_pid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "processPid"))

    @builtins.property
    @jsii.member(jsii_name="processStartTime")
    def process_start_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "processStartTime"))

    @builtins.property
    @jsii.member(jsii_name="processUid")
    def process_uid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "processUid"))

    @builtins.property
    @jsii.member(jsii_name="processUsername")
    def process_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processUsername"))

    @builtins.property
    @jsii.member(jsii_name="virtCmd")
    def virt_cmd(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtCmd"))

    @builtins.property
    @jsii.member(jsii_name="virtProcessName")
    def virt_process_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtProcessName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStruct]:
        return typing.cast(typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9d02afb4e2abd258b0789072a0927ff57780814232bb02de03b4216aa978028)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__472ac614b3f6821815dda245dedbce1ddbf82450ad6a823719e1c5cd022b6310)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6044143f60f4afdb71b73a2389b123ab632d4a6295b7a02485b9e895eca68c2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__712c33127ce2759c38e0ffe489689ba9af50829fb128fd489e6262d640a741b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c3384a37bd2292fc3bd4c021a9714d48b44821d5ffbd0d159e3f4d296dd270f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c6cfa13befeefaa236a279829cce516fa5ee0976ee37216e55230ffd1077d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5be86b00215bae4efb53ab5721ae5046fb159a4d32da08c525261a708e4f73d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="containerId")
    def container_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerId"))

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @builtins.property
    @jsii.member(jsii_name="ecsId")
    def ecs_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ecsId"))

    @builtins.property
    @jsii.member(jsii_name="enterpriseProjectId")
    def enterprise_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enterpriseProjectId"))

    @builtins.property
    @jsii.member(jsii_name="hostAttr")
    def host_attr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostAttr"))

    @builtins.property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageId"))

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @builtins.property
    @jsii.member(jsii_name="microservice")
    def microservice(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "microservice"))

    @builtins.property
    @jsii.member(jsii_name="osBit")
    def os_bit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osBit"))

    @builtins.property
    @jsii.member(jsii_name="osName")
    def os_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osName"))

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersion"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="regionName")
    def region_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionName"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="sysArch")
    def sys_arch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sysArch"))

    @builtins.property
    @jsii.member(jsii_name="vmName")
    def vm_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmName"))

    @builtins.property
    @jsii.member(jsii_name="vmUuid")
    def vm_uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmUuid"))

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfo]:
        return typing.cast(typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58368edf9e3e2ced813221aaef11b7e121b74d58e2e00b28c539942f6412cf27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed1334320979fbdc97ebcca9db15a9559e7c66309392eb99f7537098833ac325)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a2d6aa1e315ee2d7c982bc9671c0156f301b06c3a124f05cf6278584e8e0b1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12b218d93c13343be2e2633b301886f056f0900d6321c266f1b280729a0ebce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87d62458b672466a29a9a908953e33e42e7956f4b2519c7c8affe08c8cc31234)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45f901ac9ef54b33f2ce16e62f49b88251b8b9c40ffea27484bc084178e61f67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudHssIntrusionEventsV5.DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a3f784067545f2ee66b7df0ad7b0063757ab7b798f3fd716e75f3c591dd80d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="loginFailCount")
    def login_fail_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "loginFailCount"))

    @builtins.property
    @jsii.member(jsii_name="loginIp")
    def login_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginIp"))

    @builtins.property
    @jsii.member(jsii_name="loginLastTime")
    def login_last_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "loginLastTime"))

    @builtins.property
    @jsii.member(jsii_name="loginMode")
    def login_mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "loginMode"))

    @builtins.property
    @jsii.member(jsii_name="pwdHash")
    def pwd_hash(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pwdHash"))

    @builtins.property
    @jsii.member(jsii_name="pwdMaxDays")
    def pwd_max_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pwdMaxDays"))

    @builtins.property
    @jsii.member(jsii_name="pwdMinDays")
    def pwd_min_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pwdMinDays"))

    @builtins.property
    @jsii.member(jsii_name="pwdUsedDays")
    def pwd_used_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pwdUsedDays"))

    @builtins.property
    @jsii.member(jsii_name="pwdWarnLeftDays")
    def pwd_warn_left_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pwdWarnLeftDays"))

    @builtins.property
    @jsii.member(jsii_name="pwdWithFuzzing")
    def pwd_with_fuzzing(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pwdWithFuzzing"))

    @builtins.property
    @jsii.member(jsii_name="servicePort")
    def service_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "servicePort"))

    @builtins.property
    @jsii.member(jsii_name="serviceType")
    def service_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceType"))

    @builtins.property
    @jsii.member(jsii_name="userGid")
    def user_gid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userGid"))

    @builtins.property
    @jsii.member(jsii_name="userGroupName")
    def user_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userGroupName"))

    @builtins.property
    @jsii.member(jsii_name="userHomeDir")
    def user_home_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userHomeDir"))

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userId"))

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStruct]:
        return typing.cast(typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b093ef56b1b093a5d934f47334a16ef067cef417e5e1a8a8bf12389c801ec283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataOpentelekomcloudHssIntrusionEventsV5",
    "DataOpentelekomcloudHssIntrusionEventsV5Config",
    "DataOpentelekomcloudHssIntrusionEventsV5Events",
    "DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStruct",
    "DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStructList",
    "DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStructOutputReference",
    "DataOpentelekomcloudHssIntrusionEventsV5EventsList",
    "DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStruct",
    "DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStructList",
    "DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStructOutputReference",
    "DataOpentelekomcloudHssIntrusionEventsV5EventsOutputReference",
    "DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStruct",
    "DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStructList",
    "DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStructOutputReference",
    "DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfo",
    "DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfoList",
    "DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfoOutputReference",
    "DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStruct",
    "DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStructList",
    "DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStructOutputReference",
]

publication.publish()

def _typecheckingstub__8ec037a6643da042fe70b8069d69295d545d2630b55d6ef133122931ad2f64cc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    category: builtins.str,
    begin_time: typing.Optional[builtins.str] = None,
    container_name: typing.Optional[builtins.str] = None,
    days: typing.Optional[jsii.Number] = None,
    end_time: typing.Optional[builtins.str] = None,
    enterprise_project_id: typing.Optional[builtins.str] = None,
    event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    handle_status: typing.Optional[builtins.str] = None,
    host_id: typing.Optional[builtins.str] = None,
    host_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    private_ip: typing.Optional[builtins.str] = None,
    severity: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__1dfab62fcd4d48a74946b28b16b0b488ac19147b35e3155f356b9befad24cd59(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2267450b9ec54ecf5e33716b77f88614a1d0a9fbd9091c7ce89bbe1f9469ba9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__065ce650bb4b0258c4d1f156d976006b8ad4928c1cf22cb514e36c2dd87a4613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f6d2d20f1b0d5bad913a1dd362fdedf30640ef5ada357d34d13d06c8cc8ccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee20c71068fedbdfad0e0950441df2a2d487a96abe559262b3b56bbc90e7502c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427fd02d02e2fb6a8e8b32a7623ed041f0bf1f3b0da82479c2974c05b57760be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab0b9b989fc38161d6b59207540c295eb09dcce09d0eca7fee716956e8aa4a3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b2b615f3ed2fe8ad2cd0c73f70056736c0ad84f992d15a3e321129913c0793(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf182bbb5a7118a11775fc4badc52ea3bd9a6f50791a975ae488a71bb29e4a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a85b7d4b1d7b6fb3dc88059a2994f4dcb7d903d216b428b721c43c9c0495631e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8424f3a372f28762003ec8093c2622e35e3b43b71e34817527a17d36d190d23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba90ce5b174ecfd7910486148d9fc2dd4fdd549fe115f685062b88ae69fb327(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1342816a9326a9f4cad167f16d513088d55bc920a8b12c7d0f2b93890608e5d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675dc4d63c5d0f7085c816a6d56c3fc3900085e382c4772500782f71188d49eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194804d25d8b8cffa92733fe86f29adfdfb7253683ae88d4dbca58d8ab963877(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    category: builtins.str,
    begin_time: typing.Optional[builtins.str] = None,
    container_name: typing.Optional[builtins.str] = None,
    days: typing.Optional[jsii.Number] = None,
    end_time: typing.Optional[builtins.str] = None,
    enterprise_project_id: typing.Optional[builtins.str] = None,
    event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    handle_status: typing.Optional[builtins.str] = None,
    host_id: typing.Optional[builtins.str] = None,
    host_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    private_ip: typing.Optional[builtins.str] = None,
    severity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c099f4e336d85ab4d9400360d1944776f34b42e205df2379e35cf5b8eb20188c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b3073678d4009b1d6c16a83ae74b35937b54ab82af8f9a9da7ec87f9b5e814a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d40fb4e9482f7c9352a15545de11a2e8bb008bc77aecd2252bb49ac1309061(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90f0d0839c2c44e2df801daddcf5ded7053e8e18555b4ffaede1520c4eaef90(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54876e928c9231c7f665422439f277dfbd2d4ce0bd3920b12820cf6897f5083(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__070c16e8051612bbe49c02bd55563a85dee5207aeb1a85148492a83927092f6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ec1372630fe23049e8a80ef7f4a873b1b016206b1d7b56d525bb6ff8ee1a9e(
    value: typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsFileInfoListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356d912d909c1b0fc16e9f103c539c5c291e33ca44f18cc95a0fd06280604422(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8f21a9c69efd9d0cd4ea84fa3b6351c5bb28f85f68621ab8822e89531e3d33(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__822dbe9d35cccab6af0248eeee138492be6c535c85871619334d42676070f531(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967df065b768bd8ef4d57ebdd26c6ca7e0140078924604877c3248fbc4c90847(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b30cc2a636d3cf24072a91b5ee208d562af24c6bbfb19d0167c723cd11101fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b5f0a5159748b141ad2fff7f545223e811d474b6865a4069addaa7669afd9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc0608d3543bca4af20ecc6eef0d769e11e6699633358505f25f734d18c14c8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278d4a08059abf717a08b3a54fd2ccea29993d31be28026e6d89fdaeced3e7a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8047158efba7bc94d5b38c2e29c9d860d49a9a4ea4704699b78fb4e01a982e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cce09e55701caa0794a35a3676d8e428273be569b35ba3a0e7b769ad3acba12(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b7e6e7a4be151e65721357d98dc348570f215a548ea5b7d1877b6e85b90cb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb2a3dac7330b93543ee728cc97b35b5aed3d6a63ee88742c87fd6bacd2aaf9(
    value: typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsOperateDetailListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aeeb79f0e0f36e889f9074b765263d231d319739a6a753c802e8d295c04ef76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__defc2711d1dfb845d7b1f20dbdb68124849587c12f51cbc1640a5f5a76baa3b9(
    value: typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5Events],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff37d312971874e72f8c283220815dd3cf1f513d4b9665f3293981480fc0d271(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07782a3a738cbf7144e58b7b91a614027b5907e32f757f85729212bcf3f7c918(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073c9f87ddfb42c6e147248ea93109ad9291a7803148f781461dfa0a39af0d49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c88f4bb07be8cdc10bcbcc90a10117f564e48761447d7cbcdf6b9f00896de7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d8a8064ca44d8cc495efffc53d5ecc3129eff625e276746843a196a8953258(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d843727bd0b19c8450c8eec52b4509956f2cc19c89a50d9d8e0f2592df4c296(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d02afb4e2abd258b0789072a0927ff57780814232bb02de03b4216aa978028(
    value: typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsProcessInfoListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472ac614b3f6821815dda245dedbce1ddbf82450ad6a823719e1c5cd022b6310(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6044143f60f4afdb71b73a2389b123ab632d4a6295b7a02485b9e895eca68c2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712c33127ce2759c38e0ffe489689ba9af50829fb128fd489e6262d640a741b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c3384a37bd2292fc3bd4c021a9714d48b44821d5ffbd0d159e3f4d296dd270f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6cfa13befeefaa236a279829cce516fa5ee0976ee37216e55230ffd1077d03(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be86b00215bae4efb53ab5721ae5046fb159a4d32da08c525261a708e4f73d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58368edf9e3e2ced813221aaef11b7e121b74d58e2e00b28c539942f6412cf27(
    value: typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsResourceInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed1334320979fbdc97ebcca9db15a9559e7c66309392eb99f7537098833ac325(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a2d6aa1e315ee2d7c982bc9671c0156f301b06c3a124f05cf6278584e8e0b1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12b218d93c13343be2e2633b301886f056f0900d6321c266f1b280729a0ebce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d62458b672466a29a9a908953e33e42e7956f4b2519c7c8affe08c8cc31234(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f901ac9ef54b33f2ce16e62f49b88251b8b9c40ffea27484bc084178e61f67(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3f784067545f2ee66b7df0ad7b0063757ab7b798f3fd716e75f3c591dd80d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b093ef56b1b093a5d934f47334a16ef067cef417e5e1a8a8bf12389c801ec283(
    value: typing.Optional[DataOpentelekomcloudHssIntrusionEventsV5EventsUserInfoListStruct],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `opentelekomcloud_dms_reassign_partitions_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_dms_reassign_partitions_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2).
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


class DmsReassignPartitionsV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dmsReassignPartitionsV2.DmsReassignPartitionsV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2 opentelekomcloud_dms_reassign_partitions_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        instance_id: builtins.str,
        reassignments: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DmsReassignPartitionsV2Reassignments", typing.Dict[builtins.str, typing.Any]]]],
        execute_at: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        is_schedule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        throttle: typing.Optional[jsii.Number] = None,
        time_estimate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2 opentelekomcloud_dms_reassign_partitions_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#instance_id DmsReassignPartitionsV2#instance_id}.
        :param reassignments: reassignments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#reassignments DmsReassignPartitionsV2#reassignments}
        :param execute_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#execute_at DmsReassignPartitionsV2#execute_at}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#id DmsReassignPartitionsV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#is_schedule DmsReassignPartitionsV2#is_schedule}.
        :param throttle: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#throttle DmsReassignPartitionsV2#throttle}.
        :param time_estimate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#time_estimate DmsReassignPartitionsV2#time_estimate}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65b89d8ccf9fbbf97454da8a0c04648f34c7e3eec141a7066ec26f7f06c03f20)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DmsReassignPartitionsV2Config(
            instance_id=instance_id,
            reassignments=reassignments,
            execute_at=execute_at,
            id=id,
            is_schedule=is_schedule,
            throttle=throttle,
            time_estimate=time_estimate,
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
        '''Generates CDKTF code for importing a DmsReassignPartitionsV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DmsReassignPartitionsV2 to import.
        :param import_from_id: The id of the existing DmsReassignPartitionsV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DmsReassignPartitionsV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__491e2f5d1c9050df7a3491b7e60d08f6b02ffd740e6ab7f5a36856c887383279)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putReassignments")
    def put_reassignments(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DmsReassignPartitionsV2Reassignments", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdd07c524a452db6ebb2fd6a2ee991e4c04e8ed5ed2b09b279c8e50cf5f7bc68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putReassignments", [value]))

    @jsii.member(jsii_name="resetExecuteAt")
    def reset_execute_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecuteAt", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsSchedule")
    def reset_is_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSchedule", []))

    @jsii.member(jsii_name="resetThrottle")
    def reset_throttle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottle", []))

    @jsii.member(jsii_name="resetTimeEstimate")
    def reset_time_estimate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeEstimate", []))

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
    @jsii.member(jsii_name="reassignments")
    def reassignments(self) -> "DmsReassignPartitionsV2ReassignmentsList":
        return typing.cast("DmsReassignPartitionsV2ReassignmentsList", jsii.get(self, "reassignments"))

    @builtins.property
    @jsii.member(jsii_name="reassignmentTime")
    def reassignment_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "reassignmentTime"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="executeAtInput")
    def execute_at_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executeAtInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="isScheduleInput")
    def is_schedule_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="reassignmentsInput")
    def reassignments_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DmsReassignPartitionsV2Reassignments"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DmsReassignPartitionsV2Reassignments"]]], jsii.get(self, "reassignmentsInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleInput")
    def throttle_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throttleInput"))

    @builtins.property
    @jsii.member(jsii_name="timeEstimateInput")
    def time_estimate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeEstimateInput"))

    @builtins.property
    @jsii.member(jsii_name="executeAt")
    def execute_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "executeAt"))

    @execute_at.setter
    def execute_at(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b23644299eda3ecb62b343a45625b4c6eddc4bff346e11bc158fc6dd06e79472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executeAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21ccf17889093d8479fed2db4fff36f712ebee3e870f028824a158441efdc4f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57da0e2dffff1dac37f557d4d82e89aa19a1c2ddeac00ead5760a6356d903638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSchedule")
    def is_schedule(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isSchedule"))

    @is_schedule.setter
    def is_schedule(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba955a1dd4579f81a1424d926d71d705b0f84720cc6355841a2d9c47f0b53d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throttle")
    def throttle(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throttle"))

    @throttle.setter
    def throttle(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f24477a84e464b7133244be2cfd1d8e34e13b07b6a0a77da8d5d7b282d2a2801)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeEstimate")
    def time_estimate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "timeEstimate"))

    @time_estimate.setter
    def time_estimate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49b3ef61dc3fdde36ca1ef123b9688d388f3a39f78e1133715fdc3202b37e298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeEstimate", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dmsReassignPartitionsV2.DmsReassignPartitionsV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "instance_id": "instanceId",
        "reassignments": "reassignments",
        "execute_at": "executeAt",
        "id": "id",
        "is_schedule": "isSchedule",
        "throttle": "throttle",
        "time_estimate": "timeEstimate",
    },
)
class DmsReassignPartitionsV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        instance_id: builtins.str,
        reassignments: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DmsReassignPartitionsV2Reassignments", typing.Dict[builtins.str, typing.Any]]]],
        execute_at: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        is_schedule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        throttle: typing.Optional[jsii.Number] = None,
        time_estimate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#instance_id DmsReassignPartitionsV2#instance_id}.
        :param reassignments: reassignments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#reassignments DmsReassignPartitionsV2#reassignments}
        :param execute_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#execute_at DmsReassignPartitionsV2#execute_at}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#id DmsReassignPartitionsV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#is_schedule DmsReassignPartitionsV2#is_schedule}.
        :param throttle: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#throttle DmsReassignPartitionsV2#throttle}.
        :param time_estimate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#time_estimate DmsReassignPartitionsV2#time_estimate}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47e12087658f880c13bf92f0d9bc50dccec51fe14327d38be636270d767c1e37)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument reassignments", value=reassignments, expected_type=type_hints["reassignments"])
            check_type(argname="argument execute_at", value=execute_at, expected_type=type_hints["execute_at"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_schedule", value=is_schedule, expected_type=type_hints["is_schedule"])
            check_type(argname="argument throttle", value=throttle, expected_type=type_hints["throttle"])
            check_type(argname="argument time_estimate", value=time_estimate, expected_type=type_hints["time_estimate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_id": instance_id,
            "reassignments": reassignments,
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
        if execute_at is not None:
            self._values["execute_at"] = execute_at
        if id is not None:
            self._values["id"] = id
        if is_schedule is not None:
            self._values["is_schedule"] = is_schedule
        if throttle is not None:
            self._values["throttle"] = throttle
        if time_estimate is not None:
            self._values["time_estimate"] = time_estimate

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
    def instance_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#instance_id DmsReassignPartitionsV2#instance_id}.'''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def reassignments(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DmsReassignPartitionsV2Reassignments"]]:
        '''reassignments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#reassignments DmsReassignPartitionsV2#reassignments}
        '''
        result = self._values.get("reassignments")
        assert result is not None, "Required property 'reassignments' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DmsReassignPartitionsV2Reassignments"]], result)

    @builtins.property
    def execute_at(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#execute_at DmsReassignPartitionsV2#execute_at}.'''
        result = self._values.get("execute_at")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#id DmsReassignPartitionsV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_schedule(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#is_schedule DmsReassignPartitionsV2#is_schedule}.'''
        result = self._values.get("is_schedule")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def throttle(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#throttle DmsReassignPartitionsV2#throttle}.'''
        result = self._values.get("throttle")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def time_estimate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#time_estimate DmsReassignPartitionsV2#time_estimate}.'''
        result = self._values.get("time_estimate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsReassignPartitionsV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dmsReassignPartitionsV2.DmsReassignPartitionsV2Reassignments",
    jsii_struct_bases=[],
    name_mapping={
        "topic": "topic",
        "assignments": "assignments",
        "brokers": "brokers",
        "replication_factor": "replicationFactor",
    },
)
class DmsReassignPartitionsV2Reassignments:
    def __init__(
        self,
        *,
        topic: builtins.str,
        assignments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DmsReassignPartitionsV2ReassignmentsAssignments", typing.Dict[builtins.str, typing.Any]]]]] = None,
        brokers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        replication_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#topic DmsReassignPartitionsV2#topic}.
        :param assignments: assignments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#assignments DmsReassignPartitionsV2#assignments}
        :param brokers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#brokers DmsReassignPartitionsV2#brokers}.
        :param replication_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#replication_factor DmsReassignPartitionsV2#replication_factor}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8751143fc64894eb165211e1feb281126fce0693e7233aaef13717fab26f94d6)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument assignments", value=assignments, expected_type=type_hints["assignments"])
            check_type(argname="argument brokers", value=brokers, expected_type=type_hints["brokers"])
            check_type(argname="argument replication_factor", value=replication_factor, expected_type=type_hints["replication_factor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic": topic,
        }
        if assignments is not None:
            self._values["assignments"] = assignments
        if brokers is not None:
            self._values["brokers"] = brokers
        if replication_factor is not None:
            self._values["replication_factor"] = replication_factor

    @builtins.property
    def topic(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#topic DmsReassignPartitionsV2#topic}.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def assignments(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DmsReassignPartitionsV2ReassignmentsAssignments"]]]:
        '''assignments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#assignments DmsReassignPartitionsV2#assignments}
        '''
        result = self._values.get("assignments")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DmsReassignPartitionsV2ReassignmentsAssignments"]]], result)

    @builtins.property
    def brokers(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#brokers DmsReassignPartitionsV2#brokers}.'''
        result = self._values.get("brokers")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def replication_factor(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#replication_factor DmsReassignPartitionsV2#replication_factor}.'''
        result = self._values.get("replication_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsReassignPartitionsV2Reassignments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dmsReassignPartitionsV2.DmsReassignPartitionsV2ReassignmentsAssignments",
    jsii_struct_bases=[],
    name_mapping={"partition": "partition", "partition_brokers": "partitionBrokers"},
)
class DmsReassignPartitionsV2ReassignmentsAssignments:
    def __init__(
        self,
        *,
        partition: typing.Optional[jsii.Number] = None,
        partition_brokers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param partition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#partition DmsReassignPartitionsV2#partition}.
        :param partition_brokers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#partition_brokers DmsReassignPartitionsV2#partition_brokers}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f261081de80c2335f6f71f76aac5bb2dc0d4b17627709935027114e3e2de92)
            check_type(argname="argument partition", value=partition, expected_type=type_hints["partition"])
            check_type(argname="argument partition_brokers", value=partition_brokers, expected_type=type_hints["partition_brokers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if partition is not None:
            self._values["partition"] = partition
        if partition_brokers is not None:
            self._values["partition_brokers"] = partition_brokers

    @builtins.property
    def partition(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#partition DmsReassignPartitionsV2#partition}.'''
        result = self._values.get("partition")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def partition_brokers(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_reassign_partitions_v2#partition_brokers DmsReassignPartitionsV2#partition_brokers}.'''
        result = self._values.get("partition_brokers")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsReassignPartitionsV2ReassignmentsAssignments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsReassignPartitionsV2ReassignmentsAssignmentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dmsReassignPartitionsV2.DmsReassignPartitionsV2ReassignmentsAssignmentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__278de9c442702b910bf8c259a8d335ac7ff6c3b85096cf9b7f305b1af97c25df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DmsReassignPartitionsV2ReassignmentsAssignmentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0876ff3bb3ed074ca90667062b44b508a9e543f7239bb46f7facf71cbea20dc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DmsReassignPartitionsV2ReassignmentsAssignmentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__698cbae669b2eedaed29788aad45084f6aada64e146ca33b3d6e2784f3efc927)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c67d8ed412cf6e69632594f2f683ee98ac11db770d0cffc72ff5c4670a79183)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a0272780cddedc0b5a45cd0e123c9dfce6d62747c05c9a9eea95c3e8c76b1de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DmsReassignPartitionsV2ReassignmentsAssignments]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DmsReassignPartitionsV2ReassignmentsAssignments]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DmsReassignPartitionsV2ReassignmentsAssignments]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d4a5ea64fa0d521527d920e30172c18e25794cbac87e4182b662300a3a2ae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DmsReassignPartitionsV2ReassignmentsAssignmentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dmsReassignPartitionsV2.DmsReassignPartitionsV2ReassignmentsAssignmentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3539cc5ec67c0c136f30d7a11899c73903ad753e6d4602f2d41a2e571d0e5514)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPartition")
    def reset_partition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartition", []))

    @jsii.member(jsii_name="resetPartitionBrokers")
    def reset_partition_brokers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionBrokers", []))

    @builtins.property
    @jsii.member(jsii_name="partitionBrokersInput")
    def partition_brokers_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "partitionBrokersInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionInput")
    def partition_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "partitionInput"))

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "partition"))

    @partition.setter
    def partition(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b4c1a058cdf19e2696a213e07503cf5552937e6421a13f7d76c7338f6d7541c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partitionBrokers")
    def partition_brokers(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "partitionBrokers"))

    @partition_brokers.setter
    def partition_brokers(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f309571788443ecad3cff28143008a1d2ec6608055b5ad0b6115f1a6d0ca355f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionBrokers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsReassignPartitionsV2ReassignmentsAssignments]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsReassignPartitionsV2ReassignmentsAssignments]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsReassignPartitionsV2ReassignmentsAssignments]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eabda94a4660081062b37f9964376b011b18d2276b425904adee38773587e79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DmsReassignPartitionsV2ReassignmentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dmsReassignPartitionsV2.DmsReassignPartitionsV2ReassignmentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef6908965ff66eb66d89c254ac07ced36f948c24cd17b3c96e0d7cee764cb218)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DmsReassignPartitionsV2ReassignmentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8816b0b6e7167696f8a3b4a0bca55e029a27a331bff494f6da5c98ff9b4598b4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DmsReassignPartitionsV2ReassignmentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e5cf3e373c65de9747ae2a25452277c1c2a70ad791459510aa2cf73a95e4fc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2357504964a157b56d101d19900c1e8b88f2385d7a8c783140cc30b243bae82d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8410c5977b077868c37b576a835f7d5fa3a1007bca63c885ef557533d0ef37f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DmsReassignPartitionsV2Reassignments]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DmsReassignPartitionsV2Reassignments]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DmsReassignPartitionsV2Reassignments]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1fc07f44104ff3f89325824415a338bd5f311111ad47728b6a293effb3abc4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DmsReassignPartitionsV2ReassignmentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dmsReassignPartitionsV2.DmsReassignPartitionsV2ReassignmentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1c3113d42a26300ac3a8b17b654761b26a78fedb28fd493a7db2de2c810e1a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAssignments")
    def put_assignments(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DmsReassignPartitionsV2ReassignmentsAssignments, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b270a416fee11ca2c4acc84be80262760a4780b80f3c09e9e7e465e27e725bda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAssignments", [value]))

    @jsii.member(jsii_name="resetAssignments")
    def reset_assignments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssignments", []))

    @jsii.member(jsii_name="resetBrokers")
    def reset_brokers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBrokers", []))

    @jsii.member(jsii_name="resetReplicationFactor")
    def reset_replication_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicationFactor", []))

    @builtins.property
    @jsii.member(jsii_name="assignments")
    def assignments(self) -> DmsReassignPartitionsV2ReassignmentsAssignmentsList:
        return typing.cast(DmsReassignPartitionsV2ReassignmentsAssignmentsList, jsii.get(self, "assignments"))

    @builtins.property
    @jsii.member(jsii_name="assignmentsInput")
    def assignments_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DmsReassignPartitionsV2ReassignmentsAssignments]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DmsReassignPartitionsV2ReassignmentsAssignments]]], jsii.get(self, "assignmentsInput"))

    @builtins.property
    @jsii.member(jsii_name="brokersInput")
    def brokers_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "brokersInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationFactorInput")
    def replication_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicationFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="brokers")
    def brokers(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "brokers"))

    @brokers.setter
    def brokers(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a44a5e1e7c3ded137861e65a494dc9e2619af3b3f6c0dca7d9f01f8e240311f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "brokers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicationFactor")
    def replication_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicationFactor"))

    @replication_factor.setter
    def replication_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0478f1cbc2922db3cf9b4c74860c8572f9bce4088078e625d596d338fc6a664d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9eca23a36e2f95757203115d164856eef7ffde5bb0a2614a6e3ee08a79d955b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsReassignPartitionsV2Reassignments]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsReassignPartitionsV2Reassignments]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsReassignPartitionsV2Reassignments]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2fc3b8f98677c7578f11f11d00e3f3bc2d5db6b52b6d55abf9290158a500a30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DmsReassignPartitionsV2",
    "DmsReassignPartitionsV2Config",
    "DmsReassignPartitionsV2Reassignments",
    "DmsReassignPartitionsV2ReassignmentsAssignments",
    "DmsReassignPartitionsV2ReassignmentsAssignmentsList",
    "DmsReassignPartitionsV2ReassignmentsAssignmentsOutputReference",
    "DmsReassignPartitionsV2ReassignmentsList",
    "DmsReassignPartitionsV2ReassignmentsOutputReference",
]

publication.publish()

def _typecheckingstub__65b89d8ccf9fbbf97454da8a0c04648f34c7e3eec141a7066ec26f7f06c03f20(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    instance_id: builtins.str,
    reassignments: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DmsReassignPartitionsV2Reassignments, typing.Dict[builtins.str, typing.Any]]]],
    execute_at: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    is_schedule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    throttle: typing.Optional[jsii.Number] = None,
    time_estimate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__491e2f5d1c9050df7a3491b7e60d08f6b02ffd740e6ab7f5a36856c887383279(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd07c524a452db6ebb2fd6a2ee991e4c04e8ed5ed2b09b279c8e50cf5f7bc68(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DmsReassignPartitionsV2Reassignments, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b23644299eda3ecb62b343a45625b4c6eddc4bff346e11bc158fc6dd06e79472(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ccf17889093d8479fed2db4fff36f712ebee3e870f028824a158441efdc4f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57da0e2dffff1dac37f557d4d82e89aa19a1c2ddeac00ead5760a6356d903638(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba955a1dd4579f81a1424d926d71d705b0f84720cc6355841a2d9c47f0b53d6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24477a84e464b7133244be2cfd1d8e34e13b07b6a0a77da8d5d7b282d2a2801(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49b3ef61dc3fdde36ca1ef123b9688d388f3a39f78e1133715fdc3202b37e298(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e12087658f880c13bf92f0d9bc50dccec51fe14327d38be636270d767c1e37(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_id: builtins.str,
    reassignments: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DmsReassignPartitionsV2Reassignments, typing.Dict[builtins.str, typing.Any]]]],
    execute_at: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    is_schedule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    throttle: typing.Optional[jsii.Number] = None,
    time_estimate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8751143fc64894eb165211e1feb281126fce0693e7233aaef13717fab26f94d6(
    *,
    topic: builtins.str,
    assignments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DmsReassignPartitionsV2ReassignmentsAssignments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    brokers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    replication_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f261081de80c2335f6f71f76aac5bb2dc0d4b17627709935027114e3e2de92(
    *,
    partition: typing.Optional[jsii.Number] = None,
    partition_brokers: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278de9c442702b910bf8c259a8d335ac7ff6c3b85096cf9b7f305b1af97c25df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0876ff3bb3ed074ca90667062b44b508a9e543f7239bb46f7facf71cbea20dc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698cbae669b2eedaed29788aad45084f6aada64e146ca33b3d6e2784f3efc927(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c67d8ed412cf6e69632594f2f683ee98ac11db770d0cffc72ff5c4670a79183(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a0272780cddedc0b5a45cd0e123c9dfce6d62747c05c9a9eea95c3e8c76b1de(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d4a5ea64fa0d521527d920e30172c18e25794cbac87e4182b662300a3a2ae8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DmsReassignPartitionsV2ReassignmentsAssignments]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3539cc5ec67c0c136f30d7a11899c73903ad753e6d4602f2d41a2e571d0e5514(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b4c1a058cdf19e2696a213e07503cf5552937e6421a13f7d76c7338f6d7541c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f309571788443ecad3cff28143008a1d2ec6608055b5ad0b6115f1a6d0ca355f(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eabda94a4660081062b37f9964376b011b18d2276b425904adee38773587e79(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsReassignPartitionsV2ReassignmentsAssignments]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6908965ff66eb66d89c254ac07ced36f948c24cd17b3c96e0d7cee764cb218(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8816b0b6e7167696f8a3b4a0bca55e029a27a331bff494f6da5c98ff9b4598b4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e5cf3e373c65de9747ae2a25452277c1c2a70ad791459510aa2cf73a95e4fc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2357504964a157b56d101d19900c1e8b88f2385d7a8c783140cc30b243bae82d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8410c5977b077868c37b576a835f7d5fa3a1007bca63c885ef557533d0ef37f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1fc07f44104ff3f89325824415a338bd5f311111ad47728b6a293effb3abc4f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DmsReassignPartitionsV2Reassignments]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c3113d42a26300ac3a8b17b654761b26a78fedb28fd493a7db2de2c810e1a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b270a416fee11ca2c4acc84be80262760a4780b80f3c09e9e7e465e27e725bda(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DmsReassignPartitionsV2ReassignmentsAssignments, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a44a5e1e7c3ded137861e65a494dc9e2619af3b3f6c0dca7d9f01f8e240311f(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0478f1cbc2922db3cf9b4c74860c8572f9bce4088078e625d596d338fc6a664d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9eca23a36e2f95757203115d164856eef7ffde5bb0a2614a6e3ee08a79d955b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2fc3b8f98677c7578f11f11d00e3f3bc2d5db6b52b6d55abf9290158a500a30(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsReassignPartitionsV2Reassignments]],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `opentelekomcloud_dis_dump_task_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_dis_dump_task_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2).
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


class DisDumpTaskV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.disDumpTaskV2.DisDumpTaskV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2 opentelekomcloud_dis_dump_task_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        stream_name: builtins.str,
        action: typing.Optional[builtins.str] = None,
        destination: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        obs_destination_descriptor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DisDumpTaskV2ObsDestinationDescriptor", typing.Dict[builtins.str, typing.Any]]]]] = None,
        obs_processing_schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DisDumpTaskV2ObsProcessingSchema", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["DisDumpTaskV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2 opentelekomcloud_dis_dump_task_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#stream_name DisDumpTaskV2#stream_name}.
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#action DisDumpTaskV2#action}.
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#destination DisDumpTaskV2#destination}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#id DisDumpTaskV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param obs_destination_descriptor: obs_destination_descriptor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#obs_destination_descriptor DisDumpTaskV2#obs_destination_descriptor}
        :param obs_processing_schema: obs_processing_schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#obs_processing_schema DisDumpTaskV2#obs_processing_schema}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#timeouts DisDumpTaskV2#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c4aea751ca0f8dbebdc185cb672ab054c673243143a90af23c9d00c3b74dc7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DisDumpTaskV2Config(
            stream_name=stream_name,
            action=action,
            destination=destination,
            id=id,
            obs_destination_descriptor=obs_destination_descriptor,
            obs_processing_schema=obs_processing_schema,
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
        '''Generates CDKTF code for importing a DisDumpTaskV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DisDumpTaskV2 to import.
        :param import_from_id: The id of the existing DisDumpTaskV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DisDumpTaskV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d707a2692e9d631ae1c339d7501941a86c0a9efed951a7e1cf0b45cb2d19060)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putObsDestinationDescriptor")
    def put_obs_destination_descriptor(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DisDumpTaskV2ObsDestinationDescriptor", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__876db20e2a517ca5f4719e20c6b4e54642fc4349aa33004a4be81076ddf7f985)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putObsDestinationDescriptor", [value]))

    @jsii.member(jsii_name="putObsProcessingSchema")
    def put_obs_processing_schema(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DisDumpTaskV2ObsProcessingSchema", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9e2de63a55eab5e1a00aaaf93f46857b5d235e2ef9231c467a3f00443d22a31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putObsProcessingSchema", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, update: typing.Optional[builtins.str] = None) -> None:
        '''
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#update DisDumpTaskV2#update}.
        '''
        value = DisDumpTaskV2Timeouts(update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetDestination")
    def reset_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestination", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetObsDestinationDescriptor")
    def reset_obs_destination_descriptor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObsDestinationDescriptor", []))

    @jsii.member(jsii_name="resetObsProcessingSchema")
    def reset_obs_processing_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObsProcessingSchema", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="lastTransferTimestamp")
    def last_transfer_timestamp(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lastTransferTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="obsDestinationDescriptor")
    def obs_destination_descriptor(self) -> "DisDumpTaskV2ObsDestinationDescriptorList":
        return typing.cast("DisDumpTaskV2ObsDestinationDescriptorList", jsii.get(self, "obsDestinationDescriptor"))

    @builtins.property
    @jsii.member(jsii_name="obsProcessingSchema")
    def obs_processing_schema(self) -> "DisDumpTaskV2ObsProcessingSchemaList":
        return typing.cast("DisDumpTaskV2ObsProcessingSchemaList", jsii.get(self, "obsProcessingSchema"))

    @builtins.property
    @jsii.member(jsii_name="partitions")
    def partitions(self) -> "DisDumpTaskV2PartitionsList":
        return typing.cast("DisDumpTaskV2PartitionsList", jsii.get(self, "partitions"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="taskId")
    def task_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DisDumpTaskV2TimeoutsOutputReference":
        return typing.cast("DisDumpTaskV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="obsDestinationDescriptorInput")
    def obs_destination_descriptor_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DisDumpTaskV2ObsDestinationDescriptor"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DisDumpTaskV2ObsDestinationDescriptor"]]], jsii.get(self, "obsDestinationDescriptorInput"))

    @builtins.property
    @jsii.member(jsii_name="obsProcessingSchemaInput")
    def obs_processing_schema_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DisDumpTaskV2ObsProcessingSchema"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DisDumpTaskV2ObsProcessingSchema"]]], jsii.get(self, "obsProcessingSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="streamNameInput")
    def stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DisDumpTaskV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DisDumpTaskV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e961b62c02303f39a15fae86c7c5b955d118b3c07dc78356d433da8efd83d74c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb91c6a20472cb7435f27c80428e403fd289e86c6117c6e74b5e23f5c7dd90a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__999004f80bfd33230705c3bb9f53660f183e9367d500b6530a29328fe6836ca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamName"))

    @stream_name.setter
    def stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd97f8dd6e85663e38fe24aeb9e658ae2565efd45d2e6352784ba52fa7d2409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.disDumpTaskV2.DisDumpTaskV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "stream_name": "streamName",
        "action": "action",
        "destination": "destination",
        "id": "id",
        "obs_destination_descriptor": "obsDestinationDescriptor",
        "obs_processing_schema": "obsProcessingSchema",
        "timeouts": "timeouts",
    },
)
class DisDumpTaskV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        stream_name: builtins.str,
        action: typing.Optional[builtins.str] = None,
        destination: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        obs_destination_descriptor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DisDumpTaskV2ObsDestinationDescriptor", typing.Dict[builtins.str, typing.Any]]]]] = None,
        obs_processing_schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DisDumpTaskV2ObsProcessingSchema", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["DisDumpTaskV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#stream_name DisDumpTaskV2#stream_name}.
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#action DisDumpTaskV2#action}.
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#destination DisDumpTaskV2#destination}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#id DisDumpTaskV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param obs_destination_descriptor: obs_destination_descriptor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#obs_destination_descriptor DisDumpTaskV2#obs_destination_descriptor}
        :param obs_processing_schema: obs_processing_schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#obs_processing_schema DisDumpTaskV2#obs_processing_schema}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#timeouts DisDumpTaskV2#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DisDumpTaskV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e4a727944ccca2eb0e51824c0cff355ce6250caa2e55b6037b9652fd2d09b4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument obs_destination_descriptor", value=obs_destination_descriptor, expected_type=type_hints["obs_destination_descriptor"])
            check_type(argname="argument obs_processing_schema", value=obs_processing_schema, expected_type=type_hints["obs_processing_schema"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stream_name": stream_name,
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
        if action is not None:
            self._values["action"] = action
        if destination is not None:
            self._values["destination"] = destination
        if id is not None:
            self._values["id"] = id
        if obs_destination_descriptor is not None:
            self._values["obs_destination_descriptor"] = obs_destination_descriptor
        if obs_processing_schema is not None:
            self._values["obs_processing_schema"] = obs_processing_schema
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
    def stream_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#stream_name DisDumpTaskV2#stream_name}.'''
        result = self._values.get("stream_name")
        assert result is not None, "Required property 'stream_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#action DisDumpTaskV2#action}.'''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#destination DisDumpTaskV2#destination}.'''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#id DisDumpTaskV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def obs_destination_descriptor(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DisDumpTaskV2ObsDestinationDescriptor"]]]:
        '''obs_destination_descriptor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#obs_destination_descriptor DisDumpTaskV2#obs_destination_descriptor}
        '''
        result = self._values.get("obs_destination_descriptor")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DisDumpTaskV2ObsDestinationDescriptor"]]], result)

    @builtins.property
    def obs_processing_schema(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DisDumpTaskV2ObsProcessingSchema"]]]:
        '''obs_processing_schema block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#obs_processing_schema DisDumpTaskV2#obs_processing_schema}
        '''
        result = self._values.get("obs_processing_schema")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DisDumpTaskV2ObsProcessingSchema"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DisDumpTaskV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#timeouts DisDumpTaskV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DisDumpTaskV2Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DisDumpTaskV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.disDumpTaskV2.DisDumpTaskV2ObsDestinationDescriptor",
    jsii_struct_bases=[],
    name_mapping={
        "agency_name": "agencyName",
        "deliver_time_interval": "deliverTimeInterval",
        "obs_bucket_path": "obsBucketPath",
        "task_name": "taskName",
        "consumer_strategy": "consumerStrategy",
        "destination_file_type": "destinationFileType",
        "file_prefix": "filePrefix",
        "partition_format": "partitionFormat",
        "record_delimiter": "recordDelimiter",
    },
)
class DisDumpTaskV2ObsDestinationDescriptor:
    def __init__(
        self,
        *,
        agency_name: builtins.str,
        deliver_time_interval: jsii.Number,
        obs_bucket_path: builtins.str,
        task_name: builtins.str,
        consumer_strategy: typing.Optional[builtins.str] = None,
        destination_file_type: typing.Optional[builtins.str] = None,
        file_prefix: typing.Optional[builtins.str] = None,
        partition_format: typing.Optional[builtins.str] = None,
        record_delimiter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param agency_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#agency_name DisDumpTaskV2#agency_name}.
        :param deliver_time_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#deliver_time_interval DisDumpTaskV2#deliver_time_interval}.
        :param obs_bucket_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#obs_bucket_path DisDumpTaskV2#obs_bucket_path}.
        :param task_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#task_name DisDumpTaskV2#task_name}.
        :param consumer_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#consumer_strategy DisDumpTaskV2#consumer_strategy}.
        :param destination_file_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#destination_file_type DisDumpTaskV2#destination_file_type}.
        :param file_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#file_prefix DisDumpTaskV2#file_prefix}.
        :param partition_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#partition_format DisDumpTaskV2#partition_format}.
        :param record_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#record_delimiter DisDumpTaskV2#record_delimiter}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10bec956236826d70cca0e72ca127216388f2a937260c4569ef093e2b1659726)
            check_type(argname="argument agency_name", value=agency_name, expected_type=type_hints["agency_name"])
            check_type(argname="argument deliver_time_interval", value=deliver_time_interval, expected_type=type_hints["deliver_time_interval"])
            check_type(argname="argument obs_bucket_path", value=obs_bucket_path, expected_type=type_hints["obs_bucket_path"])
            check_type(argname="argument task_name", value=task_name, expected_type=type_hints["task_name"])
            check_type(argname="argument consumer_strategy", value=consumer_strategy, expected_type=type_hints["consumer_strategy"])
            check_type(argname="argument destination_file_type", value=destination_file_type, expected_type=type_hints["destination_file_type"])
            check_type(argname="argument file_prefix", value=file_prefix, expected_type=type_hints["file_prefix"])
            check_type(argname="argument partition_format", value=partition_format, expected_type=type_hints["partition_format"])
            check_type(argname="argument record_delimiter", value=record_delimiter, expected_type=type_hints["record_delimiter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agency_name": agency_name,
            "deliver_time_interval": deliver_time_interval,
            "obs_bucket_path": obs_bucket_path,
            "task_name": task_name,
        }
        if consumer_strategy is not None:
            self._values["consumer_strategy"] = consumer_strategy
        if destination_file_type is not None:
            self._values["destination_file_type"] = destination_file_type
        if file_prefix is not None:
            self._values["file_prefix"] = file_prefix
        if partition_format is not None:
            self._values["partition_format"] = partition_format
        if record_delimiter is not None:
            self._values["record_delimiter"] = record_delimiter

    @builtins.property
    def agency_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#agency_name DisDumpTaskV2#agency_name}.'''
        result = self._values.get("agency_name")
        assert result is not None, "Required property 'agency_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deliver_time_interval(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#deliver_time_interval DisDumpTaskV2#deliver_time_interval}.'''
        result = self._values.get("deliver_time_interval")
        assert result is not None, "Required property 'deliver_time_interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def obs_bucket_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#obs_bucket_path DisDumpTaskV2#obs_bucket_path}.'''
        result = self._values.get("obs_bucket_path")
        assert result is not None, "Required property 'obs_bucket_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def task_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#task_name DisDumpTaskV2#task_name}.'''
        result = self._values.get("task_name")
        assert result is not None, "Required property 'task_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def consumer_strategy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#consumer_strategy DisDumpTaskV2#consumer_strategy}.'''
        result = self._values.get("consumer_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_file_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#destination_file_type DisDumpTaskV2#destination_file_type}.'''
        result = self._values.get("destination_file_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#file_prefix DisDumpTaskV2#file_prefix}.'''
        result = self._values.get("file_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#partition_format DisDumpTaskV2#partition_format}.'''
        result = self._values.get("partition_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def record_delimiter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#record_delimiter DisDumpTaskV2#record_delimiter}.'''
        result = self._values.get("record_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DisDumpTaskV2ObsDestinationDescriptor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DisDumpTaskV2ObsDestinationDescriptorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.disDumpTaskV2.DisDumpTaskV2ObsDestinationDescriptorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93d29de1530348e0921841b47d7d4fa8d732cfe117e5b3a31adb75a207f9d1ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DisDumpTaskV2ObsDestinationDescriptorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00875446ce439c1ffb3bd1ce377950726ae5edd59b8d3c0ca1e2264875d88c60)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DisDumpTaskV2ObsDestinationDescriptorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8518c6fafea8c6bf21f1e8317b6effa6b5ade0217b06384e276987cdecbaf48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77b732f237ef4598a5457fcab4a9a0caf6889d80a50a01763e329d984d14b80e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__696849da724e213d4ec030ce69e8e5255000c54c85ab94598a6c5bd969e02569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DisDumpTaskV2ObsDestinationDescriptor]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DisDumpTaskV2ObsDestinationDescriptor]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DisDumpTaskV2ObsDestinationDescriptor]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0d97cfc7a917eba323548d08752b7ea7e8dd4824f98b64313452692910935d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DisDumpTaskV2ObsDestinationDescriptorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.disDumpTaskV2.DisDumpTaskV2ObsDestinationDescriptorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7c48119310be83f8b4e9da1fd616feb6c38744c8b7cdaf96bca8df3603c10f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConsumerStrategy")
    def reset_consumer_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerStrategy", []))

    @jsii.member(jsii_name="resetDestinationFileType")
    def reset_destination_file_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationFileType", []))

    @jsii.member(jsii_name="resetFilePrefix")
    def reset_file_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilePrefix", []))

    @jsii.member(jsii_name="resetPartitionFormat")
    def reset_partition_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionFormat", []))

    @jsii.member(jsii_name="resetRecordDelimiter")
    def reset_record_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordDelimiter", []))

    @builtins.property
    @jsii.member(jsii_name="agencyNameInput")
    def agency_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerStrategyInput")
    def consumer_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="deliverTimeIntervalInput")
    def deliver_time_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deliverTimeIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationFileTypeInput")
    def destination_file_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationFileTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="filePrefixInput")
    def file_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="obsBucketPathInput")
    def obs_bucket_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "obsBucketPathInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionFormatInput")
    def partition_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partitionFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="recordDelimiterInput")
    def record_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="taskNameInput")
    def task_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskNameInput"))

    @builtins.property
    @jsii.member(jsii_name="agencyName")
    def agency_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agencyName"))

    @agency_name.setter
    def agency_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6112aa23746abc78cb660d888c532d834c3612dd362d57d9740f9c5937f365f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agencyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerStrategy")
    def consumer_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerStrategy"))

    @consumer_strategy.setter
    def consumer_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e8e52e787ff15a11b38bb92f219358d96f1f3583c3a06227e743b6a3e44790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deliverTimeInterval")
    def deliver_time_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deliverTimeInterval"))

    @deliver_time_interval.setter
    def deliver_time_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f09ea5ebec723dc10052727fc31eb76df7dd77c9ba832728b3e61ea2a182f70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliverTimeInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationFileType")
    def destination_file_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationFileType"))

    @destination_file_type.setter
    def destination_file_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3945fb4198227ce247276f61cb1ff69471166b2045316c7db21b1e39a09a25fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationFileType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filePrefix")
    def file_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filePrefix"))

    @file_prefix.setter
    def file_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e371cc875c5366e3dd9901505e836468eea8631b502e22b977d7cd8e3bf2c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="obsBucketPath")
    def obs_bucket_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "obsBucketPath"))

    @obs_bucket_path.setter
    def obs_bucket_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98bea537b66b42ccfe59d90ede185f6e18407f078fadd8d5e5e10c45fc1b5744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "obsBucketPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partitionFormat")
    def partition_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partitionFormat"))

    @partition_format.setter
    def partition_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16910d9664e0351066657b7d1002a6702d56c1852f4a4e78ac74ed3d7fc7cfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordDelimiter")
    def record_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordDelimiter"))

    @record_delimiter.setter
    def record_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c466772f730ebd45ac6823bf184f9a4ee2ad9e57569c9f2743d48bea6da1433b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskName")
    def task_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskName"))

    @task_name.setter
    def task_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd99cfb109a94024e33099a3a9daa851f3ce09ff68099b6dc2fbd6d496b71166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DisDumpTaskV2ObsDestinationDescriptor]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DisDumpTaskV2ObsDestinationDescriptor]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DisDumpTaskV2ObsDestinationDescriptor]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e88ef5813120d4930f3f437d89eb615dce1a42019ac90cb0e74c337fe592c6bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.disDumpTaskV2.DisDumpTaskV2ObsProcessingSchema",
    jsii_struct_bases=[],
    name_mapping={
        "timestamp_name": "timestampName",
        "timestamp_type": "timestampType",
        "timestamp_format": "timestampFormat",
    },
)
class DisDumpTaskV2ObsProcessingSchema:
    def __init__(
        self,
        *,
        timestamp_name: builtins.str,
        timestamp_type: builtins.str,
        timestamp_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param timestamp_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#timestamp_name DisDumpTaskV2#timestamp_name}.
        :param timestamp_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#timestamp_type DisDumpTaskV2#timestamp_type}.
        :param timestamp_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#timestamp_format DisDumpTaskV2#timestamp_format}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce65583060cf62ae61820560bc0b03557a55e97f50079cfc9eaa056ee031979b)
            check_type(argname="argument timestamp_name", value=timestamp_name, expected_type=type_hints["timestamp_name"])
            check_type(argname="argument timestamp_type", value=timestamp_type, expected_type=type_hints["timestamp_type"])
            check_type(argname="argument timestamp_format", value=timestamp_format, expected_type=type_hints["timestamp_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "timestamp_name": timestamp_name,
            "timestamp_type": timestamp_type,
        }
        if timestamp_format is not None:
            self._values["timestamp_format"] = timestamp_format

    @builtins.property
    def timestamp_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#timestamp_name DisDumpTaskV2#timestamp_name}.'''
        result = self._values.get("timestamp_name")
        assert result is not None, "Required property 'timestamp_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timestamp_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#timestamp_type DisDumpTaskV2#timestamp_type}.'''
        result = self._values.get("timestamp_type")
        assert result is not None, "Required property 'timestamp_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timestamp_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#timestamp_format DisDumpTaskV2#timestamp_format}.'''
        result = self._values.get("timestamp_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DisDumpTaskV2ObsProcessingSchema(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DisDumpTaskV2ObsProcessingSchemaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.disDumpTaskV2.DisDumpTaskV2ObsProcessingSchemaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80fe4e9b7f641ab84e155eefcae5348611d033a2ba56a4d63100b118662bb45b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DisDumpTaskV2ObsProcessingSchemaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd38def49bd727ef1ab053c0ef44ab62f4ac7485c0d5a63817e2d99b55f03ee3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DisDumpTaskV2ObsProcessingSchemaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc7a43f153526496d261edf8f97e1f7125b5007829c70184612bf3aa734f109)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a357a73fa49098df4b2bf4ef695ae9c956396ac4fc5fdeb5c57229b82a190290)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d6f3068f0a30c0c12e6108f83c8528d914a7eb8e4d751a51461cfe8cfcb88f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DisDumpTaskV2ObsProcessingSchema]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DisDumpTaskV2ObsProcessingSchema]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DisDumpTaskV2ObsProcessingSchema]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25b553d06c5d38e6751facb39aa75627d1d6203c70cfa9dbe600af1d438450e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DisDumpTaskV2ObsProcessingSchemaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.disDumpTaskV2.DisDumpTaskV2ObsProcessingSchemaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fc8668040fb76efbf5830d2cd4f112f131e3be77446e7ae3d2cc0858d5aa0ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetTimestampFormat")
    def reset_timestamp_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestampFormat", []))

    @builtins.property
    @jsii.member(jsii_name="timestampFormatInput")
    def timestamp_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampNameInput")
    def timestamp_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampTypeInput")
    def timestamp_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampFormat")
    def timestamp_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampFormat"))

    @timestamp_format.setter
    def timestamp_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__905e93963f70a2c81d3de6cb3619b94cd048e1a6e864390e277f8a4f701579cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampName")
    def timestamp_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampName"))

    @timestamp_name.setter
    def timestamp_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2be98621159d1e81f94cf7761acb314c382cb65e6f2849fd4950701d49413ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampType")
    def timestamp_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampType"))

    @timestamp_type.setter
    def timestamp_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958726067786bca0ac7bfdc7a74d63adca552a93c6ee7ceabc8ab1b92b0b6c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DisDumpTaskV2ObsProcessingSchema]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DisDumpTaskV2ObsProcessingSchema]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DisDumpTaskV2ObsProcessingSchema]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__541a7b27a88b974bb5847a2abd4eb4e135faffb49f7cb7448181365f007b84b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.disDumpTaskV2.DisDumpTaskV2Partitions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DisDumpTaskV2Partitions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DisDumpTaskV2Partitions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DisDumpTaskV2PartitionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.disDumpTaskV2.DisDumpTaskV2PartitionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b0be29f6ef680f75696b6c9829ac8f2ea67892c0803161ac261c3594647cc61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DisDumpTaskV2PartitionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4d6c1de0b574210ecd6f8b3096fdf37aeb8111151216f4d064d7558f2afb68a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DisDumpTaskV2PartitionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab3d91fb10a9b137feee066976f1f7f1472273ae51a30e840f00c29ef1aa3b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2f4328925f5ee07fe8c5380f44403727f6ceea1bb4de492db54106eb5d5adc6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8542f91379a466952d3be4b410ce88b39b3579097379316e61fcb69120cc3ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DisDumpTaskV2PartitionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.disDumpTaskV2.DisDumpTaskV2PartitionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6afd70ee8bc9adaef9dd36ee2556c0e95a53d6d4effe117f4ee7dfd5c01bebf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hashRange")
    def hash_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hashRange"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="parentPartitions")
    def parent_partitions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentPartitions"))

    @builtins.property
    @jsii.member(jsii_name="sequenceNumberRange")
    def sequence_number_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sequenceNumberRange"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DisDumpTaskV2Partitions]:
        return typing.cast(typing.Optional[DisDumpTaskV2Partitions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DisDumpTaskV2Partitions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb6f262f69a195bcc50fe5aeaff96db8662637553658409718f829412af95ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.disDumpTaskV2.DisDumpTaskV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"update": "update"},
)
class DisDumpTaskV2Timeouts:
    def __init__(self, *, update: typing.Optional[builtins.str] = None) -> None:
        '''
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#update DisDumpTaskV2#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc63570017787bcc793f1ed1362e5061ad7dc408835b3b3c141380cd1752dbbd)
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dis_dump_task_v2#update DisDumpTaskV2#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DisDumpTaskV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DisDumpTaskV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.disDumpTaskV2.DisDumpTaskV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42bb5a65bf172700233ef1d48e1e8bc11b2a5564acefabfea2084f1e0e5317cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8afb5d85fd546faed911134c4ef6d175eaa821e1aa0652281411f176ae04af6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DisDumpTaskV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DisDumpTaskV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DisDumpTaskV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c5665fcb8850a45aa4ecab658a2243c3819793804772fac8112fbbaada4435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DisDumpTaskV2",
    "DisDumpTaskV2Config",
    "DisDumpTaskV2ObsDestinationDescriptor",
    "DisDumpTaskV2ObsDestinationDescriptorList",
    "DisDumpTaskV2ObsDestinationDescriptorOutputReference",
    "DisDumpTaskV2ObsProcessingSchema",
    "DisDumpTaskV2ObsProcessingSchemaList",
    "DisDumpTaskV2ObsProcessingSchemaOutputReference",
    "DisDumpTaskV2Partitions",
    "DisDumpTaskV2PartitionsList",
    "DisDumpTaskV2PartitionsOutputReference",
    "DisDumpTaskV2Timeouts",
    "DisDumpTaskV2TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__99c4aea751ca0f8dbebdc185cb672ab054c673243143a90af23c9d00c3b74dc7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    stream_name: builtins.str,
    action: typing.Optional[builtins.str] = None,
    destination: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    obs_destination_descriptor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DisDumpTaskV2ObsDestinationDescriptor, typing.Dict[builtins.str, typing.Any]]]]] = None,
    obs_processing_schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DisDumpTaskV2ObsProcessingSchema, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[DisDumpTaskV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__0d707a2692e9d631ae1c339d7501941a86c0a9efed951a7e1cf0b45cb2d19060(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876db20e2a517ca5f4719e20c6b4e54642fc4349aa33004a4be81076ddf7f985(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DisDumpTaskV2ObsDestinationDescriptor, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e2de63a55eab5e1a00aaaf93f46857b5d235e2ef9231c467a3f00443d22a31(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DisDumpTaskV2ObsProcessingSchema, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e961b62c02303f39a15fae86c7c5b955d118b3c07dc78356d433da8efd83d74c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb91c6a20472cb7435f27c80428e403fd289e86c6117c6e74b5e23f5c7dd90a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__999004f80bfd33230705c3bb9f53660f183e9367d500b6530a29328fe6836ca0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd97f8dd6e85663e38fe24aeb9e658ae2565efd45d2e6352784ba52fa7d2409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e4a727944ccca2eb0e51824c0cff355ce6250caa2e55b6037b9652fd2d09b4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stream_name: builtins.str,
    action: typing.Optional[builtins.str] = None,
    destination: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    obs_destination_descriptor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DisDumpTaskV2ObsDestinationDescriptor, typing.Dict[builtins.str, typing.Any]]]]] = None,
    obs_processing_schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DisDumpTaskV2ObsProcessingSchema, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[DisDumpTaskV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10bec956236826d70cca0e72ca127216388f2a937260c4569ef093e2b1659726(
    *,
    agency_name: builtins.str,
    deliver_time_interval: jsii.Number,
    obs_bucket_path: builtins.str,
    task_name: builtins.str,
    consumer_strategy: typing.Optional[builtins.str] = None,
    destination_file_type: typing.Optional[builtins.str] = None,
    file_prefix: typing.Optional[builtins.str] = None,
    partition_format: typing.Optional[builtins.str] = None,
    record_delimiter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d29de1530348e0921841b47d7d4fa8d732cfe117e5b3a31adb75a207f9d1ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00875446ce439c1ffb3bd1ce377950726ae5edd59b8d3c0ca1e2264875d88c60(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8518c6fafea8c6bf21f1e8317b6effa6b5ade0217b06384e276987cdecbaf48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b732f237ef4598a5457fcab4a9a0caf6889d80a50a01763e329d984d14b80e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696849da724e213d4ec030ce69e8e5255000c54c85ab94598a6c5bd969e02569(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0d97cfc7a917eba323548d08752b7ea7e8dd4824f98b64313452692910935d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DisDumpTaskV2ObsDestinationDescriptor]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c48119310be83f8b4e9da1fd616feb6c38744c8b7cdaf96bca8df3603c10f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6112aa23746abc78cb660d888c532d834c3612dd362d57d9740f9c5937f365f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e8e52e787ff15a11b38bb92f219358d96f1f3583c3a06227e743b6a3e44790(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f09ea5ebec723dc10052727fc31eb76df7dd77c9ba832728b3e61ea2a182f70(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3945fb4198227ce247276f61cb1ff69471166b2045316c7db21b1e39a09a25fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e371cc875c5366e3dd9901505e836468eea8631b502e22b977d7cd8e3bf2c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98bea537b66b42ccfe59d90ede185f6e18407f078fadd8d5e5e10c45fc1b5744(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16910d9664e0351066657b7d1002a6702d56c1852f4a4e78ac74ed3d7fc7cfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c466772f730ebd45ac6823bf184f9a4ee2ad9e57569c9f2743d48bea6da1433b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd99cfb109a94024e33099a3a9daa851f3ce09ff68099b6dc2fbd6d496b71166(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e88ef5813120d4930f3f437d89eb615dce1a42019ac90cb0e74c337fe592c6bb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DisDumpTaskV2ObsDestinationDescriptor]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce65583060cf62ae61820560bc0b03557a55e97f50079cfc9eaa056ee031979b(
    *,
    timestamp_name: builtins.str,
    timestamp_type: builtins.str,
    timestamp_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80fe4e9b7f641ab84e155eefcae5348611d033a2ba56a4d63100b118662bb45b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd38def49bd727ef1ab053c0ef44ab62f4ac7485c0d5a63817e2d99b55f03ee3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc7a43f153526496d261edf8f97e1f7125b5007829c70184612bf3aa734f109(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a357a73fa49098df4b2bf4ef695ae9c956396ac4fc5fdeb5c57229b82a190290(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d6f3068f0a30c0c12e6108f83c8528d914a7eb8e4d751a51461cfe8cfcb88f1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b553d06c5d38e6751facb39aa75627d1d6203c70cfa9dbe600af1d438450e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DisDumpTaskV2ObsProcessingSchema]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc8668040fb76efbf5830d2cd4f112f131e3be77446e7ae3d2cc0858d5aa0ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905e93963f70a2c81d3de6cb3619b94cd048e1a6e864390e277f8a4f701579cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2be98621159d1e81f94cf7761acb314c382cb65e6f2849fd4950701d49413ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958726067786bca0ac7bfdc7a74d63adca552a93c6ee7ceabc8ab1b92b0b6c0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__541a7b27a88b974bb5847a2abd4eb4e135faffb49f7cb7448181365f007b84b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DisDumpTaskV2ObsProcessingSchema]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b0be29f6ef680f75696b6c9829ac8f2ea67892c0803161ac261c3594647cc61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d6c1de0b574210ecd6f8b3096fdf37aeb8111151216f4d064d7558f2afb68a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab3d91fb10a9b137feee066976f1f7f1472273ae51a30e840f00c29ef1aa3b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f4328925f5ee07fe8c5380f44403727f6ceea1bb4de492db54106eb5d5adc6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8542f91379a466952d3be4b410ce88b39b3579097379316e61fcb69120cc3ae(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6afd70ee8bc9adaef9dd36ee2556c0e95a53d6d4effe117f4ee7dfd5c01bebf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb6f262f69a195bcc50fe5aeaff96db8662637553658409718f829412af95ab(
    value: typing.Optional[DisDumpTaskV2Partitions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc63570017787bcc793f1ed1362e5061ad7dc408835b3b3c141380cd1752dbbd(
    *,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42bb5a65bf172700233ef1d48e1e8bc11b2a5564acefabfea2084f1e0e5317cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8afb5d85fd546faed911134c4ef6d175eaa821e1aa0652281411f176ae04af6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c5665fcb8850a45aa4ecab658a2243c3819793804772fac8112fbbaada4435(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DisDumpTaskV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

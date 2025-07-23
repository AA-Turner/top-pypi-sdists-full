r'''
# `google_data_loss_prevention_job_trigger`

Refer to the Terraform Registry for docs: [`google_data_loss_prevention_job_trigger`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger).
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


class DataLossPreventionJobTrigger(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTrigger",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger google_data_loss_prevention_job_trigger}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        parent: builtins.str,
        triggers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerTriggers", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inspect_job: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJob", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataLossPreventionJobTriggerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trigger_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger google_data_loss_prevention_job_trigger} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param parent: The parent of the trigger, either in the format 'projects/{{project}}' or 'projects/{{project}}/locations/{{location}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#parent DataLossPreventionJobTrigger#parent}
        :param triggers: triggers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#triggers DataLossPreventionJobTrigger#triggers}
        :param description: A description of the job trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#description DataLossPreventionJobTrigger#description}
        :param display_name: User set display name of the job trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#display_name DataLossPreventionJobTrigger#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#id DataLossPreventionJobTrigger#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inspect_job: inspect_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#inspect_job DataLossPreventionJobTrigger#inspect_job}
        :param status: Whether the trigger is currently active. Default value: "HEALTHY" Possible values: ["PAUSED", "HEALTHY", "CANCELLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#status DataLossPreventionJobTrigger#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#timeouts DataLossPreventionJobTrigger#timeouts}
        :param trigger_id: The trigger id can contain uppercase and lowercase letters, numbers, and hyphens; that is, it must match the regular expression: [a-zA-Z\\d-_]+. The maximum length is 100 characters. Can be empty to allow the system to generate one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#trigger_id DataLossPreventionJobTrigger#trigger_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2de68c15e704db02a281360b0daa8843a0d3b0060998cb1004bfb2c9904bf02)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataLossPreventionJobTriggerConfig(
            parent=parent,
            triggers=triggers,
            description=description,
            display_name=display_name,
            id=id,
            inspect_job=inspect_job,
            status=status,
            timeouts=timeouts,
            trigger_id=trigger_id,
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
        '''Generates CDKTF code for importing a DataLossPreventionJobTrigger resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataLossPreventionJobTrigger to import.
        :param import_from_id: The id of the existing DataLossPreventionJobTrigger that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataLossPreventionJobTrigger to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e6df625f19efc8d21266dca525a377a2ac5ce09f598b4c01e9db9126453002)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putInspectJob")
    def put_inspect_job(
        self,
        *,
        storage_config: typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfig", typing.Dict[builtins.str, typing.Any]],
        actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerInspectJobActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inspect_config: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        inspect_template_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param storage_config: storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#storage_config DataLossPreventionJobTrigger#storage_config}
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#actions DataLossPreventionJobTrigger#actions}
        :param inspect_config: inspect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#inspect_config DataLossPreventionJobTrigger#inspect_config}
        :param inspect_template_name: The name of the template to run when this job is triggered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#inspect_template_name DataLossPreventionJobTrigger#inspect_template_name}
        '''
        value = DataLossPreventionJobTriggerInspectJob(
            storage_config=storage_config,
            actions=actions,
            inspect_config=inspect_config,
            inspect_template_name=inspect_template_name,
        )

        return typing.cast(None, jsii.invoke(self, "putInspectJob", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#create DataLossPreventionJobTrigger#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#delete DataLossPreventionJobTrigger#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#update DataLossPreventionJobTrigger#update}.
        '''
        value = DataLossPreventionJobTriggerTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTriggers")
    def put_triggers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerTriggers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d09f9a0e81d65307ffcc19aa6865392920fd83ddbd0efc39109df17525f670b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTriggers", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInspectJob")
    def reset_inspect_job(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInspectJob", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTriggerId")
    def reset_trigger_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerId", []))

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
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="inspectJob")
    def inspect_job(self) -> "DataLossPreventionJobTriggerInspectJobOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobOutputReference", jsii.get(self, "inspectJob"))

    @builtins.property
    @jsii.member(jsii_name="lastRunTime")
    def last_run_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastRunTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataLossPreventionJobTriggerTimeoutsOutputReference":
        return typing.cast("DataLossPreventionJobTriggerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(self) -> "DataLossPreventionJobTriggerTriggersList":
        return typing.cast("DataLossPreventionJobTriggerTriggersList", jsii.get(self, "triggers"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inspectJobInput")
    def inspect_job_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJob"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJob"], jsii.get(self, "inspectJobInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataLossPreventionJobTriggerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataLossPreventionJobTriggerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerIdInput")
    def trigger_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="triggersInput")
    def triggers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerTriggers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerTriggers"]]], jsii.get(self, "triggersInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a060f046683b9cc93f4a82126c667f72d6dad7f1d997824df466bd387a810376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3912011ca0a1c7991d40ce71419582aaf28a01945df192d080a4c500adc0c30f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4b2854cdc644c034c208a0c0e28abe3bd8c029962c43debb4ed009236059bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e5cc32336570cc709e9f24e04b6f0da11d805b8ed74af81ca86ac876851a22a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ee0c3177da98457226086948b7fba521ffbf7c187e8258d5056db76336dbed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerId")
    def trigger_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerId"))

    @trigger_id.setter
    def trigger_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0fc7276d58af303e6513224ea5157e9b25f77768a6cef104642755729ef6a83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "parent": "parent",
        "triggers": "triggers",
        "description": "description",
        "display_name": "displayName",
        "id": "id",
        "inspect_job": "inspectJob",
        "status": "status",
        "timeouts": "timeouts",
        "trigger_id": "triggerId",
    },
)
class DataLossPreventionJobTriggerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        parent: builtins.str,
        triggers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerTriggers", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inspect_job: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJob", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataLossPreventionJobTriggerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trigger_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param parent: The parent of the trigger, either in the format 'projects/{{project}}' or 'projects/{{project}}/locations/{{location}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#parent DataLossPreventionJobTrigger#parent}
        :param triggers: triggers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#triggers DataLossPreventionJobTrigger#triggers}
        :param description: A description of the job trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#description DataLossPreventionJobTrigger#description}
        :param display_name: User set display name of the job trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#display_name DataLossPreventionJobTrigger#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#id DataLossPreventionJobTrigger#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inspect_job: inspect_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#inspect_job DataLossPreventionJobTrigger#inspect_job}
        :param status: Whether the trigger is currently active. Default value: "HEALTHY" Possible values: ["PAUSED", "HEALTHY", "CANCELLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#status DataLossPreventionJobTrigger#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#timeouts DataLossPreventionJobTrigger#timeouts}
        :param trigger_id: The trigger id can contain uppercase and lowercase letters, numbers, and hyphens; that is, it must match the regular expression: [a-zA-Z\\d-_]+. The maximum length is 100 characters. Can be empty to allow the system to generate one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#trigger_id DataLossPreventionJobTrigger#trigger_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(inspect_job, dict):
            inspect_job = DataLossPreventionJobTriggerInspectJob(**inspect_job)
        if isinstance(timeouts, dict):
            timeouts = DataLossPreventionJobTriggerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78584e8541d89523b731062903f4ef4d89e7f8d8513bea3343d48c12706bfcc7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument triggers", value=triggers, expected_type=type_hints["triggers"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inspect_job", value=inspect_job, expected_type=type_hints["inspect_job"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument trigger_id", value=trigger_id, expected_type=type_hints["trigger_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parent": parent,
            "triggers": triggers,
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
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if inspect_job is not None:
            self._values["inspect_job"] = inspect_job
        if status is not None:
            self._values["status"] = status
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if trigger_id is not None:
            self._values["trigger_id"] = trigger_id

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
    def parent(self) -> builtins.str:
        '''The parent of the trigger, either in the format 'projects/{{project}}' or 'projects/{{project}}/locations/{{location}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#parent DataLossPreventionJobTrigger#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def triggers(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerTriggers"]]:
        '''triggers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#triggers DataLossPreventionJobTrigger#triggers}
        '''
        result = self._values.get("triggers")
        assert result is not None, "Required property 'triggers' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerTriggers"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the job trigger.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#description DataLossPreventionJobTrigger#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User set display name of the job trigger.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#display_name DataLossPreventionJobTrigger#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#id DataLossPreventionJobTrigger#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inspect_job(self) -> typing.Optional["DataLossPreventionJobTriggerInspectJob"]:
        '''inspect_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#inspect_job DataLossPreventionJobTrigger#inspect_job}
        '''
        result = self._values.get("inspect_job")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJob"], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Whether the trigger is currently active. Default value: "HEALTHY" Possible values: ["PAUSED", "HEALTHY", "CANCELLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#status DataLossPreventionJobTrigger#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataLossPreventionJobTriggerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#timeouts DataLossPreventionJobTrigger#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerTimeouts"], result)

    @builtins.property
    def trigger_id(self) -> typing.Optional[builtins.str]:
        '''The trigger id can contain uppercase and lowercase letters, numbers, and hyphens;

        that is, it must match the regular expression: [a-zA-Z\\d-_]+.
        The maximum length is 100 characters. Can be empty to allow the system to generate one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#trigger_id DataLossPreventionJobTrigger#trigger_id}
        '''
        result = self._values.get("trigger_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJob",
    jsii_struct_bases=[],
    name_mapping={
        "storage_config": "storageConfig",
        "actions": "actions",
        "inspect_config": "inspectConfig",
        "inspect_template_name": "inspectTemplateName",
    },
)
class DataLossPreventionJobTriggerInspectJob:
    def __init__(
        self,
        *,
        storage_config: typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfig", typing.Dict[builtins.str, typing.Any]],
        actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerInspectJobActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inspect_config: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        inspect_template_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param storage_config: storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#storage_config DataLossPreventionJobTrigger#storage_config}
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#actions DataLossPreventionJobTrigger#actions}
        :param inspect_config: inspect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#inspect_config DataLossPreventionJobTrigger#inspect_config}
        :param inspect_template_name: The name of the template to run when this job is triggered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#inspect_template_name DataLossPreventionJobTrigger#inspect_template_name}
        '''
        if isinstance(storage_config, dict):
            storage_config = DataLossPreventionJobTriggerInspectJobStorageConfig(**storage_config)
        if isinstance(inspect_config, dict):
            inspect_config = DataLossPreventionJobTriggerInspectJobInspectConfig(**inspect_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d7084810c2287a4aa781be8c49bd54020126ca4ad27659fa785ef2b612b1642)
            check_type(argname="argument storage_config", value=storage_config, expected_type=type_hints["storage_config"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument inspect_config", value=inspect_config, expected_type=type_hints["inspect_config"])
            check_type(argname="argument inspect_template_name", value=inspect_template_name, expected_type=type_hints["inspect_template_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "storage_config": storage_config,
        }
        if actions is not None:
            self._values["actions"] = actions
        if inspect_config is not None:
            self._values["inspect_config"] = inspect_config
        if inspect_template_name is not None:
            self._values["inspect_template_name"] = inspect_template_name

    @builtins.property
    def storage_config(self) -> "DataLossPreventionJobTriggerInspectJobStorageConfig":
        '''storage_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#storage_config DataLossPreventionJobTrigger#storage_config}
        '''
        result = self._values.get("storage_config")
        assert result is not None, "Required property 'storage_config' is missing"
        return typing.cast("DataLossPreventionJobTriggerInspectJobStorageConfig", result)

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobActions"]]]:
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#actions DataLossPreventionJobTrigger#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobActions"]]], result)

    @builtins.property
    def inspect_config(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfig"]:
        '''inspect_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#inspect_config DataLossPreventionJobTrigger#inspect_config}
        '''
        result = self._values.get("inspect_config")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfig"], result)

    @builtins.property
    def inspect_template_name(self) -> typing.Optional[builtins.str]:
        '''The name of the template to run when this job is triggered.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#inspect_template_name DataLossPreventionJobTrigger#inspect_template_name}
        '''
        result = self._values.get("inspect_template_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActions",
    jsii_struct_bases=[],
    name_mapping={
        "deidentify": "deidentify",
        "job_notification_emails": "jobNotificationEmails",
        "publish_findings_to_cloud_data_catalog": "publishFindingsToCloudDataCatalog",
        "publish_summary_to_cscc": "publishSummaryToCscc",
        "publish_to_stackdriver": "publishToStackdriver",
        "pub_sub": "pubSub",
        "save_findings": "saveFindings",
    },
)
class DataLossPreventionJobTriggerInspectJobActions:
    def __init__(
        self,
        *,
        deidentify: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobActionsDeidentify", typing.Dict[builtins.str, typing.Any]]] = None,
        job_notification_emails: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails", typing.Dict[builtins.str, typing.Any]]] = None,
        publish_findings_to_cloud_data_catalog: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog", typing.Dict[builtins.str, typing.Any]]] = None,
        publish_summary_to_cscc: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc", typing.Dict[builtins.str, typing.Any]]] = None,
        publish_to_stackdriver: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver", typing.Dict[builtins.str, typing.Any]]] = None,
        pub_sub: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobActionsPubSub", typing.Dict[builtins.str, typing.Any]]] = None,
        save_findings: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobActionsSaveFindings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param deidentify: deidentify block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#deidentify DataLossPreventionJobTrigger#deidentify}
        :param job_notification_emails: job_notification_emails block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#job_notification_emails DataLossPreventionJobTrigger#job_notification_emails}
        :param publish_findings_to_cloud_data_catalog: publish_findings_to_cloud_data_catalog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#publish_findings_to_cloud_data_catalog DataLossPreventionJobTrigger#publish_findings_to_cloud_data_catalog}
        :param publish_summary_to_cscc: publish_summary_to_cscc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#publish_summary_to_cscc DataLossPreventionJobTrigger#publish_summary_to_cscc}
        :param publish_to_stackdriver: publish_to_stackdriver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#publish_to_stackdriver DataLossPreventionJobTrigger#publish_to_stackdriver}
        :param pub_sub: pub_sub block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#pub_sub DataLossPreventionJobTrigger#pub_sub}
        :param save_findings: save_findings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#save_findings DataLossPreventionJobTrigger#save_findings}
        '''
        if isinstance(deidentify, dict):
            deidentify = DataLossPreventionJobTriggerInspectJobActionsDeidentify(**deidentify)
        if isinstance(job_notification_emails, dict):
            job_notification_emails = DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails(**job_notification_emails)
        if isinstance(publish_findings_to_cloud_data_catalog, dict):
            publish_findings_to_cloud_data_catalog = DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog(**publish_findings_to_cloud_data_catalog)
        if isinstance(publish_summary_to_cscc, dict):
            publish_summary_to_cscc = DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc(**publish_summary_to_cscc)
        if isinstance(publish_to_stackdriver, dict):
            publish_to_stackdriver = DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver(**publish_to_stackdriver)
        if isinstance(pub_sub, dict):
            pub_sub = DataLossPreventionJobTriggerInspectJobActionsPubSub(**pub_sub)
        if isinstance(save_findings, dict):
            save_findings = DataLossPreventionJobTriggerInspectJobActionsSaveFindings(**save_findings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc051f2469caac11e7267bb13475c1adc0a510db0e95fd826a2ca9f5ffc6a3da)
            check_type(argname="argument deidentify", value=deidentify, expected_type=type_hints["deidentify"])
            check_type(argname="argument job_notification_emails", value=job_notification_emails, expected_type=type_hints["job_notification_emails"])
            check_type(argname="argument publish_findings_to_cloud_data_catalog", value=publish_findings_to_cloud_data_catalog, expected_type=type_hints["publish_findings_to_cloud_data_catalog"])
            check_type(argname="argument publish_summary_to_cscc", value=publish_summary_to_cscc, expected_type=type_hints["publish_summary_to_cscc"])
            check_type(argname="argument publish_to_stackdriver", value=publish_to_stackdriver, expected_type=type_hints["publish_to_stackdriver"])
            check_type(argname="argument pub_sub", value=pub_sub, expected_type=type_hints["pub_sub"])
            check_type(argname="argument save_findings", value=save_findings, expected_type=type_hints["save_findings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deidentify is not None:
            self._values["deidentify"] = deidentify
        if job_notification_emails is not None:
            self._values["job_notification_emails"] = job_notification_emails
        if publish_findings_to_cloud_data_catalog is not None:
            self._values["publish_findings_to_cloud_data_catalog"] = publish_findings_to_cloud_data_catalog
        if publish_summary_to_cscc is not None:
            self._values["publish_summary_to_cscc"] = publish_summary_to_cscc
        if publish_to_stackdriver is not None:
            self._values["publish_to_stackdriver"] = publish_to_stackdriver
        if pub_sub is not None:
            self._values["pub_sub"] = pub_sub
        if save_findings is not None:
            self._values["save_findings"] = save_findings

    @builtins.property
    def deidentify(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsDeidentify"]:
        '''deidentify block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#deidentify DataLossPreventionJobTrigger#deidentify}
        '''
        result = self._values.get("deidentify")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsDeidentify"], result)

    @builtins.property
    def job_notification_emails(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails"]:
        '''job_notification_emails block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#job_notification_emails DataLossPreventionJobTrigger#job_notification_emails}
        '''
        result = self._values.get("job_notification_emails")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails"], result)

    @builtins.property
    def publish_findings_to_cloud_data_catalog(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog"]:
        '''publish_findings_to_cloud_data_catalog block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#publish_findings_to_cloud_data_catalog DataLossPreventionJobTrigger#publish_findings_to_cloud_data_catalog}
        '''
        result = self._values.get("publish_findings_to_cloud_data_catalog")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog"], result)

    @builtins.property
    def publish_summary_to_cscc(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc"]:
        '''publish_summary_to_cscc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#publish_summary_to_cscc DataLossPreventionJobTrigger#publish_summary_to_cscc}
        '''
        result = self._values.get("publish_summary_to_cscc")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc"], result)

    @builtins.property
    def publish_to_stackdriver(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver"]:
        '''publish_to_stackdriver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#publish_to_stackdriver DataLossPreventionJobTrigger#publish_to_stackdriver}
        '''
        result = self._values.get("publish_to_stackdriver")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver"], result)

    @builtins.property
    def pub_sub(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsPubSub"]:
        '''pub_sub block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#pub_sub DataLossPreventionJobTrigger#pub_sub}
        '''
        result = self._values.get("pub_sub")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsPubSub"], result)

    @builtins.property
    def save_findings(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsSaveFindings"]:
        '''save_findings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#save_findings DataLossPreventionJobTrigger#save_findings}
        '''
        result = self._values.get("save_findings")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsSaveFindings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsDeidentify",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_storage_output": "cloudStorageOutput",
        "file_types_to_transform": "fileTypesToTransform",
        "transformation_config": "transformationConfig",
        "transformation_details_storage_config": "transformationDetailsStorageConfig",
    },
)
class DataLossPreventionJobTriggerInspectJobActionsDeidentify:
    def __init__(
        self,
        *,
        cloud_storage_output: builtins.str,
        file_types_to_transform: typing.Optional[typing.Sequence[builtins.str]] = None,
        transformation_config: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        transformation_details_storage_config: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_output: User settable Cloud Storage bucket and folders to store de-identified files. This field must be set for cloud storage deidentification. The output Cloud Storage bucket must be different from the input bucket. De-identified files will overwrite files in the output path. Form of: gs://bucket/folder/ or gs://bucket Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#cloud_storage_output DataLossPreventionJobTrigger#cloud_storage_output}
        :param file_types_to_transform: List of user-specified file type groups to transform. If specified, only the files with these filetypes will be transformed. If empty, all supported files will be transformed. Supported types may be automatically added over time. If a file type is set in this field that isn't supported by the Deidentify action then the job will fail and will not be successfully created/started. Possible values: ["IMAGE", "TEXT_FILE", "CSV", "TSV"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#file_types_to_transform DataLossPreventionJobTrigger#file_types_to_transform}
        :param transformation_config: transformation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#transformation_config DataLossPreventionJobTrigger#transformation_config}
        :param transformation_details_storage_config: transformation_details_storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#transformation_details_storage_config DataLossPreventionJobTrigger#transformation_details_storage_config}
        '''
        if isinstance(transformation_config, dict):
            transformation_config = DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig(**transformation_config)
        if isinstance(transformation_details_storage_config, dict):
            transformation_details_storage_config = DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig(**transformation_details_storage_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6255ccee82f3ce68feaa16b44bc65af157a7a3532bfbf4bee6be8afb22dd512b)
            check_type(argname="argument cloud_storage_output", value=cloud_storage_output, expected_type=type_hints["cloud_storage_output"])
            check_type(argname="argument file_types_to_transform", value=file_types_to_transform, expected_type=type_hints["file_types_to_transform"])
            check_type(argname="argument transformation_config", value=transformation_config, expected_type=type_hints["transformation_config"])
            check_type(argname="argument transformation_details_storage_config", value=transformation_details_storage_config, expected_type=type_hints["transformation_details_storage_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_storage_output": cloud_storage_output,
        }
        if file_types_to_transform is not None:
            self._values["file_types_to_transform"] = file_types_to_transform
        if transformation_config is not None:
            self._values["transformation_config"] = transformation_config
        if transformation_details_storage_config is not None:
            self._values["transformation_details_storage_config"] = transformation_details_storage_config

    @builtins.property
    def cloud_storage_output(self) -> builtins.str:
        '''User settable Cloud Storage bucket and folders to store de-identified files.

        This field must be set for cloud storage deidentification.

        The output Cloud Storage bucket must be different from the input bucket.

        De-identified files will overwrite files in the output path.

        Form of: gs://bucket/folder/ or gs://bucket

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#cloud_storage_output DataLossPreventionJobTrigger#cloud_storage_output}
        '''
        result = self._values.get("cloud_storage_output")
        assert result is not None, "Required property 'cloud_storage_output' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def file_types_to_transform(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of user-specified file type groups to transform. If specified, only the files with these filetypes will be transformed.

        If empty, all supported files will be transformed. Supported types may be automatically added over time.

        If a file type is set in this field that isn't supported by the Deidentify action then the job will fail and will not be successfully created/started. Possible values: ["IMAGE", "TEXT_FILE", "CSV", "TSV"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#file_types_to_transform DataLossPreventionJobTrigger#file_types_to_transform}
        '''
        result = self._values.get("file_types_to_transform")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def transformation_config(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig"]:
        '''transformation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#transformation_config DataLossPreventionJobTrigger#transformation_config}
        '''
        result = self._values.get("transformation_config")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig"], result)

    @builtins.property
    def transformation_details_storage_config(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig"]:
        '''transformation_details_storage_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#transformation_details_storage_config DataLossPreventionJobTrigger#transformation_details_storage_config}
        '''
        result = self._values.get("transformation_details_storage_config")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobActionsDeidentify(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobActionsDeidentifyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsDeidentifyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6952de99d9993ef7d25d3c5c599c4258ab6d93e00e5db5abeab8cddf96c759f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTransformationConfig")
    def put_transformation_config(
        self,
        *,
        deidentify_template: typing.Optional[builtins.str] = None,
        image_redact_template: typing.Optional[builtins.str] = None,
        structured_deidentify_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deidentify_template: If this template is specified, it will serve as the default de-identify template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#deidentify_template DataLossPreventionJobTrigger#deidentify_template}
        :param image_redact_template: If this template is specified, it will serve as the de-identify template for images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#image_redact_template DataLossPreventionJobTrigger#image_redact_template}
        :param structured_deidentify_template: If this template is specified, it will serve as the de-identify template for structured content such as delimited files and tables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#structured_deidentify_template DataLossPreventionJobTrigger#structured_deidentify_template}
        '''
        value = DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig(
            deidentify_template=deidentify_template,
            image_redact_template=image_redact_template,
            structured_deidentify_template=structured_deidentify_template,
        )

        return typing.cast(None, jsii.invoke(self, "putTransformationConfig", [value]))

    @jsii.member(jsii_name="putTransformationDetailsStorageConfig")
    def put_transformation_details_storage_config(
        self,
        *,
        table: typing.Union["DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param table: table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table DataLossPreventionJobTrigger#table}
        '''
        value = DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig(
            table=table
        )

        return typing.cast(None, jsii.invoke(self, "putTransformationDetailsStorageConfig", [value]))

    @jsii.member(jsii_name="resetFileTypesToTransform")
    def reset_file_types_to_transform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileTypesToTransform", []))

    @jsii.member(jsii_name="resetTransformationConfig")
    def reset_transformation_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransformationConfig", []))

    @jsii.member(jsii_name="resetTransformationDetailsStorageConfig")
    def reset_transformation_details_storage_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransformationDetailsStorageConfig", []))

    @builtins.property
    @jsii.member(jsii_name="transformationConfig")
    def transformation_config(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfigOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfigOutputReference", jsii.get(self, "transformationConfig"))

    @builtins.property
    @jsii.member(jsii_name="transformationDetailsStorageConfig")
    def transformation_details_storage_config(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigOutputReference", jsii.get(self, "transformationDetailsStorageConfig"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageOutputInput")
    def cloud_storage_output_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudStorageOutputInput"))

    @builtins.property
    @jsii.member(jsii_name="fileTypesToTransformInput")
    def file_types_to_transform_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fileTypesToTransformInput"))

    @builtins.property
    @jsii.member(jsii_name="transformationConfigInput")
    def transformation_config_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig"], jsii.get(self, "transformationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="transformationDetailsStorageConfigInput")
    def transformation_details_storage_config_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig"], jsii.get(self, "transformationDetailsStorageConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageOutput")
    def cloud_storage_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudStorageOutput"))

    @cloud_storage_output.setter
    def cloud_storage_output(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4509b34996e40672552cdd779868503f1358734ec5c0a988c22c563834d8311b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudStorageOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileTypesToTransform")
    def file_types_to_transform(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileTypesToTransform"))

    @file_types_to_transform.setter
    def file_types_to_transform(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ccf1fae7d3602eb49f0b3f9e6ac1984aa638df547c4e8bae691c04b1f0639c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileTypesToTransform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentify]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentify], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentify],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1396c3f5cda9da36c12593dc069d20ffc772807e2b6cdefc75e3f1884930fa78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "deidentify_template": "deidentifyTemplate",
        "image_redact_template": "imageRedactTemplate",
        "structured_deidentify_template": "structuredDeidentifyTemplate",
    },
)
class DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig:
    def __init__(
        self,
        *,
        deidentify_template: typing.Optional[builtins.str] = None,
        image_redact_template: typing.Optional[builtins.str] = None,
        structured_deidentify_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deidentify_template: If this template is specified, it will serve as the default de-identify template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#deidentify_template DataLossPreventionJobTrigger#deidentify_template}
        :param image_redact_template: If this template is specified, it will serve as the de-identify template for images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#image_redact_template DataLossPreventionJobTrigger#image_redact_template}
        :param structured_deidentify_template: If this template is specified, it will serve as the de-identify template for structured content such as delimited files and tables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#structured_deidentify_template DataLossPreventionJobTrigger#structured_deidentify_template}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf38e329e3b87997c12dfd2097a8dd5b2cf9462529037b97cbc6b23fd2544106)
            check_type(argname="argument deidentify_template", value=deidentify_template, expected_type=type_hints["deidentify_template"])
            check_type(argname="argument image_redact_template", value=image_redact_template, expected_type=type_hints["image_redact_template"])
            check_type(argname="argument structured_deidentify_template", value=structured_deidentify_template, expected_type=type_hints["structured_deidentify_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deidentify_template is not None:
            self._values["deidentify_template"] = deidentify_template
        if image_redact_template is not None:
            self._values["image_redact_template"] = image_redact_template
        if structured_deidentify_template is not None:
            self._values["structured_deidentify_template"] = structured_deidentify_template

    @builtins.property
    def deidentify_template(self) -> typing.Optional[builtins.str]:
        '''If this template is specified, it will serve as the default de-identify template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#deidentify_template DataLossPreventionJobTrigger#deidentify_template}
        '''
        result = self._values.get("deidentify_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_redact_template(self) -> typing.Optional[builtins.str]:
        '''If this template is specified, it will serve as the de-identify template for images.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#image_redact_template DataLossPreventionJobTrigger#image_redact_template}
        '''
        result = self._values.get("image_redact_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def structured_deidentify_template(self) -> typing.Optional[builtins.str]:
        '''If this template is specified, it will serve as the de-identify template for structured content such as delimited files and tables.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#structured_deidentify_template DataLossPreventionJobTrigger#structured_deidentify_template}
        '''
        result = self._values.get("structured_deidentify_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0a6bf2b452a8279fb51038de593d1497a95040e53b3f60a24df88b0794fe8c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDeidentifyTemplate")
    def reset_deidentify_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeidentifyTemplate", []))

    @jsii.member(jsii_name="resetImageRedactTemplate")
    def reset_image_redact_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageRedactTemplate", []))

    @jsii.member(jsii_name="resetStructuredDeidentifyTemplate")
    def reset_structured_deidentify_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStructuredDeidentifyTemplate", []))

    @builtins.property
    @jsii.member(jsii_name="deidentifyTemplateInput")
    def deidentify_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deidentifyTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="imageRedactTemplateInput")
    def image_redact_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageRedactTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="structuredDeidentifyTemplateInput")
    def structured_deidentify_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "structuredDeidentifyTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="deidentifyTemplate")
    def deidentify_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deidentifyTemplate"))

    @deidentify_template.setter
    def deidentify_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62cfd9e7fc1c34c8226f391a395930aa79a3d93e77dcdf341c05024d3da826f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deidentifyTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageRedactTemplate")
    def image_redact_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageRedactTemplate"))

    @image_redact_template.setter
    def image_redact_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1768ccb2038297b5774a23d689c724903aa302edd3b43a89ee6c4990fb629c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageRedactTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="structuredDeidentifyTemplate")
    def structured_deidentify_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "structuredDeidentifyTemplate"))

    @structured_deidentify_template.setter
    def structured_deidentify_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9c290057d8fe5fa7f0a47d3a83b2c3a9cfb40ad9a897f8e5fdcd4a2fa98ee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "structuredDeidentifyTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3751f5b18c270c31103c4c9f34c39e01713459d518776688c4ce96a518ca3c01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig",
    jsii_struct_bases=[],
    name_mapping={"table": "table"},
)
class DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig:
    def __init__(
        self,
        *,
        table: typing.Union["DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param table: table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table DataLossPreventionJobTrigger#table}
        '''
        if isinstance(table, dict):
            table = DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable(**table)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66020fd3ace64c52fd4b2ce24de77f6eeb66e4bc849271465f537142a09b64bd)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table": table,
        }

    @builtins.property
    def table(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable":
        '''table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table DataLossPreventionJobTrigger#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast("DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a9c49c00f6f944cffac74e0643a5b857434fded8ea099079b8de547b6e1bdb7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTable")
    def put_table(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#dataset_id DataLossPreventionJobTrigger#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#project_id DataLossPreventionJobTrigger#project_id}
        :param table_id: The ID of the table. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 1,024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table_id DataLossPreventionJobTrigger#table_id}
        '''
        value = DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable(
            dataset_id=dataset_id, project_id=project_id, table_id=table_id
        )

        return typing.cast(None, jsii.invoke(self, "putTable", [value]))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTableOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTableOutputReference", jsii.get(self, "table"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable"], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5c47d8f5013e620d5422506afcc63db8a883aaab4f2cd7bf8aeb238c7d9f2b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id": "datasetId",
        "project_id": "projectId",
        "table_id": "tableId",
    },
)
class DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable:
    def __init__(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#dataset_id DataLossPreventionJobTrigger#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#project_id DataLossPreventionJobTrigger#project_id}
        :param table_id: The ID of the table. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 1,024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table_id DataLossPreventionJobTrigger#table_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d322a4f5e596feb12a11c86899606683e443fa0ffdd8d709d5412f7b2bf1183f)
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
            "project_id": project_id,
        }
        if table_id is not None:
            self._values["table_id"] = table_id

    @builtins.property
    def dataset_id(self) -> builtins.str:
        '''The ID of the dataset containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#dataset_id DataLossPreventionJobTrigger#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The ID of the project containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#project_id DataLossPreventionJobTrigger#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the table.

        The ID must contain only letters (a-z,
        A-Z), numbers (0-9), or underscores (_). The maximum length
        is 1,024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table_id DataLossPreventionJobTrigger#table_id}
        '''
        result = self._values.get("table_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__991a338cc6946df4d99c603ab28020f0e61297d885f72f3c58dc0b829cb327b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTableId")
    def reset_table_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableId", []))

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tableIdInput")
    def table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb430885c0bd5b88f37b781c50f4da19de511d5a601bb8b5b8b3d505532ec001)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__965a70cfdde4f2b6b0e23da9d34b521c6b7a4b97d77ea189d25ce4ba9fd2dfd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ff15cbda74390d0136b8c63f607a09a11040f79b265ecba11a154cb575a7c95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf1aac70a24fa39551b49a578a1724cb62cd22a035c4189941abd545e1a20275)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5e4f17119f9570a20d2c0ceabbddf653a4529d850c796339ffc649b7212e124)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea47e9a864da0d5243091e150c66c495b9a41f45f405409f737500db908894a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d7b7793a4fb501448a086e714bbd4272c72b57eb827bea95bdcf8e96576f21a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionJobTriggerInspectJobActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7afb63fab054bcd5e2f0c258e593642d6d040581f7694000f2e8718b205ef89)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionJobTriggerInspectJobActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e79115c3c9741dd177f70f41cbea2344c389c8be339e9cfba463f4d10a08858)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e01bb9fee0530b3ae65672f96847d7b72e532ff9f2f468b1313a2b530b726774)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b610aabab275af61d1c025db23c883c120e3fb3eaf1549194877dd8392a5ca03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__790a6204de236976d747bba57161db52326bb2b2f0f59fc8aead07741b5312c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b954cfa638334c7ad8a3a23fa87f56314c829cc9ffdc0388d249d257a4976c09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDeidentify")
    def put_deidentify(
        self,
        *,
        cloud_storage_output: builtins.str,
        file_types_to_transform: typing.Optional[typing.Sequence[builtins.str]] = None,
        transformation_config: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        transformation_details_storage_config: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_output: User settable Cloud Storage bucket and folders to store de-identified files. This field must be set for cloud storage deidentification. The output Cloud Storage bucket must be different from the input bucket. De-identified files will overwrite files in the output path. Form of: gs://bucket/folder/ or gs://bucket Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#cloud_storage_output DataLossPreventionJobTrigger#cloud_storage_output}
        :param file_types_to_transform: List of user-specified file type groups to transform. If specified, only the files with these filetypes will be transformed. If empty, all supported files will be transformed. Supported types may be automatically added over time. If a file type is set in this field that isn't supported by the Deidentify action then the job will fail and will not be successfully created/started. Possible values: ["IMAGE", "TEXT_FILE", "CSV", "TSV"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#file_types_to_transform DataLossPreventionJobTrigger#file_types_to_transform}
        :param transformation_config: transformation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#transformation_config DataLossPreventionJobTrigger#transformation_config}
        :param transformation_details_storage_config: transformation_details_storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#transformation_details_storage_config DataLossPreventionJobTrigger#transformation_details_storage_config}
        '''
        value = DataLossPreventionJobTriggerInspectJobActionsDeidentify(
            cloud_storage_output=cloud_storage_output,
            file_types_to_transform=file_types_to_transform,
            transformation_config=transformation_config,
            transformation_details_storage_config=transformation_details_storage_config,
        )

        return typing.cast(None, jsii.invoke(self, "putDeidentify", [value]))

    @jsii.member(jsii_name="putJobNotificationEmails")
    def put_job_notification_emails(self) -> None:
        value = DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails()

        return typing.cast(None, jsii.invoke(self, "putJobNotificationEmails", [value]))

    @jsii.member(jsii_name="putPublishFindingsToCloudDataCatalog")
    def put_publish_findings_to_cloud_data_catalog(self) -> None:
        value = DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog()

        return typing.cast(None, jsii.invoke(self, "putPublishFindingsToCloudDataCatalog", [value]))

    @jsii.member(jsii_name="putPublishSummaryToCscc")
    def put_publish_summary_to_cscc(self) -> None:
        value = DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc()

        return typing.cast(None, jsii.invoke(self, "putPublishSummaryToCscc", [value]))

    @jsii.member(jsii_name="putPublishToStackdriver")
    def put_publish_to_stackdriver(self) -> None:
        value = DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver()

        return typing.cast(None, jsii.invoke(self, "putPublishToStackdriver", [value]))

    @jsii.member(jsii_name="putPubSub")
    def put_pub_sub(self, *, topic: builtins.str) -> None:
        '''
        :param topic: Cloud Pub/Sub topic to send notifications to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#topic DataLossPreventionJobTrigger#topic}
        '''
        value = DataLossPreventionJobTriggerInspectJobActionsPubSub(topic=topic)

        return typing.cast(None, jsii.invoke(self, "putPubSub", [value]))

    @jsii.member(jsii_name="putSaveFindings")
    def put_save_findings(
        self,
        *,
        output_config: typing.Union["DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param output_config: output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#output_config DataLossPreventionJobTrigger#output_config}
        '''
        value = DataLossPreventionJobTriggerInspectJobActionsSaveFindings(
            output_config=output_config
        )

        return typing.cast(None, jsii.invoke(self, "putSaveFindings", [value]))

    @jsii.member(jsii_name="resetDeidentify")
    def reset_deidentify(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeidentify", []))

    @jsii.member(jsii_name="resetJobNotificationEmails")
    def reset_job_notification_emails(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobNotificationEmails", []))

    @jsii.member(jsii_name="resetPublishFindingsToCloudDataCatalog")
    def reset_publish_findings_to_cloud_data_catalog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishFindingsToCloudDataCatalog", []))

    @jsii.member(jsii_name="resetPublishSummaryToCscc")
    def reset_publish_summary_to_cscc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishSummaryToCscc", []))

    @jsii.member(jsii_name="resetPublishToStackdriver")
    def reset_publish_to_stackdriver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishToStackdriver", []))

    @jsii.member(jsii_name="resetPubSub")
    def reset_pub_sub(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubSub", []))

    @jsii.member(jsii_name="resetSaveFindings")
    def reset_save_findings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaveFindings", []))

    @builtins.property
    @jsii.member(jsii_name="deidentify")
    def deidentify(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobActionsDeidentifyOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobActionsDeidentifyOutputReference, jsii.get(self, "deidentify"))

    @builtins.property
    @jsii.member(jsii_name="jobNotificationEmails")
    def job_notification_emails(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmailsOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmailsOutputReference, jsii.get(self, "jobNotificationEmails"))

    @builtins.property
    @jsii.member(jsii_name="publishFindingsToCloudDataCatalog")
    def publish_findings_to_cloud_data_catalog(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalogOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalogOutputReference", jsii.get(self, "publishFindingsToCloudDataCatalog"))

    @builtins.property
    @jsii.member(jsii_name="publishSummaryToCscc")
    def publish_summary_to_cscc(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCsccOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCsccOutputReference", jsii.get(self, "publishSummaryToCscc"))

    @builtins.property
    @jsii.member(jsii_name="publishToStackdriver")
    def publish_to_stackdriver(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriverOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriverOutputReference", jsii.get(self, "publishToStackdriver"))

    @builtins.property
    @jsii.member(jsii_name="pubSub")
    def pub_sub(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobActionsPubSubOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobActionsPubSubOutputReference", jsii.get(self, "pubSub"))

    @builtins.property
    @jsii.member(jsii_name="saveFindings")
    def save_findings(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputReference", jsii.get(self, "saveFindings"))

    @builtins.property
    @jsii.member(jsii_name="deidentifyInput")
    def deidentify_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentify]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentify], jsii.get(self, "deidentifyInput"))

    @builtins.property
    @jsii.member(jsii_name="jobNotificationEmailsInput")
    def job_notification_emails_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails], jsii.get(self, "jobNotificationEmailsInput"))

    @builtins.property
    @jsii.member(jsii_name="publishFindingsToCloudDataCatalogInput")
    def publish_findings_to_cloud_data_catalog_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog"], jsii.get(self, "publishFindingsToCloudDataCatalogInput"))

    @builtins.property
    @jsii.member(jsii_name="publishSummaryToCsccInput")
    def publish_summary_to_cscc_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc"], jsii.get(self, "publishSummaryToCsccInput"))

    @builtins.property
    @jsii.member(jsii_name="publishToStackdriverInput")
    def publish_to_stackdriver_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver"], jsii.get(self, "publishToStackdriverInput"))

    @builtins.property
    @jsii.member(jsii_name="pubSubInput")
    def pub_sub_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsPubSub"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsPubSub"], jsii.get(self, "pubSubInput"))

    @builtins.property
    @jsii.member(jsii_name="saveFindingsInput")
    def save_findings_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsSaveFindings"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsSaveFindings"], jsii.get(self, "saveFindingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87cb0b7e3973ac738d74ae454d26e8d37e6bc9f9d98b61298078c72686e53021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsPubSub",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic"},
)
class DataLossPreventionJobTriggerInspectJobActionsPubSub:
    def __init__(self, *, topic: builtins.str) -> None:
        '''
        :param topic: Cloud Pub/Sub topic to send notifications to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#topic DataLossPreventionJobTrigger#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10399479716dc20e9f0772fe8ce418e4e7f69d64947bb29390ec99360ac3b8e)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic": topic,
        }

    @builtins.property
    def topic(self) -> builtins.str:
        '''Cloud Pub/Sub topic to send notifications to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#topic DataLossPreventionJobTrigger#topic}
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobActionsPubSub(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobActionsPubSubOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsPubSubOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91e1a29845e30ab1e43133c300a673eb9586d49baf8aee35f2fcf9717099e3cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ae77d5f8c2a0d728bf2e2a1c915ea0ae8d1e3a5226a3e5f92a0a7b8297b58d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobActionsPubSub]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobActionsPubSub], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsPubSub],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34d8ee08fdc3faf33124ec538498b2e03a7b32d9539e4f5ec788cf3aabe009b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18a08116d347a559248283713aa9ae77728831e3a6efd50642022697db1afbed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba70105fea05f65bf413bd594d977040d2c0132ee9021ab2b8cc938d633c2a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCsccOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCsccOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b3cba9f380ff2a76e1c6a9fe88ce166b4b8c8e0aca2002c6de78b5e59ec89ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc8c2a26692b792d5126cf23368810ea9114581e317e8b19dfe56f5b5b9c13d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__000eb2028636cd870bd78c63f8afba0fd89f4f71b09d32dc0022503156e5a218)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a080d34fef8a6ed70f8404ce5187dcc7609ffff3d278e613a9ffe990b8922e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsSaveFindings",
    jsii_struct_bases=[],
    name_mapping={"output_config": "outputConfig"},
)
class DataLossPreventionJobTriggerInspectJobActionsSaveFindings:
    def __init__(
        self,
        *,
        output_config: typing.Union["DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param output_config: output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#output_config DataLossPreventionJobTrigger#output_config}
        '''
        if isinstance(output_config, dict):
            output_config = DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig(**output_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc359bc052e59241daa0911afdae16f1e0f43cfd78dff6b4267f3ae1fc623336)
            check_type(argname="argument output_config", value=output_config, expected_type=type_hints["output_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "output_config": output_config,
        }

    @builtins.property
    def output_config(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig":
        '''output_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#output_config DataLossPreventionJobTrigger#output_config}
        '''
        result = self._values.get("output_config")
        assert result is not None, "Required property 'output_config' is missing"
        return typing.cast("DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobActionsSaveFindings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig",
    jsii_struct_bases=[],
    name_mapping={"table": "table", "output_schema": "outputSchema"},
)
class DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig:
    def __init__(
        self,
        *,
        table: typing.Union["DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable", typing.Dict[builtins.str, typing.Any]],
        output_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table: table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table DataLossPreventionJobTrigger#table}
        :param output_schema: Schema used for writing the findings for Inspect jobs. This field is only used for Inspect and must be unspecified for Risk jobs. Columns are derived from the Finding object. If appending to an existing table, any columns from the predefined schema that are missing will be added. No columns in the existing table will be deleted. If unspecified, then all available columns will be used for a new table or an (existing) table with no schema, and no changes will be made to an existing table that has a schema. Only for use with external storage. Possible values: ["BASIC_COLUMNS", "GCS_COLUMNS", "DATASTORE_COLUMNS", "BIG_QUERY_COLUMNS", "ALL_COLUMNS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#output_schema DataLossPreventionJobTrigger#output_schema}
        '''
        if isinstance(table, dict):
            table = DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable(**table)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e6e1634b5fa031779f8bff2c8bfbc85fc439c1bf8f089d484ffef8c9731883)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument output_schema", value=output_schema, expected_type=type_hints["output_schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table": table,
        }
        if output_schema is not None:
            self._values["output_schema"] = output_schema

    @builtins.property
    def table(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable":
        '''table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table DataLossPreventionJobTrigger#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast("DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable", result)

    @builtins.property
    def output_schema(self) -> typing.Optional[builtins.str]:
        '''Schema used for writing the findings for Inspect jobs.

        This field is only used for
        Inspect and must be unspecified for Risk jobs. Columns are derived from the Finding
        object. If appending to an existing table, any columns from the predefined schema
        that are missing will be added. No columns in the existing table will be deleted.

        If unspecified, then all available columns will be used for a new table or an (existing)
        table with no schema, and no changes will be made to an existing table that has a schema.
        Only for use with external storage. Possible values: ["BASIC_COLUMNS", "GCS_COLUMNS", "DATASTORE_COLUMNS", "BIG_QUERY_COLUMNS", "ALL_COLUMNS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#output_schema DataLossPreventionJobTrigger#output_schema}
        '''
        result = self._values.get("output_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b3216c420cb696c7787c8d61c85684a108e53699f846590670ef613fa604e36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTable")
    def put_table(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataset_id: Dataset ID of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#dataset_id DataLossPreventionJobTrigger#dataset_id}
        :param project_id: The Google Cloud Platform project ID of the project containing the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#project_id DataLossPreventionJobTrigger#project_id}
        :param table_id: Name of the table. If is not set a new one will be generated for you with the following format: 'dlp_googleapis_yyyy_mm_dd_[dlp_job_id]'. Pacific timezone will be used for generating the date details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table_id DataLossPreventionJobTrigger#table_id}
        '''
        value = DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable(
            dataset_id=dataset_id, project_id=project_id, table_id=table_id
        )

        return typing.cast(None, jsii.invoke(self, "putTable", [value]))

    @jsii.member(jsii_name="resetOutputSchema")
    def reset_output_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputSchema", []))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTableOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTableOutputReference", jsii.get(self, "table"))

    @builtins.property
    @jsii.member(jsii_name="outputSchemaInput")
    def output_schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable"], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="outputSchema")
    def output_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputSchema"))

    @output_schema.setter
    def output_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cdf76fa521879272b1439915a3879f05e60d25ef0f4463c21407341f6b54beb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ad0701f01984f1add4a59c3661b0661afc17d20b869ca61ebbe235f0791156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id": "datasetId",
        "project_id": "projectId",
        "table_id": "tableId",
    },
)
class DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable:
    def __init__(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataset_id: Dataset ID of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#dataset_id DataLossPreventionJobTrigger#dataset_id}
        :param project_id: The Google Cloud Platform project ID of the project containing the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#project_id DataLossPreventionJobTrigger#project_id}
        :param table_id: Name of the table. If is not set a new one will be generated for you with the following format: 'dlp_googleapis_yyyy_mm_dd_[dlp_job_id]'. Pacific timezone will be used for generating the date details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table_id DataLossPreventionJobTrigger#table_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fadde11ebc41936b614223ce3e252c36eb5fef6253ec2cb325a482c5139b959)
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
            "project_id": project_id,
        }
        if table_id is not None:
            self._values["table_id"] = table_id

    @builtins.property
    def dataset_id(self) -> builtins.str:
        '''Dataset ID of the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#dataset_id DataLossPreventionJobTrigger#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The Google Cloud Platform project ID of the project containing the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#project_id DataLossPreventionJobTrigger#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_id(self) -> typing.Optional[builtins.str]:
        '''Name of the table.

        If is not set a new one will be generated for you with the following format:
        'dlp_googleapis_yyyy_mm_dd_[dlp_job_id]'. Pacific timezone will be used for generating the date details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table_id DataLossPreventionJobTrigger#table_id}
        '''
        result = self._values.get("table_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db7ae69086978f38297b60d0aa291b5c09fff5519f291f922fe55f47b0297741)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTableId")
    def reset_table_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableId", []))

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tableIdInput")
    def table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db83d4db743620b0751eb52ce764f8fb34dd594bada88f609c98cde6d35bdf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__596ba9b73fd23d85efb7f12e1c9e337bd597d27a5e9639aef2d8858fac839a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf88d167c2e6ec234dcb8b88dbfeebcd8ff7affbee86ef9e0eecc3ef69ff96bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeb96735996690e3182428e1b019b14e5b1ce0f35b1722680341832009acc4ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b31a730aa42a11b420f843392352ef5a095ffcd4f87be099b4a5dd4d1e5c4fe1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOutputConfig")
    def put_output_config(
        self,
        *,
        table: typing.Union[DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable, typing.Dict[builtins.str, typing.Any]],
        output_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table: table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table DataLossPreventionJobTrigger#table}
        :param output_schema: Schema used for writing the findings for Inspect jobs. This field is only used for Inspect and must be unspecified for Risk jobs. Columns are derived from the Finding object. If appending to an existing table, any columns from the predefined schema that are missing will be added. No columns in the existing table will be deleted. If unspecified, then all available columns will be used for a new table or an (existing) table with no schema, and no changes will be made to an existing table that has a schema. Only for use with external storage. Possible values: ["BASIC_COLUMNS", "GCS_COLUMNS", "DATASTORE_COLUMNS", "BIG_QUERY_COLUMNS", "ALL_COLUMNS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#output_schema DataLossPreventionJobTrigger#output_schema}
        '''
        value = DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig(
            table=table, output_schema=output_schema
        )

        return typing.cast(None, jsii.invoke(self, "putOutputConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="outputConfig")
    def output_config(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigOutputReference, jsii.get(self, "outputConfig"))

    @builtins.property
    @jsii.member(jsii_name="outputConfigInput")
    def output_config_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig], jsii.get(self, "outputConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobActionsSaveFindings]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobActionsSaveFindings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsSaveFindings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e896668c1a21228791415ad136b52f0b4437d2afbcf28c0acadd594196cbcafc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfig",
    jsii_struct_bases=[],
    name_mapping={
        "custom_info_types": "customInfoTypes",
        "exclude_info_types": "excludeInfoTypes",
        "include_quote": "includeQuote",
        "info_types": "infoTypes",
        "limits": "limits",
        "min_likelihood": "minLikelihood",
        "rule_set": "ruleSet",
    },
)
class DataLossPreventionJobTriggerInspectJobInspectConfig:
    def __init__(
        self,
        *,
        custom_info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        exclude_info_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_quote: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        limits: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        min_likelihood: typing.Optional[builtins.str] = None,
        rule_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param custom_info_types: custom_info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#custom_info_types DataLossPreventionJobTrigger#custom_info_types}
        :param exclude_info_types: When true, excludes type information of the findings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#exclude_info_types DataLossPreventionJobTrigger#exclude_info_types}
        :param include_quote: When true, a contextual quote from the data that triggered a finding is included in the response. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#include_quote DataLossPreventionJobTrigger#include_quote}
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#info_types DataLossPreventionJobTrigger#info_types}
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#limits DataLossPreventionJobTrigger#limits}
        :param min_likelihood: Only returns findings equal or above this threshold. See https://cloud.google.com/dlp/docs/likelihood for more info Default value: "POSSIBLE" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#min_likelihood DataLossPreventionJobTrigger#min_likelihood}
        :param rule_set: rule_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#rule_set DataLossPreventionJobTrigger#rule_set}
        '''
        if isinstance(limits, dict):
            limits = DataLossPreventionJobTriggerInspectJobInspectConfigLimits(**limits)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00d0c36718bd1a4f10474910048bb82d1875e075cf4800205c1843afcec72510)
            check_type(argname="argument custom_info_types", value=custom_info_types, expected_type=type_hints["custom_info_types"])
            check_type(argname="argument exclude_info_types", value=exclude_info_types, expected_type=type_hints["exclude_info_types"])
            check_type(argname="argument include_quote", value=include_quote, expected_type=type_hints["include_quote"])
            check_type(argname="argument info_types", value=info_types, expected_type=type_hints["info_types"])
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
            check_type(argname="argument min_likelihood", value=min_likelihood, expected_type=type_hints["min_likelihood"])
            check_type(argname="argument rule_set", value=rule_set, expected_type=type_hints["rule_set"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_info_types is not None:
            self._values["custom_info_types"] = custom_info_types
        if exclude_info_types is not None:
            self._values["exclude_info_types"] = exclude_info_types
        if include_quote is not None:
            self._values["include_quote"] = include_quote
        if info_types is not None:
            self._values["info_types"] = info_types
        if limits is not None:
            self._values["limits"] = limits
        if min_likelihood is not None:
            self._values["min_likelihood"] = min_likelihood
        if rule_set is not None:
            self._values["rule_set"] = rule_set

    @builtins.property
    def custom_info_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes"]]]:
        '''custom_info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#custom_info_types DataLossPreventionJobTrigger#custom_info_types}
        '''
        result = self._values.get("custom_info_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes"]]], result)

    @builtins.property
    def exclude_info_types(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, excludes type information of the findings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#exclude_info_types DataLossPreventionJobTrigger#exclude_info_types}
        '''
        result = self._values.get("exclude_info_types")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_quote(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, a contextual quote from the data that triggered a finding is included in the response.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#include_quote DataLossPreventionJobTrigger#include_quote}
        '''
        result = self._values.get("include_quote")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def info_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes"]]]:
        '''info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#info_types DataLossPreventionJobTrigger#info_types}
        '''
        result = self._values.get("info_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes"]]], result)

    @builtins.property
    def limits(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigLimits"]:
        '''limits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#limits DataLossPreventionJobTrigger#limits}
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigLimits"], result)

    @builtins.property
    def min_likelihood(self) -> typing.Optional[builtins.str]:
        '''Only returns findings equal or above this threshold.

        See https://cloud.google.com/dlp/docs/likelihood for more info Default value: "POSSIBLE" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#min_likelihood DataLossPreventionJobTrigger#min_likelihood}
        '''
        result = self._values.get("min_likelihood")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_set(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet"]]]:
        '''rule_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#rule_set DataLossPreventionJobTrigger#rule_set}
        '''
        result = self._values.get("rule_set")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes",
    jsii_struct_bases=[],
    name_mapping={
        "info_type": "infoType",
        "dictionary": "dictionary",
        "exclusion_type": "exclusionType",
        "likelihood": "likelihood",
        "regex": "regex",
        "sensitivity_score": "sensitivityScore",
        "stored_type": "storedType",
        "surrogate_type": "surrogateType",
    },
)
class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes:
    def __init__(
        self,
        *,
        info_type: typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType", typing.Dict[builtins.str, typing.Any]],
        dictionary: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusion_type: typing.Optional[builtins.str] = None,
        likelihood: typing.Optional[builtins.str] = None,
        regex: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex", typing.Dict[builtins.str, typing.Any]]] = None,
        sensitivity_score: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        stored_type: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType", typing.Dict[builtins.str, typing.Any]]] = None,
        surrogate_type: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param info_type: info_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#info_type DataLossPreventionJobTrigger#info_type}
        :param dictionary: dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#dictionary DataLossPreventionJobTrigger#dictionary}
        :param exclusion_type: If set to EXCLUSION_TYPE_EXCLUDE this infoType will not cause a finding to be returned. It still can be used for rules matching. Possible values: ["EXCLUSION_TYPE_EXCLUDE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#exclusion_type DataLossPreventionJobTrigger#exclusion_type}
        :param likelihood: Likelihood to return for this CustomInfoType. This base value can be altered by a detection rule if the finding meets the criteria specified by the rule. Default value: "VERY_LIKELY" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#likelihood DataLossPreventionJobTrigger#likelihood}
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#regex DataLossPreventionJobTrigger#regex}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sensitivity_score DataLossPreventionJobTrigger#sensitivity_score}
        :param stored_type: stored_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#stored_type DataLossPreventionJobTrigger#stored_type}
        :param surrogate_type: surrogate_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#surrogate_type DataLossPreventionJobTrigger#surrogate_type}
        '''
        if isinstance(info_type, dict):
            info_type = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType(**info_type)
        if isinstance(dictionary, dict):
            dictionary = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary(**dictionary)
        if isinstance(regex, dict):
            regex = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex(**regex)
        if isinstance(sensitivity_score, dict):
            sensitivity_score = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore(**sensitivity_score)
        if isinstance(stored_type, dict):
            stored_type = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType(**stored_type)
        if isinstance(surrogate_type, dict):
            surrogate_type = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType(**surrogate_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dec0a3d4fe2aa88db30c328e52c2fc8edb1809376420f46375eb9a0af567c16)
            check_type(argname="argument info_type", value=info_type, expected_type=type_hints["info_type"])
            check_type(argname="argument dictionary", value=dictionary, expected_type=type_hints["dictionary"])
            check_type(argname="argument exclusion_type", value=exclusion_type, expected_type=type_hints["exclusion_type"])
            check_type(argname="argument likelihood", value=likelihood, expected_type=type_hints["likelihood"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument sensitivity_score", value=sensitivity_score, expected_type=type_hints["sensitivity_score"])
            check_type(argname="argument stored_type", value=stored_type, expected_type=type_hints["stored_type"])
            check_type(argname="argument surrogate_type", value=surrogate_type, expected_type=type_hints["surrogate_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "info_type": info_type,
        }
        if dictionary is not None:
            self._values["dictionary"] = dictionary
        if exclusion_type is not None:
            self._values["exclusion_type"] = exclusion_type
        if likelihood is not None:
            self._values["likelihood"] = likelihood
        if regex is not None:
            self._values["regex"] = regex
        if sensitivity_score is not None:
            self._values["sensitivity_score"] = sensitivity_score
        if stored_type is not None:
            self._values["stored_type"] = stored_type
        if surrogate_type is not None:
            self._values["surrogate_type"] = surrogate_type

    @builtins.property
    def info_type(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType":
        '''info_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#info_type DataLossPreventionJobTrigger#info_type}
        '''
        result = self._values.get("info_type")
        assert result is not None, "Required property 'info_type' is missing"
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType", result)

    @builtins.property
    def dictionary(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary"]:
        '''dictionary block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#dictionary DataLossPreventionJobTrigger#dictionary}
        '''
        result = self._values.get("dictionary")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary"], result)

    @builtins.property
    def exclusion_type(self) -> typing.Optional[builtins.str]:
        '''If set to EXCLUSION_TYPE_EXCLUDE this infoType will not cause a finding to be returned.

        It still can be used for rules matching. Possible values: ["EXCLUSION_TYPE_EXCLUDE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#exclusion_type DataLossPreventionJobTrigger#exclusion_type}
        '''
        result = self._values.get("exclusion_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def likelihood(self) -> typing.Optional[builtins.str]:
        '''Likelihood to return for this CustomInfoType.

        This base value can be altered by a detection rule if the finding meets the criteria
        specified by the rule. Default value: "VERY_LIKELY" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#likelihood DataLossPreventionJobTrigger#likelihood}
        '''
        result = self._values.get("likelihood")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex"]:
        '''regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#regex DataLossPreventionJobTrigger#regex}
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex"], result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sensitivity_score DataLossPreventionJobTrigger#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore"], result)

    @builtins.property
    def stored_type(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType"]:
        '''stored_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#stored_type DataLossPreventionJobTrigger#stored_type}
        '''
        result = self._values.get("stored_type")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType"], result)

    @builtins.property
    def surrogate_type(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType"]:
        '''surrogate_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#surrogate_type DataLossPreventionJobTrigger#surrogate_type}
        '''
        result = self._values.get("surrogate_type")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary",
    jsii_struct_bases=[],
    name_mapping={"cloud_storage_path": "cloudStoragePath", "word_list": "wordList"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary:
    def __init__(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath", typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#cloud_storage_path DataLossPreventionJobTrigger#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#word_list DataLossPreventionJobTrigger#word_list}
        '''
        if isinstance(cloud_storage_path, dict):
            cloud_storage_path = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath(**cloud_storage_path)
        if isinstance(word_list, dict):
            word_list = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct(**word_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d9d3de50d75200d9c1fbb7c3328620a68694848aa0e0b78f2fa407a94842b6)
            check_type(argname="argument cloud_storage_path", value=cloud_storage_path, expected_type=type_hints["cloud_storage_path"])
            check_type(argname="argument word_list", value=word_list, expected_type=type_hints["word_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_storage_path is not None:
            self._values["cloud_storage_path"] = cloud_storage_path
        if word_list is not None:
            self._values["word_list"] = word_list

    @builtins.property
    def cloud_storage_path(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath"]:
        '''cloud_storage_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#cloud_storage_path DataLossPreventionJobTrigger#cloud_storage_path}
        '''
        result = self._values.get("cloud_storage_path")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath"], result)

    @builtins.property
    def word_list(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct"]:
        '''word_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#word_list DataLossPreventionJobTrigger#word_list}
        '''
        result = self._values.get("word_list")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath:
    def __init__(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#path DataLossPreventionJobTrigger#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__509c561e2e00962deb67c2c6242246b623eba48d9697e26b33f7c400e77ccb9d)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#path DataLossPreventionJobTrigger#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a4cedb9d7a2176f548421f2e8830a0598e5c2f7a8ce0b0193d1a61dcc1449de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71b57f2391a6a82716d81d3315ee1b336b9f0dd647959cb52679f453bf75e7f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a3865f5927e4539b0b2411af4622eabb453b661f4583e9fbffc2c12b067808f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6be02e1fc7a7577f539b9dd6bef267b963b6f7ee4b3d8d87846f6e33b5b4da36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudStoragePath")
    def put_cloud_storage_path(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#path DataLossPreventionJobTrigger#path}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath(
            path=path
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStoragePath", [value]))

    @jsii.member(jsii_name="putWordList")
    def put_word_list(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#words DataLossPreventionJobTrigger#words}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct(
            words=words
        )

        return typing.cast(None, jsii.invoke(self, "putWordList", [value]))

    @jsii.member(jsii_name="resetCloudStoragePath")
    def reset_cloud_storage_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudStoragePath", []))

    @jsii.member(jsii_name="resetWordList")
    def reset_word_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWordList", []))

    @builtins.property
    @jsii.member(jsii_name="cloudStoragePath")
    def cloud_storage_path(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference, jsii.get(self, "cloudStoragePath"))

    @builtins.property
    @jsii.member(jsii_name="wordList")
    def word_list(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference", jsii.get(self, "wordList"))

    @builtins.property
    @jsii.member(jsii_name="cloudStoragePathInput")
    def cloud_storage_path_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath], jsii.get(self, "cloudStoragePathInput"))

    @builtins.property
    @jsii.member(jsii_name="wordListInput")
    def word_list_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct"], jsii.get(self, "wordListInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59665e85b3c72e005006ff2747cd7a0f569396f169305cc9aafbd14e79c0f6a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct",
    jsii_struct_bases=[],
    name_mapping={"words": "words"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct:
    def __init__(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#words DataLossPreventionJobTrigger#words}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45e93939b41a3e56fad19a18a89c16496cad975f645aa8653a03e1d0acce6c6a)
            check_type(argname="argument words", value=words, expected_type=type_hints["words"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "words": words,
        }

    @builtins.property
    def words(self) -> typing.List[builtins.str]:
        '''Words or phrases defining the dictionary.

        The dictionary must contain at least one
        phrase and every phrase must contain at least 2 characters that are letters or digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#words DataLossPreventionJobTrigger#words}
        '''
        result = self._values.get("words")
        assert result is not None, "Required property 'words' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcc21a7fe78ba4b91bc5dd734385b5347d2f210fd323c356c0cf48d3397e279c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="wordsInput")
    def words_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "wordsInput"))

    @builtins.property
    @jsii.member(jsii_name="words")
    def words(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "words"))

    @words.setter
    def words(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207112d025bd6d9b4a558bc16586aebe09322296b69b21cb05e39c3b53f5bb74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "words", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e27d86d41b8d8419a4d4157f0f48a213026e8d1d314d333e83612a643b47304c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sensitivity_score DataLossPreventionJobTrigger#sensitivity_score}
        :param version: Version of the information type to use. By default, the version is set to stable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#version DataLossPreventionJobTrigger#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a651b39110a4e785f83960541b7c375ce52bbf9f8700c1c7de7a7a7f0525aaf)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sensitivity_score", value=sensitivity_score, expected_type=type_hints["sensitivity_score"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if sensitivity_score is not None:
            self._values["sensitivity_score"] = sensitivity_score
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the information type.

        Either a name of your choosing when creating a CustomInfoType, or one of the names
        listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sensitivity_score DataLossPreventionJobTrigger#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the information type to use. By default, the version is set to stable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#version DataLossPreventionJobTrigger#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eac671534682db04da4dd27bb11432aa735e157d1463e268df94606f98c8dfd1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore(
            score=score
        )

        return typing.cast(None, jsii.invoke(self, "putSensitivityScore", [value]))

    @jsii.member(jsii_name="resetSensitivityScore")
    def reset_sensitivity_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitivityScore", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScore")
    def sensitivity_score(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f46e799704de97e9cdeb032c194d0b89fb3f271e26dadaf53c3fdd0f2aac0d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60cafb48d72ca3bf38b237f40a50f833c8b650511867bf5feb523d69fa1a37f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77934e0f19e69c4737b55e152b6e9de6ae075121460e73c25708768fa6fc46aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1434bf435d60f06813f89b3bba8dda5a68b830fc95d2968b22fe7018ff09d24)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25d388a70588d45e06310680749e6989400ae3fc94c8c7624f80d25a41a15ac4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scoreInput")
    def score_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scoreInput"))

    @builtins.property
    @jsii.member(jsii_name="score")
    def score(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "score"))

    @score.setter
    def score(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5a7e08434debe86afc97d1780f36856a06f8f91e461dc80bc2267ac71969ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a27024519de6ca63c6d6bf97515b9780b7ff41f71379d40005c61ba04583b84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64d9608a0bcf8b5aeb59ba98ea6046686b515a68696f48156757af81237029ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6543ffcf85f72da9997439e33cb56c66b4b7d68f5d8d4c5c1fbb052659389432)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ead144469ed3ca65c0cab738e28b1af0b924792710a500b3bde42fcd1f48ec6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bad37e539525767f40a6d4a3494ecb81e73b076e0c6ffdd7c971c467d4fdb81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5237ab4e884401030f86d13f326467ebbbe4d0bc21e3788261cdf9c93278696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e16a79171e0d5056527ebe09b36140189234a4582856734c21260e0f0627b04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a2ada61cf76b3d0197f69c16ed3b7bcb72d30f8a91bcb3f4625dd24a0301641)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDictionary")
    def put_dictionary(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#cloud_storage_path DataLossPreventionJobTrigger#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#word_list DataLossPreventionJobTrigger#word_list}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary(
            cloud_storage_path=cloud_storage_path, word_list=word_list
        )

        return typing.cast(None, jsii.invoke(self, "putDictionary", [value]))

    @jsii.member(jsii_name="putInfoType")
    def put_info_type(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sensitivity_score DataLossPreventionJobTrigger#sensitivity_score}
        :param version: Version of the information type to use. By default, the version is set to stable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#version DataLossPreventionJobTrigger#version}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType(
            name=name, sensitivity_score=sensitivity_score, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putInfoType", [value]))

    @jsii.member(jsii_name="putRegex")
    def put_regex(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#pattern DataLossPreventionJobTrigger#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#group_indexes DataLossPreventionJobTrigger#group_indexes}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex(
            pattern=pattern, group_indexes=group_indexes
        )

        return typing.cast(None, jsii.invoke(self, "putRegex", [value]))

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore(
            score=score
        )

        return typing.cast(None, jsii.invoke(self, "putSensitivityScore", [value]))

    @jsii.member(jsii_name="putStoredType")
    def put_stored_type(self, *, name: builtins.str) -> None:
        '''
        :param name: Resource name of the requested StoredInfoType, for example 'organizations/433245324/storedInfoTypes/432452342' or 'projects/project-id/storedInfoTypes/432452342'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putStoredType", [value]))

    @jsii.member(jsii_name="putSurrogateType")
    def put_surrogate_type(self) -> None:
        value = DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType()

        return typing.cast(None, jsii.invoke(self, "putSurrogateType", [value]))

    @jsii.member(jsii_name="resetDictionary")
    def reset_dictionary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDictionary", []))

    @jsii.member(jsii_name="resetExclusionType")
    def reset_exclusion_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusionType", []))

    @jsii.member(jsii_name="resetLikelihood")
    def reset_likelihood(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLikelihood", []))

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @jsii.member(jsii_name="resetSensitivityScore")
    def reset_sensitivity_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitivityScore", []))

    @jsii.member(jsii_name="resetStoredType")
    def reset_stored_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStoredType", []))

    @jsii.member(jsii_name="resetSurrogateType")
    def reset_surrogate_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSurrogateType", []))

    @builtins.property
    @jsii.member(jsii_name="dictionary")
    def dictionary(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryOutputReference, jsii.get(self, "dictionary"))

    @builtins.property
    @jsii.member(jsii_name="infoType")
    def info_type(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeOutputReference, jsii.get(self, "infoType"))

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegexOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegexOutputReference", jsii.get(self, "regex"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScore")
    def sensitivity_score(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScoreOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="storedType")
    def stored_type(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredTypeOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredTypeOutputReference", jsii.get(self, "storedType"))

    @builtins.property
    @jsii.member(jsii_name="surrogateType")
    def surrogate_type(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateTypeOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateTypeOutputReference", jsii.get(self, "surrogateType"))

    @builtins.property
    @jsii.member(jsii_name="dictionaryInput")
    def dictionary_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary], jsii.get(self, "dictionaryInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionTypeInput")
    def exclusion_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exclusionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="infoTypeInput")
    def info_type_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType], jsii.get(self, "infoTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="likelihoodInput")
    def likelihood_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "likelihoodInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex"], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="storedTypeInput")
    def stored_type_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType"], jsii.get(self, "storedTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="surrogateTypeInput")
    def surrogate_type_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType"], jsii.get(self, "surrogateTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionType")
    def exclusion_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exclusionType"))

    @exclusion_type.setter
    def exclusion_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c82edd5911beec6a6a1773489b29d6e37462ade683f36ec91678af7720a27c7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="likelihood")
    def likelihood(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "likelihood"))

    @likelihood.setter
    def likelihood(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24b37f9ccf00fa2fe4d3e42fb297bdebe2aa616688cfd8b6554bb4b64feebe87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "likelihood", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11338433c97268450fc367fab3cd6897f1f2aa43664e33ac2c0e1351df268a58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern", "group_indexes": "groupIndexes"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex:
    def __init__(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#pattern DataLossPreventionJobTrigger#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#group_indexes DataLossPreventionJobTrigger#group_indexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1bf8d67022760d1c61560700ca2e0192d2e226d470fbf7f12cf5990f5865300)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument group_indexes", value=group_indexes, expected_type=type_hints["group_indexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pattern": pattern,
        }
        if group_indexes is not None:
            self._values["group_indexes"] = group_indexes

    @builtins.property
    def pattern(self) -> builtins.str:
        '''Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#pattern DataLossPreventionJobTrigger#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_indexes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The index of the submatch to extract as findings.

        When not specified, the entire match is returned. No more than 3 may be included.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#group_indexes DataLossPreventionJobTrigger#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a30df5af885620ba5a9a44048f657d4464e4141cdc890654b9f7d5e5ff37f68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGroupIndexes")
    def reset_group_indexes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupIndexes", []))

    @builtins.property
    @jsii.member(jsii_name="groupIndexesInput")
    def group_indexes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "groupIndexesInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIndexes")
    def group_indexes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "groupIndexes"))

    @group_indexes.setter
    def group_indexes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0cd9de818777c5d5b72e112e6085fc5b0ad4a36b358d95e4b8470eb26e5b7aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06434def12e9fbfa2dd103c3a9a669a7901f32fe02ad47e3a70b49155e6f3d67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22875e7034c3425f338a96248a0bb284055a2a89b9eadea73d99aef63d9507c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__133305467162b53fe8d13d5f1b65fe845eff04ad2086b2be23975fd739bfa732)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7ec98bea7345d10735535e16a49f543f4dee52f7ecaabde1f52d4a4b2d85d27)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scoreInput")
    def score_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scoreInput"))

    @builtins.property
    @jsii.member(jsii_name="score")
    def score(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "score"))

    @score.setter
    def score(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__506a616292e74d719336282b3648bad255e2ec8b8f715d72c135d1a87f0e313e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b23c23656915a17cf354658a25ae1f93ddfdc2382819c3ace70193a150097622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Resource name of the requested StoredInfoType, for example 'organizations/433245324/storedInfoTypes/432452342' or 'projects/project-id/storedInfoTypes/432452342'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__350c83a51f73b43ff1a8718b9fd8ca6c6f6b00bd0039445fbe344825bbbe5525)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Resource name of the requested StoredInfoType, for example 'organizations/433245324/storedInfoTypes/432452342' or 'projects/project-id/storedInfoTypes/432452342'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8829a7e19ca86cd55539b113ade64397b123c57fba337674f3da681f5b8ac94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b6547ddbc48c8e9691157470fb426ea36d874eadb53833ad179c81a70b4b24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b28caec158c87b0f06a639b08dc505985067c25eb139d1878a7fab6041030888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aafd36160d3a63ce9b02b081c500436f7fe46b7ac0e25ad8a1989b2dc5d6ff86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90c25d5cec165fccd9031a80c71108fbcc893aa0b0ef8dad8d82ff5e4bedbe50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sensitivity_score DataLossPreventionJobTrigger#sensitivity_score}
        :param version: Version of the information type to use. By default, the version is set to stable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#version DataLossPreventionJobTrigger#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e02cedfec2c1061be300abe65da0bc0ef670be9c3c1fd81a9badf84a3eef7c0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sensitivity_score", value=sensitivity_score, expected_type=type_hints["sensitivity_score"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if sensitivity_score is not None:
            self._values["sensitivity_score"] = sensitivity_score
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the information type.

        Either a name of your choosing when creating a CustomInfoType, or one of the names listed
        at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sensitivity_score DataLossPreventionJobTrigger#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the information type to use. By default, the version is set to stable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#version DataLossPreventionJobTrigger#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd422dedaeeba2491cf1b9b2c88776658f465c2773a30db0ce0e30c60118796b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c32b15c7c87d70bd241853656fedd5db1f8c064b3080cc7ba9443d2a7e026f1a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a24090cf6538ef7a7a5427d29165b03822a360975e0163abc794253d2dc2b3a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ce7cdf8dff166966114e876a1922400a4f23a4e1b4e876b6668ab62906eabe7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b6f5fa2d48ae1870830526bc9692de8cd2a945356232c7d4d048ee8674e9ac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4224960962547b7bc7a8114295927c03d57f0cec4bfe56f63866c674566cd071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13ce295b8c2dd596d4f3fb06dafdc74ef0e7e57eabdd2e51627f72515aaee598)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore(
            score=score
        )

        return typing.cast(None, jsii.invoke(self, "putSensitivityScore", [value]))

    @jsii.member(jsii_name="resetSensitivityScore")
    def reset_sensitivity_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitivityScore", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScore")
    def sensitivity_score(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScoreOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15eeb607e2f4f2b2b5c517074eaf341a354b4396d5750f82649c3a12737a05ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__708eedce1d2b211a348d2b185b99efe477c0d4195d9d648379936a363c4951f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__909ff18835ae9a33d57af2b79ff61309f4de7a95fe06ae9d8ae40b345bd24417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c9f469ca568416cac2ef31fa785d46ccf6f810b69881d8f199a175a30e26d18)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9a7821bb4a17002b2433002fc8467fbaa3e63606f2bd22b9115f4de09aa8d2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scoreInput")
    def score_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scoreInput"))

    @builtins.property
    @jsii.member(jsii_name="score")
    def score(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "score"))

    @score.setter
    def score(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a420e370622fd377b9c1239f76bfea77436a3ccfedd458201964a823b74a14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f8948bd8b4256e5117311ca26ed542f9622e2a2ce81b37f6a549a3dc1495750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigLimits",
    jsii_struct_bases=[],
    name_mapping={
        "max_findings_per_info_type": "maxFindingsPerInfoType",
        "max_findings_per_item": "maxFindingsPerItem",
        "max_findings_per_request": "maxFindingsPerRequest",
    },
)
class DataLossPreventionJobTriggerInspectJobInspectConfigLimits:
    def __init__(
        self,
        *,
        max_findings_per_info_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_findings_per_item: typing.Optional[jsii.Number] = None,
        max_findings_per_request: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_findings_per_info_type: max_findings_per_info_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#max_findings_per_info_type DataLossPreventionJobTrigger#max_findings_per_info_type}
        :param max_findings_per_item: Max number of findings that will be returned for each item scanned. The maximum returned is 2000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#max_findings_per_item DataLossPreventionJobTrigger#max_findings_per_item}
        :param max_findings_per_request: Max number of findings that will be returned per request/job. The maximum returned is 2000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#max_findings_per_request DataLossPreventionJobTrigger#max_findings_per_request}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f1fd422a7953954fd55dcf8e668dd54e6bfed487b71d500e985fa897d4463cf)
            check_type(argname="argument max_findings_per_info_type", value=max_findings_per_info_type, expected_type=type_hints["max_findings_per_info_type"])
            check_type(argname="argument max_findings_per_item", value=max_findings_per_item, expected_type=type_hints["max_findings_per_item"])
            check_type(argname="argument max_findings_per_request", value=max_findings_per_request, expected_type=type_hints["max_findings_per_request"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_findings_per_info_type is not None:
            self._values["max_findings_per_info_type"] = max_findings_per_info_type
        if max_findings_per_item is not None:
            self._values["max_findings_per_item"] = max_findings_per_item
        if max_findings_per_request is not None:
            self._values["max_findings_per_request"] = max_findings_per_request

    @builtins.property
    def max_findings_per_info_type(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType"]]]:
        '''max_findings_per_info_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#max_findings_per_info_type DataLossPreventionJobTrigger#max_findings_per_info_type}
        '''
        result = self._values.get("max_findings_per_info_type")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType"]]], result)

    @builtins.property
    def max_findings_per_item(self) -> typing.Optional[jsii.Number]:
        '''Max number of findings that will be returned for each item scanned. The maximum returned is 2000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#max_findings_per_item DataLossPreventionJobTrigger#max_findings_per_item}
        '''
        result = self._values.get("max_findings_per_item")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_findings_per_request(self) -> typing.Optional[jsii.Number]:
        '''Max number of findings that will be returned per request/job. The maximum returned is 2000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#max_findings_per_request DataLossPreventionJobTrigger#max_findings_per_request}
        '''
        result = self._values.get("max_findings_per_request")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType",
    jsii_struct_bases=[],
    name_mapping={"info_type": "infoType", "max_findings": "maxFindings"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType:
    def __init__(
        self,
        *,
        info_type: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType", typing.Dict[builtins.str, typing.Any]]] = None,
        max_findings: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param info_type: info_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#info_type DataLossPreventionJobTrigger#info_type}
        :param max_findings: Max findings limit for the given infoType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#max_findings DataLossPreventionJobTrigger#max_findings}
        '''
        if isinstance(info_type, dict):
            info_type = DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType(**info_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c865a438b8a601f8675e8c2b5e72108d56742c9062f0b3a8a7889295c05072da)
            check_type(argname="argument info_type", value=info_type, expected_type=type_hints["info_type"])
            check_type(argname="argument max_findings", value=max_findings, expected_type=type_hints["max_findings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if info_type is not None:
            self._values["info_type"] = info_type
        if max_findings is not None:
            self._values["max_findings"] = max_findings

    @builtins.property
    def info_type(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType"]:
        '''info_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#info_type DataLossPreventionJobTrigger#info_type}
        '''
        result = self._values.get("info_type")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType"], result)

    @builtins.property
    def max_findings(self) -> typing.Optional[jsii.Number]:
        '''Max findings limit for the given infoType.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#max_findings DataLossPreventionJobTrigger#max_findings}
        '''
        result = self._values.get("max_findings")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sensitivity_score DataLossPreventionJobTrigger#sensitivity_score}
        :param version: Version of the information type to use. By default, the version is set to stable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#version DataLossPreventionJobTrigger#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a5983a26fd6249a362a5eccabc2aec441bb91d532b43979086020be7056787c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sensitivity_score", value=sensitivity_score, expected_type=type_hints["sensitivity_score"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if sensitivity_score is not None:
            self._values["sensitivity_score"] = sensitivity_score
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the information type.

        Either a name of your choosing when creating a CustomInfoType, or one of the names listed
        at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sensitivity_score DataLossPreventionJobTrigger#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the information type to use. By default, the version is set to stable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#version DataLossPreventionJobTrigger#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fafb63f36f744b82f1a6a59eb275555b4cd78ee1ed97888cc3f7e2b1ac133d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore(
            score=score
        )

        return typing.cast(None, jsii.invoke(self, "putSensitivityScore", [value]))

    @jsii.member(jsii_name="resetSensitivityScore")
    def reset_sensitivity_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitivityScore", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScore")
    def sensitivity_score(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25ecc09eea7aca228784c1530adff1db3e1959520e74ab0819c3317b12a1ac43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef356ef54585a92342051f19f8d53706bf941b58b84c24da5b8e92f6e87f370c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b56da640ea12c43be644d35cbdd5adbfd7482fa9a4568a8b741c3b7320a7d6f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__099d0c4ce71f569198577b2ba0c8173fe6fa9d28f1f94eb22f66d15d1dc95807)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca3e4a9b8e29d59561c7da890f178a8aec3311416d33383acaff7124594147f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scoreInput")
    def score_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scoreInput"))

    @builtins.property
    @jsii.member(jsii_name="score")
    def score(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "score"))

    @score.setter
    def score(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24da2b7e5c208d911c972628f7b5d1bf7943acefb94934d7699bd849a4b529a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ff8cd63397c3615efbbd105e830803b27b4f5d4fc243542c720a7e9cdbd88eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c892289cffd49e7de77e857e7b41c5ffa336f40d23b7a9690dc7bc068f29c09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f85bca5b774d406b442717f58c5b42d33d646863516fc2bbd3f5032c1698663)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bffd5ffe67b60a8ab8d89250aa32469b4a539d0820f10f68fd213791ddf8d92)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dc8f4c9299d1428c40c1f4070d53d81a2b6dcc1c675d2222ad8474b700c15e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01f9b6954387279f791f3b2fed1ca867c3e52e64677f9d87d17e639b9945636a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40d224c918a69b2b024b794a426f3a484e29c704c06c5f91c2b121d33f7cf6e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96553ff5915d996a1fd76eef5691e3a81038442fe3f21cb2aa52a78b9bedbe11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInfoType")
    def put_info_type(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sensitivity_score DataLossPreventionJobTrigger#sensitivity_score}
        :param version: Version of the information type to use. By default, the version is set to stable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#version DataLossPreventionJobTrigger#version}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType(
            name=name, sensitivity_score=sensitivity_score, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putInfoType", [value]))

    @jsii.member(jsii_name="resetInfoType")
    def reset_info_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfoType", []))

    @jsii.member(jsii_name="resetMaxFindings")
    def reset_max_findings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxFindings", []))

    @builtins.property
    @jsii.member(jsii_name="infoType")
    def info_type(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference, jsii.get(self, "infoType"))

    @builtins.property
    @jsii.member(jsii_name="infoTypeInput")
    def info_type_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType], jsii.get(self, "infoTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFindingsInput")
    def max_findings_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxFindingsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFindings")
    def max_findings(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxFindings"))

    @max_findings.setter
    def max_findings(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19417cd7a115fd9d8682d7f33d1329b1d615c18a8d707810ae3278344f0477c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFindings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ff1aabd642e772fb102c723f666c67a58dc85b74015b49c061764e7441f5a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigLimitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__295fe56948a5e5eefd1e9d78b0b71af43a10fcc56e697d55f9682f79fe85e5e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMaxFindingsPerInfoType")
    def put_max_findings_per_info_type(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bcce518f720c31084ba8d9b74194b3eb96143d31854cf669c91bd6f651546e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMaxFindingsPerInfoType", [value]))

    @jsii.member(jsii_name="resetMaxFindingsPerInfoType")
    def reset_max_findings_per_info_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxFindingsPerInfoType", []))

    @jsii.member(jsii_name="resetMaxFindingsPerItem")
    def reset_max_findings_per_item(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxFindingsPerItem", []))

    @jsii.member(jsii_name="resetMaxFindingsPerRequest")
    def reset_max_findings_per_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxFindingsPerRequest", []))

    @builtins.property
    @jsii.member(jsii_name="maxFindingsPerInfoType")
    def max_findings_per_info_type(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeList:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeList, jsii.get(self, "maxFindingsPerInfoType"))

    @builtins.property
    @jsii.member(jsii_name="maxFindingsPerInfoTypeInput")
    def max_findings_per_info_type_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]]], jsii.get(self, "maxFindingsPerInfoTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFindingsPerItemInput")
    def max_findings_per_item_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxFindingsPerItemInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFindingsPerRequestInput")
    def max_findings_per_request_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxFindingsPerRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFindingsPerItem")
    def max_findings_per_item(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxFindingsPerItem"))

    @max_findings_per_item.setter
    def max_findings_per_item(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b1d9e1b90337bda9c8197439adf3b5f41265c22c9d5460c9d7e2288bde58173)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFindingsPerItem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxFindingsPerRequest")
    def max_findings_per_request(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxFindingsPerRequest"))

    @max_findings_per_request.setter
    def max_findings_per_request(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__598e2763e2d00ed25b87843ea1b22fe0542f7d16b32c373536aabaf0019d7e40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFindingsPerRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigLimits]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigLimits],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d14ddd143ba87d2686e7a668f4981c886dd6ae4296989c64b6d20da1059e5359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f895fc5d283c9d4bd5e5c0cdfdb9c96c85b7462c515a054f894aa7b748b367f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomInfoTypes")
    def put_custom_info_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29ae97eed286c2f8934b1e17e2eb5a47b6fe701d84ffcee23df8a413b62b0089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomInfoTypes", [value]))

    @jsii.member(jsii_name="putInfoTypes")
    def put_info_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90d18972295f45e85dc389c45421d9b416b4b3bffb9bbce85bc2f3c156bf611d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInfoTypes", [value]))

    @jsii.member(jsii_name="putLimits")
    def put_limits(
        self,
        *,
        max_findings_per_info_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType, typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_findings_per_item: typing.Optional[jsii.Number] = None,
        max_findings_per_request: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_findings_per_info_type: max_findings_per_info_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#max_findings_per_info_type DataLossPreventionJobTrigger#max_findings_per_info_type}
        :param max_findings_per_item: Max number of findings that will be returned for each item scanned. The maximum returned is 2000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#max_findings_per_item DataLossPreventionJobTrigger#max_findings_per_item}
        :param max_findings_per_request: Max number of findings that will be returned per request/job. The maximum returned is 2000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#max_findings_per_request DataLossPreventionJobTrigger#max_findings_per_request}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigLimits(
            max_findings_per_info_type=max_findings_per_info_type,
            max_findings_per_item=max_findings_per_item,
            max_findings_per_request=max_findings_per_request,
        )

        return typing.cast(None, jsii.invoke(self, "putLimits", [value]))

    @jsii.member(jsii_name="putRuleSet")
    def put_rule_set(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9a5be734d39919ee0b0b1e61394c931d374ac9a0340fee5ad21e1cf820d98df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRuleSet", [value]))

    @jsii.member(jsii_name="resetCustomInfoTypes")
    def reset_custom_info_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomInfoTypes", []))

    @jsii.member(jsii_name="resetExcludeInfoTypes")
    def reset_exclude_info_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeInfoTypes", []))

    @jsii.member(jsii_name="resetIncludeQuote")
    def reset_include_quote(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeQuote", []))

    @jsii.member(jsii_name="resetInfoTypes")
    def reset_info_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfoTypes", []))

    @jsii.member(jsii_name="resetLimits")
    def reset_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimits", []))

    @jsii.member(jsii_name="resetMinLikelihood")
    def reset_min_likelihood(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinLikelihood", []))

    @jsii.member(jsii_name="resetRuleSet")
    def reset_rule_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleSet", []))

    @builtins.property
    @jsii.member(jsii_name="customInfoTypes")
    def custom_info_types(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesList:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesList, jsii.get(self, "customInfoTypes"))

    @builtins.property
    @jsii.member(jsii_name="infoTypes")
    def info_types(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesList:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesList, jsii.get(self, "infoTypes"))

    @builtins.property
    @jsii.member(jsii_name="limits")
    def limits(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigLimitsOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigLimitsOutputReference, jsii.get(self, "limits"))

    @builtins.property
    @jsii.member(jsii_name="ruleSet")
    def rule_set(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetList":
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetList", jsii.get(self, "ruleSet"))

    @builtins.property
    @jsii.member(jsii_name="customInfoTypesInput")
    def custom_info_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]]], jsii.get(self, "customInfoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeInfoTypesInput")
    def exclude_info_types_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeInfoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="includeQuoteInput")
    def include_quote_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeQuoteInput"))

    @builtins.property
    @jsii.member(jsii_name="infoTypesInput")
    def info_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]]], jsii.get(self, "infoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="limitsInput")
    def limits_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigLimits]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigLimits], jsii.get(self, "limitsInput"))

    @builtins.property
    @jsii.member(jsii_name="minLikelihoodInput")
    def min_likelihood_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minLikelihoodInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleSetInput")
    def rule_set_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet"]]], jsii.get(self, "ruleSetInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeInfoTypes")
    def exclude_info_types(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "excludeInfoTypes"))

    @exclude_info_types.setter
    def exclude_info_types(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62f108cb88876c83a02f5f6838e1f0b0ee8b42f7c29064cdab66f997419f0171)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeInfoTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeQuote")
    def include_quote(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeQuote"))

    @include_quote.setter
    def include_quote(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22365815918b2b49a9cec4dd7d0d6b67785a0196c83ef48c37b7f7b8f1d87c95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeQuote", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minLikelihood")
    def min_likelihood(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minLikelihood"))

    @min_likelihood.setter
    def min_likelihood(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5949c18204b35287d84281da147387a46caca9b9b2633d441ea4175f35a2579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minLikelihood", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfig]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20952ce0b981344634c19d8b85ff97212d5bb2d45641cb88874307b6145c6d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet",
    jsii_struct_bases=[],
    name_mapping={"rules": "rules", "info_types": "infoTypes"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet:
    def __init__(
        self,
        *,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules", typing.Dict[builtins.str, typing.Any]]]],
        info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#rules DataLossPreventionJobTrigger#rules}
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#info_types DataLossPreventionJobTrigger#info_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efb54ef9648d7f06a768b88be856c93ba3db798ba4eeb79468cbdb8d2e3f34f1)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument info_types", value=info_types, expected_type=type_hints["info_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rules": rules,
        }
        if info_types is not None:
            self._values["info_types"] = info_types

    @builtins.property
    def rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules"]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#rules DataLossPreventionJobTrigger#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules"]], result)

    @builtins.property
    def info_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes"]]]:
        '''info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#info_types DataLossPreventionJobTrigger#info_types}
        '''
        result = self._values.get("info_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sensitivity_score DataLossPreventionJobTrigger#sensitivity_score}
        :param version: Version of the information type to use. By default, the version is set to stable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#version DataLossPreventionJobTrigger#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__791d5e516cb13aeea2d4a221d6574cf8902158b70a82e81022bb3f69cbb1d1e1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sensitivity_score", value=sensitivity_score, expected_type=type_hints["sensitivity_score"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if sensitivity_score is not None:
            self._values["sensitivity_score"] = sensitivity_score
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the information type.

        Either a name of your choosing when creating a CustomInfoType, or one of the names listed
        at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sensitivity_score DataLossPreventionJobTrigger#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the information type to use. By default, the version is set to stable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#version DataLossPreventionJobTrigger#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2e9ecf5fb918e2accbde6833d388799950a32f7259f0581bb7fa7be3dc0ed7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbfcaba0f2d9d6c84613c607c91bed33b0ac48433ec91033eff1e2666421ad3c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__443126cb9ad7063a46059b90b579e81502104d9f1e400422bd58184c9814d676)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ca20f6bb16e6ce715b77922fe908535c64c7b727dfeae6b77bbc93a48b50a05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdd72a4de5abe475ec116efeafe2628ab0b327e9bb5f84437df356b248d3101e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10842b1501ddf17578c35846a2165ef997cfd50b8617ef4105c5967093f477d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75eab1143015eaece2f13add8cc63c90831af7c76fa4245895a072ebe48142c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore(
            score=score
        )

        return typing.cast(None, jsii.invoke(self, "putSensitivityScore", [value]))

    @jsii.member(jsii_name="resetSensitivityScore")
    def reset_sensitivity_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitivityScore", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScore")
    def sensitivity_score(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b4595d1e68295ee8d0fc8b92435d7f786c789f70002f42c553d95f49eea1c3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c3447200865ffc84459829ef0f3b09ec7197f311efb099191af69a7515d7b52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635f3283c2e2d0f8ca1eed814f196ff4994d9f44101c8dda0e31ee6323165c9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397ac3b4bb5415c083fbd503bb2dfb828ba78ea9636670ae42cc5f2558975603)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__542f4ebded24948a13804dc89d35ea2ce589e7f9f29405b663817756fd754324)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scoreInput")
    def score_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scoreInput"))

    @builtins.property
    @jsii.member(jsii_name="score")
    def score(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "score"))

    @score.setter
    def score(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb2746bbd3224dbce83cd2e3c4062f11286abc5e820993797493b062330df616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7c815519b144349c286e466fb3cc36bca0f0d2f70b384e0523c853e37b2691b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71d67df94c9b58e17f4b14fe6d9943d908ee85f8c3f5d25a9f083afa11f1068d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cae6f13f05b4dfcbef446c8311503b878f682d45922ca51160d145a3c729242)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2928dc60071c516a191ec6829b25d54b9980b52a62a0026ea75b3815841005b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2992e3a98ae6bbb04bc8257bb9c66f75e78e37514775d3e99a4cc26257fbc4a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfc4d5e3b1f4cd0930bee93f64b4ec3424f8d7612440343d5ac1a417143070ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd6a10e66a39fb8c3e2f45de7bc13e76182ad5163010affec982ae9d706aaca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9ff9f029731a86934748abe585fefe9017ba95e7dea67842cbb2d9dac15cb53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInfoTypes")
    def put_info_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75cb86b716564644722872b9bc46fe71fe6f1f83ecc7807215bc678bd8eee528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInfoTypes", [value]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72c4d28dc055c11bf3f3fab9e2330e0924fe713f53df4e5b2d26cdbdeb98e85b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="resetInfoTypes")
    def reset_info_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfoTypes", []))

    @builtins.property
    @jsii.member(jsii_name="infoTypes")
    def info_types(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesList:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesList, jsii.get(self, "infoTypes"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesList":
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="infoTypesInput")
    def info_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]]], jsii.get(self, "infoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff25af8a54178e1715282b136ef5c2925e39f9f8a8cdf201462aa19654f8816d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules",
    jsii_struct_bases=[],
    name_mapping={"exclusion_rule": "exclusionRule", "hotword_rule": "hotwordRule"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules:
    def __init__(
        self,
        *,
        exclusion_rule: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule", typing.Dict[builtins.str, typing.Any]]] = None,
        hotword_rule: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param exclusion_rule: exclusion_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#exclusion_rule DataLossPreventionJobTrigger#exclusion_rule}
        :param hotword_rule: hotword_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#hotword_rule DataLossPreventionJobTrigger#hotword_rule}
        '''
        if isinstance(exclusion_rule, dict):
            exclusion_rule = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule(**exclusion_rule)
        if isinstance(hotword_rule, dict):
            hotword_rule = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule(**hotword_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__141af0f4e29c379ba8b7bfc89aea1d1d8103af7b548e390e334a6cb938beff25)
            check_type(argname="argument exclusion_rule", value=exclusion_rule, expected_type=type_hints["exclusion_rule"])
            check_type(argname="argument hotword_rule", value=hotword_rule, expected_type=type_hints["hotword_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclusion_rule is not None:
            self._values["exclusion_rule"] = exclusion_rule
        if hotword_rule is not None:
            self._values["hotword_rule"] = hotword_rule

    @builtins.property
    def exclusion_rule(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule"]:
        '''exclusion_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#exclusion_rule DataLossPreventionJobTrigger#exclusion_rule}
        '''
        result = self._values.get("exclusion_rule")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule"], result)

    @builtins.property
    def hotword_rule(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule"]:
        '''hotword_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#hotword_rule DataLossPreventionJobTrigger#hotword_rule}
        '''
        result = self._values.get("hotword_rule")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule",
    jsii_struct_bases=[],
    name_mapping={
        "matching_type": "matchingType",
        "dictionary": "dictionary",
        "exclude_by_hotword": "excludeByHotword",
        "exclude_info_types": "excludeInfoTypes",
        "regex": "regex",
    },
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule:
    def __init__(
        self,
        *,
        matching_type: builtins.str,
        dictionary: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_by_hotword: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_info_types: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes", typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param matching_type: How the rule is applied. See the documentation for more information: https://cloud.google.com/dlp/docs/reference/rest/v2/InspectConfig#MatchingType Possible values: ["MATCHING_TYPE_FULL_MATCH", "MATCHING_TYPE_PARTIAL_MATCH", "MATCHING_TYPE_INVERSE_MATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#matching_type DataLossPreventionJobTrigger#matching_type}
        :param dictionary: dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#dictionary DataLossPreventionJobTrigger#dictionary}
        :param exclude_by_hotword: exclude_by_hotword block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#exclude_by_hotword DataLossPreventionJobTrigger#exclude_by_hotword}
        :param exclude_info_types: exclude_info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#exclude_info_types DataLossPreventionJobTrigger#exclude_info_types}
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#regex DataLossPreventionJobTrigger#regex}
        '''
        if isinstance(dictionary, dict):
            dictionary = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary(**dictionary)
        if isinstance(exclude_by_hotword, dict):
            exclude_by_hotword = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword(**exclude_by_hotword)
        if isinstance(exclude_info_types, dict):
            exclude_info_types = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes(**exclude_info_types)
        if isinstance(regex, dict):
            regex = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex(**regex)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bf747850ea59aa086327b5a75c58fdbb82d0775d86909213bcd2408c5fe8356)
            check_type(argname="argument matching_type", value=matching_type, expected_type=type_hints["matching_type"])
            check_type(argname="argument dictionary", value=dictionary, expected_type=type_hints["dictionary"])
            check_type(argname="argument exclude_by_hotword", value=exclude_by_hotword, expected_type=type_hints["exclude_by_hotword"])
            check_type(argname="argument exclude_info_types", value=exclude_info_types, expected_type=type_hints["exclude_info_types"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "matching_type": matching_type,
        }
        if dictionary is not None:
            self._values["dictionary"] = dictionary
        if exclude_by_hotword is not None:
            self._values["exclude_by_hotword"] = exclude_by_hotword
        if exclude_info_types is not None:
            self._values["exclude_info_types"] = exclude_info_types
        if regex is not None:
            self._values["regex"] = regex

    @builtins.property
    def matching_type(self) -> builtins.str:
        '''How the rule is applied. See the documentation for more information: https://cloud.google.com/dlp/docs/reference/rest/v2/InspectConfig#MatchingType Possible values: ["MATCHING_TYPE_FULL_MATCH", "MATCHING_TYPE_PARTIAL_MATCH", "MATCHING_TYPE_INVERSE_MATCH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#matching_type DataLossPreventionJobTrigger#matching_type}
        '''
        result = self._values.get("matching_type")
        assert result is not None, "Required property 'matching_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dictionary(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary"]:
        '''dictionary block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#dictionary DataLossPreventionJobTrigger#dictionary}
        '''
        result = self._values.get("dictionary")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary"], result)

    @builtins.property
    def exclude_by_hotword(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword"]:
        '''exclude_by_hotword block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#exclude_by_hotword DataLossPreventionJobTrigger#exclude_by_hotword}
        '''
        result = self._values.get("exclude_by_hotword")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword"], result)

    @builtins.property
    def exclude_info_types(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes"]:
        '''exclude_info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#exclude_info_types DataLossPreventionJobTrigger#exclude_info_types}
        '''
        result = self._values.get("exclude_info_types")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes"], result)

    @builtins.property
    def regex(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex"]:
        '''regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#regex DataLossPreventionJobTrigger#regex}
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary",
    jsii_struct_bases=[],
    name_mapping={"cloud_storage_path": "cloudStoragePath", "word_list": "wordList"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary:
    def __init__(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath", typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#cloud_storage_path DataLossPreventionJobTrigger#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#word_list DataLossPreventionJobTrigger#word_list}
        '''
        if isinstance(cloud_storage_path, dict):
            cloud_storage_path = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath(**cloud_storage_path)
        if isinstance(word_list, dict):
            word_list = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct(**word_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e0a2d14b4cabe639b1f3f50b31ce2b1c05f4782bf9d005118703ce97934233)
            check_type(argname="argument cloud_storage_path", value=cloud_storage_path, expected_type=type_hints["cloud_storage_path"])
            check_type(argname="argument word_list", value=word_list, expected_type=type_hints["word_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_storage_path is not None:
            self._values["cloud_storage_path"] = cloud_storage_path
        if word_list is not None:
            self._values["word_list"] = word_list

    @builtins.property
    def cloud_storage_path(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath"]:
        '''cloud_storage_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#cloud_storage_path DataLossPreventionJobTrigger#cloud_storage_path}
        '''
        result = self._values.get("cloud_storage_path")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath"], result)

    @builtins.property
    def word_list(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct"]:
        '''word_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#word_list DataLossPreventionJobTrigger#word_list}
        '''
        result = self._values.get("word_list")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath:
    def __init__(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#path DataLossPreventionJobTrigger#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0495313097caab622fcb9db9621056f320658208b43fbc8e1ecc2b4fbdb5fc7)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#path DataLossPreventionJobTrigger#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33159a7fa740cf7575bcc6694b893c038438a5d20718c7131c6427810e2ea439)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7049d6bf76f52ffdb8e7683aaedba5efc21068d86dd308ef40331ef3e067f417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f380a8afb0b4039889664958da4562ca24f373bf434564eb544a495c6df0ba76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba1ecf53572fa98e70395041a088751e9bd99dc394b7b46f4cb6732633b0a9f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudStoragePath")
    def put_cloud_storage_path(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#path DataLossPreventionJobTrigger#path}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath(
            path=path
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStoragePath", [value]))

    @jsii.member(jsii_name="putWordList")
    def put_word_list(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#words DataLossPreventionJobTrigger#words}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct(
            words=words
        )

        return typing.cast(None, jsii.invoke(self, "putWordList", [value]))

    @jsii.member(jsii_name="resetCloudStoragePath")
    def reset_cloud_storage_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudStoragePath", []))

    @jsii.member(jsii_name="resetWordList")
    def reset_word_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWordList", []))

    @builtins.property
    @jsii.member(jsii_name="cloudStoragePath")
    def cloud_storage_path(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference, jsii.get(self, "cloudStoragePath"))

    @builtins.property
    @jsii.member(jsii_name="wordList")
    def word_list(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference", jsii.get(self, "wordList"))

    @builtins.property
    @jsii.member(jsii_name="cloudStoragePathInput")
    def cloud_storage_path_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath], jsii.get(self, "cloudStoragePathInput"))

    @builtins.property
    @jsii.member(jsii_name="wordListInput")
    def word_list_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct"], jsii.get(self, "wordListInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4b556bbf8b34c2001eb1361dec7c9b965a4e5d95771e4ea3332d79a0c8f782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct",
    jsii_struct_bases=[],
    name_mapping={"words": "words"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct:
    def __init__(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#words DataLossPreventionJobTrigger#words}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__511cb828e74fa8eba8c13c29a4bfab3f18b3e615ac58e23d64d316951f66ffcd)
            check_type(argname="argument words", value=words, expected_type=type_hints["words"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "words": words,
        }

    @builtins.property
    def words(self) -> typing.List[builtins.str]:
        '''Words or phrases defining the dictionary.

        The dictionary must contain at least one
        phrase and every phrase must contain at least 2 characters that are letters or digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#words DataLossPreventionJobTrigger#words}
        '''
        result = self._values.get("words")
        assert result is not None, "Required property 'words' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47fdaca48d3297c210af2f992b463eed59b7635968a50e90b65accafbd1efcc0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="wordsInput")
    def words_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "wordsInput"))

    @builtins.property
    @jsii.member(jsii_name="words")
    def words(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "words"))

    @words.setter
    def words(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a9c52a80ff1cab1e9d93242286f3bd6a91114f238842d752911ef2e9ca37163)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "words", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e76e7d20a70fadb669cb636bbf084179ab8c88c5830365e1501d12fc510e041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword",
    jsii_struct_bases=[],
    name_mapping={"hotword_regex": "hotwordRegex", "proximity": "proximity"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword:
    def __init__(
        self,
        *,
        hotword_regex: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex", typing.Dict[builtins.str, typing.Any]]] = None,
        proximity: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hotword_regex: hotword_regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#hotword_regex DataLossPreventionJobTrigger#hotword_regex}
        :param proximity: proximity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#proximity DataLossPreventionJobTrigger#proximity}
        '''
        if isinstance(hotword_regex, dict):
            hotword_regex = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex(**hotword_regex)
        if isinstance(proximity, dict):
            proximity = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity(**proximity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca73fd91e66edf36d134bb72bf4c579cf1dca764fee73212589b999b6389c693)
            check_type(argname="argument hotword_regex", value=hotword_regex, expected_type=type_hints["hotword_regex"])
            check_type(argname="argument proximity", value=proximity, expected_type=type_hints["proximity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hotword_regex is not None:
            self._values["hotword_regex"] = hotword_regex
        if proximity is not None:
            self._values["proximity"] = proximity

    @builtins.property
    def hotword_regex(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex"]:
        '''hotword_regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#hotword_regex DataLossPreventionJobTrigger#hotword_regex}
        '''
        result = self._values.get("hotword_regex")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex"], result)

    @builtins.property
    def proximity(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity"]:
        '''proximity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#proximity DataLossPreventionJobTrigger#proximity}
        '''
        result = self._values.get("proximity")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex",
    jsii_struct_bases=[],
    name_mapping={"group_indexes": "groupIndexes", "pattern": "pattern"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex:
    def __init__(
        self,
        *,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        pattern: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#group_indexes DataLossPreventionJobTrigger#group_indexes}
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#pattern DataLossPreventionJobTrigger#pattern}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c04693a54f36e21c96d425002cb96289e2a4a8193148bdd71e25df979884358)
            check_type(argname="argument group_indexes", value=group_indexes, expected_type=type_hints["group_indexes"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_indexes is not None:
            self._values["group_indexes"] = group_indexes
        if pattern is not None:
            self._values["pattern"] = pattern

    @builtins.property
    def group_indexes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The index of the submatch to extract as findings.

        When not specified,
        the entire match is returned. No more than 3 may be included.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#group_indexes DataLossPreventionJobTrigger#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#pattern DataLossPreventionJobTrigger#pattern}
        '''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddcd241ea7a08b7e231c33bb50e85e443c0b38ffd87e6ec319d7fc44ebe5831c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGroupIndexes")
    def reset_group_indexes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupIndexes", []))

    @jsii.member(jsii_name="resetPattern")
    def reset_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPattern", []))

    @builtins.property
    @jsii.member(jsii_name="groupIndexesInput")
    def group_indexes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "groupIndexesInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIndexes")
    def group_indexes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "groupIndexes"))

    @group_indexes.setter
    def group_indexes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c65f9e50d5abe69adfd69f739c9534405d83e4d3c0b0fe5eb2cc46abd7d97e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b8c37d66eec2dda494180fc082f8cafae09a1d8954fcd99e1d56751b015d58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5f53ba4737d83f37391a345fd6406e184c29b8303220cdfcbf9051934b33633)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec6705ed408035c54e49f376005c2f158f51f68bcaf2d444d33c2972e65bb7ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHotwordRegex")
    def put_hotword_regex(
        self,
        *,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        pattern: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#group_indexes DataLossPreventionJobTrigger#group_indexes}
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#pattern DataLossPreventionJobTrigger#pattern}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex(
            group_indexes=group_indexes, pattern=pattern
        )

        return typing.cast(None, jsii.invoke(self, "putHotwordRegex", [value]))

    @jsii.member(jsii_name="putProximity")
    def put_proximity(
        self,
        *,
        window_after: typing.Optional[jsii.Number] = None,
        window_before: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param window_after: Number of characters after the finding to consider. Either this or window_before must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#window_after DataLossPreventionJobTrigger#window_after}
        :param window_before: Number of characters before the finding to consider. Either this or window_after must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#window_before DataLossPreventionJobTrigger#window_before}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity(
            window_after=window_after, window_before=window_before
        )

        return typing.cast(None, jsii.invoke(self, "putProximity", [value]))

    @jsii.member(jsii_name="resetHotwordRegex")
    def reset_hotword_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHotwordRegex", []))

    @jsii.member(jsii_name="resetProximity")
    def reset_proximity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProximity", []))

    @builtins.property
    @jsii.member(jsii_name="hotwordRegex")
    def hotword_regex(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference, jsii.get(self, "hotwordRegex"))

    @builtins.property
    @jsii.member(jsii_name="proximity")
    def proximity(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference", jsii.get(self, "proximity"))

    @builtins.property
    @jsii.member(jsii_name="hotwordRegexInput")
    def hotword_regex_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex], jsii.get(self, "hotwordRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="proximityInput")
    def proximity_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity"], jsii.get(self, "proximityInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e0eb09a7ad939979478de961529b5452369806544429064b90f3447f35da71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity",
    jsii_struct_bases=[],
    name_mapping={"window_after": "windowAfter", "window_before": "windowBefore"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity:
    def __init__(
        self,
        *,
        window_after: typing.Optional[jsii.Number] = None,
        window_before: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param window_after: Number of characters after the finding to consider. Either this or window_before must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#window_after DataLossPreventionJobTrigger#window_after}
        :param window_before: Number of characters before the finding to consider. Either this or window_after must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#window_before DataLossPreventionJobTrigger#window_before}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__311486ead1fb7f8065d7bfdc315419db6bf5c90d201b4c6717b37d5099fd111f)
            check_type(argname="argument window_after", value=window_after, expected_type=type_hints["window_after"])
            check_type(argname="argument window_before", value=window_before, expected_type=type_hints["window_before"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if window_after is not None:
            self._values["window_after"] = window_after
        if window_before is not None:
            self._values["window_before"] = window_before

    @builtins.property
    def window_after(self) -> typing.Optional[jsii.Number]:
        '''Number of characters after the finding to consider. Either this or window_before must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#window_after DataLossPreventionJobTrigger#window_after}
        '''
        result = self._values.get("window_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def window_before(self) -> typing.Optional[jsii.Number]:
        '''Number of characters before the finding to consider. Either this or window_after must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#window_before DataLossPreventionJobTrigger#window_before}
        '''
        result = self._values.get("window_before")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__101f24ca526afca1621251458b8cef5224f07090d6c05a231b59b640eddd3cc6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetWindowAfter")
    def reset_window_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowAfter", []))

    @jsii.member(jsii_name="resetWindowBefore")
    def reset_window_before(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowBefore", []))

    @builtins.property
    @jsii.member(jsii_name="windowAfterInput")
    def window_after_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "windowAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="windowBeforeInput")
    def window_before_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "windowBeforeInput"))

    @builtins.property
    @jsii.member(jsii_name="windowAfter")
    def window_after(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "windowAfter"))

    @window_after.setter
    def window_after(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e3f4a222d8fba381db2d5201f9c3aae9a160e853bac057b40d600fbf2fbf8a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="windowBefore")
    def window_before(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "windowBefore"))

    @window_before.setter
    def window_before(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8e9da0e539063c427cc358bd02fec3186d9b698320d8858b984287312c60c14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c4e7ef91db4367bbdf9fda782501bde86567a24a3e6565a27d13e4dae684735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes",
    jsii_struct_bases=[],
    name_mapping={"info_types": "infoTypes"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes:
    def __init__(
        self,
        *,
        info_types: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#info_types DataLossPreventionJobTrigger#info_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e5155b24183f83eb6f8ffcc251577c1618c9d1f883c5046d1e9ab4a0768732)
            check_type(argname="argument info_types", value=info_types, expected_type=type_hints["info_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "info_types": info_types,
        }

    @builtins.property
    def info_types(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes"]]:
        '''info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#info_types DataLossPreventionJobTrigger#info_types}
        '''
        result = self._values.get("info_types")
        assert result is not None, "Required property 'info_types' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sensitivity_score DataLossPreventionJobTrigger#sensitivity_score}
        :param version: Version of the information type to use. By default, the version is set to stable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#version DataLossPreventionJobTrigger#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__593ebadeda94e0da3612116e78a18fcd77a17818ee5f3453ad28448710163351)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sensitivity_score", value=sensitivity_score, expected_type=type_hints["sensitivity_score"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if sensitivity_score is not None:
            self._values["sensitivity_score"] = sensitivity_score
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the information type.

        Either a name of your choosing when creating a CustomInfoType, or one of the names listed
        at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sensitivity_score DataLossPreventionJobTrigger#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the information type to use. By default, the version is set to stable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#version DataLossPreventionJobTrigger#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db3c25a25e74395826bfeda239b4535ddd638bc11b80bfdc0fc9697861f1236e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96f22ddd647acfd367e38c136f75428dc6df4e06493508ca369f8b8a441b7bb6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdb369f8b0eaf71b1fdbb2db110d5149f2b1ec417fdce4b563734f95134d9d8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f16a21b2d121f8a283361037c74a0ed0c27ce4faa0e5dccc88a126c682e7a51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b424c508ec48f7a8d5c9278deff79fb7fb2879962c05390d0343ab61f73da28f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c8b0cb3abc042f751325d2d25c013e941473303a73c86d160b9009ba991357)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f724cf76d4554a464f7d8777cc4753d77332b5ef76e8fea37a3a2bb65c663dc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore(
            score=score
        )

        return typing.cast(None, jsii.invoke(self, "putSensitivityScore", [value]))

    @jsii.member(jsii_name="resetSensitivityScore")
    def reset_sensitivity_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitivityScore", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScore")
    def sensitivity_score(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1a0e5a92b81fb2fbc57ea5d8efe4fc99b6c735e1ec52ef208d054ec8aac639b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d434c9a810fbce1d88147dec12369b413a89e179f8ccceec2ebe4e55df39cd9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8520385706c0fd21faadc81c96f06365bb3ecb62319fc30a5262a04a532bb642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7a3ee04f9359bfca2107226e5abd2309ae90d1058370eff75a52e013aaeec89)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#score DataLossPreventionJobTrigger#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__def539c2f553d3902ae3c632e11bc0ea017f33ebf887a0cbd6314f37ae9ab817)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scoreInput")
    def score_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scoreInput"))

    @builtins.property
    @jsii.member(jsii_name="score")
    def score(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "score"))

    @score.setter
    def score(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b04d1d5708bd00cf7494d00cb8e953aeb0fd0f9c1e75ecca819f95651a030e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd00ce3c8d1639a0d7b991f75bf980cf209dd761150eca3731e9754b4f2079f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15e47e213dc0608c7e01bc1170a2d768c0fc3b12a248ab2c9dfca5f25bfc1f78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInfoTypes")
    def put_info_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ddf483bf47a398bffcd68ba78fff11b7e07afac56b51b98fbd435616aca217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInfoTypes", [value]))

    @builtins.property
    @jsii.member(jsii_name="infoTypes")
    def info_types(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList, jsii.get(self, "infoTypes"))

    @builtins.property
    @jsii.member(jsii_name="infoTypesInput")
    def info_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]], jsii.get(self, "infoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af8689baa6133780305bc15e0dae015d1868bf441e4c29f91ed39849ebb7c1e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__468c2d57ebe79761a68aa06215924e85f1fd35d2b719d5c1132de011a2191639)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDictionary")
    def put_dictionary(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#cloud_storage_path DataLossPreventionJobTrigger#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#word_list DataLossPreventionJobTrigger#word_list}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary(
            cloud_storage_path=cloud_storage_path, word_list=word_list
        )

        return typing.cast(None, jsii.invoke(self, "putDictionary", [value]))

    @jsii.member(jsii_name="putExcludeByHotword")
    def put_exclude_by_hotword(
        self,
        *,
        hotword_regex: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex, typing.Dict[builtins.str, typing.Any]]] = None,
        proximity: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hotword_regex: hotword_regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#hotword_regex DataLossPreventionJobTrigger#hotword_regex}
        :param proximity: proximity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#proximity DataLossPreventionJobTrigger#proximity}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword(
            hotword_regex=hotword_regex, proximity=proximity
        )

        return typing.cast(None, jsii.invoke(self, "putExcludeByHotword", [value]))

    @jsii.member(jsii_name="putExcludeInfoTypes")
    def put_exclude_info_types(
        self,
        *,
        info_types: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#info_types DataLossPreventionJobTrigger#info_types}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes(
            info_types=info_types
        )

        return typing.cast(None, jsii.invoke(self, "putExcludeInfoTypes", [value]))

    @jsii.member(jsii_name="putRegex")
    def put_regex(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#pattern DataLossPreventionJobTrigger#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#group_indexes DataLossPreventionJobTrigger#group_indexes}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex(
            pattern=pattern, group_indexes=group_indexes
        )

        return typing.cast(None, jsii.invoke(self, "putRegex", [value]))

    @jsii.member(jsii_name="resetDictionary")
    def reset_dictionary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDictionary", []))

    @jsii.member(jsii_name="resetExcludeByHotword")
    def reset_exclude_by_hotword(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeByHotword", []))

    @jsii.member(jsii_name="resetExcludeInfoTypes")
    def reset_exclude_info_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeInfoTypes", []))

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @builtins.property
    @jsii.member(jsii_name="dictionary")
    def dictionary(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference, jsii.get(self, "dictionary"))

    @builtins.property
    @jsii.member(jsii_name="excludeByHotword")
    def exclude_by_hotword(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference, jsii.get(self, "excludeByHotword"))

    @builtins.property
    @jsii.member(jsii_name="excludeInfoTypes")
    def exclude_info_types(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference, jsii.get(self, "excludeInfoTypes"))

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegexOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegexOutputReference", jsii.get(self, "regex"))

    @builtins.property
    @jsii.member(jsii_name="dictionaryInput")
    def dictionary_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary], jsii.get(self, "dictionaryInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeByHotwordInput")
    def exclude_by_hotword_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword], jsii.get(self, "excludeByHotwordInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeInfoTypesInput")
    def exclude_info_types_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes], jsii.get(self, "excludeInfoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="matchingTypeInput")
    def matching_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchingTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex"], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="matchingType")
    def matching_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchingType"))

    @matching_type.setter
    def matching_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78685fdc50ef82fece492c45cdb71b58e4c5a97461b060aaaa25d22e3fd63d4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchingType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a7af0c5bb2277495473ad6449820c983319fe07b10b015bdc29156790c8232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern", "group_indexes": "groupIndexes"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex:
    def __init__(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#pattern DataLossPreventionJobTrigger#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#group_indexes DataLossPreventionJobTrigger#group_indexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64561f008526c9dfa704c8fc01a40b0a97967055194490f23fb98800f275d634)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument group_indexes", value=group_indexes, expected_type=type_hints["group_indexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pattern": pattern,
        }
        if group_indexes is not None:
            self._values["group_indexes"] = group_indexes

    @builtins.property
    def pattern(self) -> builtins.str:
        '''Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#pattern DataLossPreventionJobTrigger#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_indexes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The index of the submatch to extract as findings.

        When not specified, the entire match is returned. No more than 3 may be included.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#group_indexes DataLossPreventionJobTrigger#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__645d801aa9b79a1f5a5dd5b7a1b9ec1e8cbd19e7455935a27acaf90f8fe8ce29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGroupIndexes")
    def reset_group_indexes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupIndexes", []))

    @builtins.property
    @jsii.member(jsii_name="groupIndexesInput")
    def group_indexes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "groupIndexesInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIndexes")
    def group_indexes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "groupIndexes"))

    @group_indexes.setter
    def group_indexes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19c56cff3cbd39dcb4f81ab8d025d0ca239a49823be4adb84a5c9659c26e265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b6003e55df238bc9e89002ad54657deb4e8f61485f640318c428ef80e4ed1ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc66eacbc97c9019efc7d0ce1457b66d25cdbfa7c8085850290a6067841bb03a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule",
    jsii_struct_bases=[],
    name_mapping={
        "hotword_regex": "hotwordRegex",
        "likelihood_adjustment": "likelihoodAdjustment",
        "proximity": "proximity",
    },
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule:
    def __init__(
        self,
        *,
        hotword_regex: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex", typing.Dict[builtins.str, typing.Any]]] = None,
        likelihood_adjustment: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment", typing.Dict[builtins.str, typing.Any]]] = None,
        proximity: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hotword_regex: hotword_regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#hotword_regex DataLossPreventionJobTrigger#hotword_regex}
        :param likelihood_adjustment: likelihood_adjustment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#likelihood_adjustment DataLossPreventionJobTrigger#likelihood_adjustment}
        :param proximity: proximity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#proximity DataLossPreventionJobTrigger#proximity}
        '''
        if isinstance(hotword_regex, dict):
            hotword_regex = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex(**hotword_regex)
        if isinstance(likelihood_adjustment, dict):
            likelihood_adjustment = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment(**likelihood_adjustment)
        if isinstance(proximity, dict):
            proximity = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity(**proximity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5d6e1a8a0fbd2798ba91cba0a252574cc8e6f8857cd28cb02a1ddc04a65879d)
            check_type(argname="argument hotword_regex", value=hotword_regex, expected_type=type_hints["hotword_regex"])
            check_type(argname="argument likelihood_adjustment", value=likelihood_adjustment, expected_type=type_hints["likelihood_adjustment"])
            check_type(argname="argument proximity", value=proximity, expected_type=type_hints["proximity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hotword_regex is not None:
            self._values["hotword_regex"] = hotword_regex
        if likelihood_adjustment is not None:
            self._values["likelihood_adjustment"] = likelihood_adjustment
        if proximity is not None:
            self._values["proximity"] = proximity

    @builtins.property
    def hotword_regex(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex"]:
        '''hotword_regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#hotword_regex DataLossPreventionJobTrigger#hotword_regex}
        '''
        result = self._values.get("hotword_regex")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex"], result)

    @builtins.property
    def likelihood_adjustment(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment"]:
        '''likelihood_adjustment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#likelihood_adjustment DataLossPreventionJobTrigger#likelihood_adjustment}
        '''
        result = self._values.get("likelihood_adjustment")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment"], result)

    @builtins.property
    def proximity(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity"]:
        '''proximity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#proximity DataLossPreventionJobTrigger#proximity}
        '''
        result = self._values.get("proximity")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex",
    jsii_struct_bases=[],
    name_mapping={"group_indexes": "groupIndexes", "pattern": "pattern"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex:
    def __init__(
        self,
        *,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        pattern: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#group_indexes DataLossPreventionJobTrigger#group_indexes}
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#pattern DataLossPreventionJobTrigger#pattern}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__232a0a93ca8d5279e99d650eb95c179472c96d41e9643604209d3e78f425c69d)
            check_type(argname="argument group_indexes", value=group_indexes, expected_type=type_hints["group_indexes"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_indexes is not None:
            self._values["group_indexes"] = group_indexes
        if pattern is not None:
            self._values["pattern"] = pattern

    @builtins.property
    def group_indexes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The index of the submatch to extract as findings.

        When not specified,
        the entire match is returned. No more than 3 may be included.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#group_indexes DataLossPreventionJobTrigger#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#pattern DataLossPreventionJobTrigger#pattern}
        '''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34e5fb307cdb9e73f16f919e7267a04a31458f229591cd6419ed78d052a6e067)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGroupIndexes")
    def reset_group_indexes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupIndexes", []))

    @jsii.member(jsii_name="resetPattern")
    def reset_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPattern", []))

    @builtins.property
    @jsii.member(jsii_name="groupIndexesInput")
    def group_indexes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "groupIndexesInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIndexes")
    def group_indexes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "groupIndexes"))

    @group_indexes.setter
    def group_indexes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1362c3d96581afc2873d2f2cca164ea8fba0f0137cedc5f868e1ff3da413c38b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dcf52ebc4ea159934faeb50cb50096f5b53cdcee05e731d971c5752e15ca73f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dad06133fe82eabd3f38ce9c3051ad6e3013d1cf1c76c6331bd404f7eedba3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment",
    jsii_struct_bases=[],
    name_mapping={
        "fixed_likelihood": "fixedLikelihood",
        "relative_likelihood": "relativeLikelihood",
    },
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment:
    def __init__(
        self,
        *,
        fixed_likelihood: typing.Optional[builtins.str] = None,
        relative_likelihood: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed_likelihood: Set the likelihood of a finding to a fixed value. Either this or relative_likelihood can be set. Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#fixed_likelihood DataLossPreventionJobTrigger#fixed_likelihood}
        :param relative_likelihood: Increase or decrease the likelihood by the specified number of levels. For example, if a finding would be POSSIBLE without the detection rule and relativeLikelihood is 1, then it is upgraded to LIKELY, while a value of -1 would downgrade it to UNLIKELY. Likelihood may never drop below VERY_UNLIKELY or exceed VERY_LIKELY, so applying an adjustment of 1 followed by an adjustment of -1 when base likelihood is VERY_LIKELY will result in a final likelihood of LIKELY. Either this or fixed_likelihood can be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#relative_likelihood DataLossPreventionJobTrigger#relative_likelihood}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd97bbb9fe4818a97072f9be69ea77ec08ebd12733b4b2e1b460f24ce6cb21c1)
            check_type(argname="argument fixed_likelihood", value=fixed_likelihood, expected_type=type_hints["fixed_likelihood"])
            check_type(argname="argument relative_likelihood", value=relative_likelihood, expected_type=type_hints["relative_likelihood"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fixed_likelihood is not None:
            self._values["fixed_likelihood"] = fixed_likelihood
        if relative_likelihood is not None:
            self._values["relative_likelihood"] = relative_likelihood

    @builtins.property
    def fixed_likelihood(self) -> typing.Optional[builtins.str]:
        '''Set the likelihood of a finding to a fixed value.

        Either this or relative_likelihood can be set. Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#fixed_likelihood DataLossPreventionJobTrigger#fixed_likelihood}
        '''
        result = self._values.get("fixed_likelihood")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def relative_likelihood(self) -> typing.Optional[jsii.Number]:
        '''Increase or decrease the likelihood by the specified number of levels.

        For example,
        if a finding would be POSSIBLE without the detection rule and relativeLikelihood is 1,
        then it is upgraded to LIKELY, while a value of -1 would downgrade it to UNLIKELY.
        Likelihood may never drop below VERY_UNLIKELY or exceed VERY_LIKELY, so applying an
        adjustment of 1 followed by an adjustment of -1 when base likelihood is VERY_LIKELY
        will result in a final likelihood of LIKELY. Either this or fixed_likelihood can be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#relative_likelihood DataLossPreventionJobTrigger#relative_likelihood}
        '''
        result = self._values.get("relative_likelihood")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84ee1fc014c590fad8f3a5a798ab4676c7aa3fe0211d4012ba42bea3894e2b77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFixedLikelihood")
    def reset_fixed_likelihood(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedLikelihood", []))

    @jsii.member(jsii_name="resetRelativeLikelihood")
    def reset_relative_likelihood(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelativeLikelihood", []))

    @builtins.property
    @jsii.member(jsii_name="fixedLikelihoodInput")
    def fixed_likelihood_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fixedLikelihoodInput"))

    @builtins.property
    @jsii.member(jsii_name="relativeLikelihoodInput")
    def relative_likelihood_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "relativeLikelihoodInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedLikelihood")
    def fixed_likelihood(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fixedLikelihood"))

    @fixed_likelihood.setter
    def fixed_likelihood(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdad3865c93b9c1903a2c7358ac9913df551293749ce7bad7ffd26885a1dcf74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedLikelihood", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="relativeLikelihood")
    def relative_likelihood(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "relativeLikelihood"))

    @relative_likelihood.setter
    def relative_likelihood(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6f4ddcecdd4243c1044f051003d67531f307d60bf8fdbffdb050ef3bea38df0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relativeLikelihood", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f40416f7161b93bbf5188844a895973871d6c23ed221b1b470cfc53f8b3463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43f93ae0f0b91a4fff7d3d894da6f14bb37f14466a6e72b74f5a7847b8fb1b1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHotwordRegex")
    def put_hotword_regex(
        self,
        *,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        pattern: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#group_indexes DataLossPreventionJobTrigger#group_indexes}
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#pattern DataLossPreventionJobTrigger#pattern}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex(
            group_indexes=group_indexes, pattern=pattern
        )

        return typing.cast(None, jsii.invoke(self, "putHotwordRegex", [value]))

    @jsii.member(jsii_name="putLikelihoodAdjustment")
    def put_likelihood_adjustment(
        self,
        *,
        fixed_likelihood: typing.Optional[builtins.str] = None,
        relative_likelihood: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed_likelihood: Set the likelihood of a finding to a fixed value. Either this or relative_likelihood can be set. Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#fixed_likelihood DataLossPreventionJobTrigger#fixed_likelihood}
        :param relative_likelihood: Increase or decrease the likelihood by the specified number of levels. For example, if a finding would be POSSIBLE without the detection rule and relativeLikelihood is 1, then it is upgraded to LIKELY, while a value of -1 would downgrade it to UNLIKELY. Likelihood may never drop below VERY_UNLIKELY or exceed VERY_LIKELY, so applying an adjustment of 1 followed by an adjustment of -1 when base likelihood is VERY_LIKELY will result in a final likelihood of LIKELY. Either this or fixed_likelihood can be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#relative_likelihood DataLossPreventionJobTrigger#relative_likelihood}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment(
            fixed_likelihood=fixed_likelihood, relative_likelihood=relative_likelihood
        )

        return typing.cast(None, jsii.invoke(self, "putLikelihoodAdjustment", [value]))

    @jsii.member(jsii_name="putProximity")
    def put_proximity(
        self,
        *,
        window_after: typing.Optional[jsii.Number] = None,
        window_before: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param window_after: Number of characters after the finding to consider. Either this or window_before must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#window_after DataLossPreventionJobTrigger#window_after}
        :param window_before: Number of characters before the finding to consider. Either this or window_after must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#window_before DataLossPreventionJobTrigger#window_before}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity(
            window_after=window_after, window_before=window_before
        )

        return typing.cast(None, jsii.invoke(self, "putProximity", [value]))

    @jsii.member(jsii_name="resetHotwordRegex")
    def reset_hotword_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHotwordRegex", []))

    @jsii.member(jsii_name="resetLikelihoodAdjustment")
    def reset_likelihood_adjustment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLikelihoodAdjustment", []))

    @jsii.member(jsii_name="resetProximity")
    def reset_proximity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProximity", []))

    @builtins.property
    @jsii.member(jsii_name="hotwordRegex")
    def hotword_regex(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference, jsii.get(self, "hotwordRegex"))

    @builtins.property
    @jsii.member(jsii_name="likelihoodAdjustment")
    def likelihood_adjustment(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference, jsii.get(self, "likelihoodAdjustment"))

    @builtins.property
    @jsii.member(jsii_name="proximity")
    def proximity(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximityOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximityOutputReference", jsii.get(self, "proximity"))

    @builtins.property
    @jsii.member(jsii_name="hotwordRegexInput")
    def hotword_regex_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex], jsii.get(self, "hotwordRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="likelihoodAdjustmentInput")
    def likelihood_adjustment_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment], jsii.get(self, "likelihoodAdjustmentInput"))

    @builtins.property
    @jsii.member(jsii_name="proximityInput")
    def proximity_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity"], jsii.get(self, "proximityInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd991012bd4f7f7e77b04db9f0eada7571ca63d6f6532d5344c783ad21adea2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity",
    jsii_struct_bases=[],
    name_mapping={"window_after": "windowAfter", "window_before": "windowBefore"},
)
class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity:
    def __init__(
        self,
        *,
        window_after: typing.Optional[jsii.Number] = None,
        window_before: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param window_after: Number of characters after the finding to consider. Either this or window_before must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#window_after DataLossPreventionJobTrigger#window_after}
        :param window_before: Number of characters before the finding to consider. Either this or window_after must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#window_before DataLossPreventionJobTrigger#window_before}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5056326d50e95bd147ae0e77500a4795659cfe15ee2272cd95cc8ef1190fa5ac)
            check_type(argname="argument window_after", value=window_after, expected_type=type_hints["window_after"])
            check_type(argname="argument window_before", value=window_before, expected_type=type_hints["window_before"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if window_after is not None:
            self._values["window_after"] = window_after
        if window_before is not None:
            self._values["window_before"] = window_before

    @builtins.property
    def window_after(self) -> typing.Optional[jsii.Number]:
        '''Number of characters after the finding to consider. Either this or window_before must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#window_after DataLossPreventionJobTrigger#window_after}
        '''
        result = self._values.get("window_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def window_before(self) -> typing.Optional[jsii.Number]:
        '''Number of characters before the finding to consider. Either this or window_after must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#window_before DataLossPreventionJobTrigger#window_before}
        '''
        result = self._values.get("window_before")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eda93fff612ee0e72ab43573742b658f2a7f4246fc93e6acb7018b128fc3a1e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetWindowAfter")
    def reset_window_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowAfter", []))

    @jsii.member(jsii_name="resetWindowBefore")
    def reset_window_before(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowBefore", []))

    @builtins.property
    @jsii.member(jsii_name="windowAfterInput")
    def window_after_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "windowAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="windowBeforeInput")
    def window_before_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "windowBeforeInput"))

    @builtins.property
    @jsii.member(jsii_name="windowAfter")
    def window_after(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "windowAfter"))

    @window_after.setter
    def window_after(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__296462049ded22fc18f38cc9fdb1acc2f38ce0b66b4a96f623f5ace5ba84dca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="windowBefore")
    def window_before(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "windowBefore"))

    @window_before.setter
    def window_before(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0911a98ace54b2c82d332869b534ba1a3d0d521fb70fe94a6330936818b69ccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__916a2dd63824b1b761edb85b64ddb8e35c9d19a991db245f37d56900fcab5e0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27fe38c537115945de744b598495a011604c7f568eeba5def450a7ab04972877)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773483eee3ccc5e67f33cdd0176524af4f75dcbe17372f2f2e11742ce5725003)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c2e0e43693afada709fea4a3838b3a04db589d17be2de03cbc5c8469447e5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e5eb8260c14db2ae84dcb774675289c616bac475aa747a11aa954644c5ddad5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7e0cbce2312362ae0fd3453f5fec6f80069b4ba64f745535b8e280e6d5aaf57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c761731a6549f50ec50b309b22fa4fc6e3c79100605105f3520c9c6a64cd2c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb8a22bc5b687831c9e849c665d506ea1ba59cde3c5b669a97fc5ce1b6174cf5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExclusionRule")
    def put_exclusion_rule(
        self,
        *,
        matching_type: builtins.str,
        dictionary: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_by_hotword: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword, typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_info_types: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes, typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param matching_type: How the rule is applied. See the documentation for more information: https://cloud.google.com/dlp/docs/reference/rest/v2/InspectConfig#MatchingType Possible values: ["MATCHING_TYPE_FULL_MATCH", "MATCHING_TYPE_PARTIAL_MATCH", "MATCHING_TYPE_INVERSE_MATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#matching_type DataLossPreventionJobTrigger#matching_type}
        :param dictionary: dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#dictionary DataLossPreventionJobTrigger#dictionary}
        :param exclude_by_hotword: exclude_by_hotword block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#exclude_by_hotword DataLossPreventionJobTrigger#exclude_by_hotword}
        :param exclude_info_types: exclude_info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#exclude_info_types DataLossPreventionJobTrigger#exclude_info_types}
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#regex DataLossPreventionJobTrigger#regex}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule(
            matching_type=matching_type,
            dictionary=dictionary,
            exclude_by_hotword=exclude_by_hotword,
            exclude_info_types=exclude_info_types,
            regex=regex,
        )

        return typing.cast(None, jsii.invoke(self, "putExclusionRule", [value]))

    @jsii.member(jsii_name="putHotwordRule")
    def put_hotword_rule(
        self,
        *,
        hotword_regex: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex, typing.Dict[builtins.str, typing.Any]]] = None,
        likelihood_adjustment: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment, typing.Dict[builtins.str, typing.Any]]] = None,
        proximity: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hotword_regex: hotword_regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#hotword_regex DataLossPreventionJobTrigger#hotword_regex}
        :param likelihood_adjustment: likelihood_adjustment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#likelihood_adjustment DataLossPreventionJobTrigger#likelihood_adjustment}
        :param proximity: proximity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#proximity DataLossPreventionJobTrigger#proximity}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule(
            hotword_regex=hotword_regex,
            likelihood_adjustment=likelihood_adjustment,
            proximity=proximity,
        )

        return typing.cast(None, jsii.invoke(self, "putHotwordRule", [value]))

    @jsii.member(jsii_name="resetExclusionRule")
    def reset_exclusion_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusionRule", []))

    @jsii.member(jsii_name="resetHotwordRule")
    def reset_hotword_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHotwordRule", []))

    @builtins.property
    @jsii.member(jsii_name="exclusionRule")
    def exclusion_rule(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleOutputReference, jsii.get(self, "exclusionRule"))

    @builtins.property
    @jsii.member(jsii_name="hotwordRule")
    def hotword_rule(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleOutputReference, jsii.get(self, "hotwordRule"))

    @builtins.property
    @jsii.member(jsii_name="exclusionRuleInput")
    def exclusion_rule_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule], jsii.get(self, "exclusionRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="hotwordRuleInput")
    def hotword_rule_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule], jsii.get(self, "hotwordRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d35718fcb798d08fd77909429d50d8f1f6382b623e726d77259483ae77d5b582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec7071be60c2d58e05dba9408ed68729a748231ee78a53b29d177d26f05d2fd7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobActions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7da076ed92da1adf7277063e431fc9c376ff73a1ebb7eea64b3926db157a2a65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putInspectConfig")
    def put_inspect_config(
        self,
        *,
        custom_info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
        exclude_info_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_quote: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
        limits: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigLimits, typing.Dict[builtins.str, typing.Any]]] = None,
        min_likelihood: typing.Optional[builtins.str] = None,
        rule_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param custom_info_types: custom_info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#custom_info_types DataLossPreventionJobTrigger#custom_info_types}
        :param exclude_info_types: When true, excludes type information of the findings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#exclude_info_types DataLossPreventionJobTrigger#exclude_info_types}
        :param include_quote: When true, a contextual quote from the data that triggered a finding is included in the response. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#include_quote DataLossPreventionJobTrigger#include_quote}
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#info_types DataLossPreventionJobTrigger#info_types}
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#limits DataLossPreventionJobTrigger#limits}
        :param min_likelihood: Only returns findings equal or above this threshold. See https://cloud.google.com/dlp/docs/likelihood for more info Default value: "POSSIBLE" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#min_likelihood DataLossPreventionJobTrigger#min_likelihood}
        :param rule_set: rule_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#rule_set DataLossPreventionJobTrigger#rule_set}
        '''
        value = DataLossPreventionJobTriggerInspectJobInspectConfig(
            custom_info_types=custom_info_types,
            exclude_info_types=exclude_info_types,
            include_quote=include_quote,
            info_types=info_types,
            limits=limits,
            min_likelihood=min_likelihood,
            rule_set=rule_set,
        )

        return typing.cast(None, jsii.invoke(self, "putInspectConfig", [value]))

    @jsii.member(jsii_name="putStorageConfig")
    def put_storage_config(
        self,
        *,
        big_query_options: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_storage_options: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        datastore_options: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        hybrid_options: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timespan_config: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param big_query_options: big_query_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#big_query_options DataLossPreventionJobTrigger#big_query_options}
        :param cloud_storage_options: cloud_storage_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#cloud_storage_options DataLossPreventionJobTrigger#cloud_storage_options}
        :param datastore_options: datastore_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#datastore_options DataLossPreventionJobTrigger#datastore_options}
        :param hybrid_options: hybrid_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#hybrid_options DataLossPreventionJobTrigger#hybrid_options}
        :param timespan_config: timespan_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#timespan_config DataLossPreventionJobTrigger#timespan_config}
        '''
        value = DataLossPreventionJobTriggerInspectJobStorageConfig(
            big_query_options=big_query_options,
            cloud_storage_options=cloud_storage_options,
            datastore_options=datastore_options,
            hybrid_options=hybrid_options,
            timespan_config=timespan_config,
        )

        return typing.cast(None, jsii.invoke(self, "putStorageConfig", [value]))

    @jsii.member(jsii_name="resetActions")
    def reset_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActions", []))

    @jsii.member(jsii_name="resetInspectConfig")
    def reset_inspect_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInspectConfig", []))

    @jsii.member(jsii_name="resetInspectTemplateName")
    def reset_inspect_template_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInspectTemplateName", []))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> DataLossPreventionJobTriggerInspectJobActionsList:
        return typing.cast(DataLossPreventionJobTriggerInspectJobActionsList, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="inspectConfig")
    def inspect_config(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobInspectConfigOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobInspectConfigOutputReference, jsii.get(self, "inspectConfig"))

    @builtins.property
    @jsii.member(jsii_name="storageConfig")
    def storage_config(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobStorageConfigOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobStorageConfigOutputReference", jsii.get(self, "storageConfig"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobActions]]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="inspectConfigInput")
    def inspect_config_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfig]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfig], jsii.get(self, "inspectConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="inspectTemplateNameInput")
    def inspect_template_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inspectTemplateNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageConfigInput")
    def storage_config_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfig"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfig"], jsii.get(self, "storageConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="inspectTemplateName")
    def inspect_template_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inspectTemplateName"))

    @inspect_template_name.setter
    def inspect_template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc7a02a4a03d9bb34b9a29e7b93d5e0b84f4cd1dfffce9d7d16e40edd2de89d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspectTemplateName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataLossPreventionJobTriggerInspectJob]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13e845766785f892c48068ccda86d520bc99db7801c48fbff10d4b780a2d884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfig",
    jsii_struct_bases=[],
    name_mapping={
        "big_query_options": "bigQueryOptions",
        "cloud_storage_options": "cloudStorageOptions",
        "datastore_options": "datastoreOptions",
        "hybrid_options": "hybridOptions",
        "timespan_config": "timespanConfig",
    },
)
class DataLossPreventionJobTriggerInspectJobStorageConfig:
    def __init__(
        self,
        *,
        big_query_options: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_storage_options: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        datastore_options: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        hybrid_options: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timespan_config: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param big_query_options: big_query_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#big_query_options DataLossPreventionJobTrigger#big_query_options}
        :param cloud_storage_options: cloud_storage_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#cloud_storage_options DataLossPreventionJobTrigger#cloud_storage_options}
        :param datastore_options: datastore_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#datastore_options DataLossPreventionJobTrigger#datastore_options}
        :param hybrid_options: hybrid_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#hybrid_options DataLossPreventionJobTrigger#hybrid_options}
        :param timespan_config: timespan_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#timespan_config DataLossPreventionJobTrigger#timespan_config}
        '''
        if isinstance(big_query_options, dict):
            big_query_options = DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions(**big_query_options)
        if isinstance(cloud_storage_options, dict):
            cloud_storage_options = DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions(**cloud_storage_options)
        if isinstance(datastore_options, dict):
            datastore_options = DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions(**datastore_options)
        if isinstance(hybrid_options, dict):
            hybrid_options = DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions(**hybrid_options)
        if isinstance(timespan_config, dict):
            timespan_config = DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig(**timespan_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5631a1e7ba7b8629a1e43aa2e37133f51e7d38ce95521d3842cbcabbac1c8740)
            check_type(argname="argument big_query_options", value=big_query_options, expected_type=type_hints["big_query_options"])
            check_type(argname="argument cloud_storage_options", value=cloud_storage_options, expected_type=type_hints["cloud_storage_options"])
            check_type(argname="argument datastore_options", value=datastore_options, expected_type=type_hints["datastore_options"])
            check_type(argname="argument hybrid_options", value=hybrid_options, expected_type=type_hints["hybrid_options"])
            check_type(argname="argument timespan_config", value=timespan_config, expected_type=type_hints["timespan_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if big_query_options is not None:
            self._values["big_query_options"] = big_query_options
        if cloud_storage_options is not None:
            self._values["cloud_storage_options"] = cloud_storage_options
        if datastore_options is not None:
            self._values["datastore_options"] = datastore_options
        if hybrid_options is not None:
            self._values["hybrid_options"] = hybrid_options
        if timespan_config is not None:
            self._values["timespan_config"] = timespan_config

    @builtins.property
    def big_query_options(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions"]:
        '''big_query_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#big_query_options DataLossPreventionJobTrigger#big_query_options}
        '''
        result = self._values.get("big_query_options")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions"], result)

    @builtins.property
    def cloud_storage_options(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions"]:
        '''cloud_storage_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#cloud_storage_options DataLossPreventionJobTrigger#cloud_storage_options}
        '''
        result = self._values.get("cloud_storage_options")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions"], result)

    @builtins.property
    def datastore_options(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions"]:
        '''datastore_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#datastore_options DataLossPreventionJobTrigger#datastore_options}
        '''
        result = self._values.get("datastore_options")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions"], result)

    @builtins.property
    def hybrid_options(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions"]:
        '''hybrid_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#hybrid_options DataLossPreventionJobTrigger#hybrid_options}
        '''
        result = self._values.get("hybrid_options")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions"], result)

    @builtins.property
    def timespan_config(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig"]:
        '''timespan_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#timespan_config DataLossPreventionJobTrigger#timespan_config}
        '''
        result = self._values.get("timespan_config")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobStorageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions",
    jsii_struct_bases=[],
    name_mapping={
        "table_reference": "tableReference",
        "excluded_fields": "excludedFields",
        "identifying_fields": "identifyingFields",
        "included_fields": "includedFields",
        "rows_limit": "rowsLimit",
        "rows_limit_percent": "rowsLimitPercent",
        "sample_method": "sampleMethod",
    },
)
class DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions:
    def __init__(
        self,
        *,
        table_reference: typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference", typing.Dict[builtins.str, typing.Any]],
        excluded_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        identifying_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        included_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rows_limit: typing.Optional[jsii.Number] = None,
        rows_limit_percent: typing.Optional[jsii.Number] = None,
        sample_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table_reference: table_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table_reference DataLossPreventionJobTrigger#table_reference}
        :param excluded_fields: excluded_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#excluded_fields DataLossPreventionJobTrigger#excluded_fields}
        :param identifying_fields: identifying_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#identifying_fields DataLossPreventionJobTrigger#identifying_fields}
        :param included_fields: included_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#included_fields DataLossPreventionJobTrigger#included_fields}
        :param rows_limit: Max number of rows to scan. If the table has more rows than this value, the rest of the rows are omitted. If not set, or if set to 0, all rows will be scanned. Only one of rowsLimit and rowsLimitPercent can be specified. Cannot be used in conjunction with TimespanConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#rows_limit DataLossPreventionJobTrigger#rows_limit}
        :param rows_limit_percent: Max percentage of rows to scan. The rest are omitted. The number of rows scanned is rounded down. Must be between 0 and 100, inclusively. Both 0 and 100 means no limit. Defaults to 0. Only one of rowsLimit and rowsLimitPercent can be specified. Cannot be used in conjunction with TimespanConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#rows_limit_percent DataLossPreventionJobTrigger#rows_limit_percent}
        :param sample_method: How to sample rows if not all rows are scanned. Meaningful only when used in conjunction with either rowsLimit or rowsLimitPercent. If not specified, rows are scanned in the order BigQuery reads them. If TimespanConfig is set, set this to an empty string to avoid using the default value. Default value: "TOP" Possible values: ["TOP", "RANDOM_START"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sample_method DataLossPreventionJobTrigger#sample_method}
        '''
        if isinstance(table_reference, dict):
            table_reference = DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference(**table_reference)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e50d8ea420e5dc3b8272132e2134d7d30037d9661926c178b1d7c0981c245493)
            check_type(argname="argument table_reference", value=table_reference, expected_type=type_hints["table_reference"])
            check_type(argname="argument excluded_fields", value=excluded_fields, expected_type=type_hints["excluded_fields"])
            check_type(argname="argument identifying_fields", value=identifying_fields, expected_type=type_hints["identifying_fields"])
            check_type(argname="argument included_fields", value=included_fields, expected_type=type_hints["included_fields"])
            check_type(argname="argument rows_limit", value=rows_limit, expected_type=type_hints["rows_limit"])
            check_type(argname="argument rows_limit_percent", value=rows_limit_percent, expected_type=type_hints["rows_limit_percent"])
            check_type(argname="argument sample_method", value=sample_method, expected_type=type_hints["sample_method"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table_reference": table_reference,
        }
        if excluded_fields is not None:
            self._values["excluded_fields"] = excluded_fields
        if identifying_fields is not None:
            self._values["identifying_fields"] = identifying_fields
        if included_fields is not None:
            self._values["included_fields"] = included_fields
        if rows_limit is not None:
            self._values["rows_limit"] = rows_limit
        if rows_limit_percent is not None:
            self._values["rows_limit_percent"] = rows_limit_percent
        if sample_method is not None:
            self._values["sample_method"] = sample_method

    @builtins.property
    def table_reference(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference":
        '''table_reference block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table_reference DataLossPreventionJobTrigger#table_reference}
        '''
        result = self._values.get("table_reference")
        assert result is not None, "Required property 'table_reference' is missing"
        return typing.cast("DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference", result)

    @builtins.property
    def excluded_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields"]]]:
        '''excluded_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#excluded_fields DataLossPreventionJobTrigger#excluded_fields}
        '''
        result = self._values.get("excluded_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields"]]], result)

    @builtins.property
    def identifying_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields"]]]:
        '''identifying_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#identifying_fields DataLossPreventionJobTrigger#identifying_fields}
        '''
        result = self._values.get("identifying_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields"]]], result)

    @builtins.property
    def included_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields"]]]:
        '''included_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#included_fields DataLossPreventionJobTrigger#included_fields}
        '''
        result = self._values.get("included_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields"]]], result)

    @builtins.property
    def rows_limit(self) -> typing.Optional[jsii.Number]:
        '''Max number of rows to scan.

        If the table has more rows than this value, the rest of the rows are omitted.
        If not set, or if set to 0, all rows will be scanned. Only one of rowsLimit and rowsLimitPercent can be
        specified. Cannot be used in conjunction with TimespanConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#rows_limit DataLossPreventionJobTrigger#rows_limit}
        '''
        result = self._values.get("rows_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rows_limit_percent(self) -> typing.Optional[jsii.Number]:
        '''Max percentage of rows to scan.

        The rest are omitted. The number of rows scanned is rounded down.
        Must be between 0 and 100, inclusively. Both 0 and 100 means no limit. Defaults to 0. Only one of
        rowsLimit and rowsLimitPercent can be specified. Cannot be used in conjunction with TimespanConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#rows_limit_percent DataLossPreventionJobTrigger#rows_limit_percent}
        '''
        result = self._values.get("rows_limit_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sample_method(self) -> typing.Optional[builtins.str]:
        '''How to sample rows if not all rows are scanned.

        Meaningful only when used in conjunction with either
        rowsLimit or rowsLimitPercent. If not specified, rows are scanned in the order BigQuery reads them.
        If TimespanConfig is set, set this to an empty string to avoid using the default value. Default value: "TOP" Possible values: ["TOP", "RANDOM_START"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sample_method DataLossPreventionJobTrigger#sample_method}
        '''
        result = self._values.get("sample_method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Name describing the field excluded from scanning. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44df9c250d0ab0232018c2053f448cb5892c7b8b051bd871883269519bfbbf1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name describing the field excluded from scanning.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96cb20e7089f8ddbcc252953f2749d30e4aeb120a272056079a8e0c0851fdb7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6153bc734c7c46f37cb205d30ffd7282f4acb23d6b9d1e01ab43708576a990bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69288cf810acd2a39342eb22b417d7cff2f22bc74e4421e8f38bcfc37ced411c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__179d71453101b4f9e81319765ed7939923d6aad7de9c7e8cf406b45fb0266cb7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1c720adcd1d52cc33abdd52a5ac51ff60386e759753b9b45483df982743c20f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a130e52d548fda849e77b23ca1da84a80d2f7fb02f3fd602ba08f0ba8eeb88cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b3e22da972fc9b55972fb2768d06377c1ea0704ac0d27ffe28362b723413982)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d484cdbed11e59ce86649c653660ee8fd75a4c81f1c9bc4f8c55826f5506e28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91e57ad2c6e8c22fe05c5484c38bcee46b3caaa72b5249288877ab1b28522a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Name of a BigQuery field to be returned with the findings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8aed41bc5dcdaf15f587e0dfb1016882d57229899784baaf59295ca1b776043)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of a BigQuery field to be returned with the findings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f77a2f5742920a184b8ab323294232d8ed22ab88bda237090784aa785ac20eaa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9c33ef5e5ea98afb9be2c2cc7bf940ffbc9da8cca66dd5b6ff564b3ffd7106e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d92b8ebcf96957003babab1dce17a71058b18fce18b6c57c88946cc5e24cde75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dae119dd05fbd18834145b0112c2b69c130e585870d1f649087cd9b38b7765ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7a77d3df0ee01725f5f6592429808277c062b0209c3989231940325c823a746)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aedc99601aaa146e963176be07e5596c4c75a23b62c1a20ff2ddd03e1a98b7ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab5f2787d8a3ef0151545f4c6c53a7d3dbc4b1d4de8eebbca9d5b14cebd51bcc)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5b22123283512591724520dcaaded827656eb79554fb0e21cf4d5db888108f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a202d7eab59ca86f80964f2e7193cee7b4810602f8bc33cd0314ddeae33676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Name describing the field to which scanning is limited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826741c544bcdc3838ca7f483b6e1049c86bf5f902cc039cde2bc42c6c17cf9d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name describing the field to which scanning is limited.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea7a8faeaf2b652c4a3d675f6d228b5cdb84d5877e96afeabb95e87cc1a6aca2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fde4e2ad116472e6c629bbf42ca131a6ceaa193eddac0c69d0b33b2e5e75dbdb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd17db4c690e489047d53d71cbe2a1cca75aa940ef6728db3ae7f2ff653d9ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a81959d33b4ab97bc1f872a4e19bd3448765fbc7c635ee0bdaf211ace596b29a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef626f6ba0cb8afabf528cc6a32172b8d3a56c559eddbe656b86daaae50fcf92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52940cd4b432e1f3c022d91fb555ec9ba40837ea0347f6220506be6933d69435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c3f5b484da2449ab447e40b04b9c0d12f53d378f74a804ea29db3f7ee9b7586)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9daeeab52cdf6975105671fb510ef8095001675df6a098261512c2a61178f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df9c7a8c640f2d92a13cfd14753854eb54d1b175f4371e145439a24c2199e37d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__486f3bef08a251a25eeed9d83e8bfb2929d7bda078f6d42ebb614db9dd894a05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExcludedFields")
    def put_excluded_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac70960f86a974559193f30fd85db2901887bd7d9a1c914a2ee59fa90b90cdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExcludedFields", [value]))

    @jsii.member(jsii_name="putIdentifyingFields")
    def put_identifying_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a755144e0887b780436293f89c3cace809d18f7c3ff8009ed1230db0e4c91416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIdentifyingFields", [value]))

    @jsii.member(jsii_name="putIncludedFields")
    def put_included_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__896807be04309ca3ac6ad199f75fef553ec127ad07670a3431c629ac894c4192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIncludedFields", [value]))

    @jsii.member(jsii_name="putTableReference")
    def put_table_reference(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The dataset ID of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#dataset_id DataLossPreventionJobTrigger#dataset_id}
        :param project_id: The Google Cloud Platform project ID of the project containing the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#project_id DataLossPreventionJobTrigger#project_id}
        :param table_id: The name of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table_id DataLossPreventionJobTrigger#table_id}
        '''
        value = DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference(
            dataset_id=dataset_id, project_id=project_id, table_id=table_id
        )

        return typing.cast(None, jsii.invoke(self, "putTableReference", [value]))

    @jsii.member(jsii_name="resetExcludedFields")
    def reset_excluded_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedFields", []))

    @jsii.member(jsii_name="resetIdentifyingFields")
    def reset_identifying_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentifyingFields", []))

    @jsii.member(jsii_name="resetIncludedFields")
    def reset_included_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedFields", []))

    @jsii.member(jsii_name="resetRowsLimit")
    def reset_rows_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowsLimit", []))

    @jsii.member(jsii_name="resetRowsLimitPercent")
    def reset_rows_limit_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowsLimitPercent", []))

    @jsii.member(jsii_name="resetSampleMethod")
    def reset_sample_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleMethod", []))

    @builtins.property
    @jsii.member(jsii_name="excludedFields")
    def excluded_fields(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsList:
        return typing.cast(DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsList, jsii.get(self, "excludedFields"))

    @builtins.property
    @jsii.member(jsii_name="identifyingFields")
    def identifying_fields(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsList:
        return typing.cast(DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsList, jsii.get(self, "identifyingFields"))

    @builtins.property
    @jsii.member(jsii_name="includedFields")
    def included_fields(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsList:
        return typing.cast(DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsList, jsii.get(self, "includedFields"))

    @builtins.property
    @jsii.member(jsii_name="tableReference")
    def table_reference(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReferenceOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReferenceOutputReference", jsii.get(self, "tableReference"))

    @builtins.property
    @jsii.member(jsii_name="excludedFieldsInput")
    def excluded_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]]], jsii.get(self, "excludedFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="identifyingFieldsInput")
    def identifying_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]]], jsii.get(self, "identifyingFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedFieldsInput")
    def included_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]]], jsii.get(self, "includedFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="rowsLimitInput")
    def rows_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowsLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="rowsLimitPercentInput")
    def rows_limit_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowsLimitPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleMethodInput")
    def sample_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sampleMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="tableReferenceInput")
    def table_reference_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference"], jsii.get(self, "tableReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="rowsLimit")
    def rows_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rowsLimit"))

    @rows_limit.setter
    def rows_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0158d00685d10786619b723798455bf08f0c47e40329a8470e004b5035685b3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowsLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rowsLimitPercent")
    def rows_limit_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rowsLimitPercent"))

    @rows_limit_percent.setter
    def rows_limit_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85fed7c33e0468b66c7533b24a10229e0653768f9d5a86af955a687b1c174695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowsLimitPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleMethod")
    def sample_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sampleMethod"))

    @sample_method.setter
    def sample_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7bd83cbeded8ee9338f28dcd6eea51845d454099765561d91a233a0e6f03401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__847d35ac49804ae39fbce9b2751e512fa321f09932bf361e109d685f19133c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id": "datasetId",
        "project_id": "projectId",
        "table_id": "tableId",
    },
)
class DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference:
    def __init__(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The dataset ID of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#dataset_id DataLossPreventionJobTrigger#dataset_id}
        :param project_id: The Google Cloud Platform project ID of the project containing the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#project_id DataLossPreventionJobTrigger#project_id}
        :param table_id: The name of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table_id DataLossPreventionJobTrigger#table_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a565838b92a3f8f8968616b733e807ad977c20a9566c89b7f4dba910ec6df33e)
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
            "project_id": project_id,
            "table_id": table_id,
        }

    @builtins.property
    def dataset_id(self) -> builtins.str:
        '''The dataset ID of the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#dataset_id DataLossPreventionJobTrigger#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The Google Cloud Platform project ID of the project containing the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#project_id DataLossPreventionJobTrigger#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_id(self) -> builtins.str:
        '''The name of the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table_id DataLossPreventionJobTrigger#table_id}
        '''
        result = self._values.get("table_id")
        assert result is not None, "Required property 'table_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e43222f1a0f79744329c8157b44db4a41a872d9c6fcf628125c4aaba748ec7fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tableIdInput")
    def table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9d4524a8b497145e1c96718c5cfc493735f8f2f54b1b1e1cb4ea096a03ed50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edee9d259d7676666f33327d9a09b282fb46bf0c49a95a6fb85f06432575ce7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c520d4aafa71ffb55806ac2893c445cbe26950a9dbf953024127dbf1efce0dc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d16b5860e6f6409ca66f807223ff6ad3dda6d864f47bd1a106d5c7b9bb67184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions",
    jsii_struct_bases=[],
    name_mapping={
        "file_set": "fileSet",
        "bytes_limit_per_file": "bytesLimitPerFile",
        "bytes_limit_per_file_percent": "bytesLimitPerFilePercent",
        "files_limit_percent": "filesLimitPercent",
        "file_types": "fileTypes",
        "sample_method": "sampleMethod",
    },
)
class DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions:
    def __init__(
        self,
        *,
        file_set: typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet", typing.Dict[builtins.str, typing.Any]],
        bytes_limit_per_file: typing.Optional[jsii.Number] = None,
        bytes_limit_per_file_percent: typing.Optional[jsii.Number] = None,
        files_limit_percent: typing.Optional[jsii.Number] = None,
        file_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        sample_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_set: file_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#file_set DataLossPreventionJobTrigger#file_set}
        :param bytes_limit_per_file: Max number of bytes to scan from a file. If a scanned file's size is bigger than this value then the rest of the bytes are omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#bytes_limit_per_file DataLossPreventionJobTrigger#bytes_limit_per_file}
        :param bytes_limit_per_file_percent: Max percentage of bytes to scan from a file. The rest are omitted. The number of bytes scanned is rounded down. Must be between 0 and 100, inclusively. Both 0 and 100 means no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#bytes_limit_per_file_percent DataLossPreventionJobTrigger#bytes_limit_per_file_percent}
        :param files_limit_percent: Limits the number of files to scan to this percentage of the input FileSet. Number of files scanned is rounded down. Must be between 0 and 100, inclusively. Both 0 and 100 means no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#files_limit_percent DataLossPreventionJobTrigger#files_limit_percent}
        :param file_types: List of file type groups to include in the scan. If empty, all files are scanned and available data format processors are applied. In addition, the binary content of the selected files is always scanned as well. Images are scanned only as binary if the specified region does not support image inspection and no fileTypes were specified. Possible values: ["BINARY_FILE", "TEXT_FILE", "IMAGE", "WORD", "PDF", "AVRO", "CSV", "TSV", "POWERPOINT", "EXCEL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#file_types DataLossPreventionJobTrigger#file_types}
        :param sample_method: How to sample bytes if not all bytes are scanned. Meaningful only when used in conjunction with bytesLimitPerFile. If not specified, scanning would start from the top. Possible values: ["TOP", "RANDOM_START"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sample_method DataLossPreventionJobTrigger#sample_method}
        '''
        if isinstance(file_set, dict):
            file_set = DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet(**file_set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5201ca36b738d7d66a0fefa4b040f8d5e82cb614b65fd3bcc8a221cf71083b9c)
            check_type(argname="argument file_set", value=file_set, expected_type=type_hints["file_set"])
            check_type(argname="argument bytes_limit_per_file", value=bytes_limit_per_file, expected_type=type_hints["bytes_limit_per_file"])
            check_type(argname="argument bytes_limit_per_file_percent", value=bytes_limit_per_file_percent, expected_type=type_hints["bytes_limit_per_file_percent"])
            check_type(argname="argument files_limit_percent", value=files_limit_percent, expected_type=type_hints["files_limit_percent"])
            check_type(argname="argument file_types", value=file_types, expected_type=type_hints["file_types"])
            check_type(argname="argument sample_method", value=sample_method, expected_type=type_hints["sample_method"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_set": file_set,
        }
        if bytes_limit_per_file is not None:
            self._values["bytes_limit_per_file"] = bytes_limit_per_file
        if bytes_limit_per_file_percent is not None:
            self._values["bytes_limit_per_file_percent"] = bytes_limit_per_file_percent
        if files_limit_percent is not None:
            self._values["files_limit_percent"] = files_limit_percent
        if file_types is not None:
            self._values["file_types"] = file_types
        if sample_method is not None:
            self._values["sample_method"] = sample_method

    @builtins.property
    def file_set(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet":
        '''file_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#file_set DataLossPreventionJobTrigger#file_set}
        '''
        result = self._values.get("file_set")
        assert result is not None, "Required property 'file_set' is missing"
        return typing.cast("DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet", result)

    @builtins.property
    def bytes_limit_per_file(self) -> typing.Optional[jsii.Number]:
        '''Max number of bytes to scan from a file.

        If a scanned file's size is bigger than this value
        then the rest of the bytes are omitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#bytes_limit_per_file DataLossPreventionJobTrigger#bytes_limit_per_file}
        '''
        result = self._values.get("bytes_limit_per_file")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bytes_limit_per_file_percent(self) -> typing.Optional[jsii.Number]:
        '''Max percentage of bytes to scan from a file.

        The rest are omitted. The number of bytes scanned is rounded down.
        Must be between 0 and 100, inclusively. Both 0 and 100 means no limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#bytes_limit_per_file_percent DataLossPreventionJobTrigger#bytes_limit_per_file_percent}
        '''
        result = self._values.get("bytes_limit_per_file_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def files_limit_percent(self) -> typing.Optional[jsii.Number]:
        '''Limits the number of files to scan to this percentage of the input FileSet.

        Number of files scanned is rounded down.
        Must be between 0 and 100, inclusively. Both 0 and 100 means no limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#files_limit_percent DataLossPreventionJobTrigger#files_limit_percent}
        '''
        result = self._values.get("files_limit_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def file_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of file type groups to include in the scan.

        If empty, all files are scanned and available data
        format processors are applied. In addition, the binary content of the selected files is always scanned as well.
        Images are scanned only as binary if the specified region does not support image inspection and no fileTypes were specified. Possible values: ["BINARY_FILE", "TEXT_FILE", "IMAGE", "WORD", "PDF", "AVRO", "CSV", "TSV", "POWERPOINT", "EXCEL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#file_types DataLossPreventionJobTrigger#file_types}
        '''
        result = self._values.get("file_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sample_method(self) -> typing.Optional[builtins.str]:
        '''How to sample bytes if not all bytes are scanned.

        Meaningful only when used in conjunction with bytesLimitPerFile.
        If not specified, scanning would start from the top. Possible values: ["TOP", "RANDOM_START"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sample_method DataLossPreventionJobTrigger#sample_method}
        '''
        result = self._values.get("sample_method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet",
    jsii_struct_bases=[],
    name_mapping={"regex_file_set": "regexFileSet", "url": "url"},
)
class DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet:
    def __init__(
        self,
        *,
        regex_file_set: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet", typing.Dict[builtins.str, typing.Any]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param regex_file_set: regex_file_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#regex_file_set DataLossPreventionJobTrigger#regex_file_set}
        :param url: The Cloud Storage url of the file(s) to scan, in the format 'gs:///'. Trailing wildcard in the path is allowed. If the url ends in a trailing slash, the bucket or directory represented by the url will be scanned non-recursively (content in sub-directories will not be scanned). This means that 'gs://mybucket/' is equivalent to 'gs://mybucket/*', and 'gs://mybucket/directory/' is equivalent to 'gs://mybucket/directory/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#url DataLossPreventionJobTrigger#url}
        '''
        if isinstance(regex_file_set, dict):
            regex_file_set = DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet(**regex_file_set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eff0852ad366ae639dab9934ce0c52fa1f78b64c14778e59fb5e0b5ffc89668)
            check_type(argname="argument regex_file_set", value=regex_file_set, expected_type=type_hints["regex_file_set"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if regex_file_set is not None:
            self._values["regex_file_set"] = regex_file_set
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def regex_file_set(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet"]:
        '''regex_file_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#regex_file_set DataLossPreventionJobTrigger#regex_file_set}
        '''
        result = self._values.get("regex_file_set")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet"], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage url of the file(s) to scan, in the format 'gs:///'. Trailing wildcard in the path is allowed.

        If the url ends in a trailing slash, the bucket or directory represented by the url will be scanned
        non-recursively (content in sub-directories will not be scanned). This means that 'gs://mybucket/' is
        equivalent to 'gs://mybucket/*', and 'gs://mybucket/directory/' is equivalent to 'gs://mybucket/directory/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#url DataLossPreventionJobTrigger#url}
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7386c246e6d12616bad223c96008c5ec6481874cd82b06ace3e4f31c26a07024)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRegexFileSet")
    def put_regex_file_set(
        self,
        *,
        bucket_name: builtins.str,
        exclude_regex: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_regex: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param bucket_name: The name of a Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#bucket_name DataLossPreventionJobTrigger#bucket_name}
        :param exclude_regex: A list of regular expressions matching file paths to exclude. All files in the bucket that match at least one of these regular expressions will be excluded from the scan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#exclude_regex DataLossPreventionJobTrigger#exclude_regex}
        :param include_regex: A list of regular expressions matching file paths to include. All files in the bucket that match at least one of these regular expressions will be included in the set of files, except for those that also match an item in excludeRegex. Leaving this field empty will match all files by default (this is equivalent to including .* in the list) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#include_regex DataLossPreventionJobTrigger#include_regex}
        '''
        value = DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet(
            bucket_name=bucket_name,
            exclude_regex=exclude_regex,
            include_regex=include_regex,
        )

        return typing.cast(None, jsii.invoke(self, "putRegexFileSet", [value]))

    @jsii.member(jsii_name="resetRegexFileSet")
    def reset_regex_file_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegexFileSet", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="regexFileSet")
    def regex_file_set(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSetOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSetOutputReference", jsii.get(self, "regexFileSet"))

    @builtins.property
    @jsii.member(jsii_name="regexFileSetInput")
    def regex_file_set_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet"], jsii.get(self, "regexFileSetInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0403c9361a77e2cc97fb2c3b00e41a64bcb329ad88d3f2f621ca7d7f6e7c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1d6466a4fff94e847398a4798bb87acd5ef07020265558a23e722f439fdeaad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "exclude_regex": "excludeRegex",
        "include_regex": "includeRegex",
    },
)
class DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        exclude_regex: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_regex: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param bucket_name: The name of a Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#bucket_name DataLossPreventionJobTrigger#bucket_name}
        :param exclude_regex: A list of regular expressions matching file paths to exclude. All files in the bucket that match at least one of these regular expressions will be excluded from the scan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#exclude_regex DataLossPreventionJobTrigger#exclude_regex}
        :param include_regex: A list of regular expressions matching file paths to include. All files in the bucket that match at least one of these regular expressions will be included in the set of files, except for those that also match an item in excludeRegex. Leaving this field empty will match all files by default (this is equivalent to including .* in the list) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#include_regex DataLossPreventionJobTrigger#include_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c543a2260660828e712ac7a10f46f30c6003cca98a4a4ffd2d6b153c25ed4e77)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument exclude_regex", value=exclude_regex, expected_type=type_hints["exclude_regex"])
            check_type(argname="argument include_regex", value=include_regex, expected_type=type_hints["include_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if exclude_regex is not None:
            self._values["exclude_regex"] = exclude_regex
        if include_regex is not None:
            self._values["include_regex"] = include_regex

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''The name of a Cloud Storage bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#bucket_name DataLossPreventionJobTrigger#bucket_name}
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exclude_regex(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of regular expressions matching file paths to exclude.

        All files in the bucket that match at
        least one of these regular expressions will be excluded from the scan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#exclude_regex DataLossPreventionJobTrigger#exclude_regex}
        '''
        result = self._values.get("exclude_regex")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_regex(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of regular expressions matching file paths to include.

        All files in the bucket
        that match at least one of these regular expressions will be included in the set of files,
        except for those that also match an item in excludeRegex. Leaving this field empty will
        match all files by default (this is equivalent to including .* in the list)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#include_regex DataLossPreventionJobTrigger#include_regex}
        '''
        result = self._values.get("include_regex")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33a8eff3e084fd057f87c3862ae6efbcf127d46338211f2e97a9a442cf8bc33c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludeRegex")
    def reset_exclude_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeRegex", []))

    @jsii.member(jsii_name="resetIncludeRegex")
    def reset_include_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeRegex", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeRegexInput")
    def exclude_regex_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="includeRegexInput")
    def include_regex_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d2a3d8bd9d29ea50316cbee1a65607b89598844149d117d7a86252e1ce63701)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeRegex")
    def exclude_regex(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeRegex"))

    @exclude_regex.setter
    def exclude_regex(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d7ac59a0f47821791453a60e78e8a988ea596700ad69888cce6832ec7b33308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeRegex")
    def include_regex(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeRegex"))

    @include_regex.setter
    def include_regex(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe817851ee09704574fe6e08bec52f521cbc2dddf73dc747a2e0173681b7437a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c88ff1f0bdf6fe88ad6d5d3eb934d67d716569a5a4dddb2131aa326012ffca65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb4e6e2e443638bab5ba843891fb2f9deca0df0d263da6e96d20d73337c8af37)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFileSet")
    def put_file_set(
        self,
        *,
        regex_file_set: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet, typing.Dict[builtins.str, typing.Any]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param regex_file_set: regex_file_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#regex_file_set DataLossPreventionJobTrigger#regex_file_set}
        :param url: The Cloud Storage url of the file(s) to scan, in the format 'gs:///'. Trailing wildcard in the path is allowed. If the url ends in a trailing slash, the bucket or directory represented by the url will be scanned non-recursively (content in sub-directories will not be scanned). This means that 'gs://mybucket/' is equivalent to 'gs://mybucket/*', and 'gs://mybucket/directory/' is equivalent to 'gs://mybucket/directory/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#url DataLossPreventionJobTrigger#url}
        '''
        value = DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet(
            regex_file_set=regex_file_set, url=url
        )

        return typing.cast(None, jsii.invoke(self, "putFileSet", [value]))

    @jsii.member(jsii_name="resetBytesLimitPerFile")
    def reset_bytes_limit_per_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBytesLimitPerFile", []))

    @jsii.member(jsii_name="resetBytesLimitPerFilePercent")
    def reset_bytes_limit_per_file_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBytesLimitPerFilePercent", []))

    @jsii.member(jsii_name="resetFilesLimitPercent")
    def reset_files_limit_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilesLimitPercent", []))

    @jsii.member(jsii_name="resetFileTypes")
    def reset_file_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileTypes", []))

    @jsii.member(jsii_name="resetSampleMethod")
    def reset_sample_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleMethod", []))

    @builtins.property
    @jsii.member(jsii_name="fileSet")
    def file_set(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetOutputReference, jsii.get(self, "fileSet"))

    @builtins.property
    @jsii.member(jsii_name="bytesLimitPerFileInput")
    def bytes_limit_per_file_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bytesLimitPerFileInput"))

    @builtins.property
    @jsii.member(jsii_name="bytesLimitPerFilePercentInput")
    def bytes_limit_per_file_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bytesLimitPerFilePercentInput"))

    @builtins.property
    @jsii.member(jsii_name="fileSetInput")
    def file_set_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet], jsii.get(self, "fileSetInput"))

    @builtins.property
    @jsii.member(jsii_name="filesLimitPercentInput")
    def files_limit_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "filesLimitPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="fileTypesInput")
    def file_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fileTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleMethodInput")
    def sample_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sampleMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="bytesLimitPerFile")
    def bytes_limit_per_file(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bytesLimitPerFile"))

    @bytes_limit_per_file.setter
    def bytes_limit_per_file(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283189c107f08b5664dbc6f2a6ae9c29ea384494e29caa38514257f3fba087d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bytesLimitPerFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bytesLimitPerFilePercent")
    def bytes_limit_per_file_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bytesLimitPerFilePercent"))

    @bytes_limit_per_file_percent.setter
    def bytes_limit_per_file_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__474db9724b6902584d411cf6b5da384b38d2c29ac0ba7831d40b83d447f99dd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bytesLimitPerFilePercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filesLimitPercent")
    def files_limit_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "filesLimitPercent"))

    @files_limit_percent.setter
    def files_limit_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__649b2aab6a2be44b203d0d500179394a32e3cf73bd545374517b67704e487dab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filesLimitPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileTypes")
    def file_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileTypes"))

    @file_types.setter
    def file_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__365d24a8ec6c9034d3ee3dfcc1ccfe0ad9f2b089fefd68b25ee55ccd13503383)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleMethod")
    def sample_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sampleMethod"))

    @sample_method.setter
    def sample_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37cd5f0a739aa6edd834bf829d8ea2b16295a28019ebcf77381455f4b71ee99e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf76135e4d3b3019d109b7039f5ab7cc358d1d3a743c34d2bf088c14ce89d4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions",
    jsii_struct_bases=[],
    name_mapping={"kind": "kind", "partition_id": "partitionId"},
)
class DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions:
    def __init__(
        self,
        *,
        kind: typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind", typing.Dict[builtins.str, typing.Any]],
        partition_id: typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param kind: kind block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#kind DataLossPreventionJobTrigger#kind}
        :param partition_id: partition_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#partition_id DataLossPreventionJobTrigger#partition_id}
        '''
        if isinstance(kind, dict):
            kind = DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind(**kind)
        if isinstance(partition_id, dict):
            partition_id = DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId(**partition_id)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__597727aa02f003240ea9ffbf1077e7e345e9f5d548c15d32347c5cf783e7f8a0)
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument partition_id", value=partition_id, expected_type=type_hints["partition_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kind": kind,
            "partition_id": partition_id,
        }

    @builtins.property
    def kind(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind":
        '''kind block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#kind DataLossPreventionJobTrigger#kind}
        '''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast("DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind", result)

    @builtins.property
    def partition_id(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId":
        '''partition_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#partition_id DataLossPreventionJobTrigger#partition_id}
        '''
        result = self._values.get("partition_id")
        assert result is not None, "Required property 'partition_id' is missing"
        return typing.cast("DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: The name of the Datastore kind. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2446ff69bd94fed85e96731f806044fd5a7085b477122d3691dc978c6ca077d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Datastore kind.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKindOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKindOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2323c3fe06f1fc921c7f0b83d10d5797c7ba7d864b7aee4820658be3db8ee392)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89178dd72cf01f0ced4f3eea041f6a1c45fc8f413c8ba4c3bd5262d0ea96bb68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__790e9e9fc12592f337a4ab72f6a03fa5ea1b49e73e54cc49f9dcfd1ad40a3bd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3b7fee56752994df9b1b6664efcd890733c26fd117c0a82466f9b1a976c4200)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putKind")
    def put_kind(self, *, name: builtins.str) -> None:
        '''
        :param name: The name of the Datastore kind. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        value = DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putKind", [value]))

    @jsii.member(jsii_name="putPartitionId")
    def put_partition_id(
        self,
        *,
        project_id: builtins.str,
        namespace_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project_id: The ID of the project to which the entities belong. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#project_id DataLossPreventionJobTrigger#project_id}
        :param namespace_id: If not empty, the ID of the namespace to which the entities belong. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#namespace_id DataLossPreventionJobTrigger#namespace_id}
        '''
        value = DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId(
            project_id=project_id, namespace_id=namespace_id
        )

        return typing.cast(None, jsii.invoke(self, "putPartitionId", [value]))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKindOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKindOutputReference, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="partitionId")
    def partition_id(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionIdOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionIdOutputReference", jsii.get(self, "partitionId"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionIdInput")
    def partition_id_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId"], jsii.get(self, "partitionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637a3ebd86bec5cc4fdb172a4ae63fe0c7b2a7f26ab8cbc4aaaa6ba846919df5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId",
    jsii_struct_bases=[],
    name_mapping={"project_id": "projectId", "namespace_id": "namespaceId"},
)
class DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId:
    def __init__(
        self,
        *,
        project_id: builtins.str,
        namespace_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project_id: The ID of the project to which the entities belong. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#project_id DataLossPreventionJobTrigger#project_id}
        :param namespace_id: If not empty, the ID of the namespace to which the entities belong. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#namespace_id DataLossPreventionJobTrigger#namespace_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__980cee053092abf3a2639c25ff1c0df72af1d7d701b292647b59bfcb033d9d20)
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument namespace_id", value=namespace_id, expected_type=type_hints["namespace_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project_id": project_id,
        }
        if namespace_id is not None:
            self._values["namespace_id"] = namespace_id

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The ID of the project to which the entities belong.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#project_id DataLossPreventionJobTrigger#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace_id(self) -> typing.Optional[builtins.str]:
        '''If not empty, the ID of the namespace to which the entities belong.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#namespace_id DataLossPreventionJobTrigger#namespace_id}
        '''
        result = self._values.get("namespace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5622f3a8cc549c8fd33535d5ebba9bbf593a901eabc0a912687a8096264f392)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNamespaceId")
    def reset_namespace_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespaceId", []))

    @builtins.property
    @jsii.member(jsii_name="namespaceIdInput")
    def namespace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespaceId"))

    @namespace_id.setter
    def namespace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5c00cb38231c3e51f7b92ce38320f6c5fb19f511f2e8853a4af5300c26cce8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc56fe39d6ae179a01a3b8b29ae875a242e860e366eb7fe9e908047c152e7a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20aab045cf9bc841ac3800f4faa5c1eb542add12c899d46616aa735aaf54a171)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "labels": "labels",
        "required_finding_label_keys": "requiredFindingLabelKeys",
        "table_options": "tableOptions",
    },
)
class DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        required_finding_label_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        table_options: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param description: A short description of where the data is coming from. Will be stored once in the job. 256 max length. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#description DataLossPreventionJobTrigger#description}
        :param labels: To organize findings, these labels will be added to each finding. Label keys must be between 1 and 63 characters long and must conform to the following regular expression: '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?'. Label values must be between 0 and 63 characters long and must conform to the regular expression '(`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?)?'. No more than 10 labels can be associated with a given finding. Examples: - '"environment" : "production"' - '"pipeline" : "etl"' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#labels DataLossPreventionJobTrigger#labels}
        :param required_finding_label_keys: These are labels that each inspection request must include within their 'finding_labels' map. Request may contain others, but any missing one of these will be rejected. Label keys must be between 1 and 63 characters long and must conform to the following regular expression: '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?'. No more than 10 keys can be required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#required_finding_label_keys DataLossPreventionJobTrigger#required_finding_label_keys}
        :param table_options: table_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table_options DataLossPreventionJobTrigger#table_options}
        '''
        if isinstance(table_options, dict):
            table_options = DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions(**table_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8690c33e8712ec2414faeffeb63a91835d07aae56a6c521c97e28b1a7b5f325)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument required_finding_label_keys", value=required_finding_label_keys, expected_type=type_hints["required_finding_label_keys"])
            check_type(argname="argument table_options", value=table_options, expected_type=type_hints["table_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if labels is not None:
            self._values["labels"] = labels
        if required_finding_label_keys is not None:
            self._values["required_finding_label_keys"] = required_finding_label_keys
        if table_options is not None:
            self._values["table_options"] = table_options

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A short description of where the data is coming from.

        Will be stored once in the job. 256 max length.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#description DataLossPreventionJobTrigger#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''To organize findings, these labels will be added to each finding.

        Label keys must be between 1 and 63 characters long and must conform to the following regular expression: '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?'.

        Label values must be between 0 and 63 characters long and must conform to the regular expression '(`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?)?'.

        No more than 10 labels can be associated with a given finding.

        Examples:

        - '"environment" : "production"'
        - '"pipeline" : "etl"'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#labels DataLossPreventionJobTrigger#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def required_finding_label_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''These are labels that each inspection request must include within their 'finding_labels' map.

        Request
        may contain others, but any missing one of these will be rejected.

        Label keys must be between 1 and 63 characters long and must conform to the following regular expression: '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?'.

        No more than 10 keys can be required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#required_finding_label_keys DataLossPreventionJobTrigger#required_finding_label_keys}
        '''
        result = self._values.get("required_finding_label_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def table_options(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions"]:
        '''table_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table_options DataLossPreventionJobTrigger#table_options}
        '''
        result = self._values.get("table_options")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e526ba03795a4dd5ab7272e93802546b9ba4def87884dcf4c3a9a2ef2199d82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTableOptions")
    def put_table_options(
        self,
        *,
        identifying_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identifying_fields: identifying_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#identifying_fields DataLossPreventionJobTrigger#identifying_fields}
        '''
        value = DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions(
            identifying_fields=identifying_fields
        )

        return typing.cast(None, jsii.invoke(self, "putTableOptions", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetRequiredFindingLabelKeys")
    def reset_required_finding_label_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredFindingLabelKeys", []))

    @jsii.member(jsii_name="resetTableOptions")
    def reset_table_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableOptions", []))

    @builtins.property
    @jsii.member(jsii_name="tableOptions")
    def table_options(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsOutputReference", jsii.get(self, "tableOptions"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredFindingLabelKeysInput")
    def required_finding_label_keys_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "requiredFindingLabelKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="tableOptionsInput")
    def table_options_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions"], jsii.get(self, "tableOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e0aaf26df974b8d623ce2e0926beffe185ad17bffb14d1bbb64293cd2e8433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0213fbc10f2def65774deee390495403ab4ec433485b089922f58e8ce2bc55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredFindingLabelKeys")
    def required_finding_label_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requiredFindingLabelKeys"))

    @required_finding_label_keys.setter
    def required_finding_label_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6a180117f5d0f8ea75ac3b6a956fa638d68319e10c6ddbcd87558c91820d132)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredFindingLabelKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__557dd34a2988826a1eb38e2314343b870771854cabd0cb8d39dd1d81ffe0f112)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions",
    jsii_struct_bases=[],
    name_mapping={"identifying_fields": "identifyingFields"},
)
class DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions:
    def __init__(
        self,
        *,
        identifying_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identifying_fields: identifying_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#identifying_fields DataLossPreventionJobTrigger#identifying_fields}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdca56af2b7f921fa142ac69161f7b1a6ab779e8257dbc912411e151239748dc)
            check_type(argname="argument identifying_fields", value=identifying_fields, expected_type=type_hints["identifying_fields"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identifying_fields is not None:
            self._values["identifying_fields"] = identifying_fields

    @builtins.property
    def identifying_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields"]]]:
        '''identifying_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#identifying_fields DataLossPreventionJobTrigger#identifying_fields}
        '''
        result = self._values.get("identifying_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Name describing the field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d254baf430b3932c0e751fbcc09c8b8be76688a3635f8c776ce0838ce410bfc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name describing the field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__481960e19870d9380c211cc191b281c046705f65d8306366e78bed2c9782a36e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b323a236a3aea0b28ac98d2107be8d9051adbfdc62593b24ec54fbbaa6621d0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6227cc3fbf24045a424c84e01f470082964a5f93a70eae8faa0f3f90b4699b5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a6040e136d28a4658fe03ff33b08e13b19e0921e9f1c300ca811ecd910e04cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e55875e0c2d2f2aaed795b3547ecd857f782f4cbd3f6cff7d58609f7950c2a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4910db9bee257c3e12b47fb08850fd58a22f6daee0116e0ab13403787f36a0a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__821bdd678b13c17ac8b477d5bcdc880d56e5370b0d765cfaf575500fd67f1fed)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3629f1ee8cf2c3f4da799e3478d9023cfe69a79a8e2c13a7688ea9c03006a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692b5ca0483fffe2853cfc660c7c3d8afde7afce1b62e45485acae513a6e451c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71348761542954c104b3a58cc7080da874628bc12dd9bede29b18a1b60e35d69)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIdentifyingFields")
    def put_identifying_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7126bd2c4fdcaf2f5502ac1fb468fd70f31ac0cced59c3a33ca286dfdfdc8d3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIdentifyingFields", [value]))

    @jsii.member(jsii_name="resetIdentifyingFields")
    def reset_identifying_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentifyingFields", []))

    @builtins.property
    @jsii.member(jsii_name="identifyingFields")
    def identifying_fields(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsList:
        return typing.cast(DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsList, jsii.get(self, "identifyingFields"))

    @builtins.property
    @jsii.member(jsii_name="identifyingFieldsInput")
    def identifying_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]]], jsii.get(self, "identifyingFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0161cb95d3ddb8cb87c27b2910fce40c85267d23ebabcbd4a3588511c773ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerInspectJobStorageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc488bcf7edc338c5b4248290440cfbe12fe2702cc9e9f24d131ce961c63e75a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBigQueryOptions")
    def put_big_query_options(
        self,
        *,
        table_reference: typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference, typing.Dict[builtins.str, typing.Any]],
        excluded_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
        identifying_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
        included_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
        rows_limit: typing.Optional[jsii.Number] = None,
        rows_limit_percent: typing.Optional[jsii.Number] = None,
        sample_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table_reference: table_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table_reference DataLossPreventionJobTrigger#table_reference}
        :param excluded_fields: excluded_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#excluded_fields DataLossPreventionJobTrigger#excluded_fields}
        :param identifying_fields: identifying_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#identifying_fields DataLossPreventionJobTrigger#identifying_fields}
        :param included_fields: included_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#included_fields DataLossPreventionJobTrigger#included_fields}
        :param rows_limit: Max number of rows to scan. If the table has more rows than this value, the rest of the rows are omitted. If not set, or if set to 0, all rows will be scanned. Only one of rowsLimit and rowsLimitPercent can be specified. Cannot be used in conjunction with TimespanConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#rows_limit DataLossPreventionJobTrigger#rows_limit}
        :param rows_limit_percent: Max percentage of rows to scan. The rest are omitted. The number of rows scanned is rounded down. Must be between 0 and 100, inclusively. Both 0 and 100 means no limit. Defaults to 0. Only one of rowsLimit and rowsLimitPercent can be specified. Cannot be used in conjunction with TimespanConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#rows_limit_percent DataLossPreventionJobTrigger#rows_limit_percent}
        :param sample_method: How to sample rows if not all rows are scanned. Meaningful only when used in conjunction with either rowsLimit or rowsLimitPercent. If not specified, rows are scanned in the order BigQuery reads them. If TimespanConfig is set, set this to an empty string to avoid using the default value. Default value: "TOP" Possible values: ["TOP", "RANDOM_START"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sample_method DataLossPreventionJobTrigger#sample_method}
        '''
        value = DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions(
            table_reference=table_reference,
            excluded_fields=excluded_fields,
            identifying_fields=identifying_fields,
            included_fields=included_fields,
            rows_limit=rows_limit,
            rows_limit_percent=rows_limit_percent,
            sample_method=sample_method,
        )

        return typing.cast(None, jsii.invoke(self, "putBigQueryOptions", [value]))

    @jsii.member(jsii_name="putCloudStorageOptions")
    def put_cloud_storage_options(
        self,
        *,
        file_set: typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet, typing.Dict[builtins.str, typing.Any]],
        bytes_limit_per_file: typing.Optional[jsii.Number] = None,
        bytes_limit_per_file_percent: typing.Optional[jsii.Number] = None,
        files_limit_percent: typing.Optional[jsii.Number] = None,
        file_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        sample_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_set: file_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#file_set DataLossPreventionJobTrigger#file_set}
        :param bytes_limit_per_file: Max number of bytes to scan from a file. If a scanned file's size is bigger than this value then the rest of the bytes are omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#bytes_limit_per_file DataLossPreventionJobTrigger#bytes_limit_per_file}
        :param bytes_limit_per_file_percent: Max percentage of bytes to scan from a file. The rest are omitted. The number of bytes scanned is rounded down. Must be between 0 and 100, inclusively. Both 0 and 100 means no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#bytes_limit_per_file_percent DataLossPreventionJobTrigger#bytes_limit_per_file_percent}
        :param files_limit_percent: Limits the number of files to scan to this percentage of the input FileSet. Number of files scanned is rounded down. Must be between 0 and 100, inclusively. Both 0 and 100 means no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#files_limit_percent DataLossPreventionJobTrigger#files_limit_percent}
        :param file_types: List of file type groups to include in the scan. If empty, all files are scanned and available data format processors are applied. In addition, the binary content of the selected files is always scanned as well. Images are scanned only as binary if the specified region does not support image inspection and no fileTypes were specified. Possible values: ["BINARY_FILE", "TEXT_FILE", "IMAGE", "WORD", "PDF", "AVRO", "CSV", "TSV", "POWERPOINT", "EXCEL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#file_types DataLossPreventionJobTrigger#file_types}
        :param sample_method: How to sample bytes if not all bytes are scanned. Meaningful only when used in conjunction with bytesLimitPerFile. If not specified, scanning would start from the top. Possible values: ["TOP", "RANDOM_START"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#sample_method DataLossPreventionJobTrigger#sample_method}
        '''
        value = DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions(
            file_set=file_set,
            bytes_limit_per_file=bytes_limit_per_file,
            bytes_limit_per_file_percent=bytes_limit_per_file_percent,
            files_limit_percent=files_limit_percent,
            file_types=file_types,
            sample_method=sample_method,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStorageOptions", [value]))

    @jsii.member(jsii_name="putDatastoreOptions")
    def put_datastore_options(
        self,
        *,
        kind: typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind, typing.Dict[builtins.str, typing.Any]],
        partition_id: typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param kind: kind block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#kind DataLossPreventionJobTrigger#kind}
        :param partition_id: partition_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#partition_id DataLossPreventionJobTrigger#partition_id}
        '''
        value = DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions(
            kind=kind, partition_id=partition_id
        )

        return typing.cast(None, jsii.invoke(self, "putDatastoreOptions", [value]))

    @jsii.member(jsii_name="putHybridOptions")
    def put_hybrid_options(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        required_finding_label_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        table_options: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param description: A short description of where the data is coming from. Will be stored once in the job. 256 max length. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#description DataLossPreventionJobTrigger#description}
        :param labels: To organize findings, these labels will be added to each finding. Label keys must be between 1 and 63 characters long and must conform to the following regular expression: '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?'. Label values must be between 0 and 63 characters long and must conform to the regular expression '(`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?)?'. No more than 10 labels can be associated with a given finding. Examples: - '"environment" : "production"' - '"pipeline" : "etl"' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#labels DataLossPreventionJobTrigger#labels}
        :param required_finding_label_keys: These are labels that each inspection request must include within their 'finding_labels' map. Request may contain others, but any missing one of these will be rejected. Label keys must be between 1 and 63 characters long and must conform to the following regular expression: '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?'. No more than 10 keys can be required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#required_finding_label_keys DataLossPreventionJobTrigger#required_finding_label_keys}
        :param table_options: table_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#table_options DataLossPreventionJobTrigger#table_options}
        '''
        value = DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions(
            description=description,
            labels=labels,
            required_finding_label_keys=required_finding_label_keys,
            table_options=table_options,
        )

        return typing.cast(None, jsii.invoke(self, "putHybridOptions", [value]))

    @jsii.member(jsii_name="putTimespanConfig")
    def put_timespan_config(
        self,
        *,
        enable_auto_population_of_timespan_config: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        timestamp_field: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enable_auto_population_of_timespan_config: When the job is started by a JobTrigger we will automatically figure out a valid startTime to avoid scanning files that have not been modified since the last time the JobTrigger executed. This will be based on the time of the execution of the last run of the JobTrigger or the timespan endTime used in the last run of the JobTrigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#enable_auto_population_of_timespan_config DataLossPreventionJobTrigger#enable_auto_population_of_timespan_config}
        :param end_time: Exclude files, tables, or rows newer than this value. If not set, no upper time limit is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#end_time DataLossPreventionJobTrigger#end_time}
        :param start_time: Exclude files, tables, or rows older than this value. If not set, no lower time limit is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#start_time DataLossPreventionJobTrigger#start_time}
        :param timestamp_field: timestamp_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#timestamp_field DataLossPreventionJobTrigger#timestamp_field}
        '''
        value = DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig(
            enable_auto_population_of_timespan_config=enable_auto_population_of_timespan_config,
            end_time=end_time,
            start_time=start_time,
            timestamp_field=timestamp_field,
        )

        return typing.cast(None, jsii.invoke(self, "putTimespanConfig", [value]))

    @jsii.member(jsii_name="resetBigQueryOptions")
    def reset_big_query_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigQueryOptions", []))

    @jsii.member(jsii_name="resetCloudStorageOptions")
    def reset_cloud_storage_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudStorageOptions", []))

    @jsii.member(jsii_name="resetDatastoreOptions")
    def reset_datastore_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatastoreOptions", []))

    @jsii.member(jsii_name="resetHybridOptions")
    def reset_hybrid_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHybridOptions", []))

    @jsii.member(jsii_name="resetTimespanConfig")
    def reset_timespan_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimespanConfig", []))

    @builtins.property
    @jsii.member(jsii_name="bigQueryOptions")
    def big_query_options(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsOutputReference, jsii.get(self, "bigQueryOptions"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageOptions")
    def cloud_storage_options(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsOutputReference, jsii.get(self, "cloudStorageOptions"))

    @builtins.property
    @jsii.member(jsii_name="datastoreOptions")
    def datastore_options(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsOutputReference, jsii.get(self, "datastoreOptions"))

    @builtins.property
    @jsii.member(jsii_name="hybridOptions")
    def hybrid_options(
        self,
    ) -> DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsOutputReference:
        return typing.cast(DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsOutputReference, jsii.get(self, "hybridOptions"))

    @builtins.property
    @jsii.member(jsii_name="timespanConfig")
    def timespan_config(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigOutputReference", jsii.get(self, "timespanConfig"))

    @builtins.property
    @jsii.member(jsii_name="bigQueryOptionsInput")
    def big_query_options_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions], jsii.get(self, "bigQueryOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageOptionsInput")
    def cloud_storage_options_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions], jsii.get(self, "cloudStorageOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="datastoreOptionsInput")
    def datastore_options_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions], jsii.get(self, "datastoreOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="hybridOptionsInput")
    def hybrid_options_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions], jsii.get(self, "hybridOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timespanConfigInput")
    def timespan_config_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig"], jsii.get(self, "timespanConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfig]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a6587f262488e59e7f8424b690260aecfbecb2674348750c34a1f6a93b636b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_auto_population_of_timespan_config": "enableAutoPopulationOfTimespanConfig",
        "end_time": "endTime",
        "start_time": "startTime",
        "timestamp_field": "timestampField",
    },
)
class DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig:
    def __init__(
        self,
        *,
        enable_auto_population_of_timespan_config: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        timestamp_field: typing.Optional[typing.Union["DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enable_auto_population_of_timespan_config: When the job is started by a JobTrigger we will automatically figure out a valid startTime to avoid scanning files that have not been modified since the last time the JobTrigger executed. This will be based on the time of the execution of the last run of the JobTrigger or the timespan endTime used in the last run of the JobTrigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#enable_auto_population_of_timespan_config DataLossPreventionJobTrigger#enable_auto_population_of_timespan_config}
        :param end_time: Exclude files, tables, or rows newer than this value. If not set, no upper time limit is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#end_time DataLossPreventionJobTrigger#end_time}
        :param start_time: Exclude files, tables, or rows older than this value. If not set, no lower time limit is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#start_time DataLossPreventionJobTrigger#start_time}
        :param timestamp_field: timestamp_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#timestamp_field DataLossPreventionJobTrigger#timestamp_field}
        '''
        if isinstance(timestamp_field, dict):
            timestamp_field = DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField(**timestamp_field)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db113422c7b9fde599cb66f57ab43108b3ebd4c2a4f2188538db6c533973f13)
            check_type(argname="argument enable_auto_population_of_timespan_config", value=enable_auto_population_of_timespan_config, expected_type=type_hints["enable_auto_population_of_timespan_config"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument timestamp_field", value=timestamp_field, expected_type=type_hints["timestamp_field"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_auto_population_of_timespan_config is not None:
            self._values["enable_auto_population_of_timespan_config"] = enable_auto_population_of_timespan_config
        if end_time is not None:
            self._values["end_time"] = end_time
        if start_time is not None:
            self._values["start_time"] = start_time
        if timestamp_field is not None:
            self._values["timestamp_field"] = timestamp_field

    @builtins.property
    def enable_auto_population_of_timespan_config(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When the job is started by a JobTrigger we will automatically figure out a valid startTime to avoid scanning files that have not been modified since the last time the JobTrigger executed.

        This will
        be based on the time of the execution of the last run of the JobTrigger or the timespan endTime
        used in the last run of the JobTrigger.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#enable_auto_population_of_timespan_config DataLossPreventionJobTrigger#enable_auto_population_of_timespan_config}
        '''
        result = self._values.get("enable_auto_population_of_timespan_config")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''Exclude files, tables, or rows newer than this value. If not set, no upper time limit is applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#end_time DataLossPreventionJobTrigger#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''Exclude files, tables, or rows older than this value. If not set, no lower time limit is applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#start_time DataLossPreventionJobTrigger#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_field(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField"]:
        '''timestamp_field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#timestamp_field DataLossPreventionJobTrigger#timestamp_field}
        '''
        result = self._values.get("timestamp_field")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cb3642013396d9e4e18e44891147766d37537629b7609b48c824124cf880299)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTimestampField")
    def put_timestamp_field(self, *, name: builtins.str) -> None:
        '''
        :param name: Specification of the field containing the timestamp of scanned items. Used for data sources like Datastore and BigQuery. For BigQuery: Required to filter out rows based on the given start and end times. If not specified and the table was modified between the given start and end times, the entire table will be scanned. The valid data types of the timestamp field are: INTEGER, DATE, TIMESTAMP, or DATETIME BigQuery column. For Datastore. Valid data types of the timestamp field are: TIMESTAMP. Datastore entity will be scanned if the timestamp property does not exist or its value is empty or invalid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        value = DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putTimestampField", [value]))

    @jsii.member(jsii_name="resetEnableAutoPopulationOfTimespanConfig")
    def reset_enable_auto_population_of_timespan_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAutoPopulationOfTimespanConfig", []))

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @jsii.member(jsii_name="resetTimestampField")
    def reset_timestamp_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestampField", []))

    @builtins.property
    @jsii.member(jsii_name="timestampField")
    def timestamp_field(
        self,
    ) -> "DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampFieldOutputReference":
        return typing.cast("DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampFieldOutputReference", jsii.get(self, "timestampField"))

    @builtins.property
    @jsii.member(jsii_name="enableAutoPopulationOfTimespanConfigInput")
    def enable_auto_population_of_timespan_config_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableAutoPopulationOfTimespanConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampFieldInput")
    def timestamp_field_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField"], jsii.get(self, "timestampFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAutoPopulationOfTimespanConfig")
    def enable_auto_population_of_timespan_config(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableAutoPopulationOfTimespanConfig"))

    @enable_auto_population_of_timespan_config.setter
    def enable_auto_population_of_timespan_config(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6faf18ed809562dd133ef13f9be6c0c8a20e19ea238e74fa2a4c7631be1e9aa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAutoPopulationOfTimespanConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1964e5b28322be42f7f5f383da78381320cdcddfbf1acea4189d9a33037f455)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c130be22e7407013801ef620fd7765e4c5b8d3bc131e6db907fe14fca907dfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7583ed5ef307de69be5e2e800211a9f8942f416aab98ca414c12a5d2cf2f4bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Specification of the field containing the timestamp of scanned items. Used for data sources like Datastore and BigQuery. For BigQuery: Required to filter out rows based on the given start and end times. If not specified and the table was modified between the given start and end times, the entire table will be scanned. The valid data types of the timestamp field are: INTEGER, DATE, TIMESTAMP, or DATETIME BigQuery column. For Datastore. Valid data types of the timestamp field are: TIMESTAMP. Datastore entity will be scanned if the timestamp property does not exist or its value is empty or invalid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d785c106fab21fdc70503ec411596e3f113c44500598483e34e5ba3bb8d4e5f8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Specification of the field containing the timestamp of scanned items. Used for data sources like Datastore and BigQuery.

        For BigQuery: Required to filter out rows based on the given start and end times. If not specified and the table was
        modified between the given start and end times, the entire table will be scanned. The valid data types of the timestamp
        field are: INTEGER, DATE, TIMESTAMP, or DATETIME BigQuery column.

        For Datastore. Valid data types of the timestamp field are: TIMESTAMP. Datastore entity will be scanned if the
        timestamp property does not exist or its value is empty or invalid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#name DataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d957b4c019d37b70af49f2ffe72b6d953d19d5161abf2c4845befc51a89439a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8ba585a57256e9fc8e5cfaac4e3733cb8b58fde702ce0ea9855f0bcecb37b8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cbf9ae82638ade54a81fd4c6c37832854acb7b8a4edce28d1e34a7411c042ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataLossPreventionJobTriggerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#create DataLossPreventionJobTrigger#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#delete DataLossPreventionJobTrigger#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#update DataLossPreventionJobTrigger#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f44c62f805b7a3d2a4ff38a48416261b2af018cf0c92da11f00b61c7a1fada0)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#create DataLossPreventionJobTrigger#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#delete DataLossPreventionJobTrigger#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#update DataLossPreventionJobTrigger#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bfc836f7a8343937ce65c26aa2ddf058e4a3a9a8bb787bdb2800b5a90731ffb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f64023d844760277cfa3e65c25ed53850b40243f5771519af98486f78f25a0f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ccc22c148cd111a9f79742f979d50e6e2dcede861dbd4faa7027d56d90d2d37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b56e00afb2f8f4cf3fa3e6adea66a9e71fd36727b32c6314e352d73440db6923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4be87e275a604d32a950950b4e816a88da4227cbd3bdb2359d2fa7bc86e225f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerTriggers",
    jsii_struct_bases=[],
    name_mapping={"manual": "manual", "schedule": "schedule"},
)
class DataLossPreventionJobTriggerTriggers:
    def __init__(
        self,
        *,
        manual: typing.Optional[typing.Union["DataLossPreventionJobTriggerTriggersManual", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[typing.Union["DataLossPreventionJobTriggerTriggersSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param manual: manual block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#manual DataLossPreventionJobTrigger#manual}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#schedule DataLossPreventionJobTrigger#schedule}
        '''
        if isinstance(manual, dict):
            manual = DataLossPreventionJobTriggerTriggersManual(**manual)
        if isinstance(schedule, dict):
            schedule = DataLossPreventionJobTriggerTriggersSchedule(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3851f19816552368987fb461e535dc39bb96c0bb4f3c0e2b638824e62527f1db)
            check_type(argname="argument manual", value=manual, expected_type=type_hints["manual"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if manual is not None:
            self._values["manual"] = manual
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def manual(self) -> typing.Optional["DataLossPreventionJobTriggerTriggersManual"]:
        '''manual block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#manual DataLossPreventionJobTrigger#manual}
        '''
        result = self._values.get("manual")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerTriggersManual"], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerTriggersSchedule"]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#schedule DataLossPreventionJobTrigger#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerTriggersSchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerTriggers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerTriggersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerTriggersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64d287c6c80b83b6929cb712c9a6c191cb8ffe910ac54ab2dc3e2f5f37c2d6f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionJobTriggerTriggersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be148c111611690edd81d42a28840fb7e39e31e6d5a549fad9933cacc560b0da)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionJobTriggerTriggersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b216179289b43bbff583969f55af943c548fd8d275b964e5ece3cc7402aff1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30e8aa45c35c40b82bd8a043995686a3a43c80db8b6c99a10d6fe9373c3d5de6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8f58b46cb0a1ca9b97450bc3d4f62be89e1d9bcacb1d86c7a57ad71f02c8509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerTriggers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerTriggers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerTriggers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__953bd64796f0e4391536a410a65e9335f3f70e069bf83b7f4974050490ffb96d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerTriggersManual",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLossPreventionJobTriggerTriggersManual:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerTriggersManual(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerTriggersManualOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerTriggersManualOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41c63e17d48fc2632b3ad220707106022f9e41f5778d225ada4c8f2983e3e7d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerTriggersManual]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerTriggersManual], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerTriggersManual],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4975aaf7385c630427acbeebd3888cb8d9a925f72a2b89a47d0c7caf9dd256a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionJobTriggerTriggersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerTriggersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80fa1d2ea235bf8f7591ff2de9fca84d9bdc0935e80c02cf41dd1d7cd64638e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putManual")
    def put_manual(self) -> None:
        value = DataLossPreventionJobTriggerTriggersManual()

        return typing.cast(None, jsii.invoke(self, "putManual", [value]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        recurrence_period_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recurrence_period_duration: With this option a job is started a regular periodic basis. For example: every day (86400 seconds). A scheduled start time will be skipped if the previous execution has not ended when its scheduled time occurs. This value must be set to a time duration greater than or equal to 1 day and can be no longer than 60 days. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#recurrence_period_duration DataLossPreventionJobTrigger#recurrence_period_duration}
        '''
        value = DataLossPreventionJobTriggerTriggersSchedule(
            recurrence_period_duration=recurrence_period_duration
        )

        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="resetManual")
    def reset_manual(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManual", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @builtins.property
    @jsii.member(jsii_name="manual")
    def manual(self) -> DataLossPreventionJobTriggerTriggersManualOutputReference:
        return typing.cast(DataLossPreventionJobTriggerTriggersManualOutputReference, jsii.get(self, "manual"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> "DataLossPreventionJobTriggerTriggersScheduleOutputReference":
        return typing.cast("DataLossPreventionJobTriggerTriggersScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="manualInput")
    def manual_input(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerTriggersManual]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerTriggersManual], jsii.get(self, "manualInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional["DataLossPreventionJobTriggerTriggersSchedule"]:
        return typing.cast(typing.Optional["DataLossPreventionJobTriggerTriggersSchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerTriggers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerTriggers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerTriggers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb54859fcd9cec3908952d65f580dfa5b4b73c9716afe90cd4704a83d4cb549)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerTriggersSchedule",
    jsii_struct_bases=[],
    name_mapping={"recurrence_period_duration": "recurrencePeriodDuration"},
)
class DataLossPreventionJobTriggerTriggersSchedule:
    def __init__(
        self,
        *,
        recurrence_period_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recurrence_period_duration: With this option a job is started a regular periodic basis. For example: every day (86400 seconds). A scheduled start time will be skipped if the previous execution has not ended when its scheduled time occurs. This value must be set to a time duration greater than or equal to 1 day and can be no longer than 60 days. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#recurrence_period_duration DataLossPreventionJobTrigger#recurrence_period_duration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b26d9b508c6a2ee3e10b1fe1bb7abaf9236b0d6cc47fc250401201ee5ae692)
            check_type(argname="argument recurrence_period_duration", value=recurrence_period_duration, expected_type=type_hints["recurrence_period_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recurrence_period_duration is not None:
            self._values["recurrence_period_duration"] = recurrence_period_duration

    @builtins.property
    def recurrence_period_duration(self) -> typing.Optional[builtins.str]:
        '''With this option a job is started a regular periodic basis. For example: every day (86400 seconds).

        A scheduled start time will be skipped if the previous execution has not ended when its scheduled time occurs.

        This value must be set to a time duration greater than or equal to 1 day and can be no longer than 60 days.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_job_trigger#recurrence_period_duration DataLossPreventionJobTrigger#recurrence_period_duration}
        '''
        result = self._values.get("recurrence_period_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionJobTriggerTriggersSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionJobTriggerTriggersScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionJobTrigger.DataLossPreventionJobTriggerTriggersScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8aa0b2c08ea9789c731610914bc3231ec1d3f4b4eba45f7bde4a1d4166ef0e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRecurrencePeriodDuration")
    def reset_recurrence_period_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurrencePeriodDuration", []))

    @builtins.property
    @jsii.member(jsii_name="recurrencePeriodDurationInput")
    def recurrence_period_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recurrencePeriodDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrencePeriodDuration")
    def recurrence_period_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurrencePeriodDuration"))

    @recurrence_period_duration.setter
    def recurrence_period_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__372833c4e6bcdbb0cdedcf9d2f64cdc085c332edfd591430789c38e015d47cc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrencePeriodDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionJobTriggerTriggersSchedule]:
        return typing.cast(typing.Optional[DataLossPreventionJobTriggerTriggersSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionJobTriggerTriggersSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b554e5e926acd1c83e4836a9ebdcc8e617b86b14d9583c70ed94e33a53deb31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataLossPreventionJobTrigger",
    "DataLossPreventionJobTriggerConfig",
    "DataLossPreventionJobTriggerInspectJob",
    "DataLossPreventionJobTriggerInspectJobActions",
    "DataLossPreventionJobTriggerInspectJobActionsDeidentify",
    "DataLossPreventionJobTriggerInspectJobActionsDeidentifyOutputReference",
    "DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig",
    "DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfigOutputReference",
    "DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig",
    "DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigOutputReference",
    "DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable",
    "DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTableOutputReference",
    "DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails",
    "DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmailsOutputReference",
    "DataLossPreventionJobTriggerInspectJobActionsList",
    "DataLossPreventionJobTriggerInspectJobActionsOutputReference",
    "DataLossPreventionJobTriggerInspectJobActionsPubSub",
    "DataLossPreventionJobTriggerInspectJobActionsPubSubOutputReference",
    "DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog",
    "DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalogOutputReference",
    "DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc",
    "DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCsccOutputReference",
    "DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver",
    "DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriverOutputReference",
    "DataLossPreventionJobTriggerInspectJobActionsSaveFindings",
    "DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig",
    "DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigOutputReference",
    "DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable",
    "DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTableOutputReference",
    "DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfig",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesList",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegexOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScoreOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredTypeOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType",
    "DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateTypeOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes",
    "DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesList",
    "DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore",
    "DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScoreOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigLimits",
    "DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType",
    "DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType",
    "DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore",
    "DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeList",
    "DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigLimitsOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesList",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetList",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegexOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximityOutputReference",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesList",
    "DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesOutputReference",
    "DataLossPreventionJobTriggerInspectJobOutputReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfig",
    "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions",
    "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields",
    "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsList",
    "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsOutputReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields",
    "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsList",
    "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsOutputReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields",
    "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsList",
    "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsOutputReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsOutputReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReferenceOutputReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions",
    "DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet",
    "DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetOutputReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet",
    "DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSetOutputReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsOutputReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions",
    "DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind",
    "DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKindOutputReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsOutputReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId",
    "DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionIdOutputReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions",
    "DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsOutputReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions",
    "DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields",
    "DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsList",
    "DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsOutputReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsOutputReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfigOutputReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig",
    "DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigOutputReference",
    "DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField",
    "DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampFieldOutputReference",
    "DataLossPreventionJobTriggerTimeouts",
    "DataLossPreventionJobTriggerTimeoutsOutputReference",
    "DataLossPreventionJobTriggerTriggers",
    "DataLossPreventionJobTriggerTriggersList",
    "DataLossPreventionJobTriggerTriggersManual",
    "DataLossPreventionJobTriggerTriggersManualOutputReference",
    "DataLossPreventionJobTriggerTriggersOutputReference",
    "DataLossPreventionJobTriggerTriggersSchedule",
    "DataLossPreventionJobTriggerTriggersScheduleOutputReference",
]

publication.publish()

def _typecheckingstub__f2de68c15e704db02a281360b0daa8843a0d3b0060998cb1004bfb2c9904bf02(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    parent: builtins.str,
    triggers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerTriggers, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    inspect_job: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJob, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataLossPreventionJobTriggerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trigger_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__d9e6df625f19efc8d21266dca525a377a2ac5ce09f598b4c01e9db9126453002(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09f9a0e81d65307ffcc19aa6865392920fd83ddbd0efc39109df17525f670b6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerTriggers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a060f046683b9cc93f4a82126c667f72d6dad7f1d997824df466bd387a810376(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3912011ca0a1c7991d40ce71419582aaf28a01945df192d080a4c500adc0c30f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4b2854cdc644c034c208a0c0e28abe3bd8c029962c43debb4ed009236059bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e5cc32336570cc709e9f24e04b6f0da11d805b8ed74af81ca86ac876851a22a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ee0c3177da98457226086948b7fba521ffbf7c187e8258d5056db76336dbed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0fc7276d58af303e6513224ea5157e9b25f77768a6cef104642755729ef6a83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78584e8541d89523b731062903f4ef4d89e7f8d8513bea3343d48c12706bfcc7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parent: builtins.str,
    triggers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerTriggers, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    inspect_job: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJob, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataLossPreventionJobTriggerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trigger_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7084810c2287a4aa781be8c49bd54020126ca4ad27659fa785ef2b612b1642(
    *,
    storage_config: typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfig, typing.Dict[builtins.str, typing.Any]],
    actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inspect_config: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    inspect_template_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc051f2469caac11e7267bb13475c1adc0a510db0e95fd826a2ca9f5ffc6a3da(
    *,
    deidentify: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobActionsDeidentify, typing.Dict[builtins.str, typing.Any]]] = None,
    job_notification_emails: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails, typing.Dict[builtins.str, typing.Any]]] = None,
    publish_findings_to_cloud_data_catalog: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog, typing.Dict[builtins.str, typing.Any]]] = None,
    publish_summary_to_cscc: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc, typing.Dict[builtins.str, typing.Any]]] = None,
    publish_to_stackdriver: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver, typing.Dict[builtins.str, typing.Any]]] = None,
    pub_sub: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobActionsPubSub, typing.Dict[builtins.str, typing.Any]]] = None,
    save_findings: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobActionsSaveFindings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6255ccee82f3ce68feaa16b44bc65af157a7a3532bfbf4bee6be8afb22dd512b(
    *,
    cloud_storage_output: builtins.str,
    file_types_to_transform: typing.Optional[typing.Sequence[builtins.str]] = None,
    transformation_config: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    transformation_details_storage_config: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6952de99d9993ef7d25d3c5c599c4258ab6d93e00e5db5abeab8cddf96c759f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4509b34996e40672552cdd779868503f1358734ec5c0a988c22c563834d8311b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ccf1fae7d3602eb49f0b3f9e6ac1984aa638df547c4e8bae691c04b1f0639c1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1396c3f5cda9da36c12593dc069d20ffc772807e2b6cdefc75e3f1884930fa78(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentify],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf38e329e3b87997c12dfd2097a8dd5b2cf9462529037b97cbc6b23fd2544106(
    *,
    deidentify_template: typing.Optional[builtins.str] = None,
    image_redact_template: typing.Optional[builtins.str] = None,
    structured_deidentify_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a6bf2b452a8279fb51038de593d1497a95040e53b3f60a24df88b0794fe8c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62cfd9e7fc1c34c8226f391a395930aa79a3d93e77dcdf341c05024d3da826f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1768ccb2038297b5774a23d689c724903aa302edd3b43a89ee6c4990fb629c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9c290057d8fe5fa7f0a47d3a83b2c3a9cfb40ad9a897f8e5fdcd4a2fa98ee6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3751f5b18c270c31103c4c9f34c39e01713459d518776688c4ce96a518ca3c01(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66020fd3ace64c52fd4b2ce24de77f6eeb66e4bc849271465f537142a09b64bd(
    *,
    table: typing.Union[DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9c49c00f6f944cffac74e0643a5b857434fded8ea099079b8de547b6e1bdb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c47d8f5013e620d5422506afcc63db8a883aaab4f2cd7bf8aeb238c7d9f2b0(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d322a4f5e596feb12a11c86899606683e443fa0ffdd8d709d5412f7b2bf1183f(
    *,
    dataset_id: builtins.str,
    project_id: builtins.str,
    table_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__991a338cc6946df4d99c603ab28020f0e61297d885f72f3c58dc0b829cb327b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb430885c0bd5b88f37b781c50f4da19de511d5a601bb8b5b8b3d505532ec001(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965a70cfdde4f2b6b0e23da9d34b521c6b7a4b97d77ea189d25ce4ba9fd2dfd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff15cbda74390d0136b8c63f607a09a11040f79b265ecba11a154cb575a7c95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf1aac70a24fa39551b49a578a1724cb62cd22a035c4189941abd545e1a20275(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e4f17119f9570a20d2c0ceabbddf653a4529d850c796339ffc649b7212e124(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea47e9a864da0d5243091e150c66c495b9a41f45f405409f737500db908894a9(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d7b7793a4fb501448a086e714bbd4272c72b57eb827bea95bdcf8e96576f21a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7afb63fab054bcd5e2f0c258e593642d6d040581f7694000f2e8718b205ef89(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e79115c3c9741dd177f70f41cbea2344c389c8be339e9cfba463f4d10a08858(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01bb9fee0530b3ae65672f96847d7b72e532ff9f2f468b1313a2b530b726774(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b610aabab275af61d1c025db23c883c120e3fb3eaf1549194877dd8392a5ca03(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__790a6204de236976d747bba57161db52326bb2b2f0f59fc8aead07741b5312c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b954cfa638334c7ad8a3a23fa87f56314c829cc9ffdc0388d249d257a4976c09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87cb0b7e3973ac738d74ae454d26e8d37e6bc9f9d98b61298078c72686e53021(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10399479716dc20e9f0772fe8ce418e4e7f69d64947bb29390ec99360ac3b8e(
    *,
    topic: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e1a29845e30ab1e43133c300a673eb9586d49baf8aee35f2fcf9717099e3cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ae77d5f8c2a0d728bf2e2a1c915ea0ae8d1e3a5226a3e5f92a0a7b8297b58d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d8ee08fdc3faf33124ec538498b2e03a7b32d9539e4f5ec788cf3aabe009b0(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsPubSub],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a08116d347a559248283713aa9ae77728831e3a6efd50642022697db1afbed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba70105fea05f65bf413bd594d977040d2c0132ee9021ab2b8cc938d633c2a7(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3cba9f380ff2a76e1c6a9fe88ce166b4b8c8e0aca2002c6de78b5e59ec89ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc8c2a26692b792d5126cf23368810ea9114581e317e8b19dfe56f5b5b9c13d9(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000eb2028636cd870bd78c63f8afba0fd89f4f71b09d32dc0022503156e5a218(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a080d34fef8a6ed70f8404ce5187dcc7609ffff3d278e613a9ffe990b8922e2(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc359bc052e59241daa0911afdae16f1e0f43cfd78dff6b4267f3ae1fc623336(
    *,
    output_config: typing.Union[DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e6e1634b5fa031779f8bff2c8bfbc85fc439c1bf8f089d484ffef8c9731883(
    *,
    table: typing.Union[DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable, typing.Dict[builtins.str, typing.Any]],
    output_schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3216c420cb696c7787c8d61c85684a108e53699f846590670ef613fa604e36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cdf76fa521879272b1439915a3879f05e60d25ef0f4463c21407341f6b54beb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ad0701f01984f1add4a59c3661b0661afc17d20b869ca61ebbe235f0791156(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fadde11ebc41936b614223ce3e252c36eb5fef6253ec2cb325a482c5139b959(
    *,
    dataset_id: builtins.str,
    project_id: builtins.str,
    table_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db7ae69086978f38297b60d0aa291b5c09fff5519f291f922fe55f47b0297741(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db83d4db743620b0751eb52ce764f8fb34dd594bada88f609c98cde6d35bdf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__596ba9b73fd23d85efb7f12e1c9e337bd597d27a5e9639aef2d8858fac839a66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf88d167c2e6ec234dcb8b88dbfeebcd8ff7affbee86ef9e0eecc3ef69ff96bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb96735996690e3182428e1b019b14e5b1ce0f35b1722680341832009acc4ad(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31a730aa42a11b420f843392352ef5a095ffcd4f87be099b4a5dd4d1e5c4fe1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e896668c1a21228791415ad136b52f0b4437d2afbcf28c0acadd594196cbcafc(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobActionsSaveFindings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d0c36718bd1a4f10474910048bb82d1875e075cf4800205c1843afcec72510(
    *,
    custom_info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    exclude_info_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_quote: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    limits: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    min_likelihood: typing.Optional[builtins.str] = None,
    rule_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dec0a3d4fe2aa88db30c328e52c2fc8edb1809376420f46375eb9a0af567c16(
    *,
    info_type: typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType, typing.Dict[builtins.str, typing.Any]],
    dictionary: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
    exclusion_type: typing.Optional[builtins.str] = None,
    likelihood: typing.Optional[builtins.str] = None,
    regex: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex, typing.Dict[builtins.str, typing.Any]]] = None,
    sensitivity_score: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    stored_type: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType, typing.Dict[builtins.str, typing.Any]]] = None,
    surrogate_type: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d9d3de50d75200d9c1fbb7c3328620a68694848aa0e0b78f2fa407a94842b6(
    *,
    cloud_storage_path: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
    word_list: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509c561e2e00962deb67c2c6242246b623eba48d9697e26b33f7c400e77ccb9d(
    *,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4cedb9d7a2176f548421f2e8830a0598e5c2f7a8ce0b0193d1a61dcc1449de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71b57f2391a6a82716d81d3315ee1b336b9f0dd647959cb52679f453bf75e7f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3865f5927e4539b0b2411af4622eabb453b661f4583e9fbffc2c12b067808f(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be02e1fc7a7577f539b9dd6bef267b963b6f7ee4b3d8d87846f6e33b5b4da36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59665e85b3c72e005006ff2747cd7a0f569396f169305cc9aafbd14e79c0f6a2(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e93939b41a3e56fad19a18a89c16496cad975f645aa8653a03e1d0acce6c6a(
    *,
    words: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc21a7fe78ba4b91bc5dd734385b5347d2f210fd323c356c0cf48d3397e279c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207112d025bd6d9b4a558bc16586aebe09322296b69b21cb05e39c3b53f5bb74(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27d86d41b8d8419a4d4157f0f48a213026e8d1d314d333e83612a643b47304c(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a651b39110a4e785f83960541b7c375ce52bbf9f8700c1c7de7a7a7f0525aaf(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac671534682db04da4dd27bb11432aa735e157d1463e268df94606f98c8dfd1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f46e799704de97e9cdeb032c194d0b89fb3f271e26dadaf53c3fdd0f2aac0d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60cafb48d72ca3bf38b237f40a50f833c8b650511867bf5feb523d69fa1a37f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77934e0f19e69c4737b55e152b6e9de6ae075121460e73c25708768fa6fc46aa(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1434bf435d60f06813f89b3bba8dda5a68b830fc95d2968b22fe7018ff09d24(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d388a70588d45e06310680749e6989400ae3fc94c8c7624f80d25a41a15ac4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5a7e08434debe86afc97d1780f36856a06f8f91e461dc80bc2267ac71969ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a27024519de6ca63c6d6bf97515b9780b7ff41f71379d40005c61ba04583b84(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d9608a0bcf8b5aeb59ba98ea6046686b515a68696f48156757af81237029ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6543ffcf85f72da9997439e33cb56c66b4b7d68f5d8d4c5c1fbb052659389432(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ead144469ed3ca65c0cab738e28b1af0b924792710a500b3bde42fcd1f48ec6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bad37e539525767f40a6d4a3494ecb81e73b076e0c6ffdd7c971c467d4fdb81(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5237ab4e884401030f86d13f326467ebbbe4d0bc21e3788261cdf9c93278696(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e16a79171e0d5056527ebe09b36140189234a4582856734c21260e0f0627b04(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2ada61cf76b3d0197f69c16ed3b7bcb72d30f8a91bcb3f4625dd24a0301641(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82edd5911beec6a6a1773489b29d6e37462ade683f36ec91678af7720a27c7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b37f9ccf00fa2fe4d3e42fb297bdebe2aa616688cfd8b6554bb4b64feebe87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11338433c97268450fc367fab3cd6897f1f2aa43664e33ac2c0e1351df268a58(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1bf8d67022760d1c61560700ca2e0192d2e226d470fbf7f12cf5990f5865300(
    *,
    pattern: builtins.str,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a30df5af885620ba5a9a44048f657d4464e4141cdc890654b9f7d5e5ff37f68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0cd9de818777c5d5b72e112e6085fc5b0ad4a36b358d95e4b8470eb26e5b7aa(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06434def12e9fbfa2dd103c3a9a669a7901f32fe02ad47e3a70b49155e6f3d67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22875e7034c3425f338a96248a0bb284055a2a89b9eadea73d99aef63d9507c(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__133305467162b53fe8d13d5f1b65fe845eff04ad2086b2be23975fd739bfa732(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ec98bea7345d10735535e16a49f543f4dee52f7ecaabde1f52d4a4b2d85d27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506a616292e74d719336282b3648bad255e2ec8b8f715d72c135d1a87f0e313e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b23c23656915a17cf354658a25ae1f93ddfdc2382819c3ace70193a150097622(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350c83a51f73b43ff1a8718b9fd8ca6c6f6b00bd0039445fbe344825bbbe5525(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8829a7e19ca86cd55539b113ade64397b123c57fba337674f3da681f5b8ac94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b6547ddbc48c8e9691157470fb426ea36d874eadb53833ad179c81a70b4b24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b28caec158c87b0f06a639b08dc505985067c25eb139d1878a7fab6041030888(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aafd36160d3a63ce9b02b081c500436f7fe46b7ac0e25ad8a1989b2dc5d6ff86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c25d5cec165fccd9031a80c71108fbcc893aa0b0ef8dad8d82ff5e4bedbe50(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e02cedfec2c1061be300abe65da0bc0ef670be9c3c1fd81a9badf84a3eef7c0(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd422dedaeeba2491cf1b9b2c88776658f465c2773a30db0ce0e30c60118796b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32b15c7c87d70bd241853656fedd5db1f8c064b3080cc7ba9443d2a7e026f1a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a24090cf6538ef7a7a5427d29165b03822a360975e0163abc794253d2dc2b3a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce7cdf8dff166966114e876a1922400a4f23a4e1b4e876b6668ab62906eabe7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b6f5fa2d48ae1870830526bc9692de8cd2a945356232c7d4d048ee8674e9ac2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4224960962547b7bc7a8114295927c03d57f0cec4bfe56f63866c674566cd071(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ce295b8c2dd596d4f3fb06dafdc74ef0e7e57eabdd2e51627f72515aaee598(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15eeb607e2f4f2b2b5c517074eaf341a354b4396d5750f82649c3a12737a05ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__708eedce1d2b211a348d2b185b99efe477c0d4195d9d648379936a363c4951f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909ff18835ae9a33d57af2b79ff61309f4de7a95fe06ae9d8ae40b345bd24417(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9f469ca568416cac2ef31fa785d46ccf6f810b69881d8f199a175a30e26d18(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a7821bb4a17002b2433002fc8467fbaa3e63606f2bd22b9115f4de09aa8d2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a420e370622fd377b9c1239f76bfea77436a3ccfedd458201964a823b74a14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8948bd8b4256e5117311ca26ed542f9622e2a2ce81b37f6a549a3dc1495750(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f1fd422a7953954fd55dcf8e668dd54e6bfed487b71d500e985fa897d4463cf(
    *,
    max_findings_per_info_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_findings_per_item: typing.Optional[jsii.Number] = None,
    max_findings_per_request: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c865a438b8a601f8675e8c2b5e72108d56742c9062f0b3a8a7889295c05072da(
    *,
    info_type: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType, typing.Dict[builtins.str, typing.Any]]] = None,
    max_findings: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5983a26fd6249a362a5eccabc2aec441bb91d532b43979086020be7056787c(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fafb63f36f744b82f1a6a59eb275555b4cd78ee1ed97888cc3f7e2b1ac133d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ecc09eea7aca228784c1530adff1db3e1959520e74ab0819c3317b12a1ac43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef356ef54585a92342051f19f8d53706bf941b58b84c24da5b8e92f6e87f370c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b56da640ea12c43be644d35cbdd5adbfd7482fa9a4568a8b741c3b7320a7d6f3(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__099d0c4ce71f569198577b2ba0c8173fe6fa9d28f1f94eb22f66d15d1dc95807(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca3e4a9b8e29d59561c7da890f178a8aec3311416d33383acaff7124594147f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24da2b7e5c208d911c972628f7b5d1bf7943acefb94934d7699bd849a4b529a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff8cd63397c3615efbbd105e830803b27b4f5d4fc243542c720a7e9cdbd88eb(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c892289cffd49e7de77e857e7b41c5ffa336f40d23b7a9690dc7bc068f29c09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f85bca5b774d406b442717f58c5b42d33d646863516fc2bbd3f5032c1698663(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bffd5ffe67b60a8ab8d89250aa32469b4a539d0820f10f68fd213791ddf8d92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc8f4c9299d1428c40c1f4070d53d81a2b6dcc1c675d2222ad8474b700c15e9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f9b6954387279f791f3b2fed1ca867c3e52e64677f9d87d17e639b9945636a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d224c918a69b2b024b794a426f3a484e29c704c06c5f91c2b121d33f7cf6e8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96553ff5915d996a1fd76eef5691e3a81038442fe3f21cb2aa52a78b9bedbe11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19417cd7a115fd9d8682d7f33d1329b1d615c18a8d707810ae3278344f0477c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ff1aabd642e772fb102c723f666c67a58dc85b74015b49c061764e7441f5a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__295fe56948a5e5eefd1e9d78b0b71af43a10fcc56e697d55f9682f79fe85e5e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bcce518f720c31084ba8d9b74194b3eb96143d31854cf669c91bd6f651546e0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b1d9e1b90337bda9c8197439adf3b5f41265c22c9d5460c9d7e2288bde58173(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__598e2763e2d00ed25b87843ea1b22fe0542f7d16b32c373536aabaf0019d7e40(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d14ddd143ba87d2686e7a668f4981c886dd6ae4296989c64b6d20da1059e5359(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f895fc5d283c9d4bd5e5c0cdfdb9c96c85b7462c515a054f894aa7b748b367f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ae97eed286c2f8934b1e17e2eb5a47b6fe701d84ffcee23df8a413b62b0089(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90d18972295f45e85dc389c45421d9b416b4b3bffb9bbce85bc2f3c156bf611d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a5be734d39919ee0b0b1e61394c931d374ac9a0340fee5ad21e1cf820d98df(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f108cb88876c83a02f5f6838e1f0b0ee8b42f7c29064cdab66f997419f0171(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22365815918b2b49a9cec4dd7d0d6b67785a0196c83ef48c37b7f7b8f1d87c95(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5949c18204b35287d84281da147387a46caca9b9b2633d441ea4175f35a2579(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20952ce0b981344634c19d8b85ff97212d5bb2d45641cb88874307b6145c6d03(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb54ef9648d7f06a768b88be856c93ba3db798ba4eeb79468cbdb8d2e3f34f1(
    *,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules, typing.Dict[builtins.str, typing.Any]]]],
    info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791d5e516cb13aeea2d4a221d6574cf8902158b70a82e81022bb3f69cbb1d1e1(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e9ecf5fb918e2accbde6833d388799950a32f7259f0581bb7fa7be3dc0ed7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbfcaba0f2d9d6c84613c607c91bed33b0ac48433ec91033eff1e2666421ad3c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443126cb9ad7063a46059b90b579e81502104d9f1e400422bd58184c9814d676(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca20f6bb16e6ce715b77922fe908535c64c7b727dfeae6b77bbc93a48b50a05(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd72a4de5abe475ec116efeafe2628ab0b327e9bb5f84437df356b248d3101e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10842b1501ddf17578c35846a2165ef997cfd50b8617ef4105c5967093f477d5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75eab1143015eaece2f13add8cc63c90831af7c76fa4245895a072ebe48142c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b4595d1e68295ee8d0fc8b92435d7f786c789f70002f42c553d95f49eea1c3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c3447200865ffc84459829ef0f3b09ec7197f311efb099191af69a7515d7b52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635f3283c2e2d0f8ca1eed814f196ff4994d9f44101c8dda0e31ee6323165c9d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397ac3b4bb5415c083fbd503bb2dfb828ba78ea9636670ae42cc5f2558975603(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542f4ebded24948a13804dc89d35ea2ce589e7f9f29405b663817756fd754324(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb2746bbd3224dbce83cd2e3c4062f11286abc5e820993797493b062330df616(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7c815519b144349c286e466fb3cc36bca0f0d2f70b384e0523c853e37b2691b(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d67df94c9b58e17f4b14fe6d9943d908ee85f8c3f5d25a9f083afa11f1068d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cae6f13f05b4dfcbef446c8311503b878f682d45922ca51160d145a3c729242(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2928dc60071c516a191ec6829b25d54b9980b52a62a0026ea75b3815841005b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2992e3a98ae6bbb04bc8257bb9c66f75e78e37514775d3e99a4cc26257fbc4a2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc4d5e3b1f4cd0930bee93f64b4ec3424f8d7612440343d5ac1a417143070ed(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd6a10e66a39fb8c3e2f45de7bc13e76182ad5163010affec982ae9d706aaca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ff9f029731a86934748abe585fefe9017ba95e7dea67842cbb2d9dac15cb53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75cb86b716564644722872b9bc46fe71fe6f1f83ecc7807215bc678bd8eee528(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c4d28dc055c11bf3f3fab9e2330e0924fe713f53df4e5b2d26cdbdeb98e85b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff25af8a54178e1715282b136ef5c2925e39f9f8a8cdf201462aa19654f8816d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigRuleSet]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__141af0f4e29c379ba8b7bfc89aea1d1d8103af7b548e390e334a6cb938beff25(
    *,
    exclusion_rule: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule, typing.Dict[builtins.str, typing.Any]]] = None,
    hotword_rule: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf747850ea59aa086327b5a75c58fdbb82d0775d86909213bcd2408c5fe8356(
    *,
    matching_type: builtins.str,
    dictionary: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude_by_hotword: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude_info_types: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes, typing.Dict[builtins.str, typing.Any]]] = None,
    regex: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e0a2d14b4cabe639b1f3f50b31ce2b1c05f4782bf9d005118703ce97934233(
    *,
    cloud_storage_path: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
    word_list: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0495313097caab622fcb9db9621056f320658208b43fbc8e1ecc2b4fbdb5fc7(
    *,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33159a7fa740cf7575bcc6694b893c038438a5d20718c7131c6427810e2ea439(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7049d6bf76f52ffdb8e7683aaedba5efc21068d86dd308ef40331ef3e067f417(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f380a8afb0b4039889664958da4562ca24f373bf434564eb544a495c6df0ba76(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba1ecf53572fa98e70395041a088751e9bd99dc394b7b46f4cb6732633b0a9f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4b556bbf8b34c2001eb1361dec7c9b965a4e5d95771e4ea3332d79a0c8f782(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511cb828e74fa8eba8c13c29a4bfab3f18b3e615ac58e23d64d316951f66ffcd(
    *,
    words: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47fdaca48d3297c210af2f992b463eed59b7635968a50e90b65accafbd1efcc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a9c52a80ff1cab1e9d93242286f3bd6a91114f238842d752911ef2e9ca37163(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e76e7d20a70fadb669cb636bbf084179ab8c88c5830365e1501d12fc510e041(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca73fd91e66edf36d134bb72bf4c579cf1dca764fee73212589b999b6389c693(
    *,
    hotword_regex: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex, typing.Dict[builtins.str, typing.Any]]] = None,
    proximity: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c04693a54f36e21c96d425002cb96289e2a4a8193148bdd71e25df979884358(
    *,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    pattern: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddcd241ea7a08b7e231c33bb50e85e443c0b38ffd87e6ec319d7fc44ebe5831c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c65f9e50d5abe69adfd69f739c9534405d83e4d3c0b0fe5eb2cc46abd7d97e4(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b8c37d66eec2dda494180fc082f8cafae09a1d8954fcd99e1d56751b015d58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f53ba4737d83f37391a345fd6406e184c29b8303220cdfcbf9051934b33633(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec6705ed408035c54e49f376005c2f158f51f68bcaf2d444d33c2972e65bb7ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e0eb09a7ad939979478de961529b5452369806544429064b90f3447f35da71(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311486ead1fb7f8065d7bfdc315419db6bf5c90d201b4c6717b37d5099fd111f(
    *,
    window_after: typing.Optional[jsii.Number] = None,
    window_before: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101f24ca526afca1621251458b8cef5224f07090d6c05a231b59b640eddd3cc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e3f4a222d8fba381db2d5201f9c3aae9a160e853bac057b40d600fbf2fbf8a5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e9da0e539063c427cc358bd02fec3186d9b698320d8858b984287312c60c14(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c4e7ef91db4367bbdf9fda782501bde86567a24a3e6565a27d13e4dae684735(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e5155b24183f83eb6f8ffcc251577c1618c9d1f883c5046d1e9ab4a0768732(
    *,
    info_types: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__593ebadeda94e0da3612116e78a18fcd77a17818ee5f3453ad28448710163351(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db3c25a25e74395826bfeda239b4535ddd638bc11b80bfdc0fc9697861f1236e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f22ddd647acfd367e38c136f75428dc6df4e06493508ca369f8b8a441b7bb6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb369f8b0eaf71b1fdbb2db110d5149f2b1ec417fdce4b563734f95134d9d8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f16a21b2d121f8a283361037c74a0ed0c27ce4faa0e5dccc88a126c682e7a51(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b424c508ec48f7a8d5c9278deff79fb7fb2879962c05390d0343ab61f73da28f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c8b0cb3abc042f751325d2d25c013e941473303a73c86d160b9009ba991357(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f724cf76d4554a464f7d8777cc4753d77332b5ef76e8fea37a3a2bb65c663dc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1a0e5a92b81fb2fbc57ea5d8efe4fc99b6c735e1ec52ef208d054ec8aac639b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d434c9a810fbce1d88147dec12369b413a89e179f8ccceec2ebe4e55df39cd9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8520385706c0fd21faadc81c96f06365bb3ecb62319fc30a5262a04a532bb642(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a3ee04f9359bfca2107226e5abd2309ae90d1058370eff75a52e013aaeec89(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def539c2f553d3902ae3c632e11bc0ea017f33ebf887a0cbd6314f37ae9ab817(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b04d1d5708bd00cf7494d00cb8e953aeb0fd0f9c1e75ecca819f95651a030e18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd00ce3c8d1639a0d7b991f75bf980cf209dd761150eca3731e9754b4f2079f0(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e47e213dc0608c7e01bc1170a2d768c0fc3b12a248ab2c9dfca5f25bfc1f78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ddf483bf47a398bffcd68ba78fff11b7e07afac56b51b98fbd435616aca217(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8689baa6133780305bc15e0dae015d1868bf441e4c29f91ed39849ebb7c1e1(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468c2d57ebe79761a68aa06215924e85f1fd35d2b719d5c1132de011a2191639(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78685fdc50ef82fece492c45cdb71b58e4c5a97461b060aaaa25d22e3fd63d4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a7af0c5bb2277495473ad6449820c983319fe07b10b015bdc29156790c8232(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64561f008526c9dfa704c8fc01a40b0a97967055194490f23fb98800f275d634(
    *,
    pattern: builtins.str,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645d801aa9b79a1f5a5dd5b7a1b9ec1e8cbd19e7455935a27acaf90f8fe8ce29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19c56cff3cbd39dcb4f81ab8d025d0ca239a49823be4adb84a5c9659c26e265(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6003e55df238bc9e89002ad54657deb4e8f61485f640318c428ef80e4ed1ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc66eacbc97c9019efc7d0ce1457b66d25cdbfa7c8085850290a6067841bb03a(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5d6e1a8a0fbd2798ba91cba0a252574cc8e6f8857cd28cb02a1ddc04a65879d(
    *,
    hotword_regex: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex, typing.Dict[builtins.str, typing.Any]]] = None,
    likelihood_adjustment: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment, typing.Dict[builtins.str, typing.Any]]] = None,
    proximity: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__232a0a93ca8d5279e99d650eb95c179472c96d41e9643604209d3e78f425c69d(
    *,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    pattern: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e5fb307cdb9e73f16f919e7267a04a31458f229591cd6419ed78d052a6e067(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1362c3d96581afc2873d2f2cca164ea8fba0f0137cedc5f868e1ff3da413c38b(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dcf52ebc4ea159934faeb50cb50096f5b53cdcee05e731d971c5752e15ca73f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dad06133fe82eabd3f38ce9c3051ad6e3013d1cf1c76c6331bd404f7eedba3b(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd97bbb9fe4818a97072f9be69ea77ec08ebd12733b4b2e1b460f24ce6cb21c1(
    *,
    fixed_likelihood: typing.Optional[builtins.str] = None,
    relative_likelihood: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ee1fc014c590fad8f3a5a798ab4676c7aa3fe0211d4012ba42bea3894e2b77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdad3865c93b9c1903a2c7358ac9913df551293749ce7bad7ffd26885a1dcf74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6f4ddcecdd4243c1044f051003d67531f307d60bf8fdbffdb050ef3bea38df0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f40416f7161b93bbf5188844a895973871d6c23ed221b1b470cfc53f8b3463(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f93ae0f0b91a4fff7d3d894da6f14bb37f14466a6e72b74f5a7847b8fb1b1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd991012bd4f7f7e77b04db9f0eada7571ca63d6f6532d5344c783ad21adea2(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5056326d50e95bd147ae0e77500a4795659cfe15ee2272cd95cc8ef1190fa5ac(
    *,
    window_after: typing.Optional[jsii.Number] = None,
    window_before: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda93fff612ee0e72ab43573742b658f2a7f4246fc93e6acb7018b128fc3a1e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296462049ded22fc18f38cc9fdb1acc2f38ce0b66b4a96f623f5ace5ba84dca2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0911a98ace54b2c82d332869b534ba1a3d0d521fb70fe94a6330936818b69ccd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__916a2dd63824b1b761edb85b64ddb8e35c9d19a991db245f37d56900fcab5e0a(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27fe38c537115945de744b598495a011604c7f568eeba5def450a7ab04972877(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773483eee3ccc5e67f33cdd0176524af4f75dcbe17372f2f2e11742ce5725003(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c2e0e43693afada709fea4a3838b3a04db589d17be2de03cbc5c8469447e5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e5eb8260c14db2ae84dcb774675289c616bac475aa747a11aa954644c5ddad5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e0cbce2312362ae0fd3453f5fec6f80069b4ba64f745535b8e280e6d5aaf57(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c761731a6549f50ec50b309b22fa4fc6e3c79100605105f3520c9c6a64cd2c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8a22bc5b687831c9e849c665d506ea1ba59cde3c5b669a97fc5ce1b6174cf5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35718fcb798d08fd77909429d50d8f1f6382b623e726d77259483ae77d5b582(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec7071be60c2d58e05dba9408ed68729a748231ee78a53b29d177d26f05d2fd7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7da076ed92da1adf7277063e431fc9c376ff73a1ebb7eea64b3926db157a2a65(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc7a02a4a03d9bb34b9a29e7b93d5e0b84f4cd1dfffce9d7d16e40edd2de89d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13e845766785f892c48068ccda86d520bc99db7801c48fbff10d4b780a2d884(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5631a1e7ba7b8629a1e43aa2e37133f51e7d38ce95521d3842cbcabbac1c8740(
    *,
    big_query_options: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_storage_options: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    datastore_options: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    hybrid_options: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timespan_config: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e50d8ea420e5dc3b8272132e2134d7d30037d9661926c178b1d7c0981c245493(
    *,
    table_reference: typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference, typing.Dict[builtins.str, typing.Any]],
    excluded_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
    identifying_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
    included_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rows_limit: typing.Optional[jsii.Number] = None,
    rows_limit_percent: typing.Optional[jsii.Number] = None,
    sample_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44df9c250d0ab0232018c2053f448cb5892c7b8b051bd871883269519bfbbf1(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96cb20e7089f8ddbcc252953f2749d30e4aeb120a272056079a8e0c0851fdb7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6153bc734c7c46f37cb205d30ffd7282f4acb23d6b9d1e01ab43708576a990bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69288cf810acd2a39342eb22b417d7cff2f22bc74e4421e8f38bcfc37ced411c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179d71453101b4f9e81319765ed7939923d6aad7de9c7e8cf406b45fb0266cb7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c720adcd1d52cc33abdd52a5ac51ff60386e759753b9b45483df982743c20f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a130e52d548fda849e77b23ca1da84a80d2f7fb02f3fd602ba08f0ba8eeb88cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3e22da972fc9b55972fb2768d06377c1ea0704ac0d27ffe28362b723413982(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d484cdbed11e59ce86649c653660ee8fd75a4c81f1c9bc4f8c55826f5506e28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91e57ad2c6e8c22fe05c5484c38bcee46b3caaa72b5249288877ab1b28522a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8aed41bc5dcdaf15f587e0dfb1016882d57229899784baaf59295ca1b776043(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f77a2f5742920a184b8ab323294232d8ed22ab88bda237090784aa785ac20eaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9c33ef5e5ea98afb9be2c2cc7bf940ffbc9da8cca66dd5b6ff564b3ffd7106e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d92b8ebcf96957003babab1dce17a71058b18fce18b6c57c88946cc5e24cde75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dae119dd05fbd18834145b0112c2b69c130e585870d1f649087cd9b38b7765ec(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a77d3df0ee01725f5f6592429808277c062b0209c3989231940325c823a746(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedc99601aaa146e963176be07e5596c4c75a23b62c1a20ff2ddd03e1a98b7ba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5f2787d8a3ef0151545f4c6c53a7d3dbc4b1d4de8eebbca9d5b14cebd51bcc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b22123283512591724520dcaaded827656eb79554fb0e21cf4d5db888108f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a202d7eab59ca86f80964f2e7193cee7b4810602f8bc33cd0314ddeae33676(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826741c544bcdc3838ca7f483b6e1049c86bf5f902cc039cde2bc42c6c17cf9d(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7a8faeaf2b652c4a3d675f6d228b5cdb84d5877e96afeabb95e87cc1a6aca2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde4e2ad116472e6c629bbf42ca131a6ceaa193eddac0c69d0b33b2e5e75dbdb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd17db4c690e489047d53d71cbe2a1cca75aa940ef6728db3ae7f2ff653d9ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81959d33b4ab97bc1f872a4e19bd3448765fbc7c635ee0bdaf211ace596b29a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef626f6ba0cb8afabf528cc6a32172b8d3a56c559eddbe656b86daaae50fcf92(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52940cd4b432e1f3c022d91fb555ec9ba40837ea0347f6220506be6933d69435(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3f5b484da2449ab447e40b04b9c0d12f53d378f74a804ea29db3f7ee9b7586(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9daeeab52cdf6975105671fb510ef8095001675df6a098261512c2a61178f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df9c7a8c640f2d92a13cfd14753854eb54d1b175f4371e145439a24c2199e37d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__486f3bef08a251a25eeed9d83e8bfb2929d7bda078f6d42ebb614db9dd894a05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac70960f86a974559193f30fd85db2901887bd7d9a1c914a2ee59fa90b90cdf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a755144e0887b780436293f89c3cace809d18f7c3ff8009ed1230db0e4c91416(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__896807be04309ca3ac6ad199f75fef553ec127ad07670a3431c629ac894c4192(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0158d00685d10786619b723798455bf08f0c47e40329a8470e004b5035685b3a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85fed7c33e0468b66c7533b24a10229e0653768f9d5a86af955a687b1c174695(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7bd83cbeded8ee9338f28dcd6eea51845d454099765561d91a233a0e6f03401(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847d35ac49804ae39fbce9b2751e512fa321f09932bf361e109d685f19133c99(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a565838b92a3f8f8968616b733e807ad977c20a9566c89b7f4dba910ec6df33e(
    *,
    dataset_id: builtins.str,
    project_id: builtins.str,
    table_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e43222f1a0f79744329c8157b44db4a41a872d9c6fcf628125c4aaba748ec7fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9d4524a8b497145e1c96718c5cfc493735f8f2f54b1b1e1cb4ea096a03ed50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edee9d259d7676666f33327d9a09b282fb46bf0c49a95a6fb85f06432575ce7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c520d4aafa71ffb55806ac2893c445cbe26950a9dbf953024127dbf1efce0dc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d16b5860e6f6409ca66f807223ff6ad3dda6d864f47bd1a106d5c7b9bb67184(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5201ca36b738d7d66a0fefa4b040f8d5e82cb614b65fd3bcc8a221cf71083b9c(
    *,
    file_set: typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet, typing.Dict[builtins.str, typing.Any]],
    bytes_limit_per_file: typing.Optional[jsii.Number] = None,
    bytes_limit_per_file_percent: typing.Optional[jsii.Number] = None,
    files_limit_percent: typing.Optional[jsii.Number] = None,
    file_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    sample_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eff0852ad366ae639dab9934ce0c52fa1f78b64c14778e59fb5e0b5ffc89668(
    *,
    regex_file_set: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet, typing.Dict[builtins.str, typing.Any]]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7386c246e6d12616bad223c96008c5ec6481874cd82b06ace3e4f31c26a07024(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0403c9361a77e2cc97fb2c3b00e41a64bcb329ad88d3f2f621ca7d7f6e7c32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1d6466a4fff94e847398a4798bb87acd5ef07020265558a23e722f439fdeaad(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c543a2260660828e712ac7a10f46f30c6003cca98a4a4ffd2d6b153c25ed4e77(
    *,
    bucket_name: builtins.str,
    exclude_regex: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_regex: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a8eff3e084fd057f87c3862ae6efbcf127d46338211f2e97a9a442cf8bc33c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2a3d8bd9d29ea50316cbee1a65607b89598844149d117d7a86252e1ce63701(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d7ac59a0f47821791453a60e78e8a988ea596700ad69888cce6832ec7b33308(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe817851ee09704574fe6e08bec52f521cbc2dddf73dc747a2e0173681b7437a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88ff1f0bdf6fe88ad6d5d3eb934d67d716569a5a4dddb2131aa326012ffca65(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb4e6e2e443638bab5ba843891fb2f9deca0df0d263da6e96d20d73337c8af37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283189c107f08b5664dbc6f2a6ae9c29ea384494e29caa38514257f3fba087d4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474db9724b6902584d411cf6b5da384b38d2c29ac0ba7831d40b83d447f99dd2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649b2aab6a2be44b203d0d500179394a32e3cf73bd545374517b67704e487dab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__365d24a8ec6c9034d3ee3dfcc1ccfe0ad9f2b089fefd68b25ee55ccd13503383(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37cd5f0a739aa6edd834bf829d8ea2b16295a28019ebcf77381455f4b71ee99e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf76135e4d3b3019d109b7039f5ab7cc358d1d3a743c34d2bf088c14ce89d4a(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__597727aa02f003240ea9ffbf1077e7e345e9f5d548c15d32347c5cf783e7f8a0(
    *,
    kind: typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind, typing.Dict[builtins.str, typing.Any]],
    partition_id: typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2446ff69bd94fed85e96731f806044fd5a7085b477122d3691dc978c6ca077d(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2323c3fe06f1fc921c7f0b83d10d5797c7ba7d864b7aee4820658be3db8ee392(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89178dd72cf01f0ced4f3eea041f6a1c45fc8f413c8ba4c3bd5262d0ea96bb68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__790e9e9fc12592f337a4ab72f6a03fa5ea1b49e73e54cc49f9dcfd1ad40a3bd3(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b7fee56752994df9b1b6664efcd890733c26fd117c0a82466f9b1a976c4200(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637a3ebd86bec5cc4fdb172a4ae63fe0c7b2a7f26ab8cbc4aaaa6ba846919df5(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980cee053092abf3a2639c25ff1c0df72af1d7d701b292647b59bfcb033d9d20(
    *,
    project_id: builtins.str,
    namespace_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5622f3a8cc549c8fd33535d5ebba9bbf593a901eabc0a912687a8096264f392(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c00cb38231c3e51f7b92ce38320f6c5fb19f511f2e8853a4af5300c26cce8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc56fe39d6ae179a01a3b8b29ae875a242e860e366eb7fe9e908047c152e7a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20aab045cf9bc841ac3800f4faa5c1eb542add12c899d46616aa735aaf54a171(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8690c33e8712ec2414faeffeb63a91835d07aae56a6c521c97e28b1a7b5f325(
    *,
    description: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    required_finding_label_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    table_options: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e526ba03795a4dd5ab7272e93802546b9ba4def87884dcf4c3a9a2ef2199d82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e0aaf26df974b8d623ce2e0926beffe185ad17bffb14d1bbb64293cd2e8433(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0213fbc10f2def65774deee390495403ab4ec433485b089922f58e8ce2bc55(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6a180117f5d0f8ea75ac3b6a956fa638d68319e10c6ddbcd87558c91820d132(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557dd34a2988826a1eb38e2314343b870771854cabd0cb8d39dd1d81ffe0f112(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdca56af2b7f921fa142ac69161f7b1a6ab779e8257dbc912411e151239748dc(
    *,
    identifying_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d254baf430b3932c0e751fbcc09c8b8be76688a3635f8c776ce0838ce410bfc(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__481960e19870d9380c211cc191b281c046705f65d8306366e78bed2c9782a36e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b323a236a3aea0b28ac98d2107be8d9051adbfdc62593b24ec54fbbaa6621d0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6227cc3fbf24045a424c84e01f470082964a5f93a70eae8faa0f3f90b4699b5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6040e136d28a4658fe03ff33b08e13b19e0921e9f1c300ca811ecd910e04cc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e55875e0c2d2f2aaed795b3547ecd857f782f4cbd3f6cff7d58609f7950c2a6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4910db9bee257c3e12b47fb08850fd58a22f6daee0116e0ab13403787f36a0a6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821bdd678b13c17ac8b477d5bcdc880d56e5370b0d765cfaf575500fd67f1fed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3629f1ee8cf2c3f4da799e3478d9023cfe69a79a8e2c13a7688ea9c03006a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692b5ca0483fffe2853cfc660c7c3d8afde7afce1b62e45485acae513a6e451c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71348761542954c104b3a58cc7080da874628bc12dd9bede29b18a1b60e35d69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7126bd2c4fdcaf2f5502ac1fb468fd70f31ac0cced59c3a33ca286dfdfdc8d3c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0161cb95d3ddb8cb87c27b2910fce40c85267d23ebabcbd4a3588511c773ec(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc488bcf7edc338c5b4248290440cfbe12fe2702cc9e9f24d131ce961c63e75a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6587f262488e59e7f8424b690260aecfbecb2674348750c34a1f6a93b636b0(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db113422c7b9fde599cb66f57ab43108b3ebd4c2a4f2188538db6c533973f13(
    *,
    enable_auto_population_of_timespan_config: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    end_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
    timestamp_field: typing.Optional[typing.Union[DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb3642013396d9e4e18e44891147766d37537629b7609b48c824124cf880299(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6faf18ed809562dd133ef13f9be6c0c8a20e19ea238e74fa2a4c7631be1e9aa0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1964e5b28322be42f7f5f383da78381320cdcddfbf1acea4189d9a33037f455(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c130be22e7407013801ef620fd7765e4c5b8d3bc131e6db907fe14fca907dfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7583ed5ef307de69be5e2e800211a9f8942f416aab98ca414c12a5d2cf2f4bc(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d785c106fab21fdc70503ec411596e3f113c44500598483e34e5ba3bb8d4e5f8(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d957b4c019d37b70af49f2ffe72b6d953d19d5161abf2c4845befc51a89439a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ba585a57256e9fc8e5cfaac4e3733cb8b58fde702ce0ea9855f0bcecb37b8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cbf9ae82638ade54a81fd4c6c37832854acb7b8a4edce28d1e34a7411c042ac(
    value: typing.Optional[DataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f44c62f805b7a3d2a4ff38a48416261b2af018cf0c92da11f00b61c7a1fada0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bfc836f7a8343937ce65c26aa2ddf058e4a3a9a8bb787bdb2800b5a90731ffb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64023d844760277cfa3e65c25ed53850b40243f5771519af98486f78f25a0f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ccc22c148cd111a9f79742f979d50e6e2dcede861dbd4faa7027d56d90d2d37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b56e00afb2f8f4cf3fa3e6adea66a9e71fd36727b32c6314e352d73440db6923(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4be87e275a604d32a950950b4e816a88da4227cbd3bdb2359d2fa7bc86e225f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3851f19816552368987fb461e535dc39bb96c0bb4f3c0e2b638824e62527f1db(
    *,
    manual: typing.Optional[typing.Union[DataLossPreventionJobTriggerTriggersManual, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: typing.Optional[typing.Union[DataLossPreventionJobTriggerTriggersSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d287c6c80b83b6929cb712c9a6c191cb8ffe910ac54ab2dc3e2f5f37c2d6f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be148c111611690edd81d42a28840fb7e39e31e6d5a549fad9933cacc560b0da(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b216179289b43bbff583969f55af943c548fd8d275b964e5ece3cc7402aff1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e8aa45c35c40b82bd8a043995686a3a43c80db8b6c99a10d6fe9373c3d5de6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f58b46cb0a1ca9b97450bc3d4f62be89e1d9bcacb1d86c7a57ad71f02c8509(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953bd64796f0e4391536a410a65e9335f3f70e069bf83b7f4974050490ffb96d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionJobTriggerTriggers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c63e17d48fc2632b3ad220707106022f9e41f5778d225ada4c8f2983e3e7d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4975aaf7385c630427acbeebd3888cb8d9a925f72a2b89a47d0c7caf9dd256a2(
    value: typing.Optional[DataLossPreventionJobTriggerTriggersManual],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80fa1d2ea235bf8f7591ff2de9fca84d9bdc0935e80c02cf41dd1d7cd64638e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb54859fcd9cec3908952d65f580dfa5b4b73c9716afe90cd4704a83d4cb549(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionJobTriggerTriggers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b26d9b508c6a2ee3e10b1fe1bb7abaf9236b0d6cc47fc250401201ee5ae692(
    *,
    recurrence_period_duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8aa0b2c08ea9789c731610914bc3231ec1d3f4b4eba45f7bde4a1d4166ef0e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__372833c4e6bcdbb0cdedcf9d2f64cdc085c332edfd591430789c38e015d47cc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b554e5e926acd1c83e4836a9ebdcc8e617b86b14d9583c70ed94e33a53deb31(
    value: typing.Optional[DataLossPreventionJobTriggerTriggersSchedule],
) -> None:
    """Type checking stubs"""
    pass

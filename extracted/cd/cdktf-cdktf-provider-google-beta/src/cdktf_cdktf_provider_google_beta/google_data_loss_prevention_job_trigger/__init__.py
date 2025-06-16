r'''
# `google_data_loss_prevention_job_trigger`

Refer to the Terraform Registry for docs: [`google_data_loss_prevention_job_trigger`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger).
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


class GoogleDataLossPreventionJobTrigger(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTrigger",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger google_data_loss_prevention_job_trigger}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        parent: builtins.str,
        triggers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerTriggers", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inspect_job: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJob", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trigger_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger google_data_loss_prevention_job_trigger} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param parent: The parent of the trigger, either in the format 'projects/{{project}}' or 'projects/{{project}}/locations/{{location}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#parent GoogleDataLossPreventionJobTrigger#parent}
        :param triggers: triggers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#triggers GoogleDataLossPreventionJobTrigger#triggers}
        :param description: A description of the job trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#description GoogleDataLossPreventionJobTrigger#description}
        :param display_name: User set display name of the job trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#display_name GoogleDataLossPreventionJobTrigger#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#id GoogleDataLossPreventionJobTrigger#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inspect_job: inspect_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#inspect_job GoogleDataLossPreventionJobTrigger#inspect_job}
        :param status: Whether the trigger is currently active. Default value: "HEALTHY" Possible values: ["PAUSED", "HEALTHY", "CANCELLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#status GoogleDataLossPreventionJobTrigger#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#timeouts GoogleDataLossPreventionJobTrigger#timeouts}
        :param trigger_id: The trigger id can contain uppercase and lowercase letters, numbers, and hyphens; that is, it must match the regular expression: [a-zA-Z\\d-_]+. The maximum length is 100 characters. Can be empty to allow the system to generate one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#trigger_id GoogleDataLossPreventionJobTrigger#trigger_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d0d9ea6bb81a21c3992292e2afbe9aa9a2f8f38abb4c99bebbd303fdcd845e7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataLossPreventionJobTriggerConfig(
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
        '''Generates CDKTF code for importing a GoogleDataLossPreventionJobTrigger resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataLossPreventionJobTrigger to import.
        :param import_from_id: The id of the existing GoogleDataLossPreventionJobTrigger that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataLossPreventionJobTrigger to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a699a7829d9198fbf3b62d7ea4bc7f99cdf2b559f972c56838c9f85bb5152b6b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putInspectJob")
    def put_inspect_job(
        self,
        *,
        storage_config: typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfig", typing.Dict[builtins.str, typing.Any]],
        actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inspect_config: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        inspect_template_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param storage_config: storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#storage_config GoogleDataLossPreventionJobTrigger#storage_config}
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#actions GoogleDataLossPreventionJobTrigger#actions}
        :param inspect_config: inspect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#inspect_config GoogleDataLossPreventionJobTrigger#inspect_config}
        :param inspect_template_name: The name of the template to run when this job is triggered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#inspect_template_name GoogleDataLossPreventionJobTrigger#inspect_template_name}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJob(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#create GoogleDataLossPreventionJobTrigger#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#delete GoogleDataLossPreventionJobTrigger#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#update GoogleDataLossPreventionJobTrigger#update}.
        '''
        value = GoogleDataLossPreventionJobTriggerTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTriggers")
    def put_triggers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerTriggers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400b0f28743c698651f83b72bafcbabdd42c0c88da17270ff3a0d2e0d18d25c3)
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
    def inspect_job(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobOutputReference", jsii.get(self, "inspectJob"))

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
    def timeouts(self) -> "GoogleDataLossPreventionJobTriggerTimeoutsOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(self) -> "GoogleDataLossPreventionJobTriggerTriggersList":
        return typing.cast("GoogleDataLossPreventionJobTriggerTriggersList", jsii.get(self, "triggers"))

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
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJob"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJob"], jsii.get(self, "inspectJobInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataLossPreventionJobTriggerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataLossPreventionJobTriggerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerIdInput")
    def trigger_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="triggersInput")
    def triggers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerTriggers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerTriggers"]]], jsii.get(self, "triggersInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__155b1978c1188e118f5fb3d8fc7892595da4bf40caba9edb413eb51d7feace0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa804a38c1453ebd38dceca6f16a250a172272fb27aab741d9217265095266e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e06de2f2e31d5ea87be92f71c4221086ff77037865625c0a1db2ffb511f243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__513067889f32f03cc5583d26fd36be5f01794103f98df7db23fef04129565838)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e3f36361a9e3b82ec15b503ec8557057dcf268981ff6b8fadf6ca42b5fa520b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerId")
    def trigger_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerId"))

    @trigger_id.setter
    def trigger_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c70733038492c1c3406b765dd430fa8e156ac0bffbb6baee5b79be821256988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerConfig",
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
class GoogleDataLossPreventionJobTriggerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        triggers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerTriggers", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inspect_job: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJob", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param parent: The parent of the trigger, either in the format 'projects/{{project}}' or 'projects/{{project}}/locations/{{location}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#parent GoogleDataLossPreventionJobTrigger#parent}
        :param triggers: triggers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#triggers GoogleDataLossPreventionJobTrigger#triggers}
        :param description: A description of the job trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#description GoogleDataLossPreventionJobTrigger#description}
        :param display_name: User set display name of the job trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#display_name GoogleDataLossPreventionJobTrigger#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#id GoogleDataLossPreventionJobTrigger#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inspect_job: inspect_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#inspect_job GoogleDataLossPreventionJobTrigger#inspect_job}
        :param status: Whether the trigger is currently active. Default value: "HEALTHY" Possible values: ["PAUSED", "HEALTHY", "CANCELLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#status GoogleDataLossPreventionJobTrigger#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#timeouts GoogleDataLossPreventionJobTrigger#timeouts}
        :param trigger_id: The trigger id can contain uppercase and lowercase letters, numbers, and hyphens; that is, it must match the regular expression: [a-zA-Z\\d-_]+. The maximum length is 100 characters. Can be empty to allow the system to generate one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#trigger_id GoogleDataLossPreventionJobTrigger#trigger_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(inspect_job, dict):
            inspect_job = GoogleDataLossPreventionJobTriggerInspectJob(**inspect_job)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataLossPreventionJobTriggerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe4c0cfb50e9869a9b0d7c6b1af7a4b24fb732dde8e14a5cdc4ee7d8bf43dff8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#parent GoogleDataLossPreventionJobTrigger#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def triggers(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerTriggers"]]:
        '''triggers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#triggers GoogleDataLossPreventionJobTrigger#triggers}
        '''
        result = self._values.get("triggers")
        assert result is not None, "Required property 'triggers' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerTriggers"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the job trigger.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#description GoogleDataLossPreventionJobTrigger#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User set display name of the job trigger.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#display_name GoogleDataLossPreventionJobTrigger#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#id GoogleDataLossPreventionJobTrigger#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inspect_job(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJob"]:
        '''inspect_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#inspect_job GoogleDataLossPreventionJobTrigger#inspect_job}
        '''
        result = self._values.get("inspect_job")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJob"], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Whether the trigger is currently active. Default value: "HEALTHY" Possible values: ["PAUSED", "HEALTHY", "CANCELLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#status GoogleDataLossPreventionJobTrigger#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDataLossPreventionJobTriggerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#timeouts GoogleDataLossPreventionJobTrigger#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerTimeouts"], result)

    @builtins.property
    def trigger_id(self) -> typing.Optional[builtins.str]:
        '''The trigger id can contain uppercase and lowercase letters, numbers, and hyphens;

        that is, it must match the regular expression: [a-zA-Z\\d-_]+.
        The maximum length is 100 characters. Can be empty to allow the system to generate one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#trigger_id GoogleDataLossPreventionJobTrigger#trigger_id}
        '''
        result = self._values.get("trigger_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJob",
    jsii_struct_bases=[],
    name_mapping={
        "storage_config": "storageConfig",
        "actions": "actions",
        "inspect_config": "inspectConfig",
        "inspect_template_name": "inspectTemplateName",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJob:
    def __init__(
        self,
        *,
        storage_config: typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfig", typing.Dict[builtins.str, typing.Any]],
        actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inspect_config: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        inspect_template_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param storage_config: storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#storage_config GoogleDataLossPreventionJobTrigger#storage_config}
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#actions GoogleDataLossPreventionJobTrigger#actions}
        :param inspect_config: inspect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#inspect_config GoogleDataLossPreventionJobTrigger#inspect_config}
        :param inspect_template_name: The name of the template to run when this job is triggered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#inspect_template_name GoogleDataLossPreventionJobTrigger#inspect_template_name}
        '''
        if isinstance(storage_config, dict):
            storage_config = GoogleDataLossPreventionJobTriggerInspectJobStorageConfig(**storage_config)
        if isinstance(inspect_config, dict):
            inspect_config = GoogleDataLossPreventionJobTriggerInspectJobInspectConfig(**inspect_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c5535fb08c747f6d7a676bf8fa45703765fd33ca44680acc73179a4e6ea5c4)
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
    def storage_config(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobStorageConfig":
        '''storage_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#storage_config GoogleDataLossPreventionJobTrigger#storage_config}
        '''
        result = self._values.get("storage_config")
        assert result is not None, "Required property 'storage_config' is missing"
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobStorageConfig", result)

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobActions"]]]:
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#actions GoogleDataLossPreventionJobTrigger#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobActions"]]], result)

    @builtins.property
    def inspect_config(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfig"]:
        '''inspect_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#inspect_config GoogleDataLossPreventionJobTrigger#inspect_config}
        '''
        result = self._values.get("inspect_config")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfig"], result)

    @builtins.property
    def inspect_template_name(self) -> typing.Optional[builtins.str]:
        '''The name of the template to run when this job is triggered.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#inspect_template_name GoogleDataLossPreventionJobTrigger#inspect_template_name}
        '''
        result = self._values.get("inspect_template_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActions",
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
class GoogleDataLossPreventionJobTriggerInspectJobActions:
    def __init__(
        self,
        *,
        deidentify: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentify", typing.Dict[builtins.str, typing.Any]]] = None,
        job_notification_emails: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails", typing.Dict[builtins.str, typing.Any]]] = None,
        publish_findings_to_cloud_data_catalog: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog", typing.Dict[builtins.str, typing.Any]]] = None,
        publish_summary_to_cscc: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc", typing.Dict[builtins.str, typing.Any]]] = None,
        publish_to_stackdriver: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver", typing.Dict[builtins.str, typing.Any]]] = None,
        pub_sub: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobActionsPubSub", typing.Dict[builtins.str, typing.Any]]] = None,
        save_findings: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param deidentify: deidentify block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#deidentify GoogleDataLossPreventionJobTrigger#deidentify}
        :param job_notification_emails: job_notification_emails block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#job_notification_emails GoogleDataLossPreventionJobTrigger#job_notification_emails}
        :param publish_findings_to_cloud_data_catalog: publish_findings_to_cloud_data_catalog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#publish_findings_to_cloud_data_catalog GoogleDataLossPreventionJobTrigger#publish_findings_to_cloud_data_catalog}
        :param publish_summary_to_cscc: publish_summary_to_cscc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#publish_summary_to_cscc GoogleDataLossPreventionJobTrigger#publish_summary_to_cscc}
        :param publish_to_stackdriver: publish_to_stackdriver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#publish_to_stackdriver GoogleDataLossPreventionJobTrigger#publish_to_stackdriver}
        :param pub_sub: pub_sub block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#pub_sub GoogleDataLossPreventionJobTrigger#pub_sub}
        :param save_findings: save_findings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#save_findings GoogleDataLossPreventionJobTrigger#save_findings}
        '''
        if isinstance(deidentify, dict):
            deidentify = GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentify(**deidentify)
        if isinstance(job_notification_emails, dict):
            job_notification_emails = GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails(**job_notification_emails)
        if isinstance(publish_findings_to_cloud_data_catalog, dict):
            publish_findings_to_cloud_data_catalog = GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog(**publish_findings_to_cloud_data_catalog)
        if isinstance(publish_summary_to_cscc, dict):
            publish_summary_to_cscc = GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc(**publish_summary_to_cscc)
        if isinstance(publish_to_stackdriver, dict):
            publish_to_stackdriver = GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver(**publish_to_stackdriver)
        if isinstance(pub_sub, dict):
            pub_sub = GoogleDataLossPreventionJobTriggerInspectJobActionsPubSub(**pub_sub)
        if isinstance(save_findings, dict):
            save_findings = GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindings(**save_findings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b42a7716ec1a69e95512aee92a77142168bf2ba103ac5b7dddf38ed3cb422a)
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
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentify"]:
        '''deidentify block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#deidentify GoogleDataLossPreventionJobTrigger#deidentify}
        '''
        result = self._values.get("deidentify")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentify"], result)

    @builtins.property
    def job_notification_emails(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails"]:
        '''job_notification_emails block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#job_notification_emails GoogleDataLossPreventionJobTrigger#job_notification_emails}
        '''
        result = self._values.get("job_notification_emails")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails"], result)

    @builtins.property
    def publish_findings_to_cloud_data_catalog(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog"]:
        '''publish_findings_to_cloud_data_catalog block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#publish_findings_to_cloud_data_catalog GoogleDataLossPreventionJobTrigger#publish_findings_to_cloud_data_catalog}
        '''
        result = self._values.get("publish_findings_to_cloud_data_catalog")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog"], result)

    @builtins.property
    def publish_summary_to_cscc(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc"]:
        '''publish_summary_to_cscc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#publish_summary_to_cscc GoogleDataLossPreventionJobTrigger#publish_summary_to_cscc}
        '''
        result = self._values.get("publish_summary_to_cscc")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc"], result)

    @builtins.property
    def publish_to_stackdriver(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver"]:
        '''publish_to_stackdriver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#publish_to_stackdriver GoogleDataLossPreventionJobTrigger#publish_to_stackdriver}
        '''
        result = self._values.get("publish_to_stackdriver")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver"], result)

    @builtins.property
    def pub_sub(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsPubSub"]:
        '''pub_sub block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#pub_sub GoogleDataLossPreventionJobTrigger#pub_sub}
        '''
        result = self._values.get("pub_sub")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsPubSub"], result)

    @builtins.property
    def save_findings(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindings"]:
        '''save_findings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#save_findings GoogleDataLossPreventionJobTrigger#save_findings}
        '''
        result = self._values.get("save_findings")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentify",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_storage_output": "cloudStorageOutput",
        "file_types_to_transform": "fileTypesToTransform",
        "transformation_config": "transformationConfig",
        "transformation_details_storage_config": "transformationDetailsStorageConfig",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentify:
    def __init__(
        self,
        *,
        cloud_storage_output: builtins.str,
        file_types_to_transform: typing.Optional[typing.Sequence[builtins.str]] = None,
        transformation_config: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        transformation_details_storage_config: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_output: User settable Cloud Storage bucket and folders to store de-identified files. This field must be set for cloud storage deidentification. The output Cloud Storage bucket must be different from the input bucket. De-identified files will overwrite files in the output path. Form of: gs://bucket/folder/ or gs://bucket Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#cloud_storage_output GoogleDataLossPreventionJobTrigger#cloud_storage_output}
        :param file_types_to_transform: List of user-specified file type groups to transform. If specified, only the files with these filetypes will be transformed. If empty, all supported files will be transformed. Supported types may be automatically added over time. If a file type is set in this field that isn't supported by the Deidentify action then the job will fail and will not be successfully created/started. Possible values: ["IMAGE", "TEXT_FILE", "CSV", "TSV"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#file_types_to_transform GoogleDataLossPreventionJobTrigger#file_types_to_transform}
        :param transformation_config: transformation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#transformation_config GoogleDataLossPreventionJobTrigger#transformation_config}
        :param transformation_details_storage_config: transformation_details_storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#transformation_details_storage_config GoogleDataLossPreventionJobTrigger#transformation_details_storage_config}
        '''
        if isinstance(transformation_config, dict):
            transformation_config = GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig(**transformation_config)
        if isinstance(transformation_details_storage_config, dict):
            transformation_details_storage_config = GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig(**transformation_details_storage_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31b9e86fe30f1ead6b784fdbf4002015bfdef2c370738d75329555efb3ec48b0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#cloud_storage_output GoogleDataLossPreventionJobTrigger#cloud_storage_output}
        '''
        result = self._values.get("cloud_storage_output")
        assert result is not None, "Required property 'cloud_storage_output' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def file_types_to_transform(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of user-specified file type groups to transform. If specified, only the files with these filetypes will be transformed.

        If empty, all supported files will be transformed. Supported types may be automatically added over time.

        If a file type is set in this field that isn't supported by the Deidentify action then the job will fail and will not be successfully created/started. Possible values: ["IMAGE", "TEXT_FILE", "CSV", "TSV"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#file_types_to_transform GoogleDataLossPreventionJobTrigger#file_types_to_transform}
        '''
        result = self._values.get("file_types_to_transform")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def transformation_config(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig"]:
        '''transformation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#transformation_config GoogleDataLossPreventionJobTrigger#transformation_config}
        '''
        result = self._values.get("transformation_config")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig"], result)

    @builtins.property
    def transformation_details_storage_config(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig"]:
        '''transformation_details_storage_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#transformation_details_storage_config GoogleDataLossPreventionJobTrigger#transformation_details_storage_config}
        '''
        result = self._values.get("transformation_details_storage_config")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentify(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e250ee6af80b32e3cdd6ceed736152f47681624d7c6318549d40c0ae12379263)
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
        :param deidentify_template: If this template is specified, it will serve as the default de-identify template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#deidentify_template GoogleDataLossPreventionJobTrigger#deidentify_template}
        :param image_redact_template: If this template is specified, it will serve as the de-identify template for images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#image_redact_template GoogleDataLossPreventionJobTrigger#image_redact_template}
        :param structured_deidentify_template: If this template is specified, it will serve as the de-identify template for structured content such as delimited files and tables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#structured_deidentify_template GoogleDataLossPreventionJobTrigger#structured_deidentify_template}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig(
            deidentify_template=deidentify_template,
            image_redact_template=image_redact_template,
            structured_deidentify_template=structured_deidentify_template,
        )

        return typing.cast(None, jsii.invoke(self, "putTransformationConfig", [value]))

    @jsii.member(jsii_name="putTransformationDetailsStorageConfig")
    def put_transformation_details_storage_config(
        self,
        *,
        table: typing.Union["GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param table: table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table GoogleDataLossPreventionJobTrigger#table}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig(
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
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfigOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfigOutputReference", jsii.get(self, "transformationConfig"))

    @builtins.property
    @jsii.member(jsii_name="transformationDetailsStorageConfig")
    def transformation_details_storage_config(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigOutputReference", jsii.get(self, "transformationDetailsStorageConfig"))

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
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig"], jsii.get(self, "transformationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="transformationDetailsStorageConfigInput")
    def transformation_details_storage_config_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig"], jsii.get(self, "transformationDetailsStorageConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageOutput")
    def cloud_storage_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudStorageOutput"))

    @cloud_storage_output.setter
    def cloud_storage_output(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__232869f72d01ae1a405a1154dee5739ed128b0b30865566a574eceb761db5250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudStorageOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileTypesToTransform")
    def file_types_to_transform(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileTypesToTransform"))

    @file_types_to_transform.setter
    def file_types_to_transform(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46662e7b01e357a2b0e87b8ebec8a2bbda29baaadc18a8513eafcbe367aee67a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileTypesToTransform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentify]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentify], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentify],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630ff36f80174f3e04b676b935c1123b04174eacb83db16693c70e792a48511a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "deidentify_template": "deidentifyTemplate",
        "image_redact_template": "imageRedactTemplate",
        "structured_deidentify_template": "structuredDeidentifyTemplate",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig:
    def __init__(
        self,
        *,
        deidentify_template: typing.Optional[builtins.str] = None,
        image_redact_template: typing.Optional[builtins.str] = None,
        structured_deidentify_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deidentify_template: If this template is specified, it will serve as the default de-identify template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#deidentify_template GoogleDataLossPreventionJobTrigger#deidentify_template}
        :param image_redact_template: If this template is specified, it will serve as the de-identify template for images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#image_redact_template GoogleDataLossPreventionJobTrigger#image_redact_template}
        :param structured_deidentify_template: If this template is specified, it will serve as the de-identify template for structured content such as delimited files and tables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#structured_deidentify_template GoogleDataLossPreventionJobTrigger#structured_deidentify_template}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64219629580f38536ebeb7e99b6d9cdec7dace61b48e7e64b7bb9dfb9aa1ae60)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#deidentify_template GoogleDataLossPreventionJobTrigger#deidentify_template}
        '''
        result = self._values.get("deidentify_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_redact_template(self) -> typing.Optional[builtins.str]:
        '''If this template is specified, it will serve as the de-identify template for images.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#image_redact_template GoogleDataLossPreventionJobTrigger#image_redact_template}
        '''
        result = self._values.get("image_redact_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def structured_deidentify_template(self) -> typing.Optional[builtins.str]:
        '''If this template is specified, it will serve as the de-identify template for structured content such as delimited files and tables.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#structured_deidentify_template GoogleDataLossPreventionJobTrigger#structured_deidentify_template}
        '''
        result = self._values.get("structured_deidentify_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21a8a8c69865d74cb375a6c4e6d7854b75c12ae273c7969ef136a5470f770921)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f359923872a5c67f5ac249eecc1bb57235f82fff749a1874440fa7bb6cc8b245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deidentifyTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageRedactTemplate")
    def image_redact_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageRedactTemplate"))

    @image_redact_template.setter
    def image_redact_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a5cd57119b434da197c10822a37ba1a72c16b5ac9aef86056ed8b4d3a720ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageRedactTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="structuredDeidentifyTemplate")
    def structured_deidentify_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "structuredDeidentifyTemplate"))

    @structured_deidentify_template.setter
    def structured_deidentify_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b51b4405ba45d2f73bf75019f571ec21dabff5b6e99fdc247e2a53177a8f7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "structuredDeidentifyTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a823ac0410e0791c66b22b3090dc51914237ed461895d0e28e92e15e9b23d2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig",
    jsii_struct_bases=[],
    name_mapping={"table": "table"},
)
class GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig:
    def __init__(
        self,
        *,
        table: typing.Union["GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param table: table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table GoogleDataLossPreventionJobTrigger#table}
        '''
        if isinstance(table, dict):
            table = GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable(**table)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14b140b092f89441e16a1f8329ad73d20ada8dbed19edc0e8951d9829b3eee9f)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table": table,
        }

    @builtins.property
    def table(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable":
        '''table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table GoogleDataLossPreventionJobTrigger#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4115963d7d6adc60a9800cca1b64e97e300ed5f3d4de4c2d015d4b80dbc5398)
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
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#dataset_id GoogleDataLossPreventionJobTrigger#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#project_id GoogleDataLossPreventionJobTrigger#project_id}
        :param table_id: The ID of the table. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 1,024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table_id GoogleDataLossPreventionJobTrigger#table_id}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable(
            dataset_id=dataset_id, project_id=project_id, table_id=table_id
        )

        return typing.cast(None, jsii.invoke(self, "putTable", [value]))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTableOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTableOutputReference", jsii.get(self, "table"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable"], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01439deb77d02a6fe57c1d584276c0eeb5cd6e633126aae9d98c01da590b15ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id": "datasetId",
        "project_id": "projectId",
        "table_id": "tableId",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable:
    def __init__(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#dataset_id GoogleDataLossPreventionJobTrigger#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#project_id GoogleDataLossPreventionJobTrigger#project_id}
        :param table_id: The ID of the table. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 1,024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table_id GoogleDataLossPreventionJobTrigger#table_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e5dfae1ac30e9b2a65d228dd120db01004652475bb0367789dc62079cbe5fe0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#dataset_id GoogleDataLossPreventionJobTrigger#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The ID of the project containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#project_id GoogleDataLossPreventionJobTrigger#project_id}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table_id GoogleDataLossPreventionJobTrigger#table_id}
        '''
        result = self._values.get("table_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6d332b6829bd0fc98afaf00befb1360090bf97b1ba1a7162adf61ca6b96af1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90cbdf5f2344dfb00d188339b903b2f0cab8e6daa6522575641c4c2231c44b51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5a5faeaf93ab20f2f41232dec60cd25cc6f488b7db59e45fc2e01c5ddffcb43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac4c7cd2047e58a0b43a207e92ac442a666413e539270bf57d3eb5074789fe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0846541d69e4ec525b383d76c5598917dcbdf5a7c02c7377c3a9e99f0a1f2e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc69885c175ff367efa7dd29c24f0a76ee147e38a31a585a4424a2ae19e0e47e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a07bad0c78e106ca8743e7fc9f64fd9592feb593580cee83bda455e16aa502)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ada89d2b4bd33bfae64f00c58e4809bad95edb650a9394c8aaa9c9e2337946e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07166fc1b8bd816095ecb7f70f3ba1fbeca053dad1bc5b7d01a4053431d80813)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0238de74f76d7a0a29c10c53a0925e4d51afe78a72fb7ad2a45522d3069bde33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee82a645360b715581d58d263051a5a1e6dc2803c15c84550dadc383c52cd739)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b8063ba8e553098fb83f03e0272a4f1fee5c25b923d920ebdddfbb750a42b77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50eff909f45fb741e3f63b6ff9a2e0f68fa7dfe7a1895fd56473e3607f7e951c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4394ed47f2cbfccfc55da7085a29b6f6e08454cfb6e776155c90834adae16187)
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
        transformation_config: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        transformation_details_storage_config: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_output: User settable Cloud Storage bucket and folders to store de-identified files. This field must be set for cloud storage deidentification. The output Cloud Storage bucket must be different from the input bucket. De-identified files will overwrite files in the output path. Form of: gs://bucket/folder/ or gs://bucket Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#cloud_storage_output GoogleDataLossPreventionJobTrigger#cloud_storage_output}
        :param file_types_to_transform: List of user-specified file type groups to transform. If specified, only the files with these filetypes will be transformed. If empty, all supported files will be transformed. Supported types may be automatically added over time. If a file type is set in this field that isn't supported by the Deidentify action then the job will fail and will not be successfully created/started. Possible values: ["IMAGE", "TEXT_FILE", "CSV", "TSV"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#file_types_to_transform GoogleDataLossPreventionJobTrigger#file_types_to_transform}
        :param transformation_config: transformation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#transformation_config GoogleDataLossPreventionJobTrigger#transformation_config}
        :param transformation_details_storage_config: transformation_details_storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#transformation_details_storage_config GoogleDataLossPreventionJobTrigger#transformation_details_storage_config}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentify(
            cloud_storage_output=cloud_storage_output,
            file_types_to_transform=file_types_to_transform,
            transformation_config=transformation_config,
            transformation_details_storage_config=transformation_details_storage_config,
        )

        return typing.cast(None, jsii.invoke(self, "putDeidentify", [value]))

    @jsii.member(jsii_name="putJobNotificationEmails")
    def put_job_notification_emails(self) -> None:
        value = GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails()

        return typing.cast(None, jsii.invoke(self, "putJobNotificationEmails", [value]))

    @jsii.member(jsii_name="putPublishFindingsToCloudDataCatalog")
    def put_publish_findings_to_cloud_data_catalog(self) -> None:
        value = GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog()

        return typing.cast(None, jsii.invoke(self, "putPublishFindingsToCloudDataCatalog", [value]))

    @jsii.member(jsii_name="putPublishSummaryToCscc")
    def put_publish_summary_to_cscc(self) -> None:
        value = GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc()

        return typing.cast(None, jsii.invoke(self, "putPublishSummaryToCscc", [value]))

    @jsii.member(jsii_name="putPublishToStackdriver")
    def put_publish_to_stackdriver(self) -> None:
        value = GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver()

        return typing.cast(None, jsii.invoke(self, "putPublishToStackdriver", [value]))

    @jsii.member(jsii_name="putPubSub")
    def put_pub_sub(self, *, topic: builtins.str) -> None:
        '''
        :param topic: Cloud Pub/Sub topic to send notifications to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#topic GoogleDataLossPreventionJobTrigger#topic}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobActionsPubSub(topic=topic)

        return typing.cast(None, jsii.invoke(self, "putPubSub", [value]))

    @jsii.member(jsii_name="putSaveFindings")
    def put_save_findings(
        self,
        *,
        output_config: typing.Union["GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param output_config: output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#output_config GoogleDataLossPreventionJobTrigger#output_config}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindings(
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
    ) -> GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyOutputReference, jsii.get(self, "deidentify"))

    @builtins.property
    @jsii.member(jsii_name="jobNotificationEmails")
    def job_notification_emails(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmailsOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmailsOutputReference, jsii.get(self, "jobNotificationEmails"))

    @builtins.property
    @jsii.member(jsii_name="publishFindingsToCloudDataCatalog")
    def publish_findings_to_cloud_data_catalog(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalogOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalogOutputReference", jsii.get(self, "publishFindingsToCloudDataCatalog"))

    @builtins.property
    @jsii.member(jsii_name="publishSummaryToCscc")
    def publish_summary_to_cscc(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCsccOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCsccOutputReference", jsii.get(self, "publishSummaryToCscc"))

    @builtins.property
    @jsii.member(jsii_name="publishToStackdriver")
    def publish_to_stackdriver(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriverOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriverOutputReference", jsii.get(self, "publishToStackdriver"))

    @builtins.property
    @jsii.member(jsii_name="pubSub")
    def pub_sub(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobActionsPubSubOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobActionsPubSubOutputReference", jsii.get(self, "pubSub"))

    @builtins.property
    @jsii.member(jsii_name="saveFindings")
    def save_findings(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputReference", jsii.get(self, "saveFindings"))

    @builtins.property
    @jsii.member(jsii_name="deidentifyInput")
    def deidentify_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentify]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentify], jsii.get(self, "deidentifyInput"))

    @builtins.property
    @jsii.member(jsii_name="jobNotificationEmailsInput")
    def job_notification_emails_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails], jsii.get(self, "jobNotificationEmailsInput"))

    @builtins.property
    @jsii.member(jsii_name="publishFindingsToCloudDataCatalogInput")
    def publish_findings_to_cloud_data_catalog_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog"], jsii.get(self, "publishFindingsToCloudDataCatalogInput"))

    @builtins.property
    @jsii.member(jsii_name="publishSummaryToCsccInput")
    def publish_summary_to_cscc_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc"], jsii.get(self, "publishSummaryToCsccInput"))

    @builtins.property
    @jsii.member(jsii_name="publishToStackdriverInput")
    def publish_to_stackdriver_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver"], jsii.get(self, "publishToStackdriverInput"))

    @builtins.property
    @jsii.member(jsii_name="pubSubInput")
    def pub_sub_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsPubSub"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsPubSub"], jsii.get(self, "pubSubInput"))

    @builtins.property
    @jsii.member(jsii_name="saveFindingsInput")
    def save_findings_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindings"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindings"], jsii.get(self, "saveFindingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92811793c327aecb7abb5cd4b7a3a65582ea32c25476e925d6e290aba34d74f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsPubSub",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic"},
)
class GoogleDataLossPreventionJobTriggerInspectJobActionsPubSub:
    def __init__(self, *, topic: builtins.str) -> None:
        '''
        :param topic: Cloud Pub/Sub topic to send notifications to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#topic GoogleDataLossPreventionJobTrigger#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87fd1c64967036117c81eccbe629974df83c57db2db988bcdddcae863d8c4762)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic": topic,
        }

    @builtins.property
    def topic(self) -> builtins.str:
        '''Cloud Pub/Sub topic to send notifications to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#topic GoogleDataLossPreventionJobTrigger#topic}
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobActionsPubSub(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobActionsPubSubOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsPubSubOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf8d19d736c64e816a63c8b64aea56b7df27cab33f0e0e63fc5a0606b424c66b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa3eee9b5ad9285a28bebf2b19c26b4cbac2322b3b93664faa8c7465fe62701e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsPubSub]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsPubSub], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsPubSub],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__556acc8c03cdc5ddd8f25d1a40959a946c1390484e86d3e904e3f69ee76551d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adaabce584badbe1c56d1fa6df9a6e506aaef11ac657121a195204fdc483d8e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed822284194d218b539539947236940c63cee6bb898bad0f7d7595f399c5655f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCsccOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCsccOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06c841dc236c8aff9a8d1ca575526d6328bed02ae9a28dcbcd5ef0612de60a05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c4ba3d344674af5d5b44bb4ab23729fbb5082b1ad4b7aedd39a5fbe308af9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bd19d840e30c3f24e2a7d5f6706240da874d362f6273720fa8ca7ceb6b53896)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2f5569cf5a193a75170b808e23f50654d8ad6e82404dbd4dd0b7d015123f95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindings",
    jsii_struct_bases=[],
    name_mapping={"output_config": "outputConfig"},
)
class GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindings:
    def __init__(
        self,
        *,
        output_config: typing.Union["GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param output_config: output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#output_config GoogleDataLossPreventionJobTrigger#output_config}
        '''
        if isinstance(output_config, dict):
            output_config = GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig(**output_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653c253abc1015bd8d0c854597a750c18d634b70116c5a33d070ca383cbe736c)
            check_type(argname="argument output_config", value=output_config, expected_type=type_hints["output_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "output_config": output_config,
        }

    @builtins.property
    def output_config(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig":
        '''output_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#output_config GoogleDataLossPreventionJobTrigger#output_config}
        '''
        result = self._values.get("output_config")
        assert result is not None, "Required property 'output_config' is missing"
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig",
    jsii_struct_bases=[],
    name_mapping={"table": "table", "output_schema": "outputSchema"},
)
class GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig:
    def __init__(
        self,
        *,
        table: typing.Union["GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable", typing.Dict[builtins.str, typing.Any]],
        output_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table: table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table GoogleDataLossPreventionJobTrigger#table}
        :param output_schema: Schema used for writing the findings for Inspect jobs. This field is only used for Inspect and must be unspecified for Risk jobs. Columns are derived from the Finding object. If appending to an existing table, any columns from the predefined schema that are missing will be added. No columns in the existing table will be deleted. If unspecified, then all available columns will be used for a new table or an (existing) table with no schema, and no changes will be made to an existing table that has a schema. Only for use with external storage. Possible values: ["BASIC_COLUMNS", "GCS_COLUMNS", "DATASTORE_COLUMNS", "BIG_QUERY_COLUMNS", "ALL_COLUMNS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#output_schema GoogleDataLossPreventionJobTrigger#output_schema}
        '''
        if isinstance(table, dict):
            table = GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable(**table)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aff6af371263bf589c86949300f2695ca78641f969b4e20b7f81a977baba1860)
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
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable":
        '''table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table GoogleDataLossPreventionJobTrigger#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable", result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#output_schema GoogleDataLossPreventionJobTrigger#output_schema}
        '''
        result = self._values.get("output_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bc68da821c9c3c64fbcbb6db56df7ddff67663508cae084765d8d851c9ab706)
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
        :param dataset_id: Dataset ID of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#dataset_id GoogleDataLossPreventionJobTrigger#dataset_id}
        :param project_id: The Google Cloud Platform project ID of the project containing the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#project_id GoogleDataLossPreventionJobTrigger#project_id}
        :param table_id: Name of the table. If is not set a new one will be generated for you with the following format: 'dlp_googleapis_yyyy_mm_dd_[dlp_job_id]'. Pacific timezone will be used for generating the date details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table_id GoogleDataLossPreventionJobTrigger#table_id}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable(
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
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTableOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTableOutputReference", jsii.get(self, "table"))

    @builtins.property
    @jsii.member(jsii_name="outputSchemaInput")
    def output_schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable"], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="outputSchema")
    def output_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputSchema"))

    @output_schema.setter
    def output_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80abc1a808d2392cdf67a6ba7da1ebb8b1ef4b274541e35abb57c6ed9b687113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d887bdf2aaff0732dbe05fe4f94be5898830bc575273bd6022ae1e61bdfd582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id": "datasetId",
        "project_id": "projectId",
        "table_id": "tableId",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable:
    def __init__(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataset_id: Dataset ID of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#dataset_id GoogleDataLossPreventionJobTrigger#dataset_id}
        :param project_id: The Google Cloud Platform project ID of the project containing the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#project_id GoogleDataLossPreventionJobTrigger#project_id}
        :param table_id: Name of the table. If is not set a new one will be generated for you with the following format: 'dlp_googleapis_yyyy_mm_dd_[dlp_job_id]'. Pacific timezone will be used for generating the date details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table_id GoogleDataLossPreventionJobTrigger#table_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb1dafabd8bf35ef4fd6a6b8919997be86c26940a85b6b4846de19c08ad1b37)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#dataset_id GoogleDataLossPreventionJobTrigger#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The Google Cloud Platform project ID of the project containing the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#project_id GoogleDataLossPreventionJobTrigger#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_id(self) -> typing.Optional[builtins.str]:
        '''Name of the table.

        If is not set a new one will be generated for you with the following format:
        'dlp_googleapis_yyyy_mm_dd_[dlp_job_id]'. Pacific timezone will be used for generating the date details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table_id GoogleDataLossPreventionJobTrigger#table_id}
        '''
        result = self._values.get("table_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99c059279c67702a6689b344f4cd666a68c2ed66b484d1909063aaed14817e4a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e92610c5c8cf1f5dfe8711345371a151da3d8ebf71276b277805e8a028e9d0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a626d7a5ed0b54ee4b293017fbf1086c98819858bcb818e18287cfa718ea58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0efe03f64d4c645e92616373817cec6e6e59824d45ffc2a21dc6fec64d69651c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8967065c5338b7e415a4b1b5861e9b30235e4f7fe4d9eb1afa911cb6336da5cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6fb2a2e6c436bd5f88c5ef9cab9483f7babb57f49f83770d8a316ebd5b8c566)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOutputConfig")
    def put_output_config(
        self,
        *,
        table: typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable, typing.Dict[builtins.str, typing.Any]],
        output_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table: table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table GoogleDataLossPreventionJobTrigger#table}
        :param output_schema: Schema used for writing the findings for Inspect jobs. This field is only used for Inspect and must be unspecified for Risk jobs. Columns are derived from the Finding object. If appending to an existing table, any columns from the predefined schema that are missing will be added. No columns in the existing table will be deleted. If unspecified, then all available columns will be used for a new table or an (existing) table with no schema, and no changes will be made to an existing table that has a schema. Only for use with external storage. Possible values: ["BASIC_COLUMNS", "GCS_COLUMNS", "DATASTORE_COLUMNS", "BIG_QUERY_COLUMNS", "ALL_COLUMNS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#output_schema GoogleDataLossPreventionJobTrigger#output_schema}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig(
            table=table, output_schema=output_schema
        )

        return typing.cast(None, jsii.invoke(self, "putOutputConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="outputConfig")
    def output_config(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigOutputReference, jsii.get(self, "outputConfig"))

    @builtins.property
    @jsii.member(jsii_name="outputConfigInput")
    def output_config_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig], jsii.get(self, "outputConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindings]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f092e5d3963e076c06dc47c696b1a744f5d801677b9fbff68c8a8ade0a8bfb2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfig",
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
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfig:
    def __init__(
        self,
        *,
        custom_info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        exclude_info_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_quote: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        limits: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        min_likelihood: typing.Optional[builtins.str] = None,
        rule_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param custom_info_types: custom_info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#custom_info_types GoogleDataLossPreventionJobTrigger#custom_info_types}
        :param exclude_info_types: When true, excludes type information of the findings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#exclude_info_types GoogleDataLossPreventionJobTrigger#exclude_info_types}
        :param include_quote: When true, a contextual quote from the data that triggered a finding is included in the response. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#include_quote GoogleDataLossPreventionJobTrigger#include_quote}
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#info_types GoogleDataLossPreventionJobTrigger#info_types}
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#limits GoogleDataLossPreventionJobTrigger#limits}
        :param min_likelihood: Only returns findings equal or above this threshold. See https://cloud.google.com/dlp/docs/likelihood for more info Default value: "POSSIBLE" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#min_likelihood GoogleDataLossPreventionJobTrigger#min_likelihood}
        :param rule_set: rule_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#rule_set GoogleDataLossPreventionJobTrigger#rule_set}
        '''
        if isinstance(limits, dict):
            limits = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimits(**limits)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__990804f5e89328643ef870ba14ff1c7aa3dae254643f0cf5e53cd131c1a597d9)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes"]]]:
        '''custom_info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#custom_info_types GoogleDataLossPreventionJobTrigger#custom_info_types}
        '''
        result = self._values.get("custom_info_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes"]]], result)

    @builtins.property
    def exclude_info_types(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, excludes type information of the findings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#exclude_info_types GoogleDataLossPreventionJobTrigger#exclude_info_types}
        '''
        result = self._values.get("exclude_info_types")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_quote(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, a contextual quote from the data that triggered a finding is included in the response.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#include_quote GoogleDataLossPreventionJobTrigger#include_quote}
        '''
        result = self._values.get("include_quote")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def info_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes"]]]:
        '''info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#info_types GoogleDataLossPreventionJobTrigger#info_types}
        '''
        result = self._values.get("info_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes"]]], result)

    @builtins.property
    def limits(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimits"]:
        '''limits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#limits GoogleDataLossPreventionJobTrigger#limits}
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimits"], result)

    @builtins.property
    def min_likelihood(self) -> typing.Optional[builtins.str]:
        '''Only returns findings equal or above this threshold.

        See https://cloud.google.com/dlp/docs/likelihood for more info Default value: "POSSIBLE" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#min_likelihood GoogleDataLossPreventionJobTrigger#min_likelihood}
        '''
        result = self._values.get("min_likelihood")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_set(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet"]]]:
        '''rule_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#rule_set GoogleDataLossPreventionJobTrigger#rule_set}
        '''
        result = self._values.get("rule_set")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes",
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
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes:
    def __init__(
        self,
        *,
        info_type: typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType", typing.Dict[builtins.str, typing.Any]],
        dictionary: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusion_type: typing.Optional[builtins.str] = None,
        likelihood: typing.Optional[builtins.str] = None,
        regex: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex", typing.Dict[builtins.str, typing.Any]]] = None,
        sensitivity_score: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        stored_type: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType", typing.Dict[builtins.str, typing.Any]]] = None,
        surrogate_type: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param info_type: info_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#info_type GoogleDataLossPreventionJobTrigger#info_type}
        :param dictionary: dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#dictionary GoogleDataLossPreventionJobTrigger#dictionary}
        :param exclusion_type: If set to EXCLUSION_TYPE_EXCLUDE this infoType will not cause a finding to be returned. It still can be used for rules matching. Possible values: ["EXCLUSION_TYPE_EXCLUDE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#exclusion_type GoogleDataLossPreventionJobTrigger#exclusion_type}
        :param likelihood: Likelihood to return for this CustomInfoType. This base value can be altered by a detection rule if the finding meets the criteria specified by the rule. Default value: "VERY_LIKELY" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#likelihood GoogleDataLossPreventionJobTrigger#likelihood}
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#regex GoogleDataLossPreventionJobTrigger#regex}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sensitivity_score GoogleDataLossPreventionJobTrigger#sensitivity_score}
        :param stored_type: stored_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#stored_type GoogleDataLossPreventionJobTrigger#stored_type}
        :param surrogate_type: surrogate_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#surrogate_type GoogleDataLossPreventionJobTrigger#surrogate_type}
        '''
        if isinstance(info_type, dict):
            info_type = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType(**info_type)
        if isinstance(dictionary, dict):
            dictionary = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary(**dictionary)
        if isinstance(regex, dict):
            regex = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex(**regex)
        if isinstance(sensitivity_score, dict):
            sensitivity_score = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore(**sensitivity_score)
        if isinstance(stored_type, dict):
            stored_type = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType(**stored_type)
        if isinstance(surrogate_type, dict):
            surrogate_type = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType(**surrogate_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a3e8d1de39e857f825d62d7c10b3c120e2e10e49654a7992bbf156b5b94b93)
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
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType":
        '''info_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#info_type GoogleDataLossPreventionJobTrigger#info_type}
        '''
        result = self._values.get("info_type")
        assert result is not None, "Required property 'info_type' is missing"
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType", result)

    @builtins.property
    def dictionary(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary"]:
        '''dictionary block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#dictionary GoogleDataLossPreventionJobTrigger#dictionary}
        '''
        result = self._values.get("dictionary")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary"], result)

    @builtins.property
    def exclusion_type(self) -> typing.Optional[builtins.str]:
        '''If set to EXCLUSION_TYPE_EXCLUDE this infoType will not cause a finding to be returned.

        It still can be used for rules matching. Possible values: ["EXCLUSION_TYPE_EXCLUDE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#exclusion_type GoogleDataLossPreventionJobTrigger#exclusion_type}
        '''
        result = self._values.get("exclusion_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def likelihood(self) -> typing.Optional[builtins.str]:
        '''Likelihood to return for this CustomInfoType.

        This base value can be altered by a detection rule if the finding meets the criteria
        specified by the rule. Default value: "VERY_LIKELY" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#likelihood GoogleDataLossPreventionJobTrigger#likelihood}
        '''
        result = self._values.get("likelihood")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex"]:
        '''regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#regex GoogleDataLossPreventionJobTrigger#regex}
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex"], result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sensitivity_score GoogleDataLossPreventionJobTrigger#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore"], result)

    @builtins.property
    def stored_type(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType"]:
        '''stored_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#stored_type GoogleDataLossPreventionJobTrigger#stored_type}
        '''
        result = self._values.get("stored_type")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType"], result)

    @builtins.property
    def surrogate_type(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType"]:
        '''surrogate_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#surrogate_type GoogleDataLossPreventionJobTrigger#surrogate_type}
        '''
        result = self._values.get("surrogate_type")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary",
    jsii_struct_bases=[],
    name_mapping={"cloud_storage_path": "cloudStoragePath", "word_list": "wordList"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary:
    def __init__(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath", typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#cloud_storage_path GoogleDataLossPreventionJobTrigger#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#word_list GoogleDataLossPreventionJobTrigger#word_list}
        '''
        if isinstance(cloud_storage_path, dict):
            cloud_storage_path = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath(**cloud_storage_path)
        if isinstance(word_list, dict):
            word_list = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct(**word_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee54f21583bd634099308f1cd9d232547b37d53875318519f9010de8fe1412c2)
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
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath"]:
        '''cloud_storage_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#cloud_storage_path GoogleDataLossPreventionJobTrigger#cloud_storage_path}
        '''
        result = self._values.get("cloud_storage_path")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath"], result)

    @builtins.property
    def word_list(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct"]:
        '''word_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#word_list GoogleDataLossPreventionJobTrigger#word_list}
        '''
        result = self._values.get("word_list")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath:
    def __init__(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#path GoogleDataLossPreventionJobTrigger#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0322b910f0bcf63cc853ee7604fc4031cc82fa5258b979e2eeee838fae18602e)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#path GoogleDataLossPreventionJobTrigger#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef1ecd58f41881f0105dd1a93ca00bc1d546c84f1036a180153b3451ab44a62b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__412b71f6dda9ad0489aa9423b94f9ae70ef81ad5dfadde76b621083992df930f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d26884c9041faa2915b0b9038021c65a17f1160a60e7216398442b314f4f1d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddcb9bd9d29da11fbe03a86d1b16f487ee8153d62ed231ea2162cd0dfc20f03d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudStoragePath")
    def put_cloud_storage_path(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#path GoogleDataLossPreventionJobTrigger#path}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath(
            path=path
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStoragePath", [value]))

    @jsii.member(jsii_name="putWordList")
    def put_word_list(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#words GoogleDataLossPreventionJobTrigger#words}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct(
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
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference, jsii.get(self, "cloudStoragePath"))

    @builtins.property
    @jsii.member(jsii_name="wordList")
    def word_list(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference", jsii.get(self, "wordList"))

    @builtins.property
    @jsii.member(jsii_name="cloudStoragePathInput")
    def cloud_storage_path_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath], jsii.get(self, "cloudStoragePathInput"))

    @builtins.property
    @jsii.member(jsii_name="wordListInput")
    def word_list_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct"], jsii.get(self, "wordListInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf720fb292de9fce91b355f6ace5a5d076341cd3c8a865065f16c7412ed806cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct",
    jsii_struct_bases=[],
    name_mapping={"words": "words"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct:
    def __init__(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#words GoogleDataLossPreventionJobTrigger#words}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__102e66a9782ae7ed5314de1c990594bcf9f65b9fc4be0393bb4bed0371fd9135)
            check_type(argname="argument words", value=words, expected_type=type_hints["words"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "words": words,
        }

    @builtins.property
    def words(self) -> typing.List[builtins.str]:
        '''Words or phrases defining the dictionary.

        The dictionary must contain at least one
        phrase and every phrase must contain at least 2 characters that are letters or digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#words GoogleDataLossPreventionJobTrigger#words}
        '''
        result = self._values.get("words")
        assert result is not None, "Required property 'words' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b32b20be57abe505824ffc89062189912bb24d2d80814c503a5572474e26e6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__827bc6bd7af8a436fb3864eda65751430f011932a8410161387931e0b6fa97ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "words", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcef7375ff6cec402e48e06ac5a718623cbceb947fc84a935116ce2fc8a7bd74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sensitivity_score GoogleDataLossPreventionJobTrigger#sensitivity_score}
        :param version: Version of the information type to use. By default, the version is set to stable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#version GoogleDataLossPreventionJobTrigger#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05aad19afbbe280b7d5e0fbaf97e2602660f0065a580ecea39b72712beb760f8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sensitivity_score GoogleDataLossPreventionJobTrigger#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the information type to use. By default, the version is set to stable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#version GoogleDataLossPreventionJobTrigger#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a58af48a78345521f0b0d4a25da10c5eb60289bc259b5297da0c6fdf64852bec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore(
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
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__709974c4fb2b7102a3225b5fbd7c204f93420ce22847130af8135e4da854e4de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c48fd0bb65db44b5742b6f5f2f2aefc3ac5f15a5d0a9548cd5fc5361d16d47d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f78eaf423cdb89ca013a4185c939e5e94bec21db4653aba50155ccbca7ce846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b75e4a08b4dfc7adf4120a791473e3176de56cf0363725f37928e9daaffc8bb1)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efdd949d73444e1d0e8e7356f6fde912ccaeeb41f2694991d19b89b45ca62458)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03f4f9d8b40e0dc68a785c0a956bed207d6da0cb9f58a163cf2a08fdb74ec311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e648fc08ccdd5fc9891c14efe7d561799d15f259bd60871f892a827f23f7c73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71886681629ed4d0f00d5ba004551513ac8c21108d23ef3a7994e9da6c09245d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a9c9b47e18e268bdf7b1c14bc501cb1d8666b1e60fab10e5c82ca7ca93ca08e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac590962b03383938528954c77ec39969a575b519bdb08122d15fb6a203b682)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2003945b1416fe56560384a90c3d6bc4bf6d2d72d7627b58f5e059cf57ccc48f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83576019c6e470b68ecf8127068b8fc3dc13ffbedb24bc55b27f9dc3df4834ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac6af239d75aed1017bc43c6c32f71dabdeb37fec7d528a2a46f4e880497f2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9b81f8488c567d8715313c0555b70092e252060ff394fc069ffb094b99b7c34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDictionary")
    def put_dictionary(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#cloud_storage_path GoogleDataLossPreventionJobTrigger#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#word_list GoogleDataLossPreventionJobTrigger#word_list}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary(
            cloud_storage_path=cloud_storage_path, word_list=word_list
        )

        return typing.cast(None, jsii.invoke(self, "putDictionary", [value]))

    @jsii.member(jsii_name="putInfoType")
    def put_info_type(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sensitivity_score GoogleDataLossPreventionJobTrigger#sensitivity_score}
        :param version: Version of the information type to use. By default, the version is set to stable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#version GoogleDataLossPreventionJobTrigger#version}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType(
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
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#pattern GoogleDataLossPreventionJobTrigger#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#group_indexes GoogleDataLossPreventionJobTrigger#group_indexes}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex(
            pattern=pattern, group_indexes=group_indexes
        )

        return typing.cast(None, jsii.invoke(self, "putRegex", [value]))

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore(
            score=score
        )

        return typing.cast(None, jsii.invoke(self, "putSensitivityScore", [value]))

    @jsii.member(jsii_name="putStoredType")
    def put_stored_type(self, *, name: builtins.str) -> None:
        '''
        :param name: Resource name of the requested StoredInfoType, for example 'organizations/433245324/storedInfoTypes/432452342' or 'projects/project-id/storedInfoTypes/432452342'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putStoredType", [value]))

    @jsii.member(jsii_name="putSurrogateType")
    def put_surrogate_type(self) -> None:
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType()

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
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryOutputReference, jsii.get(self, "dictionary"))

    @builtins.property
    @jsii.member(jsii_name="infoType")
    def info_type(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeOutputReference, jsii.get(self, "infoType"))

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegexOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegexOutputReference", jsii.get(self, "regex"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScore")
    def sensitivity_score(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScoreOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="storedType")
    def stored_type(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredTypeOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredTypeOutputReference", jsii.get(self, "storedType"))

    @builtins.property
    @jsii.member(jsii_name="surrogateType")
    def surrogate_type(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateTypeOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateTypeOutputReference", jsii.get(self, "surrogateType"))

    @builtins.property
    @jsii.member(jsii_name="dictionaryInput")
    def dictionary_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary], jsii.get(self, "dictionaryInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionTypeInput")
    def exclusion_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exclusionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="infoTypeInput")
    def info_type_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType], jsii.get(self, "infoTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="likelihoodInput")
    def likelihood_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "likelihoodInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex"], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="storedTypeInput")
    def stored_type_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType"], jsii.get(self, "storedTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="surrogateTypeInput")
    def surrogate_type_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType"], jsii.get(self, "surrogateTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionType")
    def exclusion_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exclusionType"))

    @exclusion_type.setter
    def exclusion_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5cb670ef029902ed608d2fa03ae01ae32bb8d98a3909498ec39cd527bdb38ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="likelihood")
    def likelihood(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "likelihood"))

    @likelihood.setter
    def likelihood(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0adf72dff6d5d30786ecb1b578d1099b92ef1000e886b78de6f8c83a75c103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "likelihood", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a6d6df607a8a564bc085a32d53bde72a7c8081bdaaf121a702ccb154c80f772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern", "group_indexes": "groupIndexes"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex:
    def __init__(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#pattern GoogleDataLossPreventionJobTrigger#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#group_indexes GoogleDataLossPreventionJobTrigger#group_indexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4964fdf1370a6d1e22f8d5dcd8622d9da0cf1311964f87f146383443a815d114)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#pattern GoogleDataLossPreventionJobTrigger#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_indexes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The index of the submatch to extract as findings.

        When not specified, the entire match is returned. No more than 3 may be included.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#group_indexes GoogleDataLossPreventionJobTrigger#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22026c8d19acbb3b767d2134206b499dc1ad0c51d54d9a24244c877f96221b91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdc93ca880d997dff5e997f04087509604f1bb958809988b75f13db9429f1eeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3c548c62836780e4c08fb379ba14bac7aa3730f409844f33974bb67d4e8aeea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f9917222b629d14c977284782d66fb1d57dae59cc710c6780b66b7675260a64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c3a847d99626980199e7537fc68b6d3980843a2b5f32ac10931b9bd810e095)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab24b9829185deae8a514f8a5bc8fb31efbe4750fee758afb5b8201779c0c610)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3a5a68411ecb8de0b3b2569919c77fc7de34c15f4779d007704feb64f7ffc52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2977baec7865b90fbb6f13e175f536c571d6f65c620d14df4f035bbfc8d81037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Resource name of the requested StoredInfoType, for example 'organizations/433245324/storedInfoTypes/432452342' or 'projects/project-id/storedInfoTypes/432452342'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8d37205d89e8de66cc7881511652042a1a5c4365929bfe9a76beb0d65cf8cf6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Resource name of the requested StoredInfoType, for example 'organizations/433245324/storedInfoTypes/432452342' or 'projects/project-id/storedInfoTypes/432452342'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fae8c1657d30536b8b2c2b135a36a302027d30707d3a309ee1429401ffdef5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27b6f7da650ef8bbc78bf225e292015b0f4192db537932b86964d0d640d5c6d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b90b337821e95ca8b062f6a046732ab5d28850f89c01468ee3ea0e4b87da803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3afd49ad4a0ecd451bdcb89fb5b8f7caffd4d000cc834cff8b4b8467b72fdc31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__499a197c5871a6dd0573a67db56c4c82bbe7a67cecaffc14c772315af11cba50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sensitivity_score GoogleDataLossPreventionJobTrigger#sensitivity_score}
        :param version: Version of the information type to use. By default, the version is set to stable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#version GoogleDataLossPreventionJobTrigger#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e1ebbfbb49954ef5500e53c66a8db21680154645fca4543c0db59657c02d058)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sensitivity_score GoogleDataLossPreventionJobTrigger#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the information type to use. By default, the version is set to stable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#version GoogleDataLossPreventionJobTrigger#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23154a6fb471bdd931d29a34af1bd702f938bd5f62eb3db14c493143ba5a46d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4197adcbabb63fbcdf917ba3b132ee9de332320b7392c4057681fae6f1056761)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa6c756cacc7eb3c5390119d635cc198ab71a02648f9d4b5f6c7ec0041ba80f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a6c50124d561c012ea9f86d9253b9161808688515ddf8a2267ef8e6f6707e7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c534e09c3672b9ce14ff1bd6b4efc170bcf87547eba098eab4e132f40936fffe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13761a8520934654d56ab5a3526b5b5f5daa4820cf4888849ad57fb065eee319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3bf3ee4bc169e987897be59d015537c5a557b36e1e76ae38cfbd3aadab54e32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore(
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
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScoreOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0e1a2361c33ead6c954223de32b9cb83d148cc17b3e58f9da54d14a226a4540c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e86022ec517a3fae79b31e52d253c81b4a16380b6b5c9cb34b909b235f08a53d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3712c3808f8aa43690f083f3d52dc6ec49522a19277537711147454c7f9d53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01d7607d8179b1dbd1d1d74fee56118705dde1be5556ca877f8b6ce2029a5550)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9529386dea07fa900bdd3f5b7fb6195a3be9f27ea76f130f7073ddabd9fa5a34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4829bab90cb3a336ca284b623aaef43c2eaa5115762ba9b6fb3742555f11005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b893ef29a5e3f7c282e9082e168d4f4c02915ac164a9cd20defc69d83fda9f8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimits",
    jsii_struct_bases=[],
    name_mapping={
        "max_findings_per_info_type": "maxFindingsPerInfoType",
        "max_findings_per_item": "maxFindingsPerItem",
        "max_findings_per_request": "maxFindingsPerRequest",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimits:
    def __init__(
        self,
        *,
        max_findings_per_info_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_findings_per_item: typing.Optional[jsii.Number] = None,
        max_findings_per_request: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_findings_per_info_type: max_findings_per_info_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#max_findings_per_info_type GoogleDataLossPreventionJobTrigger#max_findings_per_info_type}
        :param max_findings_per_item: Max number of findings that will be returned for each item scanned. The maximum returned is 2000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#max_findings_per_item GoogleDataLossPreventionJobTrigger#max_findings_per_item}
        :param max_findings_per_request: Max number of findings that will be returned per request/job. The maximum returned is 2000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#max_findings_per_request GoogleDataLossPreventionJobTrigger#max_findings_per_request}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ffae029fdb9de696bce206500724fc5a810cac41c9f992acf429a1e130b3b7)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType"]]]:
        '''max_findings_per_info_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#max_findings_per_info_type GoogleDataLossPreventionJobTrigger#max_findings_per_info_type}
        '''
        result = self._values.get("max_findings_per_info_type")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType"]]], result)

    @builtins.property
    def max_findings_per_item(self) -> typing.Optional[jsii.Number]:
        '''Max number of findings that will be returned for each item scanned. The maximum returned is 2000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#max_findings_per_item GoogleDataLossPreventionJobTrigger#max_findings_per_item}
        '''
        result = self._values.get("max_findings_per_item")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_findings_per_request(self) -> typing.Optional[jsii.Number]:
        '''Max number of findings that will be returned per request/job. The maximum returned is 2000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#max_findings_per_request GoogleDataLossPreventionJobTrigger#max_findings_per_request}
        '''
        result = self._values.get("max_findings_per_request")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType",
    jsii_struct_bases=[],
    name_mapping={"info_type": "infoType", "max_findings": "maxFindings"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType:
    def __init__(
        self,
        *,
        info_type: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType", typing.Dict[builtins.str, typing.Any]]] = None,
        max_findings: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param info_type: info_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#info_type GoogleDataLossPreventionJobTrigger#info_type}
        :param max_findings: Max findings limit for the given infoType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#max_findings GoogleDataLossPreventionJobTrigger#max_findings}
        '''
        if isinstance(info_type, dict):
            info_type = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType(**info_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eefc04c355f947c448edb715f2e5fc531f71275045bd484812af48fc22300660)
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
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType"]:
        '''info_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#info_type GoogleDataLossPreventionJobTrigger#info_type}
        '''
        result = self._values.get("info_type")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType"], result)

    @builtins.property
    def max_findings(self) -> typing.Optional[jsii.Number]:
        '''Max findings limit for the given infoType.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#max_findings GoogleDataLossPreventionJobTrigger#max_findings}
        '''
        result = self._values.get("max_findings")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sensitivity_score GoogleDataLossPreventionJobTrigger#sensitivity_score}
        :param version: Version of the information type to use. By default, the version is set to stable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#version GoogleDataLossPreventionJobTrigger#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091e8eca23409f375e61ade7f1f00479ab1eae072d1b396d2e1317cd2672381a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sensitivity_score GoogleDataLossPreventionJobTrigger#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the information type to use. By default, the version is set to stable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#version GoogleDataLossPreventionJobTrigger#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__096a3490080093a390492c118b5d8b4b8a86874a2db86e9241673632c2d41b8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore(
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
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f2addfa0a7c5d69e4dc521a8d1d0a996d67dc641841db7fe66bc811f61cd0197)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__366c8db6f93402f466af67e8758d2f4cf2e6eddf6d9e2606e9abc6c94b0df396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e188aa2ca0f08529981251551a0e53d054b135f65f2dd86976550d509c2a0d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23dddf5b614d05e767534833c9340448260b2fee1b3936fb644e7fbd94356553)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5c6f35ba4e410277147da99099697e44f1c95e12039e916cc8ee5b1dc933b88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51ff21b3e22e77487980a1053f9d4853a768d7f60020485518a9d3de08e0029a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53345a826dba3534a0b5150838cc05bacadf535c9eb28374bfa06f46b6ee3a63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58b51ab7da38277749d3bfdd7bf5c116c6fcac2b79fb2ed2030a46814a13ea82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3df94cf1f14e5b10a5457b21971bae052c1fbc435733c224f29cf7c5737de91d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69d832b369f700ab47d8bb7dba4ba0bc109dc528911eae1e9ed30eb39d96695c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c635662b18047fbe476632ebc525e7becacba9e4e057ed1930f9ee1215f8ab5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__128194204a05940b27133307bb6811a3e7bb1e9b22a2e8fc5686ec7964d17a15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb9124218867891000f66098927a24563cc63d8a674a4001872af42d41c28bec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34ff59fb6c53b26c41be28bede0af21373ab78487affa7941d3c7a98ee5fa6dd)
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
        sensitivity_score: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sensitivity_score GoogleDataLossPreventionJobTrigger#sensitivity_score}
        :param version: Version of the information type to use. By default, the version is set to stable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#version GoogleDataLossPreventionJobTrigger#version}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType(
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
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference, jsii.get(self, "infoType"))

    @builtins.property
    @jsii.member(jsii_name="infoTypeInput")
    def info_type_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType], jsii.get(self, "infoTypeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8fecf0706607ca6813259cc61053d9b2df5934170b34875200bc3c100c041ef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFindings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76c29917ddbb4b9fec9f0000be7bd4bd1dfc53a3c26d13185f956adcc80a411d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__471cac9e5d98241121847d66e0b446865aa399211f6a4a1930652239c6518a6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMaxFindingsPerInfoType")
    def put_max_findings_per_info_type(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9798056f2dda6f8701a6686c21ee740ff2df733323d0713710a251e65656fa)
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
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeList:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeList, jsii.get(self, "maxFindingsPerInfoType"))

    @builtins.property
    @jsii.member(jsii_name="maxFindingsPerInfoTypeInput")
    def max_findings_per_info_type_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]]], jsii.get(self, "maxFindingsPerInfoTypeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1725cfb08028c67c315dd267e93732c2185e6f6e60f50cd5a38caf7cbf4c94d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFindingsPerItem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxFindingsPerRequest")
    def max_findings_per_request(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxFindingsPerRequest"))

    @max_findings_per_request.setter
    def max_findings_per_request(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6a3df3ce0a51c057fce0e922eb1f88d796a2d6c06b5c7e8bdc567f708746029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFindingsPerRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimits]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimits],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21ba451aa989d1a7fb9c921d5798fa93bd88631db0f14e32ce24d3e9d3a70ee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ad61d057c9b66853cca51a7304d9945e1ccd1c12841370c81f4a8b62e40b084)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomInfoTypes")
    def put_custom_info_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81c0b445f65da7118d14edd72e742fb285eb2e08567c9caa8dce0f86fe7bd3b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomInfoTypes", [value]))

    @jsii.member(jsii_name="putInfoTypes")
    def put_info_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7a79d049641f09612b66b881a7a86b9bc17c0d8b42b2ab7b549f416844f6ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInfoTypes", [value]))

    @jsii.member(jsii_name="putLimits")
    def put_limits(
        self,
        *,
        max_findings_per_info_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType, typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_findings_per_item: typing.Optional[jsii.Number] = None,
        max_findings_per_request: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_findings_per_info_type: max_findings_per_info_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#max_findings_per_info_type GoogleDataLossPreventionJobTrigger#max_findings_per_info_type}
        :param max_findings_per_item: Max number of findings that will be returned for each item scanned. The maximum returned is 2000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#max_findings_per_item GoogleDataLossPreventionJobTrigger#max_findings_per_item}
        :param max_findings_per_request: Max number of findings that will be returned per request/job. The maximum returned is 2000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#max_findings_per_request GoogleDataLossPreventionJobTrigger#max_findings_per_request}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimits(
            max_findings_per_info_type=max_findings_per_info_type,
            max_findings_per_item=max_findings_per_item,
            max_findings_per_request=max_findings_per_request,
        )

        return typing.cast(None, jsii.invoke(self, "putLimits", [value]))

    @jsii.member(jsii_name="putRuleSet")
    def put_rule_set(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c11e331c054a39168d2b594ecfa1f4d4fb6f220f1bc085b8cfd28dab10d9af2)
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
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesList:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesList, jsii.get(self, "customInfoTypes"))

    @builtins.property
    @jsii.member(jsii_name="infoTypes")
    def info_types(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesList:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesList, jsii.get(self, "infoTypes"))

    @builtins.property
    @jsii.member(jsii_name="limits")
    def limits(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsOutputReference, jsii.get(self, "limits"))

    @builtins.property
    @jsii.member(jsii_name="ruleSet")
    def rule_set(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetList":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetList", jsii.get(self, "ruleSet"))

    @builtins.property
    @jsii.member(jsii_name="customInfoTypesInput")
    def custom_info_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]]], jsii.get(self, "customInfoTypesInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]]], jsii.get(self, "infoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="limitsInput")
    def limits_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimits]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimits], jsii.get(self, "limitsInput"))

    @builtins.property
    @jsii.member(jsii_name="minLikelihoodInput")
    def min_likelihood_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minLikelihoodInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleSetInput")
    def rule_set_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet"]]], jsii.get(self, "ruleSetInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__66928169db5bb5f8787ba3456557689b3d4a22a5c5ed92eb6b4cad5c1f1b2b3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25409de0d362f8e118178d5c7afdb15e3cf379059fb9d1f6d909b04f51c6d6e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeQuote", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minLikelihood")
    def min_likelihood(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minLikelihood"))

    @min_likelihood.setter
    def min_likelihood(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__440586cdedd6d8c6499bc491d7d792b87ac00d5b160a87063416ba514b79508a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minLikelihood", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfig]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc8747fb394ba24e990e86a038ceeef3da7d1b35af5e3f0fa31cf197d890dd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet",
    jsii_struct_bases=[],
    name_mapping={"rules": "rules", "info_types": "infoTypes"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet:
    def __init__(
        self,
        *,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules", typing.Dict[builtins.str, typing.Any]]]],
        info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#rules GoogleDataLossPreventionJobTrigger#rules}
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#info_types GoogleDataLossPreventionJobTrigger#info_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7638c52e7d01924ac7eb417913988fcdaa4e1e72aa84f07b50638410c65fd638)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules"]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#rules GoogleDataLossPreventionJobTrigger#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules"]], result)

    @builtins.property
    def info_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes"]]]:
        '''info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#info_types GoogleDataLossPreventionJobTrigger#info_types}
        '''
        result = self._values.get("info_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sensitivity_score GoogleDataLossPreventionJobTrigger#sensitivity_score}
        :param version: Version of the information type to use. By default, the version is set to stable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#version GoogleDataLossPreventionJobTrigger#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85465450888bf4bc679d9fce63ef72ed4848203c446f7c8067b32e4a7d69f895)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sensitivity_score GoogleDataLossPreventionJobTrigger#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the information type to use. By default, the version is set to stable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#version GoogleDataLossPreventionJobTrigger#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3566b07e7c382e0ff6491a5aa0be5ac08697cb11127ed69759492370ec1a41e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c84ee18a33627e4b5866cda32efe336e8adff1c4076d529e0226ae4bc040fad)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6c56348a73d455b62f0873d0eba9cf456099e177ec556cce96af9a47c9d08b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b91a3ef3bf36036776aa03ba22b650262dd5e07612a370331db135e4de7c82b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__613b01162a5d58b6e51c631642c5e0162b23054b1d4a0ee9fbcf74d64db664ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ca2db557e9db7c110ced3f263f7c788cacaa002e6f72634a8891b35d2f75b4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6735ce94439377273df5169a850f192ad0ef1712606a99e9605c9aa326321be6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore(
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
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__332eec36e41d93c7ddb98f51201bc4734461cbb2b5e870e0a203eaa5e2423129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d7767976196b0a850e3191c816f0e66cff2b2b3d15975afbd12c13b284c0828)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76b04c97f4e371ae0425a0f991626707984d8b532444ff40993f030b99e0936d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__469c8c3c2f3a4a7e1dbfebda2714e6c3b3d56a4c26649a3e3cfde03710357785)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98640df5bc21e4b14748e07a0720239e7d233cdf7b7a82b4e5669a1740528af7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bce9a8906611784e618941b33b308bf664303b408c8cbefcd16c0546eee25009)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b9bf667690a439561750c56fad43a045413d2cd705bf1a71e244ec93407984b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__999a443f72f6f78329ac38742ad986a3093db4397cbf0d605936e592287eeaee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09cca8a323299372edd610b4ec06e25b158fdc5d5caef34c35ce6a8ba3fe5dd3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e0e9fc5074156bcb6aaee3f2ce3132849be977a0384a7c4a02cfa48feee567)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ccda8601e6c731c787d251da6bd1a4f55633f9ccf6b0a2d96d8d34b51caba1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75263b11a668d6f685b05e213855322a9b1bf2e5c17e2e70fa78ee807f69eea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__925b3314719e350f72dcb6d9cba489505311b803a4d0921db287d96e927a6576)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90b3e96227f04f1ad3603d3256a8ca3a17fd55e911fae6ed287c9163d553d413)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInfoTypes")
    def put_info_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70746082ef91c2b8d0e4821a8b29016311185a7e467322fd94275d2aa7028d48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInfoTypes", [value]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__896f22e518572b4c1a058692529cf5693e26718992f9c803b2c643fca497d93f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="resetInfoTypes")
    def reset_info_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfoTypes", []))

    @builtins.property
    @jsii.member(jsii_name="infoTypes")
    def info_types(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesList:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesList, jsii.get(self, "infoTypes"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesList":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="infoTypesInput")
    def info_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]]], jsii.get(self, "infoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c66e48cdc326cb3361163306bfd05d6f9a9d7309fd97b56cdfc8c3acda189a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules",
    jsii_struct_bases=[],
    name_mapping={"exclusion_rule": "exclusionRule", "hotword_rule": "hotwordRule"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules:
    def __init__(
        self,
        *,
        exclusion_rule: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule", typing.Dict[builtins.str, typing.Any]]] = None,
        hotword_rule: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param exclusion_rule: exclusion_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#exclusion_rule GoogleDataLossPreventionJobTrigger#exclusion_rule}
        :param hotword_rule: hotword_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#hotword_rule GoogleDataLossPreventionJobTrigger#hotword_rule}
        '''
        if isinstance(exclusion_rule, dict):
            exclusion_rule = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule(**exclusion_rule)
        if isinstance(hotword_rule, dict):
            hotword_rule = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule(**hotword_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6725b58213bf49d365ed36e02a5b9009deebedcaf08a609f525c5156005e7615)
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
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule"]:
        '''exclusion_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#exclusion_rule GoogleDataLossPreventionJobTrigger#exclusion_rule}
        '''
        result = self._values.get("exclusion_rule")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule"], result)

    @builtins.property
    def hotword_rule(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule"]:
        '''hotword_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#hotword_rule GoogleDataLossPreventionJobTrigger#hotword_rule}
        '''
        result = self._values.get("hotword_rule")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule",
    jsii_struct_bases=[],
    name_mapping={
        "matching_type": "matchingType",
        "dictionary": "dictionary",
        "exclude_by_hotword": "excludeByHotword",
        "exclude_info_types": "excludeInfoTypes",
        "regex": "regex",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule:
    def __init__(
        self,
        *,
        matching_type: builtins.str,
        dictionary: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_by_hotword: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_info_types: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes", typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param matching_type: How the rule is applied. See the documentation for more information: https://cloud.google.com/dlp/docs/reference/rest/v2/InspectConfig#MatchingType Possible values: ["MATCHING_TYPE_FULL_MATCH", "MATCHING_TYPE_PARTIAL_MATCH", "MATCHING_TYPE_INVERSE_MATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#matching_type GoogleDataLossPreventionJobTrigger#matching_type}
        :param dictionary: dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#dictionary GoogleDataLossPreventionJobTrigger#dictionary}
        :param exclude_by_hotword: exclude_by_hotword block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#exclude_by_hotword GoogleDataLossPreventionJobTrigger#exclude_by_hotword}
        :param exclude_info_types: exclude_info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#exclude_info_types GoogleDataLossPreventionJobTrigger#exclude_info_types}
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#regex GoogleDataLossPreventionJobTrigger#regex}
        '''
        if isinstance(dictionary, dict):
            dictionary = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary(**dictionary)
        if isinstance(exclude_by_hotword, dict):
            exclude_by_hotword = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword(**exclude_by_hotword)
        if isinstance(exclude_info_types, dict):
            exclude_info_types = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes(**exclude_info_types)
        if isinstance(regex, dict):
            regex = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex(**regex)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a75158e985165bd2fd3fdde328f5f08d8ca50c9ee732d609c6f8534382ba5252)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#matching_type GoogleDataLossPreventionJobTrigger#matching_type}
        '''
        result = self._values.get("matching_type")
        assert result is not None, "Required property 'matching_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dictionary(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary"]:
        '''dictionary block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#dictionary GoogleDataLossPreventionJobTrigger#dictionary}
        '''
        result = self._values.get("dictionary")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary"], result)

    @builtins.property
    def exclude_by_hotword(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword"]:
        '''exclude_by_hotword block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#exclude_by_hotword GoogleDataLossPreventionJobTrigger#exclude_by_hotword}
        '''
        result = self._values.get("exclude_by_hotword")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword"], result)

    @builtins.property
    def exclude_info_types(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes"]:
        '''exclude_info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#exclude_info_types GoogleDataLossPreventionJobTrigger#exclude_info_types}
        '''
        result = self._values.get("exclude_info_types")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes"], result)

    @builtins.property
    def regex(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex"]:
        '''regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#regex GoogleDataLossPreventionJobTrigger#regex}
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary",
    jsii_struct_bases=[],
    name_mapping={"cloud_storage_path": "cloudStoragePath", "word_list": "wordList"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary:
    def __init__(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath", typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#cloud_storage_path GoogleDataLossPreventionJobTrigger#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#word_list GoogleDataLossPreventionJobTrigger#word_list}
        '''
        if isinstance(cloud_storage_path, dict):
            cloud_storage_path = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath(**cloud_storage_path)
        if isinstance(word_list, dict):
            word_list = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct(**word_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e62f351a252eb37b734141b5556c2f2512c116c40e9d6410570a7ab87baad6d)
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
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath"]:
        '''cloud_storage_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#cloud_storage_path GoogleDataLossPreventionJobTrigger#cloud_storage_path}
        '''
        result = self._values.get("cloud_storage_path")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath"], result)

    @builtins.property
    def word_list(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct"]:
        '''word_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#word_list GoogleDataLossPreventionJobTrigger#word_list}
        '''
        result = self._values.get("word_list")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath:
    def __init__(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#path GoogleDataLossPreventionJobTrigger#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__931be6566e9fecbc9b61dd59cb8c31463df85bac1eb7e402a1b2f57c30361e0f)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#path GoogleDataLossPreventionJobTrigger#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4791981ad76deb6d436e1299eb1b18a3dcb133fc49285d0b7a6629f4f44ddcdc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f002317b8aa9630230e054122ef5f3b94ab150501892dcd7ed44728b91368d43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7552d7701facfe61fe4ad8180a514412f33a1bd4dbf1f68790e2db58dfea0464)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__676806e75714ccf21ba6480357a6cc509e1e1ed8cd22934603fb00becefc3b1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudStoragePath")
    def put_cloud_storage_path(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#path GoogleDataLossPreventionJobTrigger#path}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath(
            path=path
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStoragePath", [value]))

    @jsii.member(jsii_name="putWordList")
    def put_word_list(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#words GoogleDataLossPreventionJobTrigger#words}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct(
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
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference, jsii.get(self, "cloudStoragePath"))

    @builtins.property
    @jsii.member(jsii_name="wordList")
    def word_list(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference", jsii.get(self, "wordList"))

    @builtins.property
    @jsii.member(jsii_name="cloudStoragePathInput")
    def cloud_storage_path_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath], jsii.get(self, "cloudStoragePathInput"))

    @builtins.property
    @jsii.member(jsii_name="wordListInput")
    def word_list_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct"], jsii.get(self, "wordListInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__081dc39efbd1ecc5734a4f61259a7d108d9119bfc608e76224c153e72ee3fac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct",
    jsii_struct_bases=[],
    name_mapping={"words": "words"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct:
    def __init__(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#words GoogleDataLossPreventionJobTrigger#words}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8604e2c6c8c64504b42c60286e8d1075d1ac0d7131d898d9756130983489bf9e)
            check_type(argname="argument words", value=words, expected_type=type_hints["words"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "words": words,
        }

    @builtins.property
    def words(self) -> typing.List[builtins.str]:
        '''Words or phrases defining the dictionary.

        The dictionary must contain at least one
        phrase and every phrase must contain at least 2 characters that are letters or digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#words GoogleDataLossPreventionJobTrigger#words}
        '''
        result = self._values.get("words")
        assert result is not None, "Required property 'words' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8706d3fa4a203b4d33a962671b9a1749fedf26804360f4c2ff25e807070d1fe9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__392c8917072026caa1e5b37779562058be28064d538e59684d61053d30098844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "words", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b34c0ccd05cf20d67a3fc854cde02afa033561e7c78e285cb74a70ed66ed8c64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword",
    jsii_struct_bases=[],
    name_mapping={"hotword_regex": "hotwordRegex", "proximity": "proximity"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword:
    def __init__(
        self,
        *,
        hotword_regex: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex", typing.Dict[builtins.str, typing.Any]]] = None,
        proximity: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hotword_regex: hotword_regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#hotword_regex GoogleDataLossPreventionJobTrigger#hotword_regex}
        :param proximity: proximity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#proximity GoogleDataLossPreventionJobTrigger#proximity}
        '''
        if isinstance(hotword_regex, dict):
            hotword_regex = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex(**hotword_regex)
        if isinstance(proximity, dict):
            proximity = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity(**proximity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2962b30b1b6bab0871fa7bda1bbb98d2232d30087d90d9dd7cac0da5e37d7a52)
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
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex"]:
        '''hotword_regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#hotword_regex GoogleDataLossPreventionJobTrigger#hotword_regex}
        '''
        result = self._values.get("hotword_regex")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex"], result)

    @builtins.property
    def proximity(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity"]:
        '''proximity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#proximity GoogleDataLossPreventionJobTrigger#proximity}
        '''
        result = self._values.get("proximity")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex",
    jsii_struct_bases=[],
    name_mapping={"group_indexes": "groupIndexes", "pattern": "pattern"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex:
    def __init__(
        self,
        *,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        pattern: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#group_indexes GoogleDataLossPreventionJobTrigger#group_indexes}
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#pattern GoogleDataLossPreventionJobTrigger#pattern}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c2a56dbc54e63b48afc84e5516401db1538ae5daa6e8570e9b60e45ec807983)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#group_indexes GoogleDataLossPreventionJobTrigger#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#pattern GoogleDataLossPreventionJobTrigger#pattern}
        '''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c05ebcdbb555dde2c6cd977e5b3e7104be01940692ea282704b3218f152bbdcc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e7583b8cfeb629f903a4a3d7904f4aaf69ce299aac4d0d7b2491182a38997d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afd8d1179b6f61240b9c8d38044c6ceffcdb7ca2d22d5ca60e1bd7a9485862e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9333a131364be44d98333bf657c15d3d9ff80945f0fb8c4d6b09b74b33a2d3e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b4a1cebd3b7a4f06c8d812a823d80466d06358aa69e6dfc09063fd6d7ac6ace)
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
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#group_indexes GoogleDataLossPreventionJobTrigger#group_indexes}
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#pattern GoogleDataLossPreventionJobTrigger#pattern}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex(
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
        :param window_after: Number of characters after the finding to consider. Either this or window_before must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#window_after GoogleDataLossPreventionJobTrigger#window_after}
        :param window_before: Number of characters before the finding to consider. Either this or window_after must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#window_before GoogleDataLossPreventionJobTrigger#window_before}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity(
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
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference, jsii.get(self, "hotwordRegex"))

    @builtins.property
    @jsii.member(jsii_name="proximity")
    def proximity(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference", jsii.get(self, "proximity"))

    @builtins.property
    @jsii.member(jsii_name="hotwordRegexInput")
    def hotword_regex_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex], jsii.get(self, "hotwordRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="proximityInput")
    def proximity_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity"], jsii.get(self, "proximityInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8af9b82755242707549ac0892dc8f689f05cb54e7758c0e9116b6f9bc433b92e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity",
    jsii_struct_bases=[],
    name_mapping={"window_after": "windowAfter", "window_before": "windowBefore"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity:
    def __init__(
        self,
        *,
        window_after: typing.Optional[jsii.Number] = None,
        window_before: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param window_after: Number of characters after the finding to consider. Either this or window_before must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#window_after GoogleDataLossPreventionJobTrigger#window_after}
        :param window_before: Number of characters before the finding to consider. Either this or window_after must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#window_before GoogleDataLossPreventionJobTrigger#window_before}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d02869c1a28666c72742662b34d10fd00f01f088db2c9f430c7df8c1957a700)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#window_after GoogleDataLossPreventionJobTrigger#window_after}
        '''
        result = self._values.get("window_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def window_before(self) -> typing.Optional[jsii.Number]:
        '''Number of characters before the finding to consider. Either this or window_after must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#window_before GoogleDataLossPreventionJobTrigger#window_before}
        '''
        result = self._values.get("window_before")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f626432a20d5c69ac8422e8203c4f8028e2c73388eb494344f8bea796e0281fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__396ca02cb1e9afa7451858960b678e98ce2b5595ae7b9048b21bd3a987f7ea5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="windowBefore")
    def window_before(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "windowBefore"))

    @window_before.setter
    def window_before(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be92b79b5f127dc95513250f3ab39faed114f73f578d137d6b08fd42269101ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4d5a4bb56ab6614dad16b80538400e1d6a974c28c22f98ec70c1d2759f92fdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes",
    jsii_struct_bases=[],
    name_mapping={"info_types": "infoTypes"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes:
    def __init__(
        self,
        *,
        info_types: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#info_types GoogleDataLossPreventionJobTrigger#info_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a5173b1bba4727483b2d683cfef482a7d71806d1680969c83e8109b8827745)
            check_type(argname="argument info_types", value=info_types, expected_type=type_hints["info_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "info_types": info_types,
        }

    @builtins.property
    def info_types(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes"]]:
        '''info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#info_types GoogleDataLossPreventionJobTrigger#info_types}
        '''
        result = self._values.get("info_types")
        assert result is not None, "Required property 'info_types' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sensitivity_score GoogleDataLossPreventionJobTrigger#sensitivity_score}
        :param version: Version of the information type to use. By default, the version is set to stable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#version GoogleDataLossPreventionJobTrigger#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68a1f2ee54e6d04e1b1a716953824c6cd414ea79d0d7878005d4efaab540e36a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sensitivity_score GoogleDataLossPreventionJobTrigger#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the information type to use. By default, the version is set to stable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#version GoogleDataLossPreventionJobTrigger#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97e6f9d61edd74d9326bc37aafb510a8a00c1c93749b3c56652ead019ed695ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b7125367df2d0e0d5983a82aa09f325d19ed6526a1b3f81878fdf8273b3444)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe76fa06271b034cdfd72b6840af1cbb76f3368372f2cd2e2c7313c86b9e8f24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ad77a321212d778f3d8513d27e53b6c16e62804d73f68b877eb4f13bf06380e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6796eb6c59d4e84793e67f237eee3324a642453a478fe6b4134313039f0905bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a60dac2ca1ee53f45162532b4518283a90f7b908841dcc86474029b24aa8dea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e61b45bd3d7f79c3a331ba917225c9b90b22b57a4ed09cfd9e6e00580ca529f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore(
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
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0fff9d79416610dd6ceaaa0b848fa62c3d5adbfef720eccb470258e49cc2c368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b83cb72aaf963142a49037eec9a9a603d4e03fa912f09234d533004b8a638137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__170a27656b79025c6cfd93575b4287fdac3adda0927bbe95a5a6ad514034f370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0804591c7ff7e8f1cd1f13fda025d8bd2518ff614f2f339bbbd13300a8c290d6)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#score GoogleDataLossPreventionJobTrigger#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5aae5b7d4b4f2b1ab7845739e77104a75945fd1b993fc61085f9be56f76462ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e1456cca1c60b0bb337c914f42a1b3a34cd55e6baaeec1d95e902d585285a23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28284f71ca0650548bf8f676bc181122cc541ef03d0d677f69077dbc12e89de9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__535c21717fd34af59a5fc72ca918382135438d7f4d369000eae89c143dac3a38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInfoTypes")
    def put_info_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77791eb3ba4579da8dc5cafadf874c1311d2ade1628272bdd34472213c001b11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInfoTypes", [value]))

    @builtins.property
    @jsii.member(jsii_name="infoTypes")
    def info_types(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList, jsii.get(self, "infoTypes"))

    @builtins.property
    @jsii.member(jsii_name="infoTypesInput")
    def info_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]], jsii.get(self, "infoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb7be1924c9871a4e8c82ea44243cb992f41df607f48c8d44b5b672082d1346e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c63e8aa00d8fdc73db983ae30adc20376c2d254ff190235763b2f4b00f1d278c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDictionary")
    def put_dictionary(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#cloud_storage_path GoogleDataLossPreventionJobTrigger#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#word_list GoogleDataLossPreventionJobTrigger#word_list}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary(
            cloud_storage_path=cloud_storage_path, word_list=word_list
        )

        return typing.cast(None, jsii.invoke(self, "putDictionary", [value]))

    @jsii.member(jsii_name="putExcludeByHotword")
    def put_exclude_by_hotword(
        self,
        *,
        hotword_regex: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex, typing.Dict[builtins.str, typing.Any]]] = None,
        proximity: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hotword_regex: hotword_regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#hotword_regex GoogleDataLossPreventionJobTrigger#hotword_regex}
        :param proximity: proximity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#proximity GoogleDataLossPreventionJobTrigger#proximity}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword(
            hotword_regex=hotword_regex, proximity=proximity
        )

        return typing.cast(None, jsii.invoke(self, "putExcludeByHotword", [value]))

    @jsii.member(jsii_name="putExcludeInfoTypes")
    def put_exclude_info_types(
        self,
        *,
        info_types: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#info_types GoogleDataLossPreventionJobTrigger#info_types}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes(
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
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#pattern GoogleDataLossPreventionJobTrigger#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#group_indexes GoogleDataLossPreventionJobTrigger#group_indexes}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex(
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
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference, jsii.get(self, "dictionary"))

    @builtins.property
    @jsii.member(jsii_name="excludeByHotword")
    def exclude_by_hotword(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference, jsii.get(self, "excludeByHotword"))

    @builtins.property
    @jsii.member(jsii_name="excludeInfoTypes")
    def exclude_info_types(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference, jsii.get(self, "excludeInfoTypes"))

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegexOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegexOutputReference", jsii.get(self, "regex"))

    @builtins.property
    @jsii.member(jsii_name="dictionaryInput")
    def dictionary_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary], jsii.get(self, "dictionaryInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeByHotwordInput")
    def exclude_by_hotword_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword], jsii.get(self, "excludeByHotwordInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeInfoTypesInput")
    def exclude_info_types_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes], jsii.get(self, "excludeInfoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="matchingTypeInput")
    def matching_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchingTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex"], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="matchingType")
    def matching_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchingType"))

    @matching_type.setter
    def matching_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f4771ec7f6072ddde846d0ae810fc025c4d06327e3a97dc837cf6f2c5ca2f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchingType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f65da8203f7639d2b29ff57d23c1f5026bd0b68d14cddf07baa7327949540052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern", "group_indexes": "groupIndexes"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex:
    def __init__(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#pattern GoogleDataLossPreventionJobTrigger#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#group_indexes GoogleDataLossPreventionJobTrigger#group_indexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bb57de68e2ad3db654f7dbc966781dc7251e300c8ba4a40311e4dac33d998b6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#pattern GoogleDataLossPreventionJobTrigger#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_indexes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The index of the submatch to extract as findings.

        When not specified, the entire match is returned. No more than 3 may be included.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#group_indexes GoogleDataLossPreventionJobTrigger#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__498a1d1785cc2a6d78ea7ca8bd2cf2cbdaaade3452c003fe09375cd2918592f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8368cfbf736b478e0a2cb067a99c3c69a22230a4218091e209e65235ab24e6c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af17fc2dea06b3a91adcc89342838514249dcefc673a327040f5f22fd68c3c1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10111870dc8a948690f35f5690e962e9344db43cb3536b380a188f8460234830)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule",
    jsii_struct_bases=[],
    name_mapping={
        "hotword_regex": "hotwordRegex",
        "likelihood_adjustment": "likelihoodAdjustment",
        "proximity": "proximity",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule:
    def __init__(
        self,
        *,
        hotword_regex: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex", typing.Dict[builtins.str, typing.Any]]] = None,
        likelihood_adjustment: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment", typing.Dict[builtins.str, typing.Any]]] = None,
        proximity: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hotword_regex: hotword_regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#hotword_regex GoogleDataLossPreventionJobTrigger#hotword_regex}
        :param likelihood_adjustment: likelihood_adjustment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#likelihood_adjustment GoogleDataLossPreventionJobTrigger#likelihood_adjustment}
        :param proximity: proximity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#proximity GoogleDataLossPreventionJobTrigger#proximity}
        '''
        if isinstance(hotword_regex, dict):
            hotword_regex = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex(**hotword_regex)
        if isinstance(likelihood_adjustment, dict):
            likelihood_adjustment = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment(**likelihood_adjustment)
        if isinstance(proximity, dict):
            proximity = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity(**proximity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e619b75c548bb66e023626966d883c9ca7d041188a97724c5d0d0d1a1cda7b6)
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
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex"]:
        '''hotword_regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#hotword_regex GoogleDataLossPreventionJobTrigger#hotword_regex}
        '''
        result = self._values.get("hotword_regex")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex"], result)

    @builtins.property
    def likelihood_adjustment(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment"]:
        '''likelihood_adjustment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#likelihood_adjustment GoogleDataLossPreventionJobTrigger#likelihood_adjustment}
        '''
        result = self._values.get("likelihood_adjustment")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment"], result)

    @builtins.property
    def proximity(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity"]:
        '''proximity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#proximity GoogleDataLossPreventionJobTrigger#proximity}
        '''
        result = self._values.get("proximity")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex",
    jsii_struct_bases=[],
    name_mapping={"group_indexes": "groupIndexes", "pattern": "pattern"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex:
    def __init__(
        self,
        *,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        pattern: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#group_indexes GoogleDataLossPreventionJobTrigger#group_indexes}
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#pattern GoogleDataLossPreventionJobTrigger#pattern}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b46fa44d34a4e30df2cf58648f85f29be76ce4883f6d3f4a4d652441108bb1e2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#group_indexes GoogleDataLossPreventionJobTrigger#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#pattern GoogleDataLossPreventionJobTrigger#pattern}
        '''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d03ee8d3a7521f55577765744783fd6f1ecca6261614c9777bb8715870b89e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55c30ef204d09fa79f8d170360d90acf78027462df500994955f93cb1006315a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb2e8ece6015d1e307b969171bceb1d6eab3756a416caed555d25ad92edcb5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fae6b729be36ec1a78fc4a37aa77339413b29cd9248022097feb5aed936a797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment",
    jsii_struct_bases=[],
    name_mapping={
        "fixed_likelihood": "fixedLikelihood",
        "relative_likelihood": "relativeLikelihood",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment:
    def __init__(
        self,
        *,
        fixed_likelihood: typing.Optional[builtins.str] = None,
        relative_likelihood: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed_likelihood: Set the likelihood of a finding to a fixed value. Either this or relative_likelihood can be set. Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#fixed_likelihood GoogleDataLossPreventionJobTrigger#fixed_likelihood}
        :param relative_likelihood: Increase or decrease the likelihood by the specified number of levels. For example, if a finding would be POSSIBLE without the detection rule and relativeLikelihood is 1, then it is upgraded to LIKELY, while a value of -1 would downgrade it to UNLIKELY. Likelihood may never drop below VERY_UNLIKELY or exceed VERY_LIKELY, so applying an adjustment of 1 followed by an adjustment of -1 when base likelihood is VERY_LIKELY will result in a final likelihood of LIKELY. Either this or fixed_likelihood can be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#relative_likelihood GoogleDataLossPreventionJobTrigger#relative_likelihood}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95ac14dc727f40dd9d4d4e2a6757c3c03559e87ad473ba0056382663e7a7db69)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#fixed_likelihood GoogleDataLossPreventionJobTrigger#fixed_likelihood}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#relative_likelihood GoogleDataLossPreventionJobTrigger#relative_likelihood}
        '''
        result = self._values.get("relative_likelihood")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad691574efa31c927e428f210487d37c0f8c509b87bc19ee5cf8f7546fee76c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__597a0987b62c37de0f768be6dde8f15cf8e71f856d81c7b2d1eca65539300a55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedLikelihood", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="relativeLikelihood")
    def relative_likelihood(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "relativeLikelihood"))

    @relative_likelihood.setter
    def relative_likelihood(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692a2deb00f95377f48c0bb3f04f0d2968c89b8d86415a528fd3614a0aa930fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relativeLikelihood", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0c5a9cd7b73de9d969e3d8e1b1c296da11f58fd4b1659f376d632eaaec032a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ba70d3112e22da0e08b2cb6338d864bba72a878d49668e4d31810111796b461)
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
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#group_indexes GoogleDataLossPreventionJobTrigger#group_indexes}
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#pattern GoogleDataLossPreventionJobTrigger#pattern}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex(
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
        :param fixed_likelihood: Set the likelihood of a finding to a fixed value. Either this or relative_likelihood can be set. Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#fixed_likelihood GoogleDataLossPreventionJobTrigger#fixed_likelihood}
        :param relative_likelihood: Increase or decrease the likelihood by the specified number of levels. For example, if a finding would be POSSIBLE without the detection rule and relativeLikelihood is 1, then it is upgraded to LIKELY, while a value of -1 would downgrade it to UNLIKELY. Likelihood may never drop below VERY_UNLIKELY or exceed VERY_LIKELY, so applying an adjustment of 1 followed by an adjustment of -1 when base likelihood is VERY_LIKELY will result in a final likelihood of LIKELY. Either this or fixed_likelihood can be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#relative_likelihood GoogleDataLossPreventionJobTrigger#relative_likelihood}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment(
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
        :param window_after: Number of characters after the finding to consider. Either this or window_before must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#window_after GoogleDataLossPreventionJobTrigger#window_after}
        :param window_before: Number of characters before the finding to consider. Either this or window_after must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#window_before GoogleDataLossPreventionJobTrigger#window_before}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity(
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
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference, jsii.get(self, "hotwordRegex"))

    @builtins.property
    @jsii.member(jsii_name="likelihoodAdjustment")
    def likelihood_adjustment(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference, jsii.get(self, "likelihoodAdjustment"))

    @builtins.property
    @jsii.member(jsii_name="proximity")
    def proximity(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximityOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximityOutputReference", jsii.get(self, "proximity"))

    @builtins.property
    @jsii.member(jsii_name="hotwordRegexInput")
    def hotword_regex_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex], jsii.get(self, "hotwordRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="likelihoodAdjustmentInput")
    def likelihood_adjustment_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment], jsii.get(self, "likelihoodAdjustmentInput"))

    @builtins.property
    @jsii.member(jsii_name="proximityInput")
    def proximity_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity"], jsii.get(self, "proximityInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14c4f7ba756c81d8c93f3cc46f681b7618b17739aa6c1d6bf8f3e89c72491aaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity",
    jsii_struct_bases=[],
    name_mapping={"window_after": "windowAfter", "window_before": "windowBefore"},
)
class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity:
    def __init__(
        self,
        *,
        window_after: typing.Optional[jsii.Number] = None,
        window_before: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param window_after: Number of characters after the finding to consider. Either this or window_before must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#window_after GoogleDataLossPreventionJobTrigger#window_after}
        :param window_before: Number of characters before the finding to consider. Either this or window_after must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#window_before GoogleDataLossPreventionJobTrigger#window_before}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee00b9aebd89ee94a1474901048dbc45d1559620e7cc3e9f7ddd1e2a749facaa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#window_after GoogleDataLossPreventionJobTrigger#window_after}
        '''
        result = self._values.get("window_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def window_before(self) -> typing.Optional[jsii.Number]:
        '''Number of characters before the finding to consider. Either this or window_after must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#window_before GoogleDataLossPreventionJobTrigger#window_before}
        '''
        result = self._values.get("window_before")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51f94fe0204fb1daaea9f739b6316985667d9a9a86a5dc753121ec4bf95a37ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9ff2278441528f3653d946e1e9c96785e2ae27a212cc5e323e20bfacd292bfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="windowBefore")
    def window_before(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "windowBefore"))

    @window_before.setter
    def window_before(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fa4b97752c64ccc6d3c75afefd03c0b7e41affd03f715064e325dacfd787b53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d208369008187bb4f2c8ab402c6787023cc42408d601677fbb145ad274fee8e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dc64b295e2923156c7b9243bacfed4e2a3660df2ee54521eac67500f2266c79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c8f9fb7b01427acec49a4a96e9221eb4baf16911a581e848ff6a240c46fff9e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1418cfe19633fed4993226990403244c42647bece845c34bbb3a1408c59ccfd8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__797ec9b3297e638a875a2b6b7d78e13d1af7dd6c13c10a843497de27c61a90c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67bcde11d3ff2ab94b6c1f6f4984eeff5e612afdcf68803331d399409bcd4d3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7afdb7e292f20910fcd201d9dc2eb8ed0906a75486b71b75cd501f6d4c16d7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1de59faaacb781d637e4d73d74cb39891530e0df3dbf8aa00e867dbe02a527d2)
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
        dictionary: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_by_hotword: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword, typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_info_types: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes, typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param matching_type: How the rule is applied. See the documentation for more information: https://cloud.google.com/dlp/docs/reference/rest/v2/InspectConfig#MatchingType Possible values: ["MATCHING_TYPE_FULL_MATCH", "MATCHING_TYPE_PARTIAL_MATCH", "MATCHING_TYPE_INVERSE_MATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#matching_type GoogleDataLossPreventionJobTrigger#matching_type}
        :param dictionary: dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#dictionary GoogleDataLossPreventionJobTrigger#dictionary}
        :param exclude_by_hotword: exclude_by_hotword block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#exclude_by_hotword GoogleDataLossPreventionJobTrigger#exclude_by_hotword}
        :param exclude_info_types: exclude_info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#exclude_info_types GoogleDataLossPreventionJobTrigger#exclude_info_types}
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#regex GoogleDataLossPreventionJobTrigger#regex}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule(
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
        hotword_regex: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex, typing.Dict[builtins.str, typing.Any]]] = None,
        likelihood_adjustment: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment, typing.Dict[builtins.str, typing.Any]]] = None,
        proximity: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hotword_regex: hotword_regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#hotword_regex GoogleDataLossPreventionJobTrigger#hotword_regex}
        :param likelihood_adjustment: likelihood_adjustment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#likelihood_adjustment GoogleDataLossPreventionJobTrigger#likelihood_adjustment}
        :param proximity: proximity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#proximity GoogleDataLossPreventionJobTrigger#proximity}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule(
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
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleOutputReference, jsii.get(self, "exclusionRule"))

    @builtins.property
    @jsii.member(jsii_name="hotwordRule")
    def hotword_rule(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleOutputReference, jsii.get(self, "hotwordRule"))

    @builtins.property
    @jsii.member(jsii_name="exclusionRuleInput")
    def exclusion_rule_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule], jsii.get(self, "exclusionRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="hotwordRuleInput")
    def hotword_rule_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule], jsii.get(self, "hotwordRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0087fa97d4e398da1f6897294b3647c4055e0c4f6313135055fbc5bb1bd52e61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cad2701fbf31fd40d603a71601e1c5aa7850d18835bcc47b7c0c4b63683fa9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9e35eb8942f23d8ed4a312ebb111d2422a8e579c93e09bdf81499fd7b406f31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putInspectConfig")
    def put_inspect_config(
        self,
        *,
        custom_info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
        exclude_info_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_quote: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
        limits: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimits, typing.Dict[builtins.str, typing.Any]]] = None,
        min_likelihood: typing.Optional[builtins.str] = None,
        rule_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param custom_info_types: custom_info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#custom_info_types GoogleDataLossPreventionJobTrigger#custom_info_types}
        :param exclude_info_types: When true, excludes type information of the findings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#exclude_info_types GoogleDataLossPreventionJobTrigger#exclude_info_types}
        :param include_quote: When true, a contextual quote from the data that triggered a finding is included in the response. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#include_quote GoogleDataLossPreventionJobTrigger#include_quote}
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#info_types GoogleDataLossPreventionJobTrigger#info_types}
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#limits GoogleDataLossPreventionJobTrigger#limits}
        :param min_likelihood: Only returns findings equal or above this threshold. See https://cloud.google.com/dlp/docs/likelihood for more info Default value: "POSSIBLE" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#min_likelihood GoogleDataLossPreventionJobTrigger#min_likelihood}
        :param rule_set: rule_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#rule_set GoogleDataLossPreventionJobTrigger#rule_set}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobInspectConfig(
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
        big_query_options: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_storage_options: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        datastore_options: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        hybrid_options: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timespan_config: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param big_query_options: big_query_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#big_query_options GoogleDataLossPreventionJobTrigger#big_query_options}
        :param cloud_storage_options: cloud_storage_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#cloud_storage_options GoogleDataLossPreventionJobTrigger#cloud_storage_options}
        :param datastore_options: datastore_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#datastore_options GoogleDataLossPreventionJobTrigger#datastore_options}
        :param hybrid_options: hybrid_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#hybrid_options GoogleDataLossPreventionJobTrigger#hybrid_options}
        :param timespan_config: timespan_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#timespan_config GoogleDataLossPreventionJobTrigger#timespan_config}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobStorageConfig(
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
    def actions(self) -> GoogleDataLossPreventionJobTriggerInspectJobActionsList:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobActionsList, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="inspectConfig")
    def inspect_config(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobInspectConfigOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobInspectConfigOutputReference, jsii.get(self, "inspectConfig"))

    @builtins.property
    @jsii.member(jsii_name="storageConfig")
    def storage_config(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobStorageConfigOutputReference", jsii.get(self, "storageConfig"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobActions]]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="inspectConfigInput")
    def inspect_config_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfig]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfig], jsii.get(self, "inspectConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="inspectTemplateNameInput")
    def inspect_template_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inspectTemplateNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageConfigInput")
    def storage_config_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfig"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfig"], jsii.get(self, "storageConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="inspectTemplateName")
    def inspect_template_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inspectTemplateName"))

    @inspect_template_name.setter
    def inspect_template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca2ccdff2b660c95c1767469594f616cd41abc70530bab3071929b0939ff037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspectTemplateName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJob]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfdd83e0c3fc087e01e8d74b9bab7830f9fdb30e5d3cd4994e3ebb584700b261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfig",
    jsii_struct_bases=[],
    name_mapping={
        "big_query_options": "bigQueryOptions",
        "cloud_storage_options": "cloudStorageOptions",
        "datastore_options": "datastoreOptions",
        "hybrid_options": "hybridOptions",
        "timespan_config": "timespanConfig",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobStorageConfig:
    def __init__(
        self,
        *,
        big_query_options: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_storage_options: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        datastore_options: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        hybrid_options: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timespan_config: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param big_query_options: big_query_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#big_query_options GoogleDataLossPreventionJobTrigger#big_query_options}
        :param cloud_storage_options: cloud_storage_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#cloud_storage_options GoogleDataLossPreventionJobTrigger#cloud_storage_options}
        :param datastore_options: datastore_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#datastore_options GoogleDataLossPreventionJobTrigger#datastore_options}
        :param hybrid_options: hybrid_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#hybrid_options GoogleDataLossPreventionJobTrigger#hybrid_options}
        :param timespan_config: timespan_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#timespan_config GoogleDataLossPreventionJobTrigger#timespan_config}
        '''
        if isinstance(big_query_options, dict):
            big_query_options = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions(**big_query_options)
        if isinstance(cloud_storage_options, dict):
            cloud_storage_options = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions(**cloud_storage_options)
        if isinstance(datastore_options, dict):
            datastore_options = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions(**datastore_options)
        if isinstance(hybrid_options, dict):
            hybrid_options = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions(**hybrid_options)
        if isinstance(timespan_config, dict):
            timespan_config = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig(**timespan_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__470cc6c8770a59ea47874d7524831f8907158a8c09276bea5107c098d0b29df4)
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
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions"]:
        '''big_query_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#big_query_options GoogleDataLossPreventionJobTrigger#big_query_options}
        '''
        result = self._values.get("big_query_options")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions"], result)

    @builtins.property
    def cloud_storage_options(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions"]:
        '''cloud_storage_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#cloud_storage_options GoogleDataLossPreventionJobTrigger#cloud_storage_options}
        '''
        result = self._values.get("cloud_storage_options")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions"], result)

    @builtins.property
    def datastore_options(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions"]:
        '''datastore_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#datastore_options GoogleDataLossPreventionJobTrigger#datastore_options}
        '''
        result = self._values.get("datastore_options")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions"], result)

    @builtins.property
    def hybrid_options(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions"]:
        '''hybrid_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#hybrid_options GoogleDataLossPreventionJobTrigger#hybrid_options}
        '''
        result = self._values.get("hybrid_options")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions"], result)

    @builtins.property
    def timespan_config(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig"]:
        '''timespan_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#timespan_config GoogleDataLossPreventionJobTrigger#timespan_config}
        '''
        result = self._values.get("timespan_config")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobStorageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions",
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
class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions:
    def __init__(
        self,
        *,
        table_reference: typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference", typing.Dict[builtins.str, typing.Any]],
        excluded_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        identifying_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        included_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rows_limit: typing.Optional[jsii.Number] = None,
        rows_limit_percent: typing.Optional[jsii.Number] = None,
        sample_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table_reference: table_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table_reference GoogleDataLossPreventionJobTrigger#table_reference}
        :param excluded_fields: excluded_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#excluded_fields GoogleDataLossPreventionJobTrigger#excluded_fields}
        :param identifying_fields: identifying_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#identifying_fields GoogleDataLossPreventionJobTrigger#identifying_fields}
        :param included_fields: included_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#included_fields GoogleDataLossPreventionJobTrigger#included_fields}
        :param rows_limit: Max number of rows to scan. If the table has more rows than this value, the rest of the rows are omitted. If not set, or if set to 0, all rows will be scanned. Only one of rowsLimit and rowsLimitPercent can be specified. Cannot be used in conjunction with TimespanConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#rows_limit GoogleDataLossPreventionJobTrigger#rows_limit}
        :param rows_limit_percent: Max percentage of rows to scan. The rest are omitted. The number of rows scanned is rounded down. Must be between 0 and 100, inclusively. Both 0 and 100 means no limit. Defaults to 0. Only one of rowsLimit and rowsLimitPercent can be specified. Cannot be used in conjunction with TimespanConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#rows_limit_percent GoogleDataLossPreventionJobTrigger#rows_limit_percent}
        :param sample_method: How to sample rows if not all rows are scanned. Meaningful only when used in conjunction with either rowsLimit or rowsLimitPercent. If not specified, rows are scanned in the order BigQuery reads them. If TimespanConfig is set, set this to an empty string to avoid using the default value. Default value: "TOP" Possible values: ["TOP", "RANDOM_START"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sample_method GoogleDataLossPreventionJobTrigger#sample_method}
        '''
        if isinstance(table_reference, dict):
            table_reference = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference(**table_reference)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b8106c2022e7767c786de413eb10f7ae98775626901c5a3ab4abe84bd6488cb)
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
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference":
        '''table_reference block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table_reference GoogleDataLossPreventionJobTrigger#table_reference}
        '''
        result = self._values.get("table_reference")
        assert result is not None, "Required property 'table_reference' is missing"
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference", result)

    @builtins.property
    def excluded_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields"]]]:
        '''excluded_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#excluded_fields GoogleDataLossPreventionJobTrigger#excluded_fields}
        '''
        result = self._values.get("excluded_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields"]]], result)

    @builtins.property
    def identifying_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields"]]]:
        '''identifying_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#identifying_fields GoogleDataLossPreventionJobTrigger#identifying_fields}
        '''
        result = self._values.get("identifying_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields"]]], result)

    @builtins.property
    def included_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields"]]]:
        '''included_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#included_fields GoogleDataLossPreventionJobTrigger#included_fields}
        '''
        result = self._values.get("included_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields"]]], result)

    @builtins.property
    def rows_limit(self) -> typing.Optional[jsii.Number]:
        '''Max number of rows to scan.

        If the table has more rows than this value, the rest of the rows are omitted.
        If not set, or if set to 0, all rows will be scanned. Only one of rowsLimit and rowsLimitPercent can be
        specified. Cannot be used in conjunction with TimespanConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#rows_limit GoogleDataLossPreventionJobTrigger#rows_limit}
        '''
        result = self._values.get("rows_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rows_limit_percent(self) -> typing.Optional[jsii.Number]:
        '''Max percentage of rows to scan.

        The rest are omitted. The number of rows scanned is rounded down.
        Must be between 0 and 100, inclusively. Both 0 and 100 means no limit. Defaults to 0. Only one of
        rowsLimit and rowsLimitPercent can be specified. Cannot be used in conjunction with TimespanConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#rows_limit_percent GoogleDataLossPreventionJobTrigger#rows_limit_percent}
        '''
        result = self._values.get("rows_limit_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sample_method(self) -> typing.Optional[builtins.str]:
        '''How to sample rows if not all rows are scanned.

        Meaningful only when used in conjunction with either
        rowsLimit or rowsLimitPercent. If not specified, rows are scanned in the order BigQuery reads them.
        If TimespanConfig is set, set this to an empty string to avoid using the default value. Default value: "TOP" Possible values: ["TOP", "RANDOM_START"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sample_method GoogleDataLossPreventionJobTrigger#sample_method}
        '''
        result = self._values.get("sample_method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Name describing the field excluded from scanning. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbb22f32d62129a89a5d269ae6f2ce7b0c7e7cb73cec86a070134f6a7e812fe4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name describing the field excluded from scanning.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27981fb74bbcf128a1402b995dec577a0a08e73e76a4d409b9367a787bebd319)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbd74072c6536bd2cbe941aa7411a74ad5a91fe62a472f2467b52693a3edaae5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84f94f208062228dbd569304cfeb67753c07559f5b7a306b49aebcd4a01b1047)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab08003d416380c32947440a36f3c406174154410b8e8e829cd5917299b1df24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__449a5555a5ad3ff267428bf86bb5861d71da9b53fca94ca5c632daf9ab02c082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4d1df472d1899ca0db2339070c82337a0fd1300be9f02a34ccff29f471e0be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b770f36ca276b14866888dac5322f0152fac761845cb7bbc0543c2c28be4fc8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__402b210c56c696dadf8f6c6daa6fc3c7289c46f339cdc27c3db7d6441c4b590f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cdbda8402d058ed5376d4edd08b8405afc5b42e96da5b4ef02387997e03499f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Name of a BigQuery field to be returned with the findings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21351654aa52b6443e77e414f4f30f18cc73f83ffc52feb39a323d6eff6f3218)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of a BigQuery field to be returned with the findings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b83089fc7680eefa070b295da85ce347b0a80b2d2d0d66fe742b4b6edf70038)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__315e17f5e6e8bda8d572a60e0c449188c9ec969b230e3f378ab7e7392455c425)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c4993381a4ba3bc442c94ea2298ca9ade1a129060478794e26aa35f52a39099)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c0881b0f04df352908d9a6cd17ad59509592f24f3a0a07a77b4daf190eb8fb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40b8931c40e5f27a6e044e80799815bc82948d2b68c5473d2eb812a15640f9ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bdee3cfe73de716f466664c224193c53fa392b2769e59c1a7dc121de58ae99a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d685559bc6c9df65eb76286a150ea003eb6773b000ce7098bd00dc0869f686b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5e34c2bed9e0122e84dd53506d25df4f10344ee4b6dcce33c4ca85c48f6fa92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b507af889b59f9795286dbca7b45891e4f871c9bbd38502372998ade54f3b486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Name describing the field to which scanning is limited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6409be3b177f27e8aba4ebec6e6d16ac8ad0051bd999f85391429132a53daeea)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name describing the field to which scanning is limited.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64e04f6ee4394cab58da2357cd230880bc075dd0f4c2f15d672a8378584c9e40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6ae79b6035c9c034ee0bf4bb34517f84c18436d4c9605ae41fc3fc2b9402804)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ad3ad00c1722a94c2b5d150e669c2ae69e01e5a5f401925d522fedd4a531d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21e29b5450520e9c93abe51bd507fdb9f84bd01a08e35aedc9b0ba2ad2672539)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc292cb33ba59afc5c34c32d1a7b0eb61adee99a708f97663cf6e25d0ac282fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6649c0a9eee067637ed34b8fa923c75dcbb5dc9ade68a5fec86261138e3671fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd5042ee42c04032e012542143c486ff238a86e44a1f48a5cc1e3b86617f73e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bfd7cd72ff0a8c0a3d197b06747ea34693210f54207251ac494dd4baf7cbe92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24caeb2015323c7ec0c86bed60c4d915e94efc46628d61fb55505f9f7488b243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a9f8a81e90a8be6807dac86aa0133dd7e302e20974c9945a892065221f13da5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExcludedFields")
    def put_excluded_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb8a0b982076dd6ccd13b574b9f163baad1b2ac3867a71f86892dd1573ae0025)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExcludedFields", [value]))

    @jsii.member(jsii_name="putIdentifyingFields")
    def put_identifying_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__846601a8b82b30774216e44b2c92555cf0e70719ab55009435cf7f66a11d3b8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIdentifyingFields", [value]))

    @jsii.member(jsii_name="putIncludedFields")
    def put_included_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f2b8d5a46be85f004c96cb161e338fbce818acc47de3988238214923fea406)
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
        :param dataset_id: The dataset ID of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#dataset_id GoogleDataLossPreventionJobTrigger#dataset_id}
        :param project_id: The Google Cloud Platform project ID of the project containing the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#project_id GoogleDataLossPreventionJobTrigger#project_id}
        :param table_id: The name of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table_id GoogleDataLossPreventionJobTrigger#table_id}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference(
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
    ) -> GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsList:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsList, jsii.get(self, "excludedFields"))

    @builtins.property
    @jsii.member(jsii_name="identifyingFields")
    def identifying_fields(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsList:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsList, jsii.get(self, "identifyingFields"))

    @builtins.property
    @jsii.member(jsii_name="includedFields")
    def included_fields(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsList:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsList, jsii.get(self, "includedFields"))

    @builtins.property
    @jsii.member(jsii_name="tableReference")
    def table_reference(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReferenceOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReferenceOutputReference", jsii.get(self, "tableReference"))

    @builtins.property
    @jsii.member(jsii_name="excludedFieldsInput")
    def excluded_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]]], jsii.get(self, "excludedFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="identifyingFieldsInput")
    def identifying_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]]], jsii.get(self, "identifyingFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedFieldsInput")
    def included_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]]], jsii.get(self, "includedFieldsInput"))

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
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference"], jsii.get(self, "tableReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="rowsLimit")
    def rows_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rowsLimit"))

    @rows_limit.setter
    def rows_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f9a74f63452d66fa169c13d48c1d148d56f299ca72becc27bfa74e003f7997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowsLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rowsLimitPercent")
    def rows_limit_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rowsLimitPercent"))

    @rows_limit_percent.setter
    def rows_limit_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__638ab826ec221a30183f15ea7a93b6b2c0954c6aaf9e34371b5efb54e7e0ff31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowsLimitPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleMethod")
    def sample_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sampleMethod"))

    @sample_method.setter
    def sample_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae2d214021a015e12903693b0024b7598ec3285936c77bfbc919e04fec7a545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64309101dd0816e55471bc342d94dab5c889be4ab5a6cd831b801c4f633dfc25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id": "datasetId",
        "project_id": "projectId",
        "table_id": "tableId",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference:
    def __init__(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The dataset ID of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#dataset_id GoogleDataLossPreventionJobTrigger#dataset_id}
        :param project_id: The Google Cloud Platform project ID of the project containing the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#project_id GoogleDataLossPreventionJobTrigger#project_id}
        :param table_id: The name of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table_id GoogleDataLossPreventionJobTrigger#table_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c570b011b1902eb4439e906ad7c4e7405213ed752661ce8e191b0c2b2f9cdb84)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#dataset_id GoogleDataLossPreventionJobTrigger#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The Google Cloud Platform project ID of the project containing the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#project_id GoogleDataLossPreventionJobTrigger#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_id(self) -> builtins.str:
        '''The name of the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table_id GoogleDataLossPreventionJobTrigger#table_id}
        '''
        result = self._values.get("table_id")
        assert result is not None, "Required property 'table_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e58f5085c6ec7ab98460345a4c26d6b07d990c2b0274f99840caf7746bcb823)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8df201893ff971d20c66010e932b24e8996f55564ae5910e27201550aa455c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90a0118fbbab94dda57c4129b3648ace1cd737df5c5ba10d237c8d264d9c6de1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__193303ff80d001e7b840306982962241d4ba1e3b01e25d659ab651fcaa3e166d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5237a92fd8cb9a7ca01b3f05f7a27d7f48ce923e7358bfc3aee8e99bddb0c596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions",
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
class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions:
    def __init__(
        self,
        *,
        file_set: typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet", typing.Dict[builtins.str, typing.Any]],
        bytes_limit_per_file: typing.Optional[jsii.Number] = None,
        bytes_limit_per_file_percent: typing.Optional[jsii.Number] = None,
        files_limit_percent: typing.Optional[jsii.Number] = None,
        file_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        sample_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_set: file_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#file_set GoogleDataLossPreventionJobTrigger#file_set}
        :param bytes_limit_per_file: Max number of bytes to scan from a file. If a scanned file's size is bigger than this value then the rest of the bytes are omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#bytes_limit_per_file GoogleDataLossPreventionJobTrigger#bytes_limit_per_file}
        :param bytes_limit_per_file_percent: Max percentage of bytes to scan from a file. The rest are omitted. The number of bytes scanned is rounded down. Must be between 0 and 100, inclusively. Both 0 and 100 means no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#bytes_limit_per_file_percent GoogleDataLossPreventionJobTrigger#bytes_limit_per_file_percent}
        :param files_limit_percent: Limits the number of files to scan to this percentage of the input FileSet. Number of files scanned is rounded down. Must be between 0 and 100, inclusively. Both 0 and 100 means no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#files_limit_percent GoogleDataLossPreventionJobTrigger#files_limit_percent}
        :param file_types: List of file type groups to include in the scan. If empty, all files are scanned and available data format processors are applied. In addition, the binary content of the selected files is always scanned as well. Images are scanned only as binary if the specified region does not support image inspection and no fileTypes were specified. Possible values: ["BINARY_FILE", "TEXT_FILE", "IMAGE", "WORD", "PDF", "AVRO", "CSV", "TSV", "POWERPOINT", "EXCEL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#file_types GoogleDataLossPreventionJobTrigger#file_types}
        :param sample_method: How to sample bytes if not all bytes are scanned. Meaningful only when used in conjunction with bytesLimitPerFile. If not specified, scanning would start from the top. Possible values: ["TOP", "RANDOM_START"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sample_method GoogleDataLossPreventionJobTrigger#sample_method}
        '''
        if isinstance(file_set, dict):
            file_set = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet(**file_set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__011773d25ad301e98af04c879d6c51700237ae264b51dedc7fe8d7dc589a3966)
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
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet":
        '''file_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#file_set GoogleDataLossPreventionJobTrigger#file_set}
        '''
        result = self._values.get("file_set")
        assert result is not None, "Required property 'file_set' is missing"
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet", result)

    @builtins.property
    def bytes_limit_per_file(self) -> typing.Optional[jsii.Number]:
        '''Max number of bytes to scan from a file.

        If a scanned file's size is bigger than this value
        then the rest of the bytes are omitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#bytes_limit_per_file GoogleDataLossPreventionJobTrigger#bytes_limit_per_file}
        '''
        result = self._values.get("bytes_limit_per_file")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bytes_limit_per_file_percent(self) -> typing.Optional[jsii.Number]:
        '''Max percentage of bytes to scan from a file.

        The rest are omitted. The number of bytes scanned is rounded down.
        Must be between 0 and 100, inclusively. Both 0 and 100 means no limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#bytes_limit_per_file_percent GoogleDataLossPreventionJobTrigger#bytes_limit_per_file_percent}
        '''
        result = self._values.get("bytes_limit_per_file_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def files_limit_percent(self) -> typing.Optional[jsii.Number]:
        '''Limits the number of files to scan to this percentage of the input FileSet.

        Number of files scanned is rounded down.
        Must be between 0 and 100, inclusively. Both 0 and 100 means no limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#files_limit_percent GoogleDataLossPreventionJobTrigger#files_limit_percent}
        '''
        result = self._values.get("files_limit_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def file_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of file type groups to include in the scan.

        If empty, all files are scanned and available data
        format processors are applied. In addition, the binary content of the selected files is always scanned as well.
        Images are scanned only as binary if the specified region does not support image inspection and no fileTypes were specified. Possible values: ["BINARY_FILE", "TEXT_FILE", "IMAGE", "WORD", "PDF", "AVRO", "CSV", "TSV", "POWERPOINT", "EXCEL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#file_types GoogleDataLossPreventionJobTrigger#file_types}
        '''
        result = self._values.get("file_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sample_method(self) -> typing.Optional[builtins.str]:
        '''How to sample bytes if not all bytes are scanned.

        Meaningful only when used in conjunction with bytesLimitPerFile.
        If not specified, scanning would start from the top. Possible values: ["TOP", "RANDOM_START"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sample_method GoogleDataLossPreventionJobTrigger#sample_method}
        '''
        result = self._values.get("sample_method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet",
    jsii_struct_bases=[],
    name_mapping={"regex_file_set": "regexFileSet", "url": "url"},
)
class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet:
    def __init__(
        self,
        *,
        regex_file_set: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet", typing.Dict[builtins.str, typing.Any]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param regex_file_set: regex_file_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#regex_file_set GoogleDataLossPreventionJobTrigger#regex_file_set}
        :param url: The Cloud Storage url of the file(s) to scan, in the format 'gs:///'. Trailing wildcard in the path is allowed. If the url ends in a trailing slash, the bucket or directory represented by the url will be scanned non-recursively (content in sub-directories will not be scanned). This means that 'gs://mybucket/' is equivalent to 'gs://mybucket/*', and 'gs://mybucket/directory/' is equivalent to 'gs://mybucket/directory/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#url GoogleDataLossPreventionJobTrigger#url}
        '''
        if isinstance(regex_file_set, dict):
            regex_file_set = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet(**regex_file_set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea613cbb1936411886dfcf181274f55ce8c9f414d97002627aa94cc06dbb831b)
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
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet"]:
        '''regex_file_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#regex_file_set GoogleDataLossPreventionJobTrigger#regex_file_set}
        '''
        result = self._values.get("regex_file_set")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet"], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage url of the file(s) to scan, in the format 'gs:///'. Trailing wildcard in the path is allowed.

        If the url ends in a trailing slash, the bucket or directory represented by the url will be scanned
        non-recursively (content in sub-directories will not be scanned). This means that 'gs://mybucket/' is
        equivalent to 'gs://mybucket/*', and 'gs://mybucket/directory/' is equivalent to 'gs://mybucket/directory/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#url GoogleDataLossPreventionJobTrigger#url}
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87ddf879abec18d153c9ecb1fe9ce8eab5597cef4a48369ac120174c705f78f3)
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
        :param bucket_name: The name of a Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#bucket_name GoogleDataLossPreventionJobTrigger#bucket_name}
        :param exclude_regex: A list of regular expressions matching file paths to exclude. All files in the bucket that match at least one of these regular expressions will be excluded from the scan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#exclude_regex GoogleDataLossPreventionJobTrigger#exclude_regex}
        :param include_regex: A list of regular expressions matching file paths to include. All files in the bucket that match at least one of these regular expressions will be included in the set of files, except for those that also match an item in excludeRegex. Leaving this field empty will match all files by default (this is equivalent to including .* in the list) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#include_regex GoogleDataLossPreventionJobTrigger#include_regex}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet(
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
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSetOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSetOutputReference", jsii.get(self, "regexFileSet"))

    @builtins.property
    @jsii.member(jsii_name="regexFileSetInput")
    def regex_file_set_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet"], jsii.get(self, "regexFileSetInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d479b80697bd65be485eaa94a87df63c8d987f4fc05a9d027b3d3bf51ed30de9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45d05c35a866a2acf54b439f9f9646749fe4d5aa3705c2acf19ee2f00659f9b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "exclude_regex": "excludeRegex",
        "include_regex": "includeRegex",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        exclude_regex: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_regex: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param bucket_name: The name of a Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#bucket_name GoogleDataLossPreventionJobTrigger#bucket_name}
        :param exclude_regex: A list of regular expressions matching file paths to exclude. All files in the bucket that match at least one of these regular expressions will be excluded from the scan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#exclude_regex GoogleDataLossPreventionJobTrigger#exclude_regex}
        :param include_regex: A list of regular expressions matching file paths to include. All files in the bucket that match at least one of these regular expressions will be included in the set of files, except for those that also match an item in excludeRegex. Leaving this field empty will match all files by default (this is equivalent to including .* in the list) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#include_regex GoogleDataLossPreventionJobTrigger#include_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7207511cb2fc3e4d5ce4cc7e99ed57c29d5809c273864229cf0ee09802f77504)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#bucket_name GoogleDataLossPreventionJobTrigger#bucket_name}
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exclude_regex(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of regular expressions matching file paths to exclude.

        All files in the bucket that match at
        least one of these regular expressions will be excluded from the scan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#exclude_regex GoogleDataLossPreventionJobTrigger#exclude_regex}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#include_regex GoogleDataLossPreventionJobTrigger#include_regex}
        '''
        result = self._values.get("include_regex")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__345a30286b67ba2eea9088818dd3f7fd8a2201041f8521aad4f9e4bb7682488f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe2896baaaa9434d58943169281dd2f3d0a498180a049d5c0e7d54687e689801)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeRegex")
    def exclude_regex(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeRegex"))

    @exclude_regex.setter
    def exclude_regex(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958329c24396a5beb84e54211f99ba3dece1b5a02b65e9077a47250d3069bb1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeRegex")
    def include_regex(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeRegex"))

    @include_regex.setter
    def include_regex(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ded93286b1c2e56f168c1b8c8fe43dc2b3b740eade8edd90839b0f932a3362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b13516bde22a41d741ebe4cebedc1106e8de7caa68b86c4e67eb353b96b3258f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__591f5a47569bed6356dc433ef62e62a1e0f75a5b71b81eb6cbe5538e8d1c66a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFileSet")
    def put_file_set(
        self,
        *,
        regex_file_set: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet, typing.Dict[builtins.str, typing.Any]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param regex_file_set: regex_file_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#regex_file_set GoogleDataLossPreventionJobTrigger#regex_file_set}
        :param url: The Cloud Storage url of the file(s) to scan, in the format 'gs:///'. Trailing wildcard in the path is allowed. If the url ends in a trailing slash, the bucket or directory represented by the url will be scanned non-recursively (content in sub-directories will not be scanned). This means that 'gs://mybucket/' is equivalent to 'gs://mybucket/*', and 'gs://mybucket/directory/' is equivalent to 'gs://mybucket/directory/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#url GoogleDataLossPreventionJobTrigger#url}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet(
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
    ) -> GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetOutputReference, jsii.get(self, "fileSet"))

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
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet], jsii.get(self, "fileSetInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__cc56f04e12c0ed1dd28b06f6afd7c91ef1b719a2cfe2eeed4be5f1185e91b771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bytesLimitPerFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bytesLimitPerFilePercent")
    def bytes_limit_per_file_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bytesLimitPerFilePercent"))

    @bytes_limit_per_file_percent.setter
    def bytes_limit_per_file_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03366031435dea843d2f884aa19f8870fd74fac93b7894060fc9cb1feed91f0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bytesLimitPerFilePercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filesLimitPercent")
    def files_limit_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "filesLimitPercent"))

    @files_limit_percent.setter
    def files_limit_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d768974c4528eaa132cdb50255114c3dbb1d7ca9e00e3680826608f2a6d4e322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filesLimitPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileTypes")
    def file_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileTypes"))

    @file_types.setter
    def file_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf33bd81bdbc32b739295c37076e7e38d3416290a6f4b587e10e39adbdbf57be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleMethod")
    def sample_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sampleMethod"))

    @sample_method.setter
    def sample_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a9194a8dcfd2410cf31efe23d560b0f9651b03a4419a61468ef109b1f4fdfd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8af5f8e50c60ff93f8166f46696cef9906c501f460f4a411f7381835c09b23fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions",
    jsii_struct_bases=[],
    name_mapping={"kind": "kind", "partition_id": "partitionId"},
)
class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions:
    def __init__(
        self,
        *,
        kind: typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind", typing.Dict[builtins.str, typing.Any]],
        partition_id: typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param kind: kind block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#kind GoogleDataLossPreventionJobTrigger#kind}
        :param partition_id: partition_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#partition_id GoogleDataLossPreventionJobTrigger#partition_id}
        '''
        if isinstance(kind, dict):
            kind = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind(**kind)
        if isinstance(partition_id, dict):
            partition_id = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId(**partition_id)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0df70fe325aff760dadf4c76a30ac090c7462360b26c4c80b6f44dde5a4c857)
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument partition_id", value=partition_id, expected_type=type_hints["partition_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kind": kind,
            "partition_id": partition_id,
        }

    @builtins.property
    def kind(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind":
        '''kind block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#kind GoogleDataLossPreventionJobTrigger#kind}
        '''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind", result)

    @builtins.property
    def partition_id(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId":
        '''partition_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#partition_id GoogleDataLossPreventionJobTrigger#partition_id}
        '''
        result = self._values.get("partition_id")
        assert result is not None, "Required property 'partition_id' is missing"
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: The name of the Datastore kind. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32de240167b5f71bbd1b18a6cbb8510724f89f459e18917e2cc38e0957ee08bf)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Datastore kind.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKindOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKindOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__845c2160bf04dfe18d77534cfa400dd3daec156b31b9618f32cde60272ea5954)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b179d4fd81a88df354c76c14d39c787b68c4550fa1280b569bb526c2a5d87b18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29ed8a35bb36910d10960af47fe6aad99d9255a2f1fe3af4407462a00b1d2d79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42ab23e9d6e4dddb911e54c5e09f94849dc648f9c0444b5f73ebee4c35722ef8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putKind")
    def put_kind(self, *, name: builtins.str) -> None:
        '''
        :param name: The name of the Datastore kind. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind(
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
        :param project_id: The ID of the project to which the entities belong. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#project_id GoogleDataLossPreventionJobTrigger#project_id}
        :param namespace_id: If not empty, the ID of the namespace to which the entities belong. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#namespace_id GoogleDataLossPreventionJobTrigger#namespace_id}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId(
            project_id=project_id, namespace_id=namespace_id
        )

        return typing.cast(None, jsii.invoke(self, "putPartitionId", [value]))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKindOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKindOutputReference, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="partitionId")
    def partition_id(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionIdOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionIdOutputReference", jsii.get(self, "partitionId"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionIdInput")
    def partition_id_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId"], jsii.get(self, "partitionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e62269aea7dbceb5e1e44854a12434f646ae59058bc8600c3a449018e411a47e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId",
    jsii_struct_bases=[],
    name_mapping={"project_id": "projectId", "namespace_id": "namespaceId"},
)
class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId:
    def __init__(
        self,
        *,
        project_id: builtins.str,
        namespace_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project_id: The ID of the project to which the entities belong. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#project_id GoogleDataLossPreventionJobTrigger#project_id}
        :param namespace_id: If not empty, the ID of the namespace to which the entities belong. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#namespace_id GoogleDataLossPreventionJobTrigger#namespace_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__090d678c444c13bbd535bfbc1aaac700cdf1e27e496597c0e54b3e76d67b7584)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#project_id GoogleDataLossPreventionJobTrigger#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace_id(self) -> typing.Optional[builtins.str]:
        '''If not empty, the ID of the namespace to which the entities belong.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#namespace_id GoogleDataLossPreventionJobTrigger#namespace_id}
        '''
        result = self._values.get("namespace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__573268f1e46ce0cac23683741f19a2abf8de99047216746ed926b5ee11c425b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45f711b7be9c381cfba7ae23ba26ceaf169c278108c8dcb5a7afa332bdfcbc0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ff58d99a84b803f63591572901f1cc2a050350388d92583d7d70f2357f3ee31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ab7a2001772d8134296ce8948e54e1ed14fb7ddcf0aa7bc98fab489e6f1136c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "labels": "labels",
        "required_finding_label_keys": "requiredFindingLabelKeys",
        "table_options": "tableOptions",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        required_finding_label_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        table_options: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param description: A short description of where the data is coming from. Will be stored once in the job. 256 max length. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#description GoogleDataLossPreventionJobTrigger#description}
        :param labels: To organize findings, these labels will be added to each finding. Label keys must be between 1 and 63 characters long and must conform to the following regular expression: '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?'. Label values must be between 0 and 63 characters long and must conform to the regular expression '(`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?)?'. No more than 10 labels can be associated with a given finding. Examples: - '"environment" : "production"' - '"pipeline" : "etl"' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#labels GoogleDataLossPreventionJobTrigger#labels}
        :param required_finding_label_keys: These are labels that each inspection request must include within their 'finding_labels' map. Request may contain others, but any missing one of these will be rejected. Label keys must be between 1 and 63 characters long and must conform to the following regular expression: '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?'. No more than 10 keys can be required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#required_finding_label_keys GoogleDataLossPreventionJobTrigger#required_finding_label_keys}
        :param table_options: table_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table_options GoogleDataLossPreventionJobTrigger#table_options}
        '''
        if isinstance(table_options, dict):
            table_options = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions(**table_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd16536e6c61a512035a752c6fd07368d9f740bb4c02f4eb1c398460f5949f3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#description GoogleDataLossPreventionJobTrigger#description}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#labels GoogleDataLossPreventionJobTrigger#labels}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#required_finding_label_keys GoogleDataLossPreventionJobTrigger#required_finding_label_keys}
        '''
        result = self._values.get("required_finding_label_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def table_options(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions"]:
        '''table_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table_options GoogleDataLossPreventionJobTrigger#table_options}
        '''
        result = self._values.get("table_options")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9e01619e6ad640e977e199af8f493dae2c695300a02fcdda60b884c9f8c5203)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTableOptions")
    def put_table_options(
        self,
        *,
        identifying_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identifying_fields: identifying_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#identifying_fields GoogleDataLossPreventionJobTrigger#identifying_fields}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions(
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
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsOutputReference", jsii.get(self, "tableOptions"))

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
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions"], jsii.get(self, "tableOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc285733762b34b7be58c8e60dd2c9f340d06e2df78c17224dbb1b242672fe35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bbbeb46fa0aae81dd74ba832702abd896353d621eaafea752a56e1f79382ef0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredFindingLabelKeys")
    def required_finding_label_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requiredFindingLabelKeys"))

    @required_finding_label_keys.setter
    def required_finding_label_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4159c5a1b2d0295cdd5261b7301d2825d889dff371291446cec1a983ec566358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredFindingLabelKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2030c079da9a3024190cc145647d908f355497ffea4ad34bfee6e302c6eb9b83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions",
    jsii_struct_bases=[],
    name_mapping={"identifying_fields": "identifyingFields"},
)
class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions:
    def __init__(
        self,
        *,
        identifying_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identifying_fields: identifying_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#identifying_fields GoogleDataLossPreventionJobTrigger#identifying_fields}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2a5e672cddf316de89115be0fc2ef02bfb695fb3e315d1768e26964079f8650)
            check_type(argname="argument identifying_fields", value=identifying_fields, expected_type=type_hints["identifying_fields"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identifying_fields is not None:
            self._values["identifying_fields"] = identifying_fields

    @builtins.property
    def identifying_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields"]]]:
        '''identifying_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#identifying_fields GoogleDataLossPreventionJobTrigger#identifying_fields}
        '''
        result = self._values.get("identifying_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Name describing the field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fb6837d2d4e231ffa58742e3252a19e4f9d4520685a2d811cd5bc9e733f9294)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name describing the field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d51658e892b15db6fb900cd9e83d25eef6188ab76c34b93d91aa3af02c344c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd1e47fef2f890415ad20a0275b4a7db7c02346f9485ad4af8167f9b0be0c929)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a771bc0691aabd82d39f443ecfda5f9b599c7e4e06a30f37b6474fe2dd5f7ca9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__123c5a24b05db76dfafeb053ed3e9d65d5d7455845c81474c1537dcb64fc7b08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b870666463c37cb1129cfe98555b97ac425388094db06eaab010e5e59580fe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46ea9d8b4910b88281df49e7fa7d1e00bb5b777e1ced88aefa4a6c9d0dc42fa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da0252f8ea92661fdb4d15a0199825a2bee2d046190cff478875cbcb5b3e551a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f332fe4f5710ab4976f39ecfd41c2543844761a93d00a826930df75b6792ed3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c919da13c80f3fca9aca65abd67f391606933917be15189d0d5536f9d25c39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fadb9622de7cf57d08b99dbd4693d4463c8d9a56cde0a6784558f0be1fc23890)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIdentifyingFields")
    def put_identifying_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f6633d631993f7581cb4c5567ece01c773ad94e1a01b02e7b09541cab1df4a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIdentifyingFields", [value]))

    @jsii.member(jsii_name="resetIdentifyingFields")
    def reset_identifying_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentifyingFields", []))

    @builtins.property
    @jsii.member(jsii_name="identifyingFields")
    def identifying_fields(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsList:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsList, jsii.get(self, "identifyingFields"))

    @builtins.property
    @jsii.member(jsii_name="identifyingFieldsInput")
    def identifying_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]]], jsii.get(self, "identifyingFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60601336e133794258efd43b56fd253be9d8043ac96108cfaac9cdfd34b89889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0a416030319e43eded9f6fc27911924421226085a39e3a1424addf1e560356f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBigQueryOptions")
    def put_big_query_options(
        self,
        *,
        table_reference: typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference, typing.Dict[builtins.str, typing.Any]],
        excluded_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
        identifying_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
        included_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
        rows_limit: typing.Optional[jsii.Number] = None,
        rows_limit_percent: typing.Optional[jsii.Number] = None,
        sample_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table_reference: table_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table_reference GoogleDataLossPreventionJobTrigger#table_reference}
        :param excluded_fields: excluded_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#excluded_fields GoogleDataLossPreventionJobTrigger#excluded_fields}
        :param identifying_fields: identifying_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#identifying_fields GoogleDataLossPreventionJobTrigger#identifying_fields}
        :param included_fields: included_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#included_fields GoogleDataLossPreventionJobTrigger#included_fields}
        :param rows_limit: Max number of rows to scan. If the table has more rows than this value, the rest of the rows are omitted. If not set, or if set to 0, all rows will be scanned. Only one of rowsLimit and rowsLimitPercent can be specified. Cannot be used in conjunction with TimespanConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#rows_limit GoogleDataLossPreventionJobTrigger#rows_limit}
        :param rows_limit_percent: Max percentage of rows to scan. The rest are omitted. The number of rows scanned is rounded down. Must be between 0 and 100, inclusively. Both 0 and 100 means no limit. Defaults to 0. Only one of rowsLimit and rowsLimitPercent can be specified. Cannot be used in conjunction with TimespanConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#rows_limit_percent GoogleDataLossPreventionJobTrigger#rows_limit_percent}
        :param sample_method: How to sample rows if not all rows are scanned. Meaningful only when used in conjunction with either rowsLimit or rowsLimitPercent. If not specified, rows are scanned in the order BigQuery reads them. If TimespanConfig is set, set this to an empty string to avoid using the default value. Default value: "TOP" Possible values: ["TOP", "RANDOM_START"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sample_method GoogleDataLossPreventionJobTrigger#sample_method}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions(
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
        file_set: typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet, typing.Dict[builtins.str, typing.Any]],
        bytes_limit_per_file: typing.Optional[jsii.Number] = None,
        bytes_limit_per_file_percent: typing.Optional[jsii.Number] = None,
        files_limit_percent: typing.Optional[jsii.Number] = None,
        file_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        sample_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_set: file_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#file_set GoogleDataLossPreventionJobTrigger#file_set}
        :param bytes_limit_per_file: Max number of bytes to scan from a file. If a scanned file's size is bigger than this value then the rest of the bytes are omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#bytes_limit_per_file GoogleDataLossPreventionJobTrigger#bytes_limit_per_file}
        :param bytes_limit_per_file_percent: Max percentage of bytes to scan from a file. The rest are omitted. The number of bytes scanned is rounded down. Must be between 0 and 100, inclusively. Both 0 and 100 means no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#bytes_limit_per_file_percent GoogleDataLossPreventionJobTrigger#bytes_limit_per_file_percent}
        :param files_limit_percent: Limits the number of files to scan to this percentage of the input FileSet. Number of files scanned is rounded down. Must be between 0 and 100, inclusively. Both 0 and 100 means no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#files_limit_percent GoogleDataLossPreventionJobTrigger#files_limit_percent}
        :param file_types: List of file type groups to include in the scan. If empty, all files are scanned and available data format processors are applied. In addition, the binary content of the selected files is always scanned as well. Images are scanned only as binary if the specified region does not support image inspection and no fileTypes were specified. Possible values: ["BINARY_FILE", "TEXT_FILE", "IMAGE", "WORD", "PDF", "AVRO", "CSV", "TSV", "POWERPOINT", "EXCEL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#file_types GoogleDataLossPreventionJobTrigger#file_types}
        :param sample_method: How to sample bytes if not all bytes are scanned. Meaningful only when used in conjunction with bytesLimitPerFile. If not specified, scanning would start from the top. Possible values: ["TOP", "RANDOM_START"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#sample_method GoogleDataLossPreventionJobTrigger#sample_method}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions(
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
        kind: typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind, typing.Dict[builtins.str, typing.Any]],
        partition_id: typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param kind: kind block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#kind GoogleDataLossPreventionJobTrigger#kind}
        :param partition_id: partition_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#partition_id GoogleDataLossPreventionJobTrigger#partition_id}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions(
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
        table_options: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param description: A short description of where the data is coming from. Will be stored once in the job. 256 max length. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#description GoogleDataLossPreventionJobTrigger#description}
        :param labels: To organize findings, these labels will be added to each finding. Label keys must be between 1 and 63 characters long and must conform to the following regular expression: '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?'. Label values must be between 0 and 63 characters long and must conform to the regular expression '(`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?)?'. No more than 10 labels can be associated with a given finding. Examples: - '"environment" : "production"' - '"pipeline" : "etl"' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#labels GoogleDataLossPreventionJobTrigger#labels}
        :param required_finding_label_keys: These are labels that each inspection request must include within their 'finding_labels' map. Request may contain others, but any missing one of these will be rejected. Label keys must be between 1 and 63 characters long and must conform to the following regular expression: '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?'. No more than 10 keys can be required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#required_finding_label_keys GoogleDataLossPreventionJobTrigger#required_finding_label_keys}
        :param table_options: table_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#table_options GoogleDataLossPreventionJobTrigger#table_options}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions(
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
        timestamp_field: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enable_auto_population_of_timespan_config: When the job is started by a JobTrigger we will automatically figure out a valid startTime to avoid scanning files that have not been modified since the last time the JobTrigger executed. This will be based on the time of the execution of the last run of the JobTrigger or the timespan endTime used in the last run of the JobTrigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#enable_auto_population_of_timespan_config GoogleDataLossPreventionJobTrigger#enable_auto_population_of_timespan_config}
        :param end_time: Exclude files, tables, or rows newer than this value. If not set, no upper time limit is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#end_time GoogleDataLossPreventionJobTrigger#end_time}
        :param start_time: Exclude files, tables, or rows older than this value. If not set, no lower time limit is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#start_time GoogleDataLossPreventionJobTrigger#start_time}
        :param timestamp_field: timestamp_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#timestamp_field GoogleDataLossPreventionJobTrigger#timestamp_field}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig(
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
    ) -> GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsOutputReference, jsii.get(self, "bigQueryOptions"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageOptions")
    def cloud_storage_options(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsOutputReference, jsii.get(self, "cloudStorageOptions"))

    @builtins.property
    @jsii.member(jsii_name="datastoreOptions")
    def datastore_options(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsOutputReference, jsii.get(self, "datastoreOptions"))

    @builtins.property
    @jsii.member(jsii_name="hybridOptions")
    def hybrid_options(
        self,
    ) -> GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsOutputReference, jsii.get(self, "hybridOptions"))

    @builtins.property
    @jsii.member(jsii_name="timespanConfig")
    def timespan_config(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigOutputReference", jsii.get(self, "timespanConfig"))

    @builtins.property
    @jsii.member(jsii_name="bigQueryOptionsInput")
    def big_query_options_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions], jsii.get(self, "bigQueryOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageOptionsInput")
    def cloud_storage_options_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions], jsii.get(self, "cloudStorageOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="datastoreOptionsInput")
    def datastore_options_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions], jsii.get(self, "datastoreOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="hybridOptionsInput")
    def hybrid_options_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions], jsii.get(self, "hybridOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timespanConfigInput")
    def timespan_config_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig"], jsii.get(self, "timespanConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfig]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78ff5a9b71efd577fd3b575b6d6137bcafeaa580baad08591d1eb5fb21bf68f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_auto_population_of_timespan_config": "enableAutoPopulationOfTimespanConfig",
        "end_time": "endTime",
        "start_time": "startTime",
        "timestamp_field": "timestampField",
    },
)
class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig:
    def __init__(
        self,
        *,
        enable_auto_population_of_timespan_config: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        timestamp_field: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enable_auto_population_of_timespan_config: When the job is started by a JobTrigger we will automatically figure out a valid startTime to avoid scanning files that have not been modified since the last time the JobTrigger executed. This will be based on the time of the execution of the last run of the JobTrigger or the timespan endTime used in the last run of the JobTrigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#enable_auto_population_of_timespan_config GoogleDataLossPreventionJobTrigger#enable_auto_population_of_timespan_config}
        :param end_time: Exclude files, tables, or rows newer than this value. If not set, no upper time limit is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#end_time GoogleDataLossPreventionJobTrigger#end_time}
        :param start_time: Exclude files, tables, or rows older than this value. If not set, no lower time limit is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#start_time GoogleDataLossPreventionJobTrigger#start_time}
        :param timestamp_field: timestamp_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#timestamp_field GoogleDataLossPreventionJobTrigger#timestamp_field}
        '''
        if isinstance(timestamp_field, dict):
            timestamp_field = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField(**timestamp_field)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f600b382e656d175bb217f904173c392c9ff5f0d95982191d63ec7b31c6fda4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#enable_auto_population_of_timespan_config GoogleDataLossPreventionJobTrigger#enable_auto_population_of_timespan_config}
        '''
        result = self._values.get("enable_auto_population_of_timespan_config")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''Exclude files, tables, or rows newer than this value. If not set, no upper time limit is applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#end_time GoogleDataLossPreventionJobTrigger#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''Exclude files, tables, or rows older than this value. If not set, no lower time limit is applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#start_time GoogleDataLossPreventionJobTrigger#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_field(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField"]:
        '''timestamp_field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#timestamp_field GoogleDataLossPreventionJobTrigger#timestamp_field}
        '''
        result = self._values.get("timestamp_field")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7ebe486568fbc7cf72b6ea3993aba85860c7b22005ac1a859ad3882757e6a88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTimestampField")
    def put_timestamp_field(self, *, name: builtins.str) -> None:
        '''
        :param name: Specification of the field containing the timestamp of scanned items. Used for data sources like Datastore and BigQuery. For BigQuery: Required to filter out rows based on the given start and end times. If not specified and the table was modified between the given start and end times, the entire table will be scanned. The valid data types of the timestamp field are: INTEGER, DATE, TIMESTAMP, or DATETIME BigQuery column. For Datastore. Valid data types of the timestamp field are: TIMESTAMP. Datastore entity will be scanned if the timestamp property does not exist or its value is empty or invalid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        value = GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField(
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
    ) -> "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampFieldOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampFieldOutputReference", jsii.get(self, "timestampField"))

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
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField"], jsii.get(self, "timestampFieldInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0fe5ed60194cb53649f0037563d195faf34257eecaa4bf94d7453d82dde4a7f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAutoPopulationOfTimespanConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__606dd34308eb5b17bc8bbdd57ec3ac2d2f4b0f4eb918e84560f4c8ceca5147f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c400479d32678af9ff9b8f556db388f1a3b775aef9b72d778051087c18e18c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__953733e038856ce953dd9f3df41f0c212cf3c19f0346a82204744e88314f80d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Specification of the field containing the timestamp of scanned items. Used for data sources like Datastore and BigQuery. For BigQuery: Required to filter out rows based on the given start and end times. If not specified and the table was modified between the given start and end times, the entire table will be scanned. The valid data types of the timestamp field are: INTEGER, DATE, TIMESTAMP, or DATETIME BigQuery column. For Datastore. Valid data types of the timestamp field are: TIMESTAMP. Datastore entity will be scanned if the timestamp property does not exist or its value is empty or invalid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cca4a1a0e0d01e2b7b4dd815070083e4ba32903e79d13f890806ffec1c42338)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#name GoogleDataLossPreventionJobTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a605d15d285fe8c1efd4f483eea1fb866ee51580fad608faa0aac77fc19e141d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bddd8b1ae5308cdc5537e8f87851532af43da3ffbb5d1ce953c75c674e93f59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__236627631377cc30458d4a9cb85aa125fe334d2d2acb17a05bbb287828171695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataLossPreventionJobTriggerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#create GoogleDataLossPreventionJobTrigger#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#delete GoogleDataLossPreventionJobTrigger#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#update GoogleDataLossPreventionJobTrigger#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28a69dc1bbd0162e5c6a2f793517529cc3aafbf29095e17e715b93ec100610d0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#create GoogleDataLossPreventionJobTrigger#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#delete GoogleDataLossPreventionJobTrigger#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#update GoogleDataLossPreventionJobTrigger#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed0e3419cc2cad7a4369fb91f74c6732b89f5d2c4934882254a938de701a0ef8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee1a96c3412c6efc06c95fa5090e11b67e4348c38563faee4c70ee038788f26d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2951922c5dc2c0af344219d5b2c237164043f535d7b69c91f0d7301a8d8d41aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d88b47cf765365d3247be97e0f52fbe746f576e81263be5b76d3a79143de30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e863f2ca9368abcebd14ac9283e5d19fb37008b5a0ab5e63457b20f7ceaca4fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerTriggers",
    jsii_struct_bases=[],
    name_mapping={"manual": "manual", "schedule": "schedule"},
)
class GoogleDataLossPreventionJobTriggerTriggers:
    def __init__(
        self,
        *,
        manual: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerTriggersManual", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[typing.Union["GoogleDataLossPreventionJobTriggerTriggersSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param manual: manual block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#manual GoogleDataLossPreventionJobTrigger#manual}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#schedule GoogleDataLossPreventionJobTrigger#schedule}
        '''
        if isinstance(manual, dict):
            manual = GoogleDataLossPreventionJobTriggerTriggersManual(**manual)
        if isinstance(schedule, dict):
            schedule = GoogleDataLossPreventionJobTriggerTriggersSchedule(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc8a480e434e0a23ab48b67ea4211cd10dfa60639a1ed0d0eea1d557d4c16ff8)
            check_type(argname="argument manual", value=manual, expected_type=type_hints["manual"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if manual is not None:
            self._values["manual"] = manual
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def manual(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerTriggersManual"]:
        '''manual block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#manual GoogleDataLossPreventionJobTrigger#manual}
        '''
        result = self._values.get("manual")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerTriggersManual"], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerTriggersSchedule"]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#schedule GoogleDataLossPreventionJobTrigger#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerTriggersSchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerTriggers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerTriggersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerTriggersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ebfba5fa920928859e306ab34503f76fdf9a6b686d8ddb4e3ee49f4c656a59f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionJobTriggerTriggersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a68cd8117528236fe1a5db7d8dc038cf74d62d62f291a524126999709967b39)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionJobTriggerTriggersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5322412c0443b2859688ebc0e69dc04a6499e53b067544603b36eb0121944562)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58d3703b770c1730ece4e9e6f8fc0681795017811fd74b3b2874bb8ff0d2c26d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8474b296512dab021e1c14fb81659aa1e05e3760381f82ee666ae101901fb782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerTriggers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerTriggers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerTriggers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f59a66d1df3e710f9a78e74044d22526d1a3bb9825d15a93b209105f2424dff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerTriggersManual",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataLossPreventionJobTriggerTriggersManual:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerTriggersManual(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerTriggersManualOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerTriggersManualOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db4e9b194e93e3381734dc35dae22205956e9b3820c8a2771bd95daedb6dfe25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerTriggersManual]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerTriggersManual], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerTriggersManual],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc5f142bf8b614fdad17d41578557cb106c8bab42b66ca6361407e7bd3f6a9f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionJobTriggerTriggersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerTriggersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b171d26728b745fa116f4e8f6733bc5604adc21ce997d164db4d5d16a6573af4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putManual")
    def put_manual(self) -> None:
        value = GoogleDataLossPreventionJobTriggerTriggersManual()

        return typing.cast(None, jsii.invoke(self, "putManual", [value]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        recurrence_period_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recurrence_period_duration: With this option a job is started a regular periodic basis. For example: every day (86400 seconds). A scheduled start time will be skipped if the previous execution has not ended when its scheduled time occurs. This value must be set to a time duration greater than or equal to 1 day and can be no longer than 60 days. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#recurrence_period_duration GoogleDataLossPreventionJobTrigger#recurrence_period_duration}
        '''
        value = GoogleDataLossPreventionJobTriggerTriggersSchedule(
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
    def manual(self) -> GoogleDataLossPreventionJobTriggerTriggersManualOutputReference:
        return typing.cast(GoogleDataLossPreventionJobTriggerTriggersManualOutputReference, jsii.get(self, "manual"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> "GoogleDataLossPreventionJobTriggerTriggersScheduleOutputReference":
        return typing.cast("GoogleDataLossPreventionJobTriggerTriggersScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="manualInput")
    def manual_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerTriggersManual]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerTriggersManual], jsii.get(self, "manualInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionJobTriggerTriggersSchedule"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionJobTriggerTriggersSchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerTriggers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerTriggers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerTriggers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8cb1fb0a2baf581892b6717f0241bfcdbab9991d00ae751aef4a1afbd8a7af9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerTriggersSchedule",
    jsii_struct_bases=[],
    name_mapping={"recurrence_period_duration": "recurrencePeriodDuration"},
)
class GoogleDataLossPreventionJobTriggerTriggersSchedule:
    def __init__(
        self,
        *,
        recurrence_period_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recurrence_period_duration: With this option a job is started a regular periodic basis. For example: every day (86400 seconds). A scheduled start time will be skipped if the previous execution has not ended when its scheduled time occurs. This value must be set to a time duration greater than or equal to 1 day and can be no longer than 60 days. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#recurrence_period_duration GoogleDataLossPreventionJobTrigger#recurrence_period_duration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1753ba366c5259478451cd691f732e667136e3b24ff9cc1d0ecbcc35c51c1b9a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_job_trigger#recurrence_period_duration GoogleDataLossPreventionJobTrigger#recurrence_period_duration}
        '''
        result = self._values.get("recurrence_period_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionJobTriggerTriggersSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionJobTriggerTriggersScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionJobTrigger.GoogleDataLossPreventionJobTriggerTriggersScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ba77c04cc76ec4fb919d7f4241569b7af8509f48534f2af7f20385d06c6e401)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de1773cae7784a12deb8b2d195becf09e34a711351cf1c362748d84d775f7dc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrencePeriodDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionJobTriggerTriggersSchedule]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionJobTriggerTriggersSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionJobTriggerTriggersSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e15c216c146ecce28cc440557ff966ef712bff6c43ae013974c62d66982880fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDataLossPreventionJobTrigger",
    "GoogleDataLossPreventionJobTriggerConfig",
    "GoogleDataLossPreventionJobTriggerInspectJob",
    "GoogleDataLossPreventionJobTriggerInspectJobActions",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentify",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfigOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTableOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmailsOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsList",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsPubSub",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsPubSubOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalogOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCsccOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriverOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindings",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTableOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfig",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesList",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegexOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScoreOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredTypeOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateTypeOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesList",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScoreOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimits",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeList",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesList",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetList",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegexOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximityOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesList",
    "GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfig",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsList",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFieldsOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsList",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFieldsOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsList",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFieldsOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReferenceOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSetOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKindOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionIdOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsList",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFieldsOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigOutputReference",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField",
    "GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampFieldOutputReference",
    "GoogleDataLossPreventionJobTriggerTimeouts",
    "GoogleDataLossPreventionJobTriggerTimeoutsOutputReference",
    "GoogleDataLossPreventionJobTriggerTriggers",
    "GoogleDataLossPreventionJobTriggerTriggersList",
    "GoogleDataLossPreventionJobTriggerTriggersManual",
    "GoogleDataLossPreventionJobTriggerTriggersManualOutputReference",
    "GoogleDataLossPreventionJobTriggerTriggersOutputReference",
    "GoogleDataLossPreventionJobTriggerTriggersSchedule",
    "GoogleDataLossPreventionJobTriggerTriggersScheduleOutputReference",
]

publication.publish()

def _typecheckingstub__9d0d9ea6bb81a21c3992292e2afbe9aa9a2f8f38abb4c99bebbd303fdcd845e7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    parent: builtins.str,
    triggers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerTriggers, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    inspect_job: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJob, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a699a7829d9198fbf3b62d7ea4bc7f99cdf2b559f972c56838c9f85bb5152b6b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400b0f28743c698651f83b72bafcbabdd42c0c88da17270ff3a0d2e0d18d25c3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerTriggers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155b1978c1188e118f5fb3d8fc7892595da4bf40caba9edb413eb51d7feace0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa804a38c1453ebd38dceca6f16a250a172272fb27aab741d9217265095266e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e06de2f2e31d5ea87be92f71c4221086ff77037865625c0a1db2ffb511f243(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513067889f32f03cc5583d26fd36be5f01794103f98df7db23fef04129565838(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3f36361a9e3b82ec15b503ec8557057dcf268981ff6b8fadf6ca42b5fa520b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c70733038492c1c3406b765dd430fa8e156ac0bffbb6baee5b79be821256988(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4c0cfb50e9869a9b0d7c6b1af7a4b24fb732dde8e14a5cdc4ee7d8bf43dff8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parent: builtins.str,
    triggers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerTriggers, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    inspect_job: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJob, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trigger_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c5535fb08c747f6d7a676bf8fa45703765fd33ca44680acc73179a4e6ea5c4(
    *,
    storage_config: typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfig, typing.Dict[builtins.str, typing.Any]],
    actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inspect_config: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    inspect_template_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b42a7716ec1a69e95512aee92a77142168bf2ba103ac5b7dddf38ed3cb422a(
    *,
    deidentify: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentify, typing.Dict[builtins.str, typing.Any]]] = None,
    job_notification_emails: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails, typing.Dict[builtins.str, typing.Any]]] = None,
    publish_findings_to_cloud_data_catalog: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog, typing.Dict[builtins.str, typing.Any]]] = None,
    publish_summary_to_cscc: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc, typing.Dict[builtins.str, typing.Any]]] = None,
    publish_to_stackdriver: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver, typing.Dict[builtins.str, typing.Any]]] = None,
    pub_sub: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActionsPubSub, typing.Dict[builtins.str, typing.Any]]] = None,
    save_findings: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b9e86fe30f1ead6b784fdbf4002015bfdef2c370738d75329555efb3ec48b0(
    *,
    cloud_storage_output: builtins.str,
    file_types_to_transform: typing.Optional[typing.Sequence[builtins.str]] = None,
    transformation_config: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    transformation_details_storage_config: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e250ee6af80b32e3cdd6ceed736152f47681624d7c6318549d40c0ae12379263(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__232869f72d01ae1a405a1154dee5739ed128b0b30865566a574eceb761db5250(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46662e7b01e357a2b0e87b8ebec8a2bbda29baaadc18a8513eafcbe367aee67a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630ff36f80174f3e04b676b935c1123b04174eacb83db16693c70e792a48511a(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentify],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64219629580f38536ebeb7e99b6d9cdec7dace61b48e7e64b7bb9dfb9aa1ae60(
    *,
    deidentify_template: typing.Optional[builtins.str] = None,
    image_redact_template: typing.Optional[builtins.str] = None,
    structured_deidentify_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a8a8c69865d74cb375a6c4e6d7854b75c12ae273c7969ef136a5470f770921(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f359923872a5c67f5ac249eecc1bb57235f82fff749a1874440fa7bb6cc8b245(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a5cd57119b434da197c10822a37ba1a72c16b5ac9aef86056ed8b4d3a720ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b51b4405ba45d2f73bf75019f571ec21dabff5b6e99fdc247e2a53177a8f7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a823ac0410e0791c66b22b3090dc51914237ed461895d0e28e92e15e9b23d2b(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b140b092f89441e16a1f8329ad73d20ada8dbed19edc0e8951d9829b3eee9f(
    *,
    table: typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4115963d7d6adc60a9800cca1b64e97e300ed5f3d4de4c2d015d4b80dbc5398(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01439deb77d02a6fe57c1d584276c0eeb5cd6e633126aae9d98c01da590b15ce(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5dfae1ac30e9b2a65d228dd120db01004652475bb0367789dc62079cbe5fe0(
    *,
    dataset_id: builtins.str,
    project_id: builtins.str,
    table_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d332b6829bd0fc98afaf00befb1360090bf97b1ba1a7162adf61ca6b96af1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90cbdf5f2344dfb00d188339b903b2f0cab8e6daa6522575641c4c2231c44b51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5a5faeaf93ab20f2f41232dec60cd25cc6f488b7db59e45fc2e01c5ddffcb43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac4c7cd2047e58a0b43a207e92ac442a666413e539270bf57d3eb5074789fe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0846541d69e4ec525b383d76c5598917dcbdf5a7c02c7377c3a9e99f0a1f2e23(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsDeidentifyTransformationDetailsStorageConfigTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc69885c175ff367efa7dd29c24f0a76ee147e38a31a585a4424a2ae19e0e47e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a07bad0c78e106ca8743e7fc9f64fd9592feb593580cee83bda455e16aa502(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsJobNotificationEmails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ada89d2b4bd33bfae64f00c58e4809bad95edb650a9394c8aaa9c9e2337946e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07166fc1b8bd816095ecb7f70f3ba1fbeca053dad1bc5b7d01a4053431d80813(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0238de74f76d7a0a29c10c53a0925e4d51afe78a72fb7ad2a45522d3069bde33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee82a645360b715581d58d263051a5a1e6dc2803c15c84550dadc383c52cd739(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8063ba8e553098fb83f03e0272a4f1fee5c25b923d920ebdddfbb750a42b77(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50eff909f45fb741e3f63b6ff9a2e0f68fa7dfe7a1895fd56473e3607f7e951c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4394ed47f2cbfccfc55da7085a29b6f6e08454cfb6e776155c90834adae16187(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92811793c327aecb7abb5cd4b7a3a65582ea32c25476e925d6e290aba34d74f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87fd1c64967036117c81eccbe629974df83c57db2db988bcdddcae863d8c4762(
    *,
    topic: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf8d19d736c64e816a63c8b64aea56b7df27cab33f0e0e63fc5a0606b424c66b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3eee9b5ad9285a28bebf2b19c26b4cbac2322b3b93664faa8c7465fe62701e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556acc8c03cdc5ddd8f25d1a40959a946c1390484e86d3e904e3f69ee76551d0(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsPubSub],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adaabce584badbe1c56d1fa6df9a6e506aaef11ac657121a195204fdc483d8e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed822284194d218b539539947236940c63cee6bb898bad0f7d7595f399c5655f(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsPublishFindingsToCloudDataCatalog],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06c841dc236c8aff9a8d1ca575526d6328bed02ae9a28dcbcd5ef0612de60a05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c4ba3d344674af5d5b44bb4ab23729fbb5082b1ad4b7aedd39a5fbe308af9e(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsPublishSummaryToCscc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd19d840e30c3f24e2a7d5f6706240da874d362f6273720fa8ca7ceb6b53896(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2f5569cf5a193a75170b808e23f50654d8ad6e82404dbd4dd0b7d015123f95(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsPublishToStackdriver],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653c253abc1015bd8d0c854597a750c18d634b70116c5a33d070ca383cbe736c(
    *,
    output_config: typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff6af371263bf589c86949300f2695ca78641f969b4e20b7f81a977baba1860(
    *,
    table: typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable, typing.Dict[builtins.str, typing.Any]],
    output_schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc68da821c9c3c64fbcbb6db56df7ddff67663508cae084765d8d851c9ab706(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80abc1a808d2392cdf67a6ba7da1ebb8b1ef4b274541e35abb57c6ed9b687113(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d887bdf2aaff0732dbe05fe4f94be5898830bc575273bd6022ae1e61bdfd582(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb1dafabd8bf35ef4fd6a6b8919997be86c26940a85b6b4846de19c08ad1b37(
    *,
    dataset_id: builtins.str,
    project_id: builtins.str,
    table_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c059279c67702a6689b344f4cd666a68c2ed66b484d1909063aaed14817e4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e92610c5c8cf1f5dfe8711345371a151da3d8ebf71276b277805e8a028e9d0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a626d7a5ed0b54ee4b293017fbf1086c98819858bcb818e18287cfa718ea58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efe03f64d4c645e92616373817cec6e6e59824d45ffc2a21dc6fec64d69651c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8967065c5338b7e415a4b1b5861e9b30235e4f7fe4d9eb1afa911cb6336da5cb(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindingsOutputConfigTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6fb2a2e6c436bd5f88c5ef9cab9483f7babb57f49f83770d8a316ebd5b8c566(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f092e5d3963e076c06dc47c696b1a744f5d801677b9fbff68c8a8ade0a8bfb2b(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobActionsSaveFindings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990804f5e89328643ef870ba14ff1c7aa3dae254643f0cf5e53cd131c1a597d9(
    *,
    custom_info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    exclude_info_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_quote: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    limits: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    min_likelihood: typing.Optional[builtins.str] = None,
    rule_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a3e8d1de39e857f825d62d7c10b3c120e2e10e49654a7992bbf156b5b94b93(
    *,
    info_type: typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType, typing.Dict[builtins.str, typing.Any]],
    dictionary: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
    exclusion_type: typing.Optional[builtins.str] = None,
    likelihood: typing.Optional[builtins.str] = None,
    regex: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex, typing.Dict[builtins.str, typing.Any]]] = None,
    sensitivity_score: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    stored_type: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType, typing.Dict[builtins.str, typing.Any]]] = None,
    surrogate_type: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee54f21583bd634099308f1cd9d232547b37d53875318519f9010de8fe1412c2(
    *,
    cloud_storage_path: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
    word_list: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0322b910f0bcf63cc853ee7604fc4031cc82fa5258b979e2eeee838fae18602e(
    *,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1ecd58f41881f0105dd1a93ca00bc1d546c84f1036a180153b3451ab44a62b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__412b71f6dda9ad0489aa9423b94f9ae70ef81ad5dfadde76b621083992df930f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d26884c9041faa2915b0b9038021c65a17f1160a60e7216398442b314f4f1d9(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryCloudStoragePath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddcb9bd9d29da11fbe03a86d1b16f487ee8153d62ed231ea2162cd0dfc20f03d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf720fb292de9fce91b355f6ace5a5d076341cd3c8a865065f16c7412ed806cd(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102e66a9782ae7ed5314de1c990594bcf9f65b9fc4be0393bb4bed0371fd9135(
    *,
    words: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b32b20be57abe505824ffc89062189912bb24d2d80814c503a5572474e26e6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827bc6bd7af8a436fb3864eda65751430f011932a8410161387931e0b6fa97ee(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcef7375ff6cec402e48e06ac5a718623cbceb947fc84a935116ce2fc8a7bd74(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesDictionaryWordListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05aad19afbbe280b7d5e0fbaf97e2602660f0065a580ecea39b72712beb760f8(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58af48a78345521f0b0d4a25da10c5eb60289bc259b5297da0c6fdf64852bec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709974c4fb2b7102a3225b5fbd7c204f93420ce22847130af8135e4da854e4de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48fd0bb65db44b5742b6f5f2f2aefc3ac5f15a5d0a9548cd5fc5361d16d47d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f78eaf423cdb89ca013a4185c939e5e94bec21db4653aba50155ccbca7ce846(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b75e4a08b4dfc7adf4120a791473e3176de56cf0363725f37928e9daaffc8bb1(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efdd949d73444e1d0e8e7356f6fde912ccaeeb41f2694991d19b89b45ca62458(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f4f9d8b40e0dc68a785c0a956bed207d6da0cb9f58a163cf2a08fdb74ec311(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e648fc08ccdd5fc9891c14efe7d561799d15f259bd60871f892a827f23f7c73(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesInfoTypeSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71886681629ed4d0f00d5ba004551513ac8c21108d23ef3a7994e9da6c09245d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9c9b47e18e268bdf7b1c14bc501cb1d8666b1e60fab10e5c82ca7ca93ca08e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac590962b03383938528954c77ec39969a575b519bdb08122d15fb6a203b682(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2003945b1416fe56560384a90c3d6bc4bf6d2d72d7627b58f5e059cf57ccc48f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83576019c6e470b68ecf8127068b8fc3dc13ffbedb24bc55b27f9dc3df4834ab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac6af239d75aed1017bc43c6c32f71dabdeb37fec7d528a2a46f4e880497f2d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b81f8488c567d8715313c0555b70092e252060ff394fc069ffb094b99b7c34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5cb670ef029902ed608d2fa03ae01ae32bb8d98a3909498ec39cd527bdb38ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0adf72dff6d5d30786ecb1b578d1099b92ef1000e886b78de6f8c83a75c103(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6d6df607a8a564bc085a32d53bde72a7c8081bdaaf121a702ccb154c80f772(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4964fdf1370a6d1e22f8d5dcd8622d9da0cf1311964f87f146383443a815d114(
    *,
    pattern: builtins.str,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22026c8d19acbb3b767d2134206b499dc1ad0c51d54d9a24244c877f96221b91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc93ca880d997dff5e997f04087509604f1bb958809988b75f13db9429f1eeb(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c548c62836780e4c08fb379ba14bac7aa3730f409844f33974bb67d4e8aeea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9917222b629d14c977284782d66fb1d57dae59cc710c6780b66b7675260a64(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c3a847d99626980199e7537fc68b6d3980843a2b5f32ac10931b9bd810e095(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab24b9829185deae8a514f8a5bc8fb31efbe4750fee758afb5b8201779c0c610(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a5a68411ecb8de0b3b2569919c77fc7de34c15f4779d007704feb64f7ffc52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2977baec7865b90fbb6f13e175f536c571d6f65c620d14df4f035bbfc8d81037(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d37205d89e8de66cc7881511652042a1a5c4365929bfe9a76beb0d65cf8cf6(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fae8c1657d30536b8b2c2b135a36a302027d30707d3a309ee1429401ffdef5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b6f7da650ef8bbc78bf225e292015b0f4192db537932b86964d0d640d5c6d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b90b337821e95ca8b062f6a046732ab5d28850f89c01468ee3ea0e4b87da803(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesStoredType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3afd49ad4a0ecd451bdcb89fb5b8f7caffd4d000cc834cff8b4b8467b72fdc31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499a197c5871a6dd0573a67db56c4c82bbe7a67cecaffc14c772315af11cba50(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypesSurrogateType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1ebbfbb49954ef5500e53c66a8db21680154645fca4543c0db59657c02d058(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23154a6fb471bdd931d29a34af1bd702f938bd5f62eb3db14c493143ba5a46d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4197adcbabb63fbcdf917ba3b132ee9de332320b7392c4057681fae6f1056761(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa6c756cacc7eb3c5390119d635cc198ab71a02648f9d4b5f6c7ec0041ba80f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a6c50124d561c012ea9f86d9253b9161808688515ddf8a2267ef8e6f6707e7e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c534e09c3672b9ce14ff1bd6b4efc170bcf87547eba098eab4e132f40936fffe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13761a8520934654d56ab5a3526b5b5f5daa4820cf4888849ad57fb065eee319(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3bf3ee4bc169e987897be59d015537c5a557b36e1e76ae38cfbd3aadab54e32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1a2361c33ead6c954223de32b9cb83d148cc17b3e58f9da54d14a226a4540c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86022ec517a3fae79b31e52d253c81b4a16380b6b5c9cb34b909b235f08a53d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3712c3808f8aa43690f083f3d52dc6ec49522a19277537711147454c7f9d53(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01d7607d8179b1dbd1d1d74fee56118705dde1be5556ca877f8b6ce2029a5550(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9529386dea07fa900bdd3f5b7fb6195a3be9f27ea76f130f7073ddabd9fa5a34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4829bab90cb3a336ca284b623aaef43c2eaa5115762ba9b6fb3742555f11005(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b893ef29a5e3f7c282e9082e168d4f4c02915ac164a9cd20defc69d83fda9f8d(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypesSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ffae029fdb9de696bce206500724fc5a810cac41c9f992acf429a1e130b3b7(
    *,
    max_findings_per_info_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_findings_per_item: typing.Optional[jsii.Number] = None,
    max_findings_per_request: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefc04c355f947c448edb715f2e5fc531f71275045bd484812af48fc22300660(
    *,
    info_type: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType, typing.Dict[builtins.str, typing.Any]]] = None,
    max_findings: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091e8eca23409f375e61ade7f1f00479ab1eae072d1b396d2e1317cd2672381a(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__096a3490080093a390492c118b5d8b4b8a86874a2db86e9241673632c2d41b8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2addfa0a7c5d69e4dc521a8d1d0a996d67dc641841db7fe66bc811f61cd0197(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__366c8db6f93402f466af67e8758d2f4cf2e6eddf6d9e2606e9abc6c94b0df396(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e188aa2ca0f08529981251551a0e53d054b135f65f2dd86976550d509c2a0d0(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23dddf5b614d05e767534833c9340448260b2fee1b3936fb644e7fbd94356553(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c6f35ba4e410277147da99099697e44f1c95e12039e916cc8ee5b1dc933b88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51ff21b3e22e77487980a1053f9d4853a768d7f60020485518a9d3de08e0029a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53345a826dba3534a0b5150838cc05bacadf535c9eb28374bfa06f46b6ee3a63(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b51ab7da38277749d3bfdd7bf5c116c6fcac2b79fb2ed2030a46814a13ea82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df94cf1f14e5b10a5457b21971bae052c1fbc435733c224f29cf7c5737de91d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d832b369f700ab47d8bb7dba4ba0bc109dc528911eae1e9ed30eb39d96695c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c635662b18047fbe476632ebc525e7becacba9e4e057ed1930f9ee1215f8ab5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__128194204a05940b27133307bb6811a3e7bb1e9b22a2e8fc5686ec7964d17a15(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9124218867891000f66098927a24563cc63d8a674a4001872af42d41c28bec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ff59fb6c53b26c41be28bede0af21373ab78487affa7941d3c7a98ee5fa6dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fecf0706607ca6813259cc61053d9b2df5934170b34875200bc3c100c041ef8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c29917ddbb4b9fec9f0000be7bd4bd1dfc53a3c26d13185f956adcc80a411d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471cac9e5d98241121847d66e0b446865aa399211f6a4a1930652239c6518a6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9798056f2dda6f8701a6686c21ee740ff2df733323d0713710a251e65656fa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimitsMaxFindingsPerInfoType, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1725cfb08028c67c315dd267e93732c2185e6f6e60f50cd5a38caf7cbf4c94d9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a3df3ce0a51c057fce0e922eb1f88d796a2d6c06b5c7e8bdc567f708746029(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ba451aa989d1a7fb9c921d5798fa93bd88631db0f14e32ce24d3e9d3a70ee0(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad61d057c9b66853cca51a7304d9945e1ccd1c12841370c81f4a8b62e40b084(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c0b445f65da7118d14edd72e742fb285eb2e08567c9caa8dce0f86fe7bd3b1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigCustomInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7a79d049641f09612b66b881a7a86b9bc17c0d8b42b2ab7b549f416844f6ce(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c11e331c054a39168d2b594ecfa1f4d4fb6f220f1bc085b8cfd28dab10d9af2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66928169db5bb5f8787ba3456557689b3d4a22a5c5ed92eb6b4cad5c1f1b2b3d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25409de0d362f8e118178d5c7afdb15e3cf379059fb9d1f6d909b04f51c6d6e2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__440586cdedd6d8c6499bc491d7d792b87ac00d5b160a87063416ba514b79508a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc8747fb394ba24e990e86a038ceeef3da7d1b35af5e3f0fa31cf197d890dd0(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7638c52e7d01924ac7eb417913988fcdaa4e1e72aa84f07b50638410c65fd638(
    *,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules, typing.Dict[builtins.str, typing.Any]]]],
    info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85465450888bf4bc679d9fce63ef72ed4848203c446f7c8067b32e4a7d69f895(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3566b07e7c382e0ff6491a5aa0be5ac08697cb11127ed69759492370ec1a41e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c84ee18a33627e4b5866cda32efe336e8adff1c4076d529e0226ae4bc040fad(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6c56348a73d455b62f0873d0eba9cf456099e177ec556cce96af9a47c9d08b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b91a3ef3bf36036776aa03ba22b650262dd5e07612a370331db135e4de7c82b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613b01162a5d58b6e51c631642c5e0162b23054b1d4a0ee9fbcf74d64db664ed(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ca2db557e9db7c110ced3f263f7c788cacaa002e6f72634a8891b35d2f75b4a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6735ce94439377273df5169a850f192ad0ef1712606a99e9605c9aa326321be6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332eec36e41d93c7ddb98f51201bc4734461cbb2b5e870e0a203eaa5e2423129(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d7767976196b0a850e3191c816f0e66cff2b2b3d15975afbd12c13b284c0828(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b04c97f4e371ae0425a0f991626707984d8b532444ff40993f030b99e0936d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__469c8c3c2f3a4a7e1dbfebda2714e6c3b3d56a4c26649a3e3cfde03710357785(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98640df5bc21e4b14748e07a0720239e7d233cdf7b7a82b4e5669a1740528af7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce9a8906611784e618941b33b308bf664303b408c8cbefcd16c0546eee25009(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9bf667690a439561750c56fad43a045413d2cd705bf1a71e244ec93407984b(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypesSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__999a443f72f6f78329ac38742ad986a3093db4397cbf0d605936e592287eeaee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09cca8a323299372edd610b4ec06e25b158fdc5d5caef34c35ce6a8ba3fe5dd3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e0e9fc5074156bcb6aaee3f2ce3132849be977a0384a7c4a02cfa48feee567(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ccda8601e6c731c787d251da6bd1a4f55633f9ccf6b0a2d96d8d34b51caba1d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75263b11a668d6f685b05e213855322a9b1bf2e5c17e2e70fa78ee807f69eea1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__925b3314719e350f72dcb6d9cba489505311b803a4d0921db287d96e927a6576(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90b3e96227f04f1ad3603d3256a8ca3a17fd55e911fae6ed287c9163d553d413(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70746082ef91c2b8d0e4821a8b29016311185a7e467322fd94275d2aa7028d48(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__896f22e518572b4c1a058692529cf5693e26718992f9c803b2c643fca497d93f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c66e48cdc326cb3361163306bfd05d6f9a9d7309fd97b56cdfc8c3acda189a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSet]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6725b58213bf49d365ed36e02a5b9009deebedcaf08a609f525c5156005e7615(
    *,
    exclusion_rule: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule, typing.Dict[builtins.str, typing.Any]]] = None,
    hotword_rule: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75158e985165bd2fd3fdde328f5f08d8ca50c9ee732d609c6f8534382ba5252(
    *,
    matching_type: builtins.str,
    dictionary: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude_by_hotword: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude_info_types: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes, typing.Dict[builtins.str, typing.Any]]] = None,
    regex: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e62f351a252eb37b734141b5556c2f2512c116c40e9d6410570a7ab87baad6d(
    *,
    cloud_storage_path: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
    word_list: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931be6566e9fecbc9b61dd59cb8c31463df85bac1eb7e402a1b2f57c30361e0f(
    *,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4791981ad76deb6d436e1299eb1b18a3dcb133fc49285d0b7a6629f4f44ddcdc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f002317b8aa9630230e054122ef5f3b94ab150501892dcd7ed44728b91368d43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7552d7701facfe61fe4ad8180a514412f33a1bd4dbf1f68790e2db58dfea0464(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676806e75714ccf21ba6480357a6cc509e1e1ed8cd22934603fb00becefc3b1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081dc39efbd1ecc5734a4f61259a7d108d9119bfc608e76224c153e72ee3fac9(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8604e2c6c8c64504b42c60286e8d1075d1ac0d7131d898d9756130983489bf9e(
    *,
    words: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8706d3fa4a203b4d33a962671b9a1749fedf26804360f4c2ff25e807070d1fe9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392c8917072026caa1e5b37779562058be28064d538e59684d61053d30098844(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34c0ccd05cf20d67a3fc854cde02afa033561e7c78e285cb74a70ed66ed8c64(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2962b30b1b6bab0871fa7bda1bbb98d2232d30087d90d9dd7cac0da5e37d7a52(
    *,
    hotword_regex: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex, typing.Dict[builtins.str, typing.Any]]] = None,
    proximity: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c2a56dbc54e63b48afc84e5516401db1538ae5daa6e8570e9b60e45ec807983(
    *,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    pattern: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05ebcdbb555dde2c6cd977e5b3e7104be01940692ea282704b3218f152bbdcc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7583b8cfeb629f903a4a3d7904f4aaf69ce299aac4d0d7b2491182a38997d2(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd8d1179b6f61240b9c8d38044c6ceffcdb7ca2d22d5ca60e1bd7a9485862e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9333a131364be44d98333bf657c15d3d9ff80945f0fb8c4d6b09b74b33a2d3e0(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4a1cebd3b7a4f06c8d812a823d80466d06358aa69e6dfc09063fd6d7ac6ace(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8af9b82755242707549ac0892dc8f689f05cb54e7758c0e9116b6f9bc433b92e(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d02869c1a28666c72742662b34d10fd00f01f088db2c9f430c7df8c1957a700(
    *,
    window_after: typing.Optional[jsii.Number] = None,
    window_before: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f626432a20d5c69ac8422e8203c4f8028e2c73388eb494344f8bea796e0281fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396ca02cb1e9afa7451858960b678e98ce2b5595ae7b9048b21bd3a987f7ea5a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be92b79b5f127dc95513250f3ab39faed114f73f578d137d6b08fd42269101ad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4d5a4bb56ab6614dad16b80538400e1d6a974c28c22f98ec70c1d2759f92fdb(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a5173b1bba4727483b2d683cfef482a7d71806d1680969c83e8109b8827745(
    *,
    info_types: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a1f2ee54e6d04e1b1a716953824c6cd414ea79d0d7878005d4efaab540e36a(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97e6f9d61edd74d9326bc37aafb510a8a00c1c93749b3c56652ead019ed695ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b7125367df2d0e0d5983a82aa09f325d19ed6526a1b3f81878fdf8273b3444(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe76fa06271b034cdfd72b6840af1cbb76f3368372f2cd2e2c7313c86b9e8f24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad77a321212d778f3d8513d27e53b6c16e62804d73f68b877eb4f13bf06380e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6796eb6c59d4e84793e67f237eee3324a642453a478fe6b4134313039f0905bd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a60dac2ca1ee53f45162532b4518283a90f7b908841dcc86474029b24aa8dea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e61b45bd3d7f79c3a331ba917225c9b90b22b57a4ed09cfd9e6e00580ca529f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fff9d79416610dd6ceaaa0b848fa62c3d5adbfef720eccb470258e49cc2c368(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83cb72aaf963142a49037eec9a9a603d4e03fa912f09234d533004b8a638137(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__170a27656b79025c6cfd93575b4287fdac3adda0927bbe95a5a6ad514034f370(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0804591c7ff7e8f1cd1f13fda025d8bd2518ff614f2f339bbbd13300a8c290d6(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aae5b7d4b4f2b1ab7845739e77104a75945fd1b993fc61085f9be56f76462ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1456cca1c60b0bb337c914f42a1b3a34cd55e6baaeec1d95e902d585285a23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28284f71ca0650548bf8f676bc181122cc541ef03d0d677f69077dbc12e89de9(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__535c21717fd34af59a5fc72ca918382135438d7f4d369000eae89c143dac3a38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77791eb3ba4579da8dc5cafadf874c1311d2ade1628272bdd34472213c001b11(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb7be1924c9871a4e8c82ea44243cb992f41df607f48c8d44b5b672082d1346e(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c63e8aa00d8fdc73db983ae30adc20376c2d254ff190235763b2f4b00f1d278c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f4771ec7f6072ddde846d0ae810fc025c4d06327e3a97dc837cf6f2c5ca2f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65da8203f7639d2b29ff57d23c1f5026bd0b68d14cddf07baa7327949540052(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb57de68e2ad3db654f7dbc966781dc7251e300c8ba4a40311e4dac33d998b6(
    *,
    pattern: builtins.str,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498a1d1785cc2a6d78ea7ca8bd2cf2cbdaaade3452c003fe09375cd2918592f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8368cfbf736b478e0a2cb067a99c3c69a22230a4218091e209e65235ab24e6c2(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af17fc2dea06b3a91adcc89342838514249dcefc673a327040f5f22fd68c3c1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10111870dc8a948690f35f5690e962e9344db43cb3536b380a188f8460234830(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesExclusionRuleRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e619b75c548bb66e023626966d883c9ca7d041188a97724c5d0d0d1a1cda7b6(
    *,
    hotword_regex: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex, typing.Dict[builtins.str, typing.Any]]] = None,
    likelihood_adjustment: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment, typing.Dict[builtins.str, typing.Any]]] = None,
    proximity: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46fa44d34a4e30df2cf58648f85f29be76ce4883f6d3f4a4d652441108bb1e2(
    *,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    pattern: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d03ee8d3a7521f55577765744783fd6f1ecca6261614c9777bb8715870b89e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55c30ef204d09fa79f8d170360d90acf78027462df500994955f93cb1006315a(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb2e8ece6015d1e307b969171bceb1d6eab3756a416caed555d25ad92edcb5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fae6b729be36ec1a78fc4a37aa77339413b29cd9248022097feb5aed936a797(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleHotwordRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ac14dc727f40dd9d4d4e2a6757c3c03559e87ad473ba0056382663e7a7db69(
    *,
    fixed_likelihood: typing.Optional[builtins.str] = None,
    relative_likelihood: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad691574efa31c927e428f210487d37c0f8c509b87bc19ee5cf8f7546fee76c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__597a0987b62c37de0f768be6dde8f15cf8e71f856d81c7b2d1eca65539300a55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692a2deb00f95377f48c0bb3f04f0d2968c89b8d86415a528fd3614a0aa930fb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c5a9cd7b73de9d969e3d8e1b1c296da11f58fd4b1659f376d632eaaec032a9(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba70d3112e22da0e08b2cb6338d864bba72a878d49668e4d31810111796b461(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c4f7ba756c81d8c93f3cc46f681b7618b17739aa6c1d6bf8f3e89c72491aaf(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee00b9aebd89ee94a1474901048dbc45d1559620e7cc3e9f7ddd1e2a749facaa(
    *,
    window_after: typing.Optional[jsii.Number] = None,
    window_before: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f94fe0204fb1daaea9f739b6316985667d9a9a86a5dc753121ec4bf95a37ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ff2278441528f3653d946e1e9c96785e2ae27a212cc5e323e20bfacd292bfd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa4b97752c64ccc6d3c75afefd03c0b7e41affd03f715064e325dacfd787b53(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d208369008187bb4f2c8ab402c6787023cc42408d601677fbb145ad274fee8e9(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRulesHotwordRuleProximity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc64b295e2923156c7b9243bacfed4e2a3660df2ee54521eac67500f2266c79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8f9fb7b01427acec49a4a96e9221eb4baf16911a581e848ff6a240c46fff9e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1418cfe19633fed4993226990403244c42647bece845c34bbb3a1408c59ccfd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797ec9b3297e638a875a2b6b7d78e13d1af7dd6c13c10a843497de27c61a90c8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67bcde11d3ff2ab94b6c1f6f4984eeff5e612afdcf68803331d399409bcd4d3e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7afdb7e292f20910fcd201d9dc2eb8ed0906a75486b71b75cd501f6d4c16d7eb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de59faaacb781d637e4d73d74cb39891530e0df3dbf8aa00e867dbe02a527d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0087fa97d4e398da1f6897294b3647c4055e0c4f6313135055fbc5bb1bd52e61(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobInspectConfigRuleSetRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cad2701fbf31fd40d603a71601e1c5aa7850d18835bcc47b7c0c4b63683fa9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e35eb8942f23d8ed4a312ebb111d2422a8e579c93e09bdf81499fd7b406f31(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca2ccdff2b660c95c1767469594f616cd41abc70530bab3071929b0939ff037(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfdd83e0c3fc087e01e8d74b9bab7830f9fdb30e5d3cd4994e3ebb584700b261(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470cc6c8770a59ea47874d7524831f8907158a8c09276bea5107c098d0b29df4(
    *,
    big_query_options: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_storage_options: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    datastore_options: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    hybrid_options: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timespan_config: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8106c2022e7767c786de413eb10f7ae98775626901c5a3ab4abe84bd6488cb(
    *,
    table_reference: typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference, typing.Dict[builtins.str, typing.Any]],
    excluded_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
    identifying_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
    included_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rows_limit: typing.Optional[jsii.Number] = None,
    rows_limit_percent: typing.Optional[jsii.Number] = None,
    sample_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbb22f32d62129a89a5d269ae6f2ce7b0c7e7cb73cec86a070134f6a7e812fe4(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27981fb74bbcf128a1402b995dec577a0a08e73e76a4d409b9367a787bebd319(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd74072c6536bd2cbe941aa7411a74ad5a91fe62a472f2467b52693a3edaae5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f94f208062228dbd569304cfeb67753c07559f5b7a306b49aebcd4a01b1047(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab08003d416380c32947440a36f3c406174154410b8e8e829cd5917299b1df24(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__449a5555a5ad3ff267428bf86bb5861d71da9b53fca94ca5c632daf9ab02c082(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4d1df472d1899ca0db2339070c82337a0fd1300be9f02a34ccff29f471e0be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b770f36ca276b14866888dac5322f0152fac761845cb7bbc0543c2c28be4fc8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402b210c56c696dadf8f6c6daa6fc3c7289c46f339cdc27c3db7d6441c4b590f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cdbda8402d058ed5376d4edd08b8405afc5b42e96da5b4ef02387997e03499f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21351654aa52b6443e77e414f4f30f18cc73f83ffc52feb39a323d6eff6f3218(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b83089fc7680eefa070b295da85ce347b0a80b2d2d0d66fe742b4b6edf70038(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__315e17f5e6e8bda8d572a60e0c449188c9ec969b230e3f378ab7e7392455c425(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c4993381a4ba3bc442c94ea2298ca9ade1a129060478794e26aa35f52a39099(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0881b0f04df352908d9a6cd17ad59509592f24f3a0a07a77b4daf190eb8fb1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b8931c40e5f27a6e044e80799815bc82948d2b68c5473d2eb812a15640f9ef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bdee3cfe73de716f466664c224193c53fa392b2769e59c1a7dc121de58ae99a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d685559bc6c9df65eb76286a150ea003eb6773b000ce7098bd00dc0869f686b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e34c2bed9e0122e84dd53506d25df4f10344ee4b6dcce33c4ca85c48f6fa92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b507af889b59f9795286dbca7b45891e4f871c9bbd38502372998ade54f3b486(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6409be3b177f27e8aba4ebec6e6d16ac8ad0051bd999f85391429132a53daeea(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e04f6ee4394cab58da2357cd230880bc075dd0f4c2f15d672a8378584c9e40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ae79b6035c9c034ee0bf4bb34517f84c18436d4c9605ae41fc3fc2b9402804(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ad3ad00c1722a94c2b5d150e669c2ae69e01e5a5f401925d522fedd4a531d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e29b5450520e9c93abe51bd507fdb9f84bd01a08e35aedc9b0ba2ad2672539(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc292cb33ba59afc5c34c32d1a7b0eb61adee99a708f97663cf6e25d0ac282fa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6649c0a9eee067637ed34b8fa923c75dcbb5dc9ade68a5fec86261138e3671fa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5042ee42c04032e012542143c486ff238a86e44a1f48a5cc1e3b86617f73e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bfd7cd72ff0a8c0a3d197b06747ea34693210f54207251ac494dd4baf7cbe92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24caeb2015323c7ec0c86bed60c4d915e94efc46628d61fb55505f9f7488b243(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a9f8a81e90a8be6807dac86aa0133dd7e302e20974c9945a892065221f13da5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8a0b982076dd6ccd13b574b9f163baad1b2ac3867a71f86892dd1573ae0025(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsExcludedFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846601a8b82b30774216e44b2c92555cf0e70719ab55009435cf7f66a11d3b8a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIdentifyingFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f2b8d5a46be85f004c96cb161e338fbce818acc47de3988238214923fea406(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsIncludedFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f9a74f63452d66fa169c13d48c1d148d56f299ca72becc27bfa74e003f7997(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__638ab826ec221a30183f15ea7a93b6b2c0954c6aaf9e34371b5efb54e7e0ff31(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae2d214021a015e12903693b0024b7598ec3285936c77bfbc919e04fec7a545(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64309101dd0816e55471bc342d94dab5c889be4ab5a6cd831b801c4f633dfc25(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c570b011b1902eb4439e906ad7c4e7405213ed752661ce8e191b0c2b2f9cdb84(
    *,
    dataset_id: builtins.str,
    project_id: builtins.str,
    table_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e58f5085c6ec7ab98460345a4c26d6b07d990c2b0274f99840caf7746bcb823(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8df201893ff971d20c66010e932b24e8996f55564ae5910e27201550aa455c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90a0118fbbab94dda57c4129b3648ace1cd737df5c5ba10d237c8d264d9c6de1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__193303ff80d001e7b840306982962241d4ba1e3b01e25d659ab651fcaa3e166d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5237a92fd8cb9a7ca01b3f05f7a27d7f48ce923e7358bfc3aee8e99bddb0c596(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigBigQueryOptionsTableReference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__011773d25ad301e98af04c879d6c51700237ae264b51dedc7fe8d7dc589a3966(
    *,
    file_set: typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet, typing.Dict[builtins.str, typing.Any]],
    bytes_limit_per_file: typing.Optional[jsii.Number] = None,
    bytes_limit_per_file_percent: typing.Optional[jsii.Number] = None,
    files_limit_percent: typing.Optional[jsii.Number] = None,
    file_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    sample_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea613cbb1936411886dfcf181274f55ce8c9f414d97002627aa94cc06dbb831b(
    *,
    regex_file_set: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet, typing.Dict[builtins.str, typing.Any]]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ddf879abec18d153c9ecb1fe9ce8eab5597cef4a48369ac120174c705f78f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d479b80697bd65be485eaa94a87df63c8d987f4fc05a9d027b3d3bf51ed30de9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45d05c35a866a2acf54b439f9f9646749fe4d5aa3705c2acf19ee2f00659f9b0(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7207511cb2fc3e4d5ce4cc7e99ed57c29d5809c273864229cf0ee09802f77504(
    *,
    bucket_name: builtins.str,
    exclude_regex: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_regex: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345a30286b67ba2eea9088818dd3f7fd8a2201041f8521aad4f9e4bb7682488f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2896baaaa9434d58943169281dd2f3d0a498180a049d5c0e7d54687e689801(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958329c24396a5beb84e54211f99ba3dece1b5a02b65e9077a47250d3069bb1c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ded93286b1c2e56f168c1b8c8fe43dc2b3b740eade8edd90839b0f932a3362(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b13516bde22a41d741ebe4cebedc1106e8de7caa68b86c4e67eb353b96b3258f(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptionsFileSetRegexFileSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591f5a47569bed6356dc433ef62e62a1e0f75a5b71b81eb6cbe5538e8d1c66a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc56f04e12c0ed1dd28b06f6afd7c91ef1b719a2cfe2eeed4be5f1185e91b771(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03366031435dea843d2f884aa19f8870fd74fac93b7894060fc9cb1feed91f0e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d768974c4528eaa132cdb50255114c3dbb1d7ca9e00e3680826608f2a6d4e322(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf33bd81bdbc32b739295c37076e7e38d3416290a6f4b587e10e39adbdbf57be(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9194a8dcfd2410cf31efe23d560b0f9651b03a4419a61468ef109b1f4fdfd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8af5f8e50c60ff93f8166f46696cef9906c501f460f4a411f7381835c09b23fc(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigCloudStorageOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0df70fe325aff760dadf4c76a30ac090c7462360b26c4c80b6f44dde5a4c857(
    *,
    kind: typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind, typing.Dict[builtins.str, typing.Any]],
    partition_id: typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32de240167b5f71bbd1b18a6cbb8510724f89f459e18917e2cc38e0957ee08bf(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__845c2160bf04dfe18d77534cfa400dd3daec156b31b9618f32cde60272ea5954(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b179d4fd81a88df354c76c14d39c787b68c4550fa1280b569bb526c2a5d87b18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ed8a35bb36910d10960af47fe6aad99d9255a2f1fe3af4407462a00b1d2d79(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsKind],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ab23e9d6e4dddb911e54c5e09f94849dc648f9c0444b5f73ebee4c35722ef8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e62269aea7dbceb5e1e44854a12434f646ae59058bc8600c3a449018e411a47e(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090d678c444c13bbd535bfbc1aaac700cdf1e27e496597c0e54b3e76d67b7584(
    *,
    project_id: builtins.str,
    namespace_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573268f1e46ce0cac23683741f19a2abf8de99047216746ed926b5ee11c425b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f711b7be9c381cfba7ae23ba26ceaf169c278108c8dcb5a7afa332bdfcbc0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff58d99a84b803f63591572901f1cc2a050350388d92583d7d70f2357f3ee31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab7a2001772d8134296ce8948e54e1ed14fb7ddcf0aa7bc98fab489e6f1136c(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigDatastoreOptionsPartitionId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd16536e6c61a512035a752c6fd07368d9f740bb4c02f4eb1c398460f5949f3(
    *,
    description: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    required_finding_label_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    table_options: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e01619e6ad640e977e199af8f493dae2c695300a02fcdda60b884c9f8c5203(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc285733762b34b7be58c8e60dd2c9f340d06e2df78c17224dbb1b242672fe35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bbbeb46fa0aae81dd74ba832702abd896353d621eaafea752a56e1f79382ef0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4159c5a1b2d0295cdd5261b7301d2825d889dff371291446cec1a983ec566358(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2030c079da9a3024190cc145647d908f355497ffea4ad34bfee6e302c6eb9b83(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a5e672cddf316de89115be0fc2ef02bfb695fb3e315d1768e26964079f8650(
    *,
    identifying_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fb6837d2d4e231ffa58742e3252a19e4f9d4520685a2d811cd5bc9e733f9294(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d51658e892b15db6fb900cd9e83d25eef6188ab76c34b93d91aa3af02c344c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1e47fef2f890415ad20a0275b4a7db7c02346f9485ad4af8167f9b0be0c929(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a771bc0691aabd82d39f443ecfda5f9b599c7e4e06a30f37b6474fe2dd5f7ca9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123c5a24b05db76dfafeb053ed3e9d65d5d7455845c81474c1537dcb64fc7b08(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b870666463c37cb1129cfe98555b97ac425388094db06eaab010e5e59580fe0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ea9d8b4910b88281df49e7fa7d1e00bb5b777e1ced88aefa4a6c9d0dc42fa4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0252f8ea92661fdb4d15a0199825a2bee2d046190cff478875cbcb5b3e551a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f332fe4f5710ab4976f39ecfd41c2543844761a93d00a826930df75b6792ed3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c919da13c80f3fca9aca65abd67f391606933917be15189d0d5536f9d25c39(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fadb9622de7cf57d08b99dbd4693d4463c8d9a56cde0a6784558f0be1fc23890(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6633d631993f7581cb4c5567ece01c773ad94e1a01b02e7b09541cab1df4a9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptionsIdentifyingFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60601336e133794258efd43b56fd253be9d8043ac96108cfaac9cdfd34b89889(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigHybridOptionsTableOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a416030319e43eded9f6fc27911924421226085a39e3a1424addf1e560356f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78ff5a9b71efd577fd3b575b6d6137bcafeaa580baad08591d1eb5fb21bf68f(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f600b382e656d175bb217f904173c392c9ff5f0d95982191d63ec7b31c6fda4(
    *,
    enable_auto_population_of_timespan_config: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    end_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
    timestamp_field: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ebe486568fbc7cf72b6ea3993aba85860c7b22005ac1a859ad3882757e6a88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe5ed60194cb53649f0037563d195faf34257eecaa4bf94d7453d82dde4a7f7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606dd34308eb5b17bc8bbdd57ec3ac2d2f4b0f4eb918e84560f4c8ceca5147f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c400479d32678af9ff9b8f556db388f1a3b775aef9b72d778051087c18e18c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953733e038856ce953dd9f3df41f0c212cf3c19f0346a82204744e88314f80d5(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cca4a1a0e0d01e2b7b4dd815070083e4ba32903e79d13f890806ffec1c42338(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a605d15d285fe8c1efd4f483eea1fb866ee51580fad608faa0aac77fc19e141d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bddd8b1ae5308cdc5537e8f87851532af43da3ffbb5d1ce953c75c674e93f59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236627631377cc30458d4a9cb85aa125fe334d2d2acb17a05bbb287828171695(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerInspectJobStorageConfigTimespanConfigTimestampField],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a69dc1bbd0162e5c6a2f793517529cc3aafbf29095e17e715b93ec100610d0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed0e3419cc2cad7a4369fb91f74c6732b89f5d2c4934882254a938de701a0ef8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee1a96c3412c6efc06c95fa5090e11b67e4348c38563faee4c70ee038788f26d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2951922c5dc2c0af344219d5b2c237164043f535d7b69c91f0d7301a8d8d41aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d88b47cf765365d3247be97e0f52fbe746f576e81263be5b76d3a79143de30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e863f2ca9368abcebd14ac9283e5d19fb37008b5a0ab5e63457b20f7ceaca4fa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8a480e434e0a23ab48b67ea4211cd10dfa60639a1ed0d0eea1d557d4c16ff8(
    *,
    manual: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerTriggersManual, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: typing.Optional[typing.Union[GoogleDataLossPreventionJobTriggerTriggersSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ebfba5fa920928859e306ab34503f76fdf9a6b686d8ddb4e3ee49f4c656a59f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a68cd8117528236fe1a5db7d8dc038cf74d62d62f291a524126999709967b39(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5322412c0443b2859688ebc0e69dc04a6499e53b067544603b36eb0121944562(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58d3703b770c1730ece4e9e6f8fc0681795017811fd74b3b2874bb8ff0d2c26d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8474b296512dab021e1c14fb81659aa1e05e3760381f82ee666ae101901fb782(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59a66d1df3e710f9a78e74044d22526d1a3bb9825d15a93b209105f2424dff1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionJobTriggerTriggers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db4e9b194e93e3381734dc35dae22205956e9b3820c8a2771bd95daedb6dfe25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc5f142bf8b614fdad17d41578557cb106c8bab42b66ca6361407e7bd3f6a9f7(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerTriggersManual],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b171d26728b745fa116f4e8f6733bc5604adc21ce997d164db4d5d16a6573af4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8cb1fb0a2baf581892b6717f0241bfcdbab9991d00ae751aef4a1afbd8a7af9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionJobTriggerTriggers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1753ba366c5259478451cd691f732e667136e3b24ff9cc1d0ecbcc35c51c1b9a(
    *,
    recurrence_period_duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba77c04cc76ec4fb919d7f4241569b7af8509f48534f2af7f20385d06c6e401(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de1773cae7784a12deb8b2d195becf09e34a711351cf1c362748d84d775f7dc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15c216c146ecce28cc440557ff966ef712bff6c43ae013974c62d66982880fe(
    value: typing.Optional[GoogleDataLossPreventionJobTriggerTriggersSchedule],
) -> None:
    """Type checking stubs"""
    pass

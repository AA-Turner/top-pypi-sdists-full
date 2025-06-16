r'''
# `google_dialogflow_cx_test_case`

Refer to the Terraform Registry for docs: [`google_dialogflow_cx_test_case`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case).
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


class GoogleDialogflowCxTestCase(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCase",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case google_dialogflow_cx_test_case}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        notes: typing.Optional[builtins.str] = None,
        parent: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        test_case_conversation_turns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxTestCaseTestCaseConversationTurns", typing.Dict[builtins.str, typing.Any]]]]] = None,
        test_config: typing.Optional[typing.Union["GoogleDialogflowCxTestCaseTestConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDialogflowCxTestCaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case google_dialogflow_cx_test_case} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The human-readable name of the test case, unique within the agent. Limit of 200 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#display_name GoogleDialogflowCxTestCase#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#id GoogleDialogflowCxTestCase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notes: Additional freeform notes about the test case. Limit of 400 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#notes GoogleDialogflowCxTestCase#notes}
        :param parent: The agent to create the test case for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#parent GoogleDialogflowCxTestCase#parent}
        :param tags: Tags are short descriptions that users may apply to test cases for organizational and filtering purposes. Each tag should start with "#" and has a limit of 30 characters Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#tags GoogleDialogflowCxTestCase#tags}
        :param test_case_conversation_turns: test_case_conversation_turns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#test_case_conversation_turns GoogleDialogflowCxTestCase#test_case_conversation_turns}
        :param test_config: test_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#test_config GoogleDialogflowCxTestCase#test_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#timeouts GoogleDialogflowCxTestCase#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da570f79b46ef1a1b8db3cf0389449fd5c4b15a174e1dbced6287485eca3635a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDialogflowCxTestCaseConfig(
            display_name=display_name,
            id=id,
            notes=notes,
            parent=parent,
            tags=tags,
            test_case_conversation_turns=test_case_conversation_turns,
            test_config=test_config,
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
        '''Generates CDKTF code for importing a GoogleDialogflowCxTestCase resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDialogflowCxTestCase to import.
        :param import_from_id: The id of the existing GoogleDialogflowCxTestCase that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDialogflowCxTestCase to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ed31b51b1c67f3474f93fa1cb08352dd02f2763f3dd4b1e5ba59a804ea171c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTestCaseConversationTurns")
    def put_test_case_conversation_turns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxTestCaseTestCaseConversationTurns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755ecb82aac4f2f7dda9bab2b723cfffecf856f73f4236ce236286f3422f67de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTestCaseConversationTurns", [value]))

    @jsii.member(jsii_name="putTestConfig")
    def put_test_config(
        self,
        *,
        flow: typing.Optional[builtins.str] = None,
        page: typing.Optional[builtins.str] = None,
        tracking_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param flow: Flow name to start the test case with. Format: projects//locations//agents//flows/. Only one of flow and page should be set to indicate the starting point of the test case. If neither is set, the test case will start with start page on the default start flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#flow GoogleDialogflowCxTestCase#flow}
        :param page: The page to start the test case with. Format: projects//locations//agents//flows//pages/. Only one of flow and page should be set to indicate the starting point of the test case. If neither is set, the test case will start with start page on the default start flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#page GoogleDialogflowCxTestCase#page}
        :param tracking_parameters: Session parameters to be compared when calculating differences. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#tracking_parameters GoogleDialogflowCxTestCase#tracking_parameters}
        '''
        value = GoogleDialogflowCxTestCaseTestConfig(
            flow=flow, page=page, tracking_parameters=tracking_parameters
        )

        return typing.cast(None, jsii.invoke(self, "putTestConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#create GoogleDialogflowCxTestCase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#delete GoogleDialogflowCxTestCase#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#update GoogleDialogflowCxTestCase#update}.
        '''
        value = GoogleDialogflowCxTestCaseTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNotes")
    def reset_notes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotes", []))

    @jsii.member(jsii_name="resetParent")
    def reset_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParent", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTestCaseConversationTurns")
    def reset_test_case_conversation_turns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTestCaseConversationTurns", []))

    @jsii.member(jsii_name="resetTestConfig")
    def reset_test_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTestConfig", []))

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
    @jsii.member(jsii_name="creationTime")
    def creation_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTime"))

    @builtins.property
    @jsii.member(jsii_name="lastTestResult")
    def last_test_result(self) -> "GoogleDialogflowCxTestCaseLastTestResultList":
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultList", jsii.get(self, "lastTestResult"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="testCaseConversationTurns")
    def test_case_conversation_turns(
        self,
    ) -> "GoogleDialogflowCxTestCaseTestCaseConversationTurnsList":
        return typing.cast("GoogleDialogflowCxTestCaseTestCaseConversationTurnsList", jsii.get(self, "testCaseConversationTurns"))

    @builtins.property
    @jsii.member(jsii_name="testConfig")
    def test_config(self) -> "GoogleDialogflowCxTestCaseTestConfigOutputReference":
        return typing.cast("GoogleDialogflowCxTestCaseTestConfigOutputReference", jsii.get(self, "testConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDialogflowCxTestCaseTimeoutsOutputReference":
        return typing.cast("GoogleDialogflowCxTestCaseTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="notesInput")
    def notes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notesInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="testCaseConversationTurnsInput")
    def test_case_conversation_turns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxTestCaseTestCaseConversationTurns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxTestCaseTestCaseConversationTurns"]]], jsii.get(self, "testCaseConversationTurnsInput"))

    @builtins.property
    @jsii.member(jsii_name="testConfigInput")
    def test_config_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxTestCaseTestConfig"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxTestCaseTestConfig"], jsii.get(self, "testConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDialogflowCxTestCaseTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDialogflowCxTestCaseTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2edebd5de152ff4ef216154067cddaed3d6b9d6a0d028d67ae9f49a10239da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5ef0aa31ec83ec4be9306636efa3a95cee90131390d909c819d9b1d42e7449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notes")
    def notes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notes"))

    @notes.setter
    def notes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aaca36b8b606e5ba5fcd17a7eba7ff04e041c30dc139d10432a689c1302a2ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9848d28d79af258f003419dbb5e6f36d303aac653bbeee2dfec1c7e1ba5abc68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd210ddac9d07398b44453fb5de68b3d9923d99edaaf4bd9b42dd288f1755387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "id": "id",
        "notes": "notes",
        "parent": "parent",
        "tags": "tags",
        "test_case_conversation_turns": "testCaseConversationTurns",
        "test_config": "testConfig",
        "timeouts": "timeouts",
    },
)
class GoogleDialogflowCxTestCaseConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        notes: typing.Optional[builtins.str] = None,
        parent: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        test_case_conversation_turns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxTestCaseTestCaseConversationTurns", typing.Dict[builtins.str, typing.Any]]]]] = None,
        test_config: typing.Optional[typing.Union["GoogleDialogflowCxTestCaseTestConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDialogflowCxTestCaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The human-readable name of the test case, unique within the agent. Limit of 200 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#display_name GoogleDialogflowCxTestCase#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#id GoogleDialogflowCxTestCase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notes: Additional freeform notes about the test case. Limit of 400 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#notes GoogleDialogflowCxTestCase#notes}
        :param parent: The agent to create the test case for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#parent GoogleDialogflowCxTestCase#parent}
        :param tags: Tags are short descriptions that users may apply to test cases for organizational and filtering purposes. Each tag should start with "#" and has a limit of 30 characters Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#tags GoogleDialogflowCxTestCase#tags}
        :param test_case_conversation_turns: test_case_conversation_turns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#test_case_conversation_turns GoogleDialogflowCxTestCase#test_case_conversation_turns}
        :param test_config: test_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#test_config GoogleDialogflowCxTestCase#test_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#timeouts GoogleDialogflowCxTestCase#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(test_config, dict):
            test_config = GoogleDialogflowCxTestCaseTestConfig(**test_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleDialogflowCxTestCaseTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad62f3f0e5f59a28c5437d102c5f3ff3a6dbb2bba5a7eb11a5cabcb89517927e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notes", value=notes, expected_type=type_hints["notes"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument test_case_conversation_turns", value=test_case_conversation_turns, expected_type=type_hints["test_case_conversation_turns"])
            check_type(argname="argument test_config", value=test_config, expected_type=type_hints["test_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
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
        if id is not None:
            self._values["id"] = id
        if notes is not None:
            self._values["notes"] = notes
        if parent is not None:
            self._values["parent"] = parent
        if tags is not None:
            self._values["tags"] = tags
        if test_case_conversation_turns is not None:
            self._values["test_case_conversation_turns"] = test_case_conversation_turns
        if test_config is not None:
            self._values["test_config"] = test_config
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
    def display_name(self) -> builtins.str:
        '''The human-readable name of the test case, unique within the agent. Limit of 200 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#display_name GoogleDialogflowCxTestCase#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#id GoogleDialogflowCxTestCase#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notes(self) -> typing.Optional[builtins.str]:
        '''Additional freeform notes about the test case. Limit of 400 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#notes GoogleDialogflowCxTestCase#notes}
        '''
        result = self._values.get("notes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''The agent to create the test case for. Format: projects//locations//agents/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#parent GoogleDialogflowCxTestCase#parent}
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags are short descriptions that users may apply to test cases for organizational and filtering purposes.

        Each tag should start with "#" and has a limit of 30 characters

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#tags GoogleDialogflowCxTestCase#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def test_case_conversation_turns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxTestCaseTestCaseConversationTurns"]]]:
        '''test_case_conversation_turns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#test_case_conversation_turns GoogleDialogflowCxTestCase#test_case_conversation_turns}
        '''
        result = self._values.get("test_case_conversation_turns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxTestCaseTestCaseConversationTurns"]]], result)

    @builtins.property
    def test_config(self) -> typing.Optional["GoogleDialogflowCxTestCaseTestConfig"]:
        '''test_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#test_config GoogleDialogflowCxTestCase#test_config}
        '''
        result = self._values.get("test_config")
        return typing.cast(typing.Optional["GoogleDialogflowCxTestCaseTestConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDialogflowCxTestCaseTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#timeouts GoogleDialogflowCxTestCase#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDialogflowCxTestCaseTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResult",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxTestCaseLastTestResult:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseLastTestResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurns",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxTestCaseLastTestResultConversationTurns:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseLastTestResultConversationTurns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5af901b28ed2db45b2982b7ea3bff4251f40bab6761e5ee75c30aa6c080e9e52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ba0686ee7e4a003d66409694c01c207531c314870d2e2b125fcf69134986a5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5856b7262dadf8ca111fe210d5942aefcf82cef22f902937832834a1aa525d87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9e923a4f66cd6207e6d481e48141c7ff6175c9b7eb25e237df86067ee6225f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d3bc5d6b6c0983ebb6eb325be2b2ff0af9ffc8ddf853f2622b5ffdd92df3344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0a35cd858323179f58a18e11ca1331e71d0b9caf26baa45d1a38a316f584660)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(
        self,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputList":
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputList", jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualAgentOutput")
    def virtual_agent_output(
        self,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputList":
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputList", jsii.get(self, "virtualAgentOutput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurns]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurns],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b541b29564954de4db9a9e9c8ecf526662739a0ab64fe6b0901db40edc322a0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInput",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInput",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmf",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmf:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67e520861bd5776272244a1302c598a5995b9809b4320cfac3d94687c3eb43bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da46ac89245b3e15a96873b756948ddf3c13d1829714f5df14993dbd0b30f6f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9caa163c147f1a563c602e774df8b8645d1813270398ec49fefc8b16c72b8ad2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ddc97e3b4cc1b8ca7fd74098f7ef354e14ced29b6bdcbd53405ec53b1a8f017)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2051b80e16c182cfeded60d0bac6a656ede88f78d8fa758c8f7afec6eff7ca96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c1501881ed01232ba298d3bdb48f9b50283da97d70c35d8daa37f06ad816388)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="digits")
    def digits(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "digits"))

    @builtins.property
    @jsii.member(jsii_name="finishDigit")
    def finish_digit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "finishDigit"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmf]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmf], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmf],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8088f6f1af596e6131d1442fde734622ef560ace9f6e457496a5d53124db12ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEvent",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEvent:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEvent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5baf5dafe9c269b5f47a384642552bce6d65ae0a8697dc734242d1cccd741c13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd26af89f9af066732060e43d60ee1891148710eb6ff088c2cc0064c65e6e3d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86485c7181aa253888bff52a54f92e4740b70ad8b2c4cbfb92820fb476ce469f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__125b24bd5affee995f65b961812a82f44b4adc074e033721fb6cbd9c005084ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__061a3f94db12b4b02c75f24529a95b717bc5e0fe825156331a9c7e89c820aacb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5ae4fc2360ee8204213edc971b2304c9da4041fd3aaf1ac076c06f221094159)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="event")
    def event(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "event"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEvent]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEvent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEvent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f0c8a0ea81e2acce4505695fc50b8a4b894adaf5b3664804eb6f0d1727e519)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cf85468064d523bc5a907ff5bc7976c3fa9b8881fcab1f01766613373348aa9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc0b06a22bffc301e9d51404c7539fb005fd3b58e2e565706f9a1d16b09cf53)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc21996824b92ab7570bb23ea8c8c9370135c0f727d66196af94953613197cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a36d63a5f34687b5247d903719cfcb1352fcb03547142db694faa1794d38b58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e78c66d5240ebacf122af97c34780027bbf81c5972451793cd29355d03b32030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04e7c6eb717c1db4f58cb6ebc7f3bb131a81d1f828a8ae5c0ce4dfe4729c2cde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dtmf")
    def dtmf(
        self,
    ) -> GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfList:
        return typing.cast(GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfList, jsii.get(self, "dtmf"))

    @builtins.property
    @jsii.member(jsii_name="event")
    def event(
        self,
    ) -> GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventList:
        return typing.cast(GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventList, jsii.get(self, "event"))

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(
        self,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextList":
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextList", jsii.get(self, "text"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInput]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da1401bbe3f20b2b6f2acd41f70be0dc09feeb5a2b7df356b17845b44d212082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputText",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputText:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e079c5c122f11641468f518a9f113db7f06aa21cee23c57405a16de24b08924)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c708dbb01011f05fbfdeb373b6a45d4d2011bbf063af0945367d5ee3a2f6f22a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2fbcf3f7a21a64fac4c51998105e7a1d1bdb91b1112099c3be13b36b00e66f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__349837529aaa6a1578ad0fe12c241c978aaafd1e6bebac97d8f4a00869d81f90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c62d259219571aa0652606de699b62a9d25da2f960838c1e4d4c0b3af5b2ff76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0746d7e0fb51319ff8ad013fe84cd96a873bb4f0a12932434451412101b39e46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputText]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputText], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputText],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd6f1d6523e4f5ce56d6954c290366c76d6e3b956c4a346f82abbbb1d81b55e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffbd2f19dc8768516893aca984580b30fa536c626bade176b37e8ff0a4418fd5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e59624dc287ff3d67ad76604872f25ecc257b6f67f3c680ce4baeb58031ccac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__028bdb0c626dae25312d02b6bd02c53349dd49348d86d04e90d9eedd0afac78e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__530ffeb9031cef8dce53e503edf985dc1f85107240d623820a37ad7fccd4a0b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c0973c815db376207ad6ff364c6bbc34e5cd84bc19042276905c4585bf6332e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3dbe2ee334fec4e5a4f8c778d65397176ca5f943c30725682b1769b19ed6b98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="enableSentimentAnalysis")
    def enable_sentiment_analysis(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enableSentimentAnalysis"))

    @builtins.property
    @jsii.member(jsii_name="injectedParameters")
    def injected_parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "injectedParameters"))

    @builtins.property
    @jsii.member(jsii_name="input")
    def input(
        self,
    ) -> GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputList:
        return typing.cast(GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputList, jsii.get(self, "input"))

    @builtins.property
    @jsii.member(jsii_name="isWebhookEnabled")
    def is_webhook_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isWebhookEnabled"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInput]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c31d0d4d81b103b9199f2e5c5fadad563691a020031340b3f97aafc9fb7340)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPage",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPage:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45ea77e36f86a8105f901dcfb6773a41e9d27d9d1b81ae0190413ff91546023d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b488b239947450111c5fcef92d80f1ec96ce9a8ca235e6458c6c93fe66b81b8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361918ad28bd0344e63b5628819cdf6dac41990e562c0eb90276efbd8e2457d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1245df19e386baf1f441689068051a85251f9ed2183921f6218926ccb87fb87b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c404e95bc27f17f81ee95b137998eb41b20e6e4eabe08547f9d78979c8f9c778)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80d023ee4edfe8c0162f892f01742f12f5f08eb0d47fa8764936b27b0451c47d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPage]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b29937648004a4c25b0d3c48402cf92f15beb0b7bcc29315e82b01b4357afa68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferences",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferences:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ecc62e62cc6c099b40c47d701108490b89358efd7396ef9f34031f77fcf47b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d90717de452171da4b3fc7510824ca436b53e8aeaef44b72f3cac5f48c851543)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b03428bdbb711aac47bcfdb383a0a411db4ce7c295d207a9e40c2cc470d666)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e911158040e948b8c69f0f40a3bf14157671bd8f9708fccaa1692c48df62a4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4be3e6db260583ed0596b5fa1dc7bf363c1df89db18c026486c49ee847e7480b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__173bb2624d35fd2af2e909542adae10838c365b0b335fcfffc9548328ede48de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferences]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1026223776e46445ce9d151a0b8c6a828e54bd8c2cf95b64180d645cb37bfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a10899e88ee80a20e62da5c83d8a6787cab61c61adab7eb6aec8921593b82146)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96bc4ca12b3da8dcc4d60fb168b470b5fa65c34b6204420c1b39033119ac4c40)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c5def2ece3ed71bedd2be3e97d9d9f5e1da0c2ffb6b7a283ec254148a1504ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17a8da8c8485ee4d7535cfb63a34bacdf77ee0ffc670ea24cceb62398941a5ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c64d93e9547856ca7bc57daf4bb2da966b08c11472c14442269ed16857601294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab59533c3f9e2571005d6992b41728767e30180851051973a2f419dd3a0816b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="currentPage")
    def current_page(
        self,
    ) -> GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageList:
        return typing.cast(GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageList, jsii.get(self, "currentPage"))

    @builtins.property
    @jsii.member(jsii_name="differences")
    def differences(
        self,
    ) -> GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesList:
        return typing.cast(GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesList, jsii.get(self, "differences"))

    @builtins.property
    @jsii.member(jsii_name="sessionParameters")
    def session_parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionParameters"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(
        self,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusList":
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="textResponses")
    def text_responses(
        self,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesList":
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesList", jsii.get(self, "textResponses"))

    @builtins.property
    @jsii.member(jsii_name="triggeredIntent")
    def triggered_intent(
        self,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentList":
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentList", jsii.get(self, "triggeredIntent"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutput]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fb13d263ec718c18c6721699feb9035f29308db984a1835b86e1bf1af9b0232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b4b303c9571092e07016186adb160d7897392282d126a3d0a734b4747552323)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82eaf30c34b807223a4487879a854f46956c2deb2974ad44e7367ed150bb80be)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7175df46018b755c0268886e525eaf3bef40d7e6cd15402ed58ef16425cccd74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c34b6b71007fcc5fc6201015824e0dc22fd6dbd930007e4913c607fbd2614ddc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__094b9e1b1534b893043ec8c7f82a16b0b2b3fd935343430593f92886b6503c10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcaa02a717a0a42906f4fc9560402a649f2d17fedee0eef4ca6d8474285604f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatus]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78fb6166a8e5d6878c92a779f7797ccd157461a231c921f78b2ccd046205e12f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponses",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponses:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponses(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b18f6056004b1a4094babb494b92774bfab42607ee2ca8f39faf8951990074bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6212f4ad0e9a26b8abdb2a93951176cf4182c256940fe4051ba851f1b586b979)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce6cd7982f566ae94847f63898c4b88ef93e958d3e8741ca9c78448e283b7d07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca77952d92aeef8e87541d9a7ab591689b521563d0a4c6d65905d4feb456f0a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c47d576f48ce464056a0181c6bd94b0586451df0af0e8e1cc6a083449db877c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02919435055c2dbcf520b82120f7219952dee6349f907b8ada61eb9ddaa54a1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "text"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponses]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponses], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponses],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27a3c4a56631f638d47e979c0bd025387a3ea62915c146eaf1dfe6f454035bc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntent",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntent:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8a2f847661a0d9165d559e31035d2b354ac08f33263384d6af2522f3d12df5d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad439560b3f2e313f6fac6e8abbf93a38e2d651f9b45eb135af51bf1c858ba79)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df37b3c723b1d11fd71b15969961d7e405532e6f0c6d54ced2900f4f0dd3d111)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dee1e24d5454c739e0a6916cd54aae76bc5c4d4b51769f937e7c70c622dd76c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e89bf8beedbfb4b6e893bf348c177411e951d58b2fa7b9b6cb1ab55522dbc0f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70181a1b3666fdc5c4341750483730d9320231d142476db4edbc7f8ac392ba27)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntent]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d81beaf08c38b52ba30e8e529388402d431c22ea3bfc15e015dd945a8f082c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseLastTestResultList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99a70956a452d0c1bd7c23fba551faa2293db20b494ef1db11c19eb65729c78e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxTestCaseLastTestResultOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f35cd66b28b145a107a9b73208e3e16ad269a1fdc579ca92e1f796ef1bfcfb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxTestCaseLastTestResultOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e5c899e352705d7ae65d3e264fae5d7fa4ce35006fc4ea91fbf79df536a475d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7954563252f796202352bd736636e60d8db70255dc3fa63651996462b36106bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__277173a3202907367d4fc43919492aba3397abf1607fbd4ceeb90253e1f3d64e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseLastTestResultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseLastTestResultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1e124c1630ff4753b0d693612a160d6957d9865da0129774736bf8add1777a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conversationTurns")
    def conversation_turns(
        self,
    ) -> GoogleDialogflowCxTestCaseLastTestResultConversationTurnsList:
        return typing.cast(GoogleDialogflowCxTestCaseLastTestResultConversationTurnsList, jsii.get(self, "conversationTurns"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="testResult")
    def test_result(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "testResult"))

    @builtins.property
    @jsii.member(jsii_name="testTime")
    def test_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "testTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseLastTestResult]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseLastTestResult], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResult],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f8e99c5c6bf7c5d12f9fa15bd31e60813b1f79b102eb8075ed7a8edb18f9012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurns",
    jsii_struct_bases=[],
    name_mapping={
        "user_input": "userInput",
        "virtual_agent_output": "virtualAgentOutput",
    },
)
class GoogleDialogflowCxTestCaseTestCaseConversationTurns:
    def __init__(
        self,
        *,
        user_input: typing.Optional[typing.Union["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInput", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_agent_output: typing.Optional[typing.Union["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param user_input: user_input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#user_input GoogleDialogflowCxTestCase#user_input}
        :param virtual_agent_output: virtual_agent_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#virtual_agent_output GoogleDialogflowCxTestCase#virtual_agent_output}
        '''
        if isinstance(user_input, dict):
            user_input = GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInput(**user_input)
        if isinstance(virtual_agent_output, dict):
            virtual_agent_output = GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput(**virtual_agent_output)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5281fe2a8b0d4d8d31629b2583e869d89800c3e560ea561be28bd9cff7e606f2)
            check_type(argname="argument user_input", value=user_input, expected_type=type_hints["user_input"])
            check_type(argname="argument virtual_agent_output", value=virtual_agent_output, expected_type=type_hints["virtual_agent_output"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if user_input is not None:
            self._values["user_input"] = user_input
        if virtual_agent_output is not None:
            self._values["virtual_agent_output"] = virtual_agent_output

    @builtins.property
    def user_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInput"]:
        '''user_input block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#user_input GoogleDialogflowCxTestCase#user_input}
        '''
        result = self._values.get("user_input")
        return typing.cast(typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInput"], result)

    @builtins.property
    def virtual_agent_output(
        self,
    ) -> typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput"]:
        '''virtual_agent_output block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#virtual_agent_output GoogleDialogflowCxTestCase#virtual_agent_output}
        '''
        result = self._values.get("virtual_agent_output")
        return typing.cast(typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseTestCaseConversationTurns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseTestCaseConversationTurnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dd6efa1fdf3c11e6dc1943edf8955dd38914ff320f6503e9292b2fc666ad3d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxTestCaseTestCaseConversationTurnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51a8fb3a72b99ac100062c6d09d62689cffff874590f9c44b7839f287190e30b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxTestCaseTestCaseConversationTurnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e47dfad2f5236af05ec24a4f14a1ee3ac5a03ee20908245a30ac183109e8469)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2028f7022a74b60e3c2618be10cfab1a9aaac0ff14e2bf310a03ffcc9df0ea00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59139c5dcfa4578d4bf9a4dcea385279b40d5df551aa0304d5fef09faa6e069e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxTestCaseTestCaseConversationTurns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxTestCaseTestCaseConversationTurns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxTestCaseTestCaseConversationTurns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c84f45b86e2efdff28497813652cd2067315d3315fc48aee856775587721f73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseTestCaseConversationTurnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7afb4f9b07ec2f091fcdf3590cdcdc8c633b201f67181e3e89c1cb0f2b1b3090)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putUserInput")
    def put_user_input(
        self,
        *,
        enable_sentiment_analysis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        injected_parameters: typing.Optional[builtins.str] = None,
        input: typing.Optional[typing.Union["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInput", typing.Dict[builtins.str, typing.Any]]] = None,
        is_webhook_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_sentiment_analysis: Whether sentiment analysis is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#enable_sentiment_analysis GoogleDialogflowCxTestCase#enable_sentiment_analysis}
        :param injected_parameters: Parameters that need to be injected into the conversation during intent detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#injected_parameters GoogleDialogflowCxTestCase#injected_parameters}
        :param input: input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#input GoogleDialogflowCxTestCase#input}
        :param is_webhook_enabled: If webhooks should be allowed to trigger in response to the user utterance. Often if parameters are injected, webhooks should not be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#is_webhook_enabled GoogleDialogflowCxTestCase#is_webhook_enabled}
        '''
        value = GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInput(
            enable_sentiment_analysis=enable_sentiment_analysis,
            injected_parameters=injected_parameters,
            input=input,
            is_webhook_enabled=is_webhook_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putUserInput", [value]))

    @jsii.member(jsii_name="putVirtualAgentOutput")
    def put_virtual_agent_output(
        self,
        *,
        current_page: typing.Optional[typing.Union["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage", typing.Dict[builtins.str, typing.Any]]] = None,
        session_parameters: typing.Optional[builtins.str] = None,
        text_responses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses", typing.Dict[builtins.str, typing.Any]]]]] = None,
        triggered_intent: typing.Optional[typing.Union["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param current_page: current_page block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#current_page GoogleDialogflowCxTestCase#current_page}
        :param session_parameters: The session parameters available to the bot at this point. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#session_parameters GoogleDialogflowCxTestCase#session_parameters}
        :param text_responses: text_responses block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#text_responses GoogleDialogflowCxTestCase#text_responses}
        :param triggered_intent: triggered_intent block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#triggered_intent GoogleDialogflowCxTestCase#triggered_intent}
        '''
        value = GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput(
            current_page=current_page,
            session_parameters=session_parameters,
            text_responses=text_responses,
            triggered_intent=triggered_intent,
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualAgentOutput", [value]))

    @jsii.member(jsii_name="resetUserInput")
    def reset_user_input(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserInput", []))

    @jsii.member(jsii_name="resetVirtualAgentOutput")
    def reset_virtual_agent_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualAgentOutput", []))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(
        self,
    ) -> "GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputOutputReference":
        return typing.cast("GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputOutputReference", jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualAgentOutput")
    def virtual_agent_output(
        self,
    ) -> "GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputOutputReference":
        return typing.cast("GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputOutputReference", jsii.get(self, "virtualAgentOutput"))

    @builtins.property
    @jsii.member(jsii_name="userInputInput")
    def user_input_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInput"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInput"], jsii.get(self, "userInputInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualAgentOutputInput")
    def virtual_agent_output_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput"], jsii.get(self, "virtualAgentOutputInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxTestCaseTestCaseConversationTurns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxTestCaseTestCaseConversationTurns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxTestCaseTestCaseConversationTurns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82214712acba37ac1dc675ee71b15793abb6dc9fe9a48f200bf83a38d9e80307)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInput",
    jsii_struct_bases=[],
    name_mapping={
        "enable_sentiment_analysis": "enableSentimentAnalysis",
        "injected_parameters": "injectedParameters",
        "input": "input",
        "is_webhook_enabled": "isWebhookEnabled",
    },
)
class GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInput:
    def __init__(
        self,
        *,
        enable_sentiment_analysis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        injected_parameters: typing.Optional[builtins.str] = None,
        input: typing.Optional[typing.Union["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInput", typing.Dict[builtins.str, typing.Any]]] = None,
        is_webhook_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_sentiment_analysis: Whether sentiment analysis is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#enable_sentiment_analysis GoogleDialogflowCxTestCase#enable_sentiment_analysis}
        :param injected_parameters: Parameters that need to be injected into the conversation during intent detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#injected_parameters GoogleDialogflowCxTestCase#injected_parameters}
        :param input: input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#input GoogleDialogflowCxTestCase#input}
        :param is_webhook_enabled: If webhooks should be allowed to trigger in response to the user utterance. Often if parameters are injected, webhooks should not be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#is_webhook_enabled GoogleDialogflowCxTestCase#is_webhook_enabled}
        '''
        if isinstance(input, dict):
            input = GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInput(**input)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d76cfcff4e2768f59a9a0e530c31dfe78acb1f1ca07e5e84b0962eed7fadb2)
            check_type(argname="argument enable_sentiment_analysis", value=enable_sentiment_analysis, expected_type=type_hints["enable_sentiment_analysis"])
            check_type(argname="argument injected_parameters", value=injected_parameters, expected_type=type_hints["injected_parameters"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument is_webhook_enabled", value=is_webhook_enabled, expected_type=type_hints["is_webhook_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_sentiment_analysis is not None:
            self._values["enable_sentiment_analysis"] = enable_sentiment_analysis
        if injected_parameters is not None:
            self._values["injected_parameters"] = injected_parameters
        if input is not None:
            self._values["input"] = input
        if is_webhook_enabled is not None:
            self._values["is_webhook_enabled"] = is_webhook_enabled

    @builtins.property
    def enable_sentiment_analysis(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether sentiment analysis is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#enable_sentiment_analysis GoogleDialogflowCxTestCase#enable_sentiment_analysis}
        '''
        result = self._values.get("enable_sentiment_analysis")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def injected_parameters(self) -> typing.Optional[builtins.str]:
        '''Parameters that need to be injected into the conversation during intent detection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#injected_parameters GoogleDialogflowCxTestCase#injected_parameters}
        '''
        result = self._values.get("injected_parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInput"]:
        '''input block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#input GoogleDialogflowCxTestCase#input}
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInput"], result)

    @builtins.property
    def is_webhook_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If webhooks should be allowed to trigger in response to the user utterance.

        Often if parameters are injected, webhooks should not be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#is_webhook_enabled GoogleDialogflowCxTestCase#is_webhook_enabled}
        '''
        result = self._values.get("is_webhook_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInput",
    jsii_struct_bases=[],
    name_mapping={
        "dtmf": "dtmf",
        "event": "event",
        "language_code": "languageCode",
        "text": "text",
    },
)
class GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInput:
    def __init__(
        self,
        *,
        dtmf: typing.Optional[typing.Union["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf", typing.Dict[builtins.str, typing.Any]]] = None,
        event: typing.Optional[typing.Union["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent", typing.Dict[builtins.str, typing.Any]]] = None,
        language_code: typing.Optional[builtins.str] = None,
        text: typing.Optional[typing.Union["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dtmf: dtmf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#dtmf GoogleDialogflowCxTestCase#dtmf}
        :param event: event block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#event GoogleDialogflowCxTestCase#event}
        :param language_code: The language of the input. See `Language Support <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ for a list of the currently supported language codes. Note that queries in the same session do not necessarily need to specify the same language. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#language_code GoogleDialogflowCxTestCase#language_code}
        :param text: text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#text GoogleDialogflowCxTestCase#text}
        '''
        if isinstance(dtmf, dict):
            dtmf = GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf(**dtmf)
        if isinstance(event, dict):
            event = GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent(**event)
        if isinstance(text, dict):
            text = GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText(**text)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c011468d30dbb19a8f902382df96b24bc240cd875b0e2204bf810be362a4fa)
            check_type(argname="argument dtmf", value=dtmf, expected_type=type_hints["dtmf"])
            check_type(argname="argument event", value=event, expected_type=type_hints["event"])
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dtmf is not None:
            self._values["dtmf"] = dtmf
        if event is not None:
            self._values["event"] = event
        if language_code is not None:
            self._values["language_code"] = language_code
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def dtmf(
        self,
    ) -> typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf"]:
        '''dtmf block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#dtmf GoogleDialogflowCxTestCase#dtmf}
        '''
        result = self._values.get("dtmf")
        return typing.cast(typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf"], result)

    @builtins.property
    def event(
        self,
    ) -> typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent"]:
        '''event block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#event GoogleDialogflowCxTestCase#event}
        '''
        result = self._values.get("event")
        return typing.cast(typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent"], result)

    @builtins.property
    def language_code(self) -> typing.Optional[builtins.str]:
        '''The language of the input.

        See `Language Support <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ for a list of the currently supported language codes.
        Note that queries in the same session do not necessarily need to specify the same language.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#language_code GoogleDialogflowCxTestCase#language_code}
        '''
        result = self._values.get("language_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def text(
        self,
    ) -> typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText"]:
        '''text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#text GoogleDialogflowCxTestCase#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf",
    jsii_struct_bases=[],
    name_mapping={"digits": "digits", "finish_digit": "finishDigit"},
)
class GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf:
    def __init__(
        self,
        *,
        digits: typing.Optional[builtins.str] = None,
        finish_digit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param digits: The dtmf digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#digits GoogleDialogflowCxTestCase#digits}
        :param finish_digit: The finish digit (if any). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#finish_digit GoogleDialogflowCxTestCase#finish_digit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0c50c842fb24ad8534ebecefcbd01dede6b76e927052b7efd8ba16064cb006)
            check_type(argname="argument digits", value=digits, expected_type=type_hints["digits"])
            check_type(argname="argument finish_digit", value=finish_digit, expected_type=type_hints["finish_digit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if digits is not None:
            self._values["digits"] = digits
        if finish_digit is not None:
            self._values["finish_digit"] = finish_digit

    @builtins.property
    def digits(self) -> typing.Optional[builtins.str]:
        '''The dtmf digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#digits GoogleDialogflowCxTestCase#digits}
        '''
        result = self._values.get("digits")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def finish_digit(self) -> typing.Optional[builtins.str]:
        '''The finish digit (if any).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#finish_digit GoogleDialogflowCxTestCase#finish_digit}
        '''
        result = self._values.get("finish_digit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmfOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmfOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6689d257ffbde5eaa1c3dc3d25ebc473c7c34bac90d6689582885e06cd693b61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDigits")
    def reset_digits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDigits", []))

    @jsii.member(jsii_name="resetFinishDigit")
    def reset_finish_digit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFinishDigit", []))

    @builtins.property
    @jsii.member(jsii_name="digitsInput")
    def digits_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "digitsInput"))

    @builtins.property
    @jsii.member(jsii_name="finishDigitInput")
    def finish_digit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "finishDigitInput"))

    @builtins.property
    @jsii.member(jsii_name="digits")
    def digits(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "digits"))

    @digits.setter
    def digits(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab74ee44b25d282ba183b017021a00bcdf070a987d927f6deda40d7f80eaada4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "digits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="finishDigit")
    def finish_digit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "finishDigit"))

    @finish_digit.setter
    def finish_digit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a456e34be6ef7c26daeb4da877cadc89161c318368896623b7acc50846bbf682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "finishDigit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c17e3dc6779bb09c11fd15a49edd69fcf1f01aeb0fa5b1057ae3e55c9c4779a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent",
    jsii_struct_bases=[],
    name_mapping={"event": "event"},
)
class GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent:
    def __init__(self, *, event: builtins.str) -> None:
        '''
        :param event: Name of the event. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#event GoogleDialogflowCxTestCase#event}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a8ba077fcb2ab08e8cf32f93a14427e049fed29e4ae26dcd65b3b81e9dc1a3e)
            check_type(argname="argument event", value=event, expected_type=type_hints["event"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event": event,
        }

    @builtins.property
    def event(self) -> builtins.str:
        '''Name of the event.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#event GoogleDialogflowCxTestCase#event}
        '''
        result = self._values.get("event")
        assert result is not None, "Required property 'event' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEventOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEventOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c71652c734754ad8ae2226284e4c41657a0d4b64bba9c4854a8565265b8a049f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="eventInput")
    def event_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventInput"))

    @builtins.property
    @jsii.member(jsii_name="event")
    def event(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "event"))

    @event.setter
    def event(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acc38075e3a0ed02cbde5e1ba2130fc38b3c8a57855ba0c01b107a996e76ef60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "event", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af9240a7678c97945b4d00943e8e62264bd4b791601acff8fc5f04b69e8bda3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58360ee24ff5cf8e7357472250ad896cf7c5eecce99412db7e893108e15c428d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDtmf")
    def put_dtmf(
        self,
        *,
        digits: typing.Optional[builtins.str] = None,
        finish_digit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param digits: The dtmf digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#digits GoogleDialogflowCxTestCase#digits}
        :param finish_digit: The finish digit (if any). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#finish_digit GoogleDialogflowCxTestCase#finish_digit}
        '''
        value = GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf(
            digits=digits, finish_digit=finish_digit
        )

        return typing.cast(None, jsii.invoke(self, "putDtmf", [value]))

    @jsii.member(jsii_name="putEvent")
    def put_event(self, *, event: builtins.str) -> None:
        '''
        :param event: Name of the event. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#event GoogleDialogflowCxTestCase#event}
        '''
        value = GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent(
            event=event
        )

        return typing.cast(None, jsii.invoke(self, "putEvent", [value]))

    @jsii.member(jsii_name="putText")
    def put_text(self, *, text: builtins.str) -> None:
        '''
        :param text: The natural language text to be processed. Text length must not exceed 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#text GoogleDialogflowCxTestCase#text}
        '''
        value = GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText(
            text=text
        )

        return typing.cast(None, jsii.invoke(self, "putText", [value]))

    @jsii.member(jsii_name="resetDtmf")
    def reset_dtmf(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDtmf", []))

    @jsii.member(jsii_name="resetEvent")
    def reset_event(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvent", []))

    @jsii.member(jsii_name="resetLanguageCode")
    def reset_language_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguageCode", []))

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="dtmf")
    def dtmf(
        self,
    ) -> GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmfOutputReference:
        return typing.cast(GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmfOutputReference, jsii.get(self, "dtmf"))

    @builtins.property
    @jsii.member(jsii_name="event")
    def event(
        self,
    ) -> GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEventOutputReference:
        return typing.cast(GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEventOutputReference, jsii.get(self, "event"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(
        self,
    ) -> "GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputTextOutputReference":
        return typing.cast("GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputTextOutputReference", jsii.get(self, "text"))

    @builtins.property
    @jsii.member(jsii_name="dtmfInput")
    def dtmf_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf], jsii.get(self, "dtmfInput"))

    @builtins.property
    @jsii.member(jsii_name="eventInput")
    def event_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent], jsii.get(self, "eventInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText"], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b1be76e83e43f3bf0f98ef75c78351c611e3dfbf523348f156eb988f9a5ac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInput]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c0de08c8fc9e8bf4d20afe43e670f857407e7020b357ea6ff90892a308f9884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText",
    jsii_struct_bases=[],
    name_mapping={"text": "text"},
)
class GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText:
    def __init__(self, *, text: builtins.str) -> None:
        '''
        :param text: The natural language text to be processed. Text length must not exceed 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#text GoogleDialogflowCxTestCase#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9d5495d28a820f21eb289d501cb44ffaf3fc7cc44454025da696bac46a5ccc1)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "text": text,
        }

    @builtins.property
    def text(self) -> builtins.str:
        '''The natural language text to be processed. Text length must not exceed 256 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#text GoogleDialogflowCxTestCase#text}
        '''
        result = self._values.get("text")
        assert result is not None, "Required property 'text' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bce603baea17dfa33957dad864436c48c21930415b11f57011113f01cf78526)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de94a831a90dbc6d2491bba0d66e85261e84a18c70927bd9ee34118605660c5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__794a439ce2f9fb66a72686709cedbd8656a8fdd0bf445261b0bae6ab4472db36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e57a6e4073390de8688cf129bd1a25c061f0d058656f319ccfea08ad09387db7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInput")
    def put_input(
        self,
        *,
        dtmf: typing.Optional[typing.Union[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf, typing.Dict[builtins.str, typing.Any]]] = None,
        event: typing.Optional[typing.Union[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent, typing.Dict[builtins.str, typing.Any]]] = None,
        language_code: typing.Optional[builtins.str] = None,
        text: typing.Optional[typing.Union[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dtmf: dtmf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#dtmf GoogleDialogflowCxTestCase#dtmf}
        :param event: event block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#event GoogleDialogflowCxTestCase#event}
        :param language_code: The language of the input. See `Language Support <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ for a list of the currently supported language codes. Note that queries in the same session do not necessarily need to specify the same language. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#language_code GoogleDialogflowCxTestCase#language_code}
        :param text: text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#text GoogleDialogflowCxTestCase#text}
        '''
        value = GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInput(
            dtmf=dtmf, event=event, language_code=language_code, text=text
        )

        return typing.cast(None, jsii.invoke(self, "putInput", [value]))

    @jsii.member(jsii_name="resetEnableSentimentAnalysis")
    def reset_enable_sentiment_analysis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSentimentAnalysis", []))

    @jsii.member(jsii_name="resetInjectedParameters")
    def reset_injected_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInjectedParameters", []))

    @jsii.member(jsii_name="resetInput")
    def reset_input(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInput", []))

    @jsii.member(jsii_name="resetIsWebhookEnabled")
    def reset_is_webhook_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsWebhookEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="input")
    def input(
        self,
    ) -> GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputOutputReference:
        return typing.cast(GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputOutputReference, jsii.get(self, "input"))

    @builtins.property
    @jsii.member(jsii_name="enableSentimentAnalysisInput")
    def enable_sentiment_analysis_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSentimentAnalysisInput"))

    @builtins.property
    @jsii.member(jsii_name="injectedParametersInput")
    def injected_parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "injectedParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="inputInput")
    def input_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInput]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInput], jsii.get(self, "inputInput"))

    @builtins.property
    @jsii.member(jsii_name="isWebhookEnabledInput")
    def is_webhook_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isWebhookEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSentimentAnalysis")
    def enable_sentiment_analysis(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSentimentAnalysis"))

    @enable_sentiment_analysis.setter
    def enable_sentiment_analysis(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd442886b2b5ea38ec2d87a9c64cadfc589117c85e3472fb2119bc08c4e2ffb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSentimentAnalysis", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="injectedParameters")
    def injected_parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "injectedParameters"))

    @injected_parameters.setter
    def injected_parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9053ce53de50a52f0be6cfcdca705e1d51b4cc660b4ded925d229a31fdd32926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "injectedParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isWebhookEnabled")
    def is_webhook_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isWebhookEnabled"))

    @is_webhook_enabled.setter
    def is_webhook_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14fe1620f62ba677966a16883eb65c78502296c44da8c64fabab3e2dd6a88856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isWebhookEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInput]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__152a5021c3183001814c69a26a6b3c825ddfebfa5be2d4023fc1d540145f5ff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput",
    jsii_struct_bases=[],
    name_mapping={
        "current_page": "currentPage",
        "session_parameters": "sessionParameters",
        "text_responses": "textResponses",
        "triggered_intent": "triggeredIntent",
    },
)
class GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput:
    def __init__(
        self,
        *,
        current_page: typing.Optional[typing.Union["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage", typing.Dict[builtins.str, typing.Any]]] = None,
        session_parameters: typing.Optional[builtins.str] = None,
        text_responses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses", typing.Dict[builtins.str, typing.Any]]]]] = None,
        triggered_intent: typing.Optional[typing.Union["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param current_page: current_page block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#current_page GoogleDialogflowCxTestCase#current_page}
        :param session_parameters: The session parameters available to the bot at this point. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#session_parameters GoogleDialogflowCxTestCase#session_parameters}
        :param text_responses: text_responses block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#text_responses GoogleDialogflowCxTestCase#text_responses}
        :param triggered_intent: triggered_intent block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#triggered_intent GoogleDialogflowCxTestCase#triggered_intent}
        '''
        if isinstance(current_page, dict):
            current_page = GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage(**current_page)
        if isinstance(triggered_intent, dict):
            triggered_intent = GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent(**triggered_intent)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b24daa2156a0dcb6f252e4329bb23a21f1c51c957bdf75e7bf8bff312d201f0)
            check_type(argname="argument current_page", value=current_page, expected_type=type_hints["current_page"])
            check_type(argname="argument session_parameters", value=session_parameters, expected_type=type_hints["session_parameters"])
            check_type(argname="argument text_responses", value=text_responses, expected_type=type_hints["text_responses"])
            check_type(argname="argument triggered_intent", value=triggered_intent, expected_type=type_hints["triggered_intent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if current_page is not None:
            self._values["current_page"] = current_page
        if session_parameters is not None:
            self._values["session_parameters"] = session_parameters
        if text_responses is not None:
            self._values["text_responses"] = text_responses
        if triggered_intent is not None:
            self._values["triggered_intent"] = triggered_intent

    @builtins.property
    def current_page(
        self,
    ) -> typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage"]:
        '''current_page block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#current_page GoogleDialogflowCxTestCase#current_page}
        '''
        result = self._values.get("current_page")
        return typing.cast(typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage"], result)

    @builtins.property
    def session_parameters(self) -> typing.Optional[builtins.str]:
        '''The session parameters available to the bot at this point.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#session_parameters GoogleDialogflowCxTestCase#session_parameters}
        '''
        result = self._values.get("session_parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def text_responses(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses"]]]:
        '''text_responses block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#text_responses GoogleDialogflowCxTestCase#text_responses}
        '''
        result = self._values.get("text_responses")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses"]]], result)

    @builtins.property
    def triggered_intent(
        self,
    ) -> typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent"]:
        '''triggered_intent block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#triggered_intent GoogleDialogflowCxTestCase#triggered_intent}
        '''
        result = self._values.get("triggered_intent")
        return typing.cast(typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: The unique identifier of the page. Format: projects//locations//agents//flows//pages/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#name GoogleDialogflowCxTestCase#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bac2885c51d2c7cabd6a37b2ed7b0ffc21e5e004e2d672486f6135a2c67c9aa)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the page. Format: projects//locations//agents//flows//pages/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#name GoogleDialogflowCxTestCase#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__457b5fe85285e07336d27bb408d09e3741173ea2c5a270a934236371687a1f09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e2128ea4d85c3aa4da8875bfc010dcdccfc9eb16ea4c230c5a0ce5e52ac65ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c03319ed20af0f9b3b98dcef470e6de802727a7c732f011c5c038ca797fa9e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4a642666f8b9812682829767b1a4e8483afb8cede12b69e4b63cd4f45b9a41e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCurrentPage")
    def put_current_page(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: The unique identifier of the page. Format: projects//locations//agents//flows//pages/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#name GoogleDialogflowCxTestCase#name}
        '''
        value = GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putCurrentPage", [value]))

    @jsii.member(jsii_name="putTextResponses")
    def put_text_responses(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4df3137e46beaeca720722f9a1c67b3a8e824cbd1ffeaea61c6d56ec460d493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTextResponses", [value]))

    @jsii.member(jsii_name="putTriggeredIntent")
    def put_triggered_intent(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The unique identifier of the intent. Format: projects//locations//agents//intents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#name GoogleDialogflowCxTestCase#name}
        '''
        value = GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putTriggeredIntent", [value]))

    @jsii.member(jsii_name="resetCurrentPage")
    def reset_current_page(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCurrentPage", []))

    @jsii.member(jsii_name="resetSessionParameters")
    def reset_session_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionParameters", []))

    @jsii.member(jsii_name="resetTextResponses")
    def reset_text_responses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTextResponses", []))

    @jsii.member(jsii_name="resetTriggeredIntent")
    def reset_triggered_intent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggeredIntent", []))

    @builtins.property
    @jsii.member(jsii_name="currentPage")
    def current_page(
        self,
    ) -> GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPageOutputReference:
        return typing.cast(GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPageOutputReference, jsii.get(self, "currentPage"))

    @builtins.property
    @jsii.member(jsii_name="textResponses")
    def text_responses(
        self,
    ) -> "GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesList":
        return typing.cast("GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesList", jsii.get(self, "textResponses"))

    @builtins.property
    @jsii.member(jsii_name="triggeredIntent")
    def triggered_intent(
        self,
    ) -> "GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference":
        return typing.cast("GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference", jsii.get(self, "triggeredIntent"))

    @builtins.property
    @jsii.member(jsii_name="currentPageInput")
    def current_page_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage], jsii.get(self, "currentPageInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionParametersInput")
    def session_parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="textResponsesInput")
    def text_responses_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses"]]], jsii.get(self, "textResponsesInput"))

    @builtins.property
    @jsii.member(jsii_name="triggeredIntentInput")
    def triggered_intent_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent"], jsii.get(self, "triggeredIntentInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionParameters")
    def session_parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionParameters"))

    @session_parameters.setter
    def session_parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8babea4bce0716034ffc23cd747b9ebc88a8ddc0da52e29f536cca4ea610982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e35d65993836454d665c682f73d89e6e9100e53a0a0e55d1485990b623fedf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses",
    jsii_struct_bases=[],
    name_mapping={"text": "text"},
)
class GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses:
    def __init__(
        self,
        *,
        text: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param text: A collection of text responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#text GoogleDialogflowCxTestCase#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f059c0118478eb3ea390687c80db3f9645900790d85da84185883a9a01cfbc79)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def text(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A collection of text responses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#text GoogleDialogflowCxTestCase#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3379f3b75d248975a79fe905b0c26593c4d44dbccc22cf888e16c64b81ce3317)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4cf699f27e00f6865cc00eff3ca1e382b6c68b3ddb30b47ceeac221847d9b2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ec33e89f4024f458572c946dd8b80a221c50ccde7b46b405307c621589903b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ddd73a0d889b59c8b05a1446e34fb339a41391864cd20a2ee9e73a86d88117c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f83b75d38c07810753d62e69566fd0fa7e13fc65fa60f6c0a38a6ac8da5a9381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9cf6129fdda704746db89e7b2549b306f6bd46c2feeac088dc1602069b7fedf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5786eb02d15db992a19eb8be594feb5e8997b17a5de1ddfb131fe588de28e336)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "text"))

    @text.setter
    def text(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31d1a9365227e7335c3d429e365fd5d439e00264ed2f72078e48f2ad6f01178f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__118cc2a4701b35833f5a3db2f5df44590baa74dc5098144ef219880d017b79b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: The unique identifier of the intent. Format: projects//locations//agents//intents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#name GoogleDialogflowCxTestCase#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b9d58a7e0902f782870b68a22d395bf92a2acc692496f47bc14ca0368ed0af)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the intent. Format: projects//locations//agents//intents/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#name GoogleDialogflowCxTestCase#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d778e2dde355d2350df4e9361859bc0c67410a6ce629bb948d3f05d549a63ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__47f3c2e6f7547fd597e790299535890616eaab204e180c11f795b81781f7451f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288e28d2595ad165859f6109a8b435e1c2678a8b13306e70e234d09c1fc8d09d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestConfig",
    jsii_struct_bases=[],
    name_mapping={
        "flow": "flow",
        "page": "page",
        "tracking_parameters": "trackingParameters",
    },
)
class GoogleDialogflowCxTestCaseTestConfig:
    def __init__(
        self,
        *,
        flow: typing.Optional[builtins.str] = None,
        page: typing.Optional[builtins.str] = None,
        tracking_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param flow: Flow name to start the test case with. Format: projects//locations//agents//flows/. Only one of flow and page should be set to indicate the starting point of the test case. If neither is set, the test case will start with start page on the default start flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#flow GoogleDialogflowCxTestCase#flow}
        :param page: The page to start the test case with. Format: projects//locations//agents//flows//pages/. Only one of flow and page should be set to indicate the starting point of the test case. If neither is set, the test case will start with start page on the default start flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#page GoogleDialogflowCxTestCase#page}
        :param tracking_parameters: Session parameters to be compared when calculating differences. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#tracking_parameters GoogleDialogflowCxTestCase#tracking_parameters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf066508b24d3a5fcd800df0a595de5ad0215189376459962989c3f485d8517d)
            check_type(argname="argument flow", value=flow, expected_type=type_hints["flow"])
            check_type(argname="argument page", value=page, expected_type=type_hints["page"])
            check_type(argname="argument tracking_parameters", value=tracking_parameters, expected_type=type_hints["tracking_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if flow is not None:
            self._values["flow"] = flow
        if page is not None:
            self._values["page"] = page
        if tracking_parameters is not None:
            self._values["tracking_parameters"] = tracking_parameters

    @builtins.property
    def flow(self) -> typing.Optional[builtins.str]:
        '''Flow name to start the test case with.

        Format: projects//locations//agents//flows/.
        Only one of flow and page should be set to indicate the starting point of the test case. If neither is set, the test case will start with start page on the default start flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#flow GoogleDialogflowCxTestCase#flow}
        '''
        result = self._values.get("flow")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def page(self) -> typing.Optional[builtins.str]:
        '''The page to start the test case with.

        Format: projects//locations//agents//flows//pages/.
        Only one of flow and page should be set to indicate the starting point of the test case. If neither is set, the test case will start with start page on the default start flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#page GoogleDialogflowCxTestCase#page}
        '''
        result = self._values.get("page")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tracking_parameters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Session parameters to be compared when calculating differences.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#tracking_parameters GoogleDialogflowCxTestCase#tracking_parameters}
        '''
        result = self._values.get("tracking_parameters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseTestConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseTestConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTestConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38b4d65936355ee9c7d479d89c79d9d68e033be6957ae08009ed252f07451ab8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFlow")
    def reset_flow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlow", []))

    @jsii.member(jsii_name="resetPage")
    def reset_page(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPage", []))

    @jsii.member(jsii_name="resetTrackingParameters")
    def reset_tracking_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrackingParameters", []))

    @builtins.property
    @jsii.member(jsii_name="flowInput")
    def flow_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flowInput"))

    @builtins.property
    @jsii.member(jsii_name="pageInput")
    def page_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pageInput"))

    @builtins.property
    @jsii.member(jsii_name="trackingParametersInput")
    def tracking_parameters_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "trackingParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="flow")
    def flow(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flow"))

    @flow.setter
    def flow(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e472f48d09e230ed66ee3a35e77b871700dda26f8855666efbfcedbdf0cd9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="page")
    def page(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "page"))

    @page.setter
    def page(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__231246e6f6cddb6e184dd150d4511c0a734c1552fad7b6c051fe8e1ed018e3ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "page", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trackingParameters")
    def tracking_parameters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trackingParameters"))

    @tracking_parameters.setter
    def tracking_parameters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55928c017d735940dfa70a7738039d39ac47d3f0530e4c2961af956fe2181dc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trackingParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDialogflowCxTestCaseTestConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowCxTestCaseTestConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxTestCaseTestConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d6dd6cf98012ca09a058314bcff56b81577152d89ad23d7e8a90c5c69d52829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDialogflowCxTestCaseTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#create GoogleDialogflowCxTestCase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#delete GoogleDialogflowCxTestCase#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#update GoogleDialogflowCxTestCase#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__078fb25b1b59ce93d88830a6bd300af4f9787b37b543d7308729ccd95c0068cc)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#create GoogleDialogflowCxTestCase#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#delete GoogleDialogflowCxTestCase#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dialogflow_cx_test_case#update GoogleDialogflowCxTestCase#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxTestCaseTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxTestCaseTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTestCase.GoogleDialogflowCxTestCaseTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a49d348cdd8d2866c3847f0206796cfcce0d861441e3159c5ed912c43b57a10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a8ab992a581364a9fec95a21ae1102825a6b51f38d58ba9925987f386e3edfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad21d1f2325d1e66aca612a1096c2de5ef43c9db930420d209f63f1dc2d53f58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__294f14f680ef66569fc085c70075d23cb6cc6bb24b3f22f6bf8bac78527bcd5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxTestCaseTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxTestCaseTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxTestCaseTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efa240545a6f3807d876b558fb146bacdaf035f2dd1c130116a286ae0856d7cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDialogflowCxTestCase",
    "GoogleDialogflowCxTestCaseConfig",
    "GoogleDialogflowCxTestCaseLastTestResult",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurns",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsList",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsOutputReference",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInput",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInput",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmf",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfList",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfOutputReference",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEvent",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventList",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventOutputReference",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputList",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputOutputReference",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputText",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextList",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextOutputReference",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputList",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputOutputReference",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutput",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPage",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageList",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageOutputReference",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferences",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesList",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesOutputReference",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputList",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputOutputReference",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatus",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusList",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusOutputReference",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponses",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesList",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesOutputReference",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntent",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentList",
    "GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference",
    "GoogleDialogflowCxTestCaseLastTestResultList",
    "GoogleDialogflowCxTestCaseLastTestResultOutputReference",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurns",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsList",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsOutputReference",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInput",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInput",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmfOutputReference",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEventOutputReference",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputOutputReference",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputTextOutputReference",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputOutputReference",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPageOutputReference",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputOutputReference",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesList",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesOutputReference",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent",
    "GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference",
    "GoogleDialogflowCxTestCaseTestConfig",
    "GoogleDialogflowCxTestCaseTestConfigOutputReference",
    "GoogleDialogflowCxTestCaseTimeouts",
    "GoogleDialogflowCxTestCaseTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__da570f79b46ef1a1b8db3cf0389449fd5c4b15a174e1dbced6287485eca3635a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    notes: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    test_case_conversation_turns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxTestCaseTestCaseConversationTurns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    test_config: typing.Optional[typing.Union[GoogleDialogflowCxTestCaseTestConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDialogflowCxTestCaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c2ed31b51b1c67f3474f93fa1cb08352dd02f2763f3dd4b1e5ba59a804ea171c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755ecb82aac4f2f7dda9bab2b723cfffecf856f73f4236ce236286f3422f67de(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxTestCaseTestCaseConversationTurns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2edebd5de152ff4ef216154067cddaed3d6b9d6a0d028d67ae9f49a10239da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5ef0aa31ec83ec4be9306636efa3a95cee90131390d909c819d9b1d42e7449(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aaca36b8b606e5ba5fcd17a7eba7ff04e041c30dc139d10432a689c1302a2ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9848d28d79af258f003419dbb5e6f36d303aac653bbeee2dfec1c7e1ba5abc68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd210ddac9d07398b44453fb5de68b3d9923d99edaaf4bd9b42dd288f1755387(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad62f3f0e5f59a28c5437d102c5f3ff3a6dbb2bba5a7eb11a5cabcb89517927e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    notes: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    test_case_conversation_turns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxTestCaseTestCaseConversationTurns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    test_config: typing.Optional[typing.Union[GoogleDialogflowCxTestCaseTestConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDialogflowCxTestCaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af901b28ed2db45b2982b7ea3bff4251f40bab6761e5ee75c30aa6c080e9e52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ba0686ee7e4a003d66409694c01c207531c314870d2e2b125fcf69134986a5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5856b7262dadf8ca111fe210d5942aefcf82cef22f902937832834a1aa525d87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e923a4f66cd6207e6d481e48141c7ff6175c9b7eb25e237df86067ee6225f4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3bc5d6b6c0983ebb6eb325be2b2ff0af9ffc8ddf853f2622b5ffdd92df3344(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a35cd858323179f58a18e11ca1331e71d0b9caf26baa45d1a38a316f584660(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b541b29564954de4db9a9e9c8ecf526662739a0ab64fe6b0901db40edc322a0e(
    value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67e520861bd5776272244a1302c598a5995b9809b4320cfac3d94687c3eb43bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da46ac89245b3e15a96873b756948ddf3c13d1829714f5df14993dbd0b30f6f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9caa163c147f1a563c602e774df8b8645d1813270398ec49fefc8b16c72b8ad2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ddc97e3b4cc1b8ca7fd74098f7ef354e14ced29b6bdcbd53405ec53b1a8f017(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2051b80e16c182cfeded60d0bac6a656ede88f78d8fa758c8f7afec6eff7ca96(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1501881ed01232ba298d3bdb48f9b50283da97d70c35d8daa37f06ad816388(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8088f6f1af596e6131d1442fde734622ef560ace9f6e457496a5d53124db12ba(
    value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmf],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5baf5dafe9c269b5f47a384642552bce6d65ae0a8697dc734242d1cccd741c13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd26af89f9af066732060e43d60ee1891148710eb6ff088c2cc0064c65e6e3d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86485c7181aa253888bff52a54f92e4740b70ad8b2c4cbfb92820fb476ce469f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125b24bd5affee995f65b961812a82f44b4adc074e033721fb6cbd9c005084ac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061a3f94db12b4b02c75f24529a95b717bc5e0fe825156331a9c7e89c820aacb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ae4fc2360ee8204213edc971b2304c9da4041fd3aaf1ac076c06f221094159(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f0c8a0ea81e2acce4505695fc50b8a4b894adaf5b3664804eb6f0d1727e519(
    value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEvent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf85468064d523bc5a907ff5bc7976c3fa9b8881fcab1f01766613373348aa9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc0b06a22bffc301e9d51404c7539fb005fd3b58e2e565706f9a1d16b09cf53(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc21996824b92ab7570bb23ea8c8c9370135c0f727d66196af94953613197cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a36d63a5f34687b5247d903719cfcb1352fcb03547142db694faa1794d38b58(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e78c66d5240ebacf122af97c34780027bbf81c5972451793cd29355d03b32030(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e7c6eb717c1db4f58cb6ebc7f3bb131a81d1f828a8ae5c0ce4dfe4729c2cde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1401bbe3f20b2b6f2acd41f70be0dc09feeb5a2b7df356b17845b44d212082(
    value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e079c5c122f11641468f518a9f113db7f06aa21cee23c57405a16de24b08924(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c708dbb01011f05fbfdeb373b6a45d4d2011bbf063af0945367d5ee3a2f6f22a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2fbcf3f7a21a64fac4c51998105e7a1d1bdb91b1112099c3be13b36b00e66f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__349837529aaa6a1578ad0fe12c241c978aaafd1e6bebac97d8f4a00869d81f90(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62d259219571aa0652606de699b62a9d25da2f960838c1e4d4c0b3af5b2ff76(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0746d7e0fb51319ff8ad013fe84cd96a873bb4f0a12932434451412101b39e46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd6f1d6523e4f5ce56d6954c290366c76d6e3b956c4a346f82abbbb1d81b55e0(
    value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputText],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffbd2f19dc8768516893aca984580b30fa536c626bade176b37e8ff0a4418fd5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e59624dc287ff3d67ad76604872f25ecc257b6f67f3c680ce4baeb58031ccac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028bdb0c626dae25312d02b6bd02c53349dd49348d86d04e90d9eedd0afac78e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530ffeb9031cef8dce53e503edf985dc1f85107240d623820a37ad7fccd4a0b1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0973c815db376207ad6ff364c6bbc34e5cd84bc19042276905c4585bf6332e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3dbe2ee334fec4e5a4f8c778d65397176ca5f943c30725682b1769b19ed6b98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c31d0d4d81b103b9199f2e5c5fadad563691a020031340b3f97aafc9fb7340(
    value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsUserInput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ea77e36f86a8105f901dcfb6773a41e9d27d9d1b81ae0190413ff91546023d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b488b239947450111c5fcef92d80f1ec96ce9a8ca235e6458c6c93fe66b81b8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361918ad28bd0344e63b5628819cdf6dac41990e562c0eb90276efbd8e2457d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1245df19e386baf1f441689068051a85251f9ed2183921f6218926ccb87fb87b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c404e95bc27f17f81ee95b137998eb41b20e6e4eabe08547f9d78979c8f9c778(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d023ee4edfe8c0162f892f01742f12f5f08eb0d47fa8764936b27b0451c47d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b29937648004a4c25b0d3c48402cf92f15beb0b7bcc29315e82b01b4357afa68(
    value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ecc62e62cc6c099b40c47d701108490b89358efd7396ef9f34031f77fcf47b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90717de452171da4b3fc7510824ca436b53e8aeaef44b72f3cac5f48c851543(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b03428bdbb711aac47bcfdb383a0a411db4ce7c295d207a9e40c2cc470d666(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e911158040e948b8c69f0f40a3bf14157671bd8f9708fccaa1692c48df62a4f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be3e6db260583ed0596b5fa1dc7bf363c1df89db18c026486c49ee847e7480b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173bb2624d35fd2af2e909542adae10838c365b0b335fcfffc9548328ede48de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1026223776e46445ce9d151a0b8c6a828e54bd8c2cf95b64180d645cb37bfc(
    value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferences],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10899e88ee80a20e62da5c83d8a6787cab61c61adab7eb6aec8921593b82146(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96bc4ca12b3da8dcc4d60fb168b470b5fa65c34b6204420c1b39033119ac4c40(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5def2ece3ed71bedd2be3e97d9d9f5e1da0c2ffb6b7a283ec254148a1504ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a8da8c8485ee4d7535cfb63a34bacdf77ee0ffc670ea24cceb62398941a5ab(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c64d93e9547856ca7bc57daf4bb2da966b08c11472c14442269ed16857601294(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab59533c3f9e2571005d6992b41728767e30180851051973a2f419dd3a0816b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb13d263ec718c18c6721699feb9035f29308db984a1835b86e1bf1af9b0232(
    value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b4b303c9571092e07016186adb160d7897392282d126a3d0a734b4747552323(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82eaf30c34b807223a4487879a854f46956c2deb2974ad44e7367ed150bb80be(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7175df46018b755c0268886e525eaf3bef40d7e6cd15402ed58ef16425cccd74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c34b6b71007fcc5fc6201015824e0dc22fd6dbd930007e4913c607fbd2614ddc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__094b9e1b1534b893043ec8c7f82a16b0b2b3fd935343430593f92886b6503c10(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcaa02a717a0a42906f4fc9560402a649f2d17fedee0eef4ca6d8474285604f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78fb6166a8e5d6878c92a779f7797ccd157461a231c921f78b2ccd046205e12f(
    value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18f6056004b1a4094babb494b92774bfab42607ee2ca8f39faf8951990074bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6212f4ad0e9a26b8abdb2a93951176cf4182c256940fe4051ba851f1b586b979(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce6cd7982f566ae94847f63898c4b88ef93e958d3e8741ca9c78448e283b7d07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca77952d92aeef8e87541d9a7ab591689b521563d0a4c6d65905d4feb456f0a0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47d576f48ce464056a0181c6bd94b0586451df0af0e8e1cc6a083449db877c3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02919435055c2dbcf520b82120f7219952dee6349f907b8ada61eb9ddaa54a1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a3c4a56631f638d47e979c0bd025387a3ea62915c146eaf1dfe6f454035bc4(
    value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponses],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a2f847661a0d9165d559e31035d2b354ac08f33263384d6af2522f3d12df5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad439560b3f2e313f6fac6e8abbf93a38e2d651f9b45eb135af51bf1c858ba79(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df37b3c723b1d11fd71b15969961d7e405532e6f0c6d54ced2900f4f0dd3d111(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dee1e24d5454c739e0a6916cd54aae76bc5c4d4b51769f937e7c70c622dd76c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e89bf8beedbfb4b6e893bf348c177411e951d58b2fa7b9b6cb1ab55522dbc0f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70181a1b3666fdc5c4341750483730d9320231d142476db4edbc7f8ac392ba27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d81beaf08c38b52ba30e8e529388402d431c22ea3bfc15e015dd945a8f082c4(
    value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a70956a452d0c1bd7c23fba551faa2293db20b494ef1db11c19eb65729c78e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f35cd66b28b145a107a9b73208e3e16ad269a1fdc579ca92e1f796ef1bfcfb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5c899e352705d7ae65d3e264fae5d7fa4ce35006fc4ea91fbf79df536a475d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7954563252f796202352bd736636e60d8db70255dc3fa63651996462b36106bd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__277173a3202907367d4fc43919492aba3397abf1607fbd4ceeb90253e1f3d64e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e124c1630ff4753b0d693612a160d6957d9865da0129774736bf8add1777a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f8e99c5c6bf7c5d12f9fa15bd31e60813b1f79b102eb8075ed7a8edb18f9012(
    value: typing.Optional[GoogleDialogflowCxTestCaseLastTestResult],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5281fe2a8b0d4d8d31629b2583e869d89800c3e560ea561be28bd9cff7e606f2(
    *,
    user_input: typing.Optional[typing.Union[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInput, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_agent_output: typing.Optional[typing.Union[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd6efa1fdf3c11e6dc1943edf8955dd38914ff320f6503e9292b2fc666ad3d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a8fb3a72b99ac100062c6d09d62689cffff874590f9c44b7839f287190e30b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e47dfad2f5236af05ec24a4f14a1ee3ac5a03ee20908245a30ac183109e8469(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2028f7022a74b60e3c2618be10cfab1a9aaac0ff14e2bf310a03ffcc9df0ea00(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59139c5dcfa4578d4bf9a4dcea385279b40d5df551aa0304d5fef09faa6e069e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c84f45b86e2efdff28497813652cd2067315d3315fc48aee856775587721f73(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxTestCaseTestCaseConversationTurns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7afb4f9b07ec2f091fcdf3590cdcdc8c633b201f67181e3e89c1cb0f2b1b3090(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82214712acba37ac1dc675ee71b15793abb6dc9fe9a48f200bf83a38d9e80307(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxTestCaseTestCaseConversationTurns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d76cfcff4e2768f59a9a0e530c31dfe78acb1f1ca07e5e84b0962eed7fadb2(
    *,
    enable_sentiment_analysis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    injected_parameters: typing.Optional[builtins.str] = None,
    input: typing.Optional[typing.Union[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInput, typing.Dict[builtins.str, typing.Any]]] = None,
    is_webhook_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c011468d30dbb19a8f902382df96b24bc240cd875b0e2204bf810be362a4fa(
    *,
    dtmf: typing.Optional[typing.Union[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf, typing.Dict[builtins.str, typing.Any]]] = None,
    event: typing.Optional[typing.Union[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent, typing.Dict[builtins.str, typing.Any]]] = None,
    language_code: typing.Optional[builtins.str] = None,
    text: typing.Optional[typing.Union[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0c50c842fb24ad8534ebecefcbd01dede6b76e927052b7efd8ba16064cb006(
    *,
    digits: typing.Optional[builtins.str] = None,
    finish_digit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6689d257ffbde5eaa1c3dc3d25ebc473c7c34bac90d6689582885e06cd693b61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab74ee44b25d282ba183b017021a00bcdf070a987d927f6deda40d7f80eaada4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a456e34be6ef7c26daeb4da877cadc89161c318368896623b7acc50846bbf682(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c17e3dc6779bb09c11fd15a49edd69fcf1f01aeb0fa5b1057ae3e55c9c4779a(
    value: typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a8ba077fcb2ab08e8cf32f93a14427e049fed29e4ae26dcd65b3b81e9dc1a3e(
    *,
    event: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c71652c734754ad8ae2226284e4c41657a0d4b64bba9c4854a8565265b8a049f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acc38075e3a0ed02cbde5e1ba2130fc38b3c8a57855ba0c01b107a996e76ef60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af9240a7678c97945b4d00943e8e62264bd4b791601acff8fc5f04b69e8bda3(
    value: typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58360ee24ff5cf8e7357472250ad896cf7c5eecce99412db7e893108e15c428d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b1be76e83e43f3bf0f98ef75c78351c611e3dfbf523348f156eb988f9a5ac9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0de08c8fc9e8bf4d20afe43e670f857407e7020b357ea6ff90892a308f9884(
    value: typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d5495d28a820f21eb289d501cb44ffaf3fc7cc44454025da696bac46a5ccc1(
    *,
    text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bce603baea17dfa33957dad864436c48c21930415b11f57011113f01cf78526(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de94a831a90dbc6d2491bba0d66e85261e84a18c70927bd9ee34118605660c5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794a439ce2f9fb66a72686709cedbd8656a8fdd0bf445261b0bae6ab4472db36(
    value: typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e57a6e4073390de8688cf129bd1a25c061f0d058656f319ccfea08ad09387db7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd442886b2b5ea38ec2d87a9c64cadfc589117c85e3472fb2119bc08c4e2ffb5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9053ce53de50a52f0be6cfcdca705e1d51b4cc660b4ded925d229a31fdd32926(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14fe1620f62ba677966a16883eb65c78502296c44da8c64fabab3e2dd6a88856(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152a5021c3183001814c69a26a6b3c825ddfebfa5be2d4023fc1d540145f5ff1(
    value: typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsUserInput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b24daa2156a0dcb6f252e4329bb23a21f1c51c957bdf75e7bf8bff312d201f0(
    *,
    current_page: typing.Optional[typing.Union[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage, typing.Dict[builtins.str, typing.Any]]] = None,
    session_parameters: typing.Optional[builtins.str] = None,
    text_responses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses, typing.Dict[builtins.str, typing.Any]]]]] = None,
    triggered_intent: typing.Optional[typing.Union[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bac2885c51d2c7cabd6a37b2ed7b0ffc21e5e004e2d672486f6135a2c67c9aa(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457b5fe85285e07336d27bb408d09e3741173ea2c5a270a934236371687a1f09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2128ea4d85c3aa4da8875bfc010dcdccfc9eb16ea4c230c5a0ce5e52ac65ec9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c03319ed20af0f9b3b98dcef470e6de802727a7c732f011c5c038ca797fa9e5(
    value: typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a642666f8b9812682829767b1a4e8483afb8cede12b69e4b63cd4f45b9a41e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4df3137e46beaeca720722f9a1c67b3a8e824cbd1ffeaea61c6d56ec460d493(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8babea4bce0716034ffc23cd747b9ebc88a8ddc0da52e29f536cca4ea610982(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e35d65993836454d665c682f73d89e6e9100e53a0a0e55d1485990b623fedf4(
    value: typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f059c0118478eb3ea390687c80db3f9645900790d85da84185883a9a01cfbc79(
    *,
    text: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3379f3b75d248975a79fe905b0c26593c4d44dbccc22cf888e16c64b81ce3317(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4cf699f27e00f6865cc00eff3ca1e382b6c68b3ddb30b47ceeac221847d9b2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ec33e89f4024f458572c946dd8b80a221c50ccde7b46b405307c621589903b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ddd73a0d889b59c8b05a1446e34fb339a41391864cd20a2ee9e73a86d88117c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83b75d38c07810753d62e69566fd0fa7e13fc65fa60f6c0a38a6ac8da5a9381(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9cf6129fdda704746db89e7b2549b306f6bd46c2feeac088dc1602069b7fedf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5786eb02d15db992a19eb8be594feb5e8997b17a5de1ddfb131fe588de28e336(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d1a9365227e7335c3d429e365fd5d439e00264ed2f72078e48f2ad6f01178f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__118cc2a4701b35833f5a3db2f5df44590baa74dc5098144ef219880d017b79b4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b9d58a7e0902f782870b68a22d395bf92a2acc692496f47bc14ca0368ed0af(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d778e2dde355d2350df4e9361859bc0c67410a6ce629bb948d3f05d549a63ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f3c2e6f7547fd597e790299535890616eaab204e180c11f795b81781f7451f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288e28d2595ad165859f6109a8b435e1c2678a8b13306e70e234d09c1fc8d09d(
    value: typing.Optional[GoogleDialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf066508b24d3a5fcd800df0a595de5ad0215189376459962989c3f485d8517d(
    *,
    flow: typing.Optional[builtins.str] = None,
    page: typing.Optional[builtins.str] = None,
    tracking_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b4d65936355ee9c7d479d89c79d9d68e033be6957ae08009ed252f07451ab8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e472f48d09e230ed66ee3a35e77b871700dda26f8855666efbfcedbdf0cd9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__231246e6f6cddb6e184dd150d4511c0a734c1552fad7b6c051fe8e1ed018e3ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55928c017d735940dfa70a7738039d39ac47d3f0530e4c2961af956fe2181dc9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d6dd6cf98012ca09a058314bcff56b81577152d89ad23d7e8a90c5c69d52829(
    value: typing.Optional[GoogleDialogflowCxTestCaseTestConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078fb25b1b59ce93d88830a6bd300af4f9787b37b543d7308729ccd95c0068cc(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a49d348cdd8d2866c3847f0206796cfcce0d861441e3159c5ed912c43b57a10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a8ab992a581364a9fec95a21ae1102825a6b51f38d58ba9925987f386e3edfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad21d1f2325d1e66aca612a1096c2de5ef43c9db930420d209f63f1dc2d53f58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294f14f680ef66569fc085c70075d23cb6cc6bb24b3f22f6bf8bac78527bcd5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa240545a6f3807d876b558fb146bacdaf035f2dd1c130116a286ae0856d7cc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxTestCaseTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `google_dialogflow_cx_test_case`

Refer to the Terraform Registry for docs: [`google_dialogflow_cx_test_case`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case).
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


class DialogflowCxTestCase(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCase",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case google_dialogflow_cx_test_case}.'''

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
        test_case_conversation_turns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxTestCaseTestCaseConversationTurns", typing.Dict[builtins.str, typing.Any]]]]] = None,
        test_config: typing.Optional[typing.Union["DialogflowCxTestCaseTestConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxTestCaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case google_dialogflow_cx_test_case} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The human-readable name of the test case, unique within the agent. Limit of 200 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#display_name DialogflowCxTestCase#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#id DialogflowCxTestCase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notes: Additional freeform notes about the test case. Limit of 400 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#notes DialogflowCxTestCase#notes}
        :param parent: The agent to create the test case for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#parent DialogflowCxTestCase#parent}
        :param tags: Tags are short descriptions that users may apply to test cases for organizational and filtering purposes. Each tag should start with "#" and has a limit of 30 characters Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#tags DialogflowCxTestCase#tags}
        :param test_case_conversation_turns: test_case_conversation_turns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#test_case_conversation_turns DialogflowCxTestCase#test_case_conversation_turns}
        :param test_config: test_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#test_config DialogflowCxTestCase#test_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#timeouts DialogflowCxTestCase#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73eddce12cbd1ddb43734f22d6dfd1875189c24df62c9b9c815a542c285f3a3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DialogflowCxTestCaseConfig(
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
        '''Generates CDKTF code for importing a DialogflowCxTestCase resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DialogflowCxTestCase to import.
        :param import_from_id: The id of the existing DialogflowCxTestCase that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DialogflowCxTestCase to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62745e87f1806084ee560b257b0ba4b53cf2a879b2330b3fe46b54a46be9f4be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTestCaseConversationTurns")
    def put_test_case_conversation_turns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxTestCaseTestCaseConversationTurns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e1ab8476e197c822be7db944a75c33ffc3de8cc9c726dbacba8755d0c82a802)
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
        :param flow: Flow name to start the test case with. Format: projects//locations//agents//flows/. Only one of flow and page should be set to indicate the starting point of the test case. If neither is set, the test case will start with start page on the default start flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#flow DialogflowCxTestCase#flow}
        :param page: The page to start the test case with. Format: projects//locations//agents//flows//pages/. Only one of flow and page should be set to indicate the starting point of the test case. If neither is set, the test case will start with start page on the default start flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#page DialogflowCxTestCase#page}
        :param tracking_parameters: Session parameters to be compared when calculating differences. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#tracking_parameters DialogflowCxTestCase#tracking_parameters}
        '''
        value = DialogflowCxTestCaseTestConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#create DialogflowCxTestCase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#delete DialogflowCxTestCase#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#update DialogflowCxTestCase#update}.
        '''
        value = DialogflowCxTestCaseTimeouts(
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
    def last_test_result(self) -> "DialogflowCxTestCaseLastTestResultList":
        return typing.cast("DialogflowCxTestCaseLastTestResultList", jsii.get(self, "lastTestResult"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="testCaseConversationTurns")
    def test_case_conversation_turns(
        self,
    ) -> "DialogflowCxTestCaseTestCaseConversationTurnsList":
        return typing.cast("DialogflowCxTestCaseTestCaseConversationTurnsList", jsii.get(self, "testCaseConversationTurns"))

    @builtins.property
    @jsii.member(jsii_name="testConfig")
    def test_config(self) -> "DialogflowCxTestCaseTestConfigOutputReference":
        return typing.cast("DialogflowCxTestCaseTestConfigOutputReference", jsii.get(self, "testConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DialogflowCxTestCaseTimeoutsOutputReference":
        return typing.cast("DialogflowCxTestCaseTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxTestCaseTestCaseConversationTurns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxTestCaseTestCaseConversationTurns"]]], jsii.get(self, "testCaseConversationTurnsInput"))

    @builtins.property
    @jsii.member(jsii_name="testConfigInput")
    def test_config_input(self) -> typing.Optional["DialogflowCxTestCaseTestConfig"]:
        return typing.cast(typing.Optional["DialogflowCxTestCaseTestConfig"], jsii.get(self, "testConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowCxTestCaseTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowCxTestCaseTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a02c16306b6801d7497f109dba7162163a70700893103baa1ce4f64d92fab130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7ffb2bfe9edb57eccc62cdf243424bab024dbe7fe8e41b68b3a731eda7fc2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notes")
    def notes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notes"))

    @notes.setter
    def notes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f86b173db27ad7b5aca5e8067d75f4a3138fa58da7232188aa247282ca284216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afaed9b89aa78a398dcba8d8891246b4e7cf214fa52203e4d93556c7790c11d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e910887e8e693212c0b7e2643681755d6bedf09965316f4249c73f727551b4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseConfig",
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
class DialogflowCxTestCaseConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        test_case_conversation_turns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxTestCaseTestCaseConversationTurns", typing.Dict[builtins.str, typing.Any]]]]] = None,
        test_config: typing.Optional[typing.Union["DialogflowCxTestCaseTestConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxTestCaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The human-readable name of the test case, unique within the agent. Limit of 200 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#display_name DialogflowCxTestCase#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#id DialogflowCxTestCase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notes: Additional freeform notes about the test case. Limit of 400 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#notes DialogflowCxTestCase#notes}
        :param parent: The agent to create the test case for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#parent DialogflowCxTestCase#parent}
        :param tags: Tags are short descriptions that users may apply to test cases for organizational and filtering purposes. Each tag should start with "#" and has a limit of 30 characters Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#tags DialogflowCxTestCase#tags}
        :param test_case_conversation_turns: test_case_conversation_turns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#test_case_conversation_turns DialogflowCxTestCase#test_case_conversation_turns}
        :param test_config: test_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#test_config DialogflowCxTestCase#test_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#timeouts DialogflowCxTestCase#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(test_config, dict):
            test_config = DialogflowCxTestCaseTestConfig(**test_config)
        if isinstance(timeouts, dict):
            timeouts = DialogflowCxTestCaseTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bf79737c0a45409096c310a68daf6ffe315136381dfc2e1ec7ce9f7be544f3d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#display_name DialogflowCxTestCase#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#id DialogflowCxTestCase#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notes(self) -> typing.Optional[builtins.str]:
        '''Additional freeform notes about the test case. Limit of 400 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#notes DialogflowCxTestCase#notes}
        '''
        result = self._values.get("notes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''The agent to create the test case for. Format: projects//locations//agents/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#parent DialogflowCxTestCase#parent}
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags are short descriptions that users may apply to test cases for organizational and filtering purposes.

        Each tag should start with "#" and has a limit of 30 characters

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#tags DialogflowCxTestCase#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def test_case_conversation_turns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxTestCaseTestCaseConversationTurns"]]]:
        '''test_case_conversation_turns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#test_case_conversation_turns DialogflowCxTestCase#test_case_conversation_turns}
        '''
        result = self._values.get("test_case_conversation_turns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxTestCaseTestCaseConversationTurns"]]], result)

    @builtins.property
    def test_config(self) -> typing.Optional["DialogflowCxTestCaseTestConfig"]:
        '''test_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#test_config DialogflowCxTestCase#test_config}
        '''
        result = self._values.get("test_config")
        return typing.cast(typing.Optional["DialogflowCxTestCaseTestConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DialogflowCxTestCaseTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#timeouts DialogflowCxTestCase#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DialogflowCxTestCaseTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResult",
    jsii_struct_bases=[],
    name_mapping={},
)
class DialogflowCxTestCaseLastTestResult:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseLastTestResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurns",
    jsii_struct_bases=[],
    name_mapping={},
)
class DialogflowCxTestCaseLastTestResultConversationTurns:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseLastTestResultConversationTurns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseLastTestResultConversationTurnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3b55b3d1aec34f86068ed7396637a474412d0ec172c6df3abfe0bd95c200be0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1906d615e00d51fc3df3f2eb134459a52a9cbce3390e44ce212a6252b4e3cba)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1930aaf7bce4701d701d61c096f6694caa3df3a896591379be910ebbced2501)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52f6aa7eb862187b55ab390b62aca1762eae3d1aa68abefd1c78240ebba1e643)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cd89a470da7e8e7dc2b86eedd81167335bf7e3cce5bf930a62c2d0103d267fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseLastTestResultConversationTurnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c0a7c50a9a5bb746628329e41685be289d98511ee3851bae0411743b8ed76e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(
        self,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputList":
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsUserInputList", jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualAgentOutput")
    def virtual_agent_output(
        self,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputList":
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputList", jsii.get(self, "virtualAgentOutput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurns]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurns],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9162612c13d7cb2ba43a2ea91463735eba3dda3e2a1a7b63cc019b8d0edadc01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsUserInput",
    jsii_struct_bases=[],
    name_mapping={},
)
class DialogflowCxTestCaseLastTestResultConversationTurnsUserInput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseLastTestResultConversationTurnsUserInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInput",
    jsii_struct_bases=[],
    name_mapping={},
)
class DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmf",
    jsii_struct_bases=[],
    name_mapping={},
)
class DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmf:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72a3f099777a61c7308baade45db94026d6980b600a1791b338ec501a99ed86c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adbfeb25df1c4de4f2aedc1bad61417c7e7cfc80808c19e7298bfee307c5bfa1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a915bb42d2798adac83f18e13ca536b0edc83d6f323b1a4ebefa2600a74c6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c760f04f991872ccbec3c84fe9d05b32a6aa8af9b495649da75d6d880639b3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73e480ac3a96e2b1368d21cd28ab581e7f1b6b7ad61a27928b75456e9dc15704)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__388911fd8adae1cae0b0a4c4efdd805ee731d9a173a1c6d67dd001cae74667c7)
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
    ) -> typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmf]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmf], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmf],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce1db591cc4df524f87e89e46a8e3510f20a38bdff7227351d7b0044d12070d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEvent",
    jsii_struct_bases=[],
    name_mapping={},
)
class DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEvent:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEvent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb73266ddb34fa4126720144a81372f6c3f07b31b64edbc23bd3afbbba1cdf3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daca691869caa6f041fb9cfd63fd9d423a0d247606e29914c103b539b774a7bb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d91bec808cf4d2bbb6e035fdffe797d68f3b16e3e5628669cd83bb6789c183d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eadf21e62b022e071ca390d27c21fd58aa260fa38760f11d5fd047f90e66ed78)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89c7fece880f8b6b9da7f11466a0ca982137f22728af6a2499e68067bb165ba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__410d687a74ba311ff68c798875ad750bba842044d630292eddb25bff0f0ab93f)
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
    ) -> typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEvent]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEvent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEvent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f7ee7fdac5698e22b86f4bfe85c3861b2b193308d530ee7a7fae58ed822b03c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c86304ddcb588ffb0c0a9ee5b4108c907e0c91a55ef5c42bcc0b3721c1fec643)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be2926f12374c4afc467b88ebe503f31a101464a8c705176bde413e89f79d84)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__712805c526c65da2b38d370d0592ebb71cb8f75e8ee160b4f290aa1b46d660c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2b72175f94c3dc0c2de8fe2ed9115f711648a249682e0fef4f8795c2956d463)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd95a34a457658defc0bd9025c3650d95e92c7df86b713933c68e8ad4f21f8da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11d388c070199382a488edea0e234e5b3ca623b1c417b0fa280fb6cf26b88d35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dtmf")
    def dtmf(
        self,
    ) -> DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfList:
        return typing.cast(DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfList, jsii.get(self, "dtmf"))

    @builtins.property
    @jsii.member(jsii_name="event")
    def event(
        self,
    ) -> DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventList:
        return typing.cast(DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventList, jsii.get(self, "event"))

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(
        self,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextList":
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextList", jsii.get(self, "text"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInput]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__967218a7b62673fb3a20f7f83bc66cba8e265726ad6b8f733978eb9edb719faa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputText",
    jsii_struct_bases=[],
    name_mapping={},
)
class DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputText:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19928d70620fe4bf4321eee556b14c4d1b335731cc5c196e570d20f9139fe9f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cff662681bd77502d8f66e61c4cb0680921368facde81e9d7d1747c23e9606f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c37c2ce464863d676ebfedf6519667befa515a0d12c8a30e43701dd8c425e60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94d3d8b1a5c4613cfa0f95d6905895cac28079838bf3ef8f0dc35f2180c5dc0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__faedeb7accfba96cba44e6742ed249e4567f1594db1bae66d79b97a3b34cecff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__953df4322332f583656f77bcaeb4fa75baeebf9e4f9558acb828e827baf8adad)
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
    ) -> typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputText]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputText], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputText],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf142a643c11f5bcab27aaa16d4f668222327f08a8ce20afff396fd2dd64590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseLastTestResultConversationTurnsUserInputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsUserInputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0e2d3cb88f5986d2db6c9b220653fcb203d30fd48df55dd1094cc5670873f34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__391f1d29769825d17e738f9801951ebbbc8cb92c9817daa07c6233fdd7306c7f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsUserInputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9d129ca60e0460944891d60d3883275796f852132bdf488b5af48f890cbbb3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__150e25c5e5275535078ca6e4ed5bfae540c493c675d7b275f4ae11c17f5eda03)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3103e4aca021f37dbfe9000e7df408125017c9d3e7aced5558ed364488a4210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseLastTestResultConversationTurnsUserInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsUserInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06c9ac784dc8ca611820e8b8b5ab16873cb4327926234f8ec3c9fb3c50b00c09)
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
    ) -> DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputList:
        return typing.cast(DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputList, jsii.get(self, "input"))

    @builtins.property
    @jsii.member(jsii_name="isWebhookEnabled")
    def is_webhook_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isWebhookEnabled"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInput]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__776a8628fc65ee987db9cfa4ae0bbb84b73918371f106809f84b7171611d8d6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPage",
    jsii_struct_bases=[],
    name_mapping={},
)
class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPage:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a819f5afbcddeb4dbb1b5cd225eec52ae1e3427414627d1dd7dcf842fe58d34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860cde3d7fdbafafc5a9c5994483278c62a005c12e9d9b13d701f813a8b2df11)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fafec5f278b7b3206059428df238ec072bc1595fa24c8d879bcd68e9851773b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__665f4e934dcdaa2065c4ea6605d9e1e214a8f59b8eb32ce52af974ea60fd3d0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bd74320adab999ee4d71ba936935995d5eeef4534a33dd66c890e791a1c35b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__005d1d6a29eb30e6660d8caf21eae05e7773663a62236b7f01dc09401e32bc87)
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
    ) -> typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPage]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66eefc5d8c023f970060b732b99514debdbb0e1dc07ff9c57af183c99390e285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferences",
    jsii_struct_bases=[],
    name_mapping={},
)
class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferences:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__849774746ccc52ff3ba9afb5407e0910592e32f6ee3538ce8c1b5f298375665e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccfd11a6504b6394bd34b1b3edfa319f598eb1fa65a5131520b8fd442f85e15c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740092a09ff779cb2cad29a7b37bcc7dfa42037498ff3fdd1d6c138c8176b675)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc02601511131a99353abfef5c1e179ef9103e0d7ad10552f0f514ab4aab2f61)
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
            type_hints = typing.get_type_hints(_typecheckingstub__706fa42d2455c5a949cb2bd0bc89b3d6842b3141446b73d82e7d21e619d8f0c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e85f9dec50468272083960d4e93ffda569c8869fc33efdd21e4c0ec86d01e2b)
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
    ) -> typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferences]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4c57009da38626e2582b780d885d1bf0f3b00d2667a800c7892b396824f2ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3db9f52b3e5695310e05a3f20d162aed2861d864299ccdfb9dab4362e4515428)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a9e0c748095d7bbe365e80d3d071501865552a5facd1c61e02924a629e40179)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036aab0a0a4aa691714c34eb88ae871c39aec3aaba046a06dc08fe28f6bb35d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8e7be6800a73305ee8e5453f1b2b07bee7df24063f47db2c7a6c2b7b6f3bab6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d91999d6e61abded72eca2526c42c24c9e130a9a6c31986a0aebf3ad4bb46a50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c45b3e0ab3a3f6cc092f6912923ccd7df9671401b3eaf160461639dd97f00cc5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="currentPage")
    def current_page(
        self,
    ) -> DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageList:
        return typing.cast(DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageList, jsii.get(self, "currentPage"))

    @builtins.property
    @jsii.member(jsii_name="differences")
    def differences(
        self,
    ) -> DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesList:
        return typing.cast(DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesList, jsii.get(self, "differences"))

    @builtins.property
    @jsii.member(jsii_name="sessionParameters")
    def session_parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionParameters"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(
        self,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusList":
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="textResponses")
    def text_responses(
        self,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesList":
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesList", jsii.get(self, "textResponses"))

    @builtins.property
    @jsii.member(jsii_name="triggeredIntent")
    def triggered_intent(
        self,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentList":
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentList", jsii.get(self, "triggeredIntent"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutput]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b8abd850402a8bac8297dcd50ad1f7e76f3df63b6bd66b66ea62d15f51f8c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__964bf0fd55dcb3fa36db2ddd262aab234833784a4001a11cf398b08db94d1e76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9320a92914490e02cae1145df4262964e23e33394af9246d48d37ec3ef6256)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33fbc4b58928af28a20d7e0578217b31edf3a6647d7858af55214aae5a29385b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67974450bd4b4f6115ebb4278132cdfe9dbc18fe61dd1629aca44a57716abbf0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d769acf1525a91bf8f48a0d67ba284be816f3b9e67bd1efa809ff1bbc7f1311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__101ca70e18860e655b5340f667ad7989859ba3d0ecda05bd20e74c0d00d6454a)
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
    ) -> typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatus]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ddbd3e271508ab0193a907b0712a023a99417a3a3329137f0f90ec30d681f03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponses",
    jsii_struct_bases=[],
    name_mapping={},
)
class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponses:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponses(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40cd57777ba0e11b7750e4401a1a15dac011b0ab800e6bbe4100c194f8b0f335)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baae3a0878fc7bde7849134d161029a330d14288284f5d1e2d8a97d5eec1f3f5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cf9909a6cf2d35490e58cc028837d986f75f761aab3bd671682c161f1f662a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efdc2600591df69b1308801f27d0b87fcfd934ce326179cc5209a0dcb2b0086a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d82e26777795a6da49337f6177451419026474e24b95737ae08f7603a3851712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d62138392312e90b072d818970183bcad582506dba7e8e8360abf8d751a607e)
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
    ) -> typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponses]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponses], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponses],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c016ef1d85f2dc7f5bdbe770769aefb7ec5a02dac5207e9927fea5b9cdab2340)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntent",
    jsii_struct_bases=[],
    name_mapping={},
)
class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntent:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98dc1d29280a069938ba3d208cfa7e6dcd3649a6e085f7d2b7a4ea5b46120fcb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3587e8a513cd9d1601dfd68b014f671094ba4a5a83b29ee05bc47092ef2dd75b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f3f166c655e8ddd249cd0fe1341094e89b112302af67a94837d43995000b10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1aec7bb89e206bbebd56c15d91142fed8d67daf2be0a355d919612e7bd10d16b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91413beea5d091fe8b6c417a428da0b9f52958c05811f243cb34d8e04c5cadf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2802a15c4d7636c1c7e5dfc2adff01ad18abdd20c5ea4f22e58f70fe13fadaec)
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
    ) -> typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntent]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3816636d86212bbbaadfd1c4e0a24e96114ec64cc13795833c2d05f260046841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseLastTestResultList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20cc242081687b0a729769812582f6ee0e33df78b75204fa1aca9c1e5fbd79f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxTestCaseLastTestResultOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc75285fc08df62bc8fcbe48ff1e1c97b21022cb91452a277d2bd8d8fb1949f0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxTestCaseLastTestResultOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04dc5af30ce3c8c43e99c3bfbc53af48430a69c0a611b94d85d410918296fd1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4184b474216b192b2cb5c0f80ecd9753b365d8b93dd14c92221089cfa040b27)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddb177474b6fa285b459fcd4edb2d3a001f6aee4ccd363aef7d398e2dfa39525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseLastTestResultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseLastTestResultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dacaa68e37915ee9815d90a3f0692d7a0175190a2322f6014f6a0826581a6a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conversationTurns")
    def conversation_turns(
        self,
    ) -> DialogflowCxTestCaseLastTestResultConversationTurnsList:
        return typing.cast(DialogflowCxTestCaseLastTestResultConversationTurnsList, jsii.get(self, "conversationTurns"))

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
    def internal_value(self) -> typing.Optional[DialogflowCxTestCaseLastTestResult]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseLastTestResult], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseLastTestResult],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__501a1f374a7f9e1b7b3aed27d0b755c15ea0a0bd674260d991bd3e24679ef1ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurns",
    jsii_struct_bases=[],
    name_mapping={
        "user_input": "userInput",
        "virtual_agent_output": "virtualAgentOutput",
    },
)
class DialogflowCxTestCaseTestCaseConversationTurns:
    def __init__(
        self,
        *,
        user_input: typing.Optional[typing.Union["DialogflowCxTestCaseTestCaseConversationTurnsUserInput", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_agent_output: typing.Optional[typing.Union["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param user_input: user_input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#user_input DialogflowCxTestCase#user_input}
        :param virtual_agent_output: virtual_agent_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#virtual_agent_output DialogflowCxTestCase#virtual_agent_output}
        '''
        if isinstance(user_input, dict):
            user_input = DialogflowCxTestCaseTestCaseConversationTurnsUserInput(**user_input)
        if isinstance(virtual_agent_output, dict):
            virtual_agent_output = DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput(**virtual_agent_output)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a979d70023c1aeb916f5af8d5221071c33b987c9290ef4eff0ea424447a848d)
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
    ) -> typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsUserInput"]:
        '''user_input block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#user_input DialogflowCxTestCase#user_input}
        '''
        result = self._values.get("user_input")
        return typing.cast(typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsUserInput"], result)

    @builtins.property
    def virtual_agent_output(
        self,
    ) -> typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput"]:
        '''virtual_agent_output block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#virtual_agent_output DialogflowCxTestCase#virtual_agent_output}
        '''
        result = self._values.get("virtual_agent_output")
        return typing.cast(typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseTestCaseConversationTurns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseTestCaseConversationTurnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1962f339747658545535a72b8dad0f2d7d51274ec2edd8cb9a859d6de3d571e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxTestCaseTestCaseConversationTurnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c75b007c41900b04efc7a08c864e28132a7c41a88b8e9b09482f7e380b955c71)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxTestCaseTestCaseConversationTurnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ec6a6b9c4ced75e559cd31717da4d90eda065f28caae5df6af97863c4a226bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e5f0ebec4869626a1b6f60272e6ea9edd403e6b39461cd85983f6583b8ded43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d73f715e20ec9b2260525a4d156da78bf5bd509435fb05497de121240dc457ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxTestCaseTestCaseConversationTurns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxTestCaseTestCaseConversationTurns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxTestCaseTestCaseConversationTurns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdccdc471b878c40ea0732e79bdc9102cc0e0520dff22e73fea26b87b6888151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseTestCaseConversationTurnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a00183ff40b9c2be523f9839fe2f2728075e011fd5c11d20f013c82b6c37f8c3)
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
        input: typing.Optional[typing.Union["DialogflowCxTestCaseTestCaseConversationTurnsUserInputInput", typing.Dict[builtins.str, typing.Any]]] = None,
        is_webhook_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_sentiment_analysis: Whether sentiment analysis is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#enable_sentiment_analysis DialogflowCxTestCase#enable_sentiment_analysis}
        :param injected_parameters: Parameters that need to be injected into the conversation during intent detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#injected_parameters DialogflowCxTestCase#injected_parameters}
        :param input: input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#input DialogflowCxTestCase#input}
        :param is_webhook_enabled: If webhooks should be allowed to trigger in response to the user utterance. Often if parameters are injected, webhooks should not be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#is_webhook_enabled DialogflowCxTestCase#is_webhook_enabled}
        '''
        value = DialogflowCxTestCaseTestCaseConversationTurnsUserInput(
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
        current_page: typing.Optional[typing.Union["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage", typing.Dict[builtins.str, typing.Any]]] = None,
        session_parameters: typing.Optional[builtins.str] = None,
        text_responses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses", typing.Dict[builtins.str, typing.Any]]]]] = None,
        triggered_intent: typing.Optional[typing.Union["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param current_page: current_page block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#current_page DialogflowCxTestCase#current_page}
        :param session_parameters: The session parameters available to the bot at this point. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#session_parameters DialogflowCxTestCase#session_parameters}
        :param text_responses: text_responses block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#text_responses DialogflowCxTestCase#text_responses}
        :param triggered_intent: triggered_intent block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#triggered_intent DialogflowCxTestCase#triggered_intent}
        '''
        value = DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput(
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
    ) -> "DialogflowCxTestCaseTestCaseConversationTurnsUserInputOutputReference":
        return typing.cast("DialogflowCxTestCaseTestCaseConversationTurnsUserInputOutputReference", jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualAgentOutput")
    def virtual_agent_output(
        self,
    ) -> "DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputOutputReference":
        return typing.cast("DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputOutputReference", jsii.get(self, "virtualAgentOutput"))

    @builtins.property
    @jsii.member(jsii_name="userInputInput")
    def user_input_input(
        self,
    ) -> typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsUserInput"]:
        return typing.cast(typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsUserInput"], jsii.get(self, "userInputInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualAgentOutputInput")
    def virtual_agent_output_input(
        self,
    ) -> typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput"]:
        return typing.cast(typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput"], jsii.get(self, "virtualAgentOutputInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxTestCaseTestCaseConversationTurns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxTestCaseTestCaseConversationTurns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxTestCaseTestCaseConversationTurns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22efc7699d79f1e489a1d64f7cdce5c4963c3000bcc9b2ba9623307ef00e2fe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsUserInput",
    jsii_struct_bases=[],
    name_mapping={
        "enable_sentiment_analysis": "enableSentimentAnalysis",
        "injected_parameters": "injectedParameters",
        "input": "input",
        "is_webhook_enabled": "isWebhookEnabled",
    },
)
class DialogflowCxTestCaseTestCaseConversationTurnsUserInput:
    def __init__(
        self,
        *,
        enable_sentiment_analysis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        injected_parameters: typing.Optional[builtins.str] = None,
        input: typing.Optional[typing.Union["DialogflowCxTestCaseTestCaseConversationTurnsUserInputInput", typing.Dict[builtins.str, typing.Any]]] = None,
        is_webhook_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_sentiment_analysis: Whether sentiment analysis is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#enable_sentiment_analysis DialogflowCxTestCase#enable_sentiment_analysis}
        :param injected_parameters: Parameters that need to be injected into the conversation during intent detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#injected_parameters DialogflowCxTestCase#injected_parameters}
        :param input: input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#input DialogflowCxTestCase#input}
        :param is_webhook_enabled: If webhooks should be allowed to trigger in response to the user utterance. Often if parameters are injected, webhooks should not be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#is_webhook_enabled DialogflowCxTestCase#is_webhook_enabled}
        '''
        if isinstance(input, dict):
            input = DialogflowCxTestCaseTestCaseConversationTurnsUserInputInput(**input)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e41ce938b7b83a606f58bad4d34a5eae051525c8e18165c6dc81ce306cd122f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#enable_sentiment_analysis DialogflowCxTestCase#enable_sentiment_analysis}
        '''
        result = self._values.get("enable_sentiment_analysis")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def injected_parameters(self) -> typing.Optional[builtins.str]:
        '''Parameters that need to be injected into the conversation during intent detection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#injected_parameters DialogflowCxTestCase#injected_parameters}
        '''
        result = self._values.get("injected_parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsUserInputInput"]:
        '''input block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#input DialogflowCxTestCase#input}
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsUserInputInput"], result)

    @builtins.property
    def is_webhook_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If webhooks should be allowed to trigger in response to the user utterance.

        Often if parameters are injected, webhooks should not be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#is_webhook_enabled DialogflowCxTestCase#is_webhook_enabled}
        '''
        result = self._values.get("is_webhook_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseTestCaseConversationTurnsUserInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsUserInputInput",
    jsii_struct_bases=[],
    name_mapping={
        "dtmf": "dtmf",
        "event": "event",
        "language_code": "languageCode",
        "text": "text",
    },
)
class DialogflowCxTestCaseTestCaseConversationTurnsUserInputInput:
    def __init__(
        self,
        *,
        dtmf: typing.Optional[typing.Union["DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf", typing.Dict[builtins.str, typing.Any]]] = None,
        event: typing.Optional[typing.Union["DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent", typing.Dict[builtins.str, typing.Any]]] = None,
        language_code: typing.Optional[builtins.str] = None,
        text: typing.Optional[typing.Union["DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dtmf: dtmf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#dtmf DialogflowCxTestCase#dtmf}
        :param event: event block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#event DialogflowCxTestCase#event}
        :param language_code: The language of the input. See `Language Support <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ for a list of the currently supported language codes. Note that queries in the same session do not necessarily need to specify the same language. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#language_code DialogflowCxTestCase#language_code}
        :param text: text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#text DialogflowCxTestCase#text}
        '''
        if isinstance(dtmf, dict):
            dtmf = DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf(**dtmf)
        if isinstance(event, dict):
            event = DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent(**event)
        if isinstance(text, dict):
            text = DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText(**text)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72f7e94cdec51ad6cf81259a7685abfa661b8a4004e7ec30ce8f89510de4c8f4)
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
    ) -> typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf"]:
        '''dtmf block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#dtmf DialogflowCxTestCase#dtmf}
        '''
        result = self._values.get("dtmf")
        return typing.cast(typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf"], result)

    @builtins.property
    def event(
        self,
    ) -> typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent"]:
        '''event block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#event DialogflowCxTestCase#event}
        '''
        result = self._values.get("event")
        return typing.cast(typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent"], result)

    @builtins.property
    def language_code(self) -> typing.Optional[builtins.str]:
        '''The language of the input.

        See `Language Support <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ for a list of the currently supported language codes.
        Note that queries in the same session do not necessarily need to specify the same language.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#language_code DialogflowCxTestCase#language_code}
        '''
        result = self._values.get("language_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def text(
        self,
    ) -> typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText"]:
        '''text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#text DialogflowCxTestCase#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseTestCaseConversationTurnsUserInputInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf",
    jsii_struct_bases=[],
    name_mapping={"digits": "digits", "finish_digit": "finishDigit"},
)
class DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf:
    def __init__(
        self,
        *,
        digits: typing.Optional[builtins.str] = None,
        finish_digit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param digits: The dtmf digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#digits DialogflowCxTestCase#digits}
        :param finish_digit: The finish digit (if any). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#finish_digit DialogflowCxTestCase#finish_digit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1976d9a1a6acbbfe9d61639546d348a3209f63ce08cc2a3b5f2d09551f6985af)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#digits DialogflowCxTestCase#digits}
        '''
        result = self._values.get("digits")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def finish_digit(self) -> typing.Optional[builtins.str]:
        '''The finish digit (if any).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#finish_digit DialogflowCxTestCase#finish_digit}
        '''
        result = self._values.get("finish_digit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmfOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmfOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__755435303cf12d7a37c01b641da3024f38f7e63c2ff8a2cc5a76530a159b5ae2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d02939c92188544736c16a03addf74b18565587eb8e4f13dcf696677365ba54b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "digits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="finishDigit")
    def finish_digit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "finishDigit"))

    @finish_digit.setter
    def finish_digit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f9fb66087cd989e61baa9f5941247dfc4fc8c14370416fca8ce0156e0c10eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "finishDigit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad2ef28e15445fd12d8833755a223f38dcb8ffecafcb0a5ef640518c9ba6321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent",
    jsii_struct_bases=[],
    name_mapping={"event": "event"},
)
class DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent:
    def __init__(self, *, event: builtins.str) -> None:
        '''
        :param event: Name of the event. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#event DialogflowCxTestCase#event}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e479633774451ec32eb859a84836a5b85fba148e4cd30ee1247401e145bfb95)
            check_type(argname="argument event", value=event, expected_type=type_hints["event"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event": event,
        }

    @builtins.property
    def event(self) -> builtins.str:
        '''Name of the event.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#event DialogflowCxTestCase#event}
        '''
        result = self._values.get("event")
        assert result is not None, "Required property 'event' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEventOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEventOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fa97963c3b1684c2ccf9feb2cc90e51e56d564e4cdf766e700d3b8207fef964)
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
            type_hints = typing.get_type_hints(_typecheckingstub__361a740387d7834360f63a39292309c4fa8b571fc10f1844e09c3959d98a7d66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "event", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ea10ac3b10b9c1cd75eabf530306b107809dc09d8fe9c0280f6fdfabfbfba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e50ca9d8d37dacc1d2863e1e81668d941bd14852d3de5792a5e25665a580680)
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
        :param digits: The dtmf digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#digits DialogflowCxTestCase#digits}
        :param finish_digit: The finish digit (if any). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#finish_digit DialogflowCxTestCase#finish_digit}
        '''
        value = DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf(
            digits=digits, finish_digit=finish_digit
        )

        return typing.cast(None, jsii.invoke(self, "putDtmf", [value]))

    @jsii.member(jsii_name="putEvent")
    def put_event(self, *, event: builtins.str) -> None:
        '''
        :param event: Name of the event. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#event DialogflowCxTestCase#event}
        '''
        value = DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent(
            event=event
        )

        return typing.cast(None, jsii.invoke(self, "putEvent", [value]))

    @jsii.member(jsii_name="putText")
    def put_text(self, *, text: builtins.str) -> None:
        '''
        :param text: The natural language text to be processed. Text length must not exceed 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#text DialogflowCxTestCase#text}
        '''
        value = DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText(
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
    ) -> DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmfOutputReference:
        return typing.cast(DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmfOutputReference, jsii.get(self, "dtmf"))

    @builtins.property
    @jsii.member(jsii_name="event")
    def event(
        self,
    ) -> DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEventOutputReference:
        return typing.cast(DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEventOutputReference, jsii.get(self, "event"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(
        self,
    ) -> "DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputTextOutputReference":
        return typing.cast("DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputTextOutputReference", jsii.get(self, "text"))

    @builtins.property
    @jsii.member(jsii_name="dtmfInput")
    def dtmf_input(
        self,
    ) -> typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf], jsii.get(self, "dtmfInput"))

    @builtins.property
    @jsii.member(jsii_name="eventInput")
    def event_input(
        self,
    ) -> typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent], jsii.get(self, "eventInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(
        self,
    ) -> typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText"]:
        return typing.cast(typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText"], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af859997828e8816eaf7ba2cd969844f2c16cb3c9618fb1c40b054ab372648f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInput]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20d40300394b59abe8e65b7ee92d951248aace8dfa9cf113f55db59a6b72a4b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText",
    jsii_struct_bases=[],
    name_mapping={"text": "text"},
)
class DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText:
    def __init__(self, *, text: builtins.str) -> None:
        '''
        :param text: The natural language text to be processed. Text length must not exceed 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#text DialogflowCxTestCase#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ca5c8890434b9c82cebe3d7ff127252ea0f1f13dafdf42851d00f41c4592c41)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "text": text,
        }

    @builtins.property
    def text(self) -> builtins.str:
        '''The natural language text to be processed. Text length must not exceed 256 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#text DialogflowCxTestCase#text}
        '''
        result = self._values.get("text")
        assert result is not None, "Required property 'text' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41b4c9132e3e8d08fb17d2fad5837f5205c4680e9a85abdddb6c9ce6a35d90a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f758b71447b8497d01e5d9934fcbccd94b17130c0e9f3fb6b4e767c33eaebb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4812a3e89858879adc8402eb2c14a297c44e3acdebb0f2bd58fa2c48bb795974)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseTestCaseConversationTurnsUserInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsUserInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce0e06363fe8b7724c9a4fa2bc7f7eaa2cdba4e918960bff3bcab725907e1782)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInput")
    def put_input(
        self,
        *,
        dtmf: typing.Optional[typing.Union[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf, typing.Dict[builtins.str, typing.Any]]] = None,
        event: typing.Optional[typing.Union[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent, typing.Dict[builtins.str, typing.Any]]] = None,
        language_code: typing.Optional[builtins.str] = None,
        text: typing.Optional[typing.Union[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dtmf: dtmf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#dtmf DialogflowCxTestCase#dtmf}
        :param event: event block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#event DialogflowCxTestCase#event}
        :param language_code: The language of the input. See `Language Support <https://cloud.google.com/dialogflow/cx/docs/reference/language>`_ for a list of the currently supported language codes. Note that queries in the same session do not necessarily need to specify the same language. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#language_code DialogflowCxTestCase#language_code}
        :param text: text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#text DialogflowCxTestCase#text}
        '''
        value = DialogflowCxTestCaseTestCaseConversationTurnsUserInputInput(
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
    ) -> DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputOutputReference:
        return typing.cast(DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputOutputReference, jsii.get(self, "input"))

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
    ) -> typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInput]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInput], jsii.get(self, "inputInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b80c097e2b04bb9181686730785df3c345da685afcfe9e4a17743daa91caa092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSentimentAnalysis", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="injectedParameters")
    def injected_parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "injectedParameters"))

    @injected_parameters.setter
    def injected_parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a216f89972650da1c507524c5e8416346413b92032a08cac406474450bbd56b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdf59272c377de16776ab39be10432f70a0d37dfc1f92e3478d1e6b96d38dd5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isWebhookEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInput]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a76fc34d6288cb9b1cb64a20fde4633de27506d1dcfb0a4b71b2b1475a0ff141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput",
    jsii_struct_bases=[],
    name_mapping={
        "current_page": "currentPage",
        "session_parameters": "sessionParameters",
        "text_responses": "textResponses",
        "triggered_intent": "triggeredIntent",
    },
)
class DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput:
    def __init__(
        self,
        *,
        current_page: typing.Optional[typing.Union["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage", typing.Dict[builtins.str, typing.Any]]] = None,
        session_parameters: typing.Optional[builtins.str] = None,
        text_responses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses", typing.Dict[builtins.str, typing.Any]]]]] = None,
        triggered_intent: typing.Optional[typing.Union["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param current_page: current_page block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#current_page DialogflowCxTestCase#current_page}
        :param session_parameters: The session parameters available to the bot at this point. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#session_parameters DialogflowCxTestCase#session_parameters}
        :param text_responses: text_responses block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#text_responses DialogflowCxTestCase#text_responses}
        :param triggered_intent: triggered_intent block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#triggered_intent DialogflowCxTestCase#triggered_intent}
        '''
        if isinstance(current_page, dict):
            current_page = DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage(**current_page)
        if isinstance(triggered_intent, dict):
            triggered_intent = DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent(**triggered_intent)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f878f4a42f0e9090c5c608afece0f93dd8e3c52f4c7bd3366934a978589d0f7)
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
    ) -> typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage"]:
        '''current_page block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#current_page DialogflowCxTestCase#current_page}
        '''
        result = self._values.get("current_page")
        return typing.cast(typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage"], result)

    @builtins.property
    def session_parameters(self) -> typing.Optional[builtins.str]:
        '''The session parameters available to the bot at this point.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#session_parameters DialogflowCxTestCase#session_parameters}
        '''
        result = self._values.get("session_parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def text_responses(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses"]]]:
        '''text_responses block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#text_responses DialogflowCxTestCase#text_responses}
        '''
        result = self._values.get("text_responses")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses"]]], result)

    @builtins.property
    def triggered_intent(
        self,
    ) -> typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent"]:
        '''triggered_intent block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#triggered_intent DialogflowCxTestCase#triggered_intent}
        '''
        result = self._values.get("triggered_intent")
        return typing.cast(typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: The unique identifier of the page. Format: projects//locations//agents//flows//pages/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#name DialogflowCxTestCase#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45feac79a65c94e2242fcdfae9a57d570dd40a10eee472eca27be00239d27431)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the page. Format: projects//locations//agents//flows//pages/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#name DialogflowCxTestCase#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b15fdca04d29937d1271ab074f373eb36a10233ad738cceaefbf7d39977dbf12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__877434e74d74f8802d8b4d5852ef5124ecb9b515508176122c9fb6cca6e037af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd13f3276c0ae797d3639b1912ee06ad9d3af1b7577907e85d7f304aaf39a350)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__567ad19421d5d3f19ae8ff3c3bf845e768edc060f9314726c9f287f36bc7b7a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCurrentPage")
    def put_current_page(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: The unique identifier of the page. Format: projects//locations//agents//flows//pages/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#name DialogflowCxTestCase#name}
        '''
        value = DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putCurrentPage", [value]))

    @jsii.member(jsii_name="putTextResponses")
    def put_text_responses(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80876f8b964112e6332f06151e1463cc30812bd24f0e4058aad9a89849bcb1c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTextResponses", [value]))

    @jsii.member(jsii_name="putTriggeredIntent")
    def put_triggered_intent(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The unique identifier of the intent. Format: projects//locations//agents//intents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#name DialogflowCxTestCase#name}
        '''
        value = DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent(
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
    ) -> DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPageOutputReference:
        return typing.cast(DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPageOutputReference, jsii.get(self, "currentPage"))

    @builtins.property
    @jsii.member(jsii_name="textResponses")
    def text_responses(
        self,
    ) -> "DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesList":
        return typing.cast("DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesList", jsii.get(self, "textResponses"))

    @builtins.property
    @jsii.member(jsii_name="triggeredIntent")
    def triggered_intent(
        self,
    ) -> "DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference":
        return typing.cast("DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference", jsii.get(self, "triggeredIntent"))

    @builtins.property
    @jsii.member(jsii_name="currentPageInput")
    def current_page_input(
        self,
    ) -> typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage], jsii.get(self, "currentPageInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionParametersInput")
    def session_parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="textResponsesInput")
    def text_responses_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses"]]], jsii.get(self, "textResponsesInput"))

    @builtins.property
    @jsii.member(jsii_name="triggeredIntentInput")
    def triggered_intent_input(
        self,
    ) -> typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent"]:
        return typing.cast(typing.Optional["DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent"], jsii.get(self, "triggeredIntentInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionParameters")
    def session_parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionParameters"))

    @session_parameters.setter
    def session_parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c95771de1821e9b6f3920e730a9aec2fdc3e776a1ba68d638548a8f77891a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029b1927ea94c66a950571e905878160e2a119d3c206a0bcac35339129a0ef8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses",
    jsii_struct_bases=[],
    name_mapping={"text": "text"},
)
class DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses:
    def __init__(
        self,
        *,
        text: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param text: A collection of text responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#text DialogflowCxTestCase#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e4caa74d25653f31ba2941e7d350e47a1ab0debab1ada83406739879c81a70a)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def text(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A collection of text responses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#text DialogflowCxTestCase#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__495ca1e8c68c2172fc48e2b996e4a55707a2e0262ff58348ed7b78992b6cad52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77780c43584eb70b9965c9502ce3deca323daf50ee2f77222e7154d25da04215)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b42f5083880479ecd48387d0266ab854c94ae55a5e7ac528b087191792b2fc57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ef3a24cb6d4e1fcaf8127c8b112957ea0d97d735c6c422f29bb1580db978c00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c326523cd820504ae029c074fd7b75b6557da1ab29849b745b6cb0e66aaa6e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5994ef52eb3245ce557ae21286abbe56b8027ac2a9824553a1473868c28d541)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d450fb2623462e63f9f64ff0f6853ce2642d56a6add5133af0188e3f342d0622)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ff0437abdc0007b34ee22575eb0278dd8240ea06f34d4bdaafe5005bc4a7fed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5193767efb1488423e8534488daa5b171497184a00cc537ae871a9ff67f7f183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: The unique identifier of the intent. Format: projects//locations//agents//intents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#name DialogflowCxTestCase#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f36602b056bd3bfc5fface298162767f2fb8254fc9bdfef4db8d7baec9195c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the intent. Format: projects//locations//agents//intents/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#name DialogflowCxTestCase#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d663f5fb9f449f85f46ae8deee71cc85d0a1d19f47cf2fdc1a3fe4d528e7d82e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51a19dfa2e98ae5ccf775eac9bbc4030648dd4dedbf9542b7d00b51b6a8e83ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26a6811698caef557aeb3b3ce2a0ef393e638a9b4f08131e6925fc472b20ec2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestConfig",
    jsii_struct_bases=[],
    name_mapping={
        "flow": "flow",
        "page": "page",
        "tracking_parameters": "trackingParameters",
    },
)
class DialogflowCxTestCaseTestConfig:
    def __init__(
        self,
        *,
        flow: typing.Optional[builtins.str] = None,
        page: typing.Optional[builtins.str] = None,
        tracking_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param flow: Flow name to start the test case with. Format: projects//locations//agents//flows/. Only one of flow and page should be set to indicate the starting point of the test case. If neither is set, the test case will start with start page on the default start flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#flow DialogflowCxTestCase#flow}
        :param page: The page to start the test case with. Format: projects//locations//agents//flows//pages/. Only one of flow and page should be set to indicate the starting point of the test case. If neither is set, the test case will start with start page on the default start flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#page DialogflowCxTestCase#page}
        :param tracking_parameters: Session parameters to be compared when calculating differences. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#tracking_parameters DialogflowCxTestCase#tracking_parameters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ceb2ef6009579048dd31d0b4397e2484e9f5865104ed2e700f37a1cde724600)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#flow DialogflowCxTestCase#flow}
        '''
        result = self._values.get("flow")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def page(self) -> typing.Optional[builtins.str]:
        '''The page to start the test case with.

        Format: projects//locations//agents//flows//pages/.
        Only one of flow and page should be set to indicate the starting point of the test case. If neither is set, the test case will start with start page on the default start flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#page DialogflowCxTestCase#page}
        '''
        result = self._values.get("page")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tracking_parameters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Session parameters to be compared when calculating differences.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#tracking_parameters DialogflowCxTestCase#tracking_parameters}
        '''
        result = self._values.get("tracking_parameters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseTestConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseTestConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTestConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb4c3b0c076629ff93b672b20f19c46fc58d395ea5d61483e85820311c65b4c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__929f556f40ca1adda166451083e237cffa882279137c3f53dbb99c4ab395c533)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="page")
    def page(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "page"))

    @page.setter
    def page(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ffa4a98605b2215c3603371981e9acfc4ca08c3edcb59079e8a8cdde7cf7c9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "page", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trackingParameters")
    def tracking_parameters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trackingParameters"))

    @tracking_parameters.setter
    def tracking_parameters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1997f91d32224fc59d227d9e4bc0fce9ef3142d7a8bf45457f70d1a7cca0908b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trackingParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowCxTestCaseTestConfig]:
        return typing.cast(typing.Optional[DialogflowCxTestCaseTestConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxTestCaseTestConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e54126bd3ba303d96c2c61d6d83e891e2ea1986b43707c06f3010a0699ad58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DialogflowCxTestCaseTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#create DialogflowCxTestCase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#delete DialogflowCxTestCase#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#update DialogflowCxTestCase#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0718e674a7e95ee798305d8cce76309050dbe1ea3d8b704019323472f3c347c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#create DialogflowCxTestCase#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#delete DialogflowCxTestCase#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_test_case#update DialogflowCxTestCase#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxTestCaseTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxTestCaseTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTestCase.DialogflowCxTestCaseTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5272a40793775846973ca1539b9cc5ab0d29e0a52132b823f2f9cb4ecca2f6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e46baf752538a46f27a84c3227062eb27c9bd6989c8475c07810f4308cfd635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acfc5f225cd714d219f7c827a0b3d8fe6687bf473521c4809817d4db74ae2359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ba8b802c2957efc00901b684b9b9669f011ee37df11e9a96084631a27dd867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxTestCaseTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxTestCaseTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxTestCaseTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf8d93971861fe3aa739b65129997d23d5c2e31a1f30274b16dff20289987de2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DialogflowCxTestCase",
    "DialogflowCxTestCaseConfig",
    "DialogflowCxTestCaseLastTestResult",
    "DialogflowCxTestCaseLastTestResultConversationTurns",
    "DialogflowCxTestCaseLastTestResultConversationTurnsList",
    "DialogflowCxTestCaseLastTestResultConversationTurnsOutputReference",
    "DialogflowCxTestCaseLastTestResultConversationTurnsUserInput",
    "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInput",
    "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmf",
    "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfList",
    "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmfOutputReference",
    "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEvent",
    "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventList",
    "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEventOutputReference",
    "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputList",
    "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputOutputReference",
    "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputText",
    "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextList",
    "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputTextOutputReference",
    "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputList",
    "DialogflowCxTestCaseLastTestResultConversationTurnsUserInputOutputReference",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutput",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPage",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageList",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPageOutputReference",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferences",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesList",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferencesOutputReference",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputList",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputOutputReference",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatus",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusList",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatusOutputReference",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponses",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesList",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponsesOutputReference",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntent",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentList",
    "DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference",
    "DialogflowCxTestCaseLastTestResultList",
    "DialogflowCxTestCaseLastTestResultOutputReference",
    "DialogflowCxTestCaseTestCaseConversationTurns",
    "DialogflowCxTestCaseTestCaseConversationTurnsList",
    "DialogflowCxTestCaseTestCaseConversationTurnsOutputReference",
    "DialogflowCxTestCaseTestCaseConversationTurnsUserInput",
    "DialogflowCxTestCaseTestCaseConversationTurnsUserInputInput",
    "DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf",
    "DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmfOutputReference",
    "DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent",
    "DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEventOutputReference",
    "DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputOutputReference",
    "DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText",
    "DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputTextOutputReference",
    "DialogflowCxTestCaseTestCaseConversationTurnsUserInputOutputReference",
    "DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput",
    "DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage",
    "DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPageOutputReference",
    "DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputOutputReference",
    "DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses",
    "DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesList",
    "DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponsesOutputReference",
    "DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent",
    "DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntentOutputReference",
    "DialogflowCxTestCaseTestConfig",
    "DialogflowCxTestCaseTestConfigOutputReference",
    "DialogflowCxTestCaseTimeouts",
    "DialogflowCxTestCaseTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f73eddce12cbd1ddb43734f22d6dfd1875189c24df62c9b9c815a542c285f3a3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    notes: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    test_case_conversation_turns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxTestCaseTestCaseConversationTurns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    test_config: typing.Optional[typing.Union[DialogflowCxTestCaseTestConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxTestCaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__62745e87f1806084ee560b257b0ba4b53cf2a879b2330b3fe46b54a46be9f4be(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e1ab8476e197c822be7db944a75c33ffc3de8cc9c726dbacba8755d0c82a802(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxTestCaseTestCaseConversationTurns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02c16306b6801d7497f109dba7162163a70700893103baa1ce4f64d92fab130(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7ffb2bfe9edb57eccc62cdf243424bab024dbe7fe8e41b68b3a731eda7fc2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f86b173db27ad7b5aca5e8067d75f4a3138fa58da7232188aa247282ca284216(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afaed9b89aa78a398dcba8d8891246b4e7cf214fa52203e4d93556c7790c11d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e910887e8e693212c0b7e2643681755d6bedf09965316f4249c73f727551b4a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf79737c0a45409096c310a68daf6ffe315136381dfc2e1ec7ce9f7be544f3d(
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
    test_case_conversation_turns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxTestCaseTestCaseConversationTurns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    test_config: typing.Optional[typing.Union[DialogflowCxTestCaseTestConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxTestCaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b55b3d1aec34f86068ed7396637a474412d0ec172c6df3abfe0bd95c200be0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1906d615e00d51fc3df3f2eb134459a52a9cbce3390e44ce212a6252b4e3cba(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1930aaf7bce4701d701d61c096f6694caa3df3a896591379be910ebbced2501(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f6aa7eb862187b55ab390b62aca1762eae3d1aa68abefd1c78240ebba1e643(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd89a470da7e8e7dc2b86eedd81167335bf7e3cce5bf930a62c2d0103d267fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0a7c50a9a5bb746628329e41685be289d98511ee3851bae0411743b8ed76e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9162612c13d7cb2ba43a2ea91463735eba3dda3e2a1a7b63cc019b8d0edadc01(
    value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a3f099777a61c7308baade45db94026d6980b600a1791b338ec501a99ed86c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adbfeb25df1c4de4f2aedc1bad61417c7e7cfc80808c19e7298bfee307c5bfa1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a915bb42d2798adac83f18e13ca536b0edc83d6f323b1a4ebefa2600a74c6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c760f04f991872ccbec3c84fe9d05b32a6aa8af9b495649da75d6d880639b3e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e480ac3a96e2b1368d21cd28ab581e7f1b6b7ad61a27928b75456e9dc15704(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388911fd8adae1cae0b0a4c4efdd805ee731d9a173a1c6d67dd001cae74667c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce1db591cc4df524f87e89e46a8e3510f20a38bdff7227351d7b0044d12070d(
    value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputDtmf],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb73266ddb34fa4126720144a81372f6c3f07b31b64edbc23bd3afbbba1cdf3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daca691869caa6f041fb9cfd63fd9d423a0d247606e29914c103b539b774a7bb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d91bec808cf4d2bbb6e035fdffe797d68f3b16e3e5628669cd83bb6789c183d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eadf21e62b022e071ca390d27c21fd58aa260fa38760f11d5fd047f90e66ed78(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c7fece880f8b6b9da7f11466a0ca982137f22728af6a2499e68067bb165ba9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__410d687a74ba311ff68c798875ad750bba842044d630292eddb25bff0f0ab93f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7ee7fdac5698e22b86f4bfe85c3861b2b193308d530ee7a7fae58ed822b03c(
    value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputEvent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86304ddcb588ffb0c0a9ee5b4108c907e0c91a55ef5c42bcc0b3721c1fec643(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be2926f12374c4afc467b88ebe503f31a101464a8c705176bde413e89f79d84(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712805c526c65da2b38d370d0592ebb71cb8f75e8ee160b4f290aa1b46d660c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b72175f94c3dc0c2de8fe2ed9115f711648a249682e0fef4f8795c2956d463(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd95a34a457658defc0bd9025c3650d95e92c7df86b713933c68e8ad4f21f8da(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d388c070199382a488edea0e234e5b3ca623b1c417b0fa280fb6cf26b88d35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967218a7b62673fb3a20f7f83bc66cba8e265726ad6b8f733978eb9edb719faa(
    value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19928d70620fe4bf4321eee556b14c4d1b335731cc5c196e570d20f9139fe9f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cff662681bd77502d8f66e61c4cb0680921368facde81e9d7d1747c23e9606f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c37c2ce464863d676ebfedf6519667befa515a0d12c8a30e43701dd8c425e60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d3d8b1a5c4613cfa0f95d6905895cac28079838bf3ef8f0dc35f2180c5dc0b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faedeb7accfba96cba44e6742ed249e4567f1594db1bae66d79b97a3b34cecff(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953df4322332f583656f77bcaeb4fa75baeebf9e4f9558acb828e827baf8adad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf142a643c11f5bcab27aaa16d4f668222327f08a8ce20afff396fd2dd64590(
    value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInputInputText],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e2d3cb88f5986d2db6c9b220653fcb203d30fd48df55dd1094cc5670873f34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391f1d29769825d17e738f9801951ebbbc8cb92c9817daa07c6233fdd7306c7f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9d129ca60e0460944891d60d3883275796f852132bdf488b5af48f890cbbb3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150e25c5e5275535078ca6e4ed5bfae540c493c675d7b275f4ae11c17f5eda03(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3103e4aca021f37dbfe9000e7df408125017c9d3e7aced5558ed364488a4210(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06c9ac784dc8ca611820e8b8b5ab16873cb4327926234f8ec3c9fb3c50b00c09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776a8628fc65ee987db9cfa4ae0bbb84b73918371f106809f84b7171611d8d6e(
    value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsUserInput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a819f5afbcddeb4dbb1b5cd225eec52ae1e3427414627d1dd7dcf842fe58d34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860cde3d7fdbafafc5a9c5994483278c62a005c12e9d9b13d701f813a8b2df11(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fafec5f278b7b3206059428df238ec072bc1595fa24c8d879bcd68e9851773b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665f4e934dcdaa2065c4ea6605d9e1e214a8f59b8eb32ce52af974ea60fd3d0e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bd74320adab999ee4d71ba936935995d5eeef4534a33dd66c890e791a1c35b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005d1d6a29eb30e6660d8caf21eae05e7773663a62236b7f01dc09401e32bc87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66eefc5d8c023f970060b732b99514debdbb0e1dc07ff9c57af183c99390e285(
    value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputCurrentPage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849774746ccc52ff3ba9afb5407e0910592e32f6ee3538ce8c1b5f298375665e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccfd11a6504b6394bd34b1b3edfa319f598eb1fa65a5131520b8fd442f85e15c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740092a09ff779cb2cad29a7b37bcc7dfa42037498ff3fdd1d6c138c8176b675(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc02601511131a99353abfef5c1e179ef9103e0d7ad10552f0f514ab4aab2f61(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__706fa42d2455c5a949cb2bd0bc89b3d6842b3141446b73d82e7d21e619d8f0c1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e85f9dec50468272083960d4e93ffda569c8869fc33efdd21e4c0ec86d01e2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4c57009da38626e2582b780d885d1bf0f3b00d2667a800c7892b396824f2ed(
    value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputDifferences],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db9f52b3e5695310e05a3f20d162aed2861d864299ccdfb9dab4362e4515428(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a9e0c748095d7bbe365e80d3d071501865552a5facd1c61e02924a629e40179(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036aab0a0a4aa691714c34eb88ae871c39aec3aaba046a06dc08fe28f6bb35d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e7be6800a73305ee8e5453f1b2b07bee7df24063f47db2c7a6c2b7b6f3bab6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d91999d6e61abded72eca2526c42c24c9e130a9a6c31986a0aebf3ad4bb46a50(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45b3e0ab3a3f6cc092f6912923ccd7df9671401b3eaf160461639dd97f00cc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b8abd850402a8bac8297dcd50ad1f7e76f3df63b6bd66b66ea62d15f51f8c2(
    value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__964bf0fd55dcb3fa36db2ddd262aab234833784a4001a11cf398b08db94d1e76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9320a92914490e02cae1145df4262964e23e33394af9246d48d37ec3ef6256(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33fbc4b58928af28a20d7e0578217b31edf3a6647d7858af55214aae5a29385b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67974450bd4b4f6115ebb4278132cdfe9dbc18fe61dd1629aca44a57716abbf0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d769acf1525a91bf8f48a0d67ba284be816f3b9e67bd1efa809ff1bbc7f1311(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101ca70e18860e655b5340f667ad7989859ba3d0ecda05bd20e74c0d00d6454a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ddbd3e271508ab0193a907b0712a023a99417a3a3329137f0f90ec30d681f03(
    value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40cd57777ba0e11b7750e4401a1a15dac011b0ab800e6bbe4100c194f8b0f335(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baae3a0878fc7bde7849134d161029a330d14288284f5d1e2d8a97d5eec1f3f5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cf9909a6cf2d35490e58cc028837d986f75f761aab3bd671682c161f1f662a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efdc2600591df69b1308801f27d0b87fcfd934ce326179cc5209a0dcb2b0086a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d82e26777795a6da49337f6177451419026474e24b95737ae08f7603a3851712(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d62138392312e90b072d818970183bcad582506dba7e8e8360abf8d751a607e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c016ef1d85f2dc7f5bdbe770769aefb7ec5a02dac5207e9927fea5b9cdab2340(
    value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTextResponses],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98dc1d29280a069938ba3d208cfa7e6dcd3649a6e085f7d2b7a4ea5b46120fcb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3587e8a513cd9d1601dfd68b014f671094ba4a5a83b29ee05bc47092ef2dd75b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f3f166c655e8ddd249cd0fe1341094e89b112302af67a94837d43995000b10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aec7bb89e206bbebd56c15d91142fed8d67daf2be0a355d919612e7bd10d16b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91413beea5d091fe8b6c417a428da0b9f52958c05811f243cb34d8e04c5cadf8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2802a15c4d7636c1c7e5dfc2adff01ad18abdd20c5ea4f22e58f70fe13fadaec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3816636d86212bbbaadfd1c4e0a24e96114ec64cc13795833c2d05f260046841(
    value: typing.Optional[DialogflowCxTestCaseLastTestResultConversationTurnsVirtualAgentOutputTriggeredIntent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20cc242081687b0a729769812582f6ee0e33df78b75204fa1aca9c1e5fbd79f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc75285fc08df62bc8fcbe48ff1e1c97b21022cb91452a277d2bd8d8fb1949f0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04dc5af30ce3c8c43e99c3bfbc53af48430a69c0a611b94d85d410918296fd1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4184b474216b192b2cb5c0f80ecd9753b365d8b93dd14c92221089cfa040b27(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb177474b6fa285b459fcd4edb2d3a001f6aee4ccd363aef7d398e2dfa39525(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dacaa68e37915ee9815d90a3f0692d7a0175190a2322f6014f6a0826581a6a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__501a1f374a7f9e1b7b3aed27d0b755c15ea0a0bd674260d991bd3e24679ef1ae(
    value: typing.Optional[DialogflowCxTestCaseLastTestResult],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a979d70023c1aeb916f5af8d5221071c33b987c9290ef4eff0ea424447a848d(
    *,
    user_input: typing.Optional[typing.Union[DialogflowCxTestCaseTestCaseConversationTurnsUserInput, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_agent_output: typing.Optional[typing.Union[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1962f339747658545535a72b8dad0f2d7d51274ec2edd8cb9a859d6de3d571e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75b007c41900b04efc7a08c864e28132a7c41a88b8e9b09482f7e380b955c71(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ec6a6b9c4ced75e559cd31717da4d90eda065f28caae5df6af97863c4a226bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5f0ebec4869626a1b6f60272e6ea9edd403e6b39461cd85983f6583b8ded43(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73f715e20ec9b2260525a4d156da78bf5bd509435fb05497de121240dc457ee(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdccdc471b878c40ea0732e79bdc9102cc0e0520dff22e73fea26b87b6888151(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxTestCaseTestCaseConversationTurns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00183ff40b9c2be523f9839fe2f2728075e011fd5c11d20f013c82b6c37f8c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22efc7699d79f1e489a1d64f7cdce5c4963c3000bcc9b2ba9623307ef00e2fe8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxTestCaseTestCaseConversationTurns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e41ce938b7b83a606f58bad4d34a5eae051525c8e18165c6dc81ce306cd122f(
    *,
    enable_sentiment_analysis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    injected_parameters: typing.Optional[builtins.str] = None,
    input: typing.Optional[typing.Union[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInput, typing.Dict[builtins.str, typing.Any]]] = None,
    is_webhook_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f7e94cdec51ad6cf81259a7685abfa661b8a4004e7ec30ce8f89510de4c8f4(
    *,
    dtmf: typing.Optional[typing.Union[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf, typing.Dict[builtins.str, typing.Any]]] = None,
    event: typing.Optional[typing.Union[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent, typing.Dict[builtins.str, typing.Any]]] = None,
    language_code: typing.Optional[builtins.str] = None,
    text: typing.Optional[typing.Union[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1976d9a1a6acbbfe9d61639546d348a3209f63ce08cc2a3b5f2d09551f6985af(
    *,
    digits: typing.Optional[builtins.str] = None,
    finish_digit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755435303cf12d7a37c01b641da3024f38f7e63c2ff8a2cc5a76530a159b5ae2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02939c92188544736c16a03addf74b18565587eb8e4f13dcf696677365ba54b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f9fb66087cd989e61baa9f5941247dfc4fc8c14370416fca8ce0156e0c10eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad2ef28e15445fd12d8833755a223f38dcb8ffecafcb0a5ef640518c9ba6321(
    value: typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputDtmf],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e479633774451ec32eb859a84836a5b85fba148e4cd30ee1247401e145bfb95(
    *,
    event: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa97963c3b1684c2ccf9feb2cc90e51e56d564e4cdf766e700d3b8207fef964(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361a740387d7834360f63a39292309c4fa8b571fc10f1844e09c3959d98a7d66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ea10ac3b10b9c1cd75eabf530306b107809dc09d8fe9c0280f6fdfabfbfba6(
    value: typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputEvent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e50ca9d8d37dacc1d2863e1e81668d941bd14852d3de5792a5e25665a580680(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af859997828e8816eaf7ba2cd969844f2c16cb3c9618fb1c40b054ab372648f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d40300394b59abe8e65b7ee92d951248aace8dfa9cf113f55db59a6b72a4b0(
    value: typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca5c8890434b9c82cebe3d7ff127252ea0f1f13dafdf42851d00f41c4592c41(
    *,
    text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b4c9132e3e8d08fb17d2fad5837f5205c4680e9a85abdddb6c9ce6a35d90a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f758b71447b8497d01e5d9934fcbccd94b17130c0e9f3fb6b4e767c33eaebb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4812a3e89858879adc8402eb2c14a297c44e3acdebb0f2bd58fa2c48bb795974(
    value: typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInputInputText],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0e06363fe8b7724c9a4fa2bc7f7eaa2cdba4e918960bff3bcab725907e1782(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b80c097e2b04bb9181686730785df3c345da685afcfe9e4a17743daa91caa092(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a216f89972650da1c507524c5e8416346413b92032a08cac406474450bbd56b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf59272c377de16776ab39be10432f70a0d37dfc1f92e3478d1e6b96d38dd5e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a76fc34d6288cb9b1cb64a20fde4633de27506d1dcfb0a4b71b2b1475a0ff141(
    value: typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsUserInput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f878f4a42f0e9090c5c608afece0f93dd8e3c52f4c7bd3366934a978589d0f7(
    *,
    current_page: typing.Optional[typing.Union[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage, typing.Dict[builtins.str, typing.Any]]] = None,
    session_parameters: typing.Optional[builtins.str] = None,
    text_responses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses, typing.Dict[builtins.str, typing.Any]]]]] = None,
    triggered_intent: typing.Optional[typing.Union[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45feac79a65c94e2242fcdfae9a57d570dd40a10eee472eca27be00239d27431(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b15fdca04d29937d1271ab074f373eb36a10233ad738cceaefbf7d39977dbf12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__877434e74d74f8802d8b4d5852ef5124ecb9b515508176122c9fb6cca6e037af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd13f3276c0ae797d3639b1912ee06ad9d3af1b7577907e85d7f304aaf39a350(
    value: typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputCurrentPage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567ad19421d5d3f19ae8ff3c3bf845e768edc060f9314726c9f287f36bc7b7a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80876f8b964112e6332f06151e1463cc30812bd24f0e4058aad9a89849bcb1c9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c95771de1821e9b6f3920e730a9aec2fdc3e776a1ba68d638548a8f77891a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029b1927ea94c66a950571e905878160e2a119d3c206a0bcac35339129a0ef8a(
    value: typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4caa74d25653f31ba2941e7d350e47a1ab0debab1ada83406739879c81a70a(
    *,
    text: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__495ca1e8c68c2172fc48e2b996e4a55707a2e0262ff58348ed7b78992b6cad52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77780c43584eb70b9965c9502ce3deca323daf50ee2f77222e7154d25da04215(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42f5083880479ecd48387d0266ab854c94ae55a5e7ac528b087191792b2fc57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef3a24cb6d4e1fcaf8127c8b112957ea0d97d735c6c422f29bb1580db978c00(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c326523cd820504ae029c074fd7b75b6557da1ab29849b745b6cb0e66aaa6e2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5994ef52eb3245ce557ae21286abbe56b8027ac2a9824553a1473868c28d541(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d450fb2623462e63f9f64ff0f6853ce2642d56a6add5133af0188e3f342d0622(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff0437abdc0007b34ee22575eb0278dd8240ea06f34d4bdaafe5005bc4a7fed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5193767efb1488423e8534488daa5b171497184a00cc537ae871a9ff67f7f183(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTextResponses]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f36602b056bd3bfc5fface298162767f2fb8254fc9bdfef4db8d7baec9195c(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d663f5fb9f449f85f46ae8deee71cc85d0a1d19f47cf2fdc1a3fe4d528e7d82e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a19dfa2e98ae5ccf775eac9bbc4030648dd4dedbf9542b7d00b51b6a8e83ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a6811698caef557aeb3b3ce2a0ef393e638a9b4f08131e6925fc472b20ec2a(
    value: typing.Optional[DialogflowCxTestCaseTestCaseConversationTurnsVirtualAgentOutputTriggeredIntent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ceb2ef6009579048dd31d0b4397e2484e9f5865104ed2e700f37a1cde724600(
    *,
    flow: typing.Optional[builtins.str] = None,
    page: typing.Optional[builtins.str] = None,
    tracking_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4c3b0c076629ff93b672b20f19c46fc58d395ea5d61483e85820311c65b4c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__929f556f40ca1adda166451083e237cffa882279137c3f53dbb99c4ab395c533(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ffa4a98605b2215c3603371981e9acfc4ca08c3edcb59079e8a8cdde7cf7c9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1997f91d32224fc59d227d9e4bc0fce9ef3142d7a8bf45457f70d1a7cca0908b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e54126bd3ba303d96c2c61d6d83e891e2ea1986b43707c06f3010a0699ad58(
    value: typing.Optional[DialogflowCxTestCaseTestConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0718e674a7e95ee798305d8cce76309050dbe1ea3d8b704019323472f3c347c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5272a40793775846973ca1539b9cc5ab0d29e0a52132b823f2f9cb4ecca2f6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e46baf752538a46f27a84c3227062eb27c9bd6989c8475c07810f4308cfd635(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfc5f225cd714d219f7c827a0b3d8fe6687bf473521c4809817d4db74ae2359(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ba8b802c2957efc00901b684b9b9669f011ee37df11e9a96084631a27dd867(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf8d93971861fe3aa739b65129997d23d5c2e31a1f30274b16dff20289987de2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxTestCaseTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

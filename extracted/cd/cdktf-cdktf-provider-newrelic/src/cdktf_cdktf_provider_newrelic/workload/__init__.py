r'''
# `newrelic_workload`

Refer to the Terraform Registry for docs: [`newrelic_workload`](https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload).
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


class Workload(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.workload.Workload",
):
    '''Represents a {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload newrelic_workload}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        entity_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
        entity_search_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadEntitySearchQuery", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        scope_account_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
        status_config_automatic: typing.Optional[typing.Union["WorkloadStatusConfigAutomatic", typing.Dict[builtins.str, typing.Any]]] = None,
        status_config_static: typing.Optional[typing.Union["WorkloadStatusConfigStatic", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload newrelic_workload} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The workload's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#name Workload#name}
        :param account_id: The New Relic account ID where you want to create the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#account_id Workload#account_id}
        :param description: Relevant information about the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#description Workload#description}
        :param entity_guids: A list of entity GUIDs manually assigned to this workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#entity_guids Workload#entity_guids}
        :param entity_search_query: entity_search_query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#entity_search_query Workload#entity_search_query}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#id Workload#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scope_account_ids: A list of account IDs that will be used to get entities from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#scope_account_ids Workload#scope_account_ids}
        :param status_config_automatic: status_config_automatic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#status_config_automatic Workload#status_config_automatic}
        :param status_config_static: status_config_static block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#status_config_static Workload#status_config_static}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c84a24c4f38c3ef30d3f5161cdba9bb64eee076db5f5553a4f809c953ae264)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WorkloadConfig(
            name=name,
            account_id=account_id,
            description=description,
            entity_guids=entity_guids,
            entity_search_query=entity_search_query,
            id=id,
            scope_account_ids=scope_account_ids,
            status_config_automatic=status_config_automatic,
            status_config_static=status_config_static,
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
        '''Generates CDKTF code for importing a Workload resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Workload to import.
        :param import_from_id: The id of the existing Workload that should be imported. Refer to the {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Workload to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78c6d22b46c6d9128e5e557d2d71cd448294ed73678a01e0334002e0965d8a33)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEntitySearchQuery")
    def put_entity_search_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadEntitySearchQuery", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb17858658b02a6b3c791e7cf25d7a79382f62c8cf1b83d4f308394278484be5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEntitySearchQuery", [value]))

    @jsii.member(jsii_name="putStatusConfigAutomatic")
    def put_status_config_automatic(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        remaining_entities_rule: typing.Optional[typing.Union["WorkloadStatusConfigAutomaticRemainingEntitiesRule", typing.Dict[builtins.str, typing.Any]]] = None,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadStatusConfigAutomaticRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Whether the automatic status configuration is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#enabled Workload#enabled}
        :param remaining_entities_rule: remaining_entities_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#remaining_entities_rule Workload#remaining_entities_rule}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#rule Workload#rule}
        '''
        value = WorkloadStatusConfigAutomatic(
            enabled=enabled, remaining_entities_rule=remaining_entities_rule, rule=rule
        )

        return typing.cast(None, jsii.invoke(self, "putStatusConfigAutomatic", [value]))

    @jsii.member(jsii_name="putStatusConfigStatic")
    def put_status_config_static(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        status: builtins.str,
        description: typing.Optional[builtins.str] = None,
        summary: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Whether the static status configuration is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#enabled Workload#enabled}
        :param status: The status of the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#status Workload#status}
        :param description: A description that provides additional details about the status of the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#description Workload#description}
        :param summary: A short description of the status of the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#summary Workload#summary}
        '''
        value = WorkloadStatusConfigStatic(
            enabled=enabled, status=status, description=description, summary=summary
        )

        return typing.cast(None, jsii.invoke(self, "putStatusConfigStatic", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEntityGuids")
    def reset_entity_guids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntityGuids", []))

    @jsii.member(jsii_name="resetEntitySearchQuery")
    def reset_entity_search_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntitySearchQuery", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetScopeAccountIds")
    def reset_scope_account_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopeAccountIds", []))

    @jsii.member(jsii_name="resetStatusConfigAutomatic")
    def reset_status_config_automatic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatusConfigAutomatic", []))

    @jsii.member(jsii_name="resetStatusConfigStatic")
    def reset_status_config_static(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatusConfigStatic", []))

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
    @jsii.member(jsii_name="compositeEntitySearchQuery")
    def composite_entity_search_query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compositeEntitySearchQuery"))

    @builtins.property
    @jsii.member(jsii_name="entitySearchQuery")
    def entity_search_query(self) -> "WorkloadEntitySearchQueryList":
        return typing.cast("WorkloadEntitySearchQueryList", jsii.get(self, "entitySearchQuery"))

    @builtins.property
    @jsii.member(jsii_name="guid")
    def guid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "guid"))

    @builtins.property
    @jsii.member(jsii_name="permalink")
    def permalink(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permalink"))

    @builtins.property
    @jsii.member(jsii_name="statusConfigAutomatic")
    def status_config_automatic(self) -> "WorkloadStatusConfigAutomaticOutputReference":
        return typing.cast("WorkloadStatusConfigAutomaticOutputReference", jsii.get(self, "statusConfigAutomatic"))

    @builtins.property
    @jsii.member(jsii_name="statusConfigStatic")
    def status_config_static(self) -> "WorkloadStatusConfigStaticOutputReference":
        return typing.cast("WorkloadStatusConfigStaticOutputReference", jsii.get(self, "statusConfigStatic"))

    @builtins.property
    @jsii.member(jsii_name="workloadId")
    def workload_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "workloadId"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="entityGuidsInput")
    def entity_guids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "entityGuidsInput"))

    @builtins.property
    @jsii.member(jsii_name="entitySearchQueryInput")
    def entity_search_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadEntitySearchQuery"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadEntitySearchQuery"]]], jsii.get(self, "entitySearchQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeAccountIdsInput")
    def scope_account_ids_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "scopeAccountIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="statusConfigAutomaticInput")
    def status_config_automatic_input(
        self,
    ) -> typing.Optional["WorkloadStatusConfigAutomatic"]:
        return typing.cast(typing.Optional["WorkloadStatusConfigAutomatic"], jsii.get(self, "statusConfigAutomaticInput"))

    @builtins.property
    @jsii.member(jsii_name="statusConfigStaticInput")
    def status_config_static_input(
        self,
    ) -> typing.Optional["WorkloadStatusConfigStatic"]:
        return typing.cast(typing.Optional["WorkloadStatusConfigStatic"], jsii.get(self, "statusConfigStaticInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f64f29e8b77dcac4dc81e8ed6edbfdc4b69cce6938cd39e6788ef28800aa1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e452871bb43697a03da988af42e1a30e7c56279491d4eba9192e0ad0ada2e9e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entityGuids")
    def entity_guids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "entityGuids"))

    @entity_guids.setter
    def entity_guids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22e993a3e82122b8a6089a8111a0d64f78c63ed07f0bbe27820d196b1a6fe0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityGuids", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcb7a581ec502adf3f10f8047f27e330fffecef68635038c2291612a36a9b4c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3d83898b029370510bb0b9c6c66b56d62e62b91d356761744ff0b2085d2a29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopeAccountIds")
    def scope_account_ids(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "scopeAccountIds"))

    @scope_account_ids.setter
    def scope_account_ids(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10cc920a500c17b05d61f7039394ee3e0f4ecf223e34db0fe3cecea94b153a7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopeAccountIds", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "account_id": "accountId",
        "description": "description",
        "entity_guids": "entityGuids",
        "entity_search_query": "entitySearchQuery",
        "id": "id",
        "scope_account_ids": "scopeAccountIds",
        "status_config_automatic": "statusConfigAutomatic",
        "status_config_static": "statusConfigStatic",
    },
)
class WorkloadConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        entity_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
        entity_search_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadEntitySearchQuery", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        scope_account_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
        status_config_automatic: typing.Optional[typing.Union["WorkloadStatusConfigAutomatic", typing.Dict[builtins.str, typing.Any]]] = None,
        status_config_static: typing.Optional[typing.Union["WorkloadStatusConfigStatic", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The workload's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#name Workload#name}
        :param account_id: The New Relic account ID where you want to create the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#account_id Workload#account_id}
        :param description: Relevant information about the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#description Workload#description}
        :param entity_guids: A list of entity GUIDs manually assigned to this workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#entity_guids Workload#entity_guids}
        :param entity_search_query: entity_search_query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#entity_search_query Workload#entity_search_query}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#id Workload#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scope_account_ids: A list of account IDs that will be used to get entities from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#scope_account_ids Workload#scope_account_ids}
        :param status_config_automatic: status_config_automatic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#status_config_automatic Workload#status_config_automatic}
        :param status_config_static: status_config_static block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#status_config_static Workload#status_config_static}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(status_config_automatic, dict):
            status_config_automatic = WorkloadStatusConfigAutomatic(**status_config_automatic)
        if isinstance(status_config_static, dict):
            status_config_static = WorkloadStatusConfigStatic(**status_config_static)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e9848cc3752655143f1f3c6f4e14c2f25eb5892d5f91b7a145f9cb469c1753)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument entity_guids", value=entity_guids, expected_type=type_hints["entity_guids"])
            check_type(argname="argument entity_search_query", value=entity_search_query, expected_type=type_hints["entity_search_query"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument scope_account_ids", value=scope_account_ids, expected_type=type_hints["scope_account_ids"])
            check_type(argname="argument status_config_automatic", value=status_config_automatic, expected_type=type_hints["status_config_automatic"])
            check_type(argname="argument status_config_static", value=status_config_static, expected_type=type_hints["status_config_static"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if description is not None:
            self._values["description"] = description
        if entity_guids is not None:
            self._values["entity_guids"] = entity_guids
        if entity_search_query is not None:
            self._values["entity_search_query"] = entity_search_query
        if id is not None:
            self._values["id"] = id
        if scope_account_ids is not None:
            self._values["scope_account_ids"] = scope_account_ids
        if status_config_automatic is not None:
            self._values["status_config_automatic"] = status_config_automatic
        if status_config_static is not None:
            self._values["status_config_static"] = status_config_static

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
    def name(self) -> builtins.str:
        '''The workload's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#name Workload#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The New Relic account ID where you want to create the workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#account_id Workload#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Relevant information about the workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#description Workload#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entity_guids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of entity GUIDs manually assigned to this workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#entity_guids Workload#entity_guids}
        '''
        result = self._values.get("entity_guids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def entity_search_query(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadEntitySearchQuery"]]]:
        '''entity_search_query block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#entity_search_query Workload#entity_search_query}
        '''
        result = self._values.get("entity_search_query")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadEntitySearchQuery"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#id Workload#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope_account_ids(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''A list of account IDs that will be used to get entities from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#scope_account_ids Workload#scope_account_ids}
        '''
        result = self._values.get("scope_account_ids")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def status_config_automatic(
        self,
    ) -> typing.Optional["WorkloadStatusConfigAutomatic"]:
        '''status_config_automatic block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#status_config_automatic Workload#status_config_automatic}
        '''
        result = self._values.get("status_config_automatic")
        return typing.cast(typing.Optional["WorkloadStatusConfigAutomatic"], result)

    @builtins.property
    def status_config_static(self) -> typing.Optional["WorkloadStatusConfigStatic"]:
        '''status_config_static block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#status_config_static Workload#status_config_static}
        '''
        result = self._values.get("status_config_static")
        return typing.cast(typing.Optional["WorkloadStatusConfigStatic"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadEntitySearchQuery",
    jsii_struct_bases=[],
    name_mapping={"query": "query"},
)
class WorkloadEntitySearchQuery:
    def __init__(self, *, query: builtins.str) -> None:
        '''
        :param query: A valid entity search query; empty, and null values are considered invalid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#query Workload#query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b47eb6b510709dcb2f9bd4bae146c7c9048634fccc5ef6faad90d4dbc20f93fc)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }

    @builtins.property
    def query(self) -> builtins.str:
        '''A valid entity search query; empty, and null values are considered invalid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#query Workload#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadEntitySearchQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadEntitySearchQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadEntitySearchQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31c933d2e1d5d8ebccdabb9a57e77fa892e9065b61fe94f58636298abe53cc80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "WorkloadEntitySearchQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a041998e3afd8ed15d59d686004f995bd19d03432802d33f2045fdab5e7c51af)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkloadEntitySearchQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fb1c3487b1cf34f0f6e2a70043e3b2a76ae600f83cd8f30659693e8b1385048)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10131cc491359787f5d3503316c4903e23f73ae6e4f9a26c7721fb6ff800d382)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3b0469a80f16eab2aa0986ff4123f4151b80bbf94d63dc4c9d9fccc912d245f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadEntitySearchQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadEntitySearchQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadEntitySearchQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8701122b569fdd7f87d80606b66cc5bfe2a86a3ae655c08df58a4ac01b6643e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadEntitySearchQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadEntitySearchQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9da2a036c12c889cde97236c510ab8f025bd4cfe991d798482b5a203f9fc949)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff3cee74a1cd8f1bcb90c67bdd29dbdc55822982be37eeb015b4e0ee7eaf99f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadEntitySearchQuery]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadEntitySearchQuery]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadEntitySearchQuery]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a601811cdf27e053bd0be642a1a5a2438f10a4eadb962ccfea69d3b207a9b91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadStatusConfigAutomatic",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "remaining_entities_rule": "remainingEntitiesRule",
        "rule": "rule",
    },
)
class WorkloadStatusConfigAutomatic:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        remaining_entities_rule: typing.Optional[typing.Union["WorkloadStatusConfigAutomaticRemainingEntitiesRule", typing.Dict[builtins.str, typing.Any]]] = None,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadStatusConfigAutomaticRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Whether the automatic status configuration is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#enabled Workload#enabled}
        :param remaining_entities_rule: remaining_entities_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#remaining_entities_rule Workload#remaining_entities_rule}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#rule Workload#rule}
        '''
        if isinstance(remaining_entities_rule, dict):
            remaining_entities_rule = WorkloadStatusConfigAutomaticRemainingEntitiesRule(**remaining_entities_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c2515c514f218c4bbd6e06fbe688e90f3f266e1be20061b5c16bc08bdcbaeff)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument remaining_entities_rule", value=remaining_entities_rule, expected_type=type_hints["remaining_entities_rule"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if remaining_entities_rule is not None:
            self._values["remaining_entities_rule"] = remaining_entities_rule
        if rule is not None:
            self._values["rule"] = rule

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the automatic status configuration is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#enabled Workload#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def remaining_entities_rule(
        self,
    ) -> typing.Optional["WorkloadStatusConfigAutomaticRemainingEntitiesRule"]:
        '''remaining_entities_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#remaining_entities_rule Workload#remaining_entities_rule}
        '''
        result = self._values.get("remaining_entities_rule")
        return typing.cast(typing.Optional["WorkloadStatusConfigAutomaticRemainingEntitiesRule"], result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadStatusConfigAutomaticRule"]]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#rule Workload#rule}
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadStatusConfigAutomaticRule"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadStatusConfigAutomatic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadStatusConfigAutomaticOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadStatusConfigAutomaticOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5162026445a3a548406de0b758d802b8ffa1e4d0112fb717b784a0513abcbbc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRemainingEntitiesRule")
    def put_remaining_entities_rule(
        self,
        *,
        remaining_entities_rule_rollup: typing.Union["WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollup", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param remaining_entities_rule_rollup: remaining_entities_rule_rollup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#remaining_entities_rule_rollup Workload#remaining_entities_rule_rollup}
        '''
        value = WorkloadStatusConfigAutomaticRemainingEntitiesRule(
            remaining_entities_rule_rollup=remaining_entities_rule_rollup
        )

        return typing.cast(None, jsii.invoke(self, "putRemainingEntitiesRule", [value]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadStatusConfigAutomaticRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18096890087264eafe7311936d2092525586af1d1db7e7fff54a7d9cfbd6185b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="resetRemainingEntitiesRule")
    def reset_remaining_entities_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemainingEntitiesRule", []))

    @jsii.member(jsii_name="resetRule")
    def reset_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRule", []))

    @builtins.property
    @jsii.member(jsii_name="remainingEntitiesRule")
    def remaining_entities_rule(
        self,
    ) -> "WorkloadStatusConfigAutomaticRemainingEntitiesRuleOutputReference":
        return typing.cast("WorkloadStatusConfigAutomaticRemainingEntitiesRuleOutputReference", jsii.get(self, "remainingEntitiesRule"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "WorkloadStatusConfigAutomaticRuleList":
        return typing.cast("WorkloadStatusConfigAutomaticRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="remainingEntitiesRuleInput")
    def remaining_entities_rule_input(
        self,
    ) -> typing.Optional["WorkloadStatusConfigAutomaticRemainingEntitiesRule"]:
        return typing.cast(typing.Optional["WorkloadStatusConfigAutomaticRemainingEntitiesRule"], jsii.get(self, "remainingEntitiesRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadStatusConfigAutomaticRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadStatusConfigAutomaticRule"]]], jsii.get(self, "ruleInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8823c1d7f4bde019c39b1567602666fd451a4038b52d360bb4a9083d62a78337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WorkloadStatusConfigAutomatic]:
        return typing.cast(typing.Optional[WorkloadStatusConfigAutomatic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadStatusConfigAutomatic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0bd1d5527190c496f9940f6bdfe1c2b56dc1b2b44b0cbd8a3bfc09fbd3cd775)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadStatusConfigAutomaticRemainingEntitiesRule",
    jsii_struct_bases=[],
    name_mapping={"remaining_entities_rule_rollup": "remainingEntitiesRuleRollup"},
)
class WorkloadStatusConfigAutomaticRemainingEntitiesRule:
    def __init__(
        self,
        *,
        remaining_entities_rule_rollup: typing.Union["WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollup", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param remaining_entities_rule_rollup: remaining_entities_rule_rollup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#remaining_entities_rule_rollup Workload#remaining_entities_rule_rollup}
        '''
        if isinstance(remaining_entities_rule_rollup, dict):
            remaining_entities_rule_rollup = WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollup(**remaining_entities_rule_rollup)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5314b4bb73a0fb82c8082b752eb4ad533e3e7864ec0b8693c61090c845526864)
            check_type(argname="argument remaining_entities_rule_rollup", value=remaining_entities_rule_rollup, expected_type=type_hints["remaining_entities_rule_rollup"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "remaining_entities_rule_rollup": remaining_entities_rule_rollup,
        }

    @builtins.property
    def remaining_entities_rule_rollup(
        self,
    ) -> "WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollup":
        '''remaining_entities_rule_rollup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#remaining_entities_rule_rollup Workload#remaining_entities_rule_rollup}
        '''
        result = self._values.get("remaining_entities_rule_rollup")
        assert result is not None, "Required property 'remaining_entities_rule_rollup' is missing"
        return typing.cast("WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollup", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadStatusConfigAutomaticRemainingEntitiesRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadStatusConfigAutomaticRemainingEntitiesRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadStatusConfigAutomaticRemainingEntitiesRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31822ab35bc63a90a9f9e9def7a5f1c09ccce1232b777e1e36e6e29bcecb68d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRemainingEntitiesRuleRollup")
    def put_remaining_entities_rule_rollup(
        self,
        *,
        group_by: builtins.str,
        strategy: builtins.str,
        threshold_type: typing.Optional[builtins.str] = None,
        threshold_value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param group_by: The grouping to be applied to the remaining entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#group_by Workload#group_by}
        :param strategy: The rollup strategy that is applied to a group of entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#strategy Workload#strategy}
        :param threshold_type: Type of threshold defined for the rule. This is an optional field that only applies when strategy is WORST_STATUS_WINS. Use a threshold to roll up the worst status only after a certain amount of entities are not operational. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#threshold_type Workload#threshold_type}
        :param threshold_value: Threshold value defined for the rule. This optional field is used in combination with thresholdType. If the threshold type is null, the threshold value will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#threshold_value Workload#threshold_value}
        '''
        value = WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollup(
            group_by=group_by,
            strategy=strategy,
            threshold_type=threshold_type,
            threshold_value=threshold_value,
        )

        return typing.cast(None, jsii.invoke(self, "putRemainingEntitiesRuleRollup", [value]))

    @builtins.property
    @jsii.member(jsii_name="remainingEntitiesRuleRollup")
    def remaining_entities_rule_rollup(
        self,
    ) -> "WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollupOutputReference":
        return typing.cast("WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollupOutputReference", jsii.get(self, "remainingEntitiesRuleRollup"))

    @builtins.property
    @jsii.member(jsii_name="remainingEntitiesRuleRollupInput")
    def remaining_entities_rule_rollup_input(
        self,
    ) -> typing.Optional["WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollup"]:
        return typing.cast(typing.Optional["WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollup"], jsii.get(self, "remainingEntitiesRuleRollupInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadStatusConfigAutomaticRemainingEntitiesRule]:
        return typing.cast(typing.Optional[WorkloadStatusConfigAutomaticRemainingEntitiesRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadStatusConfigAutomaticRemainingEntitiesRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc9e02fb1f7e2a9cc4eb96eb13ac7eb957d99290580259e08b08a680f49b098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollup",
    jsii_struct_bases=[],
    name_mapping={
        "group_by": "groupBy",
        "strategy": "strategy",
        "threshold_type": "thresholdType",
        "threshold_value": "thresholdValue",
    },
)
class WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollup:
    def __init__(
        self,
        *,
        group_by: builtins.str,
        strategy: builtins.str,
        threshold_type: typing.Optional[builtins.str] = None,
        threshold_value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param group_by: The grouping to be applied to the remaining entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#group_by Workload#group_by}
        :param strategy: The rollup strategy that is applied to a group of entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#strategy Workload#strategy}
        :param threshold_type: Type of threshold defined for the rule. This is an optional field that only applies when strategy is WORST_STATUS_WINS. Use a threshold to roll up the worst status only after a certain amount of entities are not operational. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#threshold_type Workload#threshold_type}
        :param threshold_value: Threshold value defined for the rule. This optional field is used in combination with thresholdType. If the threshold type is null, the threshold value will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#threshold_value Workload#threshold_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f3f45e15175ebaf1fa56327dbe4843f48ee615a4b65d97222926e15e258952)
            check_type(argname="argument group_by", value=group_by, expected_type=type_hints["group_by"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument threshold_type", value=threshold_type, expected_type=type_hints["threshold_type"])
            check_type(argname="argument threshold_value", value=threshold_value, expected_type=type_hints["threshold_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_by": group_by,
            "strategy": strategy,
        }
        if threshold_type is not None:
            self._values["threshold_type"] = threshold_type
        if threshold_value is not None:
            self._values["threshold_value"] = threshold_value

    @builtins.property
    def group_by(self) -> builtins.str:
        '''The grouping to be applied to the remaining entities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#group_by Workload#group_by}
        '''
        result = self._values.get("group_by")
        assert result is not None, "Required property 'group_by' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def strategy(self) -> builtins.str:
        '''The rollup strategy that is applied to a group of entities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#strategy Workload#strategy}
        '''
        result = self._values.get("strategy")
        assert result is not None, "Required property 'strategy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def threshold_type(self) -> typing.Optional[builtins.str]:
        '''Type of threshold defined for the rule.

        This is an optional field that only applies when strategy is WORST_STATUS_WINS. Use a threshold to roll up the worst status only after a certain amount of entities are not operational.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#threshold_type Workload#threshold_type}
        '''
        result = self._values.get("threshold_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold_value(self) -> typing.Optional[jsii.Number]:
        '''Threshold value defined for the rule.

        This optional field is used in combination with thresholdType. If the threshold type is null, the threshold value will be ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#threshold_value Workload#threshold_value}
        '''
        result = self._values.get("threshold_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d74747a6ae642cc46ca21a29ab56ed369efa2f34e55a1a69005e2b14a402534)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetThresholdType")
    def reset_threshold_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThresholdType", []))

    @jsii.member(jsii_name="resetThresholdValue")
    def reset_threshold_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThresholdValue", []))

    @builtins.property
    @jsii.member(jsii_name="groupByInput")
    def group_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupByInput"))

    @builtins.property
    @jsii.member(jsii_name="strategyInput")
    def strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "strategyInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdTypeInput")
    def threshold_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thresholdTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdValueInput")
    def threshold_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdValueInput"))

    @builtins.property
    @jsii.member(jsii_name="groupBy")
    def group_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupBy"))

    @group_by.setter
    def group_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e622d102ac623c1cbcc692fd655f79a75354fd8e4c48b874a12412760b95c34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "strategy"))

    @strategy.setter
    def strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ecfb2c7a9b85d9c81f611cf1cfa2099abd6a90fefe59b0ba13b4197e7fd42df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdType")
    def threshold_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thresholdType"))

    @threshold_type.setter
    def threshold_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6a6b1e120dad2775d61dc1182a5edf8e300045e5b48520db8ee65e1d975f9bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdValue")
    def threshold_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "thresholdValue"))

    @threshold_value.setter
    def threshold_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__359fa9e9275bbfd5ca6452112364aabdfc5ac1a6a41659a8f5cfe2553ff5788b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollup]:
        return typing.cast(typing.Optional[WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__752888c871c2ceb8a67efcebb6de2b3611bc9a3b5fc3fda9423c005ecba23bbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadStatusConfigAutomaticRule",
    jsii_struct_bases=[],
    name_mapping={
        "rollup": "rollup",
        "entity_guids": "entityGuids",
        "nrql_query": "nrqlQuery",
    },
)
class WorkloadStatusConfigAutomaticRule:
    def __init__(
        self,
        *,
        rollup: typing.Union["WorkloadStatusConfigAutomaticRuleRollup", typing.Dict[builtins.str, typing.Any]],
        entity_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
        nrql_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadStatusConfigAutomaticRuleNrqlQuery", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param rollup: rollup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#rollup Workload#rollup}
        :param entity_guids: A list of entity GUIDs composing the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#entity_guids Workload#entity_guids}
        :param nrql_query: nrql_query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#nrql_query Workload#nrql_query}
        '''
        if isinstance(rollup, dict):
            rollup = WorkloadStatusConfigAutomaticRuleRollup(**rollup)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41f361068868bd2a6637ba556b24ec47b634b1924c2fb3483e7b1e4fc6b54407)
            check_type(argname="argument rollup", value=rollup, expected_type=type_hints["rollup"])
            check_type(argname="argument entity_guids", value=entity_guids, expected_type=type_hints["entity_guids"])
            check_type(argname="argument nrql_query", value=nrql_query, expected_type=type_hints["nrql_query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rollup": rollup,
        }
        if entity_guids is not None:
            self._values["entity_guids"] = entity_guids
        if nrql_query is not None:
            self._values["nrql_query"] = nrql_query

    @builtins.property
    def rollup(self) -> "WorkloadStatusConfigAutomaticRuleRollup":
        '''rollup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#rollup Workload#rollup}
        '''
        result = self._values.get("rollup")
        assert result is not None, "Required property 'rollup' is missing"
        return typing.cast("WorkloadStatusConfigAutomaticRuleRollup", result)

    @builtins.property
    def entity_guids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of entity GUIDs composing the rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#entity_guids Workload#entity_guids}
        '''
        result = self._values.get("entity_guids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def nrql_query(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadStatusConfigAutomaticRuleNrqlQuery"]]]:
        '''nrql_query block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#nrql_query Workload#nrql_query}
        '''
        result = self._values.get("nrql_query")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadStatusConfigAutomaticRuleNrqlQuery"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadStatusConfigAutomaticRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadStatusConfigAutomaticRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadStatusConfigAutomaticRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fb61d3574b504126d166ed0a8d2b9d4ed5ea6f304fbbbf6121de68a250af5c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkloadStatusConfigAutomaticRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48b4a88a72fa26babb5a06a83ebdcda50e603b03542a399701821a4beb6ea32b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkloadStatusConfigAutomaticRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32daf9bb35b9c0da7d97c2bbf2618fb7f3d4b6122a43e245284924bdc63b7a72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e77b9b24ae121736eb776f444bb19afcc7dc9ddc690946a662ffcb238dd72b2e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15c806b99f3b8f54f1d270c200f19fc9226d640a1742cc1c2b77c04d5fb2f81d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadStatusConfigAutomaticRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadStatusConfigAutomaticRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadStatusConfigAutomaticRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e23990a661fea84b76ca361a167dc982b39132488181441042b90ce21ca20b8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadStatusConfigAutomaticRuleNrqlQuery",
    jsii_struct_bases=[],
    name_mapping={"query": "query"},
)
class WorkloadStatusConfigAutomaticRuleNrqlQuery:
    def __init__(self, *, query: builtins.str) -> None:
        '''
        :param query: The entity search query that is used to perform the search of a group of entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#query Workload#query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ddc5ab23486a42232d9d2dc1d674e88e10fbe9c8619ffbb0df085680967eeac)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }

    @builtins.property
    def query(self) -> builtins.str:
        '''The entity search query that is used to perform the search of a group of entities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#query Workload#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadStatusConfigAutomaticRuleNrqlQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadStatusConfigAutomaticRuleNrqlQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadStatusConfigAutomaticRuleNrqlQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4e43e15633fc50a339efd11fac6bcef2c9a8387c742db11f61b7ad56d792379)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkloadStatusConfigAutomaticRuleNrqlQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aa0163ced0b78e5940343a473a22cf42a82720d62305e4151b3b87901c2d010)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkloadStatusConfigAutomaticRuleNrqlQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__595d20a2e4e9e80892cf7b347e76d9eb2c5c5d1e48f2008702830637690ea715)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b08bd6e7e96805d98e2691e1425ccf4775ed555e9554168bfa2eab1c573142b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dec2b7647bc781c2547acf2ce0da5ec7d27923c693d4502153e14d101973c6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadStatusConfigAutomaticRuleNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadStatusConfigAutomaticRuleNrqlQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadStatusConfigAutomaticRuleNrqlQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edde305bbc4968404d9451a935062a593a3d26c67c11d48a52bd88706d4b1bea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadStatusConfigAutomaticRuleNrqlQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadStatusConfigAutomaticRuleNrqlQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d56055ce40c8f9dce766fc0c781111cb49cb75a1809cabaf9b7dedff56193202)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a8ef9343d8e6b9a42c9907c268e80f159c2a373a762b9c287b7d1b5ded43bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadStatusConfigAutomaticRuleNrqlQuery]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadStatusConfigAutomaticRuleNrqlQuery]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadStatusConfigAutomaticRuleNrqlQuery]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ec3cb5aec6bfec5710948eb8c968dc5f1834c3253988a45279b26aae2eaee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadStatusConfigAutomaticRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadStatusConfigAutomaticRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe17e8e5d6ed3b7d893f77b47d7ee4ea94f59be067d20fa947e36046abd85dad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNrqlQuery")
    def put_nrql_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadStatusConfigAutomaticRuleNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da1f4a5f75a317c3ad97f6cc99ddd013608c456a6ef44aba16a3c8a864ab0c62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNrqlQuery", [value]))

    @jsii.member(jsii_name="putRollup")
    def put_rollup(
        self,
        *,
        strategy: builtins.str,
        threshold_type: typing.Optional[builtins.str] = None,
        threshold_value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param strategy: The rollup strategy that is applied to a group of entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#strategy Workload#strategy}
        :param threshold_type: Type of threshold defined for the rule. This is an optional field that only applies when strategy is WORST_STATUS_WINS. Use a threshold to roll up the worst status only after a certain amount of entities are not operational. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#threshold_type Workload#threshold_type}
        :param threshold_value: Threshold value defined for the rule. This optional field is used in combination with thresholdType. If the threshold type is null, the threshold value will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#threshold_value Workload#threshold_value}
        '''
        value = WorkloadStatusConfigAutomaticRuleRollup(
            strategy=strategy,
            threshold_type=threshold_type,
            threshold_value=threshold_value,
        )

        return typing.cast(None, jsii.invoke(self, "putRollup", [value]))

    @jsii.member(jsii_name="resetEntityGuids")
    def reset_entity_guids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntityGuids", []))

    @jsii.member(jsii_name="resetNrqlQuery")
    def reset_nrql_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNrqlQuery", []))

    @builtins.property
    @jsii.member(jsii_name="nrqlQuery")
    def nrql_query(self) -> WorkloadStatusConfigAutomaticRuleNrqlQueryList:
        return typing.cast(WorkloadStatusConfigAutomaticRuleNrqlQueryList, jsii.get(self, "nrqlQuery"))

    @builtins.property
    @jsii.member(jsii_name="rollup")
    def rollup(self) -> "WorkloadStatusConfigAutomaticRuleRollupOutputReference":
        return typing.cast("WorkloadStatusConfigAutomaticRuleRollupOutputReference", jsii.get(self, "rollup"))

    @builtins.property
    @jsii.member(jsii_name="entityGuidsInput")
    def entity_guids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "entityGuidsInput"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQueryInput")
    def nrql_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadStatusConfigAutomaticRuleNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadStatusConfigAutomaticRuleNrqlQuery]]], jsii.get(self, "nrqlQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="rollupInput")
    def rollup_input(
        self,
    ) -> typing.Optional["WorkloadStatusConfigAutomaticRuleRollup"]:
        return typing.cast(typing.Optional["WorkloadStatusConfigAutomaticRuleRollup"], jsii.get(self, "rollupInput"))

    @builtins.property
    @jsii.member(jsii_name="entityGuids")
    def entity_guids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "entityGuids"))

    @entity_guids.setter
    def entity_guids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac5323aff2231a657cf46202657699f8aa2d712511e123821175ede864c84f1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityGuids", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadStatusConfigAutomaticRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadStatusConfigAutomaticRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadStatusConfigAutomaticRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce312e80012a60299b3cef16dd3ce41e7cbae1ef0e4fd30e373fd4df344f917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadStatusConfigAutomaticRuleRollup",
    jsii_struct_bases=[],
    name_mapping={
        "strategy": "strategy",
        "threshold_type": "thresholdType",
        "threshold_value": "thresholdValue",
    },
)
class WorkloadStatusConfigAutomaticRuleRollup:
    def __init__(
        self,
        *,
        strategy: builtins.str,
        threshold_type: typing.Optional[builtins.str] = None,
        threshold_value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param strategy: The rollup strategy that is applied to a group of entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#strategy Workload#strategy}
        :param threshold_type: Type of threshold defined for the rule. This is an optional field that only applies when strategy is WORST_STATUS_WINS. Use a threshold to roll up the worst status only after a certain amount of entities are not operational. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#threshold_type Workload#threshold_type}
        :param threshold_value: Threshold value defined for the rule. This optional field is used in combination with thresholdType. If the threshold type is null, the threshold value will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#threshold_value Workload#threshold_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__498c7b5ea1bd945eaf6204c90473fa9d1bf4b2e7ded651d98efe0cac8094e786)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument threshold_type", value=threshold_type, expected_type=type_hints["threshold_type"])
            check_type(argname="argument threshold_value", value=threshold_value, expected_type=type_hints["threshold_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "strategy": strategy,
        }
        if threshold_type is not None:
            self._values["threshold_type"] = threshold_type
        if threshold_value is not None:
            self._values["threshold_value"] = threshold_value

    @builtins.property
    def strategy(self) -> builtins.str:
        '''The rollup strategy that is applied to a group of entities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#strategy Workload#strategy}
        '''
        result = self._values.get("strategy")
        assert result is not None, "Required property 'strategy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def threshold_type(self) -> typing.Optional[builtins.str]:
        '''Type of threshold defined for the rule.

        This is an optional field that only applies when strategy is WORST_STATUS_WINS. Use a threshold to roll up the worst status only after a certain amount of entities are not operational.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#threshold_type Workload#threshold_type}
        '''
        result = self._values.get("threshold_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold_value(self) -> typing.Optional[jsii.Number]:
        '''Threshold value defined for the rule.

        This optional field is used in combination with thresholdType. If the threshold type is null, the threshold value will be ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#threshold_value Workload#threshold_value}
        '''
        result = self._values.get("threshold_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadStatusConfigAutomaticRuleRollup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadStatusConfigAutomaticRuleRollupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadStatusConfigAutomaticRuleRollupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ccbb3f918b53ab34d02f4e253321a2897cdfbfae74351963036e487a3354c24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetThresholdType")
    def reset_threshold_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThresholdType", []))

    @jsii.member(jsii_name="resetThresholdValue")
    def reset_threshold_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThresholdValue", []))

    @builtins.property
    @jsii.member(jsii_name="strategyInput")
    def strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "strategyInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdTypeInput")
    def threshold_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thresholdTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdValueInput")
    def threshold_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdValueInput"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "strategy"))

    @strategy.setter
    def strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e25819db48550f4f8d936b69a96c349126d01a1c8619378a82fcf327aa9ac48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdType")
    def threshold_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thresholdType"))

    @threshold_type.setter
    def threshold_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa28ed6dae3045fa494aaf8db38bc0216f4f843fdd939e1da6828056d3f82f46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdValue")
    def threshold_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "thresholdValue"))

    @threshold_value.setter
    def threshold_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0bc9a5fc8030cb8274813da1950a181cdbf1553a203bc1642d9ceb4fe81a839)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadStatusConfigAutomaticRuleRollup]:
        return typing.cast(typing.Optional[WorkloadStatusConfigAutomaticRuleRollup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadStatusConfigAutomaticRuleRollup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95e5e6e3e1c149678bea9f6f49004128823e02fae89fb08494a71e2814984cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadStatusConfigStatic",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "status": "status",
        "description": "description",
        "summary": "summary",
    },
)
class WorkloadStatusConfigStatic:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        status: builtins.str,
        description: typing.Optional[builtins.str] = None,
        summary: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Whether the static status configuration is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#enabled Workload#enabled}
        :param status: The status of the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#status Workload#status}
        :param description: A description that provides additional details about the status of the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#description Workload#description}
        :param summary: A short description of the status of the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#summary Workload#summary}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94baa187d886028ef781ffa38a0e99d757889751620b355d227fdd2a830c94bc)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument summary", value=summary, expected_type=type_hints["summary"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "status": status,
        }
        if description is not None:
            self._values["description"] = description
        if summary is not None:
            self._values["summary"] = summary

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the static status configuration is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#enabled Workload#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def status(self) -> builtins.str:
        '''The status of the workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#status Workload#status}
        '''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description that provides additional details about the status of the workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#description Workload#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def summary(self) -> typing.Optional[builtins.str]:
        '''A short description of the status of the workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/workload#summary Workload#summary}
        '''
        result = self._values.get("summary")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadStatusConfigStatic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadStatusConfigStaticOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.workload.WorkloadStatusConfigStaticOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9bd2eceb2bb857363d284270aa646db73a3c1e383d8231ed6c50f80eb6a8c38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetSummary")
    def reset_summary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSummary", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="summaryInput")
    def summary_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "summaryInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e4eb4cca5772c9e589dd2cc7de05cd2c7106093f1e0e925b16ac31a3afc4293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__c7bcbc6f3d04b5b4dfbddd2a37f9a13914c4331436ab22fbcff45c9b0e720013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1610bfad7b40a2217467e83a66f62ce394932a51841b92cce9b31480eb3fe40d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="summary")
    def summary(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "summary"))

    @summary.setter
    def summary(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b99857a13f20750dbd7fb743f80f895d11bc2530b4efc8989c23ed4a83f7e1cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "summary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WorkloadStatusConfigStatic]:
        return typing.cast(typing.Optional[WorkloadStatusConfigStatic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadStatusConfigStatic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d2200aa0b1f9169fafa72d1809a856b9932aade3a892e04de16455b10bc660e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Workload",
    "WorkloadConfig",
    "WorkloadEntitySearchQuery",
    "WorkloadEntitySearchQueryList",
    "WorkloadEntitySearchQueryOutputReference",
    "WorkloadStatusConfigAutomatic",
    "WorkloadStatusConfigAutomaticOutputReference",
    "WorkloadStatusConfigAutomaticRemainingEntitiesRule",
    "WorkloadStatusConfigAutomaticRemainingEntitiesRuleOutputReference",
    "WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollup",
    "WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollupOutputReference",
    "WorkloadStatusConfigAutomaticRule",
    "WorkloadStatusConfigAutomaticRuleList",
    "WorkloadStatusConfigAutomaticRuleNrqlQuery",
    "WorkloadStatusConfigAutomaticRuleNrqlQueryList",
    "WorkloadStatusConfigAutomaticRuleNrqlQueryOutputReference",
    "WorkloadStatusConfigAutomaticRuleOutputReference",
    "WorkloadStatusConfigAutomaticRuleRollup",
    "WorkloadStatusConfigAutomaticRuleRollupOutputReference",
    "WorkloadStatusConfigStatic",
    "WorkloadStatusConfigStaticOutputReference",
]

publication.publish()

def _typecheckingstub__13c84a24c4f38c3ef30d3f5161cdba9bb64eee076db5f5553a4f809c953ae264(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    entity_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
    entity_search_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadEntitySearchQuery, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    scope_account_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
    status_config_automatic: typing.Optional[typing.Union[WorkloadStatusConfigAutomatic, typing.Dict[builtins.str, typing.Any]]] = None,
    status_config_static: typing.Optional[typing.Union[WorkloadStatusConfigStatic, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__78c6d22b46c6d9128e5e557d2d71cd448294ed73678a01e0334002e0965d8a33(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb17858658b02a6b3c791e7cf25d7a79382f62c8cf1b83d4f308394278484be5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadEntitySearchQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f64f29e8b77dcac4dc81e8ed6edbfdc4b69cce6938cd39e6788ef28800aa1f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e452871bb43697a03da988af42e1a30e7c56279491d4eba9192e0ad0ada2e9e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22e993a3e82122b8a6089a8111a0d64f78c63ed07f0bbe27820d196b1a6fe0c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb7a581ec502adf3f10f8047f27e330fffecef68635038c2291612a36a9b4c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3d83898b029370510bb0b9c6c66b56d62e62b91d356761744ff0b2085d2a29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10cc920a500c17b05d61f7039394ee3e0f4ecf223e34db0fe3cecea94b153a7c(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e9848cc3752655143f1f3c6f4e14c2f25eb5892d5f91b7a145f9cb469c1753(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    entity_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
    entity_search_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadEntitySearchQuery, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    scope_account_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
    status_config_automatic: typing.Optional[typing.Union[WorkloadStatusConfigAutomatic, typing.Dict[builtins.str, typing.Any]]] = None,
    status_config_static: typing.Optional[typing.Union[WorkloadStatusConfigStatic, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47eb6b510709dcb2f9bd4bae146c7c9048634fccc5ef6faad90d4dbc20f93fc(
    *,
    query: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c933d2e1d5d8ebccdabb9a57e77fa892e9065b61fe94f58636298abe53cc80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a041998e3afd8ed15d59d686004f995bd19d03432802d33f2045fdab5e7c51af(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb1c3487b1cf34f0f6e2a70043e3b2a76ae600f83cd8f30659693e8b1385048(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10131cc491359787f5d3503316c4903e23f73ae6e4f9a26c7721fb6ff800d382(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b0469a80f16eab2aa0986ff4123f4151b80bbf94d63dc4c9d9fccc912d245f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8701122b569fdd7f87d80606b66cc5bfe2a86a3ae655c08df58a4ac01b6643e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadEntitySearchQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9da2a036c12c889cde97236c510ab8f025bd4cfe991d798482b5a203f9fc949(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff3cee74a1cd8f1bcb90c67bdd29dbdc55822982be37eeb015b4e0ee7eaf99f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a601811cdf27e053bd0be642a1a5a2438f10a4eadb962ccfea69d3b207a9b91(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadEntitySearchQuery]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2515c514f218c4bbd6e06fbe688e90f3f266e1be20061b5c16bc08bdcbaeff(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    remaining_entities_rule: typing.Optional[typing.Union[WorkloadStatusConfigAutomaticRemainingEntitiesRule, typing.Dict[builtins.str, typing.Any]]] = None,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadStatusConfigAutomaticRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5162026445a3a548406de0b758d802b8ffa1e4d0112fb717b784a0513abcbbc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18096890087264eafe7311936d2092525586af1d1db7e7fff54a7d9cfbd6185b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadStatusConfigAutomaticRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8823c1d7f4bde019c39b1567602666fd451a4038b52d360bb4a9083d62a78337(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0bd1d5527190c496f9940f6bdfe1c2b56dc1b2b44b0cbd8a3bfc09fbd3cd775(
    value: typing.Optional[WorkloadStatusConfigAutomatic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5314b4bb73a0fb82c8082b752eb4ad533e3e7864ec0b8693c61090c845526864(
    *,
    remaining_entities_rule_rollup: typing.Union[WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollup, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31822ab35bc63a90a9f9e9def7a5f1c09ccce1232b777e1e36e6e29bcecb68d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc9e02fb1f7e2a9cc4eb96eb13ac7eb957d99290580259e08b08a680f49b098(
    value: typing.Optional[WorkloadStatusConfigAutomaticRemainingEntitiesRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f3f45e15175ebaf1fa56327dbe4843f48ee615a4b65d97222926e15e258952(
    *,
    group_by: builtins.str,
    strategy: builtins.str,
    threshold_type: typing.Optional[builtins.str] = None,
    threshold_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d74747a6ae642cc46ca21a29ab56ed369efa2f34e55a1a69005e2b14a402534(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e622d102ac623c1cbcc692fd655f79a75354fd8e4c48b874a12412760b95c34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ecfb2c7a9b85d9c81f611cf1cfa2099abd6a90fefe59b0ba13b4197e7fd42df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a6b1e120dad2775d61dc1182a5edf8e300045e5b48520db8ee65e1d975f9bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359fa9e9275bbfd5ca6452112364aabdfc5ac1a6a41659a8f5cfe2553ff5788b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752888c871c2ceb8a67efcebb6de2b3611bc9a3b5fc3fda9423c005ecba23bbd(
    value: typing.Optional[WorkloadStatusConfigAutomaticRemainingEntitiesRuleRemainingEntitiesRuleRollup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f361068868bd2a6637ba556b24ec47b634b1924c2fb3483e7b1e4fc6b54407(
    *,
    rollup: typing.Union[WorkloadStatusConfigAutomaticRuleRollup, typing.Dict[builtins.str, typing.Any]],
    entity_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
    nrql_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadStatusConfigAutomaticRuleNrqlQuery, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb61d3574b504126d166ed0a8d2b9d4ed5ea6f304fbbbf6121de68a250af5c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48b4a88a72fa26babb5a06a83ebdcda50e603b03542a399701821a4beb6ea32b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32daf9bb35b9c0da7d97c2bbf2618fb7f3d4b6122a43e245284924bdc63b7a72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e77b9b24ae121736eb776f444bb19afcc7dc9ddc690946a662ffcb238dd72b2e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c806b99f3b8f54f1d270c200f19fc9226d640a1742cc1c2b77c04d5fb2f81d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e23990a661fea84b76ca361a167dc982b39132488181441042b90ce21ca20b8e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadStatusConfigAutomaticRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ddc5ab23486a42232d9d2dc1d674e88e10fbe9c8619ffbb0df085680967eeac(
    *,
    query: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e43e15633fc50a339efd11fac6bcef2c9a8387c742db11f61b7ad56d792379(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa0163ced0b78e5940343a473a22cf42a82720d62305e4151b3b87901c2d010(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__595d20a2e4e9e80892cf7b347e76d9eb2c5c5d1e48f2008702830637690ea715(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b08bd6e7e96805d98e2691e1425ccf4775ed555e9554168bfa2eab1c573142b8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dec2b7647bc781c2547acf2ce0da5ec7d27923c693d4502153e14d101973c6e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edde305bbc4968404d9451a935062a593a3d26c67c11d48a52bd88706d4b1bea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadStatusConfigAutomaticRuleNrqlQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56055ce40c8f9dce766fc0c781111cb49cb75a1809cabaf9b7dedff56193202(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a8ef9343d8e6b9a42c9907c268e80f159c2a373a762b9c287b7d1b5ded43bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ec3cb5aec6bfec5710948eb8c968dc5f1834c3253988a45279b26aae2eaee1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadStatusConfigAutomaticRuleNrqlQuery]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe17e8e5d6ed3b7d893f77b47d7ee4ea94f59be067d20fa947e36046abd85dad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1f4a5f75a317c3ad97f6cc99ddd013608c456a6ef44aba16a3c8a864ab0c62(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadStatusConfigAutomaticRuleNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5323aff2231a657cf46202657699f8aa2d712511e123821175ede864c84f1b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce312e80012a60299b3cef16dd3ce41e7cbae1ef0e4fd30e373fd4df344f917(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadStatusConfigAutomaticRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498c7b5ea1bd945eaf6204c90473fa9d1bf4b2e7ded651d98efe0cac8094e786(
    *,
    strategy: builtins.str,
    threshold_type: typing.Optional[builtins.str] = None,
    threshold_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ccbb3f918b53ab34d02f4e253321a2897cdfbfae74351963036e487a3354c24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e25819db48550f4f8d936b69a96c349126d01a1c8619378a82fcf327aa9ac48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa28ed6dae3045fa494aaf8db38bc0216f4f843fdd939e1da6828056d3f82f46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0bc9a5fc8030cb8274813da1950a181cdbf1553a203bc1642d9ceb4fe81a839(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95e5e6e3e1c149678bea9f6f49004128823e02fae89fb08494a71e2814984cb(
    value: typing.Optional[WorkloadStatusConfigAutomaticRuleRollup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94baa187d886028ef781ffa38a0e99d757889751620b355d227fdd2a830c94bc(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    status: builtins.str,
    description: typing.Optional[builtins.str] = None,
    summary: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9bd2eceb2bb857363d284270aa646db73a3c1e383d8231ed6c50f80eb6a8c38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4eb4cca5772c9e589dd2cc7de05cd2c7106093f1e0e925b16ac31a3afc4293(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7bcbc6f3d04b5b4dfbddd2a37f9a13914c4331436ab22fbcff45c9b0e720013(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1610bfad7b40a2217467e83a66f62ce394932a51841b92cce9b31480eb3fe40d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b99857a13f20750dbd7fb743f80f895d11bc2530b4efc8989c23ed4a83f7e1cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d2200aa0b1f9169fafa72d1809a856b9932aade3a892e04de16455b10bc660e(
    value: typing.Optional[WorkloadStatusConfigStatic],
) -> None:
    """Type checking stubs"""
    pass

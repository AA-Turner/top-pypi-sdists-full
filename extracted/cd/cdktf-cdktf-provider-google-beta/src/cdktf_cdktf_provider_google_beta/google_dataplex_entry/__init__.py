r'''
# `google_dataplex_entry`

Refer to the Terraform Registry for docs: [`google_dataplex_entry`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry).
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


class GoogleDataplexEntry(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexEntry.GoogleDataplexEntry",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry google_dataplex_entry}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        entry_type: builtins.str,
        aspects: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataplexEntryAspects", typing.Dict[builtins.str, typing.Any]]]]] = None,
        entry_group_id: typing.Optional[builtins.str] = None,
        entry_id: typing.Optional[builtins.str] = None,
        entry_source: typing.Optional[typing.Union["GoogleDataplexEntryEntrySource", typing.Dict[builtins.str, typing.Any]]] = None,
        fully_qualified_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        parent_entry: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataplexEntryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry google_dataplex_entry} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param entry_type: The relative resource name of the entry type that was used to create this entry, in the format projects/{project_number}/locations/{locationId}/entryTypes/{entryTypeId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#entry_type GoogleDataplexEntry#entry_type}
        :param aspects: aspects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#aspects GoogleDataplexEntry#aspects}
        :param entry_group_id: The entry group id of the entry group the entry will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#entry_group_id GoogleDataplexEntry#entry_group_id}
        :param entry_id: The entry id of the entry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#entry_id GoogleDataplexEntry#entry_id}
        :param entry_source: entry_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#entry_source GoogleDataplexEntry#entry_source}
        :param fully_qualified_name: A name for the entry that can be referenced by an external system. For more information, see https://cloud.google.com/dataplex/docs/fully-qualified-names. The maximum size of the field is 4000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#fully_qualified_name GoogleDataplexEntry#fully_qualified_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#id GoogleDataplexEntry#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: The location where entry will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#location GoogleDataplexEntry#location}
        :param parent_entry: The resource name of the parent entry, in the format projects/{project_number}/locations/{locationId}/entryGroups/{entryGroupId}/entries/{entryId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#parent_entry GoogleDataplexEntry#parent_entry}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#project GoogleDataplexEntry#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#timeouts GoogleDataplexEntry#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abfea7e74d56d0e05cc7f1ce43c7d038087bc0f3cad0dba9bcac0dafa0b4510b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataplexEntryConfig(
            entry_type=entry_type,
            aspects=aspects,
            entry_group_id=entry_group_id,
            entry_id=entry_id,
            entry_source=entry_source,
            fully_qualified_name=fully_qualified_name,
            id=id,
            location=location,
            parent_entry=parent_entry,
            project=project,
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
        '''Generates CDKTF code for importing a GoogleDataplexEntry resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataplexEntry to import.
        :param import_from_id: The id of the existing GoogleDataplexEntry that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataplexEntry to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__386391c9dcbaea00bf8e6d214d2529a393ee654277cc9d2bce9615a72501f3cc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAspects")
    def put_aspects(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataplexEntryAspects", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a3ff0aab60b96be92a13ae59b2c704b4f7c6d38260bf79db0eaa8083305bb9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAspects", [value]))

    @jsii.member(jsii_name="putEntrySource")
    def put_entry_source(
        self,
        *,
        ancestors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataplexEntryEntrySourceAncestors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        create_time: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        platform: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
        system_attribute: typing.Optional[builtins.str] = None,
        update_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ancestors: ancestors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#ancestors GoogleDataplexEntry#ancestors}
        :param create_time: The time when the resource was created in the source system. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#create_time GoogleDataplexEntry#create_time}
        :param description: A description of the data resource. Maximum length is 2,000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#description GoogleDataplexEntry#description}
        :param display_name: A user-friendly display name. Maximum length is 500 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#display_name GoogleDataplexEntry#display_name}
        :param labels: User-defined labels. The maximum size of keys and values is 128 characters each. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#labels GoogleDataplexEntry#labels}
        :param platform: The platform containing the source system. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#platform GoogleDataplexEntry#platform}
        :param resource: The name of the resource in the source system. Maximum length is 4,000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#resource GoogleDataplexEntry#resource}
        :param system_attribute: The name of the source system. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#system GoogleDataplexEntry#system}
        :param update_time: The time when the resource was last updated in the source system. If the entry exists in the system and its EntrySource has updateTime populated, further updates to the EntrySource of the entry must provide incremental updates to its updateTime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#update_time GoogleDataplexEntry#update_time}
        '''
        value = GoogleDataplexEntryEntrySource(
            ancestors=ancestors,
            create_time=create_time,
            description=description,
            display_name=display_name,
            labels=labels,
            platform=platform,
            resource=resource,
            system_attribute=system_attribute,
            update_time=update_time,
        )

        return typing.cast(None, jsii.invoke(self, "putEntrySource", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#create GoogleDataplexEntry#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#delete GoogleDataplexEntry#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#update GoogleDataplexEntry#update}.
        '''
        value = GoogleDataplexEntryTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAspects")
    def reset_aspects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAspects", []))

    @jsii.member(jsii_name="resetEntryGroupId")
    def reset_entry_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntryGroupId", []))

    @jsii.member(jsii_name="resetEntryId")
    def reset_entry_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntryId", []))

    @jsii.member(jsii_name="resetEntrySource")
    def reset_entry_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntrySource", []))

    @jsii.member(jsii_name="resetFullyQualifiedName")
    def reset_fully_qualified_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFullyQualifiedName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetParentEntry")
    def reset_parent_entry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParentEntry", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="aspects")
    def aspects(self) -> "GoogleDataplexEntryAspectsList":
        return typing.cast("GoogleDataplexEntryAspectsList", jsii.get(self, "aspects"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="entrySource")
    def entry_source(self) -> "GoogleDataplexEntryEntrySourceOutputReference":
        return typing.cast("GoogleDataplexEntryEntrySourceOutputReference", jsii.get(self, "entrySource"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDataplexEntryTimeoutsOutputReference":
        return typing.cast("GoogleDataplexEntryTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="aspectsInput")
    def aspects_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataplexEntryAspects"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataplexEntryAspects"]]], jsii.get(self, "aspectsInput"))

    @builtins.property
    @jsii.member(jsii_name="entryGroupIdInput")
    def entry_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entryGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="entryIdInput")
    def entry_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="entrySourceInput")
    def entry_source_input(self) -> typing.Optional["GoogleDataplexEntryEntrySource"]:
        return typing.cast(typing.Optional["GoogleDataplexEntryEntrySource"], jsii.get(self, "entrySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="entryTypeInput")
    def entry_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entryTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedNameInput")
    def fully_qualified_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fullyQualifiedNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="parentEntryInput")
    def parent_entry_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentEntryInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataplexEntryTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataplexEntryTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="entryGroupId")
    def entry_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entryGroupId"))

    @entry_group_id.setter
    def entry_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e04e348e415609a680023bc7ccbbf8f8849535bb4dcdcfeadaaace3aaa1800b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entryGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entryId")
    def entry_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entryId"))

    @entry_id.setter
    def entry_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ea8ab15b4e4e5a7b8b4ef750f08eef2ff8c4ef9aa889e1ba42338211fe4b291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entryType")
    def entry_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entryType"))

    @entry_type.setter
    def entry_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d357bf54050ba28f6dd8d00b92bb02f06495926ee97a9aa441532d8989b24e22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entryType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @fully_qualified_name.setter
    def fully_qualified_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2bd06629635affdf526bc9ee1c4553680114e3e5622c41d9e18303eb7185c15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fullyQualifiedName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0473407fb02784c766c18da3e99d8f078f5dcddfa09e0cd5aaa7102a8a2191a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760a0b34c04b666970be4749e76b521af5728a91b7fdcaf691e0d51a6d73eef4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parentEntry")
    def parent_entry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentEntry"))

    @parent_entry.setter
    def parent_entry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0956c1413b159174a0dd8c0430cfc3d8cdfae114d4a2205bb53f8b91a42f2d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentEntry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27062a7a727d3cf79b3f09310bfcd335369661389224fe1ff3ed344a08b898b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexEntry.GoogleDataplexEntryAspects",
    jsii_struct_bases=[],
    name_mapping={"aspect": "aspect", "aspect_key": "aspectKey"},
)
class GoogleDataplexEntryAspects:
    def __init__(
        self,
        *,
        aspect: typing.Union["GoogleDataplexEntryAspectsAspect", typing.Dict[builtins.str, typing.Any]],
        aspect_key: builtins.str,
    ) -> None:
        '''
        :param aspect: aspect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#aspect GoogleDataplexEntry#aspect}
        :param aspect_key: Depending on how the aspect is attached to the entry, the format of the aspect key can be one of the following:. If the aspect is attached directly to the entry: {project_number}.{locationId}.{aspectTypeId} If the aspect is attached to an entry's path: {project_number}.{locationId}.{aspectTypeId}@{path} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#aspect_key GoogleDataplexEntry#aspect_key}
        '''
        if isinstance(aspect, dict):
            aspect = GoogleDataplexEntryAspectsAspect(**aspect)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c4fe757aa81d71a08b82176557051c0efc05052ed6482a8a43c6b0068afc937)
            check_type(argname="argument aspect", value=aspect, expected_type=type_hints["aspect"])
            check_type(argname="argument aspect_key", value=aspect_key, expected_type=type_hints["aspect_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aspect": aspect,
            "aspect_key": aspect_key,
        }

    @builtins.property
    def aspect(self) -> "GoogleDataplexEntryAspectsAspect":
        '''aspect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#aspect GoogleDataplexEntry#aspect}
        '''
        result = self._values.get("aspect")
        assert result is not None, "Required property 'aspect' is missing"
        return typing.cast("GoogleDataplexEntryAspectsAspect", result)

    @builtins.property
    def aspect_key(self) -> builtins.str:
        '''Depending on how the aspect is attached to the entry, the format of the aspect key can be one of the following:.

        If the aspect is attached directly to the entry: {project_number}.{locationId}.{aspectTypeId}
        If the aspect is attached to an entry's path: {project_number}.{locationId}.{aspectTypeId}@{path}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#aspect_key GoogleDataplexEntry#aspect_key}
        '''
        result = self._values.get("aspect_key")
        assert result is not None, "Required property 'aspect_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexEntryAspects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexEntry.GoogleDataplexEntryAspectsAspect",
    jsii_struct_bases=[],
    name_mapping={"data": "data"},
)
class GoogleDataplexEntryAspectsAspect:
    def __init__(self, *, data: builtins.str) -> None:
        '''
        :param data: The content of the aspect in JSON form, according to its aspect type schema. The maximum size of the field is 120KB (encoded as UTF-8). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#data GoogleDataplexEntry#data}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573a8800f763d15be33ccbd933f54772aa37d70c9f39ddc59255abd44fbaea82)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data": data,
        }

    @builtins.property
    def data(self) -> builtins.str:
        '''The content of the aspect in JSON form, according to its aspect type schema.

        The maximum size of the field is 120KB (encoded as UTF-8).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#data GoogleDataplexEntry#data}
        '''
        result = self._values.get("data")
        assert result is not None, "Required property 'data' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexEntryAspectsAspect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataplexEntryAspectsAspectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexEntry.GoogleDataplexEntryAspectsAspectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9649bbbcf4231c0ebe6f31a213098d157847d79f4f6aca3bad95d0eedef76dca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="aspectType")
    def aspect_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aspectType"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "data"))

    @data.setter
    def data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09afbff25b645c9f98f83693af89cc85758d5f2e2ccd521dcc91653cba8839dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataplexEntryAspectsAspect]:
        return typing.cast(typing.Optional[GoogleDataplexEntryAspectsAspect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataplexEntryAspectsAspect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e545e26ddabbba7eb669a30596642210f592ec020af3558277d3f90de7dc3891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataplexEntryAspectsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexEntry.GoogleDataplexEntryAspectsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5863aeca28ec51fa74a0e25e038a86977084f0b0b1542dd5d659f88bb3afe72)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GoogleDataplexEntryAspectsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__205e61cf0c46454a6ecf1cbbd0447dff991e502f48b0dbcd9b0160f5bf161c52)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataplexEntryAspectsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37277d3b2e3a19bd09a22e2e90a66179fe2d7942f409a091a7184fa5a9eba468)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80f949bf049c05b79e7f82ba341908f700caaebe5aea3834765cd20390266b37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__469420f165dd153b2ae82044311f85f70747a5282a6c9bcbf2d69ce0aafde00a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataplexEntryAspects]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataplexEntryAspects]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataplexEntryAspects]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f9cbee55162bd94577dc4b0a6b032527b4d079c113705977a416e4e12bee28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataplexEntryAspectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexEntry.GoogleDataplexEntryAspectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a11f366149ca04d0bcf3352b5d284036342ae634e49e9cd2107b949e2075123)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAspect")
    def put_aspect(self, *, data: builtins.str) -> None:
        '''
        :param data: The content of the aspect in JSON form, according to its aspect type schema. The maximum size of the field is 120KB (encoded as UTF-8). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#data GoogleDataplexEntry#data}
        '''
        value = GoogleDataplexEntryAspectsAspect(data=data)

        return typing.cast(None, jsii.invoke(self, "putAspect", [value]))

    @builtins.property
    @jsii.member(jsii_name="aspect")
    def aspect(self) -> GoogleDataplexEntryAspectsAspectOutputReference:
        return typing.cast(GoogleDataplexEntryAspectsAspectOutputReference, jsii.get(self, "aspect"))

    @builtins.property
    @jsii.member(jsii_name="aspectInput")
    def aspect_input(self) -> typing.Optional[GoogleDataplexEntryAspectsAspect]:
        return typing.cast(typing.Optional[GoogleDataplexEntryAspectsAspect], jsii.get(self, "aspectInput"))

    @builtins.property
    @jsii.member(jsii_name="aspectKeyInput")
    def aspect_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aspectKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="aspectKey")
    def aspect_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aspectKey"))

    @aspect_key.setter
    def aspect_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc8834b0e2e8cfc1617a6779470cb1a023fb59f4026ad412cf765e28eddb9ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aspectKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataplexEntryAspects]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataplexEntryAspects]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataplexEntryAspects]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2e7de2e375bf5aa30f06827f5a7a249b9371481a8d87a0e9dc29f023e68f87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexEntry.GoogleDataplexEntryConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "entry_type": "entryType",
        "aspects": "aspects",
        "entry_group_id": "entryGroupId",
        "entry_id": "entryId",
        "entry_source": "entrySource",
        "fully_qualified_name": "fullyQualifiedName",
        "id": "id",
        "location": "location",
        "parent_entry": "parentEntry",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleDataplexEntryConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        entry_type: builtins.str,
        aspects: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataplexEntryAspects, typing.Dict[builtins.str, typing.Any]]]]] = None,
        entry_group_id: typing.Optional[builtins.str] = None,
        entry_id: typing.Optional[builtins.str] = None,
        entry_source: typing.Optional[typing.Union["GoogleDataplexEntryEntrySource", typing.Dict[builtins.str, typing.Any]]] = None,
        fully_qualified_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        parent_entry: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataplexEntryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param entry_type: The relative resource name of the entry type that was used to create this entry, in the format projects/{project_number}/locations/{locationId}/entryTypes/{entryTypeId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#entry_type GoogleDataplexEntry#entry_type}
        :param aspects: aspects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#aspects GoogleDataplexEntry#aspects}
        :param entry_group_id: The entry group id of the entry group the entry will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#entry_group_id GoogleDataplexEntry#entry_group_id}
        :param entry_id: The entry id of the entry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#entry_id GoogleDataplexEntry#entry_id}
        :param entry_source: entry_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#entry_source GoogleDataplexEntry#entry_source}
        :param fully_qualified_name: A name for the entry that can be referenced by an external system. For more information, see https://cloud.google.com/dataplex/docs/fully-qualified-names. The maximum size of the field is 4000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#fully_qualified_name GoogleDataplexEntry#fully_qualified_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#id GoogleDataplexEntry#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: The location where entry will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#location GoogleDataplexEntry#location}
        :param parent_entry: The resource name of the parent entry, in the format projects/{project_number}/locations/{locationId}/entryGroups/{entryGroupId}/entries/{entryId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#parent_entry GoogleDataplexEntry#parent_entry}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#project GoogleDataplexEntry#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#timeouts GoogleDataplexEntry#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(entry_source, dict):
            entry_source = GoogleDataplexEntryEntrySource(**entry_source)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataplexEntryTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__829888f89a47c11ba383e2b561e7274a974e18328ede62bd79ba724214a36775)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument entry_type", value=entry_type, expected_type=type_hints["entry_type"])
            check_type(argname="argument aspects", value=aspects, expected_type=type_hints["aspects"])
            check_type(argname="argument entry_group_id", value=entry_group_id, expected_type=type_hints["entry_group_id"])
            check_type(argname="argument entry_id", value=entry_id, expected_type=type_hints["entry_id"])
            check_type(argname="argument entry_source", value=entry_source, expected_type=type_hints["entry_source"])
            check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument parent_entry", value=parent_entry, expected_type=type_hints["parent_entry"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entry_type": entry_type,
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
        if aspects is not None:
            self._values["aspects"] = aspects
        if entry_group_id is not None:
            self._values["entry_group_id"] = entry_group_id
        if entry_id is not None:
            self._values["entry_id"] = entry_id
        if entry_source is not None:
            self._values["entry_source"] = entry_source
        if fully_qualified_name is not None:
            self._values["fully_qualified_name"] = fully_qualified_name
        if id is not None:
            self._values["id"] = id
        if location is not None:
            self._values["location"] = location
        if parent_entry is not None:
            self._values["parent_entry"] = parent_entry
        if project is not None:
            self._values["project"] = project
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
    def entry_type(self) -> builtins.str:
        '''The relative resource name of the entry type that was used to create this entry, in the format projects/{project_number}/locations/{locationId}/entryTypes/{entryTypeId}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#entry_type GoogleDataplexEntry#entry_type}
        '''
        result = self._values.get("entry_type")
        assert result is not None, "Required property 'entry_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aspects(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataplexEntryAspects]]]:
        '''aspects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#aspects GoogleDataplexEntry#aspects}
        '''
        result = self._values.get("aspects")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataplexEntryAspects]]], result)

    @builtins.property
    def entry_group_id(self) -> typing.Optional[builtins.str]:
        '''The entry group id of the entry group the entry will be created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#entry_group_id GoogleDataplexEntry#entry_group_id}
        '''
        result = self._values.get("entry_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entry_id(self) -> typing.Optional[builtins.str]:
        '''The entry id of the entry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#entry_id GoogleDataplexEntry#entry_id}
        '''
        result = self._values.get("entry_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entry_source(self) -> typing.Optional["GoogleDataplexEntryEntrySource"]:
        '''entry_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#entry_source GoogleDataplexEntry#entry_source}
        '''
        result = self._values.get("entry_source")
        return typing.cast(typing.Optional["GoogleDataplexEntryEntrySource"], result)

    @builtins.property
    def fully_qualified_name(self) -> typing.Optional[builtins.str]:
        '''A name for the entry that can be referenced by an external system.

        For more information, see https://cloud.google.com/dataplex/docs/fully-qualified-names.
        The maximum size of the field is 4000 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#fully_qualified_name GoogleDataplexEntry#fully_qualified_name}
        '''
        result = self._values.get("fully_qualified_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#id GoogleDataplexEntry#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location where entry will be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#location GoogleDataplexEntry#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_entry(self) -> typing.Optional[builtins.str]:
        '''The resource name of the parent entry, in the format projects/{project_number}/locations/{locationId}/entryGroups/{entryGroupId}/entries/{entryId}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#parent_entry GoogleDataplexEntry#parent_entry}
        '''
        result = self._values.get("parent_entry")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#project GoogleDataplexEntry#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDataplexEntryTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#timeouts GoogleDataplexEntry#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataplexEntryTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexEntryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexEntry.GoogleDataplexEntryEntrySource",
    jsii_struct_bases=[],
    name_mapping={
        "ancestors": "ancestors",
        "create_time": "createTime",
        "description": "description",
        "display_name": "displayName",
        "labels": "labels",
        "platform": "platform",
        "resource": "resource",
        "system_attribute": "systemAttribute",
        "update_time": "updateTime",
    },
)
class GoogleDataplexEntryEntrySource:
    def __init__(
        self,
        *,
        ancestors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataplexEntryEntrySourceAncestors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        create_time: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        platform: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
        system_attribute: typing.Optional[builtins.str] = None,
        update_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ancestors: ancestors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#ancestors GoogleDataplexEntry#ancestors}
        :param create_time: The time when the resource was created in the source system. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#create_time GoogleDataplexEntry#create_time}
        :param description: A description of the data resource. Maximum length is 2,000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#description GoogleDataplexEntry#description}
        :param display_name: A user-friendly display name. Maximum length is 500 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#display_name GoogleDataplexEntry#display_name}
        :param labels: User-defined labels. The maximum size of keys and values is 128 characters each. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#labels GoogleDataplexEntry#labels}
        :param platform: The platform containing the source system. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#platform GoogleDataplexEntry#platform}
        :param resource: The name of the resource in the source system. Maximum length is 4,000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#resource GoogleDataplexEntry#resource}
        :param system_attribute: The name of the source system. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#system GoogleDataplexEntry#system}
        :param update_time: The time when the resource was last updated in the source system. If the entry exists in the system and its EntrySource has updateTime populated, further updates to the EntrySource of the entry must provide incremental updates to its updateTime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#update_time GoogleDataplexEntry#update_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f20eef4ae8d59ec35a63e3c95b6f8ff3314e1145afc54ec2a3096436497b229)
            check_type(argname="argument ancestors", value=ancestors, expected_type=type_hints["ancestors"])
            check_type(argname="argument create_time", value=create_time, expected_type=type_hints["create_time"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument system_attribute", value=system_attribute, expected_type=type_hints["system_attribute"])
            check_type(argname="argument update_time", value=update_time, expected_type=type_hints["update_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ancestors is not None:
            self._values["ancestors"] = ancestors
        if create_time is not None:
            self._values["create_time"] = create_time
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if labels is not None:
            self._values["labels"] = labels
        if platform is not None:
            self._values["platform"] = platform
        if resource is not None:
            self._values["resource"] = resource
        if system_attribute is not None:
            self._values["system_attribute"] = system_attribute
        if update_time is not None:
            self._values["update_time"] = update_time

    @builtins.property
    def ancestors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataplexEntryEntrySourceAncestors"]]]:
        '''ancestors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#ancestors GoogleDataplexEntry#ancestors}
        '''
        result = self._values.get("ancestors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataplexEntryEntrySourceAncestors"]]], result)

    @builtins.property
    def create_time(self) -> typing.Optional[builtins.str]:
        '''The time when the resource was created in the source system.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#create_time GoogleDataplexEntry#create_time}
        '''
        result = self._values.get("create_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the data resource. Maximum length is 2,000 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#description GoogleDataplexEntry#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''A user-friendly display name. Maximum length is 500 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#display_name GoogleDataplexEntry#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined labels.

        The maximum size of keys and values is 128 characters each.
        An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#labels GoogleDataplexEntry#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''The platform containing the source system. Maximum length is 64 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#platform GoogleDataplexEntry#platform}
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''The name of the resource in the source system. Maximum length is 4,000 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#resource GoogleDataplexEntry#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_attribute(self) -> typing.Optional[builtins.str]:
        '''The name of the source system. Maximum length is 64 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#system GoogleDataplexEntry#system}
        '''
        result = self._values.get("system_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update_time(self) -> typing.Optional[builtins.str]:
        '''The time when the resource was last updated in the source system.

        If the entry exists in the system and its EntrySource has updateTime populated,
        further updates to the EntrySource of the entry must provide incremental updates to its updateTime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#update_time GoogleDataplexEntry#update_time}
        '''
        result = self._values.get("update_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexEntryEntrySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexEntry.GoogleDataplexEntryEntrySourceAncestors",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class GoogleDataplexEntryEntrySourceAncestors:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the ancestor resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#name GoogleDataplexEntry#name}
        :param type: The type of the ancestor resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#type GoogleDataplexEntry#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d3176bf3d3bb3d26293be7a7348009976d2e48f3fa1972b321bbc992e6416d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the ancestor resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#name GoogleDataplexEntry#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the ancestor resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#type GoogleDataplexEntry#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexEntryEntrySourceAncestors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataplexEntryEntrySourceAncestorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexEntry.GoogleDataplexEntryEntrySourceAncestorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0621cf8698f6a14e99e71881d91f4841467b48707d12c0518e81ccc65930d74f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataplexEntryEntrySourceAncestorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__191c2a76ca64d97fdd8fea207b4dd471b3252e73a4db82531013a0ae9fe1041a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataplexEntryEntrySourceAncestorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e281e4a6f026105f48dbe58f0b8eccd59594892e3c86bad889f87d005607efbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e289afba689c9251246f98e3c22cabff04037664c9aa6e82e4b601f087c8b268)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d46bc6c8aacf21116970d4f91e33685ba65f7dfaa6bb068a019c093f112957c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataplexEntryEntrySourceAncestors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataplexEntryEntrySourceAncestors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataplexEntryEntrySourceAncestors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dbd64e5bc654b68d5acdde9214f1de25fff9aa56d39af9928ea8ae88c8b44be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataplexEntryEntrySourceAncestorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexEntry.GoogleDataplexEntryEntrySourceAncestorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2045cc864330a21e15f5c3fb40fc07f2bd28eeff7d121e045f478089d264cb04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7047e7cddfe8c99882d6f9ed9ad285d66289bb4902edfce3de990f8a91cf7963)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb258c1e0dbf39e36c66fa75e8d090ec73877c705ebccf942dd1f228945dd35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataplexEntryEntrySourceAncestors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataplexEntryEntrySourceAncestors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataplexEntryEntrySourceAncestors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ada58db6d2bc802780e77ee5357c78ff82a1bea2e441c5eda9c21de1d390f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataplexEntryEntrySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexEntry.GoogleDataplexEntryEntrySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__595409a40fff1eeaaf61d2ad2abeecf5631dffbf9f122ed23d138be170a30020)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAncestors")
    def put_ancestors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataplexEntryEntrySourceAncestors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f7013008a9caeb70aed1ae0356b273fcccc25c6abcbe506d8937a7480a1d667)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAncestors", [value]))

    @jsii.member(jsii_name="resetAncestors")
    def reset_ancestors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAncestors", []))

    @jsii.member(jsii_name="resetCreateTime")
    def reset_create_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateTime", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetPlatform")
    def reset_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatform", []))

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @jsii.member(jsii_name="resetSystemAttribute")
    def reset_system_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemAttribute", []))

    @jsii.member(jsii_name="resetUpdateTime")
    def reset_update_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateTime", []))

    @builtins.property
    @jsii.member(jsii_name="ancestors")
    def ancestors(self) -> GoogleDataplexEntryEntrySourceAncestorsList:
        return typing.cast(GoogleDataplexEntryEntrySourceAncestorsList, jsii.get(self, "ancestors"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="ancestorsInput")
    def ancestors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataplexEntryEntrySourceAncestors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataplexEntryEntrySourceAncestors]]], jsii.get(self, "ancestorsInput"))

    @builtins.property
    @jsii.member(jsii_name="createTimeInput")
    def create_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="platformInput")
    def platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="systemAttributeInput")
    def system_attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "systemAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="updateTimeInput")
    def update_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @create_time.setter
    def create_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ced71e19e400f4fcd58116a0286e95e0961517d9f4b9a1eb6f88d89c837a8b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef86389c7d4bd95d68c2f7830218b516773f1aefd0f67ecaf4470b8683b7421d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__304494a116dcfca0b14a178b5914e57080fc35216e71bdccc317830bb228e717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5278778b9433056f67ae25e0d3f88eef71f5ac0837f5a95215d20dceb2c7b464)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @platform.setter
    def platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f67b6c6ef9f6faa6bf0cf730f1e6e424458f3fb12fc36190134f1a14d76fbaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__321502a7f6b85a839e507e3b5c2fc97b669939bc51e6204baa71f1e903a51083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemAttribute")
    def system_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemAttribute"))

    @system_attribute.setter
    def system_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dd210edef06bcf0cc302c8fbefd55d911a8de24256faada0660630b706b8934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @update_time.setter
    def update_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d21bea918b78fa1363fbe4509ae18328c35b3a6bdc3a67f2c1227546b38acaa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataplexEntryEntrySource]:
        return typing.cast(typing.Optional[GoogleDataplexEntryEntrySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataplexEntryEntrySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08c4336566550e6adb101f7051bf3dddf479724f08d8942e56555a0e7c6f5778)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexEntry.GoogleDataplexEntryTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataplexEntryTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#create GoogleDataplexEntry#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#delete GoogleDataplexEntry#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#update GoogleDataplexEntry#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9296d3b779805ed97449e553412e175e213aa6cacb7e6fd30ca400d00dd77a4b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#create GoogleDataplexEntry#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#delete GoogleDataplexEntry#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_entry#update GoogleDataplexEntry#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexEntryTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataplexEntryTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexEntry.GoogleDataplexEntryTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16138214ff2c0084f055bf22793e5cabbc541eb65faf3315c67b7bd725e51d98)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bce6cc032187d19325640834411cd857947882ea25979ff02080a6a745e9b3d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__685a09b72b92babd25df0b7458c32f50635b8fd10d62b758421adb33589dc04b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60a1639c2aa660ae44885192985cd14298e0225875990cd4fd19f3d873b2f844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataplexEntryTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataplexEntryTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataplexEntryTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1372cfc79193b2559d7615e82983fc9476002fc5f98db65c97918b6d105dfde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDataplexEntry",
    "GoogleDataplexEntryAspects",
    "GoogleDataplexEntryAspectsAspect",
    "GoogleDataplexEntryAspectsAspectOutputReference",
    "GoogleDataplexEntryAspectsList",
    "GoogleDataplexEntryAspectsOutputReference",
    "GoogleDataplexEntryConfig",
    "GoogleDataplexEntryEntrySource",
    "GoogleDataplexEntryEntrySourceAncestors",
    "GoogleDataplexEntryEntrySourceAncestorsList",
    "GoogleDataplexEntryEntrySourceAncestorsOutputReference",
    "GoogleDataplexEntryEntrySourceOutputReference",
    "GoogleDataplexEntryTimeouts",
    "GoogleDataplexEntryTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__abfea7e74d56d0e05cc7f1ce43c7d038087bc0f3cad0dba9bcac0dafa0b4510b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    entry_type: builtins.str,
    aspects: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataplexEntryAspects, typing.Dict[builtins.str, typing.Any]]]]] = None,
    entry_group_id: typing.Optional[builtins.str] = None,
    entry_id: typing.Optional[builtins.str] = None,
    entry_source: typing.Optional[typing.Union[GoogleDataplexEntryEntrySource, typing.Dict[builtins.str, typing.Any]]] = None,
    fully_qualified_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    parent_entry: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataplexEntryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__386391c9dcbaea00bf8e6d214d2529a393ee654277cc9d2bce9615a72501f3cc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3ff0aab60b96be92a13ae59b2c704b4f7c6d38260bf79db0eaa8083305bb9e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataplexEntryAspects, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04e348e415609a680023bc7ccbbf8f8849535bb4dcdcfeadaaace3aaa1800b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea8ab15b4e4e5a7b8b4ef750f08eef2ff8c4ef9aa889e1ba42338211fe4b291(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d357bf54050ba28f6dd8d00b92bb02f06495926ee97a9aa441532d8989b24e22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2bd06629635affdf526bc9ee1c4553680114e3e5622c41d9e18303eb7185c15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0473407fb02784c766c18da3e99d8f078f5dcddfa09e0cd5aaa7102a8a2191a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760a0b34c04b666970be4749e76b521af5728a91b7fdcaf691e0d51a6d73eef4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0956c1413b159174a0dd8c0430cfc3d8cdfae114d4a2205bb53f8b91a42f2d0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27062a7a727d3cf79b3f09310bfcd335369661389224fe1ff3ed344a08b898b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4fe757aa81d71a08b82176557051c0efc05052ed6482a8a43c6b0068afc937(
    *,
    aspect: typing.Union[GoogleDataplexEntryAspectsAspect, typing.Dict[builtins.str, typing.Any]],
    aspect_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573a8800f763d15be33ccbd933f54772aa37d70c9f39ddc59255abd44fbaea82(
    *,
    data: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9649bbbcf4231c0ebe6f31a213098d157847d79f4f6aca3bad95d0eedef76dca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09afbff25b645c9f98f83693af89cc85758d5f2e2ccd521dcc91653cba8839dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e545e26ddabbba7eb669a30596642210f592ec020af3558277d3f90de7dc3891(
    value: typing.Optional[GoogleDataplexEntryAspectsAspect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5863aeca28ec51fa74a0e25e038a86977084f0b0b1542dd5d659f88bb3afe72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205e61cf0c46454a6ecf1cbbd0447dff991e502f48b0dbcd9b0160f5bf161c52(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37277d3b2e3a19bd09a22e2e90a66179fe2d7942f409a091a7184fa5a9eba468(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f949bf049c05b79e7f82ba341908f700caaebe5aea3834765cd20390266b37(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__469420f165dd153b2ae82044311f85f70747a5282a6c9bcbf2d69ce0aafde00a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f9cbee55162bd94577dc4b0a6b032527b4d079c113705977a416e4e12bee28(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataplexEntryAspects]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a11f366149ca04d0bcf3352b5d284036342ae634e49e9cd2107b949e2075123(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc8834b0e2e8cfc1617a6779470cb1a023fb59f4026ad412cf765e28eddb9ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2e7de2e375bf5aa30f06827f5a7a249b9371481a8d87a0e9dc29f023e68f87(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataplexEntryAspects]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__829888f89a47c11ba383e2b561e7274a974e18328ede62bd79ba724214a36775(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    entry_type: builtins.str,
    aspects: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataplexEntryAspects, typing.Dict[builtins.str, typing.Any]]]]] = None,
    entry_group_id: typing.Optional[builtins.str] = None,
    entry_id: typing.Optional[builtins.str] = None,
    entry_source: typing.Optional[typing.Union[GoogleDataplexEntryEntrySource, typing.Dict[builtins.str, typing.Any]]] = None,
    fully_qualified_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    parent_entry: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataplexEntryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f20eef4ae8d59ec35a63e3c95b6f8ff3314e1145afc54ec2a3096436497b229(
    *,
    ancestors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataplexEntryEntrySourceAncestors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    create_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    platform: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
    system_attribute: typing.Optional[builtins.str] = None,
    update_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d3176bf3d3bb3d26293be7a7348009976d2e48f3fa1972b321bbc992e6416d(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0621cf8698f6a14e99e71881d91f4841467b48707d12c0518e81ccc65930d74f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__191c2a76ca64d97fdd8fea207b4dd471b3252e73a4db82531013a0ae9fe1041a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e281e4a6f026105f48dbe58f0b8eccd59594892e3c86bad889f87d005607efbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e289afba689c9251246f98e3c22cabff04037664c9aa6e82e4b601f087c8b268(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d46bc6c8aacf21116970d4f91e33685ba65f7dfaa6bb068a019c093f112957c0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dbd64e5bc654b68d5acdde9214f1de25fff9aa56d39af9928ea8ae88c8b44be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataplexEntryEntrySourceAncestors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2045cc864330a21e15f5c3fb40fc07f2bd28eeff7d121e045f478089d264cb04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7047e7cddfe8c99882d6f9ed9ad285d66289bb4902edfce3de990f8a91cf7963(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb258c1e0dbf39e36c66fa75e8d090ec73877c705ebccf942dd1f228945dd35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ada58db6d2bc802780e77ee5357c78ff82a1bea2e441c5eda9c21de1d390f5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataplexEntryEntrySourceAncestors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__595409a40fff1eeaaf61d2ad2abeecf5631dffbf9f122ed23d138be170a30020(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7013008a9caeb70aed1ae0356b273fcccc25c6abcbe506d8937a7480a1d667(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataplexEntryEntrySourceAncestors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ced71e19e400f4fcd58116a0286e95e0961517d9f4b9a1eb6f88d89c837a8b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef86389c7d4bd95d68c2f7830218b516773f1aefd0f67ecaf4470b8683b7421d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304494a116dcfca0b14a178b5914e57080fc35216e71bdccc317830bb228e717(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5278778b9433056f67ae25e0d3f88eef71f5ac0837f5a95215d20dceb2c7b464(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f67b6c6ef9f6faa6bf0cf730f1e6e424458f3fb12fc36190134f1a14d76fbaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__321502a7f6b85a839e507e3b5c2fc97b669939bc51e6204baa71f1e903a51083(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd210edef06bcf0cc302c8fbefd55d911a8de24256faada0660630b706b8934(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d21bea918b78fa1363fbe4509ae18328c35b3a6bdc3a67f2c1227546b38acaa4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c4336566550e6adb101f7051bf3dddf479724f08d8942e56555a0e7c6f5778(
    value: typing.Optional[GoogleDataplexEntryEntrySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9296d3b779805ed97449e553412e175e213aa6cacb7e6fd30ca400d00dd77a4b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16138214ff2c0084f055bf22793e5cabbc541eb65faf3315c67b7bd725e51d98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce6cc032187d19325640834411cd857947882ea25979ff02080a6a745e9b3d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685a09b72b92babd25df0b7458c32f50635b8fd10d62b758421adb33589dc04b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a1639c2aa660ae44885192985cd14298e0225875990cd4fd19f3d873b2f844(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1372cfc79193b2559d7615e82983fc9476002fc5f98db65c97918b6d105dfde(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataplexEntryTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

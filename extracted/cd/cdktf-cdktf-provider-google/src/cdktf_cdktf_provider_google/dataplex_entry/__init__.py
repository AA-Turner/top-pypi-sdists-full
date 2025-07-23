r'''
# `google_dataplex_entry`

Refer to the Terraform Registry for docs: [`google_dataplex_entry`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry).
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


class DataplexEntry(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexEntry.DataplexEntry",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry google_dataplex_entry}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        entry_type: builtins.str,
        aspects: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataplexEntryAspects", typing.Dict[builtins.str, typing.Any]]]]] = None,
        entry_group_id: typing.Optional[builtins.str] = None,
        entry_id: typing.Optional[builtins.str] = None,
        entry_source: typing.Optional[typing.Union["DataplexEntryEntrySource", typing.Dict[builtins.str, typing.Any]]] = None,
        fully_qualified_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        parent_entry: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataplexEntryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry google_dataplex_entry} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param entry_type: The relative resource name of the entry type that was used to create this entry, in the format projects/{project_number}/locations/{locationId}/entryTypes/{entryTypeId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#entry_type DataplexEntry#entry_type}
        :param aspects: aspects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#aspects DataplexEntry#aspects}
        :param entry_group_id: The entry group id of the entry group the entry will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#entry_group_id DataplexEntry#entry_group_id}
        :param entry_id: The entry id of the entry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#entry_id DataplexEntry#entry_id}
        :param entry_source: entry_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#entry_source DataplexEntry#entry_source}
        :param fully_qualified_name: A name for the entry that can be referenced by an external system. For more information, see https://cloud.google.com/dataplex/docs/fully-qualified-names. The maximum size of the field is 4000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#fully_qualified_name DataplexEntry#fully_qualified_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#id DataplexEntry#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: The location where entry will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#location DataplexEntry#location}
        :param parent_entry: The resource name of the parent entry, in the format projects/{project_number}/locations/{locationId}/entryGroups/{entryGroupId}/entries/{entryId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#parent_entry DataplexEntry#parent_entry}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#project DataplexEntry#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#timeouts DataplexEntry#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dee993c664e2ea81ab041fa8d322c8d7b4c10b4848b9c62c84da00040fbb4fe1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataplexEntryConfig(
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
        '''Generates CDKTF code for importing a DataplexEntry resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataplexEntry to import.
        :param import_from_id: The id of the existing DataplexEntry that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataplexEntry to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daa3c8341682d5865a4ca04ac14f5620a391f9aa6183bbd8df73304d9d97d65d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAspects")
    def put_aspects(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataplexEntryAspects", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df58d5dbc72356b86401eb7383737fa9f6f0741dfddc23a1664dc23426f2da31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAspects", [value]))

    @jsii.member(jsii_name="putEntrySource")
    def put_entry_source(
        self,
        *,
        ancestors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataplexEntryEntrySourceAncestors", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param ancestors: ancestors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#ancestors DataplexEntry#ancestors}
        :param create_time: The time when the resource was created in the source system. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#create_time DataplexEntry#create_time}
        :param description: A description of the data resource. Maximum length is 2,000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#description DataplexEntry#description}
        :param display_name: A user-friendly display name. Maximum length is 500 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#display_name DataplexEntry#display_name}
        :param labels: User-defined labels. The maximum size of keys and values is 128 characters each. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#labels DataplexEntry#labels}
        :param platform: The platform containing the source system. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#platform DataplexEntry#platform}
        :param resource: The name of the resource in the source system. Maximum length is 4,000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#resource DataplexEntry#resource}
        :param system_attribute: The name of the source system. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#system DataplexEntry#system}
        :param update_time: The time when the resource was last updated in the source system. If the entry exists in the system and its EntrySource has updateTime populated, further updates to the EntrySource of the entry must provide incremental updates to its updateTime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#update_time DataplexEntry#update_time}
        '''
        value = DataplexEntryEntrySource(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#create DataplexEntry#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#delete DataplexEntry#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#update DataplexEntry#update}.
        '''
        value = DataplexEntryTimeouts(create=create, delete=delete, update=update)

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
    def aspects(self) -> "DataplexEntryAspectsList":
        return typing.cast("DataplexEntryAspectsList", jsii.get(self, "aspects"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="entrySource")
    def entry_source(self) -> "DataplexEntryEntrySourceOutputReference":
        return typing.cast("DataplexEntryEntrySourceOutputReference", jsii.get(self, "entrySource"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataplexEntryTimeoutsOutputReference":
        return typing.cast("DataplexEntryTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="aspectsInput")
    def aspects_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataplexEntryAspects"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataplexEntryAspects"]]], jsii.get(self, "aspectsInput"))

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
    def entry_source_input(self) -> typing.Optional["DataplexEntryEntrySource"]:
        return typing.cast(typing.Optional["DataplexEntryEntrySource"], jsii.get(self, "entrySourceInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataplexEntryTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataplexEntryTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="entryGroupId")
    def entry_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entryGroupId"))

    @entry_group_id.setter
    def entry_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__912f3958ae4abbb879b8f0c367789eaae66f0a4d9562ed53fafdb280aa72d39f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entryGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entryId")
    def entry_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entryId"))

    @entry_id.setter
    def entry_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f8f72d6a614691f7149ea9d36524d563a43ed6aaf902244dbee2d27d926229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entryType")
    def entry_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entryType"))

    @entry_type.setter
    def entry_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdae445589eb546e62b120b167537b4c65b06f4a87836580b4ee8330e5ceda43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entryType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @fully_qualified_name.setter
    def fully_qualified_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__799650a3cb337e1d9df8ac016a1925c7a3e67e61b4e3649acc9cb8dd5770b75e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fullyQualifiedName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00f6130552525f154c57bdf8ede4e705297adfc932165d015e72e0f387d363ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__205dccef8bb6b708dd918576916deb8f26f65a475606be54dec470c3aa267e1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parentEntry")
    def parent_entry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentEntry"))

    @parent_entry.setter
    def parent_entry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79a226b6fbdd5fa815aa115e969159756927b7289c948094ebd9824201d21db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentEntry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3db3b35891b504fbb53f974443ab42b00e6ec3b708d5fe8d2a056c8d58803fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexEntry.DataplexEntryAspects",
    jsii_struct_bases=[],
    name_mapping={"aspect": "aspect", "aspect_key": "aspectKey"},
)
class DataplexEntryAspects:
    def __init__(
        self,
        *,
        aspect: typing.Union["DataplexEntryAspectsAspect", typing.Dict[builtins.str, typing.Any]],
        aspect_key: builtins.str,
    ) -> None:
        '''
        :param aspect: aspect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#aspect DataplexEntry#aspect}
        :param aspect_key: Depending on how the aspect is attached to the entry, the format of the aspect key can be one of the following:. If the aspect is attached directly to the entry: {project_number}.{locationId}.{aspectTypeId} If the aspect is attached to an entry's path: {project_number}.{locationId}.{aspectTypeId}@{path} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#aspect_key DataplexEntry#aspect_key}
        '''
        if isinstance(aspect, dict):
            aspect = DataplexEntryAspectsAspect(**aspect)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__136360cefb1f5260ff46f4c2fd76b610ae57c6a971d7b56d3fa468c43127bef2)
            check_type(argname="argument aspect", value=aspect, expected_type=type_hints["aspect"])
            check_type(argname="argument aspect_key", value=aspect_key, expected_type=type_hints["aspect_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aspect": aspect,
            "aspect_key": aspect_key,
        }

    @builtins.property
    def aspect(self) -> "DataplexEntryAspectsAspect":
        '''aspect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#aspect DataplexEntry#aspect}
        '''
        result = self._values.get("aspect")
        assert result is not None, "Required property 'aspect' is missing"
        return typing.cast("DataplexEntryAspectsAspect", result)

    @builtins.property
    def aspect_key(self) -> builtins.str:
        '''Depending on how the aspect is attached to the entry, the format of the aspect key can be one of the following:.

        If the aspect is attached directly to the entry: {project_number}.{locationId}.{aspectTypeId}
        If the aspect is attached to an entry's path: {project_number}.{locationId}.{aspectTypeId}@{path}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#aspect_key DataplexEntry#aspect_key}
        '''
        result = self._values.get("aspect_key")
        assert result is not None, "Required property 'aspect_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexEntryAspects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexEntry.DataplexEntryAspectsAspect",
    jsii_struct_bases=[],
    name_mapping={"data": "data"},
)
class DataplexEntryAspectsAspect:
    def __init__(self, *, data: builtins.str) -> None:
        '''
        :param data: The content of the aspect in JSON form, according to its aspect type schema. The maximum size of the field is 120KB (encoded as UTF-8). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#data DataplexEntry#data}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__899a4df70587095c7cbfa958272d99007670371e7d8198af0fbf01fa5868ba0b)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data": data,
        }

    @builtins.property
    def data(self) -> builtins.str:
        '''The content of the aspect in JSON form, according to its aspect type schema.

        The maximum size of the field is 120KB (encoded as UTF-8).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#data DataplexEntry#data}
        '''
        result = self._values.get("data")
        assert result is not None, "Required property 'data' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexEntryAspectsAspect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexEntryAspectsAspectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexEntry.DataplexEntryAspectsAspectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76ed7e66ca1fe9a6295c6e40c913a2035248bf8045ec78ba66396356569ab790)
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
            type_hints = typing.get_type_hints(_typecheckingstub__908d237a524dc6cc071d29de2d2a3a3327d627bc80de5cde0c3d554429200917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexEntryAspectsAspect]:
        return typing.cast(typing.Optional[DataplexEntryAspectsAspect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexEntryAspectsAspect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e27e5ed8a7114682e534fe66913877990b7a67e74ab4fbdb256e2a7b1002b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexEntryAspectsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexEntry.DataplexEntryAspectsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__308e59897a8995fd4a3fde6a58fe708700afff94c528a50373a6493c5805624f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataplexEntryAspectsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3faf0b98d33cf3de2377751209fe1bc1855f634fb0b322c755f03ce49df940af)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataplexEntryAspectsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__953d2026fd96b6e8df6d58b5edd61f58937f5f5c5d0a1b7407ee790893e0fdb9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9d8557c30c98fd74193c925cb9d4a204b301e481d74f92b043663ac84a0b2e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b16fb15d7edf4a4bcc59fdd8e8c07ecfc99cb93b52f90d06f09c42bc10821f91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataplexEntryAspects]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataplexEntryAspects]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataplexEntryAspects]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf581716ab2a6347c376878022b40187f0115eefe51700a6200669de63ff93a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexEntryAspectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexEntry.DataplexEntryAspectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e3c45496077bf9222b12ff5a81cb86b093488ce22e26e8e1abc5c2956184889)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAspect")
    def put_aspect(self, *, data: builtins.str) -> None:
        '''
        :param data: The content of the aspect in JSON form, according to its aspect type schema. The maximum size of the field is 120KB (encoded as UTF-8). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#data DataplexEntry#data}
        '''
        value = DataplexEntryAspectsAspect(data=data)

        return typing.cast(None, jsii.invoke(self, "putAspect", [value]))

    @builtins.property
    @jsii.member(jsii_name="aspect")
    def aspect(self) -> DataplexEntryAspectsAspectOutputReference:
        return typing.cast(DataplexEntryAspectsAspectOutputReference, jsii.get(self, "aspect"))

    @builtins.property
    @jsii.member(jsii_name="aspectInput")
    def aspect_input(self) -> typing.Optional[DataplexEntryAspectsAspect]:
        return typing.cast(typing.Optional[DataplexEntryAspectsAspect], jsii.get(self, "aspectInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__250adb13195a450f7d4f50aae7bae996bc49c1e354531a05e3465670d93e16c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aspectKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexEntryAspects]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexEntryAspects]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexEntryAspects]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__073ada29c413c0e7ca8ff40745d68a5510de1e067be220489db3995e0552d311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexEntry.DataplexEntryConfig",
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
class DataplexEntryConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        aspects: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataplexEntryAspects, typing.Dict[builtins.str, typing.Any]]]]] = None,
        entry_group_id: typing.Optional[builtins.str] = None,
        entry_id: typing.Optional[builtins.str] = None,
        entry_source: typing.Optional[typing.Union["DataplexEntryEntrySource", typing.Dict[builtins.str, typing.Any]]] = None,
        fully_qualified_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        parent_entry: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataplexEntryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param entry_type: The relative resource name of the entry type that was used to create this entry, in the format projects/{project_number}/locations/{locationId}/entryTypes/{entryTypeId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#entry_type DataplexEntry#entry_type}
        :param aspects: aspects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#aspects DataplexEntry#aspects}
        :param entry_group_id: The entry group id of the entry group the entry will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#entry_group_id DataplexEntry#entry_group_id}
        :param entry_id: The entry id of the entry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#entry_id DataplexEntry#entry_id}
        :param entry_source: entry_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#entry_source DataplexEntry#entry_source}
        :param fully_qualified_name: A name for the entry that can be referenced by an external system. For more information, see https://cloud.google.com/dataplex/docs/fully-qualified-names. The maximum size of the field is 4000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#fully_qualified_name DataplexEntry#fully_qualified_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#id DataplexEntry#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: The location where entry will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#location DataplexEntry#location}
        :param parent_entry: The resource name of the parent entry, in the format projects/{project_number}/locations/{locationId}/entryGroups/{entryGroupId}/entries/{entryId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#parent_entry DataplexEntry#parent_entry}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#project DataplexEntry#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#timeouts DataplexEntry#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(entry_source, dict):
            entry_source = DataplexEntryEntrySource(**entry_source)
        if isinstance(timeouts, dict):
            timeouts = DataplexEntryTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6de93d67cbfa0702744ad1927bb956e66ed1238ad08a2f72f51894068bc43295)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#entry_type DataplexEntry#entry_type}
        '''
        result = self._values.get("entry_type")
        assert result is not None, "Required property 'entry_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aspects(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataplexEntryAspects]]]:
        '''aspects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#aspects DataplexEntry#aspects}
        '''
        result = self._values.get("aspects")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataplexEntryAspects]]], result)

    @builtins.property
    def entry_group_id(self) -> typing.Optional[builtins.str]:
        '''The entry group id of the entry group the entry will be created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#entry_group_id DataplexEntry#entry_group_id}
        '''
        result = self._values.get("entry_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entry_id(self) -> typing.Optional[builtins.str]:
        '''The entry id of the entry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#entry_id DataplexEntry#entry_id}
        '''
        result = self._values.get("entry_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entry_source(self) -> typing.Optional["DataplexEntryEntrySource"]:
        '''entry_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#entry_source DataplexEntry#entry_source}
        '''
        result = self._values.get("entry_source")
        return typing.cast(typing.Optional["DataplexEntryEntrySource"], result)

    @builtins.property
    def fully_qualified_name(self) -> typing.Optional[builtins.str]:
        '''A name for the entry that can be referenced by an external system.

        For more information, see https://cloud.google.com/dataplex/docs/fully-qualified-names.
        The maximum size of the field is 4000 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#fully_qualified_name DataplexEntry#fully_qualified_name}
        '''
        result = self._values.get("fully_qualified_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#id DataplexEntry#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location where entry will be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#location DataplexEntry#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_entry(self) -> typing.Optional[builtins.str]:
        '''The resource name of the parent entry, in the format projects/{project_number}/locations/{locationId}/entryGroups/{entryGroupId}/entries/{entryId}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#parent_entry DataplexEntry#parent_entry}
        '''
        result = self._values.get("parent_entry")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#project DataplexEntry#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataplexEntryTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#timeouts DataplexEntry#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataplexEntryTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexEntryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexEntry.DataplexEntryEntrySource",
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
class DataplexEntryEntrySource:
    def __init__(
        self,
        *,
        ancestors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataplexEntryEntrySourceAncestors", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param ancestors: ancestors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#ancestors DataplexEntry#ancestors}
        :param create_time: The time when the resource was created in the source system. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#create_time DataplexEntry#create_time}
        :param description: A description of the data resource. Maximum length is 2,000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#description DataplexEntry#description}
        :param display_name: A user-friendly display name. Maximum length is 500 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#display_name DataplexEntry#display_name}
        :param labels: User-defined labels. The maximum size of keys and values is 128 characters each. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#labels DataplexEntry#labels}
        :param platform: The platform containing the source system. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#platform DataplexEntry#platform}
        :param resource: The name of the resource in the source system. Maximum length is 4,000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#resource DataplexEntry#resource}
        :param system_attribute: The name of the source system. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#system DataplexEntry#system}
        :param update_time: The time when the resource was last updated in the source system. If the entry exists in the system and its EntrySource has updateTime populated, further updates to the EntrySource of the entry must provide incremental updates to its updateTime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#update_time DataplexEntry#update_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4613345ef4ae3872d646c486214f384d742d7417196bc790ae127b4e424abf64)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataplexEntryEntrySourceAncestors"]]]:
        '''ancestors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#ancestors DataplexEntry#ancestors}
        '''
        result = self._values.get("ancestors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataplexEntryEntrySourceAncestors"]]], result)

    @builtins.property
    def create_time(self) -> typing.Optional[builtins.str]:
        '''The time when the resource was created in the source system.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#create_time DataplexEntry#create_time}
        '''
        result = self._values.get("create_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the data resource. Maximum length is 2,000 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#description DataplexEntry#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''A user-friendly display name. Maximum length is 500 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#display_name DataplexEntry#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined labels.

        The maximum size of keys and values is 128 characters each.
        An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#labels DataplexEntry#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''The platform containing the source system. Maximum length is 64 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#platform DataplexEntry#platform}
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''The name of the resource in the source system. Maximum length is 4,000 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#resource DataplexEntry#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_attribute(self) -> typing.Optional[builtins.str]:
        '''The name of the source system. Maximum length is 64 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#system DataplexEntry#system}
        '''
        result = self._values.get("system_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update_time(self) -> typing.Optional[builtins.str]:
        '''The time when the resource was last updated in the source system.

        If the entry exists in the system and its EntrySource has updateTime populated,
        further updates to the EntrySource of the entry must provide incremental updates to its updateTime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#update_time DataplexEntry#update_time}
        '''
        result = self._values.get("update_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexEntryEntrySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexEntry.DataplexEntryEntrySourceAncestors",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class DataplexEntryEntrySourceAncestors:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the ancestor resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#name DataplexEntry#name}
        :param type: The type of the ancestor resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#type DataplexEntry#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332ecf58d14ae50db266ad5ddcdaa4e541658cbd08d56d52de9a62dd840e8057)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#name DataplexEntry#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the ancestor resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#type DataplexEntry#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexEntryEntrySourceAncestors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexEntryEntrySourceAncestorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexEntry.DataplexEntryEntrySourceAncestorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c526d4b273fc82dc7ae02b4d505cff36cc9d59d6069266cb00740eb3bd37d4ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataplexEntryEntrySourceAncestorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__251d9810f17f86b56a61b62fc07831ab3be79eae23bff2e30a869105113a50ff)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataplexEntryEntrySourceAncestorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de704c2ae99118c01c49bd2e1e985428bea4638f6bb2e1a9224e63005b8691f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c2210e9179ba3c4779aa7bfed47b1de4d3b85343e144d5d55cf6e59715321bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1278f0fb3d5ac6d5d7e6143e6e0b46ad86aefd4f575cb7457c808b3a28229264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataplexEntryEntrySourceAncestors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataplexEntryEntrySourceAncestors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataplexEntryEntrySourceAncestors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__956325656b8a75b70a142638ef2c194be6f64bdd83f87fd04f024d90f6a8e5cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexEntryEntrySourceAncestorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexEntry.DataplexEntryEntrySourceAncestorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__704f3c501063e4754fbda30d767e1d19da864689b7ea6a831177193dcfb6de3b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__224f7b6a10636a04b6fe512e4babcd110a6f2ff4ca03e6a7592d54101757b33b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a045629247e7b1ab7555cd5fb0dd2c5b8156818b474653972b4fe200e8f92631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexEntryEntrySourceAncestors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexEntryEntrySourceAncestors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexEntryEntrySourceAncestors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7414d493e9cf55f17d9edf5a059e670caf8a46d45661d467ab9e766612d0f6d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexEntryEntrySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexEntry.DataplexEntryEntrySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4a1cc2372d7df84ebd21fac80d5c1c27f2f6a181f39ba68344dc16557d4b58f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAncestors")
    def put_ancestors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataplexEntryEntrySourceAncestors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb6a2337c8f5375dd08e7a6ff827794163258b3eef68d795afd62e214c85fc88)
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
    def ancestors(self) -> DataplexEntryEntrySourceAncestorsList:
        return typing.cast(DataplexEntryEntrySourceAncestorsList, jsii.get(self, "ancestors"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="ancestorsInput")
    def ancestors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataplexEntryEntrySourceAncestors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataplexEntryEntrySourceAncestors]]], jsii.get(self, "ancestorsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__375d89d275d33e5b071018dfff33df833b7b47850be2b25884717da7f66861ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34c783531ae91b89b9f8414bea3be26b1957283fa78b755b44efa8ada71d222e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e872fdf2c120a2e0439e199d583100f513224b009aebab949587760043aa119)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__544c660d3bf3d7276161fc7ca19e50897743db051580c18a6d71fb601e224649)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @platform.setter
    def platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088a94945ba0148b36298c812bc4da470e80786244d2a67b677bdcac49adc300)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d62fb7e414c2b0a7e58feb6c5afdf7f16597292c83fd327aad609d6662b6f83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemAttribute")
    def system_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemAttribute"))

    @system_attribute.setter
    def system_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7fa1ff72caa14fee709603f1cdac2087ea7f88f453b1e96366051efba5f080e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @update_time.setter
    def update_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ba072ef7ad5d3b390c361acb88d2bb816e752af082d7dbb61d0d41be4657c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexEntryEntrySource]:
        return typing.cast(typing.Optional[DataplexEntryEntrySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataplexEntryEntrySource]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844b8cb150317b6f7fb1ca30a521b0051dcb9c5ad65922a069192599be362c2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexEntry.DataplexEntryTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataplexEntryTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#create DataplexEntry#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#delete DataplexEntry#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#update DataplexEntry#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b1e20af0f4d1b6f642dd65c17d1822212a6b677184c0e70b9cba125ce2d52a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#create DataplexEntry#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#delete DataplexEntry#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_entry#update DataplexEntry#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexEntryTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexEntryTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexEntry.DataplexEntryTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52bc5d97bf865f0dedf7c1cd3df253b6ae763f757691495d4b3b387cd6697aad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb6d7982ea7e276965d18949e44c8d335b710a49db71885ad706e940bb17c0aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e907ceaccdb910f5cb6a3f4b74747b627173139b1e53e5d03fd4a55a72cd3c98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a48b1c4f7a21745adc9b241ab2563c43f9022461be670681c54f9afa3f9188f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexEntryTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexEntryTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexEntryTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__488be1d6533e5d3498df35be83a47feca60c07859b641bb8bd3b0d9f548e00eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataplexEntry",
    "DataplexEntryAspects",
    "DataplexEntryAspectsAspect",
    "DataplexEntryAspectsAspectOutputReference",
    "DataplexEntryAspectsList",
    "DataplexEntryAspectsOutputReference",
    "DataplexEntryConfig",
    "DataplexEntryEntrySource",
    "DataplexEntryEntrySourceAncestors",
    "DataplexEntryEntrySourceAncestorsList",
    "DataplexEntryEntrySourceAncestorsOutputReference",
    "DataplexEntryEntrySourceOutputReference",
    "DataplexEntryTimeouts",
    "DataplexEntryTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__dee993c664e2ea81ab041fa8d322c8d7b4c10b4848b9c62c84da00040fbb4fe1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    entry_type: builtins.str,
    aspects: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataplexEntryAspects, typing.Dict[builtins.str, typing.Any]]]]] = None,
    entry_group_id: typing.Optional[builtins.str] = None,
    entry_id: typing.Optional[builtins.str] = None,
    entry_source: typing.Optional[typing.Union[DataplexEntryEntrySource, typing.Dict[builtins.str, typing.Any]]] = None,
    fully_qualified_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    parent_entry: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataplexEntryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__daa3c8341682d5865a4ca04ac14f5620a391f9aa6183bbd8df73304d9d97d65d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df58d5dbc72356b86401eb7383737fa9f6f0741dfddc23a1664dc23426f2da31(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataplexEntryAspects, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__912f3958ae4abbb879b8f0c367789eaae66f0a4d9562ed53fafdb280aa72d39f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f8f72d6a614691f7149ea9d36524d563a43ed6aaf902244dbee2d27d926229(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdae445589eb546e62b120b167537b4c65b06f4a87836580b4ee8330e5ceda43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799650a3cb337e1d9df8ac016a1925c7a3e67e61b4e3649acc9cb8dd5770b75e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f6130552525f154c57bdf8ede4e705297adfc932165d015e72e0f387d363ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205dccef8bb6b708dd918576916deb8f26f65a475606be54dec470c3aa267e1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79a226b6fbdd5fa815aa115e969159756927b7289c948094ebd9824201d21db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3db3b35891b504fbb53f974443ab42b00e6ec3b708d5fe8d2a056c8d58803fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__136360cefb1f5260ff46f4c2fd76b610ae57c6a971d7b56d3fa468c43127bef2(
    *,
    aspect: typing.Union[DataplexEntryAspectsAspect, typing.Dict[builtins.str, typing.Any]],
    aspect_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899a4df70587095c7cbfa958272d99007670371e7d8198af0fbf01fa5868ba0b(
    *,
    data: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ed7e66ca1fe9a6295c6e40c913a2035248bf8045ec78ba66396356569ab790(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908d237a524dc6cc071d29de2d2a3a3327d627bc80de5cde0c3d554429200917(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e27e5ed8a7114682e534fe66913877990b7a67e74ab4fbdb256e2a7b1002b6(
    value: typing.Optional[DataplexEntryAspectsAspect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308e59897a8995fd4a3fde6a58fe708700afff94c528a50373a6493c5805624f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3faf0b98d33cf3de2377751209fe1bc1855f634fb0b322c755f03ce49df940af(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953d2026fd96b6e8df6d58b5edd61f58937f5f5c5d0a1b7407ee790893e0fdb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9d8557c30c98fd74193c925cb9d4a204b301e481d74f92b043663ac84a0b2e5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b16fb15d7edf4a4bcc59fdd8e8c07ecfc99cb93b52f90d06f09c42bc10821f91(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf581716ab2a6347c376878022b40187f0115eefe51700a6200669de63ff93a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataplexEntryAspects]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e3c45496077bf9222b12ff5a81cb86b093488ce22e26e8e1abc5c2956184889(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250adb13195a450f7d4f50aae7bae996bc49c1e354531a05e3465670d93e16c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073ada29c413c0e7ca8ff40745d68a5510de1e067be220489db3995e0552d311(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexEntryAspects]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de93d67cbfa0702744ad1927bb956e66ed1238ad08a2f72f51894068bc43295(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    entry_type: builtins.str,
    aspects: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataplexEntryAspects, typing.Dict[builtins.str, typing.Any]]]]] = None,
    entry_group_id: typing.Optional[builtins.str] = None,
    entry_id: typing.Optional[builtins.str] = None,
    entry_source: typing.Optional[typing.Union[DataplexEntryEntrySource, typing.Dict[builtins.str, typing.Any]]] = None,
    fully_qualified_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    parent_entry: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataplexEntryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4613345ef4ae3872d646c486214f384d742d7417196bc790ae127b4e424abf64(
    *,
    ancestors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataplexEntryEntrySourceAncestors, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__332ecf58d14ae50db266ad5ddcdaa4e541658cbd08d56d52de9a62dd840e8057(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c526d4b273fc82dc7ae02b4d505cff36cc9d59d6069266cb00740eb3bd37d4ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__251d9810f17f86b56a61b62fc07831ab3be79eae23bff2e30a869105113a50ff(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de704c2ae99118c01c49bd2e1e985428bea4638f6bb2e1a9224e63005b8691f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2210e9179ba3c4779aa7bfed47b1de4d3b85343e144d5d55cf6e59715321bc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1278f0fb3d5ac6d5d7e6143e6e0b46ad86aefd4f575cb7457c808b3a28229264(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956325656b8a75b70a142638ef2c194be6f64bdd83f87fd04f024d90f6a8e5cc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataplexEntryEntrySourceAncestors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__704f3c501063e4754fbda30d767e1d19da864689b7ea6a831177193dcfb6de3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__224f7b6a10636a04b6fe512e4babcd110a6f2ff4ca03e6a7592d54101757b33b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a045629247e7b1ab7555cd5fb0dd2c5b8156818b474653972b4fe200e8f92631(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7414d493e9cf55f17d9edf5a059e670caf8a46d45661d467ab9e766612d0f6d3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexEntryEntrySourceAncestors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a1cc2372d7df84ebd21fac80d5c1c27f2f6a181f39ba68344dc16557d4b58f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6a2337c8f5375dd08e7a6ff827794163258b3eef68d795afd62e214c85fc88(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataplexEntryEntrySourceAncestors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375d89d275d33e5b071018dfff33df833b7b47850be2b25884717da7f66861ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c783531ae91b89b9f8414bea3be26b1957283fa78b755b44efa8ada71d222e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e872fdf2c120a2e0439e199d583100f513224b009aebab949587760043aa119(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544c660d3bf3d7276161fc7ca19e50897743db051580c18a6d71fb601e224649(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088a94945ba0148b36298c812bc4da470e80786244d2a67b677bdcac49adc300(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d62fb7e414c2b0a7e58feb6c5afdf7f16597292c83fd327aad609d6662b6f83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fa1ff72caa14fee709603f1cdac2087ea7f88f453b1e96366051efba5f080e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ba072ef7ad5d3b390c361acb88d2bb816e752af082d7dbb61d0d41be4657c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844b8cb150317b6f7fb1ca30a521b0051dcb9c5ad65922a069192599be362c2b(
    value: typing.Optional[DataplexEntryEntrySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b1e20af0f4d1b6f642dd65c17d1822212a6b677184c0e70b9cba125ce2d52a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52bc5d97bf865f0dedf7c1cd3df253b6ae763f757691495d4b3b387cd6697aad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb6d7982ea7e276965d18949e44c8d335b710a49db71885ad706e940bb17c0aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e907ceaccdb910f5cb6a3f4b74747b627173139b1e53e5d03fd4a55a72cd3c98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a48b1c4f7a21745adc9b241ab2563c43f9022461be670681c54f9afa3f9188f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488be1d6533e5d3498df35be83a47feca60c07859b641bb8bd3b0d9f548e00eb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexEntryTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

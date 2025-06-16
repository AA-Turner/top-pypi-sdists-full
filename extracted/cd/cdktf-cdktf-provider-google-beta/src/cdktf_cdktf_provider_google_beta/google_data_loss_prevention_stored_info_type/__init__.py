r'''
# `google_data_loss_prevention_stored_info_type`

Refer to the Terraform Registry for docs: [`google_data_loss_prevention_stored_info_type`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type).
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


class GoogleDataLossPreventionStoredInfoType(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoType",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type google_data_loss_prevention_stored_info_type}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        parent: builtins.str,
        description: typing.Optional[builtins.str] = None,
        dictionary: typing.Optional[typing.Union["GoogleDataLossPreventionStoredInfoTypeDictionary", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        large_custom_dictionary: typing.Optional[typing.Union["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary", typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[typing.Union["GoogleDataLossPreventionStoredInfoTypeRegex", typing.Dict[builtins.str, typing.Any]]] = None,
        stored_info_type_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataLossPreventionStoredInfoTypeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type google_data_loss_prevention_stored_info_type} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param parent: The parent of the info type in any of the following formats:. - 'projects/{{project}}' - 'projects/{{project}}/locations/{{location}}' - 'organizations/{{organization_id}}' - 'organizations/{{organization_id}}/locations/{{location}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#parent GoogleDataLossPreventionStoredInfoType#parent}
        :param description: A description of the info type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#description GoogleDataLossPreventionStoredInfoType#description}
        :param dictionary: dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#dictionary GoogleDataLossPreventionStoredInfoType#dictionary}
        :param display_name: User set display name of the info type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#display_name GoogleDataLossPreventionStoredInfoType#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#id GoogleDataLossPreventionStoredInfoType#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param large_custom_dictionary: large_custom_dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#large_custom_dictionary GoogleDataLossPreventionStoredInfoType#large_custom_dictionary}
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#regex GoogleDataLossPreventionStoredInfoType#regex}
        :param stored_info_type_id: The storedInfoType ID can contain uppercase and lowercase letters, numbers, and hyphens; that is, it must match the regular expression: [a-zA-Z\\d-_]+. The maximum length is 100 characters. Can be empty to allow the system to generate one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#stored_info_type_id GoogleDataLossPreventionStoredInfoType#stored_info_type_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#timeouts GoogleDataLossPreventionStoredInfoType#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f13228fc5d00a1a8f5560e0144dbd3bd1843debe9d2760fcd2b10c54a4c9215)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataLossPreventionStoredInfoTypeConfig(
            parent=parent,
            description=description,
            dictionary=dictionary,
            display_name=display_name,
            id=id,
            large_custom_dictionary=large_custom_dictionary,
            regex=regex,
            stored_info_type_id=stored_info_type_id,
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
        '''Generates CDKTF code for importing a GoogleDataLossPreventionStoredInfoType resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataLossPreventionStoredInfoType to import.
        :param import_from_id: The id of the existing GoogleDataLossPreventionStoredInfoType that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataLossPreventionStoredInfoType to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60493e4a8fdcffabfa9ee0cad57db3763bb659e1d6bee788187edb5b84a58f7d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDictionary")
    def put_dictionary(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union["GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePath", typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union["GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#cloud_storage_path GoogleDataLossPreventionStoredInfoType#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#word_list GoogleDataLossPreventionStoredInfoType#word_list}
        '''
        value = GoogleDataLossPreventionStoredInfoTypeDictionary(
            cloud_storage_path=cloud_storage_path, word_list=word_list
        )

        return typing.cast(None, jsii.invoke(self, "putDictionary", [value]))

    @jsii.member(jsii_name="putLargeCustomDictionary")
    def put_large_custom_dictionary(
        self,
        *,
        output_path: typing.Union["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath", typing.Dict[builtins.str, typing.Any]],
        big_query_field: typing.Optional[typing.Union["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_storage_file_set: typing.Optional[typing.Union["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param output_path: output_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#output_path GoogleDataLossPreventionStoredInfoType#output_path}
        :param big_query_field: big_query_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#big_query_field GoogleDataLossPreventionStoredInfoType#big_query_field}
        :param cloud_storage_file_set: cloud_storage_file_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#cloud_storage_file_set GoogleDataLossPreventionStoredInfoType#cloud_storage_file_set}
        '''
        value = GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary(
            output_path=output_path,
            big_query_field=big_query_field,
            cloud_storage_file_set=cloud_storage_file_set,
        )

        return typing.cast(None, jsii.invoke(self, "putLargeCustomDictionary", [value]))

    @jsii.member(jsii_name="putRegex")
    def put_regex(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#pattern GoogleDataLossPreventionStoredInfoType#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#group_indexes GoogleDataLossPreventionStoredInfoType#group_indexes}
        '''
        value = GoogleDataLossPreventionStoredInfoTypeRegex(
            pattern=pattern, group_indexes=group_indexes
        )

        return typing.cast(None, jsii.invoke(self, "putRegex", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#create GoogleDataLossPreventionStoredInfoType#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#delete GoogleDataLossPreventionStoredInfoType#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#update GoogleDataLossPreventionStoredInfoType#update}.
        '''
        value = GoogleDataLossPreventionStoredInfoTypeTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDictionary")
    def reset_dictionary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDictionary", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLargeCustomDictionary")
    def reset_large_custom_dictionary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLargeCustomDictionary", []))

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @jsii.member(jsii_name="resetStoredInfoTypeId")
    def reset_stored_info_type_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStoredInfoTypeId", []))

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
    @jsii.member(jsii_name="dictionary")
    def dictionary(
        self,
    ) -> "GoogleDataLossPreventionStoredInfoTypeDictionaryOutputReference":
        return typing.cast("GoogleDataLossPreventionStoredInfoTypeDictionaryOutputReference", jsii.get(self, "dictionary"))

    @builtins.property
    @jsii.member(jsii_name="largeCustomDictionary")
    def large_custom_dictionary(
        self,
    ) -> "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputReference":
        return typing.cast("GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputReference", jsii.get(self, "largeCustomDictionary"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> "GoogleDataLossPreventionStoredInfoTypeRegexOutputReference":
        return typing.cast("GoogleDataLossPreventionStoredInfoTypeRegexOutputReference", jsii.get(self, "regex"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleDataLossPreventionStoredInfoTypeTimeoutsOutputReference":
        return typing.cast("GoogleDataLossPreventionStoredInfoTypeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dictionaryInput")
    def dictionary_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionStoredInfoTypeDictionary"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionStoredInfoTypeDictionary"], jsii.get(self, "dictionaryInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="largeCustomDictionaryInput")
    def large_custom_dictionary_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary"], jsii.get(self, "largeCustomDictionaryInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionStoredInfoTypeRegex"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionStoredInfoTypeRegex"], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="storedInfoTypeIdInput")
    def stored_info_type_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storedInfoTypeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataLossPreventionStoredInfoTypeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataLossPreventionStoredInfoTypeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3966aa79e92046d45c1274719e36a1530f14f2a6d76de279c19c7a1c6b5520c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241045139ab89c2c0e01d7d79fd93e64066d49a83172cb275c36bd415b6ccdc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb8b70f5eac09d2e50bee55b60ddeccd77991168087415a2458f44cacad94cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82fcb244674289c6ffd439ca498bd333ddde9039f9463baf5eb51c108a87c2b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storedInfoTypeId")
    def stored_info_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storedInfoTypeId"))

    @stored_info_type_id.setter
    def stored_info_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a16fe2403a7d449dd83a7f67dc5100d0b997410309c47e6fa64d1fcf8a0f803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storedInfoTypeId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeConfig",
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
        "description": "description",
        "dictionary": "dictionary",
        "display_name": "displayName",
        "id": "id",
        "large_custom_dictionary": "largeCustomDictionary",
        "regex": "regex",
        "stored_info_type_id": "storedInfoTypeId",
        "timeouts": "timeouts",
    },
)
class GoogleDataLossPreventionStoredInfoTypeConfig(
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
        parent: builtins.str,
        description: typing.Optional[builtins.str] = None,
        dictionary: typing.Optional[typing.Union["GoogleDataLossPreventionStoredInfoTypeDictionary", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        large_custom_dictionary: typing.Optional[typing.Union["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary", typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[typing.Union["GoogleDataLossPreventionStoredInfoTypeRegex", typing.Dict[builtins.str, typing.Any]]] = None,
        stored_info_type_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataLossPreventionStoredInfoTypeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param parent: The parent of the info type in any of the following formats:. - 'projects/{{project}}' - 'projects/{{project}}/locations/{{location}}' - 'organizations/{{organization_id}}' - 'organizations/{{organization_id}}/locations/{{location}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#parent GoogleDataLossPreventionStoredInfoType#parent}
        :param description: A description of the info type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#description GoogleDataLossPreventionStoredInfoType#description}
        :param dictionary: dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#dictionary GoogleDataLossPreventionStoredInfoType#dictionary}
        :param display_name: User set display name of the info type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#display_name GoogleDataLossPreventionStoredInfoType#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#id GoogleDataLossPreventionStoredInfoType#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param large_custom_dictionary: large_custom_dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#large_custom_dictionary GoogleDataLossPreventionStoredInfoType#large_custom_dictionary}
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#regex GoogleDataLossPreventionStoredInfoType#regex}
        :param stored_info_type_id: The storedInfoType ID can contain uppercase and lowercase letters, numbers, and hyphens; that is, it must match the regular expression: [a-zA-Z\\d-_]+. The maximum length is 100 characters. Can be empty to allow the system to generate one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#stored_info_type_id GoogleDataLossPreventionStoredInfoType#stored_info_type_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#timeouts GoogleDataLossPreventionStoredInfoType#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(dictionary, dict):
            dictionary = GoogleDataLossPreventionStoredInfoTypeDictionary(**dictionary)
        if isinstance(large_custom_dictionary, dict):
            large_custom_dictionary = GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary(**large_custom_dictionary)
        if isinstance(regex, dict):
            regex = GoogleDataLossPreventionStoredInfoTypeRegex(**regex)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataLossPreventionStoredInfoTypeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e0b97e14de631504776ed6a9538c55f03e330d707921ac0167f664c4724b26)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dictionary", value=dictionary, expected_type=type_hints["dictionary"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument large_custom_dictionary", value=large_custom_dictionary, expected_type=type_hints["large_custom_dictionary"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument stored_info_type_id", value=stored_info_type_id, expected_type=type_hints["stored_info_type_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parent": parent,
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
        if dictionary is not None:
            self._values["dictionary"] = dictionary
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if large_custom_dictionary is not None:
            self._values["large_custom_dictionary"] = large_custom_dictionary
        if regex is not None:
            self._values["regex"] = regex
        if stored_info_type_id is not None:
            self._values["stored_info_type_id"] = stored_info_type_id
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
    def parent(self) -> builtins.str:
        '''The parent of the info type in any of the following formats:.

        - 'projects/{{project}}'
        - 'projects/{{project}}/locations/{{location}}'
        - 'organizations/{{organization_id}}'
        - 'organizations/{{organization_id}}/locations/{{location}}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#parent GoogleDataLossPreventionStoredInfoType#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the info type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#description GoogleDataLossPreventionStoredInfoType#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dictionary(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionStoredInfoTypeDictionary"]:
        '''dictionary block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#dictionary GoogleDataLossPreventionStoredInfoType#dictionary}
        '''
        result = self._values.get("dictionary")
        return typing.cast(typing.Optional["GoogleDataLossPreventionStoredInfoTypeDictionary"], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User set display name of the info type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#display_name GoogleDataLossPreventionStoredInfoType#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#id GoogleDataLossPreventionStoredInfoType#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def large_custom_dictionary(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary"]:
        '''large_custom_dictionary block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#large_custom_dictionary GoogleDataLossPreventionStoredInfoType#large_custom_dictionary}
        '''
        result = self._values.get("large_custom_dictionary")
        return typing.cast(typing.Optional["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary"], result)

    @builtins.property
    def regex(self) -> typing.Optional["GoogleDataLossPreventionStoredInfoTypeRegex"]:
        '''regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#regex GoogleDataLossPreventionStoredInfoType#regex}
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional["GoogleDataLossPreventionStoredInfoTypeRegex"], result)

    @builtins.property
    def stored_info_type_id(self) -> typing.Optional[builtins.str]:
        '''The storedInfoType ID can contain uppercase and lowercase letters, numbers, and hyphens;

        that is, it must match the regular expression: [a-zA-Z\\d-_]+. The maximum length is 100
        characters. Can be empty to allow the system to generate one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#stored_info_type_id GoogleDataLossPreventionStoredInfoType#stored_info_type_id}
        '''
        result = self._values.get("stored_info_type_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionStoredInfoTypeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#timeouts GoogleDataLossPreventionStoredInfoType#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataLossPreventionStoredInfoTypeTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionStoredInfoTypeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeDictionary",
    jsii_struct_bases=[],
    name_mapping={"cloud_storage_path": "cloudStoragePath", "word_list": "wordList"},
)
class GoogleDataLossPreventionStoredInfoTypeDictionary:
    def __init__(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union["GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePath", typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union["GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#cloud_storage_path GoogleDataLossPreventionStoredInfoType#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#word_list GoogleDataLossPreventionStoredInfoType#word_list}
        '''
        if isinstance(cloud_storage_path, dict):
            cloud_storage_path = GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePath(**cloud_storage_path)
        if isinstance(word_list, dict):
            word_list = GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStruct(**word_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae9c364aaf755850480dd00e276cad0b25f8245ed23a0085f0301f69dc299e73)
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
    ) -> typing.Optional["GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePath"]:
        '''cloud_storage_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#cloud_storage_path GoogleDataLossPreventionStoredInfoType#cloud_storage_path}
        '''
        result = self._values.get("cloud_storage_path")
        return typing.cast(typing.Optional["GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePath"], result)

    @builtins.property
    def word_list(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStruct"]:
        '''word_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#word_list GoogleDataLossPreventionStoredInfoType#word_list}
        '''
        result = self._values.get("word_list")
        return typing.cast(typing.Optional["GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStruct"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionStoredInfoTypeDictionary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePath",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePath:
    def __init__(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#path GoogleDataLossPreventionStoredInfoType#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc299aa540c2d94774e23bd7acc2ec8506a23373171ffe47f5244990e9907af4)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#path GoogleDataLossPreventionStoredInfoType#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13f2d3e44c188b2f5fa44e947530424028969b0c443738afa78df533cd98f52d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0eb52e00b360b8936dda409e0534db0b090a23473882a1eb498d8e7279722df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b28abb95244d20c87f406d821a4add388aae8c11d2bee73bdbd4d1201b2c5810)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionStoredInfoTypeDictionaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeDictionaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63d4396de45e5cd096838dd98a577fb91e95748198bae326676913f79d88ac0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudStoragePath")
    def put_cloud_storage_path(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#path GoogleDataLossPreventionStoredInfoType#path}
        '''
        value = GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePath(
            path=path
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStoragePath", [value]))

    @jsii.member(jsii_name="putWordList")
    def put_word_list(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#words GoogleDataLossPreventionStoredInfoType#words}
        '''
        value = GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStruct(
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
    ) -> GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePathOutputReference:
        return typing.cast(GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePathOutputReference, jsii.get(self, "cloudStoragePath"))

    @builtins.property
    @jsii.member(jsii_name="wordList")
    def word_list(
        self,
    ) -> "GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStructOutputReference":
        return typing.cast("GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStructOutputReference", jsii.get(self, "wordList"))

    @builtins.property
    @jsii.member(jsii_name="cloudStoragePathInput")
    def cloud_storage_path_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePath], jsii.get(self, "cloudStoragePathInput"))

    @builtins.property
    @jsii.member(jsii_name="wordListInput")
    def word_list_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStruct"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStruct"], jsii.get(self, "wordListInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionStoredInfoTypeDictionary]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionStoredInfoTypeDictionary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeDictionary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__390e65a7cf2d89c3cf9710e046e8f8e3e25d94121bf28fef8b301e856e1607c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStruct",
    jsii_struct_bases=[],
    name_mapping={"words": "words"},
)
class GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStruct:
    def __init__(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#words GoogleDataLossPreventionStoredInfoType#words}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c8f4b14494bb02acc78116001e7579bad8d796b193312f41071ef6f564d4688)
            check_type(argname="argument words", value=words, expected_type=type_hints["words"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "words": words,
        }

    @builtins.property
    def words(self) -> typing.List[builtins.str]:
        '''Words or phrases defining the dictionary.

        The dictionary must contain at least one
        phrase and every phrase must contain at least 2 characters that are letters or digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#words GoogleDataLossPreventionStoredInfoType#words}
        '''
        result = self._values.get("words")
        assert result is not None, "Required property 'words' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5903d1d783cbcac93490243311839adc54261f5cfba9eaf68a336e30ad5f8078)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abb0a2098244ba3d9d7f2c05ebbaf4ecf6010c5c844abb8397d1521a4a096973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "words", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStruct]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cadd51c6226d9d4fda6ee89ded1eaa42ec8b386f2cb575bbabeb9b38d8d989b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary",
    jsii_struct_bases=[],
    name_mapping={
        "output_path": "outputPath",
        "big_query_field": "bigQueryField",
        "cloud_storage_file_set": "cloudStorageFileSet",
    },
)
class GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary:
    def __init__(
        self,
        *,
        output_path: typing.Union["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath", typing.Dict[builtins.str, typing.Any]],
        big_query_field: typing.Optional[typing.Union["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_storage_file_set: typing.Optional[typing.Union["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param output_path: output_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#output_path GoogleDataLossPreventionStoredInfoType#output_path}
        :param big_query_field: big_query_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#big_query_field GoogleDataLossPreventionStoredInfoType#big_query_field}
        :param cloud_storage_file_set: cloud_storage_file_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#cloud_storage_file_set GoogleDataLossPreventionStoredInfoType#cloud_storage_file_set}
        '''
        if isinstance(output_path, dict):
            output_path = GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath(**output_path)
        if isinstance(big_query_field, dict):
            big_query_field = GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField(**big_query_field)
        if isinstance(cloud_storage_file_set, dict):
            cloud_storage_file_set = GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet(**cloud_storage_file_set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77970925b987709b9eeaf75f3706914d8b197998215d29ef9c3975e45f0243de)
            check_type(argname="argument output_path", value=output_path, expected_type=type_hints["output_path"])
            check_type(argname="argument big_query_field", value=big_query_field, expected_type=type_hints["big_query_field"])
            check_type(argname="argument cloud_storage_file_set", value=cloud_storage_file_set, expected_type=type_hints["cloud_storage_file_set"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "output_path": output_path,
        }
        if big_query_field is not None:
            self._values["big_query_field"] = big_query_field
        if cloud_storage_file_set is not None:
            self._values["cloud_storage_file_set"] = cloud_storage_file_set

    @builtins.property
    def output_path(
        self,
    ) -> "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath":
        '''output_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#output_path GoogleDataLossPreventionStoredInfoType#output_path}
        '''
        result = self._values.get("output_path")
        assert result is not None, "Required property 'output_path' is missing"
        return typing.cast("GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath", result)

    @builtins.property
    def big_query_field(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField"]:
        '''big_query_field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#big_query_field GoogleDataLossPreventionStoredInfoType#big_query_field}
        '''
        result = self._values.get("big_query_field")
        return typing.cast(typing.Optional["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField"], result)

    @builtins.property
    def cloud_storage_file_set(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet"]:
        '''cloud_storage_file_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#cloud_storage_file_set GoogleDataLossPreventionStoredInfoType#cloud_storage_file_set}
        '''
        result = self._values.get("cloud_storage_file_set")
        return typing.cast(typing.Optional["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField",
    jsii_struct_bases=[],
    name_mapping={"field": "field", "table": "table"},
)
class GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField:
    def __init__(
        self,
        *,
        field: typing.Union["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField", typing.Dict[builtins.str, typing.Any]],
        table: typing.Union["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param field: field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#field GoogleDataLossPreventionStoredInfoType#field}
        :param table: table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#table GoogleDataLossPreventionStoredInfoType#table}
        '''
        if isinstance(field, dict):
            field = GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField(**field)
        if isinstance(table, dict):
            table = GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable(**table)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b207b654aaac95b2c3437da1b409e03dc63ba76489d5e3bc2a909eb737aff4b)
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "field": field,
            "table": table,
        }

    @builtins.property
    def field(
        self,
    ) -> "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField":
        '''field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#field GoogleDataLossPreventionStoredInfoType#field}
        '''
        result = self._values.get("field")
        assert result is not None, "Required property 'field' is missing"
        return typing.cast("GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField", result)

    @builtins.property
    def table(
        self,
    ) -> "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable":
        '''table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#table GoogleDataLossPreventionStoredInfoType#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast("GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Name describing the field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#name GoogleDataLossPreventionStoredInfoType#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8307698bff81fca13a288f4e9521874a5eeb8d68a7a7ce17b7723e3da3616b3b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name describing the field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#name GoogleDataLossPreventionStoredInfoType#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8019a3ab0787c38b57174981b78eaadc263955b5c6ae9f9edb66ac3b42b6c677)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0482a5418559b5c5c6b39a9ca73e8a97743d04fa36658f69c2de3cfb47a70298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f915e3c67b3172664a46d599d428afab55315ff87b76d57911d528918e78a0e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1f167a8df7f680d86cd3d13545563338921877248cb8f7b93aec4955c0ebfc2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putField")
    def put_field(self, *, name: builtins.str) -> None:
        '''
        :param name: Name describing the field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#name GoogleDataLossPreventionStoredInfoType#name}
        '''
        value = GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putField", [value]))

    @jsii.member(jsii_name="putTable")
    def put_table(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The dataset ID of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#dataset_id GoogleDataLossPreventionStoredInfoType#dataset_id}
        :param project_id: The Google Cloud Platform project ID of the project containing the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#project_id GoogleDataLossPreventionStoredInfoType#project_id}
        :param table_id: The name of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#table_id GoogleDataLossPreventionStoredInfoType#table_id}
        '''
        value = GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable(
            dataset_id=dataset_id, project_id=project_id, table_id=table_id
        )

        return typing.cast(None, jsii.invoke(self, "putTable", [value]))

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(
        self,
    ) -> GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldFieldOutputReference:
        return typing.cast(GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldFieldOutputReference, jsii.get(self, "field"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(
        self,
    ) -> "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTableOutputReference":
        return typing.cast("GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTableOutputReference", jsii.get(self, "table"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable"], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea6cd74ab5fc6b784b4b6e65d1e760ad77e12cf0c30c23daf665690c0f017d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id": "datasetId",
        "project_id": "projectId",
        "table_id": "tableId",
    },
)
class GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable:
    def __init__(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The dataset ID of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#dataset_id GoogleDataLossPreventionStoredInfoType#dataset_id}
        :param project_id: The Google Cloud Platform project ID of the project containing the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#project_id GoogleDataLossPreventionStoredInfoType#project_id}
        :param table_id: The name of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#table_id GoogleDataLossPreventionStoredInfoType#table_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ad35fef4647d670dbe1fab095d3b7a1e32f239f34a54f8aa11bf998f9c63eb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#dataset_id GoogleDataLossPreventionStoredInfoType#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The Google Cloud Platform project ID of the project containing the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#project_id GoogleDataLossPreventionStoredInfoType#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_id(self) -> builtins.str:
        '''The name of the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#table_id GoogleDataLossPreventionStoredInfoType#table_id}
        '''
        result = self._values.get("table_id")
        assert result is not None, "Required property 'table_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91fb442e907db956f18d435e1eb1d1db63817a8dfbc1e1dae9ae427e00110606)
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
            type_hints = typing.get_type_hints(_typecheckingstub__310dbc706d652f3acf6fa25570a74755f886b12fe523153b572fbd2303273e2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb2d86ca34f5315285f8153be2dd1cc665dd0eacc304a5290958f5d276f5c873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9e14527d6171ac80936fe5da119baa08b7a8e71894797cfaabed16acba6efc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22dfa9c0450f6953b97d91be6fc7350ad0d9e21dd179cbb00842df1e01b77238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet",
    jsii_struct_bases=[],
    name_mapping={"url": "url"},
)
class GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet:
    def __init__(self, *, url: builtins.str) -> None:
        '''
        :param url: The url, in the format 'gs:///'. Trailing wildcard in the path is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#url GoogleDataLossPreventionStoredInfoType#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0efd92278b6846a8fc41b7fcc8acfd2889eab6b3e9e35b71b45e374fd859ab20)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }

    @builtins.property
    def url(self) -> builtins.str:
        '''The url, in the format 'gs:///'. Trailing wildcard in the path is allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#url GoogleDataLossPreventionStoredInfoType#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c475334cc0966fade4233e3cde769812c9880951a2c31939aa9dbce0302479de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__294d3c9f59cfe0973b1c43243d8eb48e5674fe614836cf4bad0e2402b6695f07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bed5918721b82b4787b425037c3623b782d4eb7987e4fd62dadd8ff360a2229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath:
    def __init__(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#path GoogleDataLossPreventionStoredInfoType#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a52b851d2e1befbe7133ddab3a43dd23c54e72b0a4048510afcb01bbef51138)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#path GoogleDataLossPreventionStoredInfoType#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4b1ccf56ce91fc5ee5e306eee4af3ab1af6bc8ab6b1c91de66c5526e18f06e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0261f26444e7d9311aca3cca6fddffa195831915147208a5c701d0a447ecc767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7aefab0f00c3934367cdb83cd39e389ef2f76e845bb587f4e9a9493ec8b23e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc33372f4b365977971f8ba81a9d82825a369f73943cf81267062bd36d4c72a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBigQueryField")
    def put_big_query_field(
        self,
        *,
        field: typing.Union[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField, typing.Dict[builtins.str, typing.Any]],
        table: typing.Union[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param field: field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#field GoogleDataLossPreventionStoredInfoType#field}
        :param table: table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#table GoogleDataLossPreventionStoredInfoType#table}
        '''
        value = GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField(
            field=field, table=table
        )

        return typing.cast(None, jsii.invoke(self, "putBigQueryField", [value]))

    @jsii.member(jsii_name="putCloudStorageFileSet")
    def put_cloud_storage_file_set(self, *, url: builtins.str) -> None:
        '''
        :param url: The url, in the format 'gs:///'. Trailing wildcard in the path is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#url GoogleDataLossPreventionStoredInfoType#url}
        '''
        value = GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet(
            url=url
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStorageFileSet", [value]))

    @jsii.member(jsii_name="putOutputPath")
    def put_output_path(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#path GoogleDataLossPreventionStoredInfoType#path}
        '''
        value = GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath(
            path=path
        )

        return typing.cast(None, jsii.invoke(self, "putOutputPath", [value]))

    @jsii.member(jsii_name="resetBigQueryField")
    def reset_big_query_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigQueryField", []))

    @jsii.member(jsii_name="resetCloudStorageFileSet")
    def reset_cloud_storage_file_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudStorageFileSet", []))

    @builtins.property
    @jsii.member(jsii_name="bigQueryField")
    def big_query_field(
        self,
    ) -> GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldOutputReference:
        return typing.cast(GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldOutputReference, jsii.get(self, "bigQueryField"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageFileSet")
    def cloud_storage_file_set(
        self,
    ) -> GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSetOutputReference:
        return typing.cast(GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSetOutputReference, jsii.get(self, "cloudStorageFileSet"))

    @builtins.property
    @jsii.member(jsii_name="outputPath")
    def output_path(
        self,
    ) -> GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPathOutputReference:
        return typing.cast(GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPathOutputReference, jsii.get(self, "outputPath"))

    @builtins.property
    @jsii.member(jsii_name="bigQueryFieldInput")
    def big_query_field_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField], jsii.get(self, "bigQueryFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageFileSetInput")
    def cloud_storage_file_set_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet], jsii.get(self, "cloudStorageFileSetInput"))

    @builtins.property
    @jsii.member(jsii_name="outputPathInput")
    def output_path_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath], jsii.get(self, "outputPathInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b01b00db4e989946e5b042df17c4429d81ceb18067e95a8f2b9da701e07eaf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeRegex",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern", "group_indexes": "groupIndexes"},
)
class GoogleDataLossPreventionStoredInfoTypeRegex:
    def __init__(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#pattern GoogleDataLossPreventionStoredInfoType#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#group_indexes GoogleDataLossPreventionStoredInfoType#group_indexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175500a9fb284692da21c09d22b9bdbee29a9151faedac83f19d74e681ad8267)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#pattern GoogleDataLossPreventionStoredInfoType#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_indexes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The index of the submatch to extract as findings.

        When not specified, the entire match is returned. No more than 3 may be included.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#group_indexes GoogleDataLossPreventionStoredInfoType#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionStoredInfoTypeRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionStoredInfoTypeRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f25c61d5701a810dcc013ed51464538f10a5037b73342a305cae784f2da698d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c51707e34cf715038a2d2829d2c7335fc0826213a6b8587249093fe110daf76d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f640d68ec8cf7066d663d68b983ee9e35983e5ad5e36bcff0e8061fa2e5b723b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionStoredInfoTypeRegex]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionStoredInfoTypeRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f219ffceaccae45626def7d096fec857612ffe258860d569e41dbd9c22d04156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataLossPreventionStoredInfoTypeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#create GoogleDataLossPreventionStoredInfoType#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#delete GoogleDataLossPreventionStoredInfoType#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#update GoogleDataLossPreventionStoredInfoType#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df4ccc372ac2ce3cd5432f09281f230077902889f4c3358d7f1f84a79124862b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#create GoogleDataLossPreventionStoredInfoType#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#delete GoogleDataLossPreventionStoredInfoType#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_stored_info_type#update GoogleDataLossPreventionStoredInfoType#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionStoredInfoTypeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionStoredInfoTypeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionStoredInfoType.GoogleDataLossPreventionStoredInfoTypeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adac1dc780b81259dbe7898f9c0100a3324348a89bf6d8852418769a2c289d88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b487c5838c577dc0a73c8ecd6444824d04d643b8e2710cc6144639e2302e086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4782d1e7724f6159e89ae4b268d540870303762c46f4ad140626ec858c82f7a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35ee5ad06de6ab2ce8e5ffaac6b18ab25b62fab2790dbfe3c09e80a9a896e642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionStoredInfoTypeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionStoredInfoTypeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionStoredInfoTypeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857944c13dec26563e7949b7ac6e7b28f2a1ae987c1234e5cd88bc51d076e294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDataLossPreventionStoredInfoType",
    "GoogleDataLossPreventionStoredInfoTypeConfig",
    "GoogleDataLossPreventionStoredInfoTypeDictionary",
    "GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePath",
    "GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePathOutputReference",
    "GoogleDataLossPreventionStoredInfoTypeDictionaryOutputReference",
    "GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStruct",
    "GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStructOutputReference",
    "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary",
    "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField",
    "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField",
    "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldFieldOutputReference",
    "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldOutputReference",
    "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable",
    "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTableOutputReference",
    "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet",
    "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSetOutputReference",
    "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath",
    "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPathOutputReference",
    "GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputReference",
    "GoogleDataLossPreventionStoredInfoTypeRegex",
    "GoogleDataLossPreventionStoredInfoTypeRegexOutputReference",
    "GoogleDataLossPreventionStoredInfoTypeTimeouts",
    "GoogleDataLossPreventionStoredInfoTypeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__1f13228fc5d00a1a8f5560e0144dbd3bd1843debe9d2760fcd2b10c54a4c9215(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    parent: builtins.str,
    description: typing.Optional[builtins.str] = None,
    dictionary: typing.Optional[typing.Union[GoogleDataLossPreventionStoredInfoTypeDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    large_custom_dictionary: typing.Optional[typing.Union[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
    regex: typing.Optional[typing.Union[GoogleDataLossPreventionStoredInfoTypeRegex, typing.Dict[builtins.str, typing.Any]]] = None,
    stored_info_type_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataLossPreventionStoredInfoTypeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__60493e4a8fdcffabfa9ee0cad57db3763bb659e1d6bee788187edb5b84a58f7d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3966aa79e92046d45c1274719e36a1530f14f2a6d76de279c19c7a1c6b5520c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241045139ab89c2c0e01d7d79fd93e64066d49a83172cb275c36bd415b6ccdc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb8b70f5eac09d2e50bee55b60ddeccd77991168087415a2458f44cacad94cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82fcb244674289c6ffd439ca498bd333ddde9039f9463baf5eb51c108a87c2b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a16fe2403a7d449dd83a7f67dc5100d0b997410309c47e6fa64d1fcf8a0f803(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e0b97e14de631504776ed6a9538c55f03e330d707921ac0167f664c4724b26(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parent: builtins.str,
    description: typing.Optional[builtins.str] = None,
    dictionary: typing.Optional[typing.Union[GoogleDataLossPreventionStoredInfoTypeDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    large_custom_dictionary: typing.Optional[typing.Union[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
    regex: typing.Optional[typing.Union[GoogleDataLossPreventionStoredInfoTypeRegex, typing.Dict[builtins.str, typing.Any]]] = None,
    stored_info_type_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataLossPreventionStoredInfoTypeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae9c364aaf755850480dd00e276cad0b25f8245ed23a0085f0301f69dc299e73(
    *,
    cloud_storage_path: typing.Optional[typing.Union[GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
    word_list: typing.Optional[typing.Union[GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc299aa540c2d94774e23bd7acc2ec8506a23373171ffe47f5244990e9907af4(
    *,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f2d3e44c188b2f5fa44e947530424028969b0c443738afa78df533cd98f52d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0eb52e00b360b8936dda409e0534db0b090a23473882a1eb498d8e7279722df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b28abb95244d20c87f406d821a4add388aae8c11d2bee73bdbd4d1201b2c5810(
    value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeDictionaryCloudStoragePath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d4396de45e5cd096838dd98a577fb91e95748198bae326676913f79d88ac0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390e65a7cf2d89c3cf9710e046e8f8e3e25d94121bf28fef8b301e856e1607c8(
    value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeDictionary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c8f4b14494bb02acc78116001e7579bad8d796b193312f41071ef6f564d4688(
    *,
    words: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5903d1d783cbcac93490243311839adc54261f5cfba9eaf68a336e30ad5f8078(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb0a2098244ba3d9d7f2c05ebbaf4ecf6010c5c844abb8397d1521a4a096973(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cadd51c6226d9d4fda6ee89ded1eaa42ec8b386f2cb575bbabeb9b38d8d989b(
    value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeDictionaryWordListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77970925b987709b9eeaf75f3706914d8b197998215d29ef9c3975e45f0243de(
    *,
    output_path: typing.Union[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath, typing.Dict[builtins.str, typing.Any]],
    big_query_field: typing.Optional[typing.Union[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_storage_file_set: typing.Optional[typing.Union[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b207b654aaac95b2c3437da1b409e03dc63ba76489d5e3bc2a909eb737aff4b(
    *,
    field: typing.Union[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField, typing.Dict[builtins.str, typing.Any]],
    table: typing.Union[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8307698bff81fca13a288f4e9521874a5eeb8d68a7a7ce17b7723e3da3616b3b(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8019a3ab0787c38b57174981b78eaadc263955b5c6ae9f9edb66ac3b42b6c677(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0482a5418559b5c5c6b39a9ca73e8a97743d04fa36658f69c2de3cfb47a70298(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f915e3c67b3172664a46d599d428afab55315ff87b76d57911d528918e78a0e4(
    value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1f167a8df7f680d86cd3d13545563338921877248cb8f7b93aec4955c0ebfc2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6cd74ab5fc6b784b4b6e65d1e760ad77e12cf0c30c23daf665690c0f017d5e(
    value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ad35fef4647d670dbe1fab095d3b7a1e32f239f34a54f8aa11bf998f9c63eb(
    *,
    dataset_id: builtins.str,
    project_id: builtins.str,
    table_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91fb442e907db956f18d435e1eb1d1db63817a8dfbc1e1dae9ae427e00110606(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310dbc706d652f3acf6fa25570a74755f886b12fe523153b572fbd2303273e2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2d86ca34f5315285f8153be2dd1cc665dd0eacc304a5290958f5d276f5c873(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9e14527d6171ac80936fe5da119baa08b7a8e71894797cfaabed16acba6efc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22dfa9c0450f6953b97d91be6fc7350ad0d9e21dd179cbb00842df1e01b77238(
    value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efd92278b6846a8fc41b7fcc8acfd2889eab6b3e9e35b71b45e374fd859ab20(
    *,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c475334cc0966fade4233e3cde769812c9880951a2c31939aa9dbce0302479de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294d3c9f59cfe0973b1c43243d8eb48e5674fe614836cf4bad0e2402b6695f07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bed5918721b82b4787b425037c3623b782d4eb7987e4fd62dadd8ff360a2229(
    value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a52b851d2e1befbe7133ddab3a43dd23c54e72b0a4048510afcb01bbef51138(
    *,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b1ccf56ce91fc5ee5e306eee4af3ab1af6bc8ab6b1c91de66c5526e18f06e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0261f26444e7d9311aca3cca6fddffa195831915147208a5c701d0a447ecc767(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7aefab0f00c3934367cdb83cd39e389ef2f76e845bb587f4e9a9493ec8b23e6(
    value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc33372f4b365977971f8ba81a9d82825a369f73943cf81267062bd36d4c72a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b01b00db4e989946e5b042df17c4429d81ceb18067e95a8f2b9da701e07eaf0(
    value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeLargeCustomDictionary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175500a9fb284692da21c09d22b9bdbee29a9151faedac83f19d74e681ad8267(
    *,
    pattern: builtins.str,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25c61d5701a810dcc013ed51464538f10a5037b73342a305cae784f2da698d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c51707e34cf715038a2d2829d2c7335fc0826213a6b8587249093fe110daf76d(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f640d68ec8cf7066d663d68b983ee9e35983e5ad5e36bcff0e8061fa2e5b723b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f219ffceaccae45626def7d096fec857612ffe258860d569e41dbd9c22d04156(
    value: typing.Optional[GoogleDataLossPreventionStoredInfoTypeRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4ccc372ac2ce3cd5432f09281f230077902889f4c3358d7f1f84a79124862b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adac1dc780b81259dbe7898f9c0100a3324348a89bf6d8852418769a2c289d88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b487c5838c577dc0a73c8ecd6444824d04d643b8e2710cc6144639e2302e086(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4782d1e7724f6159e89ae4b268d540870303762c46f4ad140626ec858c82f7a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ee5ad06de6ab2ce8e5ffaac6b18ab25b62fab2790dbfe3c09e80a9a896e642(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857944c13dec26563e7949b7ac6e7b28f2a1ae987c1234e5cd88bc51d076e294(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionStoredInfoTypeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

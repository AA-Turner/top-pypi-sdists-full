r'''
# `google_data_loss_prevention_stored_info_type`

Refer to the Terraform Registry for docs: [`google_data_loss_prevention_stored_info_type`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type).
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


class DataLossPreventionStoredInfoType(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoType",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type google_data_loss_prevention_stored_info_type}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        parent: builtins.str,
        description: typing.Optional[builtins.str] = None,
        dictionary: typing.Optional[typing.Union["DataLossPreventionStoredInfoTypeDictionary", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        large_custom_dictionary: typing.Optional[typing.Union["DataLossPreventionStoredInfoTypeLargeCustomDictionary", typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[typing.Union["DataLossPreventionStoredInfoTypeRegex", typing.Dict[builtins.str, typing.Any]]] = None,
        stored_info_type_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataLossPreventionStoredInfoTypeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type google_data_loss_prevention_stored_info_type} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param parent: The parent of the info type in any of the following formats:. - 'projects/{{project}}' - 'projects/{{project}}/locations/{{location}}' - 'organizations/{{organization_id}}' - 'organizations/{{organization_id}}/locations/{{location}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#parent DataLossPreventionStoredInfoType#parent}
        :param description: A description of the info type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#description DataLossPreventionStoredInfoType#description}
        :param dictionary: dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#dictionary DataLossPreventionStoredInfoType#dictionary}
        :param display_name: User set display name of the info type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#display_name DataLossPreventionStoredInfoType#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#id DataLossPreventionStoredInfoType#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param large_custom_dictionary: large_custom_dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#large_custom_dictionary DataLossPreventionStoredInfoType#large_custom_dictionary}
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#regex DataLossPreventionStoredInfoType#regex}
        :param stored_info_type_id: The storedInfoType ID can contain uppercase and lowercase letters, numbers, and hyphens; that is, it must match the regular expression: [a-zA-Z\\d-_]+. The maximum length is 100 characters. Can be empty to allow the system to generate one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#stored_info_type_id DataLossPreventionStoredInfoType#stored_info_type_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#timeouts DataLossPreventionStoredInfoType#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63fdff0bb027af40fa63b283eab87993180cd1cf6f0d71b6338e8b8508decd89)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataLossPreventionStoredInfoTypeConfig(
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
        '''Generates CDKTF code for importing a DataLossPreventionStoredInfoType resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataLossPreventionStoredInfoType to import.
        :param import_from_id: The id of the existing DataLossPreventionStoredInfoType that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataLossPreventionStoredInfoType to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3fa4a9d54c99cd018aae29934a827c855747678c25fcaaf52081dcb4c845198)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDictionary")
    def put_dictionary(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union["DataLossPreventionStoredInfoTypeDictionaryCloudStoragePath", typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union["DataLossPreventionStoredInfoTypeDictionaryWordListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#cloud_storage_path DataLossPreventionStoredInfoType#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#word_list DataLossPreventionStoredInfoType#word_list}
        '''
        value = DataLossPreventionStoredInfoTypeDictionary(
            cloud_storage_path=cloud_storage_path, word_list=word_list
        )

        return typing.cast(None, jsii.invoke(self, "putDictionary", [value]))

    @jsii.member(jsii_name="putLargeCustomDictionary")
    def put_large_custom_dictionary(
        self,
        *,
        output_path: typing.Union["DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath", typing.Dict[builtins.str, typing.Any]],
        big_query_field: typing.Optional[typing.Union["DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_storage_file_set: typing.Optional[typing.Union["DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param output_path: output_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#output_path DataLossPreventionStoredInfoType#output_path}
        :param big_query_field: big_query_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#big_query_field DataLossPreventionStoredInfoType#big_query_field}
        :param cloud_storage_file_set: cloud_storage_file_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#cloud_storage_file_set DataLossPreventionStoredInfoType#cloud_storage_file_set}
        '''
        value = DataLossPreventionStoredInfoTypeLargeCustomDictionary(
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
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#pattern DataLossPreventionStoredInfoType#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#group_indexes DataLossPreventionStoredInfoType#group_indexes}
        '''
        value = DataLossPreventionStoredInfoTypeRegex(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#create DataLossPreventionStoredInfoType#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#delete DataLossPreventionStoredInfoType#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#update DataLossPreventionStoredInfoType#update}.
        '''
        value = DataLossPreventionStoredInfoTypeTimeouts(
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
    def dictionary(self) -> "DataLossPreventionStoredInfoTypeDictionaryOutputReference":
        return typing.cast("DataLossPreventionStoredInfoTypeDictionaryOutputReference", jsii.get(self, "dictionary"))

    @builtins.property
    @jsii.member(jsii_name="largeCustomDictionary")
    def large_custom_dictionary(
        self,
    ) -> "DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputReference":
        return typing.cast("DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputReference", jsii.get(self, "largeCustomDictionary"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> "DataLossPreventionStoredInfoTypeRegexOutputReference":
        return typing.cast("DataLossPreventionStoredInfoTypeRegexOutputReference", jsii.get(self, "regex"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataLossPreventionStoredInfoTypeTimeoutsOutputReference":
        return typing.cast("DataLossPreventionStoredInfoTypeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dictionaryInput")
    def dictionary_input(
        self,
    ) -> typing.Optional["DataLossPreventionStoredInfoTypeDictionary"]:
        return typing.cast(typing.Optional["DataLossPreventionStoredInfoTypeDictionary"], jsii.get(self, "dictionaryInput"))

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
    ) -> typing.Optional["DataLossPreventionStoredInfoTypeLargeCustomDictionary"]:
        return typing.cast(typing.Optional["DataLossPreventionStoredInfoTypeLargeCustomDictionary"], jsii.get(self, "largeCustomDictionaryInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(self) -> typing.Optional["DataLossPreventionStoredInfoTypeRegex"]:
        return typing.cast(typing.Optional["DataLossPreventionStoredInfoTypeRegex"], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="storedInfoTypeIdInput")
    def stored_info_type_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storedInfoTypeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataLossPreventionStoredInfoTypeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataLossPreventionStoredInfoTypeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1efcbd39945dac0f8250626e5a0c6c1ef0c88a17a4bc6d6bf2f25bf79694af53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__196aae1aa59be61de3a898d32ec3d71cfc7b7a71273796eddc53fb6abb64876c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac9eaf458d1de32fb87f648541299258be3a542b8c830bdc837126de6b096d44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0060f6a5e375b77739d721d72ec7f8ac32866ff62861885e56d680adaee43247)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storedInfoTypeId")
    def stored_info_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storedInfoTypeId"))

    @stored_info_type_id.setter
    def stored_info_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccec234485579b1690d8856da8c06ff4e15f46d0e7c61eee3cb43bf6e3121ba2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storedInfoTypeId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeConfig",
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
class DataLossPreventionStoredInfoTypeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dictionary: typing.Optional[typing.Union["DataLossPreventionStoredInfoTypeDictionary", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        large_custom_dictionary: typing.Optional[typing.Union["DataLossPreventionStoredInfoTypeLargeCustomDictionary", typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[typing.Union["DataLossPreventionStoredInfoTypeRegex", typing.Dict[builtins.str, typing.Any]]] = None,
        stored_info_type_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataLossPreventionStoredInfoTypeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param parent: The parent of the info type in any of the following formats:. - 'projects/{{project}}' - 'projects/{{project}}/locations/{{location}}' - 'organizations/{{organization_id}}' - 'organizations/{{organization_id}}/locations/{{location}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#parent DataLossPreventionStoredInfoType#parent}
        :param description: A description of the info type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#description DataLossPreventionStoredInfoType#description}
        :param dictionary: dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#dictionary DataLossPreventionStoredInfoType#dictionary}
        :param display_name: User set display name of the info type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#display_name DataLossPreventionStoredInfoType#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#id DataLossPreventionStoredInfoType#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param large_custom_dictionary: large_custom_dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#large_custom_dictionary DataLossPreventionStoredInfoType#large_custom_dictionary}
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#regex DataLossPreventionStoredInfoType#regex}
        :param stored_info_type_id: The storedInfoType ID can contain uppercase and lowercase letters, numbers, and hyphens; that is, it must match the regular expression: [a-zA-Z\\d-_]+. The maximum length is 100 characters. Can be empty to allow the system to generate one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#stored_info_type_id DataLossPreventionStoredInfoType#stored_info_type_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#timeouts DataLossPreventionStoredInfoType#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(dictionary, dict):
            dictionary = DataLossPreventionStoredInfoTypeDictionary(**dictionary)
        if isinstance(large_custom_dictionary, dict):
            large_custom_dictionary = DataLossPreventionStoredInfoTypeLargeCustomDictionary(**large_custom_dictionary)
        if isinstance(regex, dict):
            regex = DataLossPreventionStoredInfoTypeRegex(**regex)
        if isinstance(timeouts, dict):
            timeouts = DataLossPreventionStoredInfoTypeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddabfab8160f5fd0b60f703253f30676b284358205f07c9ab8c19b6f18908681)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#parent DataLossPreventionStoredInfoType#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the info type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#description DataLossPreventionStoredInfoType#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dictionary(
        self,
    ) -> typing.Optional["DataLossPreventionStoredInfoTypeDictionary"]:
        '''dictionary block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#dictionary DataLossPreventionStoredInfoType#dictionary}
        '''
        result = self._values.get("dictionary")
        return typing.cast(typing.Optional["DataLossPreventionStoredInfoTypeDictionary"], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User set display name of the info type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#display_name DataLossPreventionStoredInfoType#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#id DataLossPreventionStoredInfoType#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def large_custom_dictionary(
        self,
    ) -> typing.Optional["DataLossPreventionStoredInfoTypeLargeCustomDictionary"]:
        '''large_custom_dictionary block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#large_custom_dictionary DataLossPreventionStoredInfoType#large_custom_dictionary}
        '''
        result = self._values.get("large_custom_dictionary")
        return typing.cast(typing.Optional["DataLossPreventionStoredInfoTypeLargeCustomDictionary"], result)

    @builtins.property
    def regex(self) -> typing.Optional["DataLossPreventionStoredInfoTypeRegex"]:
        '''regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#regex DataLossPreventionStoredInfoType#regex}
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional["DataLossPreventionStoredInfoTypeRegex"], result)

    @builtins.property
    def stored_info_type_id(self) -> typing.Optional[builtins.str]:
        '''The storedInfoType ID can contain uppercase and lowercase letters, numbers, and hyphens;

        that is, it must match the regular expression: [a-zA-Z\\d-_]+. The maximum length is 100
        characters. Can be empty to allow the system to generate one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#stored_info_type_id DataLossPreventionStoredInfoType#stored_info_type_id}
        '''
        result = self._values.get("stored_info_type_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataLossPreventionStoredInfoTypeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#timeouts DataLossPreventionStoredInfoType#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataLossPreventionStoredInfoTypeTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionStoredInfoTypeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeDictionary",
    jsii_struct_bases=[],
    name_mapping={"cloud_storage_path": "cloudStoragePath", "word_list": "wordList"},
)
class DataLossPreventionStoredInfoTypeDictionary:
    def __init__(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union["DataLossPreventionStoredInfoTypeDictionaryCloudStoragePath", typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union["DataLossPreventionStoredInfoTypeDictionaryWordListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#cloud_storage_path DataLossPreventionStoredInfoType#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#word_list DataLossPreventionStoredInfoType#word_list}
        '''
        if isinstance(cloud_storage_path, dict):
            cloud_storage_path = DataLossPreventionStoredInfoTypeDictionaryCloudStoragePath(**cloud_storage_path)
        if isinstance(word_list, dict):
            word_list = DataLossPreventionStoredInfoTypeDictionaryWordListStruct(**word_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca889ea46fd892b2a0ae5e73d226c7b1b53bb5d89b7590fd41922419c3cc9e54)
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
    ) -> typing.Optional["DataLossPreventionStoredInfoTypeDictionaryCloudStoragePath"]:
        '''cloud_storage_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#cloud_storage_path DataLossPreventionStoredInfoType#cloud_storage_path}
        '''
        result = self._values.get("cloud_storage_path")
        return typing.cast(typing.Optional["DataLossPreventionStoredInfoTypeDictionaryCloudStoragePath"], result)

    @builtins.property
    def word_list(
        self,
    ) -> typing.Optional["DataLossPreventionStoredInfoTypeDictionaryWordListStruct"]:
        '''word_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#word_list DataLossPreventionStoredInfoType#word_list}
        '''
        result = self._values.get("word_list")
        return typing.cast(typing.Optional["DataLossPreventionStoredInfoTypeDictionaryWordListStruct"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionStoredInfoTypeDictionary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeDictionaryCloudStoragePath",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class DataLossPreventionStoredInfoTypeDictionaryCloudStoragePath:
    def __init__(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#path DataLossPreventionStoredInfoType#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da803f983d8596bec08027631d687a64ca5d7ea6f8103e46032e0b9127d5954f)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#path DataLossPreventionStoredInfoType#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionStoredInfoTypeDictionaryCloudStoragePath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionStoredInfoTypeDictionaryCloudStoragePathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeDictionaryCloudStoragePathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc888f0f7607f541e7b5c9595a02137ab62b4290454b04c4dc74fce84c626ee0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a335ee9be24aa811cfcdeeafc721b28d439d838ae4d04b8dce97416f77e5c17d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionStoredInfoTypeDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[DataLossPreventionStoredInfoTypeDictionaryCloudStoragePath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionStoredInfoTypeDictionaryCloudStoragePath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3358df03b4e89cac0004a55dd8cf6cf056a2fd9d1c5742027d25f87ca25b77af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionStoredInfoTypeDictionaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeDictionaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__366fae9b875ff33e29e680e0dae5fba0beec20bdd66c5434111420c139ef168f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudStoragePath")
    def put_cloud_storage_path(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#path DataLossPreventionStoredInfoType#path}
        '''
        value = DataLossPreventionStoredInfoTypeDictionaryCloudStoragePath(path=path)

        return typing.cast(None, jsii.invoke(self, "putCloudStoragePath", [value]))

    @jsii.member(jsii_name="putWordList")
    def put_word_list(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#words DataLossPreventionStoredInfoType#words}
        '''
        value = DataLossPreventionStoredInfoTypeDictionaryWordListStruct(words=words)

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
    ) -> DataLossPreventionStoredInfoTypeDictionaryCloudStoragePathOutputReference:
        return typing.cast(DataLossPreventionStoredInfoTypeDictionaryCloudStoragePathOutputReference, jsii.get(self, "cloudStoragePath"))

    @builtins.property
    @jsii.member(jsii_name="wordList")
    def word_list(
        self,
    ) -> "DataLossPreventionStoredInfoTypeDictionaryWordListStructOutputReference":
        return typing.cast("DataLossPreventionStoredInfoTypeDictionaryWordListStructOutputReference", jsii.get(self, "wordList"))

    @builtins.property
    @jsii.member(jsii_name="cloudStoragePathInput")
    def cloud_storage_path_input(
        self,
    ) -> typing.Optional[DataLossPreventionStoredInfoTypeDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[DataLossPreventionStoredInfoTypeDictionaryCloudStoragePath], jsii.get(self, "cloudStoragePathInput"))

    @builtins.property
    @jsii.member(jsii_name="wordListInput")
    def word_list_input(
        self,
    ) -> typing.Optional["DataLossPreventionStoredInfoTypeDictionaryWordListStruct"]:
        return typing.cast(typing.Optional["DataLossPreventionStoredInfoTypeDictionaryWordListStruct"], jsii.get(self, "wordListInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionStoredInfoTypeDictionary]:
        return typing.cast(typing.Optional[DataLossPreventionStoredInfoTypeDictionary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionStoredInfoTypeDictionary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c280bd1757fc63f0a16dcd98ce6bb59eeb045f7a718e528a0fd462bf4b294b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeDictionaryWordListStruct",
    jsii_struct_bases=[],
    name_mapping={"words": "words"},
)
class DataLossPreventionStoredInfoTypeDictionaryWordListStruct:
    def __init__(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#words DataLossPreventionStoredInfoType#words}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba7af5e377c75171d638e084c97ed74dc3247cca911dfcbd47ff50cf989fff32)
            check_type(argname="argument words", value=words, expected_type=type_hints["words"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "words": words,
        }

    @builtins.property
    def words(self) -> typing.List[builtins.str]:
        '''Words or phrases defining the dictionary.

        The dictionary must contain at least one
        phrase and every phrase must contain at least 2 characters that are letters or digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#words DataLossPreventionStoredInfoType#words}
        '''
        result = self._values.get("words")
        assert result is not None, "Required property 'words' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionStoredInfoTypeDictionaryWordListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionStoredInfoTypeDictionaryWordListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeDictionaryWordListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74056f8f87e2b22d7a8ce7060eab8277ac2bc637f4bb3194cc986c2d4248854d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__000b72c4dde2ec4212cccefb77ecef6b2159304d8bcb4a58e2043ea0a573597d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "words", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionStoredInfoTypeDictionaryWordListStruct]:
        return typing.cast(typing.Optional[DataLossPreventionStoredInfoTypeDictionaryWordListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionStoredInfoTypeDictionaryWordListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3ad6ff933a80c3f2960f69ea41c9e81b588861b5a4a030c3b2cb40498aca32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeLargeCustomDictionary",
    jsii_struct_bases=[],
    name_mapping={
        "output_path": "outputPath",
        "big_query_field": "bigQueryField",
        "cloud_storage_file_set": "cloudStorageFileSet",
    },
)
class DataLossPreventionStoredInfoTypeLargeCustomDictionary:
    def __init__(
        self,
        *,
        output_path: typing.Union["DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath", typing.Dict[builtins.str, typing.Any]],
        big_query_field: typing.Optional[typing.Union["DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_storage_file_set: typing.Optional[typing.Union["DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param output_path: output_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#output_path DataLossPreventionStoredInfoType#output_path}
        :param big_query_field: big_query_field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#big_query_field DataLossPreventionStoredInfoType#big_query_field}
        :param cloud_storage_file_set: cloud_storage_file_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#cloud_storage_file_set DataLossPreventionStoredInfoType#cloud_storage_file_set}
        '''
        if isinstance(output_path, dict):
            output_path = DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath(**output_path)
        if isinstance(big_query_field, dict):
            big_query_field = DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField(**big_query_field)
        if isinstance(cloud_storage_file_set, dict):
            cloud_storage_file_set = DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet(**cloud_storage_file_set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7f7b60022eb91dca1c3db2bb938dd1f1bc3ffeaf37427891c67f6b3a5e22416)
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
    ) -> "DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath":
        '''output_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#output_path DataLossPreventionStoredInfoType#output_path}
        '''
        result = self._values.get("output_path")
        assert result is not None, "Required property 'output_path' is missing"
        return typing.cast("DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath", result)

    @builtins.property
    def big_query_field(
        self,
    ) -> typing.Optional["DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField"]:
        '''big_query_field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#big_query_field DataLossPreventionStoredInfoType#big_query_field}
        '''
        result = self._values.get("big_query_field")
        return typing.cast(typing.Optional["DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField"], result)

    @builtins.property
    def cloud_storage_file_set(
        self,
    ) -> typing.Optional["DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet"]:
        '''cloud_storage_file_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#cloud_storage_file_set DataLossPreventionStoredInfoType#cloud_storage_file_set}
        '''
        result = self._values.get("cloud_storage_file_set")
        return typing.cast(typing.Optional["DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionStoredInfoTypeLargeCustomDictionary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField",
    jsii_struct_bases=[],
    name_mapping={"field": "field", "table": "table"},
)
class DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField:
    def __init__(
        self,
        *,
        field: typing.Union["DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField", typing.Dict[builtins.str, typing.Any]],
        table: typing.Union["DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param field: field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#field DataLossPreventionStoredInfoType#field}
        :param table: table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#table DataLossPreventionStoredInfoType#table}
        '''
        if isinstance(field, dict):
            field = DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField(**field)
        if isinstance(table, dict):
            table = DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable(**table)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1546dcbf1319ba2d3ccac68f2467a7994035ef9c1b4c0819e87fa94a79bf346)
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "field": field,
            "table": table,
        }

    @builtins.property
    def field(
        self,
    ) -> "DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField":
        '''field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#field DataLossPreventionStoredInfoType#field}
        '''
        result = self._values.get("field")
        assert result is not None, "Required property 'field' is missing"
        return typing.cast("DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField", result)

    @builtins.property
    def table(
        self,
    ) -> "DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable":
        '''table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#table DataLossPreventionStoredInfoType#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast("DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Name describing the field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#name DataLossPreventionStoredInfoType#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6958afe96d7288d0cb47d896a6627c33ebeb52116c587690911a6b6574e0762e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name describing the field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#name DataLossPreventionStoredInfoType#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c58abad801a09a13b1a123e060bca4e81668452f96b38cab64dd4b7eb7a0f590)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3019d332b4eeec1796b274596664be0fcdafcddc59cbcf5ebf2e7287dd59bab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField]:
        return typing.cast(typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e37cbbaa553245148278ee5d80a71cbe07b1d7e1733877b0cb248c5078823a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09d7cc37901ee36bd5a57681569ea12dd1626390ff68ce5e28b2264b36d16c7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putField")
    def put_field(self, *, name: builtins.str) -> None:
        '''
        :param name: Name describing the field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#name DataLossPreventionStoredInfoType#name}
        '''
        value = DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField(
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
        :param dataset_id: The dataset ID of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#dataset_id DataLossPreventionStoredInfoType#dataset_id}
        :param project_id: The Google Cloud Platform project ID of the project containing the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#project_id DataLossPreventionStoredInfoType#project_id}
        :param table_id: The name of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#table_id DataLossPreventionStoredInfoType#table_id}
        '''
        value = DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable(
            dataset_id=dataset_id, project_id=project_id, table_id=table_id
        )

        return typing.cast(None, jsii.invoke(self, "putTable", [value]))

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(
        self,
    ) -> DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldFieldOutputReference:
        return typing.cast(DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldFieldOutputReference, jsii.get(self, "field"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(
        self,
    ) -> "DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTableOutputReference":
        return typing.cast("DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTableOutputReference", jsii.get(self, "table"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(
        self,
    ) -> typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField]:
        return typing.cast(typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(
        self,
    ) -> typing.Optional["DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable"]:
        return typing.cast(typing.Optional["DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable"], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField]:
        return typing.cast(typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f527d92dc61e44904b09da132eccdc105c1e884a2a472693a61f10d0b6c9536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id": "datasetId",
        "project_id": "projectId",
        "table_id": "tableId",
    },
)
class DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable:
    def __init__(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The dataset ID of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#dataset_id DataLossPreventionStoredInfoType#dataset_id}
        :param project_id: The Google Cloud Platform project ID of the project containing the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#project_id DataLossPreventionStoredInfoType#project_id}
        :param table_id: The name of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#table_id DataLossPreventionStoredInfoType#table_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__491c06445fa47b2a67a96eb3ba3254c743a03b5a7c7b43beb65dadc07195f773)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#dataset_id DataLossPreventionStoredInfoType#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The Google Cloud Platform project ID of the project containing the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#project_id DataLossPreventionStoredInfoType#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_id(self) -> builtins.str:
        '''The name of the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#table_id DataLossPreventionStoredInfoType#table_id}
        '''
        result = self._values.get("table_id")
        assert result is not None, "Required property 'table_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__468b4273d9f8083480bda57ac37adedc43306f3bb3f6633eb04eead42affdb6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c1eadc04acd02ea70c183943e47f3db660777fea61e3ea226f4d2593261b2f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8a59bde8b3757a845e1bbf1e9db28307827e77e2e81f8eb8b55609140c0c9a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ef41f59675132c3bfe84b786cfd05788607b98d27ed14020c851f07377ee16c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable]:
        return typing.cast(typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944f9f8e5dc045e47d36c94a950b4785c2767a9991beca1ce3ea1c7287074e06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet",
    jsii_struct_bases=[],
    name_mapping={"url": "url"},
)
class DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet:
    def __init__(self, *, url: builtins.str) -> None:
        '''
        :param url: The url, in the format 'gs:///'. Trailing wildcard in the path is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#url DataLossPreventionStoredInfoType#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04b719398cad2e7485295add028e2edb4d84fe01bb0d56accd77f025edc33be6)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }

    @builtins.property
    def url(self) -> builtins.str:
        '''The url, in the format 'gs:///'. Trailing wildcard in the path is allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#url DataLossPreventionStoredInfoType#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f051c8773134beae820f95c60c3941fd50388e23cbf9db463a0daeafdf92536)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90c20bd4088e15a01e01eb64b544ad4e5d61d6acda7f91445ad267940e5a2112)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet]:
        return typing.cast(typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0ccef7aa525b5323ace8014c6ece3412dcb76853b7092f07a459d890902cdfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath:
    def __init__(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#path DataLossPreventionStoredInfoType#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__068da0c73b59048639726840c1884bad4e5b36412109ba8e0c0e5cad0e7a3bee)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#path DataLossPreventionStoredInfoType#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af6e45224cd921ac4740a070da77689b3ee3eb0ecd4fcc819c29107b60559d5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1258c0cf569decd257d4be76583cc0b17cbc16abe8fdb6f5b9a4d63cbcb11d8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath]:
        return typing.cast(typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__160edd19d9b4638ecf3e13a2e617eb34dafe8734c8d5ef01c752985696909e32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b692019594e576e4e174646f7550c45ed142f6aa043e9aa82cbc46c68c87e0a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBigQueryField")
    def put_big_query_field(
        self,
        *,
        field: typing.Union[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField, typing.Dict[builtins.str, typing.Any]],
        table: typing.Union[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param field: field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#field DataLossPreventionStoredInfoType#field}
        :param table: table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#table DataLossPreventionStoredInfoType#table}
        '''
        value = DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField(
            field=field, table=table
        )

        return typing.cast(None, jsii.invoke(self, "putBigQueryField", [value]))

    @jsii.member(jsii_name="putCloudStorageFileSet")
    def put_cloud_storage_file_set(self, *, url: builtins.str) -> None:
        '''
        :param url: The url, in the format 'gs:///'. Trailing wildcard in the path is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#url DataLossPreventionStoredInfoType#url}
        '''
        value = DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet(
            url=url
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStorageFileSet", [value]))

    @jsii.member(jsii_name="putOutputPath")
    def put_output_path(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#path DataLossPreventionStoredInfoType#path}
        '''
        value = DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath(
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
    ) -> DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldOutputReference:
        return typing.cast(DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldOutputReference, jsii.get(self, "bigQueryField"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageFileSet")
    def cloud_storage_file_set(
        self,
    ) -> DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSetOutputReference:
        return typing.cast(DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSetOutputReference, jsii.get(self, "cloudStorageFileSet"))

    @builtins.property
    @jsii.member(jsii_name="outputPath")
    def output_path(
        self,
    ) -> DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPathOutputReference:
        return typing.cast(DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPathOutputReference, jsii.get(self, "outputPath"))

    @builtins.property
    @jsii.member(jsii_name="bigQueryFieldInput")
    def big_query_field_input(
        self,
    ) -> typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField]:
        return typing.cast(typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField], jsii.get(self, "bigQueryFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageFileSetInput")
    def cloud_storage_file_set_input(
        self,
    ) -> typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet]:
        return typing.cast(typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet], jsii.get(self, "cloudStorageFileSetInput"))

    @builtins.property
    @jsii.member(jsii_name="outputPathInput")
    def output_path_input(
        self,
    ) -> typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath]:
        return typing.cast(typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath], jsii.get(self, "outputPathInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionary]:
        return typing.cast(typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__057fe394e88bd8532ba2e8b164796f19d5f3366f99cbb7668ee8a8a2a995139b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeRegex",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern", "group_indexes": "groupIndexes"},
)
class DataLossPreventionStoredInfoTypeRegex:
    def __init__(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#pattern DataLossPreventionStoredInfoType#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#group_indexes DataLossPreventionStoredInfoType#group_indexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a01340775700520dc88978b6a5a0f28159cfc65ee880578180f1509b2b3ce17b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#pattern DataLossPreventionStoredInfoType#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_indexes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The index of the submatch to extract as findings.

        When not specified, the entire match is returned. No more than 3 may be included.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#group_indexes DataLossPreventionStoredInfoType#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionStoredInfoTypeRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionStoredInfoTypeRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10027b7259afe5dcd00947b25f3a42d608c82fa1b73f16a4af3d12de2b69d5b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2932700a6f9de3804103681defecc89aea373b32c1c3a7cf8f5246555d36ade9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a7fd5a37eb80cacbe0a761201ea3dcef21edfc8543c266e75100733ea661360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataLossPreventionStoredInfoTypeRegex]:
        return typing.cast(typing.Optional[DataLossPreventionStoredInfoTypeRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionStoredInfoTypeRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b31746a42bcec1486982696bee09817ad0668306c571b56dc67242c9080715c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataLossPreventionStoredInfoTypeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#create DataLossPreventionStoredInfoType#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#delete DataLossPreventionStoredInfoType#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#update DataLossPreventionStoredInfoType#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c380080470cb3ceb8978de4040204dc883e8ca4da995d91516c305e9724cf626)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#create DataLossPreventionStoredInfoType#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#delete DataLossPreventionStoredInfoType#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_stored_info_type#update DataLossPreventionStoredInfoType#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionStoredInfoTypeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionStoredInfoTypeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionStoredInfoType.DataLossPreventionStoredInfoTypeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7acfa6b5b1ce7c9f3926e4b748687b91cf82160a46ddaf03f6fd11561eaab894)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02a51fc9cd89d099178fc7bfc08e4c9c3c6f011f78f1865f5ac369e3a976b50e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f9e5d4aab83a8031f4e2e8d4df13afce2034f81d58e787230ccf1f4de96d1bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e562e0784b2cf47d38201854d73ec1350ce838792a945ccbcc138ee391bc82a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionStoredInfoTypeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionStoredInfoTypeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionStoredInfoTypeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5279318c7a6455f75e63a84eea240acf5f80c5413957490888bfd4edf4f81faf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataLossPreventionStoredInfoType",
    "DataLossPreventionStoredInfoTypeConfig",
    "DataLossPreventionStoredInfoTypeDictionary",
    "DataLossPreventionStoredInfoTypeDictionaryCloudStoragePath",
    "DataLossPreventionStoredInfoTypeDictionaryCloudStoragePathOutputReference",
    "DataLossPreventionStoredInfoTypeDictionaryOutputReference",
    "DataLossPreventionStoredInfoTypeDictionaryWordListStruct",
    "DataLossPreventionStoredInfoTypeDictionaryWordListStructOutputReference",
    "DataLossPreventionStoredInfoTypeLargeCustomDictionary",
    "DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField",
    "DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField",
    "DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldFieldOutputReference",
    "DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldOutputReference",
    "DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable",
    "DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTableOutputReference",
    "DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet",
    "DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSetOutputReference",
    "DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath",
    "DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPathOutputReference",
    "DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputReference",
    "DataLossPreventionStoredInfoTypeRegex",
    "DataLossPreventionStoredInfoTypeRegexOutputReference",
    "DataLossPreventionStoredInfoTypeTimeouts",
    "DataLossPreventionStoredInfoTypeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__63fdff0bb027af40fa63b283eab87993180cd1cf6f0d71b6338e8b8508decd89(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    parent: builtins.str,
    description: typing.Optional[builtins.str] = None,
    dictionary: typing.Optional[typing.Union[DataLossPreventionStoredInfoTypeDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    large_custom_dictionary: typing.Optional[typing.Union[DataLossPreventionStoredInfoTypeLargeCustomDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
    regex: typing.Optional[typing.Union[DataLossPreventionStoredInfoTypeRegex, typing.Dict[builtins.str, typing.Any]]] = None,
    stored_info_type_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataLossPreventionStoredInfoTypeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a3fa4a9d54c99cd018aae29934a827c855747678c25fcaaf52081dcb4c845198(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1efcbd39945dac0f8250626e5a0c6c1ef0c88a17a4bc6d6bf2f25bf79694af53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__196aae1aa59be61de3a898d32ec3d71cfc7b7a71273796eddc53fb6abb64876c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac9eaf458d1de32fb87f648541299258be3a542b8c830bdc837126de6b096d44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0060f6a5e375b77739d721d72ec7f8ac32866ff62861885e56d680adaee43247(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccec234485579b1690d8856da8c06ff4e15f46d0e7c61eee3cb43bf6e3121ba2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddabfab8160f5fd0b60f703253f30676b284358205f07c9ab8c19b6f18908681(
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
    dictionary: typing.Optional[typing.Union[DataLossPreventionStoredInfoTypeDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    large_custom_dictionary: typing.Optional[typing.Union[DataLossPreventionStoredInfoTypeLargeCustomDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
    regex: typing.Optional[typing.Union[DataLossPreventionStoredInfoTypeRegex, typing.Dict[builtins.str, typing.Any]]] = None,
    stored_info_type_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataLossPreventionStoredInfoTypeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca889ea46fd892b2a0ae5e73d226c7b1b53bb5d89b7590fd41922419c3cc9e54(
    *,
    cloud_storage_path: typing.Optional[typing.Union[DataLossPreventionStoredInfoTypeDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
    word_list: typing.Optional[typing.Union[DataLossPreventionStoredInfoTypeDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da803f983d8596bec08027631d687a64ca5d7ea6f8103e46032e0b9127d5954f(
    *,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc888f0f7607f541e7b5c9595a02137ab62b4290454b04c4dc74fce84c626ee0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a335ee9be24aa811cfcdeeafc721b28d439d838ae4d04b8dce97416f77e5c17d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3358df03b4e89cac0004a55dd8cf6cf056a2fd9d1c5742027d25f87ca25b77af(
    value: typing.Optional[DataLossPreventionStoredInfoTypeDictionaryCloudStoragePath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__366fae9b875ff33e29e680e0dae5fba0beec20bdd66c5434111420c139ef168f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c280bd1757fc63f0a16dcd98ce6bb59eeb045f7a718e528a0fd462bf4b294b1(
    value: typing.Optional[DataLossPreventionStoredInfoTypeDictionary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7af5e377c75171d638e084c97ed74dc3247cca911dfcbd47ff50cf989fff32(
    *,
    words: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74056f8f87e2b22d7a8ce7060eab8277ac2bc637f4bb3194cc986c2d4248854d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000b72c4dde2ec4212cccefb77ecef6b2159304d8bcb4a58e2043ea0a573597d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3ad6ff933a80c3f2960f69ea41c9e81b588861b5a4a030c3b2cb40498aca32(
    value: typing.Optional[DataLossPreventionStoredInfoTypeDictionaryWordListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f7b60022eb91dca1c3db2bb938dd1f1bc3ffeaf37427891c67f6b3a5e22416(
    *,
    output_path: typing.Union[DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath, typing.Dict[builtins.str, typing.Any]],
    big_query_field: typing.Optional[typing.Union[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_storage_file_set: typing.Optional[typing.Union[DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1546dcbf1319ba2d3ccac68f2467a7994035ef9c1b4c0819e87fa94a79bf346(
    *,
    field: typing.Union[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField, typing.Dict[builtins.str, typing.Any]],
    table: typing.Union[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6958afe96d7288d0cb47d896a6627c33ebeb52116c587690911a6b6574e0762e(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58abad801a09a13b1a123e060bca4e81668452f96b38cab64dd4b7eb7a0f590(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3019d332b4eeec1796b274596664be0fcdafcddc59cbcf5ebf2e7287dd59bab2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e37cbbaa553245148278ee5d80a71cbe07b1d7e1733877b0cb248c5078823a1(
    value: typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldField],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d7cc37901ee36bd5a57681569ea12dd1626390ff68ce5e28b2264b36d16c7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f527d92dc61e44904b09da132eccdc105c1e884a2a472693a61f10d0b6c9536(
    value: typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryField],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491c06445fa47b2a67a96eb3ba3254c743a03b5a7c7b43beb65dadc07195f773(
    *,
    dataset_id: builtins.str,
    project_id: builtins.str,
    table_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468b4273d9f8083480bda57ac37adedc43306f3bb3f6633eb04eead42affdb6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1eadc04acd02ea70c183943e47f3db660777fea61e3ea226f4d2593261b2f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a59bde8b3757a845e1bbf1e9db28307827e77e2e81f8eb8b55609140c0c9a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef41f59675132c3bfe84b786cfd05788607b98d27ed14020c851f07377ee16c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944f9f8e5dc045e47d36c94a950b4785c2767a9991beca1ce3ea1c7287074e06(
    value: typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryBigQueryFieldTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b719398cad2e7485295add028e2edb4d84fe01bb0d56accd77f025edc33be6(
    *,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f051c8773134beae820f95c60c3941fd50388e23cbf9db463a0daeafdf92536(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c20bd4088e15a01e01eb64b544ad4e5d61d6acda7f91445ad267940e5a2112(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ccef7aa525b5323ace8014c6ece3412dcb76853b7092f07a459d890902cdfe(
    value: typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryCloudStorageFileSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068da0c73b59048639726840c1884bad4e5b36412109ba8e0c0e5cad0e7a3bee(
    *,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af6e45224cd921ac4740a070da77689b3ee3eb0ecd4fcc819c29107b60559d5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1258c0cf569decd257d4be76583cc0b17cbc16abe8fdb6f5b9a4d63cbcb11d8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160edd19d9b4638ecf3e13a2e617eb34dafe8734c8d5ef01c752985696909e32(
    value: typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionaryOutputPath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b692019594e576e4e174646f7550c45ed142f6aa043e9aa82cbc46c68c87e0a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057fe394e88bd8532ba2e8b164796f19d5f3366f99cbb7668ee8a8a2a995139b(
    value: typing.Optional[DataLossPreventionStoredInfoTypeLargeCustomDictionary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01340775700520dc88978b6a5a0f28159cfc65ee880578180f1509b2b3ce17b(
    *,
    pattern: builtins.str,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10027b7259afe5dcd00947b25f3a42d608c82fa1b73f16a4af3d12de2b69d5b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2932700a6f9de3804103681defecc89aea373b32c1c3a7cf8f5246555d36ade9(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7fd5a37eb80cacbe0a761201ea3dcef21edfc8543c266e75100733ea661360(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31746a42bcec1486982696bee09817ad0668306c571b56dc67242c9080715c9(
    value: typing.Optional[DataLossPreventionStoredInfoTypeRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c380080470cb3ceb8978de4040204dc883e8ca4da995d91516c305e9724cf626(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7acfa6b5b1ce7c9f3926e4b748687b91cf82160a46ddaf03f6fd11561eaab894(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a51fc9cd89d099178fc7bfc08e4c9c3c6f011f78f1865f5ac369e3a976b50e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9e5d4aab83a8031f4e2e8d4df13afce2034f81d58e787230ccf1f4de96d1bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e562e0784b2cf47d38201854d73ec1350ce838792a945ccbcc138ee391bc82a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5279318c7a6455f75e63a84eea240acf5f80c5413957490888bfd4edf4f81faf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionStoredInfoTypeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

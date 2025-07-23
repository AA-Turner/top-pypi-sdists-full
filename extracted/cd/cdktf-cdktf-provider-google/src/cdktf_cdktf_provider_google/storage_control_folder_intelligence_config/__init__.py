r'''
# `google_storage_control_folder_intelligence_config`

Refer to the Terraform Registry for docs: [`google_storage_control_folder_intelligence_config`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config).
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


class StorageControlFolderIntelligenceConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config google_storage_control_folder_intelligence_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        edition_config: typing.Optional[builtins.str] = None,
        filter: typing.Optional[typing.Union["StorageControlFolderIntelligenceConfigFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["StorageControlFolderIntelligenceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config google_storage_control_folder_intelligence_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Identifier of the GCP Folder. For GCP Folder, this field can be folder number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#name StorageControlFolderIntelligenceConfig#name}
        :param edition_config: Edition configuration of the Storage Intelligence resource. Valid values are INHERIT, TRIAL, DISABLED and STANDARD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#edition_config StorageControlFolderIntelligenceConfig#edition_config}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#filter StorageControlFolderIntelligenceConfig#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#id StorageControlFolderIntelligenceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#timeouts StorageControlFolderIntelligenceConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e83c20f04f6a6af2a7ff70dfa922838d0c8ccb258a589fcd5fb9f06e46ad283)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StorageControlFolderIntelligenceConfigConfig(
            name=name,
            edition_config=edition_config,
            filter=filter,
            id=id,
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
        '''Generates CDKTF code for importing a StorageControlFolderIntelligenceConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StorageControlFolderIntelligenceConfig to import.
        :param import_from_id: The id of the existing StorageControlFolderIntelligenceConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StorageControlFolderIntelligenceConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f38c7060dca1e974f4160d898c6b5776825647dfd2f4f9978cbf5c8e637088)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        *,
        excluded_cloud_storage_buckets: typing.Optional[typing.Union["StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        excluded_cloud_storage_locations: typing.Optional[typing.Union["StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_buckets: typing.Optional[typing.Union["StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_locations: typing.Optional[typing.Union["StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excluded_cloud_storage_buckets: excluded_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#excluded_cloud_storage_buckets StorageControlFolderIntelligenceConfig#excluded_cloud_storage_buckets}
        :param excluded_cloud_storage_locations: excluded_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#excluded_cloud_storage_locations StorageControlFolderIntelligenceConfig#excluded_cloud_storage_locations}
        :param included_cloud_storage_buckets: included_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#included_cloud_storage_buckets StorageControlFolderIntelligenceConfig#included_cloud_storage_buckets}
        :param included_cloud_storage_locations: included_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#included_cloud_storage_locations StorageControlFolderIntelligenceConfig#included_cloud_storage_locations}
        '''
        value = StorageControlFolderIntelligenceConfigFilter(
            excluded_cloud_storage_buckets=excluded_cloud_storage_buckets,
            excluded_cloud_storage_locations=excluded_cloud_storage_locations,
            included_cloud_storage_buckets=included_cloud_storage_buckets,
            included_cloud_storage_locations=included_cloud_storage_locations,
        )

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#create StorageControlFolderIntelligenceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#delete StorageControlFolderIntelligenceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#update StorageControlFolderIntelligenceConfig#update}.
        '''
        value = StorageControlFolderIntelligenceConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetEditionConfig")
    def reset_edition_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEditionConfig", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="effectiveIntelligenceConfig")
    def effective_intelligence_config(
        self,
    ) -> "StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfigList":
        return typing.cast("StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfigList", jsii.get(self, "effectiveIntelligenceConfig"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> "StorageControlFolderIntelligenceConfigFilterOutputReference":
        return typing.cast("StorageControlFolderIntelligenceConfigFilterOutputReference", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "StorageControlFolderIntelligenceConfigTimeoutsOutputReference":
        return typing.cast("StorageControlFolderIntelligenceConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="trialConfig")
    def trial_config(self) -> "StorageControlFolderIntelligenceConfigTrialConfigList":
        return typing.cast("StorageControlFolderIntelligenceConfigTrialConfigList", jsii.get(self, "trialConfig"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="editionConfigInput")
    def edition_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "editionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional["StorageControlFolderIntelligenceConfigFilter"]:
        return typing.cast(typing.Optional["StorageControlFolderIntelligenceConfigFilter"], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageControlFolderIntelligenceConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageControlFolderIntelligenceConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="editionConfig")
    def edition_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "editionConfig"))

    @edition_config.setter
    def edition_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f067a25cbbc21083a37a6716ece681aaad9fdcfc97f3ad13faf62a91dba4e960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "editionConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b0735e93d4c874efcadfaef41cbcdb0498e7483a8c810f089df9268caf15be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d36f504bf378d2533c6af7103dfd5241f56edaf34ac1604464dc051d6d8529a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigConfig",
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
        "edition_config": "editionConfig",
        "filter": "filter",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class StorageControlFolderIntelligenceConfigConfig(
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
        name: builtins.str,
        edition_config: typing.Optional[builtins.str] = None,
        filter: typing.Optional[typing.Union["StorageControlFolderIntelligenceConfigFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["StorageControlFolderIntelligenceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Identifier of the GCP Folder. For GCP Folder, this field can be folder number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#name StorageControlFolderIntelligenceConfig#name}
        :param edition_config: Edition configuration of the Storage Intelligence resource. Valid values are INHERIT, TRIAL, DISABLED and STANDARD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#edition_config StorageControlFolderIntelligenceConfig#edition_config}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#filter StorageControlFolderIntelligenceConfig#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#id StorageControlFolderIntelligenceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#timeouts StorageControlFolderIntelligenceConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(filter, dict):
            filter = StorageControlFolderIntelligenceConfigFilter(**filter)
        if isinstance(timeouts, dict):
            timeouts = StorageControlFolderIntelligenceConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43ec80ae280bbd602a368a1d91173fa95d2c26be86371e79262d854df0d724bf)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument edition_config", value=edition_config, expected_type=type_hints["edition_config"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
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
        if edition_config is not None:
            self._values["edition_config"] = edition_config
        if filter is not None:
            self._values["filter"] = filter
        if id is not None:
            self._values["id"] = id
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
    def name(self) -> builtins.str:
        '''Identifier of the GCP Folder. For GCP Folder, this field can be folder number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#name StorageControlFolderIntelligenceConfig#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def edition_config(self) -> typing.Optional[builtins.str]:
        '''Edition configuration of the Storage Intelligence resource. Valid values are INHERIT, TRIAL, DISABLED and STANDARD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#edition_config StorageControlFolderIntelligenceConfig#edition_config}
        '''
        result = self._values.get("edition_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter(self) -> typing.Optional["StorageControlFolderIntelligenceConfigFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#filter StorageControlFolderIntelligenceConfig#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional["StorageControlFolderIntelligenceConfigFilter"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#id StorageControlFolderIntelligenceConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["StorageControlFolderIntelligenceConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#timeouts StorageControlFolderIntelligenceConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["StorageControlFolderIntelligenceConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlFolderIntelligenceConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d460fad3048cbf6e26f52cac6cb0a19374898e3dd284254f5e86ffaf57a7f7f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__577e1f911297632ee3c36e4c2287e35e831e7404f53e4fa96c09a292c71c0411)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ccfeba8580c00b5291ae22bf341bee30f4ae6f65a271895ca58546ba0d4161)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b96264ddeb9df9da08e3b22b870735598e4a7ce1123baa2a51bd34a3479ba60d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd6b6d21b72e3545ca94aac31c81e2ee0b6a529b7edcdcb5baf50d3ec18bb0dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c22b9b579fe92d2489f43bbfdcbec9c09721866abe9cd6ad026baed644340878)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="effectiveEdition")
    def effective_edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveEdition"))

    @builtins.property
    @jsii.member(jsii_name="intelligenceConfig")
    def intelligence_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intelligenceConfig"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfig]:
        return typing.cast(typing.Optional[StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8501f83b04e4cf55b271b6d392cf15b7556c1f767bdc82fae9ef4229005db28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigFilter",
    jsii_struct_bases=[],
    name_mapping={
        "excluded_cloud_storage_buckets": "excludedCloudStorageBuckets",
        "excluded_cloud_storage_locations": "excludedCloudStorageLocations",
        "included_cloud_storage_buckets": "includedCloudStorageBuckets",
        "included_cloud_storage_locations": "includedCloudStorageLocations",
    },
)
class StorageControlFolderIntelligenceConfigFilter:
    def __init__(
        self,
        *,
        excluded_cloud_storage_buckets: typing.Optional[typing.Union["StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        excluded_cloud_storage_locations: typing.Optional[typing.Union["StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_buckets: typing.Optional[typing.Union["StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_locations: typing.Optional[typing.Union["StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excluded_cloud_storage_buckets: excluded_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#excluded_cloud_storage_buckets StorageControlFolderIntelligenceConfig#excluded_cloud_storage_buckets}
        :param excluded_cloud_storage_locations: excluded_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#excluded_cloud_storage_locations StorageControlFolderIntelligenceConfig#excluded_cloud_storage_locations}
        :param included_cloud_storage_buckets: included_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#included_cloud_storage_buckets StorageControlFolderIntelligenceConfig#included_cloud_storage_buckets}
        :param included_cloud_storage_locations: included_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#included_cloud_storage_locations StorageControlFolderIntelligenceConfig#included_cloud_storage_locations}
        '''
        if isinstance(excluded_cloud_storage_buckets, dict):
            excluded_cloud_storage_buckets = StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBuckets(**excluded_cloud_storage_buckets)
        if isinstance(excluded_cloud_storage_locations, dict):
            excluded_cloud_storage_locations = StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocations(**excluded_cloud_storage_locations)
        if isinstance(included_cloud_storage_buckets, dict):
            included_cloud_storage_buckets = StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBuckets(**included_cloud_storage_buckets)
        if isinstance(included_cloud_storage_locations, dict):
            included_cloud_storage_locations = StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocations(**included_cloud_storage_locations)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0bc80beb5f614595e08007382f3c7ed1852d8a2654eb2b6b61167db2b4ad87f)
            check_type(argname="argument excluded_cloud_storage_buckets", value=excluded_cloud_storage_buckets, expected_type=type_hints["excluded_cloud_storage_buckets"])
            check_type(argname="argument excluded_cloud_storage_locations", value=excluded_cloud_storage_locations, expected_type=type_hints["excluded_cloud_storage_locations"])
            check_type(argname="argument included_cloud_storage_buckets", value=included_cloud_storage_buckets, expected_type=type_hints["included_cloud_storage_buckets"])
            check_type(argname="argument included_cloud_storage_locations", value=included_cloud_storage_locations, expected_type=type_hints["included_cloud_storage_locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excluded_cloud_storage_buckets is not None:
            self._values["excluded_cloud_storage_buckets"] = excluded_cloud_storage_buckets
        if excluded_cloud_storage_locations is not None:
            self._values["excluded_cloud_storage_locations"] = excluded_cloud_storage_locations
        if included_cloud_storage_buckets is not None:
            self._values["included_cloud_storage_buckets"] = included_cloud_storage_buckets
        if included_cloud_storage_locations is not None:
            self._values["included_cloud_storage_locations"] = included_cloud_storage_locations

    @builtins.property
    def excluded_cloud_storage_buckets(
        self,
    ) -> typing.Optional["StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBuckets"]:
        '''excluded_cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#excluded_cloud_storage_buckets StorageControlFolderIntelligenceConfig#excluded_cloud_storage_buckets}
        '''
        result = self._values.get("excluded_cloud_storage_buckets")
        return typing.cast(typing.Optional["StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBuckets"], result)

    @builtins.property
    def excluded_cloud_storage_locations(
        self,
    ) -> typing.Optional["StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocations"]:
        '''excluded_cloud_storage_locations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#excluded_cloud_storage_locations StorageControlFolderIntelligenceConfig#excluded_cloud_storage_locations}
        '''
        result = self._values.get("excluded_cloud_storage_locations")
        return typing.cast(typing.Optional["StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocations"], result)

    @builtins.property
    def included_cloud_storage_buckets(
        self,
    ) -> typing.Optional["StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBuckets"]:
        '''included_cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#included_cloud_storage_buckets StorageControlFolderIntelligenceConfig#included_cloud_storage_buckets}
        '''
        result = self._values.get("included_cloud_storage_buckets")
        return typing.cast(typing.Optional["StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBuckets"], result)

    @builtins.property
    def included_cloud_storage_locations(
        self,
    ) -> typing.Optional["StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocations"]:
        '''included_cloud_storage_locations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#included_cloud_storage_locations StorageControlFolderIntelligenceConfig#included_cloud_storage_locations}
        '''
        result = self._values.get("included_cloud_storage_locations")
        return typing.cast(typing.Optional["StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocations"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlFolderIntelligenceConfigFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={"bucket_id_regexes": "bucketIdRegexes"},
)
class StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBuckets:
    def __init__(self, *, bucket_id_regexes: typing.Sequence[builtins.str]) -> None:
        '''
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#bucket_id_regexes StorageControlFolderIntelligenceConfig#bucket_id_regexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3fc7d83fd1d0d64fa0eb63bdcbda59f2d43e81f78b46f1267b7c4514606c8be)
            check_type(argname="argument bucket_id_regexes", value=bucket_id_regexes, expected_type=type_hints["bucket_id_regexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_id_regexes": bucket_id_regexes,
        }

    @builtins.property
    def bucket_id_regexes(self) -> typing.List[builtins.str]:
        '''List of bucket id regexes to exclude in the storage intelligence plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#bucket_id_regexes StorageControlFolderIntelligenceConfig#bucket_id_regexes}
        '''
        result = self._values.get("bucket_id_regexes")
        assert result is not None, "Required property 'bucket_id_regexes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__673d7422b92ed058350345ceb81bb293bb0552a877339dffe5f7b2a9f2b96e28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="bucketIdRegexesInput")
    def bucket_id_regexes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "bucketIdRegexesInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketIdRegexes")
    def bucket_id_regexes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "bucketIdRegexes"))

    @bucket_id_regexes.setter
    def bucket_id_regexes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd3eeef5a5a2c38fd8d603dad09670f1af0f75c8eb891f1caf98c5f39ffa745e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketIdRegexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b180b123c99c4194a723476b26203314e7c2e4287f8d21638d8f0713ea751d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocations",
    jsii_struct_bases=[],
    name_mapping={"locations": "locations"},
)
class StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocations:
    def __init__(self, *, locations: typing.Sequence[builtins.str]) -> None:
        '''
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#locations StorageControlFolderIntelligenceConfig#locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0f0aeb3d5e1dac41134578fd2306867525c63bd48e8f74a754186b0424b097)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locations": locations,
        }

    @builtins.property
    def locations(self) -> typing.List[builtins.str]:
        '''List of locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#locations StorageControlFolderIntelligenceConfig#locations}
        '''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89718513eb491106f8cc413ffe5a908de0d75e09b93139c92c9a0a4e9493c15d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="locationsInput")
    def locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "locationsInput"))

    @builtins.property
    @jsii.member(jsii_name="locations")
    def locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "locations"))

    @locations.setter
    def locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b6ccbf00e58b19565831cf7dae011b69c9490ad176873aa315e9f5f174847f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocations]:
        return typing.cast(typing.Optional[StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1d470304e2b23eceee8e36a62b5a926c5cc7d5dc400b38580a9c83884faba53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={"bucket_id_regexes": "bucketIdRegexes"},
)
class StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBuckets:
    def __init__(self, *, bucket_id_regexes: typing.Sequence[builtins.str]) -> None:
        '''
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#bucket_id_regexes StorageControlFolderIntelligenceConfig#bucket_id_regexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1c256ac9b39cacca01d39ad2934bfe2367734f2cb0afdc9a5eac475f1276f46)
            check_type(argname="argument bucket_id_regexes", value=bucket_id_regexes, expected_type=type_hints["bucket_id_regexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_id_regexes": bucket_id_regexes,
        }

    @builtins.property
    def bucket_id_regexes(self) -> typing.List[builtins.str]:
        '''List of bucket id regexes to exclude in the storage intelligence plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#bucket_id_regexes StorageControlFolderIntelligenceConfig#bucket_id_regexes}
        '''
        result = self._values.get("bucket_id_regexes")
        assert result is not None, "Required property 'bucket_id_regexes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1e80b770b7e978d4a70507f455be29574a86c4d53b7b7939460a097ef68db7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="bucketIdRegexesInput")
    def bucket_id_regexes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "bucketIdRegexesInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketIdRegexes")
    def bucket_id_regexes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "bucketIdRegexes"))

    @bucket_id_regexes.setter
    def bucket_id_regexes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a5ee3803f095823422756cfdfb5727acebe9d41bf6404ec1ecdea4ddadef7f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketIdRegexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f191e90f40c3a00c57732d6334958a3d2dbb45d44dfd3669f4af1b45ddd0d3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocations",
    jsii_struct_bases=[],
    name_mapping={"locations": "locations"},
)
class StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocations:
    def __init__(self, *, locations: typing.Sequence[builtins.str]) -> None:
        '''
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#locations StorageControlFolderIntelligenceConfig#locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cf4092b5102ba46c5165a62869e35de3e109129ccd70de75b2f4a65f1a00beb)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locations": locations,
        }

    @builtins.property
    def locations(self) -> typing.List[builtins.str]:
        '''List of locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#locations StorageControlFolderIntelligenceConfig#locations}
        '''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af71fa13c52ad73dad7555387111f4cded2d7e338dfa92d8cd72fa1cf53951d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="locationsInput")
    def locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "locationsInput"))

    @builtins.property
    @jsii.member(jsii_name="locations")
    def locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "locations"))

    @locations.setter
    def locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88aad610805b97d50d619aa4f5f712b2d3849b22ee5948d08c2786e40174fe05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocations]:
        return typing.cast(typing.Optional[StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fad1f4d7069ac6b0b76b8b65a7e4c9bbdf8a1e6999cb22f956fef27b1010944)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageControlFolderIntelligenceConfigFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3a5c750bbee5e2d94662b7400453fa9727e112fd89eaf362e3ab080b83a60d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExcludedCloudStorageBuckets")
    def put_excluded_cloud_storage_buckets(
        self,
        *,
        bucket_id_regexes: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#bucket_id_regexes StorageControlFolderIntelligenceConfig#bucket_id_regexes}
        '''
        value = StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBuckets(
            bucket_id_regexes=bucket_id_regexes
        )

        return typing.cast(None, jsii.invoke(self, "putExcludedCloudStorageBuckets", [value]))

    @jsii.member(jsii_name="putExcludedCloudStorageLocations")
    def put_excluded_cloud_storage_locations(
        self,
        *,
        locations: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#locations StorageControlFolderIntelligenceConfig#locations}
        '''
        value = StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocations(
            locations=locations
        )

        return typing.cast(None, jsii.invoke(self, "putExcludedCloudStorageLocations", [value]))

    @jsii.member(jsii_name="putIncludedCloudStorageBuckets")
    def put_included_cloud_storage_buckets(
        self,
        *,
        bucket_id_regexes: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#bucket_id_regexes StorageControlFolderIntelligenceConfig#bucket_id_regexes}
        '''
        value = StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBuckets(
            bucket_id_regexes=bucket_id_regexes
        )

        return typing.cast(None, jsii.invoke(self, "putIncludedCloudStorageBuckets", [value]))

    @jsii.member(jsii_name="putIncludedCloudStorageLocations")
    def put_included_cloud_storage_locations(
        self,
        *,
        locations: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#locations StorageControlFolderIntelligenceConfig#locations}
        '''
        value = StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocations(
            locations=locations
        )

        return typing.cast(None, jsii.invoke(self, "putIncludedCloudStorageLocations", [value]))

    @jsii.member(jsii_name="resetExcludedCloudStorageBuckets")
    def reset_excluded_cloud_storage_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedCloudStorageBuckets", []))

    @jsii.member(jsii_name="resetExcludedCloudStorageLocations")
    def reset_excluded_cloud_storage_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedCloudStorageLocations", []))

    @jsii.member(jsii_name="resetIncludedCloudStorageBuckets")
    def reset_included_cloud_storage_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedCloudStorageBuckets", []))

    @jsii.member(jsii_name="resetIncludedCloudStorageLocations")
    def reset_included_cloud_storage_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedCloudStorageLocations", []))

    @builtins.property
    @jsii.member(jsii_name="excludedCloudStorageBuckets")
    def excluded_cloud_storage_buckets(
        self,
    ) -> StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference:
        return typing.cast(StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference, jsii.get(self, "excludedCloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="excludedCloudStorageLocations")
    def excluded_cloud_storage_locations(
        self,
    ) -> StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference:
        return typing.cast(StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference, jsii.get(self, "excludedCloudStorageLocations"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageBuckets")
    def included_cloud_storage_buckets(
        self,
    ) -> StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference:
        return typing.cast(StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference, jsii.get(self, "includedCloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageLocations")
    def included_cloud_storage_locations(
        self,
    ) -> StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference:
        return typing.cast(StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference, jsii.get(self, "includedCloudStorageLocations"))

    @builtins.property
    @jsii.member(jsii_name="excludedCloudStorageBucketsInput")
    def excluded_cloud_storage_buckets_input(
        self,
    ) -> typing.Optional[StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBuckets], jsii.get(self, "excludedCloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedCloudStorageLocationsInput")
    def excluded_cloud_storage_locations_input(
        self,
    ) -> typing.Optional[StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocations]:
        return typing.cast(typing.Optional[StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocations], jsii.get(self, "excludedCloudStorageLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageBucketsInput")
    def included_cloud_storage_buckets_input(
        self,
    ) -> typing.Optional[StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBuckets], jsii.get(self, "includedCloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageLocationsInput")
    def included_cloud_storage_locations_input(
        self,
    ) -> typing.Optional[StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocations]:
        return typing.cast(typing.Optional[StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocations], jsii.get(self, "includedCloudStorageLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageControlFolderIntelligenceConfigFilter]:
        return typing.cast(typing.Optional[StorageControlFolderIntelligenceConfigFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlFolderIntelligenceConfigFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ee02a7cf6bd16c1a1537aa5424878af3cab880f7b0a4517bbe7d242764340e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class StorageControlFolderIntelligenceConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#create StorageControlFolderIntelligenceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#delete StorageControlFolderIntelligenceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#update StorageControlFolderIntelligenceConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb77ee0cf88160893fbbe991de057c832c514fcfa93f8fbfe59624f00c244df4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#create StorageControlFolderIntelligenceConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#delete StorageControlFolderIntelligenceConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_folder_intelligence_config#update StorageControlFolderIntelligenceConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlFolderIntelligenceConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlFolderIntelligenceConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1e850e872b9904e975c6e484576714adacf355fa82af3e1cc3c3e6c9e47c53d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5e3670e110fd2d1e4468f3afe83db572a6327b96a24fdafec54e0ded7df00eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b01511d759d8f3aff8c51283d72a82b9a250cfb217aea0a73e62cac5818d5fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6878b55587a3889d2c5496acc42299cacde905e527929f764e2c45d4668721c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageControlFolderIntelligenceConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageControlFolderIntelligenceConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageControlFolderIntelligenceConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82eb2c5620dbc9152d2ccaa1fa9f0211b99e24e1da98c2e91959ee150afb0422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigTrialConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class StorageControlFolderIntelligenceConfigTrialConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlFolderIntelligenceConfigTrialConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlFolderIntelligenceConfigTrialConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigTrialConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12d8314900ade3fe80662f20332888d7f938eafe07bb6095761fb85390660cc5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StorageControlFolderIntelligenceConfigTrialConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a426a9c0c4884e2f024bfffe658d77814e3e2df9c0e4f620352c473008107f40)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageControlFolderIntelligenceConfigTrialConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fb5274ef33c6fa54f1b455c43d90a8921352a2f0e0917b9ffead045a0edd65d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49a708528558fcabd768a59076dbc68eaf5443a557b18055a6ecfbc59ef77bdb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fb9da5a505698ceda02dbd5d42acc1d502ca30874d896e0c5575af778ef26ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class StorageControlFolderIntelligenceConfigTrialConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlFolderIntelligenceConfig.StorageControlFolderIntelligenceConfigTrialConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f34f65b2149762c3759d2695e7ec57bbed61b20f469135e0fc7117dcee987863)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="expireTime")
    def expire_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageControlFolderIntelligenceConfigTrialConfig]:
        return typing.cast(typing.Optional[StorageControlFolderIntelligenceConfigTrialConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlFolderIntelligenceConfigTrialConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809dd1382f03758c80168599799d219339745ba41cc53c728e9f6ab998253bbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StorageControlFolderIntelligenceConfig",
    "StorageControlFolderIntelligenceConfigConfig",
    "StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfig",
    "StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfigList",
    "StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfigOutputReference",
    "StorageControlFolderIntelligenceConfigFilter",
    "StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBuckets",
    "StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference",
    "StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocations",
    "StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference",
    "StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBuckets",
    "StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference",
    "StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocations",
    "StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference",
    "StorageControlFolderIntelligenceConfigFilterOutputReference",
    "StorageControlFolderIntelligenceConfigTimeouts",
    "StorageControlFolderIntelligenceConfigTimeoutsOutputReference",
    "StorageControlFolderIntelligenceConfigTrialConfig",
    "StorageControlFolderIntelligenceConfigTrialConfigList",
    "StorageControlFolderIntelligenceConfigTrialConfigOutputReference",
]

publication.publish()

def _typecheckingstub__2e83c20f04f6a6af2a7ff70dfa922838d0c8ccb258a589fcd5fb9f06e46ad283(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    edition_config: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[StorageControlFolderIntelligenceConfigFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[StorageControlFolderIntelligenceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__82f38c7060dca1e974f4160d898c6b5776825647dfd2f4f9978cbf5c8e637088(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f067a25cbbc21083a37a6716ece681aaad9fdcfc97f3ad13faf62a91dba4e960(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b0735e93d4c874efcadfaef41cbcdb0498e7483a8c810f089df9268caf15be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36f504bf378d2533c6af7103dfd5241f56edaf34ac1604464dc051d6d8529a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ec80ae280bbd602a368a1d91173fa95d2c26be86371e79262d854df0d724bf(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    edition_config: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[StorageControlFolderIntelligenceConfigFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[StorageControlFolderIntelligenceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d460fad3048cbf6e26f52cac6cb0a19374898e3dd284254f5e86ffaf57a7f7f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__577e1f911297632ee3c36e4c2287e35e831e7404f53e4fa96c09a292c71c0411(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ccfeba8580c00b5291ae22bf341bee30f4ae6f65a271895ca58546ba0d4161(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96264ddeb9df9da08e3b22b870735598e4a7ce1123baa2a51bd34a3479ba60d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd6b6d21b72e3545ca94aac31c81e2ee0b6a529b7edcdcb5baf50d3ec18bb0dc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c22b9b579fe92d2489f43bbfdcbec9c09721866abe9cd6ad026baed644340878(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8501f83b04e4cf55b271b6d392cf15b7556c1f767bdc82fae9ef4229005db28(
    value: typing.Optional[StorageControlFolderIntelligenceConfigEffectiveIntelligenceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0bc80beb5f614595e08007382f3c7ed1852d8a2654eb2b6b61167db2b4ad87f(
    *,
    excluded_cloud_storage_buckets: typing.Optional[typing.Union[StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    excluded_cloud_storage_locations: typing.Optional[typing.Union[StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
    included_cloud_storage_buckets: typing.Optional[typing.Union[StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    included_cloud_storage_locations: typing.Optional[typing.Union[StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3fc7d83fd1d0d64fa0eb63bdcbda59f2d43e81f78b46f1267b7c4514606c8be(
    *,
    bucket_id_regexes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673d7422b92ed058350345ceb81bb293bb0552a877339dffe5f7b2a9f2b96e28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd3eeef5a5a2c38fd8d603dad09670f1af0f75c8eb891f1caf98c5f39ffa745e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b180b123c99c4194a723476b26203314e7c2e4287f8d21638d8f0713ea751d0(
    value: typing.Optional[StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0f0aeb3d5e1dac41134578fd2306867525c63bd48e8f74a754186b0424b097(
    *,
    locations: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89718513eb491106f8cc413ffe5a908de0d75e09b93139c92c9a0a4e9493c15d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6ccbf00e58b19565831cf7dae011b69c9490ad176873aa315e9f5f174847f0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d470304e2b23eceee8e36a62b5a926c5cc7d5dc400b38580a9c83884faba53(
    value: typing.Optional[StorageControlFolderIntelligenceConfigFilterExcludedCloudStorageLocations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c256ac9b39cacca01d39ad2934bfe2367734f2cb0afdc9a5eac475f1276f46(
    *,
    bucket_id_regexes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e80b770b7e978d4a70507f455be29574a86c4d53b7b7939460a097ef68db7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a5ee3803f095823422756cfdfb5727acebe9d41bf6404ec1ecdea4ddadef7f1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f191e90f40c3a00c57732d6334958a3d2dbb45d44dfd3669f4af1b45ddd0d3b(
    value: typing.Optional[StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf4092b5102ba46c5165a62869e35de3e109129ccd70de75b2f4a65f1a00beb(
    *,
    locations: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af71fa13c52ad73dad7555387111f4cded2d7e338dfa92d8cd72fa1cf53951d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88aad610805b97d50d619aa4f5f712b2d3849b22ee5948d08c2786e40174fe05(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fad1f4d7069ac6b0b76b8b65a7e4c9bbdf8a1e6999cb22f956fef27b1010944(
    value: typing.Optional[StorageControlFolderIntelligenceConfigFilterIncludedCloudStorageLocations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a5c750bbee5e2d94662b7400453fa9727e112fd89eaf362e3ab080b83a60d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee02a7cf6bd16c1a1537aa5424878af3cab880f7b0a4517bbe7d242764340e8(
    value: typing.Optional[StorageControlFolderIntelligenceConfigFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb77ee0cf88160893fbbe991de057c832c514fcfa93f8fbfe59624f00c244df4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e850e872b9904e975c6e484576714adacf355fa82af3e1cc3c3e6c9e47c53d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e3670e110fd2d1e4468f3afe83db572a6327b96a24fdafec54e0ded7df00eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b01511d759d8f3aff8c51283d72a82b9a250cfb217aea0a73e62cac5818d5fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6878b55587a3889d2c5496acc42299cacde905e527929f764e2c45d4668721c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82eb2c5620dbc9152d2ccaa1fa9f0211b99e24e1da98c2e91959ee150afb0422(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageControlFolderIntelligenceConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d8314900ade3fe80662f20332888d7f938eafe07bb6095761fb85390660cc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a426a9c0c4884e2f024bfffe658d77814e3e2df9c0e4f620352c473008107f40(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb5274ef33c6fa54f1b455c43d90a8921352a2f0e0917b9ffead045a0edd65d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49a708528558fcabd768a59076dbc68eaf5443a557b18055a6ecfbc59ef77bdb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb9da5a505698ceda02dbd5d42acc1d502ca30874d896e0c5575af778ef26ee(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34f65b2149762c3759d2695e7ec57bbed61b20f469135e0fc7117dcee987863(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809dd1382f03758c80168599799d219339745ba41cc53c728e9f6ab998253bbd(
    value: typing.Optional[StorageControlFolderIntelligenceConfigTrialConfig],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `google_storage_control_project_intelligence_config`

Refer to the Terraform Registry for docs: [`google_storage_control_project_intelligence_config`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config).
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


class StorageControlProjectIntelligenceConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config google_storage_control_project_intelligence_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        edition_config: typing.Optional[builtins.str] = None,
        filter: typing.Optional[typing.Union["StorageControlProjectIntelligenceConfigFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["StorageControlProjectIntelligenceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config google_storage_control_project_intelligence_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Identifier of the GCP project. For GCP project, this field can be project name or project number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#name StorageControlProjectIntelligenceConfig#name}
        :param edition_config: Edition configuration of the Storage Intelligence resource. Valid values are INHERIT, TRIAL, DISABLED and STANDARD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#edition_config StorageControlProjectIntelligenceConfig#edition_config}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#filter StorageControlProjectIntelligenceConfig#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#id StorageControlProjectIntelligenceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#timeouts StorageControlProjectIntelligenceConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69065bc8727cfb8644e31f37ef7fc3707069e8e7b423b63106a5bb45d12b72dc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StorageControlProjectIntelligenceConfigConfig(
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
        '''Generates CDKTF code for importing a StorageControlProjectIntelligenceConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StorageControlProjectIntelligenceConfig to import.
        :param import_from_id: The id of the existing StorageControlProjectIntelligenceConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StorageControlProjectIntelligenceConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4e31565eae8d0ee1aa75023de24706e10c8f7136a9fb47415d262802db24ca)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        *,
        excluded_cloud_storage_buckets: typing.Optional[typing.Union["StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        excluded_cloud_storage_locations: typing.Optional[typing.Union["StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_buckets: typing.Optional[typing.Union["StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_locations: typing.Optional[typing.Union["StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excluded_cloud_storage_buckets: excluded_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#excluded_cloud_storage_buckets StorageControlProjectIntelligenceConfig#excluded_cloud_storage_buckets}
        :param excluded_cloud_storage_locations: excluded_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#excluded_cloud_storage_locations StorageControlProjectIntelligenceConfig#excluded_cloud_storage_locations}
        :param included_cloud_storage_buckets: included_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#included_cloud_storage_buckets StorageControlProjectIntelligenceConfig#included_cloud_storage_buckets}
        :param included_cloud_storage_locations: included_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#included_cloud_storage_locations StorageControlProjectIntelligenceConfig#included_cloud_storage_locations}
        '''
        value = StorageControlProjectIntelligenceConfigFilter(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#create StorageControlProjectIntelligenceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#delete StorageControlProjectIntelligenceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#update StorageControlProjectIntelligenceConfig#update}.
        '''
        value = StorageControlProjectIntelligenceConfigTimeouts(
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
    ) -> "StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigList":
        return typing.cast("StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigList", jsii.get(self, "effectiveIntelligenceConfig"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> "StorageControlProjectIntelligenceConfigFilterOutputReference":
        return typing.cast("StorageControlProjectIntelligenceConfigFilterOutputReference", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "StorageControlProjectIntelligenceConfigTimeoutsOutputReference":
        return typing.cast("StorageControlProjectIntelligenceConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="trialConfig")
    def trial_config(self) -> "StorageControlProjectIntelligenceConfigTrialConfigList":
        return typing.cast("StorageControlProjectIntelligenceConfigTrialConfigList", jsii.get(self, "trialConfig"))

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
    ) -> typing.Optional["StorageControlProjectIntelligenceConfigFilter"]:
        return typing.cast(typing.Optional["StorageControlProjectIntelligenceConfigFilter"], jsii.get(self, "filterInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageControlProjectIntelligenceConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageControlProjectIntelligenceConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="editionConfig")
    def edition_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "editionConfig"))

    @edition_config.setter
    def edition_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__545d59a4870547b6ec2dc44d6df2e7b80e5aa9001e78164ea006c00f1e62cad5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "editionConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc1409c2453ee6a5f635bfc9723180fc860f822dbbd7d1204df5c5cd38ad62d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a95ca877747a0f72cc71d047929b7e69f5124220e8d61d821c8d3878b992eb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigConfig",
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
class StorageControlProjectIntelligenceConfigConfig(
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
        filter: typing.Optional[typing.Union["StorageControlProjectIntelligenceConfigFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["StorageControlProjectIntelligenceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Identifier of the GCP project. For GCP project, this field can be project name or project number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#name StorageControlProjectIntelligenceConfig#name}
        :param edition_config: Edition configuration of the Storage Intelligence resource. Valid values are INHERIT, TRIAL, DISABLED and STANDARD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#edition_config StorageControlProjectIntelligenceConfig#edition_config}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#filter StorageControlProjectIntelligenceConfig#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#id StorageControlProjectIntelligenceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#timeouts StorageControlProjectIntelligenceConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(filter, dict):
            filter = StorageControlProjectIntelligenceConfigFilter(**filter)
        if isinstance(timeouts, dict):
            timeouts = StorageControlProjectIntelligenceConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f7ea2151348d12ddefb7d6b3cddc7b8a565fad9bd82a0255091bda2b4521015)
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
        '''Identifier of the GCP project. For GCP project, this field can be project name or project number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#name StorageControlProjectIntelligenceConfig#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def edition_config(self) -> typing.Optional[builtins.str]:
        '''Edition configuration of the Storage Intelligence resource. Valid values are INHERIT, TRIAL, DISABLED and STANDARD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#edition_config StorageControlProjectIntelligenceConfig#edition_config}
        '''
        result = self._values.get("edition_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional["StorageControlProjectIntelligenceConfigFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#filter StorageControlProjectIntelligenceConfig#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional["StorageControlProjectIntelligenceConfigFilter"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#id StorageControlProjectIntelligenceConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["StorageControlProjectIntelligenceConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#timeouts StorageControlProjectIntelligenceConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["StorageControlProjectIntelligenceConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlProjectIntelligenceConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac591e6f50f2f11ebdad18e34fc2b330a0cfdc66ee84135eb9c66dd7f3102c63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ac4c135c6a34e89f43038d8a473f059cb3d3ddae3e8eeba33366a5e2041094)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5649d050cdf52d5d234b85b6550d606f85d8e01edf08c45e25212df5d7d0fb41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a37d3ee7306ad828f1a9c494ca2aa35119e0bdf4f4a360ff980daa61bb523105)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d41a2880cdde6833a38db14fd732ce0912f21664b5482f21897fd8d15adcc3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f0190c8bc0e2274bd74ce962e160ac2f48a82359abd863d073f97d2f4c3d858)
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
    ) -> typing.Optional[StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfig]:
        return typing.cast(typing.Optional[StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31e67ca7f9279500e5d0f3041c909f28151d8deb13261f372a36570d4c27b11e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigFilter",
    jsii_struct_bases=[],
    name_mapping={
        "excluded_cloud_storage_buckets": "excludedCloudStorageBuckets",
        "excluded_cloud_storage_locations": "excludedCloudStorageLocations",
        "included_cloud_storage_buckets": "includedCloudStorageBuckets",
        "included_cloud_storage_locations": "includedCloudStorageLocations",
    },
)
class StorageControlProjectIntelligenceConfigFilter:
    def __init__(
        self,
        *,
        excluded_cloud_storage_buckets: typing.Optional[typing.Union["StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        excluded_cloud_storage_locations: typing.Optional[typing.Union["StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_buckets: typing.Optional[typing.Union["StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_locations: typing.Optional[typing.Union["StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excluded_cloud_storage_buckets: excluded_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#excluded_cloud_storage_buckets StorageControlProjectIntelligenceConfig#excluded_cloud_storage_buckets}
        :param excluded_cloud_storage_locations: excluded_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#excluded_cloud_storage_locations StorageControlProjectIntelligenceConfig#excluded_cloud_storage_locations}
        :param included_cloud_storage_buckets: included_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#included_cloud_storage_buckets StorageControlProjectIntelligenceConfig#included_cloud_storage_buckets}
        :param included_cloud_storage_locations: included_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#included_cloud_storage_locations StorageControlProjectIntelligenceConfig#included_cloud_storage_locations}
        '''
        if isinstance(excluded_cloud_storage_buckets, dict):
            excluded_cloud_storage_buckets = StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets(**excluded_cloud_storage_buckets)
        if isinstance(excluded_cloud_storage_locations, dict):
            excluded_cloud_storage_locations = StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations(**excluded_cloud_storage_locations)
        if isinstance(included_cloud_storage_buckets, dict):
            included_cloud_storage_buckets = StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets(**included_cloud_storage_buckets)
        if isinstance(included_cloud_storage_locations, dict):
            included_cloud_storage_locations = StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations(**included_cloud_storage_locations)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b626a53e2562a6d16af036355e284aea5268c25efded5064eb1e4bcb5504545e)
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
    ) -> typing.Optional["StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets"]:
        '''excluded_cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#excluded_cloud_storage_buckets StorageControlProjectIntelligenceConfig#excluded_cloud_storage_buckets}
        '''
        result = self._values.get("excluded_cloud_storage_buckets")
        return typing.cast(typing.Optional["StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets"], result)

    @builtins.property
    def excluded_cloud_storage_locations(
        self,
    ) -> typing.Optional["StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations"]:
        '''excluded_cloud_storage_locations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#excluded_cloud_storage_locations StorageControlProjectIntelligenceConfig#excluded_cloud_storage_locations}
        '''
        result = self._values.get("excluded_cloud_storage_locations")
        return typing.cast(typing.Optional["StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations"], result)

    @builtins.property
    def included_cloud_storage_buckets(
        self,
    ) -> typing.Optional["StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets"]:
        '''included_cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#included_cloud_storage_buckets StorageControlProjectIntelligenceConfig#included_cloud_storage_buckets}
        '''
        result = self._values.get("included_cloud_storage_buckets")
        return typing.cast(typing.Optional["StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets"], result)

    @builtins.property
    def included_cloud_storage_locations(
        self,
    ) -> typing.Optional["StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations"]:
        '''included_cloud_storage_locations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#included_cloud_storage_locations StorageControlProjectIntelligenceConfig#included_cloud_storage_locations}
        '''
        result = self._values.get("included_cloud_storage_locations")
        return typing.cast(typing.Optional["StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlProjectIntelligenceConfigFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={"bucket_id_regexes": "bucketIdRegexes"},
)
class StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets:
    def __init__(self, *, bucket_id_regexes: typing.Sequence[builtins.str]) -> None:
        '''
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#bucket_id_regexes StorageControlProjectIntelligenceConfig#bucket_id_regexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d46e1a8bc69eea2c4034a2d592a9beac82fdabf0b217a1de1216b1165d8e1cb)
            check_type(argname="argument bucket_id_regexes", value=bucket_id_regexes, expected_type=type_hints["bucket_id_regexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_id_regexes": bucket_id_regexes,
        }

    @builtins.property
    def bucket_id_regexes(self) -> typing.List[builtins.str]:
        '''List of bucket id regexes to exclude in the storage intelligence plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#bucket_id_regexes StorageControlProjectIntelligenceConfig#bucket_id_regexes}
        '''
        result = self._values.get("bucket_id_regexes")
        assert result is not None, "Required property 'bucket_id_regexes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57f41937c93febd121cf7ed6322882f53353bb4434a13d0329ed40c948ca9327)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ae8638c16566a9b9e8e367bde089c8ae9babeedcbc86cd3916e9d122a3f1bc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketIdRegexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce401e72a6e28268c7a43bea359076addd36cb95932425b0936cbe41d254f375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations",
    jsii_struct_bases=[],
    name_mapping={"locations": "locations"},
)
class StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations:
    def __init__(self, *, locations: typing.Sequence[builtins.str]) -> None:
        '''
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#locations StorageControlProjectIntelligenceConfig#locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0a027f3153fba5a3c891dfed098b60694235820f305d188a6d7317c3cadd79c)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locations": locations,
        }

    @builtins.property
    def locations(self) -> typing.List[builtins.str]:
        '''List of locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#locations StorageControlProjectIntelligenceConfig#locations}
        '''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7994e9db8d86854c5a02af9c24cee8545b751d743072e70a704cee2e3402a5c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb0e2519f07ef002f27d6f457f050a726daf0b170ab146704242bede4f86d974)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations]:
        return typing.cast(typing.Optional[StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a778e7f99fddb0a6f565742402e68be2f202847809617c28a2074a3fc29d564b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={"bucket_id_regexes": "bucketIdRegexes"},
)
class StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets:
    def __init__(self, *, bucket_id_regexes: typing.Sequence[builtins.str]) -> None:
        '''
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#bucket_id_regexes StorageControlProjectIntelligenceConfig#bucket_id_regexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398bdc3f682d5013a5cfbafc081367cc0c614545571703c85668625279a64d87)
            check_type(argname="argument bucket_id_regexes", value=bucket_id_regexes, expected_type=type_hints["bucket_id_regexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_id_regexes": bucket_id_regexes,
        }

    @builtins.property
    def bucket_id_regexes(self) -> typing.List[builtins.str]:
        '''List of bucket id regexes to exclude in the storage intelligence plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#bucket_id_regexes StorageControlProjectIntelligenceConfig#bucket_id_regexes}
        '''
        result = self._values.get("bucket_id_regexes")
        assert result is not None, "Required property 'bucket_id_regexes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f8785a40d776b7f07db7f5b73d90ab8aae2743682b0a8f77ce94b7b1d53b006)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bce117acab5b07a037b05b4086bcfbcdd6f35bee95f21568dedef2ffc7a211d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketIdRegexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea2332bbf32fb8370ca5e0c6e2458792d3d91fd58a3cd72010ee520878e4afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations",
    jsii_struct_bases=[],
    name_mapping={"locations": "locations"},
)
class StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations:
    def __init__(self, *, locations: typing.Sequence[builtins.str]) -> None:
        '''
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#locations StorageControlProjectIntelligenceConfig#locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75db50f40a74d0caf018185bec1db6ccf393125b474648f87b72303b0edad62c)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locations": locations,
        }

    @builtins.property
    def locations(self) -> typing.List[builtins.str]:
        '''List of locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#locations StorageControlProjectIntelligenceConfig#locations}
        '''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d51c89fe41c9347b29e30fa24bb734281b43a6c5a047a7097d3f03688a77d8cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c662babd94790cc1f85f1e95e174fce51268605af02bbb1164f3b02f5ec28c8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations]:
        return typing.cast(typing.Optional[StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e3a4e60b1c5eb22de38c41d1c375709e821d1e373b0f9ef27ec5d2934917225)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageControlProjectIntelligenceConfigFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5e36f7311aaa0d459fbe36c6dd89cfb2248d0f0d424894cca0641f6cf4ad7e6)
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
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#bucket_id_regexes StorageControlProjectIntelligenceConfig#bucket_id_regexes}
        '''
        value = StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets(
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
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#locations StorageControlProjectIntelligenceConfig#locations}
        '''
        value = StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations(
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
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#bucket_id_regexes StorageControlProjectIntelligenceConfig#bucket_id_regexes}
        '''
        value = StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets(
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
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#locations StorageControlProjectIntelligenceConfig#locations}
        '''
        value = StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations(
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
    ) -> StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference:
        return typing.cast(StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference, jsii.get(self, "excludedCloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="excludedCloudStorageLocations")
    def excluded_cloud_storage_locations(
        self,
    ) -> StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference:
        return typing.cast(StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference, jsii.get(self, "excludedCloudStorageLocations"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageBuckets")
    def included_cloud_storage_buckets(
        self,
    ) -> StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference:
        return typing.cast(StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference, jsii.get(self, "includedCloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageLocations")
    def included_cloud_storage_locations(
        self,
    ) -> StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference:
        return typing.cast(StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference, jsii.get(self, "includedCloudStorageLocations"))

    @builtins.property
    @jsii.member(jsii_name="excludedCloudStorageBucketsInput")
    def excluded_cloud_storage_buckets_input(
        self,
    ) -> typing.Optional[StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets], jsii.get(self, "excludedCloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedCloudStorageLocationsInput")
    def excluded_cloud_storage_locations_input(
        self,
    ) -> typing.Optional[StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations]:
        return typing.cast(typing.Optional[StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations], jsii.get(self, "excludedCloudStorageLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageBucketsInput")
    def included_cloud_storage_buckets_input(
        self,
    ) -> typing.Optional[StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets], jsii.get(self, "includedCloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageLocationsInput")
    def included_cloud_storage_locations_input(
        self,
    ) -> typing.Optional[StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations]:
        return typing.cast(typing.Optional[StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations], jsii.get(self, "includedCloudStorageLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageControlProjectIntelligenceConfigFilter]:
        return typing.cast(typing.Optional[StorageControlProjectIntelligenceConfigFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlProjectIntelligenceConfigFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ff9ad2bd8a537de80d695021b097c46af03ea7a654266358a5f9b434b93de8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class StorageControlProjectIntelligenceConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#create StorageControlProjectIntelligenceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#delete StorageControlProjectIntelligenceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#update StorageControlProjectIntelligenceConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a2e0411dc83606022fedfe2894040edbda29d0d04aae50c0c35fe1bbda1e7f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#create StorageControlProjectIntelligenceConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#delete StorageControlProjectIntelligenceConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_project_intelligence_config#update StorageControlProjectIntelligenceConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlProjectIntelligenceConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlProjectIntelligenceConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61ee3171aa600367d7b2885dd06ac7466bf5d479bd89b4e0d784d8733b18daea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__524cb217960a2085a9f8415d4cb6b849e7cd3604da7b66e9624d2889adfbe10f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d7ca707a416f69074b811db14df3966cf4c0839d5f490e9abb084dad3cfe2b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13a49bdb4b9980e4593fbb8cb522a6261830927fc3342ccdc604589a7e2fe6af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageControlProjectIntelligenceConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageControlProjectIntelligenceConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageControlProjectIntelligenceConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18193cf7abce20b9ecb66671443fbba6856f8a739ba7526c97b800aea6cea81d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigTrialConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class StorageControlProjectIntelligenceConfigTrialConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlProjectIntelligenceConfigTrialConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlProjectIntelligenceConfigTrialConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigTrialConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__077d7ab3db4d8a0880ce2d41b245ec06195719b3e1998a36e1cd344fdfae9fb4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StorageControlProjectIntelligenceConfigTrialConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5affbaf85e05af1bda41987412d8413fa338ada41184ec749ada59159712bf58)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageControlProjectIntelligenceConfigTrialConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64162cdd38d1ef78e0ea89b681d6db03d2113f86ab11ccc1a083ba6f8efd7ffa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eabd280af4607494818196c6c41f71d51fed05ada43b2c33ae872b23bab78a7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0efce4bbc63c58859199812bc08352ec84080917f589fdb35e14d86cc6f8d8fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class StorageControlProjectIntelligenceConfigTrialConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlProjectIntelligenceConfig.StorageControlProjectIntelligenceConfigTrialConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a69e5a2384a6ed2a2f53abcb1e624a520bf54d681798f2f043597f8a2793a1d6)
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
    ) -> typing.Optional[StorageControlProjectIntelligenceConfigTrialConfig]:
        return typing.cast(typing.Optional[StorageControlProjectIntelligenceConfigTrialConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlProjectIntelligenceConfigTrialConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec46be696e319df4f05c6154808bda7427e5d8c2a531e20fda7bb33f3c65d48f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StorageControlProjectIntelligenceConfig",
    "StorageControlProjectIntelligenceConfigConfig",
    "StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfig",
    "StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigList",
    "StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigOutputReference",
    "StorageControlProjectIntelligenceConfigFilter",
    "StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets",
    "StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference",
    "StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations",
    "StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference",
    "StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets",
    "StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference",
    "StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations",
    "StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference",
    "StorageControlProjectIntelligenceConfigFilterOutputReference",
    "StorageControlProjectIntelligenceConfigTimeouts",
    "StorageControlProjectIntelligenceConfigTimeoutsOutputReference",
    "StorageControlProjectIntelligenceConfigTrialConfig",
    "StorageControlProjectIntelligenceConfigTrialConfigList",
    "StorageControlProjectIntelligenceConfigTrialConfigOutputReference",
]

publication.publish()

def _typecheckingstub__69065bc8727cfb8644e31f37ef7fc3707069e8e7b423b63106a5bb45d12b72dc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    edition_config: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[StorageControlProjectIntelligenceConfigFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[StorageControlProjectIntelligenceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4a4e31565eae8d0ee1aa75023de24706e10c8f7136a9fb47415d262802db24ca(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545d59a4870547b6ec2dc44d6df2e7b80e5aa9001e78164ea006c00f1e62cad5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc1409c2453ee6a5f635bfc9723180fc860f822dbbd7d1204df5c5cd38ad62d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a95ca877747a0f72cc71d047929b7e69f5124220e8d61d821c8d3878b992eb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7ea2151348d12ddefb7d6b3cddc7b8a565fad9bd82a0255091bda2b4521015(
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
    filter: typing.Optional[typing.Union[StorageControlProjectIntelligenceConfigFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[StorageControlProjectIntelligenceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac591e6f50f2f11ebdad18e34fc2b330a0cfdc66ee84135eb9c66dd7f3102c63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ac4c135c6a34e89f43038d8a473f059cb3d3ddae3e8eeba33366a5e2041094(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5649d050cdf52d5d234b85b6550d606f85d8e01edf08c45e25212df5d7d0fb41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a37d3ee7306ad828f1a9c494ca2aa35119e0bdf4f4a360ff980daa61bb523105(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d41a2880cdde6833a38db14fd732ce0912f21664b5482f21897fd8d15adcc3d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0190c8bc0e2274bd74ce962e160ac2f48a82359abd863d073f97d2f4c3d858(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e67ca7f9279500e5d0f3041c909f28151d8deb13261f372a36570d4c27b11e(
    value: typing.Optional[StorageControlProjectIntelligenceConfigEffectiveIntelligenceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b626a53e2562a6d16af036355e284aea5268c25efded5064eb1e4bcb5504545e(
    *,
    excluded_cloud_storage_buckets: typing.Optional[typing.Union[StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    excluded_cloud_storage_locations: typing.Optional[typing.Union[StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
    included_cloud_storage_buckets: typing.Optional[typing.Union[StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    included_cloud_storage_locations: typing.Optional[typing.Union[StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d46e1a8bc69eea2c4034a2d592a9beac82fdabf0b217a1de1216b1165d8e1cb(
    *,
    bucket_id_regexes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f41937c93febd121cf7ed6322882f53353bb4434a13d0329ed40c948ca9327(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae8638c16566a9b9e8e367bde089c8ae9babeedcbc86cd3916e9d122a3f1bc0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce401e72a6e28268c7a43bea359076addd36cb95932425b0936cbe41d254f375(
    value: typing.Optional[StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a027f3153fba5a3c891dfed098b60694235820f305d188a6d7317c3cadd79c(
    *,
    locations: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7994e9db8d86854c5a02af9c24cee8545b751d743072e70a704cee2e3402a5c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0e2519f07ef002f27d6f457f050a726daf0b170ab146704242bede4f86d974(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a778e7f99fddb0a6f565742402e68be2f202847809617c28a2074a3fc29d564b(
    value: typing.Optional[StorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398bdc3f682d5013a5cfbafc081367cc0c614545571703c85668625279a64d87(
    *,
    bucket_id_regexes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f8785a40d776b7f07db7f5b73d90ab8aae2743682b0a8f77ce94b7b1d53b006(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce117acab5b07a037b05b4086bcfbcdd6f35bee95f21568dedef2ffc7a211d4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea2332bbf32fb8370ca5e0c6e2458792d3d91fd58a3cd72010ee520878e4afa(
    value: typing.Optional[StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75db50f40a74d0caf018185bec1db6ccf393125b474648f87b72303b0edad62c(
    *,
    locations: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d51c89fe41c9347b29e30fa24bb734281b43a6c5a047a7097d3f03688a77d8cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c662babd94790cc1f85f1e95e174fce51268605af02bbb1164f3b02f5ec28c8d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3a4e60b1c5eb22de38c41d1c375709e821d1e373b0f9ef27ec5d2934917225(
    value: typing.Optional[StorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e36f7311aaa0d459fbe36c6dd89cfb2248d0f0d424894cca0641f6cf4ad7e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ff9ad2bd8a537de80d695021b097c46af03ea7a654266358a5f9b434b93de8(
    value: typing.Optional[StorageControlProjectIntelligenceConfigFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a2e0411dc83606022fedfe2894040edbda29d0d04aae50c0c35fe1bbda1e7f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ee3171aa600367d7b2885dd06ac7466bf5d479bd89b4e0d784d8733b18daea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524cb217960a2085a9f8415d4cb6b849e7cd3604da7b66e9624d2889adfbe10f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d7ca707a416f69074b811db14df3966cf4c0839d5f490e9abb084dad3cfe2b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a49bdb4b9980e4593fbb8cb522a6261830927fc3342ccdc604589a7e2fe6af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18193cf7abce20b9ecb66671443fbba6856f8a739ba7526c97b800aea6cea81d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageControlProjectIntelligenceConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077d7ab3db4d8a0880ce2d41b245ec06195719b3e1998a36e1cd344fdfae9fb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5affbaf85e05af1bda41987412d8413fa338ada41184ec749ada59159712bf58(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64162cdd38d1ef78e0ea89b681d6db03d2113f86ab11ccc1a083ba6f8efd7ffa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eabd280af4607494818196c6c41f71d51fed05ada43b2c33ae872b23bab78a7d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efce4bbc63c58859199812bc08352ec84080917f589fdb35e14d86cc6f8d8fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69e5a2384a6ed2a2f53abcb1e624a520bf54d681798f2f043597f8a2793a1d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec46be696e319df4f05c6154808bda7427e5d8c2a531e20fda7bb33f3c65d48f(
    value: typing.Optional[StorageControlProjectIntelligenceConfigTrialConfig],
) -> None:
    """Type checking stubs"""
    pass

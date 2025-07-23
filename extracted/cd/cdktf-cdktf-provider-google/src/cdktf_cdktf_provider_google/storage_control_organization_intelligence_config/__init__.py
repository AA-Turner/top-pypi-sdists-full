r'''
# `google_storage_control_organization_intelligence_config`

Refer to the Terraform Registry for docs: [`google_storage_control_organization_intelligence_config`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config).
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


class StorageControlOrganizationIntelligenceConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config google_storage_control_organization_intelligence_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        edition_config: typing.Optional[builtins.str] = None,
        filter: typing.Optional[typing.Union["StorageControlOrganizationIntelligenceConfigFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["StorageControlOrganizationIntelligenceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config google_storage_control_organization_intelligence_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Identifier of the GCP Organization. For GCP org, this field should be organization number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#name StorageControlOrganizationIntelligenceConfig#name}
        :param edition_config: Edition configuration of the Storage Intelligence resource. Valid values are INHERIT, DISABLED, TRIAL and STANDARD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#edition_config StorageControlOrganizationIntelligenceConfig#edition_config}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#filter StorageControlOrganizationIntelligenceConfig#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#id StorageControlOrganizationIntelligenceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#timeouts StorageControlOrganizationIntelligenceConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee0825624641babd8ca903a76a3751d7c3a50ad8fa8b9b17109a0c39a2509fb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StorageControlOrganizationIntelligenceConfigConfig(
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
        '''Generates CDKTF code for importing a StorageControlOrganizationIntelligenceConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StorageControlOrganizationIntelligenceConfig to import.
        :param import_from_id: The id of the existing StorageControlOrganizationIntelligenceConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StorageControlOrganizationIntelligenceConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e7835388c6591c38748fce040aaa3d6be7f6a3b90a6773d00a1f8b8fe191625)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        *,
        excluded_cloud_storage_buckets: typing.Optional[typing.Union["StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        excluded_cloud_storage_locations: typing.Optional[typing.Union["StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_buckets: typing.Optional[typing.Union["StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_locations: typing.Optional[typing.Union["StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excluded_cloud_storage_buckets: excluded_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#excluded_cloud_storage_buckets StorageControlOrganizationIntelligenceConfig#excluded_cloud_storage_buckets}
        :param excluded_cloud_storage_locations: excluded_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#excluded_cloud_storage_locations StorageControlOrganizationIntelligenceConfig#excluded_cloud_storage_locations}
        :param included_cloud_storage_buckets: included_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#included_cloud_storage_buckets StorageControlOrganizationIntelligenceConfig#included_cloud_storage_buckets}
        :param included_cloud_storage_locations: included_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#included_cloud_storage_locations StorageControlOrganizationIntelligenceConfig#included_cloud_storage_locations}
        '''
        value = StorageControlOrganizationIntelligenceConfigFilter(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#create StorageControlOrganizationIntelligenceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#delete StorageControlOrganizationIntelligenceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#update StorageControlOrganizationIntelligenceConfig#update}.
        '''
        value = StorageControlOrganizationIntelligenceConfigTimeouts(
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
    ) -> "StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigList":
        return typing.cast("StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigList", jsii.get(self, "effectiveIntelligenceConfig"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(
        self,
    ) -> "StorageControlOrganizationIntelligenceConfigFilterOutputReference":
        return typing.cast("StorageControlOrganizationIntelligenceConfigFilterOutputReference", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "StorageControlOrganizationIntelligenceConfigTimeoutsOutputReference":
        return typing.cast("StorageControlOrganizationIntelligenceConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="trialConfig")
    def trial_config(
        self,
    ) -> "StorageControlOrganizationIntelligenceConfigTrialConfigList":
        return typing.cast("StorageControlOrganizationIntelligenceConfigTrialConfigList", jsii.get(self, "trialConfig"))

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
    ) -> typing.Optional["StorageControlOrganizationIntelligenceConfigFilter"]:
        return typing.cast(typing.Optional["StorageControlOrganizationIntelligenceConfigFilter"], jsii.get(self, "filterInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageControlOrganizationIntelligenceConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageControlOrganizationIntelligenceConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="editionConfig")
    def edition_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "editionConfig"))

    @edition_config.setter
    def edition_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda56cc9badc778f98ee3ec7b57eca774370f0e4d1b86f0578ca28c4b204fe2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "editionConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9fe4db8f4ad00d8d5fcd2f4f48747b4765220ffc0310fadd7757fe3287ce698)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a38eb01c45cd22b1fb929497c34bed27e5c04e71222ab47a9f01b09ba507738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigConfig",
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
class StorageControlOrganizationIntelligenceConfigConfig(
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
        filter: typing.Optional[typing.Union["StorageControlOrganizationIntelligenceConfigFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["StorageControlOrganizationIntelligenceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Identifier of the GCP Organization. For GCP org, this field should be organization number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#name StorageControlOrganizationIntelligenceConfig#name}
        :param edition_config: Edition configuration of the Storage Intelligence resource. Valid values are INHERIT, DISABLED, TRIAL and STANDARD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#edition_config StorageControlOrganizationIntelligenceConfig#edition_config}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#filter StorageControlOrganizationIntelligenceConfig#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#id StorageControlOrganizationIntelligenceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#timeouts StorageControlOrganizationIntelligenceConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(filter, dict):
            filter = StorageControlOrganizationIntelligenceConfigFilter(**filter)
        if isinstance(timeouts, dict):
            timeouts = StorageControlOrganizationIntelligenceConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da809ca2482a259e3fbffbb53464a36dca641abad300f1002e62cca3210c424b)
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
        '''Identifier of the GCP Organization. For GCP org, this field should be organization number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#name StorageControlOrganizationIntelligenceConfig#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def edition_config(self) -> typing.Optional[builtins.str]:
        '''Edition configuration of the Storage Intelligence resource. Valid values are INHERIT, DISABLED, TRIAL and STANDARD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#edition_config StorageControlOrganizationIntelligenceConfig#edition_config}
        '''
        result = self._values.get("edition_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional["StorageControlOrganizationIntelligenceConfigFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#filter StorageControlOrganizationIntelligenceConfig#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional["StorageControlOrganizationIntelligenceConfigFilter"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#id StorageControlOrganizationIntelligenceConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["StorageControlOrganizationIntelligenceConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#timeouts StorageControlOrganizationIntelligenceConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["StorageControlOrganizationIntelligenceConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlOrganizationIntelligenceConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10c33da4be4e8a6b40c5dba5180597874ba134c3df6f33af507a2454b7374628)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__801aec2b602224c14fc34a734a896f0f8da45109e2ef48fdb4c5b1010226244c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0e604bcc26c424a9f29a4e2e29d0d4cade4ecec599d5ed132d041fab0b794c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b2217ecd735ab77784f711d43f469b8bec29fbc581a300827c636e558a589b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09b9307cdeb74e810cfed421073b36f2a1828e25c83f2eb4f923f5849536df1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__580cc2f6620a2bac0f382c98ef30c62511e56ebf6432178ee4af38a5f77554ae)
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
    ) -> typing.Optional[StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfig]:
        return typing.cast(typing.Optional[StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48b7d8b7cf1143ae484bcc9ba210642cec106652f818fb725e8ae90e25e57b1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigFilter",
    jsii_struct_bases=[],
    name_mapping={
        "excluded_cloud_storage_buckets": "excludedCloudStorageBuckets",
        "excluded_cloud_storage_locations": "excludedCloudStorageLocations",
        "included_cloud_storage_buckets": "includedCloudStorageBuckets",
        "included_cloud_storage_locations": "includedCloudStorageLocations",
    },
)
class StorageControlOrganizationIntelligenceConfigFilter:
    def __init__(
        self,
        *,
        excluded_cloud_storage_buckets: typing.Optional[typing.Union["StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        excluded_cloud_storage_locations: typing.Optional[typing.Union["StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_buckets: typing.Optional[typing.Union["StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_locations: typing.Optional[typing.Union["StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excluded_cloud_storage_buckets: excluded_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#excluded_cloud_storage_buckets StorageControlOrganizationIntelligenceConfig#excluded_cloud_storage_buckets}
        :param excluded_cloud_storage_locations: excluded_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#excluded_cloud_storage_locations StorageControlOrganizationIntelligenceConfig#excluded_cloud_storage_locations}
        :param included_cloud_storage_buckets: included_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#included_cloud_storage_buckets StorageControlOrganizationIntelligenceConfig#included_cloud_storage_buckets}
        :param included_cloud_storage_locations: included_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#included_cloud_storage_locations StorageControlOrganizationIntelligenceConfig#included_cloud_storage_locations}
        '''
        if isinstance(excluded_cloud_storage_buckets, dict):
            excluded_cloud_storage_buckets = StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets(**excluded_cloud_storage_buckets)
        if isinstance(excluded_cloud_storage_locations, dict):
            excluded_cloud_storage_locations = StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations(**excluded_cloud_storage_locations)
        if isinstance(included_cloud_storage_buckets, dict):
            included_cloud_storage_buckets = StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets(**included_cloud_storage_buckets)
        if isinstance(included_cloud_storage_locations, dict):
            included_cloud_storage_locations = StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations(**included_cloud_storage_locations)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56dcbc9393e754426895a546451e573e0b31afeb44ff787fc2380565ae3afc9)
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
    ) -> typing.Optional["StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets"]:
        '''excluded_cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#excluded_cloud_storage_buckets StorageControlOrganizationIntelligenceConfig#excluded_cloud_storage_buckets}
        '''
        result = self._values.get("excluded_cloud_storage_buckets")
        return typing.cast(typing.Optional["StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets"], result)

    @builtins.property
    def excluded_cloud_storage_locations(
        self,
    ) -> typing.Optional["StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations"]:
        '''excluded_cloud_storage_locations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#excluded_cloud_storage_locations StorageControlOrganizationIntelligenceConfig#excluded_cloud_storage_locations}
        '''
        result = self._values.get("excluded_cloud_storage_locations")
        return typing.cast(typing.Optional["StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations"], result)

    @builtins.property
    def included_cloud_storage_buckets(
        self,
    ) -> typing.Optional["StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets"]:
        '''included_cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#included_cloud_storage_buckets StorageControlOrganizationIntelligenceConfig#included_cloud_storage_buckets}
        '''
        result = self._values.get("included_cloud_storage_buckets")
        return typing.cast(typing.Optional["StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets"], result)

    @builtins.property
    def included_cloud_storage_locations(
        self,
    ) -> typing.Optional["StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations"]:
        '''included_cloud_storage_locations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#included_cloud_storage_locations StorageControlOrganizationIntelligenceConfig#included_cloud_storage_locations}
        '''
        result = self._values.get("included_cloud_storage_locations")
        return typing.cast(typing.Optional["StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlOrganizationIntelligenceConfigFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={"bucket_id_regexes": "bucketIdRegexes"},
)
class StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets:
    def __init__(self, *, bucket_id_regexes: typing.Sequence[builtins.str]) -> None:
        '''
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#bucket_id_regexes StorageControlOrganizationIntelligenceConfig#bucket_id_regexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01e2d54926a4b21a57f746b38ec1b8ec77c4fc08b939a97d88fe863a27b7899a)
            check_type(argname="argument bucket_id_regexes", value=bucket_id_regexes, expected_type=type_hints["bucket_id_regexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_id_regexes": bucket_id_regexes,
        }

    @builtins.property
    def bucket_id_regexes(self) -> typing.List[builtins.str]:
        '''List of bucket id regexes to exclude in the storage intelligence plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#bucket_id_regexes StorageControlOrganizationIntelligenceConfig#bucket_id_regexes}
        '''
        result = self._values.get("bucket_id_regexes")
        assert result is not None, "Required property 'bucket_id_regexes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd7f5ccd7a716a50d0101b63d72f397713ab67f5945d530ea7d1a0c12f34bf67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd538476f9a27c9d8c37d8873258f90248c9a8505badda3343259de579204035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketIdRegexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f5f0c439e297bfecd869b2f2077c0277b9b01d41b9d81a73b7505bfa8e26bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations",
    jsii_struct_bases=[],
    name_mapping={"locations": "locations"},
)
class StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations:
    def __init__(self, *, locations: typing.Sequence[builtins.str]) -> None:
        '''
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#locations StorageControlOrganizationIntelligenceConfig#locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a56db6e6f116fef2ceeae847e3ad246356c6cc4679e6ce6f351c2d96b7fb2eff)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locations": locations,
        }

    @builtins.property
    def locations(self) -> typing.List[builtins.str]:
        '''List of locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#locations StorageControlOrganizationIntelligenceConfig#locations}
        '''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21ef173473549c4d0ef2b00428354287d5efc66d838e1467cc78e7345ce647ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__634b175f45af0aa54d350168e995bad72038ef505c75d6ea77a75fdff6449b6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations]:
        return typing.cast(typing.Optional[StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8ed11992a44f8b273456f4b6746f84545e9e7f133c90b3748e23ac7a8f4f4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={"bucket_id_regexes": "bucketIdRegexes"},
)
class StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets:
    def __init__(self, *, bucket_id_regexes: typing.Sequence[builtins.str]) -> None:
        '''
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#bucket_id_regexes StorageControlOrganizationIntelligenceConfig#bucket_id_regexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c2759f5f3b251fd8db2c21f5964c3e426ca2d8bf105e6d2b77ac04030ce1065)
            check_type(argname="argument bucket_id_regexes", value=bucket_id_regexes, expected_type=type_hints["bucket_id_regexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_id_regexes": bucket_id_regexes,
        }

    @builtins.property
    def bucket_id_regexes(self) -> typing.List[builtins.str]:
        '''List of bucket id regexes to exclude in the storage intelligence plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#bucket_id_regexes StorageControlOrganizationIntelligenceConfig#bucket_id_regexes}
        '''
        result = self._values.get("bucket_id_regexes")
        assert result is not None, "Required property 'bucket_id_regexes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e41a1b14f20d66c176662273089f983e405c37f347f576e747e6cac83650ced)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c54f8dd78b0c54a52c9c3d0684cca33f7916f1fd14717dec619f4cb268165fac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketIdRegexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea61a828c6441e9f069dca405fceba242d9bed9dc65198a988fe3a62aa2a62c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations",
    jsii_struct_bases=[],
    name_mapping={"locations": "locations"},
)
class StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations:
    def __init__(self, *, locations: typing.Sequence[builtins.str]) -> None:
        '''
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#locations StorageControlOrganizationIntelligenceConfig#locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__410d0c5adc154f88c851648d2cbbdcf316bd48bba1c6887e587485b65c096ef5)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locations": locations,
        }

    @builtins.property
    def locations(self) -> typing.List[builtins.str]:
        '''List of locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#locations StorageControlOrganizationIntelligenceConfig#locations}
        '''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9877f7f3daa185d9af5624f7a4e966b048841bed835d35915dd7a5bcc4134cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e985d428f89925d16f73abe576aaa8ab7cdb7fccd3b5258b257a6646b08a98d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations]:
        return typing.cast(typing.Optional[StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a06400e0b624b4b97f71f9f90f944f872c46c368a58b1d05ac3521f94974a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageControlOrganizationIntelligenceConfigFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27eedb70dbc11fc78d8ea3b578a2b9080d71a16c754c0223bbb8bc82e88e885e)
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
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#bucket_id_regexes StorageControlOrganizationIntelligenceConfig#bucket_id_regexes}
        '''
        value = StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets(
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
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#locations StorageControlOrganizationIntelligenceConfig#locations}
        '''
        value = StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations(
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
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#bucket_id_regexes StorageControlOrganizationIntelligenceConfig#bucket_id_regexes}
        '''
        value = StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets(
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
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#locations StorageControlOrganizationIntelligenceConfig#locations}
        '''
        value = StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations(
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
    ) -> StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference:
        return typing.cast(StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference, jsii.get(self, "excludedCloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="excludedCloudStorageLocations")
    def excluded_cloud_storage_locations(
        self,
    ) -> StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference:
        return typing.cast(StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference, jsii.get(self, "excludedCloudStorageLocations"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageBuckets")
    def included_cloud_storage_buckets(
        self,
    ) -> StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference:
        return typing.cast(StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference, jsii.get(self, "includedCloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageLocations")
    def included_cloud_storage_locations(
        self,
    ) -> StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference:
        return typing.cast(StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference, jsii.get(self, "includedCloudStorageLocations"))

    @builtins.property
    @jsii.member(jsii_name="excludedCloudStorageBucketsInput")
    def excluded_cloud_storage_buckets_input(
        self,
    ) -> typing.Optional[StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets], jsii.get(self, "excludedCloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedCloudStorageLocationsInput")
    def excluded_cloud_storage_locations_input(
        self,
    ) -> typing.Optional[StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations]:
        return typing.cast(typing.Optional[StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations], jsii.get(self, "excludedCloudStorageLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageBucketsInput")
    def included_cloud_storage_buckets_input(
        self,
    ) -> typing.Optional[StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets], jsii.get(self, "includedCloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageLocationsInput")
    def included_cloud_storage_locations_input(
        self,
    ) -> typing.Optional[StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations]:
        return typing.cast(typing.Optional[StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations], jsii.get(self, "includedCloudStorageLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageControlOrganizationIntelligenceConfigFilter]:
        return typing.cast(typing.Optional[StorageControlOrganizationIntelligenceConfigFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlOrganizationIntelligenceConfigFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9fe3c5faf006ba2410d28a08667f4777866e4b4ba18a89c8a35ddd3ee8dd329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class StorageControlOrganizationIntelligenceConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#create StorageControlOrganizationIntelligenceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#delete StorageControlOrganizationIntelligenceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#update StorageControlOrganizationIntelligenceConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1989c78575a81bca0a97ab4c6ae1f0acd73f3ffea89ff5f3ae6b059d2761e7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#create StorageControlOrganizationIntelligenceConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#delete StorageControlOrganizationIntelligenceConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_control_organization_intelligence_config#update StorageControlOrganizationIntelligenceConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlOrganizationIntelligenceConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlOrganizationIntelligenceConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15a9ad1f789519d1ed3ad2f4c24f4ccfef61b416bef8fe1deeec5afb114d6d0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5382da55e18b6faa716a77543bb8eab0de86a908afb6cae4f9facf0b305f95b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28fde97036a3c3ef456000bf335993ae68386ec910577b70ace13ff087f199d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a600812f41da48799b01827c3ebd2bb25ae8922adbe49374ee23c48caf6e8e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageControlOrganizationIntelligenceConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageControlOrganizationIntelligenceConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageControlOrganizationIntelligenceConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cddd05e6240cef293f47476cc1d05ca82c70db8fae74afb0f545c3cd965d1ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigTrialConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class StorageControlOrganizationIntelligenceConfigTrialConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageControlOrganizationIntelligenceConfigTrialConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageControlOrganizationIntelligenceConfigTrialConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigTrialConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b86b9971492411ac288ffe5842754aff61f2c4dfc7df060fcdacf550bfa9e422)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StorageControlOrganizationIntelligenceConfigTrialConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7343ea69cacc99f2ceb67662934297c1b4f32fe84f4954fc922791f07c08f950)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageControlOrganizationIntelligenceConfigTrialConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d24626611f5538fdb9ee5ffacd1ab4b2d232fac6efa9e69b4e953ad7a3a5ec6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__628a09c61e6adb84871fb19b21273e6fc19775d9ed0813974ac06d29afe804fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9e64f321ea38e48935cd2aacee9ee5494d892ebf58281070c485da0f2790a89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class StorageControlOrganizationIntelligenceConfigTrialConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageControlOrganizationIntelligenceConfig.StorageControlOrganizationIntelligenceConfigTrialConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80588fe44cd1806b09f7273b489b98b259e307b1f823efe4c2efea6a6dd0ab3d)
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
    ) -> typing.Optional[StorageControlOrganizationIntelligenceConfigTrialConfig]:
        return typing.cast(typing.Optional[StorageControlOrganizationIntelligenceConfigTrialConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageControlOrganizationIntelligenceConfigTrialConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea15e850138bdc6717e645d7ad13c412bd4cdfaff214f0d8a21fde6667c19ecd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StorageControlOrganizationIntelligenceConfig",
    "StorageControlOrganizationIntelligenceConfigConfig",
    "StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfig",
    "StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigList",
    "StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigOutputReference",
    "StorageControlOrganizationIntelligenceConfigFilter",
    "StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets",
    "StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference",
    "StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations",
    "StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference",
    "StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets",
    "StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference",
    "StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations",
    "StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference",
    "StorageControlOrganizationIntelligenceConfigFilterOutputReference",
    "StorageControlOrganizationIntelligenceConfigTimeouts",
    "StorageControlOrganizationIntelligenceConfigTimeoutsOutputReference",
    "StorageControlOrganizationIntelligenceConfigTrialConfig",
    "StorageControlOrganizationIntelligenceConfigTrialConfigList",
    "StorageControlOrganizationIntelligenceConfigTrialConfigOutputReference",
]

publication.publish()

def _typecheckingstub__bee0825624641babd8ca903a76a3751d7c3a50ad8fa8b9b17109a0c39a2509fb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    edition_config: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[StorageControlOrganizationIntelligenceConfigFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[StorageControlOrganizationIntelligenceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5e7835388c6591c38748fce040aaa3d6be7f6a3b90a6773d00a1f8b8fe191625(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda56cc9badc778f98ee3ec7b57eca774370f0e4d1b86f0578ca28c4b204fe2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9fe4db8f4ad00d8d5fcd2f4f48747b4765220ffc0310fadd7757fe3287ce698(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a38eb01c45cd22b1fb929497c34bed27e5c04e71222ab47a9f01b09ba507738(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da809ca2482a259e3fbffbb53464a36dca641abad300f1002e62cca3210c424b(
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
    filter: typing.Optional[typing.Union[StorageControlOrganizationIntelligenceConfigFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[StorageControlOrganizationIntelligenceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c33da4be4e8a6b40c5dba5180597874ba134c3df6f33af507a2454b7374628(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__801aec2b602224c14fc34a734a896f0f8da45109e2ef48fdb4c5b1010226244c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e604bcc26c424a9f29a4e2e29d0d4cade4ecec599d5ed132d041fab0b794c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2217ecd735ab77784f711d43f469b8bec29fbc581a300827c636e558a589b3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b9307cdeb74e810cfed421073b36f2a1828e25c83f2eb4f923f5849536df1b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580cc2f6620a2bac0f382c98ef30c62511e56ebf6432178ee4af38a5f77554ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48b7d8b7cf1143ae484bcc9ba210642cec106652f818fb725e8ae90e25e57b1a(
    value: typing.Optional[StorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56dcbc9393e754426895a546451e573e0b31afeb44ff787fc2380565ae3afc9(
    *,
    excluded_cloud_storage_buckets: typing.Optional[typing.Union[StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    excluded_cloud_storage_locations: typing.Optional[typing.Union[StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
    included_cloud_storage_buckets: typing.Optional[typing.Union[StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    included_cloud_storage_locations: typing.Optional[typing.Union[StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e2d54926a4b21a57f746b38ec1b8ec77c4fc08b939a97d88fe863a27b7899a(
    *,
    bucket_id_regexes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7f5ccd7a716a50d0101b63d72f397713ab67f5945d530ea7d1a0c12f34bf67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd538476f9a27c9d8c37d8873258f90248c9a8505badda3343259de579204035(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5f0c439e297bfecd869b2f2077c0277b9b01d41b9d81a73b7505bfa8e26bc6(
    value: typing.Optional[StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a56db6e6f116fef2ceeae847e3ad246356c6cc4679e6ce6f351c2d96b7fb2eff(
    *,
    locations: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ef173473549c4d0ef2b00428354287d5efc66d838e1467cc78e7345ce647ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__634b175f45af0aa54d350168e995bad72038ef505c75d6ea77a75fdff6449b6d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8ed11992a44f8b273456f4b6746f84545e9e7f133c90b3748e23ac7a8f4f4e(
    value: typing.Optional[StorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2759f5f3b251fd8db2c21f5964c3e426ca2d8bf105e6d2b77ac04030ce1065(
    *,
    bucket_id_regexes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e41a1b14f20d66c176662273089f983e405c37f347f576e747e6cac83650ced(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54f8dd78b0c54a52c9c3d0684cca33f7916f1fd14717dec619f4cb268165fac(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea61a828c6441e9f069dca405fceba242d9bed9dc65198a988fe3a62aa2a62c3(
    value: typing.Optional[StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__410d0c5adc154f88c851648d2cbbdcf316bd48bba1c6887e587485b65c096ef5(
    *,
    locations: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9877f7f3daa185d9af5624f7a4e966b048841bed835d35915dd7a5bcc4134cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e985d428f89925d16f73abe576aaa8ab7cdb7fccd3b5258b257a6646b08a98d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a06400e0b624b4b97f71f9f90f944f872c46c368a58b1d05ac3521f94974a9(
    value: typing.Optional[StorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27eedb70dbc11fc78d8ea3b578a2b9080d71a16c754c0223bbb8bc82e88e885e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9fe3c5faf006ba2410d28a08667f4777866e4b4ba18a89c8a35ddd3ee8dd329(
    value: typing.Optional[StorageControlOrganizationIntelligenceConfigFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1989c78575a81bca0a97ab4c6ae1f0acd73f3ffea89ff5f3ae6b059d2761e7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a9ad1f789519d1ed3ad2f4c24f4ccfef61b416bef8fe1deeec5afb114d6d0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5382da55e18b6faa716a77543bb8eab0de86a908afb6cae4f9facf0b305f95b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28fde97036a3c3ef456000bf335993ae68386ec910577b70ace13ff087f199d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a600812f41da48799b01827c3ebd2bb25ae8922adbe49374ee23c48caf6e8e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cddd05e6240cef293f47476cc1d05ca82c70db8fae74afb0f545c3cd965d1ef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageControlOrganizationIntelligenceConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86b9971492411ac288ffe5842754aff61f2c4dfc7df060fcdacf550bfa9e422(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7343ea69cacc99f2ceb67662934297c1b4f32fe84f4954fc922791f07c08f950(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d24626611f5538fdb9ee5ffacd1ab4b2d232fac6efa9e69b4e953ad7a3a5ec6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__628a09c61e6adb84871fb19b21273e6fc19775d9ed0813974ac06d29afe804fc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e64f321ea38e48935cd2aacee9ee5494d892ebf58281070c485da0f2790a89(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80588fe44cd1806b09f7273b489b98b259e307b1f823efe4c2efea6a6dd0ab3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea15e850138bdc6717e645d7ad13c412bd4cdfaff214f0d8a21fde6667c19ecd(
    value: typing.Optional[StorageControlOrganizationIntelligenceConfigTrialConfig],
) -> None:
    """Type checking stubs"""
    pass

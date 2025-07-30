r'''
# `google_storage_insights_dataset_config`

Refer to the Terraform Registry for docs: [`google_storage_insights_dataset_config`](https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config).
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


class StorageInsightsDatasetConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config google_storage_insights_dataset_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dataset_config_id: builtins.str,
        identity: typing.Union["StorageInsightsDatasetConfigIdentity", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        retention_period_days: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        exclude_cloud_storage_buckets: typing.Optional[typing.Union["StorageInsightsDatasetConfigExcludeCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_cloud_storage_locations: typing.Optional[typing.Union["StorageInsightsDatasetConfigExcludeCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        include_cloud_storage_buckets: typing.Optional[typing.Union["StorageInsightsDatasetConfigIncludeCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        include_cloud_storage_locations: typing.Optional[typing.Union["StorageInsightsDatasetConfigIncludeCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        include_newly_created_buckets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        link_dataset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        organization_number: typing.Optional[builtins.str] = None,
        organization_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        source_folders: typing.Optional[typing.Union["StorageInsightsDatasetConfigSourceFolders", typing.Dict[builtins.str, typing.Any]]] = None,
        source_projects: typing.Optional[typing.Union["StorageInsightsDatasetConfigSourceProjects", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["StorageInsightsDatasetConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config google_storage_insights_dataset_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dataset_config_id: The user-defined ID of the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#dataset_config_id StorageInsightsDatasetConfig#dataset_config_id}
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#identity StorageInsightsDatasetConfig#identity}
        :param location: The location of the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#location StorageInsightsDatasetConfig#location}
        :param retention_period_days: Number of days of history that must be retained. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#retention_period_days StorageInsightsDatasetConfig#retention_period_days}
        :param description: An optional user-provided description for the dataset configuration with a maximum length of 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#description StorageInsightsDatasetConfig#description}
        :param exclude_cloud_storage_buckets: exclude_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#exclude_cloud_storage_buckets StorageInsightsDatasetConfig#exclude_cloud_storage_buckets}
        :param exclude_cloud_storage_locations: exclude_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#exclude_cloud_storage_locations StorageInsightsDatasetConfig#exclude_cloud_storage_locations}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#id StorageInsightsDatasetConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_cloud_storage_buckets: include_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#include_cloud_storage_buckets StorageInsightsDatasetConfig#include_cloud_storage_buckets}
        :param include_cloud_storage_locations: include_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#include_cloud_storage_locations StorageInsightsDatasetConfig#include_cloud_storage_locations}
        :param include_newly_created_buckets: If set to true, the request includes all the newly created buckets in the dataset that meet the inclusion and exclusion rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#include_newly_created_buckets StorageInsightsDatasetConfig#include_newly_created_buckets}
        :param link_dataset: A boolean terraform only flag to link/unlink dataset. Setting this field to true while creation will automatically link the created dataset as an additional functionality. -> **Note** A dataset config resource can only be destroyed once it is unlinked, so users must set this field to false to unlink the dataset and destroy the dataset config resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#link_dataset StorageInsightsDatasetConfig#link_dataset}
        :param organization_number: Organization resource ID that the source projects should belong to. Projects that do not belong to the provided organization are not considered when creating the dataset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#organization_number StorageInsightsDatasetConfig#organization_number}
        :param organization_scope: Defines the options for providing a source organization for the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#organization_scope StorageInsightsDatasetConfig#organization_scope}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#project StorageInsightsDatasetConfig#project}.
        :param source_folders: source_folders block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#source_folders StorageInsightsDatasetConfig#source_folders}
        :param source_projects: source_projects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#source_projects StorageInsightsDatasetConfig#source_projects}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#timeouts StorageInsightsDatasetConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee2219e5370b3f000996248d1df311d65018b20c9a68aaeb27cc0b2102e7b00)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StorageInsightsDatasetConfigConfig(
            dataset_config_id=dataset_config_id,
            identity=identity,
            location=location,
            retention_period_days=retention_period_days,
            description=description,
            exclude_cloud_storage_buckets=exclude_cloud_storage_buckets,
            exclude_cloud_storage_locations=exclude_cloud_storage_locations,
            id=id,
            include_cloud_storage_buckets=include_cloud_storage_buckets,
            include_cloud_storage_locations=include_cloud_storage_locations,
            include_newly_created_buckets=include_newly_created_buckets,
            link_dataset=link_dataset,
            organization_number=organization_number,
            organization_scope=organization_scope,
            project=project,
            source_folders=source_folders,
            source_projects=source_projects,
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
        '''Generates CDKTF code for importing a StorageInsightsDatasetConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StorageInsightsDatasetConfig to import.
        :param import_from_id: The id of the existing StorageInsightsDatasetConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StorageInsightsDatasetConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2f231f8fd4ac1fed39a534bb0fe31adaf1d73d098d5dcc073fae9865e79edd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putExcludeCloudStorageBuckets")
    def put_exclude_cloud_storage_buckets(
        self,
        *,
        cloud_storage_buckets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param cloud_storage_buckets: cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#cloud_storage_buckets StorageInsightsDatasetConfig#cloud_storage_buckets}
        '''
        value = StorageInsightsDatasetConfigExcludeCloudStorageBuckets(
            cloud_storage_buckets=cloud_storage_buckets
        )

        return typing.cast(None, jsii.invoke(self, "putExcludeCloudStorageBuckets", [value]))

    @jsii.member(jsii_name="putExcludeCloudStorageLocations")
    def put_exclude_cloud_storage_locations(
        self,
        *,
        locations: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param locations: The list of cloud storage locations to exclude in the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#locations StorageInsightsDatasetConfig#locations}
        '''
        value = StorageInsightsDatasetConfigExcludeCloudStorageLocations(
            locations=locations
        )

        return typing.cast(None, jsii.invoke(self, "putExcludeCloudStorageLocations", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(self, *, type: builtins.str) -> None:
        '''
        :param type: Type of identity to use for the DatasetConfig. Possible values: ["IDENTITY_TYPE_PER_CONFIG", "IDENTITY_TYPE_PER_PROJECT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#type StorageInsightsDatasetConfig#type}
        '''
        value = StorageInsightsDatasetConfigIdentity(type=type)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putIncludeCloudStorageBuckets")
    def put_include_cloud_storage_buckets(
        self,
        *,
        cloud_storage_buckets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param cloud_storage_buckets: cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#cloud_storage_buckets StorageInsightsDatasetConfig#cloud_storage_buckets}
        '''
        value = StorageInsightsDatasetConfigIncludeCloudStorageBuckets(
            cloud_storage_buckets=cloud_storage_buckets
        )

        return typing.cast(None, jsii.invoke(self, "putIncludeCloudStorageBuckets", [value]))

    @jsii.member(jsii_name="putIncludeCloudStorageLocations")
    def put_include_cloud_storage_locations(
        self,
        *,
        locations: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param locations: The list of cloud storage locations to include in the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#locations StorageInsightsDatasetConfig#locations}
        '''
        value = StorageInsightsDatasetConfigIncludeCloudStorageLocations(
            locations=locations
        )

        return typing.cast(None, jsii.invoke(self, "putIncludeCloudStorageLocations", [value]))

    @jsii.member(jsii_name="putSourceFolders")
    def put_source_folders(
        self,
        *,
        folder_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param folder_numbers: The list of folder numbers to include in the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#folder_numbers StorageInsightsDatasetConfig#folder_numbers}
        '''
        value = StorageInsightsDatasetConfigSourceFolders(
            folder_numbers=folder_numbers
        )

        return typing.cast(None, jsii.invoke(self, "putSourceFolders", [value]))

    @jsii.member(jsii_name="putSourceProjects")
    def put_source_projects(
        self,
        *,
        project_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param project_numbers: The list of project numbers to include in the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#project_numbers StorageInsightsDatasetConfig#project_numbers}
        '''
        value = StorageInsightsDatasetConfigSourceProjects(
            project_numbers=project_numbers
        )

        return typing.cast(None, jsii.invoke(self, "putSourceProjects", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#create StorageInsightsDatasetConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#delete StorageInsightsDatasetConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#update StorageInsightsDatasetConfig#update}.
        '''
        value = StorageInsightsDatasetConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExcludeCloudStorageBuckets")
    def reset_exclude_cloud_storage_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeCloudStorageBuckets", []))

    @jsii.member(jsii_name="resetExcludeCloudStorageLocations")
    def reset_exclude_cloud_storage_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeCloudStorageLocations", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncludeCloudStorageBuckets")
    def reset_include_cloud_storage_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeCloudStorageBuckets", []))

    @jsii.member(jsii_name="resetIncludeCloudStorageLocations")
    def reset_include_cloud_storage_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeCloudStorageLocations", []))

    @jsii.member(jsii_name="resetIncludeNewlyCreatedBuckets")
    def reset_include_newly_created_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeNewlyCreatedBuckets", []))

    @jsii.member(jsii_name="resetLinkDataset")
    def reset_link_dataset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinkDataset", []))

    @jsii.member(jsii_name="resetOrganizationNumber")
    def reset_organization_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationNumber", []))

    @jsii.member(jsii_name="resetOrganizationScope")
    def reset_organization_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationScope", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSourceFolders")
    def reset_source_folders(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFolders", []))

    @jsii.member(jsii_name="resetSourceProjects")
    def reset_source_projects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceProjects", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="datasetConfigState")
    def dataset_config_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetConfigState"))

    @builtins.property
    @jsii.member(jsii_name="excludeCloudStorageBuckets")
    def exclude_cloud_storage_buckets(
        self,
    ) -> "StorageInsightsDatasetConfigExcludeCloudStorageBucketsOutputReference":
        return typing.cast("StorageInsightsDatasetConfigExcludeCloudStorageBucketsOutputReference", jsii.get(self, "excludeCloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="excludeCloudStorageLocations")
    def exclude_cloud_storage_locations(
        self,
    ) -> "StorageInsightsDatasetConfigExcludeCloudStorageLocationsOutputReference":
        return typing.cast("StorageInsightsDatasetConfigExcludeCloudStorageLocationsOutputReference", jsii.get(self, "excludeCloudStorageLocations"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "StorageInsightsDatasetConfigIdentityOutputReference":
        return typing.cast("StorageInsightsDatasetConfigIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="includeCloudStorageBuckets")
    def include_cloud_storage_buckets(
        self,
    ) -> "StorageInsightsDatasetConfigIncludeCloudStorageBucketsOutputReference":
        return typing.cast("StorageInsightsDatasetConfigIncludeCloudStorageBucketsOutputReference", jsii.get(self, "includeCloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="includeCloudStorageLocations")
    def include_cloud_storage_locations(
        self,
    ) -> "StorageInsightsDatasetConfigIncludeCloudStorageLocationsOutputReference":
        return typing.cast("StorageInsightsDatasetConfigIncludeCloudStorageLocationsOutputReference", jsii.get(self, "includeCloudStorageLocations"))

    @builtins.property
    @jsii.member(jsii_name="link")
    def link(self) -> "StorageInsightsDatasetConfigLinkList":
        return typing.cast("StorageInsightsDatasetConfigLinkList", jsii.get(self, "link"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="sourceFolders")
    def source_folders(
        self,
    ) -> "StorageInsightsDatasetConfigSourceFoldersOutputReference":
        return typing.cast("StorageInsightsDatasetConfigSourceFoldersOutputReference", jsii.get(self, "sourceFolders"))

    @builtins.property
    @jsii.member(jsii_name="sourceProjects")
    def source_projects(
        self,
    ) -> "StorageInsightsDatasetConfigSourceProjectsOutputReference":
        return typing.cast("StorageInsightsDatasetConfigSourceProjectsOutputReference", jsii.get(self, "sourceProjects"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "StorageInsightsDatasetConfigTimeoutsOutputReference":
        return typing.cast("StorageInsightsDatasetConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="datasetConfigIdInput")
    def dataset_config_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetConfigIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeCloudStorageBucketsInput")
    def exclude_cloud_storage_buckets_input(
        self,
    ) -> typing.Optional["StorageInsightsDatasetConfigExcludeCloudStorageBuckets"]:
        return typing.cast(typing.Optional["StorageInsightsDatasetConfigExcludeCloudStorageBuckets"], jsii.get(self, "excludeCloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeCloudStorageLocationsInput")
    def exclude_cloud_storage_locations_input(
        self,
    ) -> typing.Optional["StorageInsightsDatasetConfigExcludeCloudStorageLocations"]:
        return typing.cast(typing.Optional["StorageInsightsDatasetConfigExcludeCloudStorageLocations"], jsii.get(self, "excludeCloudStorageLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["StorageInsightsDatasetConfigIdentity"]:
        return typing.cast(typing.Optional["StorageInsightsDatasetConfigIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeCloudStorageBucketsInput")
    def include_cloud_storage_buckets_input(
        self,
    ) -> typing.Optional["StorageInsightsDatasetConfigIncludeCloudStorageBuckets"]:
        return typing.cast(typing.Optional["StorageInsightsDatasetConfigIncludeCloudStorageBuckets"], jsii.get(self, "includeCloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeCloudStorageLocationsInput")
    def include_cloud_storage_locations_input(
        self,
    ) -> typing.Optional["StorageInsightsDatasetConfigIncludeCloudStorageLocations"]:
        return typing.cast(typing.Optional["StorageInsightsDatasetConfigIncludeCloudStorageLocations"], jsii.get(self, "includeCloudStorageLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeNewlyCreatedBucketsInput")
    def include_newly_created_buckets_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeNewlyCreatedBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="linkDatasetInput")
    def link_dataset_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "linkDatasetInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationNumberInput")
    def organization_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationScopeInput")
    def organization_scope_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "organizationScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodDaysInput")
    def retention_period_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPeriodDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFoldersInput")
    def source_folders_input(
        self,
    ) -> typing.Optional["StorageInsightsDatasetConfigSourceFolders"]:
        return typing.cast(typing.Optional["StorageInsightsDatasetConfigSourceFolders"], jsii.get(self, "sourceFoldersInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceProjectsInput")
    def source_projects_input(
        self,
    ) -> typing.Optional["StorageInsightsDatasetConfigSourceProjects"]:
        return typing.cast(typing.Optional["StorageInsightsDatasetConfigSourceProjects"], jsii.get(self, "sourceProjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageInsightsDatasetConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageInsightsDatasetConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetConfigId")
    def dataset_config_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetConfigId"))

    @dataset_config_id.setter
    def dataset_config_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82dd1335bd1bf6b2ed22d02a141891cfeed66121d0d83dfae4650e35838a04de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetConfigId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a55fab7709e9ba6354e297c814427a3edd7bfd1c1dbc7c295959d366b3087bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de4d58f4306ae44f78b807fd42f7b9f9225939874bc75b1a0f01d100dc2d281c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeNewlyCreatedBuckets")
    def include_newly_created_buckets(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeNewlyCreatedBuckets"))

    @include_newly_created_buckets.setter
    def include_newly_created_buckets(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68349938cc5e18223d0f16fb32226647880d718922465470eca2ac25b712c673)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeNewlyCreatedBuckets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linkDataset")
    def link_dataset(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "linkDataset"))

    @link_dataset.setter
    def link_dataset(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f58090bc5bae01f180e4056f35bea800a8e86e8d841665928a306e8cc083923a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkDataset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ea1076e8f863f45585ca9e5c2e2806e3b198ee65ab3da78d4481879d70cdd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationNumber")
    def organization_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationNumber"))

    @organization_number.setter
    def organization_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1248a0b16f5057225d9867763bb3e9780977ec264420eefba08365eae2977aef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationScope")
    def organization_scope(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "organizationScope"))

    @organization_scope.setter
    def organization_scope(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dac95f9a2ebd45b079c4304a021488f2dbca5c9b45a9dcea600db0fbbaf15ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f60465146d010ddb80b83348d27879e28c6bda48c66e41cab2836ae559bf59c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodDays")
    def retention_period_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPeriodDays"))

    @retention_period_days.setter
    def retention_period_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a108eacc15ffd1da62efe28e651d91dccfec7ae83a28b48add5ead4078cc1d2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriodDays", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dataset_config_id": "datasetConfigId",
        "identity": "identity",
        "location": "location",
        "retention_period_days": "retentionPeriodDays",
        "description": "description",
        "exclude_cloud_storage_buckets": "excludeCloudStorageBuckets",
        "exclude_cloud_storage_locations": "excludeCloudStorageLocations",
        "id": "id",
        "include_cloud_storage_buckets": "includeCloudStorageBuckets",
        "include_cloud_storage_locations": "includeCloudStorageLocations",
        "include_newly_created_buckets": "includeNewlyCreatedBuckets",
        "link_dataset": "linkDataset",
        "organization_number": "organizationNumber",
        "organization_scope": "organizationScope",
        "project": "project",
        "source_folders": "sourceFolders",
        "source_projects": "sourceProjects",
        "timeouts": "timeouts",
    },
)
class StorageInsightsDatasetConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dataset_config_id: builtins.str,
        identity: typing.Union["StorageInsightsDatasetConfigIdentity", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        retention_period_days: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        exclude_cloud_storage_buckets: typing.Optional[typing.Union["StorageInsightsDatasetConfigExcludeCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_cloud_storage_locations: typing.Optional[typing.Union["StorageInsightsDatasetConfigExcludeCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        include_cloud_storage_buckets: typing.Optional[typing.Union["StorageInsightsDatasetConfigIncludeCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        include_cloud_storage_locations: typing.Optional[typing.Union["StorageInsightsDatasetConfigIncludeCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        include_newly_created_buckets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        link_dataset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        organization_number: typing.Optional[builtins.str] = None,
        organization_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        source_folders: typing.Optional[typing.Union["StorageInsightsDatasetConfigSourceFolders", typing.Dict[builtins.str, typing.Any]]] = None,
        source_projects: typing.Optional[typing.Union["StorageInsightsDatasetConfigSourceProjects", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["StorageInsightsDatasetConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dataset_config_id: The user-defined ID of the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#dataset_config_id StorageInsightsDatasetConfig#dataset_config_id}
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#identity StorageInsightsDatasetConfig#identity}
        :param location: The location of the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#location StorageInsightsDatasetConfig#location}
        :param retention_period_days: Number of days of history that must be retained. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#retention_period_days StorageInsightsDatasetConfig#retention_period_days}
        :param description: An optional user-provided description for the dataset configuration with a maximum length of 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#description StorageInsightsDatasetConfig#description}
        :param exclude_cloud_storage_buckets: exclude_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#exclude_cloud_storage_buckets StorageInsightsDatasetConfig#exclude_cloud_storage_buckets}
        :param exclude_cloud_storage_locations: exclude_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#exclude_cloud_storage_locations StorageInsightsDatasetConfig#exclude_cloud_storage_locations}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#id StorageInsightsDatasetConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_cloud_storage_buckets: include_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#include_cloud_storage_buckets StorageInsightsDatasetConfig#include_cloud_storage_buckets}
        :param include_cloud_storage_locations: include_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#include_cloud_storage_locations StorageInsightsDatasetConfig#include_cloud_storage_locations}
        :param include_newly_created_buckets: If set to true, the request includes all the newly created buckets in the dataset that meet the inclusion and exclusion rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#include_newly_created_buckets StorageInsightsDatasetConfig#include_newly_created_buckets}
        :param link_dataset: A boolean terraform only flag to link/unlink dataset. Setting this field to true while creation will automatically link the created dataset as an additional functionality. -> **Note** A dataset config resource can only be destroyed once it is unlinked, so users must set this field to false to unlink the dataset and destroy the dataset config resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#link_dataset StorageInsightsDatasetConfig#link_dataset}
        :param organization_number: Organization resource ID that the source projects should belong to. Projects that do not belong to the provided organization are not considered when creating the dataset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#organization_number StorageInsightsDatasetConfig#organization_number}
        :param organization_scope: Defines the options for providing a source organization for the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#organization_scope StorageInsightsDatasetConfig#organization_scope}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#project StorageInsightsDatasetConfig#project}.
        :param source_folders: source_folders block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#source_folders StorageInsightsDatasetConfig#source_folders}
        :param source_projects: source_projects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#source_projects StorageInsightsDatasetConfig#source_projects}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#timeouts StorageInsightsDatasetConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(identity, dict):
            identity = StorageInsightsDatasetConfigIdentity(**identity)
        if isinstance(exclude_cloud_storage_buckets, dict):
            exclude_cloud_storage_buckets = StorageInsightsDatasetConfigExcludeCloudStorageBuckets(**exclude_cloud_storage_buckets)
        if isinstance(exclude_cloud_storage_locations, dict):
            exclude_cloud_storage_locations = StorageInsightsDatasetConfigExcludeCloudStorageLocations(**exclude_cloud_storage_locations)
        if isinstance(include_cloud_storage_buckets, dict):
            include_cloud_storage_buckets = StorageInsightsDatasetConfigIncludeCloudStorageBuckets(**include_cloud_storage_buckets)
        if isinstance(include_cloud_storage_locations, dict):
            include_cloud_storage_locations = StorageInsightsDatasetConfigIncludeCloudStorageLocations(**include_cloud_storage_locations)
        if isinstance(source_folders, dict):
            source_folders = StorageInsightsDatasetConfigSourceFolders(**source_folders)
        if isinstance(source_projects, dict):
            source_projects = StorageInsightsDatasetConfigSourceProjects(**source_projects)
        if isinstance(timeouts, dict):
            timeouts = StorageInsightsDatasetConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__882f56583fdca1c45472b260748a76a0d1018a32bf4800c931899eb382b1ecb5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dataset_config_id", value=dataset_config_id, expected_type=type_hints["dataset_config_id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument retention_period_days", value=retention_period_days, expected_type=type_hints["retention_period_days"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument exclude_cloud_storage_buckets", value=exclude_cloud_storage_buckets, expected_type=type_hints["exclude_cloud_storage_buckets"])
            check_type(argname="argument exclude_cloud_storage_locations", value=exclude_cloud_storage_locations, expected_type=type_hints["exclude_cloud_storage_locations"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument include_cloud_storage_buckets", value=include_cloud_storage_buckets, expected_type=type_hints["include_cloud_storage_buckets"])
            check_type(argname="argument include_cloud_storage_locations", value=include_cloud_storage_locations, expected_type=type_hints["include_cloud_storage_locations"])
            check_type(argname="argument include_newly_created_buckets", value=include_newly_created_buckets, expected_type=type_hints["include_newly_created_buckets"])
            check_type(argname="argument link_dataset", value=link_dataset, expected_type=type_hints["link_dataset"])
            check_type(argname="argument organization_number", value=organization_number, expected_type=type_hints["organization_number"])
            check_type(argname="argument organization_scope", value=organization_scope, expected_type=type_hints["organization_scope"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument source_folders", value=source_folders, expected_type=type_hints["source_folders"])
            check_type(argname="argument source_projects", value=source_projects, expected_type=type_hints["source_projects"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_config_id": dataset_config_id,
            "identity": identity,
            "location": location,
            "retention_period_days": retention_period_days,
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
        if exclude_cloud_storage_buckets is not None:
            self._values["exclude_cloud_storage_buckets"] = exclude_cloud_storage_buckets
        if exclude_cloud_storage_locations is not None:
            self._values["exclude_cloud_storage_locations"] = exclude_cloud_storage_locations
        if id is not None:
            self._values["id"] = id
        if include_cloud_storage_buckets is not None:
            self._values["include_cloud_storage_buckets"] = include_cloud_storage_buckets
        if include_cloud_storage_locations is not None:
            self._values["include_cloud_storage_locations"] = include_cloud_storage_locations
        if include_newly_created_buckets is not None:
            self._values["include_newly_created_buckets"] = include_newly_created_buckets
        if link_dataset is not None:
            self._values["link_dataset"] = link_dataset
        if organization_number is not None:
            self._values["organization_number"] = organization_number
        if organization_scope is not None:
            self._values["organization_scope"] = organization_scope
        if project is not None:
            self._values["project"] = project
        if source_folders is not None:
            self._values["source_folders"] = source_folders
        if source_projects is not None:
            self._values["source_projects"] = source_projects
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
    def dataset_config_id(self) -> builtins.str:
        '''The user-defined ID of the DatasetConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#dataset_config_id StorageInsightsDatasetConfig#dataset_config_id}
        '''
        result = self._values.get("dataset_config_id")
        assert result is not None, "Required property 'dataset_config_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity(self) -> "StorageInsightsDatasetConfigIdentity":
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#identity StorageInsightsDatasetConfig#identity}
        '''
        result = self._values.get("identity")
        assert result is not None, "Required property 'identity' is missing"
        return typing.cast("StorageInsightsDatasetConfigIdentity", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the DatasetConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#location StorageInsightsDatasetConfig#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_period_days(self) -> jsii.Number:
        '''Number of days of history that must be retained.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#retention_period_days StorageInsightsDatasetConfig#retention_period_days}
        '''
        result = self._values.get("retention_period_days")
        assert result is not None, "Required property 'retention_period_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional user-provided description for the dataset configuration with a maximum length of 256 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#description StorageInsightsDatasetConfig#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude_cloud_storage_buckets(
        self,
    ) -> typing.Optional["StorageInsightsDatasetConfigExcludeCloudStorageBuckets"]:
        '''exclude_cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#exclude_cloud_storage_buckets StorageInsightsDatasetConfig#exclude_cloud_storage_buckets}
        '''
        result = self._values.get("exclude_cloud_storage_buckets")
        return typing.cast(typing.Optional["StorageInsightsDatasetConfigExcludeCloudStorageBuckets"], result)

    @builtins.property
    def exclude_cloud_storage_locations(
        self,
    ) -> typing.Optional["StorageInsightsDatasetConfigExcludeCloudStorageLocations"]:
        '''exclude_cloud_storage_locations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#exclude_cloud_storage_locations StorageInsightsDatasetConfig#exclude_cloud_storage_locations}
        '''
        result = self._values.get("exclude_cloud_storage_locations")
        return typing.cast(typing.Optional["StorageInsightsDatasetConfigExcludeCloudStorageLocations"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#id StorageInsightsDatasetConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_cloud_storage_buckets(
        self,
    ) -> typing.Optional["StorageInsightsDatasetConfigIncludeCloudStorageBuckets"]:
        '''include_cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#include_cloud_storage_buckets StorageInsightsDatasetConfig#include_cloud_storage_buckets}
        '''
        result = self._values.get("include_cloud_storage_buckets")
        return typing.cast(typing.Optional["StorageInsightsDatasetConfigIncludeCloudStorageBuckets"], result)

    @builtins.property
    def include_cloud_storage_locations(
        self,
    ) -> typing.Optional["StorageInsightsDatasetConfigIncludeCloudStorageLocations"]:
        '''include_cloud_storage_locations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#include_cloud_storage_locations StorageInsightsDatasetConfig#include_cloud_storage_locations}
        '''
        result = self._values.get("include_cloud_storage_locations")
        return typing.cast(typing.Optional["StorageInsightsDatasetConfigIncludeCloudStorageLocations"], result)

    @builtins.property
    def include_newly_created_buckets(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the request includes all the newly created buckets in the dataset that meet the inclusion and exclusion rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#include_newly_created_buckets StorageInsightsDatasetConfig#include_newly_created_buckets}
        '''
        result = self._values.get("include_newly_created_buckets")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def link_dataset(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean terraform only flag to link/unlink dataset.

        Setting this field to true while creation will automatically link the created dataset as an additional functionality.
        -> **Note** A dataset config resource can only be destroyed once it is unlinked,
        so users must set this field to false to unlink the dataset and destroy the dataset config resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#link_dataset StorageInsightsDatasetConfig#link_dataset}
        '''
        result = self._values.get("link_dataset")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def organization_number(self) -> typing.Optional[builtins.str]:
        '''Organization resource ID that the source projects should belong to.

        Projects that do not belong to the provided organization are not considered when creating the dataset.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#organization_number StorageInsightsDatasetConfig#organization_number}
        '''
        result = self._values.get("organization_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization_scope(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines the options for providing a source organization for the DatasetConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#organization_scope StorageInsightsDatasetConfig#organization_scope}
        '''
        result = self._values.get("organization_scope")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#project StorageInsightsDatasetConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_folders(
        self,
    ) -> typing.Optional["StorageInsightsDatasetConfigSourceFolders"]:
        '''source_folders block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#source_folders StorageInsightsDatasetConfig#source_folders}
        '''
        result = self._values.get("source_folders")
        return typing.cast(typing.Optional["StorageInsightsDatasetConfigSourceFolders"], result)

    @builtins.property
    def source_projects(
        self,
    ) -> typing.Optional["StorageInsightsDatasetConfigSourceProjects"]:
        '''source_projects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#source_projects StorageInsightsDatasetConfig#source_projects}
        '''
        result = self._values.get("source_projects")
        return typing.cast(typing.Optional["StorageInsightsDatasetConfigSourceProjects"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["StorageInsightsDatasetConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#timeouts StorageInsightsDatasetConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["StorageInsightsDatasetConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsDatasetConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigExcludeCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={"cloud_storage_buckets": "cloudStorageBuckets"},
)
class StorageInsightsDatasetConfigExcludeCloudStorageBuckets:
    def __init__(
        self,
        *,
        cloud_storage_buckets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param cloud_storage_buckets: cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#cloud_storage_buckets StorageInsightsDatasetConfig#cloud_storage_buckets}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4225bd9520c86647c68f0bdd5f3f77a2742b5906cb2a1afe3bfb514b33e7ec35)
            check_type(argname="argument cloud_storage_buckets", value=cloud_storage_buckets, expected_type=type_hints["cloud_storage_buckets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_storage_buckets": cloud_storage_buckets,
        }

    @builtins.property
    def cloud_storage_buckets(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets"]]:
        '''cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#cloud_storage_buckets StorageInsightsDatasetConfig#cloud_storage_buckets}
        '''
        result = self._values.get("cloud_storage_buckets")
        assert result is not None, "Required property 'cloud_storage_buckets' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsDatasetConfigExcludeCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix_regex": "bucketPrefixRegex",
    },
)
class StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: The list of cloud storage bucket names to exclude in the DatasetConfig. Exactly one of the bucket_name and bucket_prefix_regex should be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#bucket_name StorageInsightsDatasetConfig#bucket_name}
        :param bucket_prefix_regex: The list of regex patterns for bucket names matching the regex. Regex should follow the syntax specified in google/re2 on GitHub. Exactly one of the bucket_name and bucket_prefix_regex should be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#bucket_prefix_regex StorageInsightsDatasetConfig#bucket_prefix_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bfa56324644ca0510e45e5f327746d8d3d8ce72753227e42193e22615d02907)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix_regex", value=bucket_prefix_regex, expected_type=type_hints["bucket_prefix_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix_regex is not None:
            self._values["bucket_prefix_regex"] = bucket_prefix_regex

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''The list of cloud storage bucket names to exclude in the DatasetConfig.

        Exactly one of the bucket_name and bucket_prefix_regex should be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#bucket_name StorageInsightsDatasetConfig#bucket_name}
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix_regex(self) -> typing.Optional[builtins.str]:
        '''The list of regex patterns for bucket names matching the regex.

        Regex should follow the syntax specified in google/re2 on GitHub.
        Exactly one of the bucket_name and bucket_prefix_regex should be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#bucket_prefix_regex StorageInsightsDatasetConfig#bucket_prefix_regex}
        '''
        result = self._values.get("bucket_prefix_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__caa68027b6d2b2aed89dccd191480f1c0f2038de5a94f4251f2df121c507891e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac2cb054fc723eca8e9e33e8ec825af434af50c553a5c70d25fd6a72f50f96e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a35c07e6d24da57567e28ec031119874aeb2291378d47d5caba8a42763aed4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eda83c20f8f8656cb2e1846c5862cde48056d146a95b68c4acdcc119bfe293e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__254dc4defeebcf3b2882ad6b5ee7a7788eb470cf027a3387d231aabff552e020)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8150dc3c0b5c8e1b12815a977c52c7d3975c47de1cf5e614a424d6633d22af26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5978d3b16ab079601260cbae46475d8f801b71de52aa64e7bbb0c90db3d50767)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefixRegex")
    def reset_bucket_prefix_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefixRegex", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixRegexInput")
    def bucket_prefix_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53faa208e6900e9ee44db120cfd3fc519dcf409373894855796c2c4c3b12d6e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixRegex")
    def bucket_prefix_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefixRegex"))

    @bucket_prefix_regex.setter
    def bucket_prefix_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e55b73c104f325f0c8648e56e6388d5f78562a45650faf3f3186a80118a759)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefixRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a94a53bb4e0e68fb988d0fcf5aadb04e746036c1c38fab39f1861e5886554a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageInsightsDatasetConfigExcludeCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigExcludeCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8711d0a21110f2c082f57e9c8c2807e1fe0decd5cb1f1bf59767a787b4387fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudStorageBuckets")
    def put_cloud_storage_buckets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68dd83931a5a609dc17c51dbd652c8008ad05c62220ca7f4ad1ec41e6f1268e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCloudStorageBuckets", [value]))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageBuckets")
    def cloud_storage_buckets(
        self,
    ) -> StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsList:
        return typing.cast(StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsList, jsii.get(self, "cloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageBucketsInput")
    def cloud_storage_buckets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]]], jsii.get(self, "cloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageInsightsDatasetConfigExcludeCloudStorageBuckets]:
        return typing.cast(typing.Optional[StorageInsightsDatasetConfigExcludeCloudStorageBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageInsightsDatasetConfigExcludeCloudStorageBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fd5361a644940a7e65eb0e63149da780e763834defe164e4d185f8932422bd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigExcludeCloudStorageLocations",
    jsii_struct_bases=[],
    name_mapping={"locations": "locations"},
)
class StorageInsightsDatasetConfigExcludeCloudStorageLocations:
    def __init__(self, *, locations: typing.Sequence[builtins.str]) -> None:
        '''
        :param locations: The list of cloud storage locations to exclude in the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#locations StorageInsightsDatasetConfig#locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78d7935df1add3649894a7ef62ff07b4e47eb1003cff5e6d5f005f9301448617)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locations": locations,
        }

    @builtins.property
    def locations(self) -> typing.List[builtins.str]:
        '''The list of cloud storage locations to exclude in the DatasetConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#locations StorageInsightsDatasetConfig#locations}
        '''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsDatasetConfigExcludeCloudStorageLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageInsightsDatasetConfigExcludeCloudStorageLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigExcludeCloudStorageLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcbca59d4d57c1490906a4342c77df4229d066e547863c197d3c4a6dc5fb7214)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d0f8fb8a12e7f5ab133f5ace3507d1f3402d56faa9070300703358ffa5b8953)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageInsightsDatasetConfigExcludeCloudStorageLocations]:
        return typing.cast(typing.Optional[StorageInsightsDatasetConfigExcludeCloudStorageLocations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageInsightsDatasetConfigExcludeCloudStorageLocations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d6c26e5d239023fe49f92cbf39223c12e36639a5ac9a4a3e4eec33ab3b79a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class StorageInsightsDatasetConfigIdentity:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Type of identity to use for the DatasetConfig. Possible values: ["IDENTITY_TYPE_PER_CONFIG", "IDENTITY_TYPE_PER_PROJECT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#type StorageInsightsDatasetConfig#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c06bd4b39f71086b7888b4b6b04f18ad82ccadd1a2ac79d0fdc68dd0701633)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of identity to use for the DatasetConfig. Possible values: ["IDENTITY_TYPE_PER_CONFIG", "IDENTITY_TYPE_PER_PROJECT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#type StorageInsightsDatasetConfig#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsDatasetConfigIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageInsightsDatasetConfigIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__173e839943ed488a040304f3b7554736ac43e8945676279ed716c1ee14978663)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2483ec667f1518b4ad0796a83e3b2b615f96efedbd58c9440111893e44b9c281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageInsightsDatasetConfigIdentity]:
        return typing.cast(typing.Optional[StorageInsightsDatasetConfigIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageInsightsDatasetConfigIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__017ccdec4ae8d8c332f640bc776a3fa199902db2ab5e9261063736de40f027a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigIncludeCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={"cloud_storage_buckets": "cloudStorageBuckets"},
)
class StorageInsightsDatasetConfigIncludeCloudStorageBuckets:
    def __init__(
        self,
        *,
        cloud_storage_buckets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param cloud_storage_buckets: cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#cloud_storage_buckets StorageInsightsDatasetConfig#cloud_storage_buckets}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1048c27191bc66f3e2cd289b435696bfe28b59c8cf93d9079de5009b1bd770b7)
            check_type(argname="argument cloud_storage_buckets", value=cloud_storage_buckets, expected_type=type_hints["cloud_storage_buckets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_storage_buckets": cloud_storage_buckets,
        }

    @builtins.property
    def cloud_storage_buckets(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets"]]:
        '''cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#cloud_storage_buckets StorageInsightsDatasetConfig#cloud_storage_buckets}
        '''
        result = self._values.get("cloud_storage_buckets")
        assert result is not None, "Required property 'cloud_storage_buckets' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsDatasetConfigIncludeCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix_regex": "bucketPrefixRegex",
    },
)
class StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: The list of cloud storage bucket names to include in the DatasetConfig. Exactly one of the bucket_name and bucket_prefix_regex should be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#bucket_name StorageInsightsDatasetConfig#bucket_name}
        :param bucket_prefix_regex: The list of regex patterns for bucket names matching the regex. Regex should follow the syntax specified in google/re2 on GitHub. Exactly one of the bucket_name and bucket_prefix_regex should be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#bucket_prefix_regex StorageInsightsDatasetConfig#bucket_prefix_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496153a8397cb5eb9aae6156d84d68e8eb0a9be677693b6bb9837f21dc5cbaef)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix_regex", value=bucket_prefix_regex, expected_type=type_hints["bucket_prefix_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix_regex is not None:
            self._values["bucket_prefix_regex"] = bucket_prefix_regex

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''The list of cloud storage bucket names to include in the DatasetConfig.

        Exactly one of the bucket_name and bucket_prefix_regex should be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#bucket_name StorageInsightsDatasetConfig#bucket_name}
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix_regex(self) -> typing.Optional[builtins.str]:
        '''The list of regex patterns for bucket names matching the regex.

        Regex should follow the syntax specified in google/re2 on GitHub.
        Exactly one of the bucket_name and bucket_prefix_regex should be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#bucket_prefix_regex StorageInsightsDatasetConfig#bucket_prefix_regex}
        '''
        result = self._values.get("bucket_prefix_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4de812c81791b40885b214ec4f19dbeeea2c37bee62643c71bbc9b255fea417)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e50f362f12940a5719ba0dfaed477a4d790da8bb265d0c9423d513d734b70ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf5f7e92427f645ab8e407a67ae62eea5b0dae4f70a6916833af9acc5c80f5c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e33d5c2d06cbae8a495292daa56b0c7bd5397faf9e6a27624c299e622e98db8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3739714faca6d835d3eed38f9a19438e5185665c83a82409453aefc12710e598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd40c975bc13d61dcfcb276a9470fcacd15e78f76c4c79aff8e193ff1fa2937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c23f785a24502a6c68c28d63a99c6a78b7c14237b9ec9125334d585fe72e63d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefixRegex")
    def reset_bucket_prefix_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefixRegex", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixRegexInput")
    def bucket_prefix_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__339290ee6cd361f274ea424b188714b191aa6d19271a1bc5a3e8606c3438fa82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixRegex")
    def bucket_prefix_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefixRegex"))

    @bucket_prefix_regex.setter
    def bucket_prefix_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf1895642c760e475191d786a29337b64078b83be2f4f32449d0ac9b748c7fcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefixRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19a65238f57fbd820a655e96b130c51d2d835ba70bfe5e00bc134e674370ce67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageInsightsDatasetConfigIncludeCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigIncludeCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a7f27b62b8e4670f4c4252964b0bcf5766dce51a88fd594ed9904044ac8ed34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudStorageBuckets")
    def put_cloud_storage_buckets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cb1231d565aa8247068f5ee522f40023830104e5dcdc4db63a1d399b3a4fce5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCloudStorageBuckets", [value]))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageBuckets")
    def cloud_storage_buckets(
        self,
    ) -> StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsList:
        return typing.cast(StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsList, jsii.get(self, "cloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageBucketsInput")
    def cloud_storage_buckets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]]], jsii.get(self, "cloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageInsightsDatasetConfigIncludeCloudStorageBuckets]:
        return typing.cast(typing.Optional[StorageInsightsDatasetConfigIncludeCloudStorageBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageInsightsDatasetConfigIncludeCloudStorageBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fd5b5e6da56b0cba1a9bd507a415484a05f98ec4be3a5ddf04236fca29562a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigIncludeCloudStorageLocations",
    jsii_struct_bases=[],
    name_mapping={"locations": "locations"},
)
class StorageInsightsDatasetConfigIncludeCloudStorageLocations:
    def __init__(self, *, locations: typing.Sequence[builtins.str]) -> None:
        '''
        :param locations: The list of cloud storage locations to include in the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#locations StorageInsightsDatasetConfig#locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b89eec1ebff63807a45128681bb14ef270ffb269c0dd5dc40eb381bf636c6e26)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locations": locations,
        }

    @builtins.property
    def locations(self) -> typing.List[builtins.str]:
        '''The list of cloud storage locations to include in the DatasetConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#locations StorageInsightsDatasetConfig#locations}
        '''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsDatasetConfigIncludeCloudStorageLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageInsightsDatasetConfigIncludeCloudStorageLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigIncludeCloudStorageLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fee8afa5cc36b108b9beea254db8f12ec8b48fe9c8e0192b9deebca59f6142a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82f1bc02881223035fefbe6a489a39ef9bd89a4911a0a54c418452db5b571ab6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageInsightsDatasetConfigIncludeCloudStorageLocations]:
        return typing.cast(typing.Optional[StorageInsightsDatasetConfigIncludeCloudStorageLocations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageInsightsDatasetConfigIncludeCloudStorageLocations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a97468cad2c50c50766b683ef4efda5aede80f0cd8d635763bcceaf1d278a7fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigLink",
    jsii_struct_bases=[],
    name_mapping={},
)
class StorageInsightsDatasetConfigLink:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsDatasetConfigLink(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageInsightsDatasetConfigLinkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigLinkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6570ce2cd6ddaf39147d5337e00317e1e453af3fc1d1762aea6f72b795beb55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StorageInsightsDatasetConfigLinkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a32840af9a01b808df31abe0d813cf471337dee90f0bed7452d3bceb562633)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageInsightsDatasetConfigLinkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e1b759d39c7b75caf8bb072c8fc3fa036606bebf1e8d22a379e6bcec0d8c7ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffefbd6e756a5bc1f4f79576829f43e183b03792469b2cbf9288c140628e90e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7939966c6d448ce4c52dd7ff97318dfdeac7dcac277dc3009f2eec4219ab2f18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class StorageInsightsDatasetConfigLinkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigLinkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f49c2300e06e2da114785ed42087f96aacc1fc3145395dc46f5ee18ae40d994)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataset"))

    @builtins.property
    @jsii.member(jsii_name="linked")
    def linked(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "linked"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageInsightsDatasetConfigLink]:
        return typing.cast(typing.Optional[StorageInsightsDatasetConfigLink], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageInsightsDatasetConfigLink],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cad852e38222abe75df3efb84965f6d82ab9742887007bda32c5d865e5dca940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigSourceFolders",
    jsii_struct_bases=[],
    name_mapping={"folder_numbers": "folderNumbers"},
)
class StorageInsightsDatasetConfigSourceFolders:
    def __init__(
        self,
        *,
        folder_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param folder_numbers: The list of folder numbers to include in the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#folder_numbers StorageInsightsDatasetConfig#folder_numbers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0115f914cfa2e9387da0a305aa89a5fe479170177bb87e15af42ebbcf3e0b22)
            check_type(argname="argument folder_numbers", value=folder_numbers, expected_type=type_hints["folder_numbers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if folder_numbers is not None:
            self._values["folder_numbers"] = folder_numbers

    @builtins.property
    def folder_numbers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of folder numbers to include in the DatasetConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#folder_numbers StorageInsightsDatasetConfig#folder_numbers}
        '''
        result = self._values.get("folder_numbers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsDatasetConfigSourceFolders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageInsightsDatasetConfigSourceFoldersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigSourceFoldersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb084d15e4429acae9bfcddb08589fa25717c57ce03b4f0b9195f03a67933956)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFolderNumbers")
    def reset_folder_numbers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFolderNumbers", []))

    @builtins.property
    @jsii.member(jsii_name="folderNumbersInput")
    def folder_numbers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "folderNumbersInput"))

    @builtins.property
    @jsii.member(jsii_name="folderNumbers")
    def folder_numbers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "folderNumbers"))

    @folder_numbers.setter
    def folder_numbers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d639cea89f1958803d9820655c5ec724cc9776f5802ec2474e6c0d160eb260d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "folderNumbers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageInsightsDatasetConfigSourceFolders]:
        return typing.cast(typing.Optional[StorageInsightsDatasetConfigSourceFolders], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageInsightsDatasetConfigSourceFolders],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feab71ddd359e0140e32e15a798605dc09167b4e50b4e6d4ddd441a846164c78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigSourceProjects",
    jsii_struct_bases=[],
    name_mapping={"project_numbers": "projectNumbers"},
)
class StorageInsightsDatasetConfigSourceProjects:
    def __init__(
        self,
        *,
        project_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param project_numbers: The list of project numbers to include in the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#project_numbers StorageInsightsDatasetConfig#project_numbers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54449a145359cbd0ea7ab193d838e4f38bbe2a41cda491eb645f3ab7cfc03c79)
            check_type(argname="argument project_numbers", value=project_numbers, expected_type=type_hints["project_numbers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if project_numbers is not None:
            self._values["project_numbers"] = project_numbers

    @builtins.property
    def project_numbers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of project numbers to include in the DatasetConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#project_numbers StorageInsightsDatasetConfig#project_numbers}
        '''
        result = self._values.get("project_numbers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsDatasetConfigSourceProjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageInsightsDatasetConfigSourceProjectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigSourceProjectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23927e8ebc73c6afafde3ed9c212fe8d83b70ed3bf544a39171c3a82b0c3aeae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProjectNumbers")
    def reset_project_numbers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectNumbers", []))

    @builtins.property
    @jsii.member(jsii_name="projectNumbersInput")
    def project_numbers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "projectNumbersInput"))

    @builtins.property
    @jsii.member(jsii_name="projectNumbers")
    def project_numbers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "projectNumbers"))

    @project_numbers.setter
    def project_numbers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04109dd84718e24b7b5e891c197477517b28c9a7695e9cd23a5e3b7dc41d6967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectNumbers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageInsightsDatasetConfigSourceProjects]:
        return typing.cast(typing.Optional[StorageInsightsDatasetConfigSourceProjects], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageInsightsDatasetConfigSourceProjects],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e9b5cf0135cfcb67b26c8dd8b8f20afec4a310672cc124d0df569ea996cd50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class StorageInsightsDatasetConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#create StorageInsightsDatasetConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#delete StorageInsightsDatasetConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#update StorageInsightsDatasetConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f1cbf9f1a3ef3994dae70818eeeeec4ab2c6b6c85bed5a03f48e6df385af23)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#create StorageInsightsDatasetConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#delete StorageInsightsDatasetConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/storage_insights_dataset_config#update StorageInsightsDatasetConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsDatasetConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageInsightsDatasetConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsDatasetConfig.StorageInsightsDatasetConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f882e001251388e67a4717ee5a7aa1ffc394cb46d5d81fb60be801eab0b5d38b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b24379016a161268e876a4a03d9351effedc326623f0719a83120211cd36547)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87a2f8689153bc9f18591711aa9b805bf870894f77360eabac6a9bcca8da46d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51727eb2751d3af41eebb3fd8aaf3d105114a943fcdf61ba93f3279d69301e81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageInsightsDatasetConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageInsightsDatasetConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageInsightsDatasetConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af610ff2abb4aeed58501c19f80224f543d76f89a80ecbecbaf65dce20b2f83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StorageInsightsDatasetConfig",
    "StorageInsightsDatasetConfigConfig",
    "StorageInsightsDatasetConfigExcludeCloudStorageBuckets",
    "StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets",
    "StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsList",
    "StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsOutputReference",
    "StorageInsightsDatasetConfigExcludeCloudStorageBucketsOutputReference",
    "StorageInsightsDatasetConfigExcludeCloudStorageLocations",
    "StorageInsightsDatasetConfigExcludeCloudStorageLocationsOutputReference",
    "StorageInsightsDatasetConfigIdentity",
    "StorageInsightsDatasetConfigIdentityOutputReference",
    "StorageInsightsDatasetConfigIncludeCloudStorageBuckets",
    "StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets",
    "StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsList",
    "StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsOutputReference",
    "StorageInsightsDatasetConfigIncludeCloudStorageBucketsOutputReference",
    "StorageInsightsDatasetConfigIncludeCloudStorageLocations",
    "StorageInsightsDatasetConfigIncludeCloudStorageLocationsOutputReference",
    "StorageInsightsDatasetConfigLink",
    "StorageInsightsDatasetConfigLinkList",
    "StorageInsightsDatasetConfigLinkOutputReference",
    "StorageInsightsDatasetConfigSourceFolders",
    "StorageInsightsDatasetConfigSourceFoldersOutputReference",
    "StorageInsightsDatasetConfigSourceProjects",
    "StorageInsightsDatasetConfigSourceProjectsOutputReference",
    "StorageInsightsDatasetConfigTimeouts",
    "StorageInsightsDatasetConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__fee2219e5370b3f000996248d1df311d65018b20c9a68aaeb27cc0b2102e7b00(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dataset_config_id: builtins.str,
    identity: typing.Union[StorageInsightsDatasetConfigIdentity, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    retention_period_days: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    exclude_cloud_storage_buckets: typing.Optional[typing.Union[StorageInsightsDatasetConfigExcludeCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude_cloud_storage_locations: typing.Optional[typing.Union[StorageInsightsDatasetConfigExcludeCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    include_cloud_storage_buckets: typing.Optional[typing.Union[StorageInsightsDatasetConfigIncludeCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    include_cloud_storage_locations: typing.Optional[typing.Union[StorageInsightsDatasetConfigIncludeCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
    include_newly_created_buckets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    link_dataset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    organization_number: typing.Optional[builtins.str] = None,
    organization_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    source_folders: typing.Optional[typing.Union[StorageInsightsDatasetConfigSourceFolders, typing.Dict[builtins.str, typing.Any]]] = None,
    source_projects: typing.Optional[typing.Union[StorageInsightsDatasetConfigSourceProjects, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[StorageInsightsDatasetConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__dc2f231f8fd4ac1fed39a534bb0fe31adaf1d73d098d5dcc073fae9865e79edd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82dd1335bd1bf6b2ed22d02a141891cfeed66121d0d83dfae4650e35838a04de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a55fab7709e9ba6354e297c814427a3edd7bfd1c1dbc7c295959d366b3087bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de4d58f4306ae44f78b807fd42f7b9f9225939874bc75b1a0f01d100dc2d281c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68349938cc5e18223d0f16fb32226647880d718922465470eca2ac25b712c673(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58090bc5bae01f180e4056f35bea800a8e86e8d841665928a306e8cc083923a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ea1076e8f863f45585ca9e5c2e2806e3b198ee65ab3da78d4481879d70cdd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1248a0b16f5057225d9867763bb3e9780977ec264420eefba08365eae2977aef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dac95f9a2ebd45b079c4304a021488f2dbca5c9b45a9dcea600db0fbbaf15ac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60465146d010ddb80b83348d27879e28c6bda48c66e41cab2836ae559bf59c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a108eacc15ffd1da62efe28e651d91dccfec7ae83a28b48add5ead4078cc1d2e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882f56583fdca1c45472b260748a76a0d1018a32bf4800c931899eb382b1ecb5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dataset_config_id: builtins.str,
    identity: typing.Union[StorageInsightsDatasetConfigIdentity, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    retention_period_days: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    exclude_cloud_storage_buckets: typing.Optional[typing.Union[StorageInsightsDatasetConfigExcludeCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude_cloud_storage_locations: typing.Optional[typing.Union[StorageInsightsDatasetConfigExcludeCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    include_cloud_storage_buckets: typing.Optional[typing.Union[StorageInsightsDatasetConfigIncludeCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    include_cloud_storage_locations: typing.Optional[typing.Union[StorageInsightsDatasetConfigIncludeCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
    include_newly_created_buckets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    link_dataset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    organization_number: typing.Optional[builtins.str] = None,
    organization_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    source_folders: typing.Optional[typing.Union[StorageInsightsDatasetConfigSourceFolders, typing.Dict[builtins.str, typing.Any]]] = None,
    source_projects: typing.Optional[typing.Union[StorageInsightsDatasetConfigSourceProjects, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[StorageInsightsDatasetConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4225bd9520c86647c68f0bdd5f3f77a2742b5906cb2a1afe3bfb514b33e7ec35(
    *,
    cloud_storage_buckets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bfa56324644ca0510e45e5f327746d8d3d8ce72753227e42193e22615d02907(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa68027b6d2b2aed89dccd191480f1c0f2038de5a94f4251f2df121c507891e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac2cb054fc723eca8e9e33e8ec825af434af50c553a5c70d25fd6a72f50f96e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a35c07e6d24da57567e28ec031119874aeb2291378d47d5caba8a42763aed4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda83c20f8f8656cb2e1846c5862cde48056d146a95b68c4acdcc119bfe293e8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__254dc4defeebcf3b2882ad6b5ee7a7788eb470cf027a3387d231aabff552e020(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8150dc3c0b5c8e1b12815a977c52c7d3975c47de1cf5e614a424d6633d22af26(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5978d3b16ab079601260cbae46475d8f801b71de52aa64e7bbb0c90db3d50767(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53faa208e6900e9ee44db120cfd3fc519dcf409373894855796c2c4c3b12d6e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e55b73c104f325f0c8648e56e6388d5f78562a45650faf3f3186a80118a759(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a94a53bb4e0e68fb988d0fcf5aadb04e746036c1c38fab39f1861e5886554a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8711d0a21110f2c082f57e9c8c2807e1fe0decd5cb1f1bf59767a787b4387fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68dd83931a5a609dc17c51dbd652c8008ad05c62220ca7f4ad1ec41e6f1268e4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd5361a644940a7e65eb0e63149da780e763834defe164e4d185f8932422bd0(
    value: typing.Optional[StorageInsightsDatasetConfigExcludeCloudStorageBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d7935df1add3649894a7ef62ff07b4e47eb1003cff5e6d5f005f9301448617(
    *,
    locations: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcbca59d4d57c1490906a4342c77df4229d066e547863c197d3c4a6dc5fb7214(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0f8fb8a12e7f5ab133f5ace3507d1f3402d56faa9070300703358ffa5b8953(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6c26e5d239023fe49f92cbf39223c12e36639a5ac9a4a3e4eec33ab3b79a3f(
    value: typing.Optional[StorageInsightsDatasetConfigExcludeCloudStorageLocations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c06bd4b39f71086b7888b4b6b04f18ad82ccadd1a2ac79d0fdc68dd0701633(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173e839943ed488a040304f3b7554736ac43e8945676279ed716c1ee14978663(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2483ec667f1518b4ad0796a83e3b2b615f96efedbd58c9440111893e44b9c281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__017ccdec4ae8d8c332f640bc776a3fa199902db2ab5e9261063736de40f027a7(
    value: typing.Optional[StorageInsightsDatasetConfigIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1048c27191bc66f3e2cd289b435696bfe28b59c8cf93d9079de5009b1bd770b7(
    *,
    cloud_storage_buckets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496153a8397cb5eb9aae6156d84d68e8eb0a9be677693b6bb9837f21dc5cbaef(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4de812c81791b40885b214ec4f19dbeeea2c37bee62643c71bbc9b255fea417(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e50f362f12940a5719ba0dfaed477a4d790da8bb265d0c9423d513d734b70ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf5f7e92427f645ab8e407a67ae62eea5b0dae4f70a6916833af9acc5c80f5c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33d5c2d06cbae8a495292daa56b0c7bd5397faf9e6a27624c299e622e98db8d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3739714faca6d835d3eed38f9a19438e5185665c83a82409453aefc12710e598(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd40c975bc13d61dcfcb276a9470fcacd15e78f76c4c79aff8e193ff1fa2937(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c23f785a24502a6c68c28d63a99c6a78b7c14237b9ec9125334d585fe72e63d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__339290ee6cd361f274ea424b188714b191aa6d19271a1bc5a3e8606c3438fa82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf1895642c760e475191d786a29337b64078b83be2f4f32449d0ac9b748c7fcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a65238f57fbd820a655e96b130c51d2d835ba70bfe5e00bc134e674370ce67(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a7f27b62b8e4670f4c4252964b0bcf5766dce51a88fd594ed9904044ac8ed34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cb1231d565aa8247068f5ee522f40023830104e5dcdc4db63a1d399b3a4fce5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd5b5e6da56b0cba1a9bd507a415484a05f98ec4be3a5ddf04236fca29562a9(
    value: typing.Optional[StorageInsightsDatasetConfigIncludeCloudStorageBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89eec1ebff63807a45128681bb14ef270ffb269c0dd5dc40eb381bf636c6e26(
    *,
    locations: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fee8afa5cc36b108b9beea254db8f12ec8b48fe9c8e0192b9deebca59f6142a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f1bc02881223035fefbe6a489a39ef9bd89a4911a0a54c418452db5b571ab6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a97468cad2c50c50766b683ef4efda5aede80f0cd8d635763bcceaf1d278a7fa(
    value: typing.Optional[StorageInsightsDatasetConfigIncludeCloudStorageLocations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6570ce2cd6ddaf39147d5337e00317e1e453af3fc1d1762aea6f72b795beb55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a32840af9a01b808df31abe0d813cf471337dee90f0bed7452d3bceb562633(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e1b759d39c7b75caf8bb072c8fc3fa036606bebf1e8d22a379e6bcec0d8c7ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffefbd6e756a5bc1f4f79576829f43e183b03792469b2cbf9288c140628e90e8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7939966c6d448ce4c52dd7ff97318dfdeac7dcac277dc3009f2eec4219ab2f18(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f49c2300e06e2da114785ed42087f96aacc1fc3145395dc46f5ee18ae40d994(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad852e38222abe75df3efb84965f6d82ab9742887007bda32c5d865e5dca940(
    value: typing.Optional[StorageInsightsDatasetConfigLink],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0115f914cfa2e9387da0a305aa89a5fe479170177bb87e15af42ebbcf3e0b22(
    *,
    folder_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb084d15e4429acae9bfcddb08589fa25717c57ce03b4f0b9195f03a67933956(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d639cea89f1958803d9820655c5ec724cc9776f5802ec2474e6c0d160eb260d4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feab71ddd359e0140e32e15a798605dc09167b4e50b4e6d4ddd441a846164c78(
    value: typing.Optional[StorageInsightsDatasetConfigSourceFolders],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54449a145359cbd0ea7ab193d838e4f38bbe2a41cda491eb645f3ab7cfc03c79(
    *,
    project_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23927e8ebc73c6afafde3ed9c212fe8d83b70ed3bf544a39171c3a82b0c3aeae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04109dd84718e24b7b5e891c197477517b28c9a7695e9cd23a5e3b7dc41d6967(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e9b5cf0135cfcb67b26c8dd8b8f20afec4a310672cc124d0df569ea996cd50(
    value: typing.Optional[StorageInsightsDatasetConfigSourceProjects],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f1cbf9f1a3ef3994dae70818eeeeec4ab2c6b6c85bed5a03f48e6df385af23(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f882e001251388e67a4717ee5a7aa1ffc394cb46d5d81fb60be801eab0b5d38b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b24379016a161268e876a4a03d9351effedc326623f0719a83120211cd36547(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87a2f8689153bc9f18591711aa9b805bf870894f77360eabac6a9bcca8da46d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51727eb2751d3af41eebb3fd8aaf3d105114a943fcdf61ba93f3279d69301e81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af610ff2abb4aeed58501c19f80224f543d76f89a80ecbecbaf65dce20b2f83(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageInsightsDatasetConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

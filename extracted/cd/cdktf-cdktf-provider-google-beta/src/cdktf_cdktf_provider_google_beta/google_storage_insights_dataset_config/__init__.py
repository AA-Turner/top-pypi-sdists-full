r'''
# `google_storage_insights_dataset_config`

Refer to the Terraform Registry for docs: [`google_storage_insights_dataset_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config).
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


class GoogleStorageInsightsDatasetConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config google_storage_insights_dataset_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dataset_config_id: builtins.str,
        identity: typing.Union["GoogleStorageInsightsDatasetConfigIdentity", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        retention_period_days: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        exclude_cloud_storage_buckets: typing.Optional[typing.Union["GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_cloud_storage_locations: typing.Optional[typing.Union["GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        include_cloud_storage_buckets: typing.Optional[typing.Union["GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        include_cloud_storage_locations: typing.Optional[typing.Union["GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        include_newly_created_buckets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        link_dataset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        organization_number: typing.Optional[builtins.str] = None,
        organization_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        source_folders: typing.Optional[typing.Union["GoogleStorageInsightsDatasetConfigSourceFolders", typing.Dict[builtins.str, typing.Any]]] = None,
        source_projects: typing.Optional[typing.Union["GoogleStorageInsightsDatasetConfigSourceProjects", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleStorageInsightsDatasetConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config google_storage_insights_dataset_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dataset_config_id: The user-defined ID of the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#dataset_config_id GoogleStorageInsightsDatasetConfig#dataset_config_id}
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#identity GoogleStorageInsightsDatasetConfig#identity}
        :param location: The location of the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#location GoogleStorageInsightsDatasetConfig#location}
        :param retention_period_days: Number of days of history that must be retained. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#retention_period_days GoogleStorageInsightsDatasetConfig#retention_period_days}
        :param description: An optional user-provided description for the dataset configuration with a maximum length of 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#description GoogleStorageInsightsDatasetConfig#description}
        :param exclude_cloud_storage_buckets: exclude_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#exclude_cloud_storage_buckets GoogleStorageInsightsDatasetConfig#exclude_cloud_storage_buckets}
        :param exclude_cloud_storage_locations: exclude_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#exclude_cloud_storage_locations GoogleStorageInsightsDatasetConfig#exclude_cloud_storage_locations}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#id GoogleStorageInsightsDatasetConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_cloud_storage_buckets: include_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#include_cloud_storage_buckets GoogleStorageInsightsDatasetConfig#include_cloud_storage_buckets}
        :param include_cloud_storage_locations: include_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#include_cloud_storage_locations GoogleStorageInsightsDatasetConfig#include_cloud_storage_locations}
        :param include_newly_created_buckets: If set to true, the request includes all the newly created buckets in the dataset that meet the inclusion and exclusion rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#include_newly_created_buckets GoogleStorageInsightsDatasetConfig#include_newly_created_buckets}
        :param link_dataset: A boolean terraform only flag to link/unlink dataset. Setting this field to true while creation will automatically link the created dataset as an additional functionality. -> **Note** A dataset config resource can only be destroyed once it is unlinked, so users must set this field to false to unlink the dataset and destroy the dataset config resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#link_dataset GoogleStorageInsightsDatasetConfig#link_dataset}
        :param organization_number: Organization resource ID that the source projects should belong to. Projects that do not belong to the provided organization are not considered when creating the dataset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#organization_number GoogleStorageInsightsDatasetConfig#organization_number}
        :param organization_scope: Defines the options for providing a source organization for the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#organization_scope GoogleStorageInsightsDatasetConfig#organization_scope}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#project GoogleStorageInsightsDatasetConfig#project}.
        :param source_folders: source_folders block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#source_folders GoogleStorageInsightsDatasetConfig#source_folders}
        :param source_projects: source_projects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#source_projects GoogleStorageInsightsDatasetConfig#source_projects}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#timeouts GoogleStorageInsightsDatasetConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd118eda5ec27b17ad5423292711c5faeae6271902b34f879dce6936f348d7f4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleStorageInsightsDatasetConfigConfig(
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
        '''Generates CDKTF code for importing a GoogleStorageInsightsDatasetConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleStorageInsightsDatasetConfig to import.
        :param import_from_id: The id of the existing GoogleStorageInsightsDatasetConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleStorageInsightsDatasetConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe935ce3479a8f6b03be3f402901d84d6f268f94f18c2ccc2eb93b16129d4ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putExcludeCloudStorageBuckets")
    def put_exclude_cloud_storage_buckets(
        self,
        *,
        cloud_storage_buckets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param cloud_storage_buckets: cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#cloud_storage_buckets GoogleStorageInsightsDatasetConfig#cloud_storage_buckets}
        '''
        value = GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets(
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
        :param locations: The list of cloud storage locations to exclude in the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#locations GoogleStorageInsightsDatasetConfig#locations}
        '''
        value = GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations(
            locations=locations
        )

        return typing.cast(None, jsii.invoke(self, "putExcludeCloudStorageLocations", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(self, *, type: builtins.str) -> None:
        '''
        :param type: Type of identity to use for the DatasetConfig. Possible values: ["IDENTITY_TYPE_PER_CONFIG", "IDENTITY_TYPE_PER_PROJECT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#type GoogleStorageInsightsDatasetConfig#type}
        '''
        value = GoogleStorageInsightsDatasetConfigIdentity(type=type)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putIncludeCloudStorageBuckets")
    def put_include_cloud_storage_buckets(
        self,
        *,
        cloud_storage_buckets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param cloud_storage_buckets: cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#cloud_storage_buckets GoogleStorageInsightsDatasetConfig#cloud_storage_buckets}
        '''
        value = GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets(
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
        :param locations: The list of cloud storage locations to include in the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#locations GoogleStorageInsightsDatasetConfig#locations}
        '''
        value = GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations(
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
        :param folder_numbers: The list of folder numbers to include in the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#folder_numbers GoogleStorageInsightsDatasetConfig#folder_numbers}
        '''
        value = GoogleStorageInsightsDatasetConfigSourceFolders(
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
        :param project_numbers: The list of project numbers to include in the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#project_numbers GoogleStorageInsightsDatasetConfig#project_numbers}
        '''
        value = GoogleStorageInsightsDatasetConfigSourceProjects(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#create GoogleStorageInsightsDatasetConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#delete GoogleStorageInsightsDatasetConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#update GoogleStorageInsightsDatasetConfig#update}.
        '''
        value = GoogleStorageInsightsDatasetConfigTimeouts(
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
    ) -> "GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsOutputReference":
        return typing.cast("GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsOutputReference", jsii.get(self, "excludeCloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="excludeCloudStorageLocations")
    def exclude_cloud_storage_locations(
        self,
    ) -> "GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocationsOutputReference":
        return typing.cast("GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocationsOutputReference", jsii.get(self, "excludeCloudStorageLocations"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "GoogleStorageInsightsDatasetConfigIdentityOutputReference":
        return typing.cast("GoogleStorageInsightsDatasetConfigIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="includeCloudStorageBuckets")
    def include_cloud_storage_buckets(
        self,
    ) -> "GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsOutputReference":
        return typing.cast("GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsOutputReference", jsii.get(self, "includeCloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="includeCloudStorageLocations")
    def include_cloud_storage_locations(
        self,
    ) -> "GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocationsOutputReference":
        return typing.cast("GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocationsOutputReference", jsii.get(self, "includeCloudStorageLocations"))

    @builtins.property
    @jsii.member(jsii_name="link")
    def link(self) -> "GoogleStorageInsightsDatasetConfigLinkList":
        return typing.cast("GoogleStorageInsightsDatasetConfigLinkList", jsii.get(self, "link"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="sourceFolders")
    def source_folders(
        self,
    ) -> "GoogleStorageInsightsDatasetConfigSourceFoldersOutputReference":
        return typing.cast("GoogleStorageInsightsDatasetConfigSourceFoldersOutputReference", jsii.get(self, "sourceFolders"))

    @builtins.property
    @jsii.member(jsii_name="sourceProjects")
    def source_projects(
        self,
    ) -> "GoogleStorageInsightsDatasetConfigSourceProjectsOutputReference":
        return typing.cast("GoogleStorageInsightsDatasetConfigSourceProjectsOutputReference", jsii.get(self, "sourceProjects"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleStorageInsightsDatasetConfigTimeoutsOutputReference":
        return typing.cast("GoogleStorageInsightsDatasetConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets"]:
        return typing.cast(typing.Optional["GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets"], jsii.get(self, "excludeCloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeCloudStorageLocationsInput")
    def exclude_cloud_storage_locations_input(
        self,
    ) -> typing.Optional["GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations"]:
        return typing.cast(typing.Optional["GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations"], jsii.get(self, "excludeCloudStorageLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(
        self,
    ) -> typing.Optional["GoogleStorageInsightsDatasetConfigIdentity"]:
        return typing.cast(typing.Optional["GoogleStorageInsightsDatasetConfigIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeCloudStorageBucketsInput")
    def include_cloud_storage_buckets_input(
        self,
    ) -> typing.Optional["GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets"]:
        return typing.cast(typing.Optional["GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets"], jsii.get(self, "includeCloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeCloudStorageLocationsInput")
    def include_cloud_storage_locations_input(
        self,
    ) -> typing.Optional["GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations"]:
        return typing.cast(typing.Optional["GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations"], jsii.get(self, "includeCloudStorageLocationsInput"))

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
    ) -> typing.Optional["GoogleStorageInsightsDatasetConfigSourceFolders"]:
        return typing.cast(typing.Optional["GoogleStorageInsightsDatasetConfigSourceFolders"], jsii.get(self, "sourceFoldersInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceProjectsInput")
    def source_projects_input(
        self,
    ) -> typing.Optional["GoogleStorageInsightsDatasetConfigSourceProjects"]:
        return typing.cast(typing.Optional["GoogleStorageInsightsDatasetConfigSourceProjects"], jsii.get(self, "sourceProjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleStorageInsightsDatasetConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleStorageInsightsDatasetConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetConfigId")
    def dataset_config_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetConfigId"))

    @dataset_config_id.setter
    def dataset_config_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dda24f4b7043f732e5b2d291c16d0ca74faaa69185da1d2c0f8a4561b888a1b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetConfigId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__391db625efb3e8ef6a9c7a4e45e0fa87bc70a87bba9fd7f04e6d9c1b108ee0d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03ec6ae01fc021118f999c0fc06310b056380fec1a1c70621526494dc06f5a41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dcb3191d50bf2eb62b9842655e264cc6edbb752bcfc3419c13ad188cd361715)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8796847910a585a94edccd053f80fbd4a84de9d1c2c2b56e481db3c6cf5b9ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkDataset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ecd6975f2efb3eda81a915713ef1c66289eb190a1931e83e6a42ef0be4d7ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationNumber")
    def organization_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationNumber"))

    @organization_number.setter
    def organization_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b391342337bdffc4bddba4d10587a9289f539c320eba6cf2e0988d3f69ca18b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e72c9821646781c3b7e4ec169a1d6cb354de58d12f76571b19b25948ffc53d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffba5cbf9e84b468cec30f13de9623e7d8ff4ba81ee7be7d62f68b52af0b7b42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodDays")
    def retention_period_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPeriodDays"))

    @retention_period_days.setter
    def retention_period_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e128d329254e2dc3ad364c9e39b9038d2b340409c2eddb4e8ef66dc02a26e19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriodDays", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigConfig",
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
class GoogleStorageInsightsDatasetConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        identity: typing.Union["GoogleStorageInsightsDatasetConfigIdentity", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        retention_period_days: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        exclude_cloud_storage_buckets: typing.Optional[typing.Union["GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_cloud_storage_locations: typing.Optional[typing.Union["GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        include_cloud_storage_buckets: typing.Optional[typing.Union["GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        include_cloud_storage_locations: typing.Optional[typing.Union["GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        include_newly_created_buckets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        link_dataset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        organization_number: typing.Optional[builtins.str] = None,
        organization_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        source_folders: typing.Optional[typing.Union["GoogleStorageInsightsDatasetConfigSourceFolders", typing.Dict[builtins.str, typing.Any]]] = None,
        source_projects: typing.Optional[typing.Union["GoogleStorageInsightsDatasetConfigSourceProjects", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleStorageInsightsDatasetConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dataset_config_id: The user-defined ID of the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#dataset_config_id GoogleStorageInsightsDatasetConfig#dataset_config_id}
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#identity GoogleStorageInsightsDatasetConfig#identity}
        :param location: The location of the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#location GoogleStorageInsightsDatasetConfig#location}
        :param retention_period_days: Number of days of history that must be retained. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#retention_period_days GoogleStorageInsightsDatasetConfig#retention_period_days}
        :param description: An optional user-provided description for the dataset configuration with a maximum length of 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#description GoogleStorageInsightsDatasetConfig#description}
        :param exclude_cloud_storage_buckets: exclude_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#exclude_cloud_storage_buckets GoogleStorageInsightsDatasetConfig#exclude_cloud_storage_buckets}
        :param exclude_cloud_storage_locations: exclude_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#exclude_cloud_storage_locations GoogleStorageInsightsDatasetConfig#exclude_cloud_storage_locations}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#id GoogleStorageInsightsDatasetConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_cloud_storage_buckets: include_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#include_cloud_storage_buckets GoogleStorageInsightsDatasetConfig#include_cloud_storage_buckets}
        :param include_cloud_storage_locations: include_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#include_cloud_storage_locations GoogleStorageInsightsDatasetConfig#include_cloud_storage_locations}
        :param include_newly_created_buckets: If set to true, the request includes all the newly created buckets in the dataset that meet the inclusion and exclusion rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#include_newly_created_buckets GoogleStorageInsightsDatasetConfig#include_newly_created_buckets}
        :param link_dataset: A boolean terraform only flag to link/unlink dataset. Setting this field to true while creation will automatically link the created dataset as an additional functionality. -> **Note** A dataset config resource can only be destroyed once it is unlinked, so users must set this field to false to unlink the dataset and destroy the dataset config resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#link_dataset GoogleStorageInsightsDatasetConfig#link_dataset}
        :param organization_number: Organization resource ID that the source projects should belong to. Projects that do not belong to the provided organization are not considered when creating the dataset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#organization_number GoogleStorageInsightsDatasetConfig#organization_number}
        :param organization_scope: Defines the options for providing a source organization for the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#organization_scope GoogleStorageInsightsDatasetConfig#organization_scope}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#project GoogleStorageInsightsDatasetConfig#project}.
        :param source_folders: source_folders block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#source_folders GoogleStorageInsightsDatasetConfig#source_folders}
        :param source_projects: source_projects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#source_projects GoogleStorageInsightsDatasetConfig#source_projects}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#timeouts GoogleStorageInsightsDatasetConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(identity, dict):
            identity = GoogleStorageInsightsDatasetConfigIdentity(**identity)
        if isinstance(exclude_cloud_storage_buckets, dict):
            exclude_cloud_storage_buckets = GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets(**exclude_cloud_storage_buckets)
        if isinstance(exclude_cloud_storage_locations, dict):
            exclude_cloud_storage_locations = GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations(**exclude_cloud_storage_locations)
        if isinstance(include_cloud_storage_buckets, dict):
            include_cloud_storage_buckets = GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets(**include_cloud_storage_buckets)
        if isinstance(include_cloud_storage_locations, dict):
            include_cloud_storage_locations = GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations(**include_cloud_storage_locations)
        if isinstance(source_folders, dict):
            source_folders = GoogleStorageInsightsDatasetConfigSourceFolders(**source_folders)
        if isinstance(source_projects, dict):
            source_projects = GoogleStorageInsightsDatasetConfigSourceProjects(**source_projects)
        if isinstance(timeouts, dict):
            timeouts = GoogleStorageInsightsDatasetConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ae42f51a359f6225fa5fc4f8155a3ba10042e5f5bb4ae0f74f5aebd5ac4264)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#dataset_config_id GoogleStorageInsightsDatasetConfig#dataset_config_id}
        '''
        result = self._values.get("dataset_config_id")
        assert result is not None, "Required property 'dataset_config_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity(self) -> "GoogleStorageInsightsDatasetConfigIdentity":
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#identity GoogleStorageInsightsDatasetConfig#identity}
        '''
        result = self._values.get("identity")
        assert result is not None, "Required property 'identity' is missing"
        return typing.cast("GoogleStorageInsightsDatasetConfigIdentity", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the DatasetConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#location GoogleStorageInsightsDatasetConfig#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_period_days(self) -> jsii.Number:
        '''Number of days of history that must be retained.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#retention_period_days GoogleStorageInsightsDatasetConfig#retention_period_days}
        '''
        result = self._values.get("retention_period_days")
        assert result is not None, "Required property 'retention_period_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional user-provided description for the dataset configuration with a maximum length of 256 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#description GoogleStorageInsightsDatasetConfig#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude_cloud_storage_buckets(
        self,
    ) -> typing.Optional["GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets"]:
        '''exclude_cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#exclude_cloud_storage_buckets GoogleStorageInsightsDatasetConfig#exclude_cloud_storage_buckets}
        '''
        result = self._values.get("exclude_cloud_storage_buckets")
        return typing.cast(typing.Optional["GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets"], result)

    @builtins.property
    def exclude_cloud_storage_locations(
        self,
    ) -> typing.Optional["GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations"]:
        '''exclude_cloud_storage_locations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#exclude_cloud_storage_locations GoogleStorageInsightsDatasetConfig#exclude_cloud_storage_locations}
        '''
        result = self._values.get("exclude_cloud_storage_locations")
        return typing.cast(typing.Optional["GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#id GoogleStorageInsightsDatasetConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_cloud_storage_buckets(
        self,
    ) -> typing.Optional["GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets"]:
        '''include_cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#include_cloud_storage_buckets GoogleStorageInsightsDatasetConfig#include_cloud_storage_buckets}
        '''
        result = self._values.get("include_cloud_storage_buckets")
        return typing.cast(typing.Optional["GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets"], result)

    @builtins.property
    def include_cloud_storage_locations(
        self,
    ) -> typing.Optional["GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations"]:
        '''include_cloud_storage_locations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#include_cloud_storage_locations GoogleStorageInsightsDatasetConfig#include_cloud_storage_locations}
        '''
        result = self._values.get("include_cloud_storage_locations")
        return typing.cast(typing.Optional["GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations"], result)

    @builtins.property
    def include_newly_created_buckets(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the request includes all the newly created buckets in the dataset that meet the inclusion and exclusion rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#include_newly_created_buckets GoogleStorageInsightsDatasetConfig#include_newly_created_buckets}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#link_dataset GoogleStorageInsightsDatasetConfig#link_dataset}
        '''
        result = self._values.get("link_dataset")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def organization_number(self) -> typing.Optional[builtins.str]:
        '''Organization resource ID that the source projects should belong to.

        Projects that do not belong to the provided organization are not considered when creating the dataset.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#organization_number GoogleStorageInsightsDatasetConfig#organization_number}
        '''
        result = self._values.get("organization_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization_scope(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines the options for providing a source organization for the DatasetConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#organization_scope GoogleStorageInsightsDatasetConfig#organization_scope}
        '''
        result = self._values.get("organization_scope")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#project GoogleStorageInsightsDatasetConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_folders(
        self,
    ) -> typing.Optional["GoogleStorageInsightsDatasetConfigSourceFolders"]:
        '''source_folders block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#source_folders GoogleStorageInsightsDatasetConfig#source_folders}
        '''
        result = self._values.get("source_folders")
        return typing.cast(typing.Optional["GoogleStorageInsightsDatasetConfigSourceFolders"], result)

    @builtins.property
    def source_projects(
        self,
    ) -> typing.Optional["GoogleStorageInsightsDatasetConfigSourceProjects"]:
        '''source_projects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#source_projects GoogleStorageInsightsDatasetConfig#source_projects}
        '''
        result = self._values.get("source_projects")
        return typing.cast(typing.Optional["GoogleStorageInsightsDatasetConfigSourceProjects"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleStorageInsightsDatasetConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#timeouts GoogleStorageInsightsDatasetConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleStorageInsightsDatasetConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsDatasetConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={"cloud_storage_buckets": "cloudStorageBuckets"},
)
class GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets:
    def __init__(
        self,
        *,
        cloud_storage_buckets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param cloud_storage_buckets: cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#cloud_storage_buckets GoogleStorageInsightsDatasetConfig#cloud_storage_buckets}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77e90968b9fb1240652adda4c36827e326d1a6c2e5e6212b6824e12b80c48002)
            check_type(argname="argument cloud_storage_buckets", value=cloud_storage_buckets, expected_type=type_hints["cloud_storage_buckets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_storage_buckets": cloud_storage_buckets,
        }

    @builtins.property
    def cloud_storage_buckets(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets"]]:
        '''cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#cloud_storage_buckets GoogleStorageInsightsDatasetConfig#cloud_storage_buckets}
        '''
        result = self._values.get("cloud_storage_buckets")
        assert result is not None, "Required property 'cloud_storage_buckets' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix_regex": "bucketPrefixRegex",
    },
)
class GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: The list of cloud storage bucket names to exclude in the DatasetConfig. Exactly one of the bucket_name and bucket_prefix_regex should be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#bucket_name GoogleStorageInsightsDatasetConfig#bucket_name}
        :param bucket_prefix_regex: The list of regex patterns for bucket names matching the regex. Regex should follow the syntax specified in google/re2 on GitHub. Exactly one of the bucket_name and bucket_prefix_regex should be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#bucket_prefix_regex GoogleStorageInsightsDatasetConfig#bucket_prefix_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e604ea889bcacbd43ce70c90f37f9f36b2d0fa717e0bf28cc3e62a7a83099d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#bucket_name GoogleStorageInsightsDatasetConfig#bucket_name}
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix_regex(self) -> typing.Optional[builtins.str]:
        '''The list of regex patterns for bucket names matching the regex.

        Regex should follow the syntax specified in google/re2 on GitHub.
        Exactly one of the bucket_name and bucket_prefix_regex should be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#bucket_prefix_regex GoogleStorageInsightsDatasetConfig#bucket_prefix_regex}
        '''
        result = self._values.get("bucket_prefix_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f7313797c2c8d5ce0f09326b600e7e2704059760e475018d826effe9da01f51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54c13e33a074deb6ff5d442b51c016f57b1a1b07a3b8b373dc95af9a7caafdc3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d79a539766ec46a8b6c29283bcdfd3548899ac0e97a68550280170f9efe4b53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__def83e981c44179732b6949d0a4960b4e3a9ae6a7c681be9d15ae167f24e0182)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c5517d7c14f12c4a7ea9a504b3daadc3ffcd35e5e8b30ba50516892dd3e23dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c93c5f825145b53e45c330ec813100aba0c5f158fd912c1ae3b4ce2f70676974)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db40566d561346acb7e6857215cd21c147adaa068c5eab6d5f4edfa2e8a86363)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73fc8dd573bef342414842daba187060aa5687e636252a94957603a498dc8f01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixRegex")
    def bucket_prefix_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefixRegex"))

    @bucket_prefix_regex.setter
    def bucket_prefix_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b84ecc769cc475b5dd953013681b7653037be19b3eca53a82637b0f1959d011)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefixRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c0bbab75a3a396d9328a5abc302b6b45da80e5195a3b163046eedf7d1a9ccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d161fe7e1ecb0c3a652dc09cf5b718348827b9950d385c987418e11e0c2c9ecc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudStorageBuckets")
    def put_cloud_storage_buckets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75f00352310754072a4e4043aa707b5763f01b3a68f5d31730ac2bf0da0ce9ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCloudStorageBuckets", [value]))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageBuckets")
    def cloud_storage_buckets(
        self,
    ) -> GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsList:
        return typing.cast(GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsList, jsii.get(self, "cloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageBucketsInput")
    def cloud_storage_buckets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]]], jsii.get(self, "cloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets]:
        return typing.cast(typing.Optional[GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49462869d56c9c1f745f4a0d5c750548e8552320abf422178c3cb498180516a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations",
    jsii_struct_bases=[],
    name_mapping={"locations": "locations"},
)
class GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations:
    def __init__(self, *, locations: typing.Sequence[builtins.str]) -> None:
        '''
        :param locations: The list of cloud storage locations to exclude in the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#locations GoogleStorageInsightsDatasetConfig#locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e21effbe1393d80714a5c8110878219dec58dc1f3d348c6a4fe46514bc3764c)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locations": locations,
        }

    @builtins.property
    def locations(self) -> typing.List[builtins.str]:
        '''The list of cloud storage locations to exclude in the DatasetConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#locations GoogleStorageInsightsDatasetConfig#locations}
        '''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__463ac6223cf7b7d24b04253886ebc793a7ba504f86a6a1eb4a85178f4e2ee13a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09e07c946cf43f91b29d15a27637b50f18beb47aa5052bf9608e443f3f84b8db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations]:
        return typing.cast(typing.Optional[GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89345e7e7c39df391a334a0529b30a7c0342150c7050f5ff6ab9275652c4eeca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class GoogleStorageInsightsDatasetConfigIdentity:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Type of identity to use for the DatasetConfig. Possible values: ["IDENTITY_TYPE_PER_CONFIG", "IDENTITY_TYPE_PER_PROJECT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#type GoogleStorageInsightsDatasetConfig#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd6295a717d819b3ba478565909190b5771de4b3d9f1142f9be26182096dc07c)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of identity to use for the DatasetConfig. Possible values: ["IDENTITY_TYPE_PER_CONFIG", "IDENTITY_TYPE_PER_PROJECT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#type GoogleStorageInsightsDatasetConfig#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsDatasetConfigIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageInsightsDatasetConfigIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87c87790ae8c426bf0d269d38f4d915a9799089ea80c71df33c6e837ea4fe042)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fac4ed3eed1881c19463894cdd642f633dc78a511c7dfaf6ca4095d1d6547af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageInsightsDatasetConfigIdentity]:
        return typing.cast(typing.Optional[GoogleStorageInsightsDatasetConfigIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageInsightsDatasetConfigIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6638d86908536d91ffa07842602a743bf025d38a7c42b421f4582958924f93a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={"cloud_storage_buckets": "cloudStorageBuckets"},
)
class GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets:
    def __init__(
        self,
        *,
        cloud_storage_buckets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param cloud_storage_buckets: cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#cloud_storage_buckets GoogleStorageInsightsDatasetConfig#cloud_storage_buckets}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__345fe3789dbc75fa4286637984653cda53b6a4ed1f8beb7791885cd301ae2327)
            check_type(argname="argument cloud_storage_buckets", value=cloud_storage_buckets, expected_type=type_hints["cloud_storage_buckets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_storage_buckets": cloud_storage_buckets,
        }

    @builtins.property
    def cloud_storage_buckets(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets"]]:
        '''cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#cloud_storage_buckets GoogleStorageInsightsDatasetConfig#cloud_storage_buckets}
        '''
        result = self._values.get("cloud_storage_buckets")
        assert result is not None, "Required property 'cloud_storage_buckets' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix_regex": "bucketPrefixRegex",
    },
)
class GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: The list of cloud storage bucket names to include in the DatasetConfig. Exactly one of the bucket_name and bucket_prefix_regex should be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#bucket_name GoogleStorageInsightsDatasetConfig#bucket_name}
        :param bucket_prefix_regex: The list of regex patterns for bucket names matching the regex. Regex should follow the syntax specified in google/re2 on GitHub. Exactly one of the bucket_name and bucket_prefix_regex should be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#bucket_prefix_regex GoogleStorageInsightsDatasetConfig#bucket_prefix_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b689bba9ead346e3704037bc1fbcf0a8bd737d1b80620bd35f7adaa2ac668853)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#bucket_name GoogleStorageInsightsDatasetConfig#bucket_name}
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix_regex(self) -> typing.Optional[builtins.str]:
        '''The list of regex patterns for bucket names matching the regex.

        Regex should follow the syntax specified in google/re2 on GitHub.
        Exactly one of the bucket_name and bucket_prefix_regex should be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#bucket_prefix_regex GoogleStorageInsightsDatasetConfig#bucket_prefix_regex}
        '''
        result = self._values.get("bucket_prefix_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__973635765865a1fef1c5f477e14b4a62ff657f148e7f5f7ed1f62f378ef5c92d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__711f3c7ae32e494c88399d7dc0a3553cf123018ee3fadb2ac6341c91b9f366bc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f43c32c0f62b74fe30d2eff15d0b69ea5db775215e4326ba5f08693b0ed7fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f3c8307c7076b0803538a51e95a341c243a4806287815e376afe8ab3bc41a31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84a729009e21de641aae874e99f154be018ff73eda0380990b6da94ea3625977)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c91cd81f2c5121d103c75c3e4f2eeddb8a7b6c5f6707eb35cebb8ac2df99052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c755dd1fdce5ab3e81ee7715d2b6ade932bd46b113863f2b4ea7190d0b609be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac6d4379fd2b01a28f0d60273a0a2fb18b8da0d05ec01a95c2a16c6e36b1a132)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixRegex")
    def bucket_prefix_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefixRegex"))

    @bucket_prefix_regex.setter
    def bucket_prefix_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a892f2ebea9dd846f531d7f28c1d64a98222848811d1a50fc329111fe2fd40df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefixRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1faf8bfe0f17a888f903811a219fb46cef073b6bc225e00c3a71b6e8b43af236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fc3127d304de33d0a30f5520ea13e3bffbb8c3f0bed3fb0b3da74a51d09905c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudStorageBuckets")
    def put_cloud_storage_buckets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c47e91c64ee91ece35ebcb75591780234e77a83bfed4f20888a7f57b48b676d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCloudStorageBuckets", [value]))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageBuckets")
    def cloud_storage_buckets(
        self,
    ) -> GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsList:
        return typing.cast(GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsList, jsii.get(self, "cloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageBucketsInput")
    def cloud_storage_buckets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]]], jsii.get(self, "cloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets]:
        return typing.cast(typing.Optional[GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__925c7479ae6039d52c614f12aaba64eaf1c1904c4ef6cf4febf9b727e3f2714b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations",
    jsii_struct_bases=[],
    name_mapping={"locations": "locations"},
)
class GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations:
    def __init__(self, *, locations: typing.Sequence[builtins.str]) -> None:
        '''
        :param locations: The list of cloud storage locations to include in the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#locations GoogleStorageInsightsDatasetConfig#locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc50499ba2815513487f33fb587a2914afc170ce042216e23385852ead38540d)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locations": locations,
        }

    @builtins.property
    def locations(self) -> typing.List[builtins.str]:
        '''The list of cloud storage locations to include in the DatasetConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#locations GoogleStorageInsightsDatasetConfig#locations}
        '''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0212d7f611c6257ed79df109f94267e701dea5c03584f07adb84a231f27b2c89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b426ba7ee4bf1be80356ccf7c3359c84be377d7540e7dfccc70f36ce893fb167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations]:
        return typing.cast(typing.Optional[GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2b5b3aceead9977f91c1f7b29914d2b72bfe9840e1cd43946b94235ae03fff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigLink",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleStorageInsightsDatasetConfigLink:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsDatasetConfigLink(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageInsightsDatasetConfigLinkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigLinkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a4dbf388ea398bac5cad873aee11ab75762f74355c56ff162a31da4c8cd76ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleStorageInsightsDatasetConfigLinkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3353a7aa9320bdf14b58e36f1f55e9a535409c2bedb13a01967203ac67ec016)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleStorageInsightsDatasetConfigLinkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25b4dde420f34165766d293aa376acf1ae5f7a3707070b8b0501e73e6e18e614)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01540573e861e0667c51d245aac9ef30218a30ea35b81971b8d337358fab4cd3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2ce06d49fbc4a6c31dce68f81b8024c69fc3448e59f0fca6a9c2b0edab3fb61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleStorageInsightsDatasetConfigLinkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigLinkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28875b53d91a0384ff3e8f10be2a2fbd0d0a5910b28a1432d806d0c7535c245c)
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
    def internal_value(self) -> typing.Optional[GoogleStorageInsightsDatasetConfigLink]:
        return typing.cast(typing.Optional[GoogleStorageInsightsDatasetConfigLink], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageInsightsDatasetConfigLink],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528602463ba970c526ff2ea6b3beabed317d07dcead34332206e985a88b572ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigSourceFolders",
    jsii_struct_bases=[],
    name_mapping={"folder_numbers": "folderNumbers"},
)
class GoogleStorageInsightsDatasetConfigSourceFolders:
    def __init__(
        self,
        *,
        folder_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param folder_numbers: The list of folder numbers to include in the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#folder_numbers GoogleStorageInsightsDatasetConfig#folder_numbers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba87af63de60d7d5f195d3e0eb0a5a02a6f7bb0ce3943601b6ca4deeeeaadb28)
            check_type(argname="argument folder_numbers", value=folder_numbers, expected_type=type_hints["folder_numbers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if folder_numbers is not None:
            self._values["folder_numbers"] = folder_numbers

    @builtins.property
    def folder_numbers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of folder numbers to include in the DatasetConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#folder_numbers GoogleStorageInsightsDatasetConfig#folder_numbers}
        '''
        result = self._values.get("folder_numbers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsDatasetConfigSourceFolders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageInsightsDatasetConfigSourceFoldersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigSourceFoldersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23688b196e3b248325ad0bca78144f2af931b926255e51a2b4a60a4604d93784)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9904e556bcf028eec118c1b4fccc3dc1e7b9a9abd1a557987b272135b414d76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "folderNumbers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageInsightsDatasetConfigSourceFolders]:
        return typing.cast(typing.Optional[GoogleStorageInsightsDatasetConfigSourceFolders], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageInsightsDatasetConfigSourceFolders],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0a93c36e382e136470addb36275da41ee811955f2598131af002b357bf708f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigSourceProjects",
    jsii_struct_bases=[],
    name_mapping={"project_numbers": "projectNumbers"},
)
class GoogleStorageInsightsDatasetConfigSourceProjects:
    def __init__(
        self,
        *,
        project_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param project_numbers: The list of project numbers to include in the DatasetConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#project_numbers GoogleStorageInsightsDatasetConfig#project_numbers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1af58a9a559e3f0915766183ae551ab47ad7ba31e7bafb26cd1e9912a336058)
            check_type(argname="argument project_numbers", value=project_numbers, expected_type=type_hints["project_numbers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if project_numbers is not None:
            self._values["project_numbers"] = project_numbers

    @builtins.property
    def project_numbers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of project numbers to include in the DatasetConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#project_numbers GoogleStorageInsightsDatasetConfig#project_numbers}
        '''
        result = self._values.get("project_numbers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsDatasetConfigSourceProjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageInsightsDatasetConfigSourceProjectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigSourceProjectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__628a884a04e84ce11cfbe3349fb008a23295d937ef13e68778415eb93ad35aec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76eed21f219e32fc956a6e4dc04157e5af19e7cee913da4755f992457b8743a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectNumbers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageInsightsDatasetConfigSourceProjects]:
        return typing.cast(typing.Optional[GoogleStorageInsightsDatasetConfigSourceProjects], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageInsightsDatasetConfigSourceProjects],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c8e5687aa1d60bdb933394a2ebfdf9a53d0732a5ece79c6b562b8b7f97bb39f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleStorageInsightsDatasetConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#create GoogleStorageInsightsDatasetConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#delete GoogleStorageInsightsDatasetConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#update GoogleStorageInsightsDatasetConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e09f9620a47730eec8271afc7a70104cb01d681d138a28a8526c4f692dcf2373)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#create GoogleStorageInsightsDatasetConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#delete GoogleStorageInsightsDatasetConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_storage_insights_dataset_config#update GoogleStorageInsightsDatasetConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsDatasetConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageInsightsDatasetConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsDatasetConfig.GoogleStorageInsightsDatasetConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d355df54431b6efdba5a2c1b085accce7a0cdb072b950c00a6715c42038ddfb4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a66b204ca2d12c7a649a7f8b6c202e4c0346bc41517cdbc2a105c5f90203c540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316e0af0aeec26a15f53e14aa0f25cccc95b05de6b637194233ae773315d7981)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ebb78f5f04be6b2c72f964fb23b6dee39f62496cd093d5d0559500d940675c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageInsightsDatasetConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageInsightsDatasetConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageInsightsDatasetConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e28370f198313814325e087be38c4cf9878c22d260c0e18580c2fd777f10d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleStorageInsightsDatasetConfig",
    "GoogleStorageInsightsDatasetConfigConfig",
    "GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets",
    "GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets",
    "GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsList",
    "GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBucketsOutputReference",
    "GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsOutputReference",
    "GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations",
    "GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocationsOutputReference",
    "GoogleStorageInsightsDatasetConfigIdentity",
    "GoogleStorageInsightsDatasetConfigIdentityOutputReference",
    "GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets",
    "GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets",
    "GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsList",
    "GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBucketsOutputReference",
    "GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsOutputReference",
    "GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations",
    "GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocationsOutputReference",
    "GoogleStorageInsightsDatasetConfigLink",
    "GoogleStorageInsightsDatasetConfigLinkList",
    "GoogleStorageInsightsDatasetConfigLinkOutputReference",
    "GoogleStorageInsightsDatasetConfigSourceFolders",
    "GoogleStorageInsightsDatasetConfigSourceFoldersOutputReference",
    "GoogleStorageInsightsDatasetConfigSourceProjects",
    "GoogleStorageInsightsDatasetConfigSourceProjectsOutputReference",
    "GoogleStorageInsightsDatasetConfigTimeouts",
    "GoogleStorageInsightsDatasetConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__dd118eda5ec27b17ad5423292711c5faeae6271902b34f879dce6936f348d7f4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dataset_config_id: builtins.str,
    identity: typing.Union[GoogleStorageInsightsDatasetConfigIdentity, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    retention_period_days: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    exclude_cloud_storage_buckets: typing.Optional[typing.Union[GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude_cloud_storage_locations: typing.Optional[typing.Union[GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    include_cloud_storage_buckets: typing.Optional[typing.Union[GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    include_cloud_storage_locations: typing.Optional[typing.Union[GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
    include_newly_created_buckets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    link_dataset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    organization_number: typing.Optional[builtins.str] = None,
    organization_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    source_folders: typing.Optional[typing.Union[GoogleStorageInsightsDatasetConfigSourceFolders, typing.Dict[builtins.str, typing.Any]]] = None,
    source_projects: typing.Optional[typing.Union[GoogleStorageInsightsDatasetConfigSourceProjects, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleStorageInsightsDatasetConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__dfe935ce3479a8f6b03be3f402901d84d6f268f94f18c2ccc2eb93b16129d4ec(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dda24f4b7043f732e5b2d291c16d0ca74faaa69185da1d2c0f8a4561b888a1b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391db625efb3e8ef6a9c7a4e45e0fa87bc70a87bba9fd7f04e6d9c1b108ee0d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ec6ae01fc021118f999c0fc06310b056380fec1a1c70621526494dc06f5a41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dcb3191d50bf2eb62b9842655e264cc6edbb752bcfc3419c13ad188cd361715(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8796847910a585a94edccd053f80fbd4a84de9d1c2c2b56e481db3c6cf5b9ca(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ecd6975f2efb3eda81a915713ef1c66289eb190a1931e83e6a42ef0be4d7ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b391342337bdffc4bddba4d10587a9289f539c320eba6cf2e0988d3f69ca18b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e72c9821646781c3b7e4ec169a1d6cb354de58d12f76571b19b25948ffc53d9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffba5cbf9e84b468cec30f13de9623e7d8ff4ba81ee7be7d62f68b52af0b7b42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e128d329254e2dc3ad364c9e39b9038d2b340409c2eddb4e8ef66dc02a26e19(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ae42f51a359f6225fa5fc4f8155a3ba10042e5f5bb4ae0f74f5aebd5ac4264(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dataset_config_id: builtins.str,
    identity: typing.Union[GoogleStorageInsightsDatasetConfigIdentity, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    retention_period_days: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    exclude_cloud_storage_buckets: typing.Optional[typing.Union[GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude_cloud_storage_locations: typing.Optional[typing.Union[GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    include_cloud_storage_buckets: typing.Optional[typing.Union[GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    include_cloud_storage_locations: typing.Optional[typing.Union[GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
    include_newly_created_buckets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    link_dataset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    organization_number: typing.Optional[builtins.str] = None,
    organization_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    source_folders: typing.Optional[typing.Union[GoogleStorageInsightsDatasetConfigSourceFolders, typing.Dict[builtins.str, typing.Any]]] = None,
    source_projects: typing.Optional[typing.Union[GoogleStorageInsightsDatasetConfigSourceProjects, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleStorageInsightsDatasetConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e90968b9fb1240652adda4c36827e326d1a6c2e5e6212b6824e12b80c48002(
    *,
    cloud_storage_buckets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e604ea889bcacbd43ce70c90f37f9f36b2d0fa717e0bf28cc3e62a7a83099d(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f7313797c2c8d5ce0f09326b600e7e2704059760e475018d826effe9da01f51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c13e33a074deb6ff5d442b51c016f57b1a1b07a3b8b373dc95af9a7caafdc3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d79a539766ec46a8b6c29283bcdfd3548899ac0e97a68550280170f9efe4b53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def83e981c44179732b6949d0a4960b4e3a9ae6a7c681be9d15ae167f24e0182(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5517d7c14f12c4a7ea9a504b3daadc3ffcd35e5e8b30ba50516892dd3e23dd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c93c5f825145b53e45c330ec813100aba0c5f158fd912c1ae3b4ce2f70676974(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db40566d561346acb7e6857215cd21c147adaa068c5eab6d5f4edfa2e8a86363(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73fc8dd573bef342414842daba187060aa5687e636252a94957603a498dc8f01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b84ecc769cc475b5dd953013681b7653037be19b3eca53a82637b0f1959d011(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c0bbab75a3a396d9328a5abc302b6b45da80e5195a3b163046eedf7d1a9ccd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d161fe7e1ecb0c3a652dc09cf5b718348827b9950d385c987418e11e0c2c9ecc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75f00352310754072a4e4043aa707b5763f01b3a68f5d31730ac2bf0da0ce9ff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleStorageInsightsDatasetConfigExcludeCloudStorageBucketsCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49462869d56c9c1f745f4a0d5c750548e8552320abf422178c3cb498180516a7(
    value: typing.Optional[GoogleStorageInsightsDatasetConfigExcludeCloudStorageBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e21effbe1393d80714a5c8110878219dec58dc1f3d348c6a4fe46514bc3764c(
    *,
    locations: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463ac6223cf7b7d24b04253886ebc793a7ba504f86a6a1eb4a85178f4e2ee13a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e07c946cf43f91b29d15a27637b50f18beb47aa5052bf9608e443f3f84b8db(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89345e7e7c39df391a334a0529b30a7c0342150c7050f5ff6ab9275652c4eeca(
    value: typing.Optional[GoogleStorageInsightsDatasetConfigExcludeCloudStorageLocations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd6295a717d819b3ba478565909190b5771de4b3d9f1142f9be26182096dc07c(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c87790ae8c426bf0d269d38f4d915a9799089ea80c71df33c6e837ea4fe042(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fac4ed3eed1881c19463894cdd642f633dc78a511c7dfaf6ca4095d1d6547af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6638d86908536d91ffa07842602a743bf025d38a7c42b421f4582958924f93a(
    value: typing.Optional[GoogleStorageInsightsDatasetConfigIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345fe3789dbc75fa4286637984653cda53b6a4ed1f8beb7791885cd301ae2327(
    *,
    cloud_storage_buckets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b689bba9ead346e3704037bc1fbcf0a8bd737d1b80620bd35f7adaa2ac668853(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973635765865a1fef1c5f477e14b4a62ff657f148e7f5f7ed1f62f378ef5c92d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711f3c7ae32e494c88399d7dc0a3553cf123018ee3fadb2ac6341c91b9f366bc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f43c32c0f62b74fe30d2eff15d0b69ea5db775215e4326ba5f08693b0ed7fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3c8307c7076b0803538a51e95a341c243a4806287815e376afe8ab3bc41a31(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a729009e21de641aae874e99f154be018ff73eda0380990b6da94ea3625977(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c91cd81f2c5121d103c75c3e4f2eeddb8a7b6c5f6707eb35cebb8ac2df99052(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c755dd1fdce5ab3e81ee7715d2b6ade932bd46b113863f2b4ea7190d0b609be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6d4379fd2b01a28f0d60273a0a2fb18b8da0d05ec01a95c2a16c6e36b1a132(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a892f2ebea9dd846f531d7f28c1d64a98222848811d1a50fc329111fe2fd40df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1faf8bfe0f17a888f903811a219fb46cef073b6bc225e00c3a71b6e8b43af236(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc3127d304de33d0a30f5520ea13e3bffbb8c3f0bed3fb0b3da74a51d09905c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c47e91c64ee91ece35ebcb75591780234e77a83bfed4f20888a7f57b48b676d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleStorageInsightsDatasetConfigIncludeCloudStorageBucketsCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__925c7479ae6039d52c614f12aaba64eaf1c1904c4ef6cf4febf9b727e3f2714b(
    value: typing.Optional[GoogleStorageInsightsDatasetConfigIncludeCloudStorageBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc50499ba2815513487f33fb587a2914afc170ce042216e23385852ead38540d(
    *,
    locations: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0212d7f611c6257ed79df109f94267e701dea5c03584f07adb84a231f27b2c89(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b426ba7ee4bf1be80356ccf7c3359c84be377d7540e7dfccc70f36ce893fb167(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2b5b3aceead9977f91c1f7b29914d2b72bfe9840e1cd43946b94235ae03fff(
    value: typing.Optional[GoogleStorageInsightsDatasetConfigIncludeCloudStorageLocations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4dbf388ea398bac5cad873aee11ab75762f74355c56ff162a31da4c8cd76ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3353a7aa9320bdf14b58e36f1f55e9a535409c2bedb13a01967203ac67ec016(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b4dde420f34165766d293aa376acf1ae5f7a3707070b8b0501e73e6e18e614(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01540573e861e0667c51d245aac9ef30218a30ea35b81971b8d337358fab4cd3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ce06d49fbc4a6c31dce68f81b8024c69fc3448e59f0fca6a9c2b0edab3fb61(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28875b53d91a0384ff3e8f10be2a2fbd0d0a5910b28a1432d806d0c7535c245c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528602463ba970c526ff2ea6b3beabed317d07dcead34332206e985a88b572ce(
    value: typing.Optional[GoogleStorageInsightsDatasetConfigLink],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba87af63de60d7d5f195d3e0eb0a5a02a6f7bb0ce3943601b6ca4deeeeaadb28(
    *,
    folder_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23688b196e3b248325ad0bca78144f2af931b926255e51a2b4a60a4604d93784(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9904e556bcf028eec118c1b4fccc3dc1e7b9a9abd1a557987b272135b414d76(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0a93c36e382e136470addb36275da41ee811955f2598131af002b357bf708f(
    value: typing.Optional[GoogleStorageInsightsDatasetConfigSourceFolders],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1af58a9a559e3f0915766183ae551ab47ad7ba31e7bafb26cd1e9912a336058(
    *,
    project_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__628a884a04e84ce11cfbe3349fb008a23295d937ef13e68778415eb93ad35aec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76eed21f219e32fc956a6e4dc04157e5af19e7cee913da4755f992457b8743a0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8e5687aa1d60bdb933394a2ebfdf9a53d0732a5ece79c6b562b8b7f97bb39f(
    value: typing.Optional[GoogleStorageInsightsDatasetConfigSourceProjects],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09f9620a47730eec8271afc7a70104cb01d681d138a28a8526c4f692dcf2373(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d355df54431b6efdba5a2c1b085accce7a0cdb072b950c00a6715c42038ddfb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66b204ca2d12c7a649a7f8b6c202e4c0346bc41517cdbc2a105c5f90203c540(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316e0af0aeec26a15f53e14aa0f25cccc95b05de6b637194233ae773315d7981(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ebb78f5f04be6b2c72f964fb23b6dee39f62496cd093d5d0559500d940675c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e28370f198313814325e087be38c4cf9878c22d260c0e18580c2fd777f10d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageInsightsDatasetConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

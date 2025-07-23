r'''
# `google_dataplex_asset`

Refer to the Terraform Registry for docs: [`google_dataplex_asset`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset).
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


class DataplexAsset(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAsset",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset google_dataplex_asset}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dataplex_zone: builtins.str,
        discovery_spec: typing.Union["DataplexAssetDiscoverySpec", typing.Dict[builtins.str, typing.Any]],
        lake: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_spec: typing.Union["DataplexAssetResourceSpec", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataplexAssetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset google_dataplex_asset} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dataplex_zone: The zone for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#dataplex_zone DataplexAsset#dataplex_zone}
        :param discovery_spec: discovery_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#discovery_spec DataplexAsset#discovery_spec}
        :param lake: The lake for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#lake DataplexAsset#lake}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#location DataplexAsset#location}
        :param name: The name of the asset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#name DataplexAsset#name}
        :param resource_spec: resource_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#resource_spec DataplexAsset#resource_spec}
        :param description: Optional. Description of the asset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#description DataplexAsset#description}
        :param display_name: Optional. User friendly display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#display_name DataplexAsset#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#id DataplexAsset#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. User defined labels for the asset. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#labels DataplexAsset#labels}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#project DataplexAsset#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#timeouts DataplexAsset#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9b831e76e14625eedef469ef1a19154806d5ed5048d825e14b3fc69a87ba7a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataplexAssetConfig(
            dataplex_zone=dataplex_zone,
            discovery_spec=discovery_spec,
            lake=lake,
            location=location,
            name=name,
            resource_spec=resource_spec,
            description=description,
            display_name=display_name,
            id=id,
            labels=labels,
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
        '''Generates CDKTF code for importing a DataplexAsset resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataplexAsset to import.
        :param import_from_id: The id of the existing DataplexAsset that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataplexAsset to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d9dfaf354a395bafaeb4f6be9644d5fcd240d4c88d96273c246909e5bef9edf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDiscoverySpec")
    def put_discovery_spec(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        csv_options: typing.Optional[typing.Union["DataplexAssetDiscoverySpecCsvOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        json_options: typing.Optional[typing.Union["DataplexAssetDiscoverySpecJsonOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Required. Whether discovery is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#enabled DataplexAsset#enabled}
        :param csv_options: csv_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#csv_options DataplexAsset#csv_options}
        :param exclude_patterns: Optional. The list of patterns to apply for selecting data to exclude during discovery. For Cloud Storage bucket assets, these are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these are interpreted as patterns to match table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#exclude_patterns DataplexAsset#exclude_patterns}
        :param include_patterns: Optional. The list of patterns to apply for selecting data to include during discovery if only a subset of the data should considered. For Cloud Storage bucket assets, these are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these are interpreted as patterns to match table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#include_patterns DataplexAsset#include_patterns}
        :param json_options: json_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#json_options DataplexAsset#json_options}
        :param schedule: Optional. Cron schedule (https://en.wikipedia.org/wiki/Cron) for running discovery periodically. Successive discovery runs must be scheduled at least 60 minutes apart. The default value is to run discovery every 60 minutes. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: "CRON_TZ=${IANA_TIME_ZONE}" or TZ=${IANA_TIME_ZONE}". The ${IANA_TIME_ZONE} may only be a valid string from IANA time zone database. For example, "CRON_TZ=America/New_York 1 * * * *", or "TZ=America/New_York 1 * * * *". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#schedule DataplexAsset#schedule}
        '''
        value = DataplexAssetDiscoverySpec(
            enabled=enabled,
            csv_options=csv_options,
            exclude_patterns=exclude_patterns,
            include_patterns=include_patterns,
            json_options=json_options,
            schedule=schedule,
        )

        return typing.cast(None, jsii.invoke(self, "putDiscoverySpec", [value]))

    @jsii.member(jsii_name="putResourceSpec")
    def put_resource_spec(
        self,
        *,
        type: builtins.str,
        name: typing.Optional[builtins.str] = None,
        read_access_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Required. Immutable. Type of resource. Possible values: STORAGE_BUCKET, BIGQUERY_DATASET. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#type DataplexAsset#type}
        :param name: Immutable. Relative name of the cloud resource that contains the data that is being managed within a lake. For example: ``projects/{project_number}/buckets/{bucket_id}`` ``projects/{project_number}/datasets/{dataset_id}`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#name DataplexAsset#name}
        :param read_access_mode: Optional. Determines how read permissions are handled for each asset and their associated tables. Only available to storage buckets assets. Possible values: DIRECT, MANAGED Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#read_access_mode DataplexAsset#read_access_mode}
        '''
        value = DataplexAssetResourceSpec(
            type=type, name=name, read_access_mode=read_access_mode
        )

        return typing.cast(None, jsii.invoke(self, "putResourceSpec", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#create DataplexAsset#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#delete DataplexAsset#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#update DataplexAsset#update}.
        '''
        value = DataplexAssetTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="discoverySpec")
    def discovery_spec(self) -> "DataplexAssetDiscoverySpecOutputReference":
        return typing.cast("DataplexAssetDiscoverySpecOutputReference", jsii.get(self, "discoverySpec"))

    @builtins.property
    @jsii.member(jsii_name="discoveryStatus")
    def discovery_status(self) -> "DataplexAssetDiscoveryStatusList":
        return typing.cast("DataplexAssetDiscoveryStatusList", jsii.get(self, "discoveryStatus"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="resourceSpec")
    def resource_spec(self) -> "DataplexAssetResourceSpecOutputReference":
        return typing.cast("DataplexAssetResourceSpecOutputReference", jsii.get(self, "resourceSpec"))

    @builtins.property
    @jsii.member(jsii_name="resourceStatus")
    def resource_status(self) -> "DataplexAssetResourceStatusList":
        return typing.cast("DataplexAssetResourceStatusList", jsii.get(self, "resourceStatus"))

    @builtins.property
    @jsii.member(jsii_name="securityStatus")
    def security_status(self) -> "DataplexAssetSecurityStatusList":
        return typing.cast("DataplexAssetSecurityStatusList", jsii.get(self, "securityStatus"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataplexAssetTimeoutsOutputReference":
        return typing.cast("DataplexAssetTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="dataplexZoneInput")
    def dataplex_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataplexZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="discoverySpecInput")
    def discovery_spec_input(self) -> typing.Optional["DataplexAssetDiscoverySpec"]:
        return typing.cast(typing.Optional["DataplexAssetDiscoverySpec"], jsii.get(self, "discoverySpecInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="lakeInput")
    def lake_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lakeInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceSpecInput")
    def resource_spec_input(self) -> typing.Optional["DataplexAssetResourceSpec"]:
        return typing.cast(typing.Optional["DataplexAssetResourceSpec"], jsii.get(self, "resourceSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataplexAssetTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataplexAssetTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataplexZone")
    def dataplex_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataplexZone"))

    @dataplex_zone.setter
    def dataplex_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46e4e9995f38d33874a2a30e17cc21d6268cddb09f4abed18289c967482fbce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataplexZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e21edcae6cc3b82cc08997b89d3d6c456ce2e167d950ce5cc0aa15800ac9f238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e702e06faef2d342e354ab1f6300bebbed5ec9a208441cfd826430f6a7db16b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__215a9eef775c2b7a0644e56caf4c61088da11fd682ddcbcccae83c5a9a10452f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc0a56a9792abb01120bdb8bc1103d05d6d4532ebd364a44c1a7e6bca93a158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lake")
    def lake(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lake"))

    @lake.setter
    def lake(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f6311faa21da640b6902091809eb392daafd380fbd4832802b2813fd0c7ac8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lake", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ac44aa535ca51bf3ebdac97a92ee06bb8681bca5403d15aa5d68db095dcb2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e4cc735b0f0e40831c54715231c7cbe93311c590c1f0a9e40442e9740b5f745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba44b197c87c85e05b14d9d264c9f02f07da21151ecc7b4211be58f4ab691df2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dataplex_zone": "dataplexZone",
        "discovery_spec": "discoverySpec",
        "lake": "lake",
        "location": "location",
        "name": "name",
        "resource_spec": "resourceSpec",
        "description": "description",
        "display_name": "displayName",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class DataplexAssetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dataplex_zone: builtins.str,
        discovery_spec: typing.Union["DataplexAssetDiscoverySpec", typing.Dict[builtins.str, typing.Any]],
        lake: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_spec: typing.Union["DataplexAssetResourceSpec", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataplexAssetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dataplex_zone: The zone for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#dataplex_zone DataplexAsset#dataplex_zone}
        :param discovery_spec: discovery_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#discovery_spec DataplexAsset#discovery_spec}
        :param lake: The lake for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#lake DataplexAsset#lake}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#location DataplexAsset#location}
        :param name: The name of the asset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#name DataplexAsset#name}
        :param resource_spec: resource_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#resource_spec DataplexAsset#resource_spec}
        :param description: Optional. Description of the asset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#description DataplexAsset#description}
        :param display_name: Optional. User friendly display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#display_name DataplexAsset#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#id DataplexAsset#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. User defined labels for the asset. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#labels DataplexAsset#labels}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#project DataplexAsset#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#timeouts DataplexAsset#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(discovery_spec, dict):
            discovery_spec = DataplexAssetDiscoverySpec(**discovery_spec)
        if isinstance(resource_spec, dict):
            resource_spec = DataplexAssetResourceSpec(**resource_spec)
        if isinstance(timeouts, dict):
            timeouts = DataplexAssetTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a616f0134251f5edeb30b0170b886b2d620286b5976e1cd3465edd89d3a18749)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dataplex_zone", value=dataplex_zone, expected_type=type_hints["dataplex_zone"])
            check_type(argname="argument discovery_spec", value=discovery_spec, expected_type=type_hints["discovery_spec"])
            check_type(argname="argument lake", value=lake, expected_type=type_hints["lake"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_spec", value=resource_spec, expected_type=type_hints["resource_spec"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataplex_zone": dataplex_zone,
            "discovery_spec": discovery_spec,
            "lake": lake,
            "location": location,
            "name": name,
            "resource_spec": resource_spec,
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
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
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
    def dataplex_zone(self) -> builtins.str:
        '''The zone for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#dataplex_zone DataplexAsset#dataplex_zone}
        '''
        result = self._values.get("dataplex_zone")
        assert result is not None, "Required property 'dataplex_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def discovery_spec(self) -> "DataplexAssetDiscoverySpec":
        '''discovery_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#discovery_spec DataplexAsset#discovery_spec}
        '''
        result = self._values.get("discovery_spec")
        assert result is not None, "Required property 'discovery_spec' is missing"
        return typing.cast("DataplexAssetDiscoverySpec", result)

    @builtins.property
    def lake(self) -> builtins.str:
        '''The lake for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#lake DataplexAsset#lake}
        '''
        result = self._values.get("lake")
        assert result is not None, "Required property 'lake' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#location DataplexAsset#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the asset.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#name DataplexAsset#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_spec(self) -> "DataplexAssetResourceSpec":
        '''resource_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#resource_spec DataplexAsset#resource_spec}
        '''
        result = self._values.get("resource_spec")
        assert result is not None, "Required property 'resource_spec' is missing"
        return typing.cast("DataplexAssetResourceSpec", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Description of the asset.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#description DataplexAsset#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Optional. User friendly display name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#display_name DataplexAsset#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#id DataplexAsset#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. User defined labels for the asset.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field ``effective_labels`` for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#labels DataplexAsset#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#project DataplexAsset#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataplexAssetTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#timeouts DataplexAsset#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataplexAssetTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexAssetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetDiscoverySpec",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "csv_options": "csvOptions",
        "exclude_patterns": "excludePatterns",
        "include_patterns": "includePatterns",
        "json_options": "jsonOptions",
        "schedule": "schedule",
    },
)
class DataplexAssetDiscoverySpec:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        csv_options: typing.Optional[typing.Union["DataplexAssetDiscoverySpecCsvOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        json_options: typing.Optional[typing.Union["DataplexAssetDiscoverySpecJsonOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Required. Whether discovery is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#enabled DataplexAsset#enabled}
        :param csv_options: csv_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#csv_options DataplexAsset#csv_options}
        :param exclude_patterns: Optional. The list of patterns to apply for selecting data to exclude during discovery. For Cloud Storage bucket assets, these are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these are interpreted as patterns to match table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#exclude_patterns DataplexAsset#exclude_patterns}
        :param include_patterns: Optional. The list of patterns to apply for selecting data to include during discovery if only a subset of the data should considered. For Cloud Storage bucket assets, these are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these are interpreted as patterns to match table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#include_patterns DataplexAsset#include_patterns}
        :param json_options: json_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#json_options DataplexAsset#json_options}
        :param schedule: Optional. Cron schedule (https://en.wikipedia.org/wiki/Cron) for running discovery periodically. Successive discovery runs must be scheduled at least 60 minutes apart. The default value is to run discovery every 60 minutes. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: "CRON_TZ=${IANA_TIME_ZONE}" or TZ=${IANA_TIME_ZONE}". The ${IANA_TIME_ZONE} may only be a valid string from IANA time zone database. For example, "CRON_TZ=America/New_York 1 * * * *", or "TZ=America/New_York 1 * * * *". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#schedule DataplexAsset#schedule}
        '''
        if isinstance(csv_options, dict):
            csv_options = DataplexAssetDiscoverySpecCsvOptions(**csv_options)
        if isinstance(json_options, dict):
            json_options = DataplexAssetDiscoverySpecJsonOptions(**json_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__738c53360759489a8b68fb55b56370fc4b5800ab059bfd01ebecfff6e9728f0a)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument csv_options", value=csv_options, expected_type=type_hints["csv_options"])
            check_type(argname="argument exclude_patterns", value=exclude_patterns, expected_type=type_hints["exclude_patterns"])
            check_type(argname="argument include_patterns", value=include_patterns, expected_type=type_hints["include_patterns"])
            check_type(argname="argument json_options", value=json_options, expected_type=type_hints["json_options"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if csv_options is not None:
            self._values["csv_options"] = csv_options
        if exclude_patterns is not None:
            self._values["exclude_patterns"] = exclude_patterns
        if include_patterns is not None:
            self._values["include_patterns"] = include_patterns
        if json_options is not None:
            self._values["json_options"] = json_options
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Required. Whether discovery is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#enabled DataplexAsset#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def csv_options(self) -> typing.Optional["DataplexAssetDiscoverySpecCsvOptions"]:
        '''csv_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#csv_options DataplexAsset#csv_options}
        '''
        result = self._values.get("csv_options")
        return typing.cast(typing.Optional["DataplexAssetDiscoverySpecCsvOptions"], result)

    @builtins.property
    def exclude_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        The list of patterns to apply for selecting data to exclude during discovery. For Cloud Storage bucket assets, these are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these are interpreted as patterns to match table names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#exclude_patterns DataplexAsset#exclude_patterns}
        '''
        result = self._values.get("exclude_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        The list of patterns to apply for selecting data to include during discovery if only a subset of the data should considered. For Cloud Storage bucket assets, these are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these are interpreted as patterns to match table names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#include_patterns DataplexAsset#include_patterns}
        '''
        result = self._values.get("include_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def json_options(self) -> typing.Optional["DataplexAssetDiscoverySpecJsonOptions"]:
        '''json_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#json_options DataplexAsset#json_options}
        '''
        result = self._values.get("json_options")
        return typing.cast(typing.Optional["DataplexAssetDiscoverySpecJsonOptions"], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Cron schedule (https://en.wikipedia.org/wiki/Cron) for running discovery periodically. Successive discovery runs must be scheduled at least 60 minutes apart. The default value is to run discovery every 60 minutes. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: "CRON_TZ=${IANA_TIME_ZONE}" or TZ=${IANA_TIME_ZONE}". The ${IANA_TIME_ZONE} may only be a valid string from IANA time zone database. For example, "CRON_TZ=America/New_York 1 * * * *", or "TZ=America/New_York 1 * * * *".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#schedule DataplexAsset#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexAssetDiscoverySpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetDiscoverySpecCsvOptions",
    jsii_struct_bases=[],
    name_mapping={
        "delimiter": "delimiter",
        "disable_type_inference": "disableTypeInference",
        "encoding": "encoding",
        "header_rows": "headerRows",
    },
)
class DataplexAssetDiscoverySpecCsvOptions:
    def __init__(
        self,
        *,
        delimiter: typing.Optional[builtins.str] = None,
        disable_type_inference: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encoding: typing.Optional[builtins.str] = None,
        header_rows: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delimiter: Optional. The delimiter being used to separate values. This defaults to ','. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#delimiter DataplexAsset#delimiter}
        :param disable_type_inference: Optional. Whether to disable the inference of data type for CSV data. If true, all columns will be registered as strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#disable_type_inference DataplexAsset#disable_type_inference}
        :param encoding: Optional. The character encoding of the data. The default is UTF-8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#encoding DataplexAsset#encoding}
        :param header_rows: Optional. The number of rows to interpret as header rows that should be skipped when reading data rows. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#header_rows DataplexAsset#header_rows}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b7e458f346608fbdc0e7290b7c77117cebc5aa70566bc1ab9110ad27afb95f8)
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
            check_type(argname="argument disable_type_inference", value=disable_type_inference, expected_type=type_hints["disable_type_inference"])
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
            check_type(argname="argument header_rows", value=header_rows, expected_type=type_hints["header_rows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delimiter is not None:
            self._values["delimiter"] = delimiter
        if disable_type_inference is not None:
            self._values["disable_type_inference"] = disable_type_inference
        if encoding is not None:
            self._values["encoding"] = encoding
        if header_rows is not None:
            self._values["header_rows"] = header_rows

    @builtins.property
    def delimiter(self) -> typing.Optional[builtins.str]:
        '''Optional. The delimiter being used to separate values. This defaults to ','.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#delimiter DataplexAsset#delimiter}
        '''
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_type_inference(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Whether to disable the inference of data type for CSV data. If true, all columns will be registered as strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#disable_type_inference DataplexAsset#disable_type_inference}
        '''
        result = self._values.get("disable_type_inference")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''Optional. The character encoding of the data. The default is UTF-8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#encoding DataplexAsset#encoding}
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_rows(self) -> typing.Optional[jsii.Number]:
        '''Optional. The number of rows to interpret as header rows that should be skipped when reading data rows.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#header_rows DataplexAsset#header_rows}
        '''
        result = self._values.get("header_rows")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexAssetDiscoverySpecCsvOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexAssetDiscoverySpecCsvOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetDiscoverySpecCsvOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77982fc804697222f2d341f234b4f19e42ec8ff820d6a82f050bfb2e759d3e97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDelimiter")
    def reset_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelimiter", []))

    @jsii.member(jsii_name="resetDisableTypeInference")
    def reset_disable_type_inference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableTypeInference", []))

    @jsii.member(jsii_name="resetEncoding")
    def reset_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncoding", []))

    @jsii.member(jsii_name="resetHeaderRows")
    def reset_header_rows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderRows", []))

    @builtins.property
    @jsii.member(jsii_name="delimiterInput")
    def delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="disableTypeInferenceInput")
    def disable_type_inference_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableTypeInferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="encodingInput")
    def encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encodingInput"))

    @builtins.property
    @jsii.member(jsii_name="headerRowsInput")
    def header_rows_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "headerRowsInput"))

    @builtins.property
    @jsii.member(jsii_name="delimiter")
    def delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delimiter"))

    @delimiter.setter
    def delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__664b686eea92dc313d3842098ae53f19e66c72e990b23ac1704edb9a1b193d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableTypeInference")
    def disable_type_inference(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableTypeInference"))

    @disable_type_inference.setter
    def disable_type_inference(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebeb0a42622ea0bb1b2b532717c6421db11e0eead4fb84d98b1fc0028c082e0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableTypeInference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @encoding.setter
    def encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b8aebac8166297117c18e054ca0be0952c88575fa7ed35ceb5b8764aa1a6d10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerRows")
    def header_rows(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "headerRows"))

    @header_rows.setter
    def header_rows(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78cf8c909242cf995d181a5641eb90715baa89b90ed0ee67557b38b51bdc1c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerRows", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexAssetDiscoverySpecCsvOptions]:
        return typing.cast(typing.Optional[DataplexAssetDiscoverySpecCsvOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexAssetDiscoverySpecCsvOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb05fc1418d87cb718781c51ab115c4fb4407b59bc0118d367ab2195517f42c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetDiscoverySpecJsonOptions",
    jsii_struct_bases=[],
    name_mapping={
        "disable_type_inference": "disableTypeInference",
        "encoding": "encoding",
    },
)
class DataplexAssetDiscoverySpecJsonOptions:
    def __init__(
        self,
        *,
        disable_type_inference: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encoding: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disable_type_inference: Optional. Whether to disable the inference of data type for Json data. If true, all columns will be registered as their primitive types (strings, number or boolean). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#disable_type_inference DataplexAsset#disable_type_inference}
        :param encoding: Optional. The character encoding of the data. The default is UTF-8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#encoding DataplexAsset#encoding}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80a41e617f4c3716830deb87ccb64a238eaee0eb4d7a2e0b04082e77f1440b8f)
            check_type(argname="argument disable_type_inference", value=disable_type_inference, expected_type=type_hints["disable_type_inference"])
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable_type_inference is not None:
            self._values["disable_type_inference"] = disable_type_inference
        if encoding is not None:
            self._values["encoding"] = encoding

    @builtins.property
    def disable_type_inference(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Whether to disable the inference of data type for Json data. If true, all columns will be registered as their primitive types (strings, number or boolean).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#disable_type_inference DataplexAsset#disable_type_inference}
        '''
        result = self._values.get("disable_type_inference")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''Optional. The character encoding of the data. The default is UTF-8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#encoding DataplexAsset#encoding}
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexAssetDiscoverySpecJsonOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexAssetDiscoverySpecJsonOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetDiscoverySpecJsonOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9909c3c97fc436e71f8758f8c5b7fd8327496442aa78a49b52a5b821857eefe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisableTypeInference")
    def reset_disable_type_inference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableTypeInference", []))

    @jsii.member(jsii_name="resetEncoding")
    def reset_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncoding", []))

    @builtins.property
    @jsii.member(jsii_name="disableTypeInferenceInput")
    def disable_type_inference_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableTypeInferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="encodingInput")
    def encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encodingInput"))

    @builtins.property
    @jsii.member(jsii_name="disableTypeInference")
    def disable_type_inference(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableTypeInference"))

    @disable_type_inference.setter
    def disable_type_inference(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cedf0c531146326e12f3a794180c4002fdfead97ae229e83cb53f34d52c4613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableTypeInference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @encoding.setter
    def encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8083880b9f469285e052ae729db1c668837a950a52137903648bc08a88d82f6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexAssetDiscoverySpecJsonOptions]:
        return typing.cast(typing.Optional[DataplexAssetDiscoverySpecJsonOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexAssetDiscoverySpecJsonOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a2ab6ea03d1f846f8defd36091b5049d43d0a1289505f7c48eba3046d3205c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexAssetDiscoverySpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetDiscoverySpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__967a0ebdfb5a039b6cffd4d3aed36c79423d1466288e06b982e300d3dbb8b1b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCsvOptions")
    def put_csv_options(
        self,
        *,
        delimiter: typing.Optional[builtins.str] = None,
        disable_type_inference: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encoding: typing.Optional[builtins.str] = None,
        header_rows: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delimiter: Optional. The delimiter being used to separate values. This defaults to ','. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#delimiter DataplexAsset#delimiter}
        :param disable_type_inference: Optional. Whether to disable the inference of data type for CSV data. If true, all columns will be registered as strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#disable_type_inference DataplexAsset#disable_type_inference}
        :param encoding: Optional. The character encoding of the data. The default is UTF-8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#encoding DataplexAsset#encoding}
        :param header_rows: Optional. The number of rows to interpret as header rows that should be skipped when reading data rows. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#header_rows DataplexAsset#header_rows}
        '''
        value = DataplexAssetDiscoverySpecCsvOptions(
            delimiter=delimiter,
            disable_type_inference=disable_type_inference,
            encoding=encoding,
            header_rows=header_rows,
        )

        return typing.cast(None, jsii.invoke(self, "putCsvOptions", [value]))

    @jsii.member(jsii_name="putJsonOptions")
    def put_json_options(
        self,
        *,
        disable_type_inference: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encoding: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disable_type_inference: Optional. Whether to disable the inference of data type for Json data. If true, all columns will be registered as their primitive types (strings, number or boolean). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#disable_type_inference DataplexAsset#disable_type_inference}
        :param encoding: Optional. The character encoding of the data. The default is UTF-8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#encoding DataplexAsset#encoding}
        '''
        value = DataplexAssetDiscoverySpecJsonOptions(
            disable_type_inference=disable_type_inference, encoding=encoding
        )

        return typing.cast(None, jsii.invoke(self, "putJsonOptions", [value]))

    @jsii.member(jsii_name="resetCsvOptions")
    def reset_csv_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsvOptions", []))

    @jsii.member(jsii_name="resetExcludePatterns")
    def reset_exclude_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludePatterns", []))

    @jsii.member(jsii_name="resetIncludePatterns")
    def reset_include_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludePatterns", []))

    @jsii.member(jsii_name="resetJsonOptions")
    def reset_json_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonOptions", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @builtins.property
    @jsii.member(jsii_name="csvOptions")
    def csv_options(self) -> DataplexAssetDiscoverySpecCsvOptionsOutputReference:
        return typing.cast(DataplexAssetDiscoverySpecCsvOptionsOutputReference, jsii.get(self, "csvOptions"))

    @builtins.property
    @jsii.member(jsii_name="jsonOptions")
    def json_options(self) -> DataplexAssetDiscoverySpecJsonOptionsOutputReference:
        return typing.cast(DataplexAssetDiscoverySpecJsonOptionsOutputReference, jsii.get(self, "jsonOptions"))

    @builtins.property
    @jsii.member(jsii_name="csvOptionsInput")
    def csv_options_input(
        self,
    ) -> typing.Optional[DataplexAssetDiscoverySpecCsvOptions]:
        return typing.cast(typing.Optional[DataplexAssetDiscoverySpecCsvOptions], jsii.get(self, "csvOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="excludePatternsInput")
    def exclude_patterns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludePatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="includePatternsInput")
    def include_patterns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includePatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonOptionsInput")
    def json_options_input(
        self,
    ) -> typing.Optional[DataplexAssetDiscoverySpecJsonOptions]:
        return typing.cast(typing.Optional[DataplexAssetDiscoverySpecJsonOptions], jsii.get(self, "jsonOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9968775a8a0d98d2477d0d53d62919ec51e66e44294a6d695b3048e3dc9dc570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludePatterns")
    def exclude_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludePatterns"))

    @exclude_patterns.setter
    def exclude_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0994d96898ba5e18beb7b886d58e379af96da8acf071f59df581eb16ca48b6f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludePatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includePatterns")
    def include_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includePatterns"))

    @include_patterns.setter
    def include_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e15ed2af2619e6b555a83a8861f94fb97e47736d187d5281dd518002ed1ea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includePatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bb807ff3701cd00a46d5682fa95209f07f9bbcf966adcc01b8beb0b9b4dee39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexAssetDiscoverySpec]:
        return typing.cast(typing.Optional[DataplexAssetDiscoverySpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexAssetDiscoverySpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14e8b63a1f45be2131ad460c2a7cc10afdd042e2197aa6a092ff3398b3283017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetDiscoveryStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataplexAssetDiscoveryStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexAssetDiscoveryStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexAssetDiscoveryStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetDiscoveryStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6900007e739596b3fc29ed5dfdf131aa5cffa047ab71b0386b28231890da841e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataplexAssetDiscoveryStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41842cac00f4bedd52fce9155d06135ce76dccb5c46fd78e5a9473b7beaa0bd0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataplexAssetDiscoveryStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c77b3fabfd54757863566eae9ca2e4005f1a95d2357b83159a1785e25e0be29d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23edf79314b1c04119c3f873884ab004b5477cc651b17c4f572a789db71a8552)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e89177172029b434c335cb4e75a4d63df4d0fb0dcc29d505f07440adb9ba222f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataplexAssetDiscoveryStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetDiscoveryStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40a869a617b2ed7856af60a98bb705940785d274a06a71fafd21084752300ac9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="lastRunDuration")
    def last_run_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastRunDuration"))

    @builtins.property
    @jsii.member(jsii_name="lastRunTime")
    def last_run_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastRunTime"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stats")
    def stats(self) -> "DataplexAssetDiscoveryStatusStatsList":
        return typing.cast("DataplexAssetDiscoveryStatusStatsList", jsii.get(self, "stats"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexAssetDiscoveryStatus]:
        return typing.cast(typing.Optional[DataplexAssetDiscoveryStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexAssetDiscoveryStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__925ad0afd647571b2df8c4850f00d807610ba0a46443df69a1ed9c8ed22f301a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetDiscoveryStatusStats",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataplexAssetDiscoveryStatusStats:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexAssetDiscoveryStatusStats(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexAssetDiscoveryStatusStatsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetDiscoveryStatusStatsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a084f13b64fcc2dc327fc7b33f1f352e963f4803a54ddb66efa4435a8603dcf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataplexAssetDiscoveryStatusStatsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85ce6ec28a52a1f8084c0a8de1f5a0f4b5133a6f42554001db951047eb46f5b5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataplexAssetDiscoveryStatusStatsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa613edddaf8e9c2f4e83c58f11f68bd5271a298ab4c9c5f5e53c998c60f89e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__517d944f4cbb41cfdf28f9f1721ec0a1ddabd63921440d9f6f0cfc1c0fa0a740)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9889b8cfbd2cb2861f2d5595d739ac6d0c51eb80f6b069aef3c9950c0b83892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataplexAssetDiscoveryStatusStatsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetDiscoveryStatusStatsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64a211f33e46d9bf5dafaadafd304483796c8c7b0b8082353dbceb27b0541ed5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dataItems")
    def data_items(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataItems"))

    @builtins.property
    @jsii.member(jsii_name="dataSize")
    def data_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataSize"))

    @builtins.property
    @jsii.member(jsii_name="filesets")
    def filesets(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "filesets"))

    @builtins.property
    @jsii.member(jsii_name="tables")
    def tables(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tables"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexAssetDiscoveryStatusStats]:
        return typing.cast(typing.Optional[DataplexAssetDiscoveryStatusStats], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexAssetDiscoveryStatusStats],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__356a6d5fc90fae4b658f830eda5d59f6f658a59b5c0b67d26dff4a573db2d75a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetResourceSpec",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "name": "name",
        "read_access_mode": "readAccessMode",
    },
)
class DataplexAssetResourceSpec:
    def __init__(
        self,
        *,
        type: builtins.str,
        name: typing.Optional[builtins.str] = None,
        read_access_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Required. Immutable. Type of resource. Possible values: STORAGE_BUCKET, BIGQUERY_DATASET. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#type DataplexAsset#type}
        :param name: Immutable. Relative name of the cloud resource that contains the data that is being managed within a lake. For example: ``projects/{project_number}/buckets/{bucket_id}`` ``projects/{project_number}/datasets/{dataset_id}`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#name DataplexAsset#name}
        :param read_access_mode: Optional. Determines how read permissions are handled for each asset and their associated tables. Only available to storage buckets assets. Possible values: DIRECT, MANAGED Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#read_access_mode DataplexAsset#read_access_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e97c3edd2b17d1f2406e704f03b5b13b9fc61cd5449d24d6fa726eab79662598)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument read_access_mode", value=read_access_mode, expected_type=type_hints["read_access_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if name is not None:
            self._values["name"] = name
        if read_access_mode is not None:
            self._values["read_access_mode"] = read_access_mode

    @builtins.property
    def type(self) -> builtins.str:
        '''Required. Immutable. Type of resource. Possible values: STORAGE_BUCKET, BIGQUERY_DATASET.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#type DataplexAsset#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Immutable.

        Relative name of the cloud resource that contains the data that is being managed within a lake. For example: ``projects/{project_number}/buckets/{bucket_id}`` ``projects/{project_number}/datasets/{dataset_id}``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#name DataplexAsset#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_access_mode(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Determines how read permissions are handled for each asset and their associated tables. Only available to storage buckets assets. Possible values: DIRECT, MANAGED

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#read_access_mode DataplexAsset#read_access_mode}
        '''
        result = self._values.get("read_access_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexAssetResourceSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexAssetResourceSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetResourceSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4645b6f9b55ed40f8e25893fd00be4c9c8145c331dd1441ddcbda0a81651be9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetReadAccessMode")
    def reset_read_access_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadAccessMode", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="readAccessModeInput")
    def read_access_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readAccessModeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__59e32530443c566495e09bffa586c6aa6607715118020574ae898fc5ac819054)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readAccessMode")
    def read_access_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "readAccessMode"))

    @read_access_mode.setter
    def read_access_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b905d1f4fd129c1e879e23f21805068e5d14f9e3c3c7b6c580fd81f46fe9088)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readAccessMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d239482d21448e0cf2fd0a19a5d7db91c954aa0c7844dcf89c65632b4560f0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexAssetResourceSpec]:
        return typing.cast(typing.Optional[DataplexAssetResourceSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataplexAssetResourceSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489114dbab7291a6b51d5c038e6a0359595ab3e974774b69f1bcad9782ec9176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetResourceStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataplexAssetResourceStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexAssetResourceStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexAssetResourceStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetResourceStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a1d36a6de9acba131ed960996bb03302ac61d0e8eafefd933dad56d8bc80c63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataplexAssetResourceStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e952bdf6bd9b77633cb7f8c4027302945c9bdda12832b85e967f7a1eb1421d57)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataplexAssetResourceStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9775da3db00c60e0153cde8a9c093fa3d31209c8ffc7cdbc026a37da861a90e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f58adc9110195e8b5d3dd28bcaf6df37f1390df6b53d191ba00e5b15fbca38af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e9c26aa8831e5bd31ed7d9987d1baaa4c267122a603ff17aa5b076d9c64ee28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataplexAssetResourceStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetResourceStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf19c410ea5a63fac0e59b936f5bc5121f08d60c47900013827a9521d815170d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexAssetResourceStatus]:
        return typing.cast(typing.Optional[DataplexAssetResourceStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexAssetResourceStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6f21d03ac20139329297ce430eeae81e85d8d9766fc5b753604b31a8230e56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetSecurityStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataplexAssetSecurityStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexAssetSecurityStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexAssetSecurityStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetSecurityStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6a7fed64a3951a8148d1baffb5be5037646ba05c2fbe4327a148d476a9705ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataplexAssetSecurityStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9216d9c44b3dc76670bf11e3fea8bd9f87accc6850355beaae3f5e80a11bf7e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataplexAssetSecurityStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a72045f981ac6ae875cca55d24b14ce875e98db90d45397e2aec8a358bbe47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__114692d0a05497e44e96e37291c533f72d47cc7f3a6914d6644c61570f9e4b2c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b667d95ddde9ba8a142f08c606bd6d76b239da7bcd811bebec14edf07bff3f39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataplexAssetSecurityStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetSecurityStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37f98f40c8de39285378a6ec6004fb2079c0c9cc8734d0b219772f19a3a290fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexAssetSecurityStatus]:
        return typing.cast(typing.Optional[DataplexAssetSecurityStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexAssetSecurityStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7108ce504562562f1222623b09766f24713680ec0b8718a416458384c041571b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataplexAssetTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#create DataplexAsset#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#delete DataplexAsset#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#update DataplexAsset#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e6cace3236311eb3a56e1b840bda4120d8867f2d7bc8486934eabe8f12b107)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#create DataplexAsset#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#delete DataplexAsset#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_asset#update DataplexAsset#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexAssetTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexAssetTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexAsset.DataplexAssetTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b582e7e891bc82ac4a21a784790ccb559c30eb1ff77d14db1b8c634db727e8d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efeb4e6d1e803dba25ec1b1aad39905e8f814ef92222814f1636c488d6cdcf53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e14e60cd7c2b17174a0845439d6d4e61b254220af5355c88f496d08fd9dff70d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b86583d5271b5eb712f029114bfe77b27399025d02666380164d6777ce72fb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexAssetTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexAssetTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexAssetTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f23e7ae6d630d7745170429ffdaf029ebba9b7a9c6357eac1f610fbc55f920a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataplexAsset",
    "DataplexAssetConfig",
    "DataplexAssetDiscoverySpec",
    "DataplexAssetDiscoverySpecCsvOptions",
    "DataplexAssetDiscoverySpecCsvOptionsOutputReference",
    "DataplexAssetDiscoverySpecJsonOptions",
    "DataplexAssetDiscoverySpecJsonOptionsOutputReference",
    "DataplexAssetDiscoverySpecOutputReference",
    "DataplexAssetDiscoveryStatus",
    "DataplexAssetDiscoveryStatusList",
    "DataplexAssetDiscoveryStatusOutputReference",
    "DataplexAssetDiscoveryStatusStats",
    "DataplexAssetDiscoveryStatusStatsList",
    "DataplexAssetDiscoveryStatusStatsOutputReference",
    "DataplexAssetResourceSpec",
    "DataplexAssetResourceSpecOutputReference",
    "DataplexAssetResourceStatus",
    "DataplexAssetResourceStatusList",
    "DataplexAssetResourceStatusOutputReference",
    "DataplexAssetSecurityStatus",
    "DataplexAssetSecurityStatusList",
    "DataplexAssetSecurityStatusOutputReference",
    "DataplexAssetTimeouts",
    "DataplexAssetTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2c9b831e76e14625eedef469ef1a19154806d5ed5048d825e14b3fc69a87ba7a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dataplex_zone: builtins.str,
    discovery_spec: typing.Union[DataplexAssetDiscoverySpec, typing.Dict[builtins.str, typing.Any]],
    lake: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_spec: typing.Union[DataplexAssetResourceSpec, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataplexAssetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__1d9dfaf354a395bafaeb4f6be9644d5fcd240d4c88d96273c246909e5bef9edf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46e4e9995f38d33874a2a30e17cc21d6268cddb09f4abed18289c967482fbce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21edcae6cc3b82cc08997b89d3d6c456ce2e167d950ce5cc0aa15800ac9f238(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e702e06faef2d342e354ab1f6300bebbed5ec9a208441cfd826430f6a7db16b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215a9eef775c2b7a0644e56caf4c61088da11fd682ddcbcccae83c5a9a10452f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc0a56a9792abb01120bdb8bc1103d05d6d4532ebd364a44c1a7e6bca93a158(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f6311faa21da640b6902091809eb392daafd380fbd4832802b2813fd0c7ac8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ac44aa535ca51bf3ebdac97a92ee06bb8681bca5403d15aa5d68db095dcb2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4cc735b0f0e40831c54715231c7cbe93311c590c1f0a9e40442e9740b5f745(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba44b197c87c85e05b14d9d264c9f02f07da21151ecc7b4211be58f4ab691df2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a616f0134251f5edeb30b0170b886b2d620286b5976e1cd3465edd89d3a18749(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dataplex_zone: builtins.str,
    discovery_spec: typing.Union[DataplexAssetDiscoverySpec, typing.Dict[builtins.str, typing.Any]],
    lake: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_spec: typing.Union[DataplexAssetResourceSpec, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataplexAssetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__738c53360759489a8b68fb55b56370fc4b5800ab059bfd01ebecfff6e9728f0a(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    csv_options: typing.Optional[typing.Union[DataplexAssetDiscoverySpecCsvOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_options: typing.Optional[typing.Union[DataplexAssetDiscoverySpecJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7e458f346608fbdc0e7290b7c77117cebc5aa70566bc1ab9110ad27afb95f8(
    *,
    delimiter: typing.Optional[builtins.str] = None,
    disable_type_inference: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encoding: typing.Optional[builtins.str] = None,
    header_rows: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77982fc804697222f2d341f234b4f19e42ec8ff820d6a82f050bfb2e759d3e97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664b686eea92dc313d3842098ae53f19e66c72e990b23ac1704edb9a1b193d20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebeb0a42622ea0bb1b2b532717c6421db11e0eead4fb84d98b1fc0028c082e0a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b8aebac8166297117c18e054ca0be0952c88575fa7ed35ceb5b8764aa1a6d10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78cf8c909242cf995d181a5641eb90715baa89b90ed0ee67557b38b51bdc1c83(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb05fc1418d87cb718781c51ab115c4fb4407b59bc0118d367ab2195517f42c(
    value: typing.Optional[DataplexAssetDiscoverySpecCsvOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a41e617f4c3716830deb87ccb64a238eaee0eb4d7a2e0b04082e77f1440b8f(
    *,
    disable_type_inference: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encoding: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9909c3c97fc436e71f8758f8c5b7fd8327496442aa78a49b52a5b821857eefe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cedf0c531146326e12f3a794180c4002fdfead97ae229e83cb53f34d52c4613(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8083880b9f469285e052ae729db1c668837a950a52137903648bc08a88d82f6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a2ab6ea03d1f846f8defd36091b5049d43d0a1289505f7c48eba3046d3205c(
    value: typing.Optional[DataplexAssetDiscoverySpecJsonOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967a0ebdfb5a039b6cffd4d3aed36c79423d1466288e06b982e300d3dbb8b1b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9968775a8a0d98d2477d0d53d62919ec51e66e44294a6d695b3048e3dc9dc570(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0994d96898ba5e18beb7b886d58e379af96da8acf071f59df581eb16ca48b6f2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e15ed2af2619e6b555a83a8861f94fb97e47736d187d5281dd518002ed1ea1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb807ff3701cd00a46d5682fa95209f07f9bbcf966adcc01b8beb0b9b4dee39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e8b63a1f45be2131ad460c2a7cc10afdd042e2197aa6a092ff3398b3283017(
    value: typing.Optional[DataplexAssetDiscoverySpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6900007e739596b3fc29ed5dfdf131aa5cffa047ab71b0386b28231890da841e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41842cac00f4bedd52fce9155d06135ce76dccb5c46fd78e5a9473b7beaa0bd0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77b3fabfd54757863566eae9ca2e4005f1a95d2357b83159a1785e25e0be29d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23edf79314b1c04119c3f873884ab004b5477cc651b17c4f572a789db71a8552(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e89177172029b434c335cb4e75a4d63df4d0fb0dcc29d505f07440adb9ba222f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a869a617b2ed7856af60a98bb705940785d274a06a71fafd21084752300ac9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__925ad0afd647571b2df8c4850f00d807610ba0a46443df69a1ed9c8ed22f301a(
    value: typing.Optional[DataplexAssetDiscoveryStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a084f13b64fcc2dc327fc7b33f1f352e963f4803a54ddb66efa4435a8603dcf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ce6ec28a52a1f8084c0a8de1f5a0f4b5133a6f42554001db951047eb46f5b5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa613edddaf8e9c2f4e83c58f11f68bd5271a298ab4c9c5f5e53c998c60f89e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517d944f4cbb41cfdf28f9f1721ec0a1ddabd63921440d9f6f0cfc1c0fa0a740(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9889b8cfbd2cb2861f2d5595d739ac6d0c51eb80f6b069aef3c9950c0b83892(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a211f33e46d9bf5dafaadafd304483796c8c7b0b8082353dbceb27b0541ed5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356a6d5fc90fae4b658f830eda5d59f6f658a59b5c0b67d26dff4a573db2d75a(
    value: typing.Optional[DataplexAssetDiscoveryStatusStats],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97c3edd2b17d1f2406e704f03b5b13b9fc61cd5449d24d6fa726eab79662598(
    *,
    type: builtins.str,
    name: typing.Optional[builtins.str] = None,
    read_access_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4645b6f9b55ed40f8e25893fd00be4c9c8145c331dd1441ddcbda0a81651be9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e32530443c566495e09bffa586c6aa6607715118020574ae898fc5ac819054(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b905d1f4fd129c1e879e23f21805068e5d14f9e3c3c7b6c580fd81f46fe9088(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d239482d21448e0cf2fd0a19a5d7db91c954aa0c7844dcf89c65632b4560f0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489114dbab7291a6b51d5c038e6a0359595ab3e974774b69f1bcad9782ec9176(
    value: typing.Optional[DataplexAssetResourceSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a1d36a6de9acba131ed960996bb03302ac61d0e8eafefd933dad56d8bc80c63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e952bdf6bd9b77633cb7f8c4027302945c9bdda12832b85e967f7a1eb1421d57(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9775da3db00c60e0153cde8a9c093fa3d31209c8ffc7cdbc026a37da861a90e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58adc9110195e8b5d3dd28bcaf6df37f1390df6b53d191ba00e5b15fbca38af(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9c26aa8831e5bd31ed7d9987d1baaa4c267122a603ff17aa5b076d9c64ee28(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf19c410ea5a63fac0e59b936f5bc5121f08d60c47900013827a9521d815170d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6f21d03ac20139329297ce430eeae81e85d8d9766fc5b753604b31a8230e56(
    value: typing.Optional[DataplexAssetResourceStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a7fed64a3951a8148d1baffb5be5037646ba05c2fbe4327a148d476a9705ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9216d9c44b3dc76670bf11e3fea8bd9f87accc6850355beaae3f5e80a11bf7e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a72045f981ac6ae875cca55d24b14ce875e98db90d45397e2aec8a358bbe47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114692d0a05497e44e96e37291c533f72d47cc7f3a6914d6644c61570f9e4b2c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b667d95ddde9ba8a142f08c606bd6d76b239da7bcd811bebec14edf07bff3f39(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f98f40c8de39285378a6ec6004fb2079c0c9cc8734d0b219772f19a3a290fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7108ce504562562f1222623b09766f24713680ec0b8718a416458384c041571b(
    value: typing.Optional[DataplexAssetSecurityStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e6cace3236311eb3a56e1b840bda4120d8867f2d7bc8486934eabe8f12b107(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b582e7e891bc82ac4a21a784790ccb559c30eb1ff77d14db1b8c634db727e8d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efeb4e6d1e803dba25ec1b1aad39905e8f814ef92222814f1636c488d6cdcf53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14e60cd7c2b17174a0845439d6d4e61b254220af5355c88f496d08fd9dff70d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b86583d5271b5eb712f029114bfe77b27399025d02666380164d6777ce72fb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f23e7ae6d630d7745170429ffdaf029ebba9b7a9c6357eac1f610fbc55f920a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexAssetTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

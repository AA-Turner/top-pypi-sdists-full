r'''
# `google_dataplex_zone`

Refer to the Terraform Registry for docs: [`google_dataplex_zone`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone).
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


class DataplexZone(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexZone.DataplexZone",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone google_dataplex_zone}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        discovery_spec: typing.Union["DataplexZoneDiscoverySpec", typing.Dict[builtins.str, typing.Any]],
        lake: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_spec: typing.Union["DataplexZoneResourceSpec", typing.Dict[builtins.str, typing.Any]],
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataplexZoneTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone google_dataplex_zone} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param discovery_spec: discovery_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#discovery_spec DataplexZone#discovery_spec}
        :param lake: The lake for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#lake DataplexZone#lake}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#location DataplexZone#location}
        :param name: The name of the zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#name DataplexZone#name}
        :param resource_spec: resource_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#resource_spec DataplexZone#resource_spec}
        :param type: Required. Immutable. The type of the zone. Possible values: TYPE_UNSPECIFIED, RAW, CURATED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#type DataplexZone#type}
        :param description: Optional. Description of the zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#description DataplexZone#description}
        :param display_name: Optional. User friendly display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#display_name DataplexZone#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#id DataplexZone#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. User defined labels for the zone. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#labels DataplexZone#labels}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#project DataplexZone#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#timeouts DataplexZone#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__551a07a5880d4a3f4c6c6577c495285a9c2436c6b20e65c60f4be3d342c9c8df)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataplexZoneConfig(
            discovery_spec=discovery_spec,
            lake=lake,
            location=location,
            name=name,
            resource_spec=resource_spec,
            type=type,
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
        '''Generates CDKTF code for importing a DataplexZone resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataplexZone to import.
        :param import_from_id: The id of the existing DataplexZone that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataplexZone to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92516416ef0ee142e1a09d2ef403a4d8af023f013519d2103dab51eb11046a72)
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
        csv_options: typing.Optional[typing.Union["DataplexZoneDiscoverySpecCsvOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        json_options: typing.Optional[typing.Union["DataplexZoneDiscoverySpecJsonOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Required. Whether discovery is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#enabled DataplexZone#enabled}
        :param csv_options: csv_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#csv_options DataplexZone#csv_options}
        :param exclude_patterns: Optional. The list of patterns to apply for selecting data to exclude during discovery. For Cloud Storage bucket assets, these are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these are interpreted as patterns to match table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#exclude_patterns DataplexZone#exclude_patterns}
        :param include_patterns: Optional. The list of patterns to apply for selecting data to include during discovery if only a subset of the data should considered. For Cloud Storage bucket assets, these are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these are interpreted as patterns to match table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#include_patterns DataplexZone#include_patterns}
        :param json_options: json_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#json_options DataplexZone#json_options}
        :param schedule: Optional. Cron schedule (https://en.wikipedia.org/wiki/Cron) for running discovery periodically. Successive discovery runs must be scheduled at least 60 minutes apart. The default value is to run discovery every 60 minutes. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: "CRON_TZ=${IANA_TIME_ZONE}" or TZ=${IANA_TIME_ZONE}". The ${IANA_TIME_ZONE} may only be a valid string from IANA time zone database. For example, "CRON_TZ=America/New_York 1 * * * *", or "TZ=America/New_York 1 * * * *". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#schedule DataplexZone#schedule}
        '''
        value = DataplexZoneDiscoverySpec(
            enabled=enabled,
            csv_options=csv_options,
            exclude_patterns=exclude_patterns,
            include_patterns=include_patterns,
            json_options=json_options,
            schedule=schedule,
        )

        return typing.cast(None, jsii.invoke(self, "putDiscoverySpec", [value]))

    @jsii.member(jsii_name="putResourceSpec")
    def put_resource_spec(self, *, location_type: builtins.str) -> None:
        '''
        :param location_type: Required. Immutable. The location type of the resources that are allowed to be attached to the assets within this zone. Possible values: LOCATION_TYPE_UNSPECIFIED, SINGLE_REGION, MULTI_REGION Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#location_type DataplexZone#location_type}
        '''
        value = DataplexZoneResourceSpec(location_type=location_type)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#create DataplexZone#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#delete DataplexZone#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#update DataplexZone#update}.
        '''
        value = DataplexZoneTimeouts(create=create, delete=delete, update=update)

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
    @jsii.member(jsii_name="assetStatus")
    def asset_status(self) -> "DataplexZoneAssetStatusList":
        return typing.cast("DataplexZoneAssetStatusList", jsii.get(self, "assetStatus"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="discoverySpec")
    def discovery_spec(self) -> "DataplexZoneDiscoverySpecOutputReference":
        return typing.cast("DataplexZoneDiscoverySpecOutputReference", jsii.get(self, "discoverySpec"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="resourceSpec")
    def resource_spec(self) -> "DataplexZoneResourceSpecOutputReference":
        return typing.cast("DataplexZoneResourceSpecOutputReference", jsii.get(self, "resourceSpec"))

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
    def timeouts(self) -> "DataplexZoneTimeoutsOutputReference":
        return typing.cast("DataplexZoneTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="discoverySpecInput")
    def discovery_spec_input(self) -> typing.Optional["DataplexZoneDiscoverySpec"]:
        return typing.cast(typing.Optional["DataplexZoneDiscoverySpec"], jsii.get(self, "discoverySpecInput"))

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
    def resource_spec_input(self) -> typing.Optional["DataplexZoneResourceSpec"]:
        return typing.cast(typing.Optional["DataplexZoneResourceSpec"], jsii.get(self, "resourceSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataplexZoneTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataplexZoneTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4935677be911f08abd281cd9d26477386b234c440d85699c6218a9a5bfdec806)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a8b51ae61be7f3e6a4680fffc51511f2e5333d1898c506f18c2e80041d0446a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ec541e9627f6f161709f13e924abafbd3a01ffe27e648b2f591d3ae69bb4041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df043efd0fbae3d1bee67aa9ddfc3ae896e365b409fc7cf8f4c58bf72e74b1f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lake")
    def lake(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lake"))

    @lake.setter
    def lake(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b790938c5e796d827c2f7befdf50d62bb71d49342d211c0c898cd7d31c20926d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lake", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce1a4deabdf98e08a5e0fe6b65f963beaa8beba039518dfa5b4c1fd3a27d6362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a39c8ddaec8b87ba8b3a8ec6a6c8e7eda83cda40209122bee65bbf8ec4ba8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9008b6f241096102e0ce684a8f63b90a778be2effdd386fe4f42b22f024122b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9b39c7249a4a9b632b552543ccc9fd0546dc82f7d5013d80d2951520c7b1c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexZone.DataplexZoneAssetStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataplexZoneAssetStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexZoneAssetStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexZoneAssetStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexZone.DataplexZoneAssetStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7b6adc6445a4d61f348f12184f84c62ed55bed325c47dd846c3abc26e4be947)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataplexZoneAssetStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cae3972991ece62387a4a1807d8f8807aeb94933a25fc5f8b74cb38d6165161)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataplexZoneAssetStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bab56da4518605cbf6b1ebe09455e26f9d7886125438b36f2d696a089ba3760)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e76994198f3a31926718a36c089e16eade21395b0bc1e53ee6b6c637e6c3a9d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6067157b57fb29975071cbc92ac99a0c7886f8b67d879cc7c2dd29ffc84d5af7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataplexZoneAssetStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexZone.DataplexZoneAssetStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c93762117cae5bc9af430c71c44ec6214441dbb4cec062769e2e63fe36837ccf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="activeAssets")
    def active_assets(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "activeAssets"))

    @builtins.property
    @jsii.member(jsii_name="securityPolicyApplyingAssets")
    def security_policy_applying_assets(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "securityPolicyApplyingAssets"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexZoneAssetStatus]:
        return typing.cast(typing.Optional[DataplexZoneAssetStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataplexZoneAssetStatus]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf06c28d6eb5b3d3018e560c789f56cb9e3f71ec53b30523bb43d5fcb9dc314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexZone.DataplexZoneConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "discovery_spec": "discoverySpec",
        "lake": "lake",
        "location": "location",
        "name": "name",
        "resource_spec": "resourceSpec",
        "type": "type",
        "description": "description",
        "display_name": "displayName",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class DataplexZoneConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        discovery_spec: typing.Union["DataplexZoneDiscoverySpec", typing.Dict[builtins.str, typing.Any]],
        lake: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_spec: typing.Union["DataplexZoneResourceSpec", typing.Dict[builtins.str, typing.Any]],
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataplexZoneTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param discovery_spec: discovery_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#discovery_spec DataplexZone#discovery_spec}
        :param lake: The lake for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#lake DataplexZone#lake}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#location DataplexZone#location}
        :param name: The name of the zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#name DataplexZone#name}
        :param resource_spec: resource_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#resource_spec DataplexZone#resource_spec}
        :param type: Required. Immutable. The type of the zone. Possible values: TYPE_UNSPECIFIED, RAW, CURATED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#type DataplexZone#type}
        :param description: Optional. Description of the zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#description DataplexZone#description}
        :param display_name: Optional. User friendly display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#display_name DataplexZone#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#id DataplexZone#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. User defined labels for the zone. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#labels DataplexZone#labels}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#project DataplexZone#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#timeouts DataplexZone#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(discovery_spec, dict):
            discovery_spec = DataplexZoneDiscoverySpec(**discovery_spec)
        if isinstance(resource_spec, dict):
            resource_spec = DataplexZoneResourceSpec(**resource_spec)
        if isinstance(timeouts, dict):
            timeouts = DataplexZoneTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635c4efb995940d15207badee05bf1b2993acbd473c25416c0b191fcdd8cbb5e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument discovery_spec", value=discovery_spec, expected_type=type_hints["discovery_spec"])
            check_type(argname="argument lake", value=lake, expected_type=type_hints["lake"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_spec", value=resource_spec, expected_type=type_hints["resource_spec"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "discovery_spec": discovery_spec,
            "lake": lake,
            "location": location,
            "name": name,
            "resource_spec": resource_spec,
            "type": type,
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
    def discovery_spec(self) -> "DataplexZoneDiscoverySpec":
        '''discovery_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#discovery_spec DataplexZone#discovery_spec}
        '''
        result = self._values.get("discovery_spec")
        assert result is not None, "Required property 'discovery_spec' is missing"
        return typing.cast("DataplexZoneDiscoverySpec", result)

    @builtins.property
    def lake(self) -> builtins.str:
        '''The lake for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#lake DataplexZone#lake}
        '''
        result = self._values.get("lake")
        assert result is not None, "Required property 'lake' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#location DataplexZone#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the zone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#name DataplexZone#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_spec(self) -> "DataplexZoneResourceSpec":
        '''resource_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#resource_spec DataplexZone#resource_spec}
        '''
        result = self._values.get("resource_spec")
        assert result is not None, "Required property 'resource_spec' is missing"
        return typing.cast("DataplexZoneResourceSpec", result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Required. Immutable. The type of the zone. Possible values: TYPE_UNSPECIFIED, RAW, CURATED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#type DataplexZone#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Description of the zone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#description DataplexZone#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Optional. User friendly display name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#display_name DataplexZone#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#id DataplexZone#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. User defined labels for the zone.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field ``effective_labels`` for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#labels DataplexZone#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#project DataplexZone#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataplexZoneTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#timeouts DataplexZone#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataplexZoneTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexZoneConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexZone.DataplexZoneDiscoverySpec",
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
class DataplexZoneDiscoverySpec:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        csv_options: typing.Optional[typing.Union["DataplexZoneDiscoverySpecCsvOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        json_options: typing.Optional[typing.Union["DataplexZoneDiscoverySpecJsonOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Required. Whether discovery is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#enabled DataplexZone#enabled}
        :param csv_options: csv_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#csv_options DataplexZone#csv_options}
        :param exclude_patterns: Optional. The list of patterns to apply for selecting data to exclude during discovery. For Cloud Storage bucket assets, these are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these are interpreted as patterns to match table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#exclude_patterns DataplexZone#exclude_patterns}
        :param include_patterns: Optional. The list of patterns to apply for selecting data to include during discovery if only a subset of the data should considered. For Cloud Storage bucket assets, these are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these are interpreted as patterns to match table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#include_patterns DataplexZone#include_patterns}
        :param json_options: json_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#json_options DataplexZone#json_options}
        :param schedule: Optional. Cron schedule (https://en.wikipedia.org/wiki/Cron) for running discovery periodically. Successive discovery runs must be scheduled at least 60 minutes apart. The default value is to run discovery every 60 minutes. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: "CRON_TZ=${IANA_TIME_ZONE}" or TZ=${IANA_TIME_ZONE}". The ${IANA_TIME_ZONE} may only be a valid string from IANA time zone database. For example, "CRON_TZ=America/New_York 1 * * * *", or "TZ=America/New_York 1 * * * *". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#schedule DataplexZone#schedule}
        '''
        if isinstance(csv_options, dict):
            csv_options = DataplexZoneDiscoverySpecCsvOptions(**csv_options)
        if isinstance(json_options, dict):
            json_options = DataplexZoneDiscoverySpecJsonOptions(**json_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb86527add7298c643890ceedc25694a28b0df90ca95fa6dd0fd45d8239b79a9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#enabled DataplexZone#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def csv_options(self) -> typing.Optional["DataplexZoneDiscoverySpecCsvOptions"]:
        '''csv_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#csv_options DataplexZone#csv_options}
        '''
        result = self._values.get("csv_options")
        return typing.cast(typing.Optional["DataplexZoneDiscoverySpecCsvOptions"], result)

    @builtins.property
    def exclude_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        The list of patterns to apply for selecting data to exclude during discovery. For Cloud Storage bucket assets, these are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these are interpreted as patterns to match table names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#exclude_patterns DataplexZone#exclude_patterns}
        '''
        result = self._values.get("exclude_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        The list of patterns to apply for selecting data to include during discovery if only a subset of the data should considered. For Cloud Storage bucket assets, these are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these are interpreted as patterns to match table names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#include_patterns DataplexZone#include_patterns}
        '''
        result = self._values.get("include_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def json_options(self) -> typing.Optional["DataplexZoneDiscoverySpecJsonOptions"]:
        '''json_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#json_options DataplexZone#json_options}
        '''
        result = self._values.get("json_options")
        return typing.cast(typing.Optional["DataplexZoneDiscoverySpecJsonOptions"], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Cron schedule (https://en.wikipedia.org/wiki/Cron) for running discovery periodically. Successive discovery runs must be scheduled at least 60 minutes apart. The default value is to run discovery every 60 minutes. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: "CRON_TZ=${IANA_TIME_ZONE}" or TZ=${IANA_TIME_ZONE}". The ${IANA_TIME_ZONE} may only be a valid string from IANA time zone database. For example, "CRON_TZ=America/New_York 1 * * * *", or "TZ=America/New_York 1 * * * *".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#schedule DataplexZone#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexZoneDiscoverySpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexZone.DataplexZoneDiscoverySpecCsvOptions",
    jsii_struct_bases=[],
    name_mapping={
        "delimiter": "delimiter",
        "disable_type_inference": "disableTypeInference",
        "encoding": "encoding",
        "header_rows": "headerRows",
    },
)
class DataplexZoneDiscoverySpecCsvOptions:
    def __init__(
        self,
        *,
        delimiter: typing.Optional[builtins.str] = None,
        disable_type_inference: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encoding: typing.Optional[builtins.str] = None,
        header_rows: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delimiter: Optional. The delimiter being used to separate values. This defaults to ','. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#delimiter DataplexZone#delimiter}
        :param disable_type_inference: Optional. Whether to disable the inference of data type for CSV data. If true, all columns will be registered as strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#disable_type_inference DataplexZone#disable_type_inference}
        :param encoding: Optional. The character encoding of the data. The default is UTF-8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#encoding DataplexZone#encoding}
        :param header_rows: Optional. The number of rows to interpret as header rows that should be skipped when reading data rows. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#header_rows DataplexZone#header_rows}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4097f87dcf65d923e5c43add5eedb13e1c1be97cf5e883b39d565fe154bffdc)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#delimiter DataplexZone#delimiter}
        '''
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_type_inference(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Whether to disable the inference of data type for CSV data. If true, all columns will be registered as strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#disable_type_inference DataplexZone#disable_type_inference}
        '''
        result = self._values.get("disable_type_inference")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''Optional. The character encoding of the data. The default is UTF-8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#encoding DataplexZone#encoding}
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_rows(self) -> typing.Optional[jsii.Number]:
        '''Optional. The number of rows to interpret as header rows that should be skipped when reading data rows.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#header_rows DataplexZone#header_rows}
        '''
        result = self._values.get("header_rows")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexZoneDiscoverySpecCsvOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexZoneDiscoverySpecCsvOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexZone.DataplexZoneDiscoverySpecCsvOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4bd31a281afcf442bcb2533aafd1729797b3c4337d2f5f62e96d628513c37a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c5e8b59193fdac115a1a92032a703f5348061b4b3d85b063744fa300e9e0dc7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df96cc3433e1fffeed417c66205008ff5b7b934b318d374796cc71dc92d6f37c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableTypeInference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @encoding.setter
    def encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d026ed83f11254579128e6fd6e4a1a6d3a02622d16af3e37b374357d8db7c359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerRows")
    def header_rows(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "headerRows"))

    @header_rows.setter
    def header_rows(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1fb143d8169c79f2d2159cdadfc326ad15bca73e03eeb4aa5b158481f89043)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerRows", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexZoneDiscoverySpecCsvOptions]:
        return typing.cast(typing.Optional[DataplexZoneDiscoverySpecCsvOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexZoneDiscoverySpecCsvOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0d705fcc424c3d71ccaf47c1631481e3aaeeec68518b5f46b9fd2566063003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexZone.DataplexZoneDiscoverySpecJsonOptions",
    jsii_struct_bases=[],
    name_mapping={
        "disable_type_inference": "disableTypeInference",
        "encoding": "encoding",
    },
)
class DataplexZoneDiscoverySpecJsonOptions:
    def __init__(
        self,
        *,
        disable_type_inference: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encoding: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disable_type_inference: Optional. Whether to disable the inference of data type for Json data. If true, all columns will be registered as their primitive types (strings, number or boolean). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#disable_type_inference DataplexZone#disable_type_inference}
        :param encoding: Optional. The character encoding of the data. The default is UTF-8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#encoding DataplexZone#encoding}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65c7412abe299bd93d8c76f1abf7541438fe34c8eef1b6601483197a2996ce71)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#disable_type_inference DataplexZone#disable_type_inference}
        '''
        result = self._values.get("disable_type_inference")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''Optional. The character encoding of the data. The default is UTF-8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#encoding DataplexZone#encoding}
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexZoneDiscoverySpecJsonOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexZoneDiscoverySpecJsonOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexZone.DataplexZoneDiscoverySpecJsonOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89b861c1de00dd8437394dc51ea25906595e8501121fd1cf5ff300f7073a3438)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5336b01c38bc05b84ff36e3d520372465fb46df453fff198a7bcd870455a1e05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableTypeInference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @encoding.setter
    def encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44156b84261913d95fd9e4d701b04a5e7544916621be94a77661dc8fd22b6ea0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexZoneDiscoverySpecJsonOptions]:
        return typing.cast(typing.Optional[DataplexZoneDiscoverySpecJsonOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexZoneDiscoverySpecJsonOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf071f6e90ee165d97e63b5f9658062ce70c26c4e28daef306525e1d92aedb5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexZoneDiscoverySpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexZone.DataplexZoneDiscoverySpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fdb1fc96dd08d534d5d5f192d3e739ab2c57a325fecfd56ee7259a1ffa1569b)
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
        :param delimiter: Optional. The delimiter being used to separate values. This defaults to ','. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#delimiter DataplexZone#delimiter}
        :param disable_type_inference: Optional. Whether to disable the inference of data type for CSV data. If true, all columns will be registered as strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#disable_type_inference DataplexZone#disable_type_inference}
        :param encoding: Optional. The character encoding of the data. The default is UTF-8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#encoding DataplexZone#encoding}
        :param header_rows: Optional. The number of rows to interpret as header rows that should be skipped when reading data rows. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#header_rows DataplexZone#header_rows}
        '''
        value = DataplexZoneDiscoverySpecCsvOptions(
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
        :param disable_type_inference: Optional. Whether to disable the inference of data type for Json data. If true, all columns will be registered as their primitive types (strings, number or boolean). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#disable_type_inference DataplexZone#disable_type_inference}
        :param encoding: Optional. The character encoding of the data. The default is UTF-8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#encoding DataplexZone#encoding}
        '''
        value = DataplexZoneDiscoverySpecJsonOptions(
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
    def csv_options(self) -> DataplexZoneDiscoverySpecCsvOptionsOutputReference:
        return typing.cast(DataplexZoneDiscoverySpecCsvOptionsOutputReference, jsii.get(self, "csvOptions"))

    @builtins.property
    @jsii.member(jsii_name="jsonOptions")
    def json_options(self) -> DataplexZoneDiscoverySpecJsonOptionsOutputReference:
        return typing.cast(DataplexZoneDiscoverySpecJsonOptionsOutputReference, jsii.get(self, "jsonOptions"))

    @builtins.property
    @jsii.member(jsii_name="csvOptionsInput")
    def csv_options_input(self) -> typing.Optional[DataplexZoneDiscoverySpecCsvOptions]:
        return typing.cast(typing.Optional[DataplexZoneDiscoverySpecCsvOptions], jsii.get(self, "csvOptionsInput"))

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
    ) -> typing.Optional[DataplexZoneDiscoverySpecJsonOptions]:
        return typing.cast(typing.Optional[DataplexZoneDiscoverySpecJsonOptions], jsii.get(self, "jsonOptionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ab85c5f146ed111f6c247e8924941c72b219586ad679af62f86791e42d027f74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludePatterns")
    def exclude_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludePatterns"))

    @exclude_patterns.setter
    def exclude_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__964ce2e2048031d37d4aa378e208ed0dd26f8609f02ef70d098bd83ad3521eb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludePatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includePatterns")
    def include_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includePatterns"))

    @include_patterns.setter
    def include_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__166b3911e7bb7e586ae6a7b6ccd32c55b5c3f43492e13a77b047f2e3d67ee38d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includePatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9934bc9d51fa3f33e92cd87ed758552d6c6903a6eea192328b7c7d7ab041e545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexZoneDiscoverySpec]:
        return typing.cast(typing.Optional[DataplexZoneDiscoverySpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataplexZoneDiscoverySpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c6011feafedb88e9d100e53cbbb0092007339bb9a6d18cb76a36e0a22808a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexZone.DataplexZoneResourceSpec",
    jsii_struct_bases=[],
    name_mapping={"location_type": "locationType"},
)
class DataplexZoneResourceSpec:
    def __init__(self, *, location_type: builtins.str) -> None:
        '''
        :param location_type: Required. Immutable. The location type of the resources that are allowed to be attached to the assets within this zone. Possible values: LOCATION_TYPE_UNSPECIFIED, SINGLE_REGION, MULTI_REGION Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#location_type DataplexZone#location_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83980176bb89a2a804e8871d35902b0bd06ed6d57648bda9f7c3a4ad6415fe7)
            check_type(argname="argument location_type", value=location_type, expected_type=type_hints["location_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location_type": location_type,
        }

    @builtins.property
    def location_type(self) -> builtins.str:
        '''Required.

        Immutable. The location type of the resources that are allowed to be attached to the assets within this zone. Possible values: LOCATION_TYPE_UNSPECIFIED, SINGLE_REGION, MULTI_REGION

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#location_type DataplexZone#location_type}
        '''
        result = self._values.get("location_type")
        assert result is not None, "Required property 'location_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexZoneResourceSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexZoneResourceSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexZone.DataplexZoneResourceSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4829ce45dd00b17ed12e0115f5b5533cf22017c7dbb4ad6473c476fef50567d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="locationTypeInput")
    def location_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="locationType")
    def location_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locationType"))

    @location_type.setter
    def location_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf8cd50f8ab92e14d5588a1133d3f55f8e2965359f80016c418d7bbebe11467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexZoneResourceSpec]:
        return typing.cast(typing.Optional[DataplexZoneResourceSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataplexZoneResourceSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e178852f161ecd739fc532302380cf331d566ca0c2abf7fe12e81e2e92f06ade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexZone.DataplexZoneTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataplexZoneTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#create DataplexZone#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#delete DataplexZone#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#update DataplexZone#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__247790c091369a0576deded90f8c725720c1b79a413f943de79b0f40ff6cd889)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#create DataplexZone#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#delete DataplexZone#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_zone#update DataplexZone#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexZoneTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexZoneTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexZone.DataplexZoneTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c133430e6dfe4c12b174038c207ebf46f10ed5a87ce7370605e126466495abe9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e39151bb2868b45b7737ab6ffb7de1a85bc8ad5849394703ed67f8ecfd81431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a81a396a8e60c2bcc8f122b7d2d293c05bf3797f7cd4a25f42ad7f60b2f841e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d7c24de0f0e31fc93ee7d8ad2619c3b5cae8bd807b4e0106300b3df3ba0d3e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexZoneTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexZoneTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexZoneTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf24a6d109b9a95a797ccf1225b30727ee263a99e7a61d053119748b1b788666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataplexZone",
    "DataplexZoneAssetStatus",
    "DataplexZoneAssetStatusList",
    "DataplexZoneAssetStatusOutputReference",
    "DataplexZoneConfig",
    "DataplexZoneDiscoverySpec",
    "DataplexZoneDiscoverySpecCsvOptions",
    "DataplexZoneDiscoverySpecCsvOptionsOutputReference",
    "DataplexZoneDiscoverySpecJsonOptions",
    "DataplexZoneDiscoverySpecJsonOptionsOutputReference",
    "DataplexZoneDiscoverySpecOutputReference",
    "DataplexZoneResourceSpec",
    "DataplexZoneResourceSpecOutputReference",
    "DataplexZoneTimeouts",
    "DataplexZoneTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__551a07a5880d4a3f4c6c6577c495285a9c2436c6b20e65c60f4be3d342c9c8df(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    discovery_spec: typing.Union[DataplexZoneDiscoverySpec, typing.Dict[builtins.str, typing.Any]],
    lake: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_spec: typing.Union[DataplexZoneResourceSpec, typing.Dict[builtins.str, typing.Any]],
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataplexZoneTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__92516416ef0ee142e1a09d2ef403a4d8af023f013519d2103dab51eb11046a72(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4935677be911f08abd281cd9d26477386b234c440d85699c6218a9a5bfdec806(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a8b51ae61be7f3e6a4680fffc51511f2e5333d1898c506f18c2e80041d0446a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec541e9627f6f161709f13e924abafbd3a01ffe27e648b2f591d3ae69bb4041(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df043efd0fbae3d1bee67aa9ddfc3ae896e365b409fc7cf8f4c58bf72e74b1f7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b790938c5e796d827c2f7befdf50d62bb71d49342d211c0c898cd7d31c20926d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1a4deabdf98e08a5e0fe6b65f963beaa8beba039518dfa5b4c1fd3a27d6362(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a39c8ddaec8b87ba8b3a8ec6a6c8e7eda83cda40209122bee65bbf8ec4ba8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9008b6f241096102e0ce684a8f63b90a778be2effdd386fe4f42b22f024122b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9b39c7249a4a9b632b552543ccc9fd0546dc82f7d5013d80d2951520c7b1c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b6adc6445a4d61f348f12184f84c62ed55bed325c47dd846c3abc26e4be947(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cae3972991ece62387a4a1807d8f8807aeb94933a25fc5f8b74cb38d6165161(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bab56da4518605cbf6b1ebe09455e26f9d7886125438b36f2d696a089ba3760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e76994198f3a31926718a36c089e16eade21395b0bc1e53ee6b6c637e6c3a9d7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6067157b57fb29975071cbc92ac99a0c7886f8b67d879cc7c2dd29ffc84d5af7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c93762117cae5bc9af430c71c44ec6214441dbb4cec062769e2e63fe36837ccf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf06c28d6eb5b3d3018e560c789f56cb9e3f71ec53b30523bb43d5fcb9dc314(
    value: typing.Optional[DataplexZoneAssetStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635c4efb995940d15207badee05bf1b2993acbd473c25416c0b191fcdd8cbb5e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    discovery_spec: typing.Union[DataplexZoneDiscoverySpec, typing.Dict[builtins.str, typing.Any]],
    lake: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_spec: typing.Union[DataplexZoneResourceSpec, typing.Dict[builtins.str, typing.Any]],
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataplexZoneTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb86527add7298c643890ceedc25694a28b0df90ca95fa6dd0fd45d8239b79a9(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    csv_options: typing.Optional[typing.Union[DataplexZoneDiscoverySpecCsvOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_options: typing.Optional[typing.Union[DataplexZoneDiscoverySpecJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4097f87dcf65d923e5c43add5eedb13e1c1be97cf5e883b39d565fe154bffdc(
    *,
    delimiter: typing.Optional[builtins.str] = None,
    disable_type_inference: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encoding: typing.Optional[builtins.str] = None,
    header_rows: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4bd31a281afcf442bcb2533aafd1729797b3c4337d2f5f62e96d628513c37a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5e8b59193fdac115a1a92032a703f5348061b4b3d85b063744fa300e9e0dc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df96cc3433e1fffeed417c66205008ff5b7b934b318d374796cc71dc92d6f37c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d026ed83f11254579128e6fd6e4a1a6d3a02622d16af3e37b374357d8db7c359(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1fb143d8169c79f2d2159cdadfc326ad15bca73e03eeb4aa5b158481f89043(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0d705fcc424c3d71ccaf47c1631481e3aaeeec68518b5f46b9fd2566063003(
    value: typing.Optional[DataplexZoneDiscoverySpecCsvOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c7412abe299bd93d8c76f1abf7541438fe34c8eef1b6601483197a2996ce71(
    *,
    disable_type_inference: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encoding: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b861c1de00dd8437394dc51ea25906595e8501121fd1cf5ff300f7073a3438(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5336b01c38bc05b84ff36e3d520372465fb46df453fff198a7bcd870455a1e05(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44156b84261913d95fd9e4d701b04a5e7544916621be94a77661dc8fd22b6ea0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf071f6e90ee165d97e63b5f9658062ce70c26c4e28daef306525e1d92aedb5e(
    value: typing.Optional[DataplexZoneDiscoverySpecJsonOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fdb1fc96dd08d534d5d5f192d3e739ab2c57a325fecfd56ee7259a1ffa1569b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab85c5f146ed111f6c247e8924941c72b219586ad679af62f86791e42d027f74(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__964ce2e2048031d37d4aa378e208ed0dd26f8609f02ef70d098bd83ad3521eb1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__166b3911e7bb7e586ae6a7b6ccd32c55b5c3f43492e13a77b047f2e3d67ee38d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9934bc9d51fa3f33e92cd87ed758552d6c6903a6eea192328b7c7d7ab041e545(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c6011feafedb88e9d100e53cbbb0092007339bb9a6d18cb76a36e0a22808a2(
    value: typing.Optional[DataplexZoneDiscoverySpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83980176bb89a2a804e8871d35902b0bd06ed6d57648bda9f7c3a4ad6415fe7(
    *,
    location_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4829ce45dd00b17ed12e0115f5b5533cf22017c7dbb4ad6473c476fef50567d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf8cd50f8ab92e14d5588a1133d3f55f8e2965359f80016c418d7bbebe11467(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e178852f161ecd739fc532302380cf331d566ca0c2abf7fe12e81e2e92f06ade(
    value: typing.Optional[DataplexZoneResourceSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247790c091369a0576deded90f8c725720c1b79a413f943de79b0f40ff6cd889(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c133430e6dfe4c12b174038c207ebf46f10ed5a87ce7370605e126466495abe9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e39151bb2868b45b7737ab6ffb7de1a85bc8ad5849394703ed67f8ecfd81431(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a81a396a8e60c2bcc8f122b7d2d293c05bf3797f7cd4a25f42ad7f60b2f841e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7c24de0f0e31fc93ee7d8ad2619c3b5cae8bd807b4e0106300b3df3ba0d3e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf24a6d109b9a95a797ccf1225b30727ee263a99e7a61d053119748b1b788666(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexZoneTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

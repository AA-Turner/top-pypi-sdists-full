r'''
# `datadog_service_level_objective`

Refer to the Terraform Registry for docs: [`datadog_service_level_objective`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective).
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


class ServiceLevelObjective(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjective",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective datadog_service_level_objective}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        thresholds: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceLevelObjectiveThresholds", typing.Dict[builtins.str, typing.Any]]]],
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        monitor_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
        query: typing.Optional[typing.Union["ServiceLevelObjectiveQuery", typing.Dict[builtins.str, typing.Any]]] = None,
        sli_specification: typing.Optional[typing.Union["ServiceLevelObjectiveSliSpecification", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_threshold: typing.Optional[jsii.Number] = None,
        timeframe: typing.Optional[builtins.str] = None,
        validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        warning_threshold: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective datadog_service_level_objective} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of Datadog service level objective. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#name ServiceLevelObjective#name}
        :param thresholds: thresholds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#thresholds ServiceLevelObjective#thresholds}
        :param type: The type of the service level objective. The mapping from these types to the types found in the Datadog Web UI can be found in the Datadog API `documentation page <https://docs.datadoghq.com/api/v1/service-level-objectives/#create-a-slo-object>`_. Valid values are ``metric``, ``monitor``, ``time_slice``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#type ServiceLevelObjective#type}
        :param description: A description of this service level objective. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#description ServiceLevelObjective#description}
        :param force_delete: A boolean indicating whether this monitor can be deleted even if it's referenced by other resources (for example, dashboards). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#force_delete ServiceLevelObjective#force_delete}
        :param groups: A static set of groups to filter monitor-based SLOs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#groups ServiceLevelObjective#groups}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#id ServiceLevelObjective#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param monitor_ids: A static set of monitor IDs to use as part of the SLO. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#monitor_ids ServiceLevelObjective#monitor_ids}
        :param query: query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#query ServiceLevelObjective#query}
        :param sli_specification: sli_specification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#sli_specification ServiceLevelObjective#sli_specification}
        :param tags: A list of tags to associate with your service level objective. This can help you categorize and filter service level objectives in the service level objectives page of the UI. Note: it's not currently possible to filter by these tags when querying via the API Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#tags ServiceLevelObjective#tags}
        :param target_threshold: The objective's target in ``(0,100)``. This must match the corresponding thresholds of the primary time frame. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#target_threshold ServiceLevelObjective#target_threshold}
        :param timeframe: The primary time frame for the objective. The mapping from these types to the types found in the Datadog Web UI can be found in the Datadog API documentation page. Valid values are ``7d``, ``30d``, ``90d``, ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#timeframe ServiceLevelObjective#timeframe}
        :param validate: Whether or not to validate the SLO. It checks if monitors added to a monitor SLO already exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#validate ServiceLevelObjective#validate}
        :param warning_threshold: The objective's warning value in ``(0,100)``. This must be greater than the target value and match the corresponding thresholds of the primary time frame. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#warning_threshold ServiceLevelObjective#warning_threshold}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5669eb7d0a788a9ff8e3d4a94593d009065ab0f39c51364f8a864ee7cee06cdb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServiceLevelObjectiveConfig(
            name=name,
            thresholds=thresholds,
            type=type,
            description=description,
            force_delete=force_delete,
            groups=groups,
            id=id,
            monitor_ids=monitor_ids,
            query=query,
            sli_specification=sli_specification,
            tags=tags,
            target_threshold=target_threshold,
            timeframe=timeframe,
            validate=validate,
            warning_threshold=warning_threshold,
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
        '''Generates CDKTF code for importing a ServiceLevelObjective resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ServiceLevelObjective to import.
        :param import_from_id: The id of the existing ServiceLevelObjective that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ServiceLevelObjective to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7792f03c4b5330b26a804dcbde84a9be98e472e7000466ef08d2b894b1927b44)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putQuery")
    def put_query(self, *, denominator: builtins.str, numerator: builtins.str) -> None:
        '''
        :param denominator: The sum of the ``total`` events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#denominator ServiceLevelObjective#denominator}
        :param numerator: The sum of all the ``good`` events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#numerator ServiceLevelObjective#numerator}
        '''
        value = ServiceLevelObjectiveQuery(
            denominator=denominator, numerator=numerator
        )

        return typing.cast(None, jsii.invoke(self, "putQuery", [value]))

    @jsii.member(jsii_name="putSliSpecification")
    def put_sli_specification(
        self,
        *,
        time_slice: typing.Union["ServiceLevelObjectiveSliSpecificationTimeSlice", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param time_slice: time_slice block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#time_slice ServiceLevelObjective#time_slice}
        '''
        value = ServiceLevelObjectiveSliSpecification(time_slice=time_slice)

        return typing.cast(None, jsii.invoke(self, "putSliSpecification", [value]))

    @jsii.member(jsii_name="putThresholds")
    def put_thresholds(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceLevelObjectiveThresholds", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eee0511af88251ff3f841d3eea5ddfae23448ff8113c58f2442ba1d879da05cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putThresholds", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetForceDelete")
    def reset_force_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDelete", []))

    @jsii.member(jsii_name="resetGroups")
    def reset_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroups", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMonitorIds")
    def reset_monitor_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorIds", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @jsii.member(jsii_name="resetSliSpecification")
    def reset_sli_specification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSliSpecification", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTargetThreshold")
    def reset_target_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetThreshold", []))

    @jsii.member(jsii_name="resetTimeframe")
    def reset_timeframe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeframe", []))

    @jsii.member(jsii_name="resetValidate")
    def reset_validate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidate", []))

    @jsii.member(jsii_name="resetWarningThreshold")
    def reset_warning_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarningThreshold", []))

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
    @jsii.member(jsii_name="query")
    def query(self) -> "ServiceLevelObjectiveQueryOutputReference":
        return typing.cast("ServiceLevelObjectiveQueryOutputReference", jsii.get(self, "query"))

    @builtins.property
    @jsii.member(jsii_name="sliSpecification")
    def sli_specification(
        self,
    ) -> "ServiceLevelObjectiveSliSpecificationOutputReference":
        return typing.cast("ServiceLevelObjectiveSliSpecificationOutputReference", jsii.get(self, "sliSpecification"))

    @builtins.property
    @jsii.member(jsii_name="thresholds")
    def thresholds(self) -> "ServiceLevelObjectiveThresholdsList":
        return typing.cast("ServiceLevelObjectiveThresholdsList", jsii.get(self, "thresholds"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDeleteInput")
    def force_delete_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsInput")
    def groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorIdsInput")
    def monitor_ids_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "monitorIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional["ServiceLevelObjectiveQuery"]:
        return typing.cast(typing.Optional["ServiceLevelObjectiveQuery"], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="sliSpecificationInput")
    def sli_specification_input(
        self,
    ) -> typing.Optional["ServiceLevelObjectiveSliSpecification"]:
        return typing.cast(typing.Optional["ServiceLevelObjectiveSliSpecification"], jsii.get(self, "sliSpecificationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetThresholdInput")
    def target_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdsInput")
    def thresholds_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLevelObjectiveThresholds"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLevelObjectiveThresholds"]]], jsii.get(self, "thresholdsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeframeInput")
    def timeframe_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeframeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="validateInput")
    def validate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "validateInput"))

    @builtins.property
    @jsii.member(jsii_name="warningThresholdInput")
    def warning_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "warningThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39031ab392683477559697ddae937aba45de71a24aeee6f1860bb8ded7d4a191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceDelete")
    def force_delete(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceDelete"))

    @force_delete.setter
    def force_delete(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be66be45447e983a11753a2a43dfed8f135ec6bea325e43e7f41147a746f821)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e1582c8809eacae55ab6262e514d73bd474c3a4386d4b216a68d186f6c6b6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__343bb9d1720006fee8bee5d7220cd6e701cc049ee331f3658295935fdb08b50b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitorIds")
    def monitor_ids(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "monitorIds"))

    @monitor_ids.setter
    def monitor_ids(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b620492081cf94a200a179acd0ec1d18cca903c91fbbca92b6ebdb36dab24f09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86d059cc07aef428d6b75797df742892160cb0478a746367237d856810e41af5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ac89e98ad2f05f3ce61005b9732c79759b2a629e1dae672e4f481801805b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetThreshold")
    def target_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetThreshold"))

    @target_threshold.setter
    def target_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f196be5bdc26e8a88d7b806627cdbf27762ccb00280a6156033bfab2d0e938)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeframe")
    def timeframe(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeframe"))

    @timeframe.setter
    def timeframe(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d653feed1369bf6fc868bbff2e63da9e838edb8ed732fe5affee89d47365f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeframe", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f84ca6c2b8ce36ac1f21df52416dbdfadad39016d5620908a0f69f7cdac9710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validate")
    def validate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "validate"))

    @validate.setter
    def validate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb8c766fdd59364dc581779f7e3153bb8b804e3502fffcda0db5fd026afa27ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warningThreshold")
    def warning_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "warningThreshold"))

    @warning_threshold.setter
    def warning_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f071981c2c3a8c8165a1a10bab8a24b71df3e03b1f2481dc2bf1ff85140bf625)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warningThreshold", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveConfig",
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
        "thresholds": "thresholds",
        "type": "type",
        "description": "description",
        "force_delete": "forceDelete",
        "groups": "groups",
        "id": "id",
        "monitor_ids": "monitorIds",
        "query": "query",
        "sli_specification": "sliSpecification",
        "tags": "tags",
        "target_threshold": "targetThreshold",
        "timeframe": "timeframe",
        "validate": "validate",
        "warning_threshold": "warningThreshold",
    },
)
class ServiceLevelObjectiveConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        thresholds: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceLevelObjectiveThresholds", typing.Dict[builtins.str, typing.Any]]]],
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        monitor_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
        query: typing.Optional[typing.Union["ServiceLevelObjectiveQuery", typing.Dict[builtins.str, typing.Any]]] = None,
        sli_specification: typing.Optional[typing.Union["ServiceLevelObjectiveSliSpecification", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_threshold: typing.Optional[jsii.Number] = None,
        timeframe: typing.Optional[builtins.str] = None,
        validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        warning_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of Datadog service level objective. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#name ServiceLevelObjective#name}
        :param thresholds: thresholds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#thresholds ServiceLevelObjective#thresholds}
        :param type: The type of the service level objective. The mapping from these types to the types found in the Datadog Web UI can be found in the Datadog API `documentation page <https://docs.datadoghq.com/api/v1/service-level-objectives/#create-a-slo-object>`_. Valid values are ``metric``, ``monitor``, ``time_slice``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#type ServiceLevelObjective#type}
        :param description: A description of this service level objective. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#description ServiceLevelObjective#description}
        :param force_delete: A boolean indicating whether this monitor can be deleted even if it's referenced by other resources (for example, dashboards). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#force_delete ServiceLevelObjective#force_delete}
        :param groups: A static set of groups to filter monitor-based SLOs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#groups ServiceLevelObjective#groups}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#id ServiceLevelObjective#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param monitor_ids: A static set of monitor IDs to use as part of the SLO. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#monitor_ids ServiceLevelObjective#monitor_ids}
        :param query: query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#query ServiceLevelObjective#query}
        :param sli_specification: sli_specification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#sli_specification ServiceLevelObjective#sli_specification}
        :param tags: A list of tags to associate with your service level objective. This can help you categorize and filter service level objectives in the service level objectives page of the UI. Note: it's not currently possible to filter by these tags when querying via the API Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#tags ServiceLevelObjective#tags}
        :param target_threshold: The objective's target in ``(0,100)``. This must match the corresponding thresholds of the primary time frame. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#target_threshold ServiceLevelObjective#target_threshold}
        :param timeframe: The primary time frame for the objective. The mapping from these types to the types found in the Datadog Web UI can be found in the Datadog API documentation page. Valid values are ``7d``, ``30d``, ``90d``, ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#timeframe ServiceLevelObjective#timeframe}
        :param validate: Whether or not to validate the SLO. It checks if monitors added to a monitor SLO already exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#validate ServiceLevelObjective#validate}
        :param warning_threshold: The objective's warning value in ``(0,100)``. This must be greater than the target value and match the corresponding thresholds of the primary time frame. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#warning_threshold ServiceLevelObjective#warning_threshold}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(query, dict):
            query = ServiceLevelObjectiveQuery(**query)
        if isinstance(sli_specification, dict):
            sli_specification = ServiceLevelObjectiveSliSpecification(**sli_specification)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb0a882d3049307ffc9d9cb776c8bc8d93f7c9d9482c4275c660dbe2be37fb18)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument thresholds", value=thresholds, expected_type=type_hints["thresholds"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument force_delete", value=force_delete, expected_type=type_hints["force_delete"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument monitor_ids", value=monitor_ids, expected_type=type_hints["monitor_ids"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument sli_specification", value=sli_specification, expected_type=type_hints["sli_specification"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_threshold", value=target_threshold, expected_type=type_hints["target_threshold"])
            check_type(argname="argument timeframe", value=timeframe, expected_type=type_hints["timeframe"])
            check_type(argname="argument validate", value=validate, expected_type=type_hints["validate"])
            check_type(argname="argument warning_threshold", value=warning_threshold, expected_type=type_hints["warning_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "thresholds": thresholds,
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
        if force_delete is not None:
            self._values["force_delete"] = force_delete
        if groups is not None:
            self._values["groups"] = groups
        if id is not None:
            self._values["id"] = id
        if monitor_ids is not None:
            self._values["monitor_ids"] = monitor_ids
        if query is not None:
            self._values["query"] = query
        if sli_specification is not None:
            self._values["sli_specification"] = sli_specification
        if tags is not None:
            self._values["tags"] = tags
        if target_threshold is not None:
            self._values["target_threshold"] = target_threshold
        if timeframe is not None:
            self._values["timeframe"] = timeframe
        if validate is not None:
            self._values["validate"] = validate
        if warning_threshold is not None:
            self._values["warning_threshold"] = warning_threshold

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
        '''Name of Datadog service level objective.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#name ServiceLevelObjective#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def thresholds(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLevelObjectiveThresholds"]]:
        '''thresholds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#thresholds ServiceLevelObjective#thresholds}
        '''
        result = self._values.get("thresholds")
        assert result is not None, "Required property 'thresholds' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLevelObjectiveThresholds"]], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the service level objective.

        The mapping from these types to the types found in the Datadog Web UI can be found in the Datadog API `documentation page <https://docs.datadoghq.com/api/v1/service-level-objectives/#create-a-slo-object>`_. Valid values are ``metric``, ``monitor``, ``time_slice``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#type ServiceLevelObjective#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of this service level objective.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#description ServiceLevelObjective#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean indicating whether this monitor can be deleted even if it's referenced by other resources (for example, dashboards).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#force_delete ServiceLevelObjective#force_delete}
        '''
        result = self._values.get("force_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A static set of groups to filter monitor-based SLOs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#groups ServiceLevelObjective#groups}
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#id ServiceLevelObjective#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitor_ids(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''A static set of monitor IDs to use as part of the SLO.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#monitor_ids ServiceLevelObjective#monitor_ids}
        '''
        result = self._values.get("monitor_ids")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def query(self) -> typing.Optional["ServiceLevelObjectiveQuery"]:
        '''query block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#query ServiceLevelObjective#query}
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional["ServiceLevelObjectiveQuery"], result)

    @builtins.property
    def sli_specification(
        self,
    ) -> typing.Optional["ServiceLevelObjectiveSliSpecification"]:
        '''sli_specification block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#sli_specification ServiceLevelObjective#sli_specification}
        '''
        result = self._values.get("sli_specification")
        return typing.cast(typing.Optional["ServiceLevelObjectiveSliSpecification"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of tags to associate with your service level objective.

        This can help you categorize and filter service level objectives in the service level objectives page of the UI. Note: it's not currently possible to filter by these tags when querying via the API

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#tags ServiceLevelObjective#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_threshold(self) -> typing.Optional[jsii.Number]:
        '''The objective's target in ``(0,100)``. This must match the corresponding thresholds of the primary time frame.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#target_threshold ServiceLevelObjective#target_threshold}
        '''
        result = self._values.get("target_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeframe(self) -> typing.Optional[builtins.str]:
        '''The primary time frame for the objective.

        The mapping from these types to the types found in the Datadog Web UI can be found in the Datadog API documentation page. Valid values are ``7d``, ``30d``, ``90d``, ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#timeframe ServiceLevelObjective#timeframe}
        '''
        result = self._values.get("timeframe")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not to validate the SLO. It checks if monitors added to a monitor SLO already exist.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#validate ServiceLevelObjective#validate}
        '''
        result = self._values.get("validate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def warning_threshold(self) -> typing.Optional[jsii.Number]:
        '''The objective's warning value in ``(0,100)``.

        This must be greater than the target value and match the corresponding thresholds of the primary time frame.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#warning_threshold ServiceLevelObjective#warning_threshold}
        '''
        result = self._values.get("warning_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelObjectiveConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveQuery",
    jsii_struct_bases=[],
    name_mapping={"denominator": "denominator", "numerator": "numerator"},
)
class ServiceLevelObjectiveQuery:
    def __init__(self, *, denominator: builtins.str, numerator: builtins.str) -> None:
        '''
        :param denominator: The sum of the ``total`` events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#denominator ServiceLevelObjective#denominator}
        :param numerator: The sum of all the ``good`` events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#numerator ServiceLevelObjective#numerator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__268e427658d3899ed81ea172f685c0cee60658032a0441d2aa0184c1e8b51c42)
            check_type(argname="argument denominator", value=denominator, expected_type=type_hints["denominator"])
            check_type(argname="argument numerator", value=numerator, expected_type=type_hints["numerator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "denominator": denominator,
            "numerator": numerator,
        }

    @builtins.property
    def denominator(self) -> builtins.str:
        '''The sum of the ``total`` events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#denominator ServiceLevelObjective#denominator}
        '''
        result = self._values.get("denominator")
        assert result is not None, "Required property 'denominator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def numerator(self) -> builtins.str:
        '''The sum of all the ``good`` events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#numerator ServiceLevelObjective#numerator}
        '''
        result = self._values.get("numerator")
        assert result is not None, "Required property 'numerator' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelObjectiveQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelObjectiveQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__948c92f863d870165d686218a2d822ea36ebb8a4f0e54b9f6650800d78e25af2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="denominatorInput")
    def denominator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "denominatorInput"))

    @builtins.property
    @jsii.member(jsii_name="numeratorInput")
    def numerator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "numeratorInput"))

    @builtins.property
    @jsii.member(jsii_name="denominator")
    def denominator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "denominator"))

    @denominator.setter
    def denominator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__568d34e5d5567f6262fe2ddb2b0fc7c52f21c63b9c69b1e521cb95ceeb704e29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "denominator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numerator")
    def numerator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "numerator"))

    @numerator.setter
    def numerator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee039ac7735b0e9d3480fe92c2b851b92b1dec39b3570be3dbbc61163f9b09bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numerator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceLevelObjectiveQuery]:
        return typing.cast(typing.Optional[ServiceLevelObjectiveQuery], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceLevelObjectiveQuery],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4008a8ababe5e2b3440b456ca2274d7187a3aaa582a19257d8d87740f7fb68f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveSliSpecification",
    jsii_struct_bases=[],
    name_mapping={"time_slice": "timeSlice"},
)
class ServiceLevelObjectiveSliSpecification:
    def __init__(
        self,
        *,
        time_slice: typing.Union["ServiceLevelObjectiveSliSpecificationTimeSlice", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param time_slice: time_slice block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#time_slice ServiceLevelObjective#time_slice}
        '''
        if isinstance(time_slice, dict):
            time_slice = ServiceLevelObjectiveSliSpecificationTimeSlice(**time_slice)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__280a1e7afe1143a94d1e952ce117c34887b4b7d37814d24c3f69d3e7dd201087)
            check_type(argname="argument time_slice", value=time_slice, expected_type=type_hints["time_slice"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "time_slice": time_slice,
        }

    @builtins.property
    def time_slice(self) -> "ServiceLevelObjectiveSliSpecificationTimeSlice":
        '''time_slice block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#time_slice ServiceLevelObjective#time_slice}
        '''
        result = self._values.get("time_slice")
        assert result is not None, "Required property 'time_slice' is missing"
        return typing.cast("ServiceLevelObjectiveSliSpecificationTimeSlice", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelObjectiveSliSpecification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelObjectiveSliSpecificationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveSliSpecificationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4968337942e5e371ec084e68842b0c22f0476b67e63c4a92003a99a92ab3c0e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTimeSlice")
    def put_time_slice(
        self,
        *,
        comparator: builtins.str,
        query: typing.Union["ServiceLevelObjectiveSliSpecificationTimeSliceQuery", typing.Dict[builtins.str, typing.Any]],
        threshold: jsii.Number,
        query_interval_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param comparator: The comparator used to compare the SLI value to the threshold. Valid values are ``>``, ``>=``, ``<``, ``<=``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#comparator ServiceLevelObjective#comparator}
        :param query: query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#query ServiceLevelObjective#query}
        :param threshold: The threshold value to which each SLI value will be compared. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#threshold ServiceLevelObjective#threshold}
        :param query_interval_seconds: The interval used when querying data, which defines the size of a time slice. Valid values are ``60``, ``300``. Defaults to ``300``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#query_interval_seconds ServiceLevelObjective#query_interval_seconds}
        '''
        value = ServiceLevelObjectiveSliSpecificationTimeSlice(
            comparator=comparator,
            query=query,
            threshold=threshold,
            query_interval_seconds=query_interval_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putTimeSlice", [value]))

    @builtins.property
    @jsii.member(jsii_name="timeSlice")
    def time_slice(
        self,
    ) -> "ServiceLevelObjectiveSliSpecificationTimeSliceOutputReference":
        return typing.cast("ServiceLevelObjectiveSliSpecificationTimeSliceOutputReference", jsii.get(self, "timeSlice"))

    @builtins.property
    @jsii.member(jsii_name="timeSliceInput")
    def time_slice_input(
        self,
    ) -> typing.Optional["ServiceLevelObjectiveSliSpecificationTimeSlice"]:
        return typing.cast(typing.Optional["ServiceLevelObjectiveSliSpecificationTimeSlice"], jsii.get(self, "timeSliceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceLevelObjectiveSliSpecification]:
        return typing.cast(typing.Optional[ServiceLevelObjectiveSliSpecification], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceLevelObjectiveSliSpecification],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c1bb7ce87f35f0e43ceb7f94748d7bc4c4bf96f5371fcaeeb575458355efa9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveSliSpecificationTimeSlice",
    jsii_struct_bases=[],
    name_mapping={
        "comparator": "comparator",
        "query": "query",
        "threshold": "threshold",
        "query_interval_seconds": "queryIntervalSeconds",
    },
)
class ServiceLevelObjectiveSliSpecificationTimeSlice:
    def __init__(
        self,
        *,
        comparator: builtins.str,
        query: typing.Union["ServiceLevelObjectiveSliSpecificationTimeSliceQuery", typing.Dict[builtins.str, typing.Any]],
        threshold: jsii.Number,
        query_interval_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param comparator: The comparator used to compare the SLI value to the threshold. Valid values are ``>``, ``>=``, ``<``, ``<=``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#comparator ServiceLevelObjective#comparator}
        :param query: query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#query ServiceLevelObjective#query}
        :param threshold: The threshold value to which each SLI value will be compared. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#threshold ServiceLevelObjective#threshold}
        :param query_interval_seconds: The interval used when querying data, which defines the size of a time slice. Valid values are ``60``, ``300``. Defaults to ``300``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#query_interval_seconds ServiceLevelObjective#query_interval_seconds}
        '''
        if isinstance(query, dict):
            query = ServiceLevelObjectiveSliSpecificationTimeSliceQuery(**query)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78436a00e8a01933eeb9edf9257cb1fa9b0404c91bdcf8e72a86f0a488828c08)
            check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument query_interval_seconds", value=query_interval_seconds, expected_type=type_hints["query_interval_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparator": comparator,
            "query": query,
            "threshold": threshold,
        }
        if query_interval_seconds is not None:
            self._values["query_interval_seconds"] = query_interval_seconds

    @builtins.property
    def comparator(self) -> builtins.str:
        '''The comparator used to compare the SLI value to the threshold. Valid values are ``>``, ``>=``, ``<``, ``<=``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#comparator ServiceLevelObjective#comparator}
        '''
        result = self._values.get("comparator")
        assert result is not None, "Required property 'comparator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query(self) -> "ServiceLevelObjectiveSliSpecificationTimeSliceQuery":
        '''query block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#query ServiceLevelObjective#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast("ServiceLevelObjectiveSliSpecificationTimeSliceQuery", result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The threshold value to which each SLI value will be compared.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#threshold ServiceLevelObjective#threshold}
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def query_interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''The interval used when querying data, which defines the size of a time slice.

        Valid values are ``60``, ``300``. Defaults to ``300``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#query_interval_seconds ServiceLevelObjective#query_interval_seconds}
        '''
        result = self._values.get("query_interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelObjectiveSliSpecificationTimeSlice(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelObjectiveSliSpecificationTimeSliceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveSliSpecificationTimeSliceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__242d1a0f06802bbde34c1ec0cd376b72947b7b2e0b326633169787ff34d2bd4a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putQuery")
    def put_query(
        self,
        *,
        formula: typing.Union["ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormula", typing.Dict[builtins.str, typing.Any]],
        query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param formula: formula block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#formula ServiceLevelObjective#formula}
        :param query: query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#query ServiceLevelObjective#query}
        '''
        value = ServiceLevelObjectiveSliSpecificationTimeSliceQuery(
            formula=formula, query=query
        )

        return typing.cast(None, jsii.invoke(self, "putQuery", [value]))

    @jsii.member(jsii_name="resetQueryIntervalSeconds")
    def reset_query_interval_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryIntervalSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(
        self,
    ) -> "ServiceLevelObjectiveSliSpecificationTimeSliceQueryOutputReference":
        return typing.cast("ServiceLevelObjectiveSliSpecificationTimeSliceQueryOutputReference", jsii.get(self, "query"))

    @builtins.property
    @jsii.member(jsii_name="comparatorInput")
    def comparator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(
        self,
    ) -> typing.Optional["ServiceLevelObjectiveSliSpecificationTimeSliceQuery"]:
        return typing.cast(typing.Optional["ServiceLevelObjectiveSliSpecificationTimeSliceQuery"], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="queryIntervalSecondsInput")
    def query_interval_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queryIntervalSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdInput")
    def threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="comparator")
    def comparator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparator"))

    @comparator.setter
    def comparator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b792764487631889fbc51d352b8f94fe314f498be2c516536218fe527c57abe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryIntervalSeconds")
    def query_interval_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queryIntervalSeconds"))

    @query_interval_seconds.setter
    def query_interval_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c297d34705bae55de99a53b1889564951b7deac9081026be06628ba48a84be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryIntervalSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85dcdd85c5517cff0ebecb11b4332a0b4f41b4598f4375be076b523dc7c3ac66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSlice]:
        return typing.cast(typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSlice], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSlice],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74de5ab41f07819c9c042e7cc673d1f2292471e80c0023794dc9709f38618ec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveSliSpecificationTimeSliceQuery",
    jsii_struct_bases=[],
    name_mapping={"formula": "formula", "query": "query"},
)
class ServiceLevelObjectiveSliSpecificationTimeSliceQuery:
    def __init__(
        self,
        *,
        formula: typing.Union["ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormula", typing.Dict[builtins.str, typing.Any]],
        query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param formula: formula block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#formula ServiceLevelObjective#formula}
        :param query: query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#query ServiceLevelObjective#query}
        '''
        if isinstance(formula, dict):
            formula = ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormula(**formula)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc2b8a7a00cc8a75e97fdf0f11f910d2ca06309ca53b3acb04dc0c60334c7618)
            check_type(argname="argument formula", value=formula, expected_type=type_hints["formula"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "formula": formula,
            "query": query,
        }

    @builtins.property
    def formula(self) -> "ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormula":
        '''formula block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#formula ServiceLevelObjective#formula}
        '''
        result = self._values.get("formula")
        assert result is not None, "Required property 'formula' is missing"
        return typing.cast("ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormula", result)

    @builtins.property
    def query(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery"]]:
        '''query block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#query ServiceLevelObjective#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelObjectiveSliSpecificationTimeSliceQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormula",
    jsii_struct_bases=[],
    name_mapping={"formula_expression": "formulaExpression"},
)
class ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormula:
    def __init__(self, *, formula_expression: builtins.str) -> None:
        '''
        :param formula_expression: The formula string, which is an expression involving named queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#formula_expression ServiceLevelObjective#formula_expression}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5d9e685a20717a59c30b7ca574fc9c3fc7e2beccfbc14e018d0477cee4b69b)
            check_type(argname="argument formula_expression", value=formula_expression, expected_type=type_hints["formula_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "formula_expression": formula_expression,
        }

    @builtins.property
    def formula_expression(self) -> builtins.str:
        '''The formula string, which is an expression involving named queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#formula_expression ServiceLevelObjective#formula_expression}
        '''
        result = self._values.get("formula_expression")
        assert result is not None, "Required property 'formula_expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormula(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormulaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormulaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f797ce8c721ded3640a9221da5148b8d7296f5ac7280403d146b40ca59ce765)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="formulaExpressionInput")
    def formula_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formulaExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="formulaExpression")
    def formula_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "formulaExpression"))

    @formula_expression.setter
    def formula_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__610773a62ab4dbea1991193381f3e1c28f4e57e21d9549529024364cf0702ba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formulaExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormula]:
        return typing.cast(typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormula], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormula],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e66c0d47568edb830fcd31eec91bb2a4f91d7e233af6ef6ccc0b22225f76bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceLevelObjectiveSliSpecificationTimeSliceQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveSliSpecificationTimeSliceQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2969794b2f6c56f5359b4e33b1875408a6daa7c1f6eb2c0a5f1e6b79b30bd4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFormula")
    def put_formula(self, *, formula_expression: builtins.str) -> None:
        '''
        :param formula_expression: The formula string, which is an expression involving named queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#formula_expression ServiceLevelObjective#formula_expression}
        '''
        value = ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormula(
            formula_expression=formula_expression
        )

        return typing.cast(None, jsii.invoke(self, "putFormula", [value]))

    @jsii.member(jsii_name="putQuery")
    def put_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98f2e0624df455f97cf86809b25f27d26cc05e3d885a63f4dde0c1143d51684e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQuery", [value]))

    @builtins.property
    @jsii.member(jsii_name="formula")
    def formula(
        self,
    ) -> ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormulaOutputReference:
        return typing.cast(ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormulaOutputReference, jsii.get(self, "formula"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> "ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryList":
        return typing.cast("ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryList", jsii.get(self, "query"))

    @builtins.property
    @jsii.member(jsii_name="formulaInput")
    def formula_input(
        self,
    ) -> typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormula]:
        return typing.cast(typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormula], jsii.get(self, "formulaInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery"]]], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSliceQuery]:
        return typing.cast(typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSliceQuery], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSliceQuery],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed6a4283b394519700310006010a7fc47dcb4bbe5b0c77f20b1c8c60a12488c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery",
    jsii_struct_bases=[],
    name_mapping={"metric_query": "metricQuery"},
)
class ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery:
    def __init__(
        self,
        *,
        metric_query: typing.Optional[typing.Union["ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQuery", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metric_query: metric_query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#metric_query ServiceLevelObjective#metric_query}
        '''
        if isinstance(metric_query, dict):
            metric_query = ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQuery(**metric_query)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba3760bed2e93a76949ef3c0e2499ad53e7436f6b9f8158d83bbe4083fdb3599)
            check_type(argname="argument metric_query", value=metric_query, expected_type=type_hints["metric_query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metric_query is not None:
            self._values["metric_query"] = metric_query

    @builtins.property
    def metric_query(
        self,
    ) -> typing.Optional["ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQuery"]:
        '''metric_query block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#metric_query ServiceLevelObjective#metric_query}
        '''
        result = self._values.get("metric_query")
        return typing.cast(typing.Optional["ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQuery"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d67caf95d0c00169dfc3e397bb197de9bade501f6451966daccb4855f798d68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c88a4cf83bd761e158f9565d2e44c8d6d537e32100f528c422d0aa15f21b8a41)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b5fdfdd432b0be0cd822aa5cd4efe1dfaac7b762a43f853f90268b859acdc44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad4a52e006ffb90588cf7f1b8d100d341718ace000b9bc0e099354b98fe173f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb943af594419ce417c85cda500a897a77a68f959cbfafc1c96bb08af1b14d5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c22dbc2b8dc31879748a3f2dbce90ba27f496c55c2594ed5f52ca9db3cf348f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQuery",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "query": "query", "data_source": "dataSource"},
)
class ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQuery:
    def __init__(
        self,
        *,
        name: builtins.str,
        query: builtins.str,
        data_source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the query for use in formulas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#name ServiceLevelObjective#name}
        :param query: The metrics query definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#query ServiceLevelObjective#query}
        :param data_source: The data source for metrics queries. Defaults to ``"metrics"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#data_source ServiceLevelObjective#data_source}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c06384952932169c29b1aaefdcee0d8098afccf7adbb1c9559237d9d3fc24b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "query": query,
        }
        if data_source is not None:
            self._values["data_source"] = data_source

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the query for use in formulas.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#name ServiceLevelObjective#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query(self) -> builtins.str:
        '''The metrics query definition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#query ServiceLevelObjective#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_source(self) -> typing.Optional[builtins.str]:
        '''The data source for metrics queries. Defaults to ``"metrics"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#data_source ServiceLevelObjective#data_source}
        '''
        result = self._values.get("data_source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ac88785eecf1bf3997902cfd6be69b149b095ba310deab182e7285cfd39ea7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataSource")
    def reset_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataSource", []))

    @builtins.property
    @jsii.member(jsii_name="dataSourceInput")
    def data_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSource")
    def data_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSource"))

    @data_source.setter
    def data_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c44774e428c3a00492843fac7a5dbfcc51d572247222005d73dac2e602067701)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1da4383dd8b2407023c93efbb23b3ccb3433494b1efa5b876edef0546d772d83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03b830f49090f65933fa3655a7491c7b723cb1f2ec7a1d960d0ce4d630ca150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQuery]:
        return typing.cast(typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQuery], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQuery],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de8cb371ffaaaebeb3e4daeed5f2cf5a087fc45452655f854612e30cc75d1c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34ab9f4c005fdc861976cd0bf72b603c9f823df95daf1ff0756a979c10ea14b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMetricQuery")
    def put_metric_query(
        self,
        *,
        name: builtins.str,
        query: builtins.str,
        data_source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the query for use in formulas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#name ServiceLevelObjective#name}
        :param query: The metrics query definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#query ServiceLevelObjective#query}
        :param data_source: The data source for metrics queries. Defaults to ``"metrics"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#data_source ServiceLevelObjective#data_source}
        '''
        value = ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQuery(
            name=name, query=query, data_source=data_source
        )

        return typing.cast(None, jsii.invoke(self, "putMetricQuery", [value]))

    @jsii.member(jsii_name="resetMetricQuery")
    def reset_metric_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricQuery", []))

    @builtins.property
    @jsii.member(jsii_name="metricQuery")
    def metric_query(
        self,
    ) -> ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQueryOutputReference:
        return typing.cast(ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQueryOutputReference, jsii.get(self, "metricQuery"))

    @builtins.property
    @jsii.member(jsii_name="metricQueryInput")
    def metric_query_input(
        self,
    ) -> typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQuery]:
        return typing.cast(typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQuery], jsii.get(self, "metricQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22448a59d481ca66b4272cbf80de2279ac623f6b1bf9b4cf90c9925ee21d2f1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveThresholds",
    jsii_struct_bases=[],
    name_mapping={"target": "target", "timeframe": "timeframe", "warning": "warning"},
)
class ServiceLevelObjectiveThresholds:
    def __init__(
        self,
        *,
        target: jsii.Number,
        timeframe: builtins.str,
        warning: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param target: The objective's target in ``(0,100)``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#target ServiceLevelObjective#target}
        :param timeframe: The time frame for the objective. The mapping from these types to the types found in the Datadog Web UI can be found in the Datadog API documentation page. Valid values are ``7d``, ``30d``, ``90d``, ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#timeframe ServiceLevelObjective#timeframe}
        :param warning: The objective's warning value in ``(0,100)``. This must be greater than the target value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#warning ServiceLevelObjective#warning}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__708fb67636caab56311bbb3038cac267a56a064003dfa3c0a8eb18ed80f260db)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument timeframe", value=timeframe, expected_type=type_hints["timeframe"])
            check_type(argname="argument warning", value=warning, expected_type=type_hints["warning"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
            "timeframe": timeframe,
        }
        if warning is not None:
            self._values["warning"] = warning

    @builtins.property
    def target(self) -> jsii.Number:
        '''The objective's target in ``(0,100)``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#target ServiceLevelObjective#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def timeframe(self) -> builtins.str:
        '''The time frame for the objective.

        The mapping from these types to the types found in the Datadog Web UI can be found in the Datadog API documentation page. Valid values are ``7d``, ``30d``, ``90d``, ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#timeframe ServiceLevelObjective#timeframe}
        '''
        result = self._values.get("timeframe")
        assert result is not None, "Required property 'timeframe' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def warning(self) -> typing.Optional[jsii.Number]:
        '''The objective's warning value in ``(0,100)``. This must be greater than the target value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/service_level_objective#warning ServiceLevelObjective#warning}
        '''
        result = self._values.get("warning")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelObjectiveThresholds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelObjectiveThresholdsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveThresholdsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10bae5ad06a4cc14c9785d193dee23f14166e1cd064ecd9f65db1de50f2d475c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceLevelObjectiveThresholdsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2457d740e602f90234fc0792d09948873f207d015b3d5a61fb40f8ca432c280)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceLevelObjectiveThresholdsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe2801235acef66be7304bbc8e64c524858f07ff3bcc4e2cca40a81f4c49c83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__709e17a06465337b2e143a3554798620bd8194f96ec05ad03e9ae4409044d66d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cea3c1a886a7d5504f55b05582f49064a3db93548381357683d38ea4272a1826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLevelObjectiveThresholds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLevelObjectiveThresholds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLevelObjectiveThresholds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e440c67b79888a615dc177d1e0ab34011448230699b02011ad660663a7281937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceLevelObjectiveThresholdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveThresholdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2895a3f729396c9ee63ac73a5449707ed2c9b6c639b356eda51187c1f0d64f3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetWarning")
    def reset_warning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarning", []))

    @builtins.property
    @jsii.member(jsii_name="targetDisplay")
    def target_display(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetDisplay"))

    @builtins.property
    @jsii.member(jsii_name="warningDisplay")
    def warning_display(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warningDisplay"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeframeInput")
    def timeframe_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeframeInput"))

    @builtins.property
    @jsii.member(jsii_name="warningInput")
    def warning_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "warningInput"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "target"))

    @target.setter
    def target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd8827b9c81c1133d50084136c83bf1237767f26d8bc25ee61c33d9a941610f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeframe")
    def timeframe(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeframe"))

    @timeframe.setter
    def timeframe(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a04afe1ff2379ca673330d58dba4ffe3fd345c187cee7f13b7fcae389b2c676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeframe", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warning")
    def warning(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "warning"))

    @warning.setter
    def warning(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b3dacb7b155ac13089cbc9eeb17a38c6e1b463a513342fdd58f3a51dfe79ee2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warning", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceLevelObjectiveThresholds]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceLevelObjectiveThresholds]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceLevelObjectiveThresholds]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4132001a03036d397b5948c2ad78e307bfb4015fa93750ffb3a1b41901f740ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ServiceLevelObjective",
    "ServiceLevelObjectiveConfig",
    "ServiceLevelObjectiveQuery",
    "ServiceLevelObjectiveQueryOutputReference",
    "ServiceLevelObjectiveSliSpecification",
    "ServiceLevelObjectiveSliSpecificationOutputReference",
    "ServiceLevelObjectiveSliSpecificationTimeSlice",
    "ServiceLevelObjectiveSliSpecificationTimeSliceOutputReference",
    "ServiceLevelObjectiveSliSpecificationTimeSliceQuery",
    "ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormula",
    "ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormulaOutputReference",
    "ServiceLevelObjectiveSliSpecificationTimeSliceQueryOutputReference",
    "ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery",
    "ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryList",
    "ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQuery",
    "ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQueryOutputReference",
    "ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryOutputReference",
    "ServiceLevelObjectiveThresholds",
    "ServiceLevelObjectiveThresholdsList",
    "ServiceLevelObjectiveThresholdsOutputReference",
]

publication.publish()

def _typecheckingstub__5669eb7d0a788a9ff8e3d4a94593d009065ab0f39c51364f8a864ee7cee06cdb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    thresholds: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceLevelObjectiveThresholds, typing.Dict[builtins.str, typing.Any]]]],
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    monitor_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
    query: typing.Optional[typing.Union[ServiceLevelObjectiveQuery, typing.Dict[builtins.str, typing.Any]]] = None,
    sli_specification: typing.Optional[typing.Union[ServiceLevelObjectiveSliSpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_threshold: typing.Optional[jsii.Number] = None,
    timeframe: typing.Optional[builtins.str] = None,
    validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    warning_threshold: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__7792f03c4b5330b26a804dcbde84a9be98e472e7000466ef08d2b894b1927b44(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee0511af88251ff3f841d3eea5ddfae23448ff8113c58f2442ba1d879da05cb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceLevelObjectiveThresholds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39031ab392683477559697ddae937aba45de71a24aeee6f1860bb8ded7d4a191(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be66be45447e983a11753a2a43dfed8f135ec6bea325e43e7f41147a746f821(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e1582c8809eacae55ab6262e514d73bd474c3a4386d4b216a68d186f6c6b6a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__343bb9d1720006fee8bee5d7220cd6e701cc049ee331f3658295935fdb08b50b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b620492081cf94a200a179acd0ec1d18cca903c91fbbca92b6ebdb36dab24f09(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d059cc07aef428d6b75797df742892160cb0478a746367237d856810e41af5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ac89e98ad2f05f3ce61005b9732c79759b2a629e1dae672e4f481801805b69(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f196be5bdc26e8a88d7b806627cdbf27762ccb00280a6156033bfab2d0e938(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d653feed1369bf6fc868bbff2e63da9e838edb8ed732fe5affee89d47365f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f84ca6c2b8ce36ac1f21df52416dbdfadad39016d5620908a0f69f7cdac9710(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8c766fdd59364dc581779f7e3153bb8b804e3502fffcda0db5fd026afa27ad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f071981c2c3a8c8165a1a10bab8a24b71df3e03b1f2481dc2bf1ff85140bf625(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0a882d3049307ffc9d9cb776c8bc8d93f7c9d9482c4275c660dbe2be37fb18(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    thresholds: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceLevelObjectiveThresholds, typing.Dict[builtins.str, typing.Any]]]],
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    monitor_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
    query: typing.Optional[typing.Union[ServiceLevelObjectiveQuery, typing.Dict[builtins.str, typing.Any]]] = None,
    sli_specification: typing.Optional[typing.Union[ServiceLevelObjectiveSliSpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_threshold: typing.Optional[jsii.Number] = None,
    timeframe: typing.Optional[builtins.str] = None,
    validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    warning_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__268e427658d3899ed81ea172f685c0cee60658032a0441d2aa0184c1e8b51c42(
    *,
    denominator: builtins.str,
    numerator: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__948c92f863d870165d686218a2d822ea36ebb8a4f0e54b9f6650800d78e25af2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__568d34e5d5567f6262fe2ddb2b0fc7c52f21c63b9c69b1e521cb95ceeb704e29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee039ac7735b0e9d3480fe92c2b851b92b1dec39b3570be3dbbc61163f9b09bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4008a8ababe5e2b3440b456ca2274d7187a3aaa582a19257d8d87740f7fb68f(
    value: typing.Optional[ServiceLevelObjectiveQuery],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__280a1e7afe1143a94d1e952ce117c34887b4b7d37814d24c3f69d3e7dd201087(
    *,
    time_slice: typing.Union[ServiceLevelObjectiveSliSpecificationTimeSlice, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4968337942e5e371ec084e68842b0c22f0476b67e63c4a92003a99a92ab3c0e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1bb7ce87f35f0e43ceb7f94748d7bc4c4bf96f5371fcaeeb575458355efa9b(
    value: typing.Optional[ServiceLevelObjectiveSliSpecification],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78436a00e8a01933eeb9edf9257cb1fa9b0404c91bdcf8e72a86f0a488828c08(
    *,
    comparator: builtins.str,
    query: typing.Union[ServiceLevelObjectiveSliSpecificationTimeSliceQuery, typing.Dict[builtins.str, typing.Any]],
    threshold: jsii.Number,
    query_interval_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242d1a0f06802bbde34c1ec0cd376b72947b7b2e0b326633169787ff34d2bd4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b792764487631889fbc51d352b8f94fe314f498be2c516536218fe527c57abe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c297d34705bae55de99a53b1889564951b7deac9081026be06628ba48a84be(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85dcdd85c5517cff0ebecb11b4332a0b4f41b4598f4375be076b523dc7c3ac66(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74de5ab41f07819c9c042e7cc673d1f2292471e80c0023794dc9709f38618ec4(
    value: typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSlice],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2b8a7a00cc8a75e97fdf0f11f910d2ca06309ca53b3acb04dc0c60334c7618(
    *,
    formula: typing.Union[ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormula, typing.Dict[builtins.str, typing.Any]],
    query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5d9e685a20717a59c30b7ca574fc9c3fc7e2beccfbc14e018d0477cee4b69b(
    *,
    formula_expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f797ce8c721ded3640a9221da5148b8d7296f5ac7280403d146b40ca59ce765(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610773a62ab4dbea1991193381f3e1c28f4e57e21d9549529024364cf0702ba9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e66c0d47568edb830fcd31eec91bb2a4f91d7e233af6ef6ccc0b22225f76bc7(
    value: typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSliceQueryFormula],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2969794b2f6c56f5359b4e33b1875408a6daa7c1f6eb2c0a5f1e6b79b30bd4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98f2e0624df455f97cf86809b25f27d26cc05e3d885a63f4dde0c1143d51684e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed6a4283b394519700310006010a7fc47dcb4bbe5b0c77f20b1c8c60a12488c7(
    value: typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSliceQuery],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3760bed2e93a76949ef3c0e2499ad53e7436f6b9f8158d83bbe4083fdb3599(
    *,
    metric_query: typing.Optional[typing.Union[ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQuery, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d67caf95d0c00169dfc3e397bb197de9bade501f6451966daccb4855f798d68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88a4cf83bd761e158f9565d2e44c8d6d537e32100f528c422d0aa15f21b8a41(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5fdfdd432b0be0cd822aa5cd4efe1dfaac7b762a43f853f90268b859acdc44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad4a52e006ffb90588cf7f1b8d100d341718ace000b9bc0e099354b98fe173f9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb943af594419ce417c85cda500a897a77a68f959cbfafc1c96bb08af1b14d5c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c22dbc2b8dc31879748a3f2dbce90ba27f496c55c2594ed5f52ca9db3cf348f4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c06384952932169c29b1aaefdcee0d8098afccf7adbb1c9559237d9d3fc24b(
    *,
    name: builtins.str,
    query: builtins.str,
    data_source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac88785eecf1bf3997902cfd6be69b149b095ba310deab182e7285cfd39ea7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44774e428c3a00492843fac7a5dbfcc51d572247222005d73dac2e602067701(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da4383dd8b2407023c93efbb23b3ccb3433494b1efa5b876edef0546d772d83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03b830f49090f65933fa3655a7491c7b723cb1f2ec7a1d960d0ce4d630ca150(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de8cb371ffaaaebeb3e4daeed5f2cf5a087fc45452655f854612e30cc75d1c4(
    value: typing.Optional[ServiceLevelObjectiveSliSpecificationTimeSliceQueryQueryMetricQuery],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ab9f4c005fdc861976cd0bf72b603c9f823df95daf1ff0756a979c10ea14b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22448a59d481ca66b4272cbf80de2279ac623f6b1bf9b4cf90c9925ee21d2f1c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceLevelObjectiveSliSpecificationTimeSliceQueryQuery]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__708fb67636caab56311bbb3038cac267a56a064003dfa3c0a8eb18ed80f260db(
    *,
    target: jsii.Number,
    timeframe: builtins.str,
    warning: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10bae5ad06a4cc14c9785d193dee23f14166e1cd064ecd9f65db1de50f2d475c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2457d740e602f90234fc0792d09948873f207d015b3d5a61fb40f8ca432c280(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe2801235acef66be7304bbc8e64c524858f07ff3bcc4e2cca40a81f4c49c83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709e17a06465337b2e143a3554798620bd8194f96ec05ad03e9ae4409044d66d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea3c1a886a7d5504f55b05582f49064a3db93548381357683d38ea4272a1826(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e440c67b79888a615dc177d1e0ab34011448230699b02011ad660663a7281937(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLevelObjectiveThresholds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2895a3f729396c9ee63ac73a5449707ed2c9b6c639b356eda51187c1f0d64f3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8827b9c81c1133d50084136c83bf1237767f26d8bc25ee61c33d9a941610f5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a04afe1ff2379ca673330d58dba4ffe3fd345c187cee7f13b7fcae389b2c676(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b3dacb7b155ac13089cbc9eeb17a38c6e1b463a513342fdd58f3a51dfe79ee2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4132001a03036d397b5948c2ad78e307bfb4015fa93750ffb3a1b41901f740ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceLevelObjectiveThresholds]],
) -> None:
    """Type checking stubs"""
    pass

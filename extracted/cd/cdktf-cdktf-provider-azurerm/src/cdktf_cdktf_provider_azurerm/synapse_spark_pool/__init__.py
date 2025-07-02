r'''
# `azurerm_synapse_spark_pool`

Refer to the Terraform Registry for docs: [`azurerm_synapse_spark_pool`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool).
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


class SynapseSparkPool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.synapseSparkPool.SynapseSparkPool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool azurerm_synapse_spark_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        node_size: builtins.str,
        node_size_family: builtins.str,
        spark_version: builtins.str,
        synapse_workspace_id: builtins.str,
        auto_pause: typing.Optional[typing.Union["SynapseSparkPoolAutoPause", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_scale: typing.Optional[typing.Union["SynapseSparkPoolAutoScale", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_size: typing.Optional[jsii.Number] = None,
        compute_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dynamic_executor_allocation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        library_requirement: typing.Optional[typing.Union["SynapseSparkPoolLibraryRequirement", typing.Dict[builtins.str, typing.Any]]] = None,
        max_executors: typing.Optional[jsii.Number] = None,
        min_executors: typing.Optional[jsii.Number] = None,
        node_count: typing.Optional[jsii.Number] = None,
        session_level_packages_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        spark_config: typing.Optional[typing.Union["SynapseSparkPoolSparkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_events_folder: typing.Optional[builtins.str] = None,
        spark_log_folder: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SynapseSparkPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool azurerm_synapse_spark_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#name SynapseSparkPool#name}.
        :param node_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#node_size SynapseSparkPool#node_size}.
        :param node_size_family: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#node_size_family SynapseSparkPool#node_size_family}.
        :param spark_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#spark_version SynapseSparkPool#spark_version}.
        :param synapse_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#synapse_workspace_id SynapseSparkPool#synapse_workspace_id}.
        :param auto_pause: auto_pause block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#auto_pause SynapseSparkPool#auto_pause}
        :param auto_scale: auto_scale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#auto_scale SynapseSparkPool#auto_scale}
        :param cache_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#cache_size SynapseSparkPool#cache_size}.
        :param compute_isolation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#compute_isolation_enabled SynapseSparkPool#compute_isolation_enabled}.
        :param dynamic_executor_allocation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#dynamic_executor_allocation_enabled SynapseSparkPool#dynamic_executor_allocation_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#id SynapseSparkPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param library_requirement: library_requirement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#library_requirement SynapseSparkPool#library_requirement}
        :param max_executors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#max_executors SynapseSparkPool#max_executors}.
        :param min_executors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#min_executors SynapseSparkPool#min_executors}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#node_count SynapseSparkPool#node_count}.
        :param session_level_packages_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#session_level_packages_enabled SynapseSparkPool#session_level_packages_enabled}.
        :param spark_config: spark_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#spark_config SynapseSparkPool#spark_config}
        :param spark_events_folder: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#spark_events_folder SynapseSparkPool#spark_events_folder}.
        :param spark_log_folder: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#spark_log_folder SynapseSparkPool#spark_log_folder}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#tags SynapseSparkPool#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#timeouts SynapseSparkPool#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1227a08cff553b751324b3978230f009ec97e84f3cab486e49367a6e1dd3cd0a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SynapseSparkPoolConfig(
            name=name,
            node_size=node_size,
            node_size_family=node_size_family,
            spark_version=spark_version,
            synapse_workspace_id=synapse_workspace_id,
            auto_pause=auto_pause,
            auto_scale=auto_scale,
            cache_size=cache_size,
            compute_isolation_enabled=compute_isolation_enabled,
            dynamic_executor_allocation_enabled=dynamic_executor_allocation_enabled,
            id=id,
            library_requirement=library_requirement,
            max_executors=max_executors,
            min_executors=min_executors,
            node_count=node_count,
            session_level_packages_enabled=session_level_packages_enabled,
            spark_config=spark_config,
            spark_events_folder=spark_events_folder,
            spark_log_folder=spark_log_folder,
            tags=tags,
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
        '''Generates CDKTF code for importing a SynapseSparkPool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SynapseSparkPool to import.
        :param import_from_id: The id of the existing SynapseSparkPool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SynapseSparkPool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87c5e6842fa3d1e7ebf3638b6304388d1bbe77323dc9c284bd11ce729c07c742)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoPause")
    def put_auto_pause(self, *, delay_in_minutes: jsii.Number) -> None:
        '''
        :param delay_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#delay_in_minutes SynapseSparkPool#delay_in_minutes}.
        '''
        value = SynapseSparkPoolAutoPause(delay_in_minutes=delay_in_minutes)

        return typing.cast(None, jsii.invoke(self, "putAutoPause", [value]))

    @jsii.member(jsii_name="putAutoScale")
    def put_auto_scale(
        self,
        *,
        max_node_count: jsii.Number,
        min_node_count: jsii.Number,
    ) -> None:
        '''
        :param max_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#max_node_count SynapseSparkPool#max_node_count}.
        :param min_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#min_node_count SynapseSparkPool#min_node_count}.
        '''
        value = SynapseSparkPoolAutoScale(
            max_node_count=max_node_count, min_node_count=min_node_count
        )

        return typing.cast(None, jsii.invoke(self, "putAutoScale", [value]))

    @jsii.member(jsii_name="putLibraryRequirement")
    def put_library_requirement(
        self,
        *,
        content: builtins.str,
        filename: builtins.str,
    ) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#content SynapseSparkPool#content}.
        :param filename: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#filename SynapseSparkPool#filename}.
        '''
        value = SynapseSparkPoolLibraryRequirement(content=content, filename=filename)

        return typing.cast(None, jsii.invoke(self, "putLibraryRequirement", [value]))

    @jsii.member(jsii_name="putSparkConfig")
    def put_spark_config(
        self,
        *,
        content: builtins.str,
        filename: builtins.str,
    ) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#content SynapseSparkPool#content}.
        :param filename: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#filename SynapseSparkPool#filename}.
        '''
        value = SynapseSparkPoolSparkConfig(content=content, filename=filename)

        return typing.cast(None, jsii.invoke(self, "putSparkConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#create SynapseSparkPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#delete SynapseSparkPool#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#read SynapseSparkPool#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#update SynapseSparkPool#update}.
        '''
        value = SynapseSparkPoolTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutoPause")
    def reset_auto_pause(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoPause", []))

    @jsii.member(jsii_name="resetAutoScale")
    def reset_auto_scale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoScale", []))

    @jsii.member(jsii_name="resetCacheSize")
    def reset_cache_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheSize", []))

    @jsii.member(jsii_name="resetComputeIsolationEnabled")
    def reset_compute_isolation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeIsolationEnabled", []))

    @jsii.member(jsii_name="resetDynamicExecutorAllocationEnabled")
    def reset_dynamic_executor_allocation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicExecutorAllocationEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLibraryRequirement")
    def reset_library_requirement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLibraryRequirement", []))

    @jsii.member(jsii_name="resetMaxExecutors")
    def reset_max_executors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxExecutors", []))

    @jsii.member(jsii_name="resetMinExecutors")
    def reset_min_executors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinExecutors", []))

    @jsii.member(jsii_name="resetNodeCount")
    def reset_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeCount", []))

    @jsii.member(jsii_name="resetSessionLevelPackagesEnabled")
    def reset_session_level_packages_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionLevelPackagesEnabled", []))

    @jsii.member(jsii_name="resetSparkConfig")
    def reset_spark_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkConfig", []))

    @jsii.member(jsii_name="resetSparkEventsFolder")
    def reset_spark_events_folder(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkEventsFolder", []))

    @jsii.member(jsii_name="resetSparkLogFolder")
    def reset_spark_log_folder(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkLogFolder", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="autoPause")
    def auto_pause(self) -> "SynapseSparkPoolAutoPauseOutputReference":
        return typing.cast("SynapseSparkPoolAutoPauseOutputReference", jsii.get(self, "autoPause"))

    @builtins.property
    @jsii.member(jsii_name="autoScale")
    def auto_scale(self) -> "SynapseSparkPoolAutoScaleOutputReference":
        return typing.cast("SynapseSparkPoolAutoScaleOutputReference", jsii.get(self, "autoScale"))

    @builtins.property
    @jsii.member(jsii_name="libraryRequirement")
    def library_requirement(
        self,
    ) -> "SynapseSparkPoolLibraryRequirementOutputReference":
        return typing.cast("SynapseSparkPoolLibraryRequirementOutputReference", jsii.get(self, "libraryRequirement"))

    @builtins.property
    @jsii.member(jsii_name="sparkConfig")
    def spark_config(self) -> "SynapseSparkPoolSparkConfigOutputReference":
        return typing.cast("SynapseSparkPoolSparkConfigOutputReference", jsii.get(self, "sparkConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SynapseSparkPoolTimeoutsOutputReference":
        return typing.cast("SynapseSparkPoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoPauseInput")
    def auto_pause_input(self) -> typing.Optional["SynapseSparkPoolAutoPause"]:
        return typing.cast(typing.Optional["SynapseSparkPoolAutoPause"], jsii.get(self, "autoPauseInput"))

    @builtins.property
    @jsii.member(jsii_name="autoScaleInput")
    def auto_scale_input(self) -> typing.Optional["SynapseSparkPoolAutoScale"]:
        return typing.cast(typing.Optional["SynapseSparkPoolAutoScale"], jsii.get(self, "autoScaleInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheSizeInput")
    def cache_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cacheSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="computeIsolationEnabledInput")
    def compute_isolation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "computeIsolationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicExecutorAllocationEnabledInput")
    def dynamic_executor_allocation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dynamicExecutorAllocationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="libraryRequirementInput")
    def library_requirement_input(
        self,
    ) -> typing.Optional["SynapseSparkPoolLibraryRequirement"]:
        return typing.cast(typing.Optional["SynapseSparkPoolLibraryRequirement"], jsii.get(self, "libraryRequirementInput"))

    @builtins.property
    @jsii.member(jsii_name="maxExecutorsInput")
    def max_executors_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxExecutorsInput"))

    @builtins.property
    @jsii.member(jsii_name="minExecutorsInput")
    def min_executors_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minExecutorsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeSizeFamilyInput")
    def node_size_family_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeSizeFamilyInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeSizeInput")
    def node_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionLevelPackagesEnabledInput")
    def session_level_packages_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sessionLevelPackagesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkConfigInput")
    def spark_config_input(self) -> typing.Optional["SynapseSparkPoolSparkConfig"]:
        return typing.cast(typing.Optional["SynapseSparkPoolSparkConfig"], jsii.get(self, "sparkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkEventsFolderInput")
    def spark_events_folder_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sparkEventsFolderInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkLogFolderInput")
    def spark_log_folder_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sparkLogFolderInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkVersionInput")
    def spark_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sparkVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="synapseWorkspaceIdInput")
    def synapse_workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "synapseWorkspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SynapseSparkPoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SynapseSparkPoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheSize")
    def cache_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cacheSize"))

    @cache_size.setter
    def cache_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9197912162c9e6a70a52a87ca5a7863210cb18aa905990258d672541911b6a20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="computeIsolationEnabled")
    def compute_isolation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "computeIsolationEnabled"))

    @compute_isolation_enabled.setter
    def compute_isolation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df41d853be8bd8455e2e23afae427bcbfba99490e103de2f135e2b531639ee4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeIsolationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dynamicExecutorAllocationEnabled")
    def dynamic_executor_allocation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dynamicExecutorAllocationEnabled"))

    @dynamic_executor_allocation_enabled.setter
    def dynamic_executor_allocation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b912174576462985f7f3537e5645c55d3882dee642f6c75de172386be5a3cc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamicExecutorAllocationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66f73848132f67c49a48e07482e70c72696c966e2037fa5f39962a74904c22bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxExecutors")
    def max_executors(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxExecutors"))

    @max_executors.setter
    def max_executors(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b497f4694bce47935a0105e55be2c67a9f263b5f8e848ffe1fd1e31064b8cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxExecutors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minExecutors")
    def min_executors(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minExecutors"))

    @min_executors.setter
    def min_executors(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__549701e5588133ee6471917dd145aa6c9a07d65ceb615af641d631f2bc2c07d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minExecutors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca2904d95afaea05b1c858132eb4b4d6f434de35e21f60264e75625906d5421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b761ec2a2b8ed7af530f096edafa498f1d5cd82ad69328dadc936c3375922832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeSize")
    def node_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeSize"))

    @node_size.setter
    def node_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f89871745034df3ea993cdb5063952acf53de2b2030ec9a5e1bfb1c8e1147e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeSizeFamily")
    def node_size_family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeSizeFamily"))

    @node_size_family.setter
    def node_size_family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3176c9ac65dce9257e360d773a09c64b445e3113e459e12adbd421fedbc94a41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeSizeFamily", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionLevelPackagesEnabled")
    def session_level_packages_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sessionLevelPackagesEnabled"))

    @session_level_packages_enabled.setter
    def session_level_packages_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2e92b635f51d647c54eded355e92dc103a789a1530054c27b127cbaa9e476d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionLevelPackagesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sparkEventsFolder")
    def spark_events_folder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sparkEventsFolder"))

    @spark_events_folder.setter
    def spark_events_folder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44e396f0fc6979bf9dda0fba7ce8118752bb280fc635ce5c94a9fab7dc0f03f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkEventsFolder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sparkLogFolder")
    def spark_log_folder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sparkLogFolder"))

    @spark_log_folder.setter
    def spark_log_folder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c09f5b3a84804d987a78fd924dcef657cae0dfe213d596e70d673e57bf3ec04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkLogFolder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sparkVersion")
    def spark_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sparkVersion"))

    @spark_version.setter
    def spark_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e59d1d96f7ecba5d7015114cca5794f2b34c3453460a09b8a9c36e9fb5bb64f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="synapseWorkspaceId")
    def synapse_workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "synapseWorkspaceId"))

    @synapse_workspace_id.setter
    def synapse_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848e7746a016ec33cb1ef99b7cc8cb0d97fc96bfd5a158f60bea492db911a76a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "synapseWorkspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9bf1a0267701394035ad2b9aafc85c175f85f74d4b55e856b205807cebde400)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.synapseSparkPool.SynapseSparkPoolAutoPause",
    jsii_struct_bases=[],
    name_mapping={"delay_in_minutes": "delayInMinutes"},
)
class SynapseSparkPoolAutoPause:
    def __init__(self, *, delay_in_minutes: jsii.Number) -> None:
        '''
        :param delay_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#delay_in_minutes SynapseSparkPool#delay_in_minutes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e861775b439feac0f0523ee128785368dff16fc96f2bf50129a195baa13e30d)
            check_type(argname="argument delay_in_minutes", value=delay_in_minutes, expected_type=type_hints["delay_in_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delay_in_minutes": delay_in_minutes,
        }

    @builtins.property
    def delay_in_minutes(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#delay_in_minutes SynapseSparkPool#delay_in_minutes}.'''
        result = self._values.get("delay_in_minutes")
        assert result is not None, "Required property 'delay_in_minutes' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynapseSparkPoolAutoPause(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SynapseSparkPoolAutoPauseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.synapseSparkPool.SynapseSparkPoolAutoPauseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d95188735de18d95d25febc98cc40b893c6532246a29510b665139ece077581)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="delayInMinutesInput")
    def delay_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "delayInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="delayInMinutes")
    def delay_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "delayInMinutes"))

    @delay_in_minutes.setter
    def delay_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93c79e4fb1d0c177f161b9db2e10ad270aa9ecb10833393f9a167fb097b77c2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delayInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SynapseSparkPoolAutoPause]:
        return typing.cast(typing.Optional[SynapseSparkPoolAutoPause], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SynapseSparkPoolAutoPause]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff57b3e2ff46978d2a720ddb10a6d3abd5f19c6769f3d8c29555ecd468f9344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.synapseSparkPool.SynapseSparkPoolAutoScale",
    jsii_struct_bases=[],
    name_mapping={"max_node_count": "maxNodeCount", "min_node_count": "minNodeCount"},
)
class SynapseSparkPoolAutoScale:
    def __init__(
        self,
        *,
        max_node_count: jsii.Number,
        min_node_count: jsii.Number,
    ) -> None:
        '''
        :param max_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#max_node_count SynapseSparkPool#max_node_count}.
        :param min_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#min_node_count SynapseSparkPool#min_node_count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f83672a354790410b42514323acdeca4f1b25e3e4beeb1046c325db9bfd58f95)
            check_type(argname="argument max_node_count", value=max_node_count, expected_type=type_hints["max_node_count"])
            check_type(argname="argument min_node_count", value=min_node_count, expected_type=type_hints["min_node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_node_count": max_node_count,
            "min_node_count": min_node_count,
        }

    @builtins.property
    def max_node_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#max_node_count SynapseSparkPool#max_node_count}.'''
        result = self._values.get("max_node_count")
        assert result is not None, "Required property 'max_node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_node_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#min_node_count SynapseSparkPool#min_node_count}.'''
        result = self._values.get("min_node_count")
        assert result is not None, "Required property 'min_node_count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynapseSparkPoolAutoScale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SynapseSparkPoolAutoScaleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.synapseSparkPool.SynapseSparkPoolAutoScaleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c715872574dc2a6ede8ae7abdf90cdaac183ce983230a52a12d4d93dca4c7747)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maxNodeCountInput")
    def max_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minNodeCountInput")
    def min_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNodeCount")
    def max_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNodeCount"))

    @max_node_count.setter
    def max_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__603aafa760d5a2fa2a8ec97bd9d0a1fdc4ff4bfbc94eff4cd2dd5b9b6ee78f17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCount")
    def min_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCount"))

    @min_node_count.setter
    def min_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787e568b131002bc07402a4d20b044ad4c87660903a6b3a913324e32e72a97f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SynapseSparkPoolAutoScale]:
        return typing.cast(typing.Optional[SynapseSparkPoolAutoScale], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SynapseSparkPoolAutoScale]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf42a6fda06be808d6c2574cada66567451e9f541533fadf3fa1963a0534b1b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.synapseSparkPool.SynapseSparkPoolConfig",
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
        "node_size": "nodeSize",
        "node_size_family": "nodeSizeFamily",
        "spark_version": "sparkVersion",
        "synapse_workspace_id": "synapseWorkspaceId",
        "auto_pause": "autoPause",
        "auto_scale": "autoScale",
        "cache_size": "cacheSize",
        "compute_isolation_enabled": "computeIsolationEnabled",
        "dynamic_executor_allocation_enabled": "dynamicExecutorAllocationEnabled",
        "id": "id",
        "library_requirement": "libraryRequirement",
        "max_executors": "maxExecutors",
        "min_executors": "minExecutors",
        "node_count": "nodeCount",
        "session_level_packages_enabled": "sessionLevelPackagesEnabled",
        "spark_config": "sparkConfig",
        "spark_events_folder": "sparkEventsFolder",
        "spark_log_folder": "sparkLogFolder",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class SynapseSparkPoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        node_size: builtins.str,
        node_size_family: builtins.str,
        spark_version: builtins.str,
        synapse_workspace_id: builtins.str,
        auto_pause: typing.Optional[typing.Union[SynapseSparkPoolAutoPause, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_scale: typing.Optional[typing.Union[SynapseSparkPoolAutoScale, typing.Dict[builtins.str, typing.Any]]] = None,
        cache_size: typing.Optional[jsii.Number] = None,
        compute_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dynamic_executor_allocation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        library_requirement: typing.Optional[typing.Union["SynapseSparkPoolLibraryRequirement", typing.Dict[builtins.str, typing.Any]]] = None,
        max_executors: typing.Optional[jsii.Number] = None,
        min_executors: typing.Optional[jsii.Number] = None,
        node_count: typing.Optional[jsii.Number] = None,
        session_level_packages_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        spark_config: typing.Optional[typing.Union["SynapseSparkPoolSparkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_events_folder: typing.Optional[builtins.str] = None,
        spark_log_folder: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SynapseSparkPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#name SynapseSparkPool#name}.
        :param node_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#node_size SynapseSparkPool#node_size}.
        :param node_size_family: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#node_size_family SynapseSparkPool#node_size_family}.
        :param spark_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#spark_version SynapseSparkPool#spark_version}.
        :param synapse_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#synapse_workspace_id SynapseSparkPool#synapse_workspace_id}.
        :param auto_pause: auto_pause block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#auto_pause SynapseSparkPool#auto_pause}
        :param auto_scale: auto_scale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#auto_scale SynapseSparkPool#auto_scale}
        :param cache_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#cache_size SynapseSparkPool#cache_size}.
        :param compute_isolation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#compute_isolation_enabled SynapseSparkPool#compute_isolation_enabled}.
        :param dynamic_executor_allocation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#dynamic_executor_allocation_enabled SynapseSparkPool#dynamic_executor_allocation_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#id SynapseSparkPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param library_requirement: library_requirement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#library_requirement SynapseSparkPool#library_requirement}
        :param max_executors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#max_executors SynapseSparkPool#max_executors}.
        :param min_executors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#min_executors SynapseSparkPool#min_executors}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#node_count SynapseSparkPool#node_count}.
        :param session_level_packages_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#session_level_packages_enabled SynapseSparkPool#session_level_packages_enabled}.
        :param spark_config: spark_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#spark_config SynapseSparkPool#spark_config}
        :param spark_events_folder: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#spark_events_folder SynapseSparkPool#spark_events_folder}.
        :param spark_log_folder: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#spark_log_folder SynapseSparkPool#spark_log_folder}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#tags SynapseSparkPool#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#timeouts SynapseSparkPool#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(auto_pause, dict):
            auto_pause = SynapseSparkPoolAutoPause(**auto_pause)
        if isinstance(auto_scale, dict):
            auto_scale = SynapseSparkPoolAutoScale(**auto_scale)
        if isinstance(library_requirement, dict):
            library_requirement = SynapseSparkPoolLibraryRequirement(**library_requirement)
        if isinstance(spark_config, dict):
            spark_config = SynapseSparkPoolSparkConfig(**spark_config)
        if isinstance(timeouts, dict):
            timeouts = SynapseSparkPoolTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c4d6b40a0dfb1f972783684b15fc85891f940ed76d00f3095feb6eaeb8d8ba)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_size", value=node_size, expected_type=type_hints["node_size"])
            check_type(argname="argument node_size_family", value=node_size_family, expected_type=type_hints["node_size_family"])
            check_type(argname="argument spark_version", value=spark_version, expected_type=type_hints["spark_version"])
            check_type(argname="argument synapse_workspace_id", value=synapse_workspace_id, expected_type=type_hints["synapse_workspace_id"])
            check_type(argname="argument auto_pause", value=auto_pause, expected_type=type_hints["auto_pause"])
            check_type(argname="argument auto_scale", value=auto_scale, expected_type=type_hints["auto_scale"])
            check_type(argname="argument cache_size", value=cache_size, expected_type=type_hints["cache_size"])
            check_type(argname="argument compute_isolation_enabled", value=compute_isolation_enabled, expected_type=type_hints["compute_isolation_enabled"])
            check_type(argname="argument dynamic_executor_allocation_enabled", value=dynamic_executor_allocation_enabled, expected_type=type_hints["dynamic_executor_allocation_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument library_requirement", value=library_requirement, expected_type=type_hints["library_requirement"])
            check_type(argname="argument max_executors", value=max_executors, expected_type=type_hints["max_executors"])
            check_type(argname="argument min_executors", value=min_executors, expected_type=type_hints["min_executors"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
            check_type(argname="argument session_level_packages_enabled", value=session_level_packages_enabled, expected_type=type_hints["session_level_packages_enabled"])
            check_type(argname="argument spark_config", value=spark_config, expected_type=type_hints["spark_config"])
            check_type(argname="argument spark_events_folder", value=spark_events_folder, expected_type=type_hints["spark_events_folder"])
            check_type(argname="argument spark_log_folder", value=spark_log_folder, expected_type=type_hints["spark_log_folder"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "node_size": node_size,
            "node_size_family": node_size_family,
            "spark_version": spark_version,
            "synapse_workspace_id": synapse_workspace_id,
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
        if auto_pause is not None:
            self._values["auto_pause"] = auto_pause
        if auto_scale is not None:
            self._values["auto_scale"] = auto_scale
        if cache_size is not None:
            self._values["cache_size"] = cache_size
        if compute_isolation_enabled is not None:
            self._values["compute_isolation_enabled"] = compute_isolation_enabled
        if dynamic_executor_allocation_enabled is not None:
            self._values["dynamic_executor_allocation_enabled"] = dynamic_executor_allocation_enabled
        if id is not None:
            self._values["id"] = id
        if library_requirement is not None:
            self._values["library_requirement"] = library_requirement
        if max_executors is not None:
            self._values["max_executors"] = max_executors
        if min_executors is not None:
            self._values["min_executors"] = min_executors
        if node_count is not None:
            self._values["node_count"] = node_count
        if session_level_packages_enabled is not None:
            self._values["session_level_packages_enabled"] = session_level_packages_enabled
        if spark_config is not None:
            self._values["spark_config"] = spark_config
        if spark_events_folder is not None:
            self._values["spark_events_folder"] = spark_events_folder
        if spark_log_folder is not None:
            self._values["spark_log_folder"] = spark_log_folder
        if tags is not None:
            self._values["tags"] = tags
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#name SynapseSparkPool#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#node_size SynapseSparkPool#node_size}.'''
        result = self._values.get("node_size")
        assert result is not None, "Required property 'node_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_size_family(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#node_size_family SynapseSparkPool#node_size_family}.'''
        result = self._values.get("node_size_family")
        assert result is not None, "Required property 'node_size_family' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spark_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#spark_version SynapseSparkPool#spark_version}.'''
        result = self._values.get("spark_version")
        assert result is not None, "Required property 'spark_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def synapse_workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#synapse_workspace_id SynapseSparkPool#synapse_workspace_id}.'''
        result = self._values.get("synapse_workspace_id")
        assert result is not None, "Required property 'synapse_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_pause(self) -> typing.Optional[SynapseSparkPoolAutoPause]:
        '''auto_pause block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#auto_pause SynapseSparkPool#auto_pause}
        '''
        result = self._values.get("auto_pause")
        return typing.cast(typing.Optional[SynapseSparkPoolAutoPause], result)

    @builtins.property
    def auto_scale(self) -> typing.Optional[SynapseSparkPoolAutoScale]:
        '''auto_scale block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#auto_scale SynapseSparkPool#auto_scale}
        '''
        result = self._values.get("auto_scale")
        return typing.cast(typing.Optional[SynapseSparkPoolAutoScale], result)

    @builtins.property
    def cache_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#cache_size SynapseSparkPool#cache_size}.'''
        result = self._values.get("cache_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def compute_isolation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#compute_isolation_enabled SynapseSparkPool#compute_isolation_enabled}.'''
        result = self._values.get("compute_isolation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dynamic_executor_allocation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#dynamic_executor_allocation_enabled SynapseSparkPool#dynamic_executor_allocation_enabled}.'''
        result = self._values.get("dynamic_executor_allocation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#id SynapseSparkPool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def library_requirement(
        self,
    ) -> typing.Optional["SynapseSparkPoolLibraryRequirement"]:
        '''library_requirement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#library_requirement SynapseSparkPool#library_requirement}
        '''
        result = self._values.get("library_requirement")
        return typing.cast(typing.Optional["SynapseSparkPoolLibraryRequirement"], result)

    @builtins.property
    def max_executors(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#max_executors SynapseSparkPool#max_executors}.'''
        result = self._values.get("max_executors")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_executors(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#min_executors SynapseSparkPool#min_executors}.'''
        result = self._values.get("min_executors")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#node_count SynapseSparkPool#node_count}.'''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def session_level_packages_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#session_level_packages_enabled SynapseSparkPool#session_level_packages_enabled}.'''
        result = self._values.get("session_level_packages_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def spark_config(self) -> typing.Optional["SynapseSparkPoolSparkConfig"]:
        '''spark_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#spark_config SynapseSparkPool#spark_config}
        '''
        result = self._values.get("spark_config")
        return typing.cast(typing.Optional["SynapseSparkPoolSparkConfig"], result)

    @builtins.property
    def spark_events_folder(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#spark_events_folder SynapseSparkPool#spark_events_folder}.'''
        result = self._values.get("spark_events_folder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark_log_folder(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#spark_log_folder SynapseSparkPool#spark_log_folder}.'''
        result = self._values.get("spark_log_folder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#tags SynapseSparkPool#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SynapseSparkPoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#timeouts SynapseSparkPool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SynapseSparkPoolTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynapseSparkPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.synapseSparkPool.SynapseSparkPoolLibraryRequirement",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "filename": "filename"},
)
class SynapseSparkPoolLibraryRequirement:
    def __init__(self, *, content: builtins.str, filename: builtins.str) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#content SynapseSparkPool#content}.
        :param filename: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#filename SynapseSparkPool#filename}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b470988f3ff7327793274387af17e56026de04fd9660ca50ad74c9d168627fcc)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "filename": filename,
        }

    @builtins.property
    def content(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#content SynapseSparkPool#content}.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filename(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#filename SynapseSparkPool#filename}.'''
        result = self._values.get("filename")
        assert result is not None, "Required property 'filename' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynapseSparkPoolLibraryRequirement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SynapseSparkPoolLibraryRequirementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.synapseSparkPool.SynapseSparkPoolLibraryRequirementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13403e44b8120f2737a11e0aca2fa9ab69715f208cd9c1c6715e7fa90ebe3af1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="filenameInput")
    def filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae07c6b1ccdaf89a25c88cfd5f927bc87d6ad348cfc4d6f46599dd5a223ed2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a24837c23d025b70393e01738fceea07080668253ab4a667545ff1bbda19960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filename", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SynapseSparkPoolLibraryRequirement]:
        return typing.cast(typing.Optional[SynapseSparkPoolLibraryRequirement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SynapseSparkPoolLibraryRequirement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79dd04991f622fac12012ef891b34beb54a9c5b270b6465338b0616ba5239f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.synapseSparkPool.SynapseSparkPoolSparkConfig",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "filename": "filename"},
)
class SynapseSparkPoolSparkConfig:
    def __init__(self, *, content: builtins.str, filename: builtins.str) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#content SynapseSparkPool#content}.
        :param filename: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#filename SynapseSparkPool#filename}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__038de899133a0d8f4737a12bb0a43527b48582b83dd0b468e1a0804253424a67)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "filename": filename,
        }

    @builtins.property
    def content(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#content SynapseSparkPool#content}.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filename(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#filename SynapseSparkPool#filename}.'''
        result = self._values.get("filename")
        assert result is not None, "Required property 'filename' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynapseSparkPoolSparkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SynapseSparkPoolSparkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.synapseSparkPool.SynapseSparkPoolSparkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd9817500c0deb4f9c356361a5430fedfaa383ad91c289c517a2aa6daad337c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="filenameInput")
    def filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb657a11f6a72a8bf513b5ce343164aab0f790f0618a72f7682ed87c415c9d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__687870655c74d84268cdeab8d45adb871c730b826e7a23060af1feb385de5bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filename", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SynapseSparkPoolSparkConfig]:
        return typing.cast(typing.Optional[SynapseSparkPoolSparkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SynapseSparkPoolSparkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86e4242c53c2df4c239490fb951ae6973340a74c5035e28721c2224086533b87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.synapseSparkPool.SynapseSparkPoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SynapseSparkPoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#create SynapseSparkPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#delete SynapseSparkPool#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#read SynapseSparkPool#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#update SynapseSparkPool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df84e393c4659a96e5d0b474595c69b8cd3c8ae6934aac4b076f79b424b32a4)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#create SynapseSparkPool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#delete SynapseSparkPool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#read SynapseSparkPool#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_spark_pool#update SynapseSparkPool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynapseSparkPoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SynapseSparkPoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.synapseSparkPool.SynapseSparkPoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8acf007ade095cc00321bff5076da4e04bddc62d13b005148e2e2c4a92588b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9da56b6e0f98867b6524b6f41ec2b512ba966fab43be6d7a4bc3f1a45ddc4861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17f33ba9209969cf288426d551dbe4e46a6ba0fde1889c29d67e10ff963f97ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eddaceb0a5f62457bf1f96d32f198516d9b274fafe40fcca6bd693b22369c4b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba58b099f0d0d6cbb0f983d225d0ccc8dd98f817848ddeca529abf7619d2ac1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynapseSparkPoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynapseSparkPoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynapseSparkPoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0b4e07dc997201b6c94e022f1dfb01be110c1e6e6f7b07d78df649cf4b8aeba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SynapseSparkPool",
    "SynapseSparkPoolAutoPause",
    "SynapseSparkPoolAutoPauseOutputReference",
    "SynapseSparkPoolAutoScale",
    "SynapseSparkPoolAutoScaleOutputReference",
    "SynapseSparkPoolConfig",
    "SynapseSparkPoolLibraryRequirement",
    "SynapseSparkPoolLibraryRequirementOutputReference",
    "SynapseSparkPoolSparkConfig",
    "SynapseSparkPoolSparkConfigOutputReference",
    "SynapseSparkPoolTimeouts",
    "SynapseSparkPoolTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__1227a08cff553b751324b3978230f009ec97e84f3cab486e49367a6e1dd3cd0a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    node_size: builtins.str,
    node_size_family: builtins.str,
    spark_version: builtins.str,
    synapse_workspace_id: builtins.str,
    auto_pause: typing.Optional[typing.Union[SynapseSparkPoolAutoPause, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_scale: typing.Optional[typing.Union[SynapseSparkPoolAutoScale, typing.Dict[builtins.str, typing.Any]]] = None,
    cache_size: typing.Optional[jsii.Number] = None,
    compute_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dynamic_executor_allocation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    library_requirement: typing.Optional[typing.Union[SynapseSparkPoolLibraryRequirement, typing.Dict[builtins.str, typing.Any]]] = None,
    max_executors: typing.Optional[jsii.Number] = None,
    min_executors: typing.Optional[jsii.Number] = None,
    node_count: typing.Optional[jsii.Number] = None,
    session_level_packages_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    spark_config: typing.Optional[typing.Union[SynapseSparkPoolSparkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_events_folder: typing.Optional[builtins.str] = None,
    spark_log_folder: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SynapseSparkPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__87c5e6842fa3d1e7ebf3638b6304388d1bbe77323dc9c284bd11ce729c07c742(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9197912162c9e6a70a52a87ca5a7863210cb18aa905990258d672541911b6a20(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df41d853be8bd8455e2e23afae427bcbfba99490e103de2f135e2b531639ee4e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b912174576462985f7f3537e5645c55d3882dee642f6c75de172386be5a3cc0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66f73848132f67c49a48e07482e70c72696c966e2037fa5f39962a74904c22bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b497f4694bce47935a0105e55be2c67a9f263b5f8e848ffe1fd1e31064b8cf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__549701e5588133ee6471917dd145aa6c9a07d65ceb615af641d631f2bc2c07d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca2904d95afaea05b1c858132eb4b4d6f434de35e21f60264e75625906d5421(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b761ec2a2b8ed7af530f096edafa498f1d5cd82ad69328dadc936c3375922832(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f89871745034df3ea993cdb5063952acf53de2b2030ec9a5e1bfb1c8e1147e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3176c9ac65dce9257e360d773a09c64b445e3113e459e12adbd421fedbc94a41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2e92b635f51d647c54eded355e92dc103a789a1530054c27b127cbaa9e476d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e396f0fc6979bf9dda0fba7ce8118752bb280fc635ce5c94a9fab7dc0f03f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c09f5b3a84804d987a78fd924dcef657cae0dfe213d596e70d673e57bf3ec04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e59d1d96f7ecba5d7015114cca5794f2b34c3453460a09b8a9c36e9fb5bb64f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848e7746a016ec33cb1ef99b7cc8cb0d97fc96bfd5a158f60bea492db911a76a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9bf1a0267701394035ad2b9aafc85c175f85f74d4b55e856b205807cebde400(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e861775b439feac0f0523ee128785368dff16fc96f2bf50129a195baa13e30d(
    *,
    delay_in_minutes: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d95188735de18d95d25febc98cc40b893c6532246a29510b665139ece077581(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c79e4fb1d0c177f161b9db2e10ad270aa9ecb10833393f9a167fb097b77c2b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff57b3e2ff46978d2a720ddb10a6d3abd5f19c6769f3d8c29555ecd468f9344(
    value: typing.Optional[SynapseSparkPoolAutoPause],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83672a354790410b42514323acdeca4f1b25e3e4beeb1046c325db9bfd58f95(
    *,
    max_node_count: jsii.Number,
    min_node_count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c715872574dc2a6ede8ae7abdf90cdaac183ce983230a52a12d4d93dca4c7747(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603aafa760d5a2fa2a8ec97bd9d0a1fdc4ff4bfbc94eff4cd2dd5b9b6ee78f17(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787e568b131002bc07402a4d20b044ad4c87660903a6b3a913324e32e72a97f9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf42a6fda06be808d6c2574cada66567451e9f541533fadf3fa1963a0534b1b9(
    value: typing.Optional[SynapseSparkPoolAutoScale],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c4d6b40a0dfb1f972783684b15fc85891f940ed76d00f3095feb6eaeb8d8ba(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    node_size: builtins.str,
    node_size_family: builtins.str,
    spark_version: builtins.str,
    synapse_workspace_id: builtins.str,
    auto_pause: typing.Optional[typing.Union[SynapseSparkPoolAutoPause, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_scale: typing.Optional[typing.Union[SynapseSparkPoolAutoScale, typing.Dict[builtins.str, typing.Any]]] = None,
    cache_size: typing.Optional[jsii.Number] = None,
    compute_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dynamic_executor_allocation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    library_requirement: typing.Optional[typing.Union[SynapseSparkPoolLibraryRequirement, typing.Dict[builtins.str, typing.Any]]] = None,
    max_executors: typing.Optional[jsii.Number] = None,
    min_executors: typing.Optional[jsii.Number] = None,
    node_count: typing.Optional[jsii.Number] = None,
    session_level_packages_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    spark_config: typing.Optional[typing.Union[SynapseSparkPoolSparkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_events_folder: typing.Optional[builtins.str] = None,
    spark_log_folder: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SynapseSparkPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b470988f3ff7327793274387af17e56026de04fd9660ca50ad74c9d168627fcc(
    *,
    content: builtins.str,
    filename: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13403e44b8120f2737a11e0aca2fa9ab69715f208cd9c1c6715e7fa90ebe3af1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae07c6b1ccdaf89a25c88cfd5f927bc87d6ad348cfc4d6f46599dd5a223ed2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a24837c23d025b70393e01738fceea07080668253ab4a667545ff1bbda19960(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79dd04991f622fac12012ef891b34beb54a9c5b270b6465338b0616ba5239f13(
    value: typing.Optional[SynapseSparkPoolLibraryRequirement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__038de899133a0d8f4737a12bb0a43527b48582b83dd0b468e1a0804253424a67(
    *,
    content: builtins.str,
    filename: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9817500c0deb4f9c356361a5430fedfaa383ad91c289c517a2aa6daad337c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb657a11f6a72a8bf513b5ce343164aab0f790f0618a72f7682ed87c415c9d07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687870655c74d84268cdeab8d45adb871c730b826e7a23060af1feb385de5bcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86e4242c53c2df4c239490fb951ae6973340a74c5035e28721c2224086533b87(
    value: typing.Optional[SynapseSparkPoolSparkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df84e393c4659a96e5d0b474595c69b8cd3c8ae6934aac4b076f79b424b32a4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8acf007ade095cc00321bff5076da4e04bddc62d13b005148e2e2c4a92588b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da56b6e0f98867b6524b6f41ec2b512ba966fab43be6d7a4bc3f1a45ddc4861(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f33ba9209969cf288426d551dbe4e46a6ba0fde1889c29d67e10ff963f97ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eddaceb0a5f62457bf1f96d32f198516d9b274fafe40fcca6bd693b22369c4b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba58b099f0d0d6cbb0f983d225d0ccc8dd98f817848ddeca529abf7619d2ac1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b4e07dc997201b6c94e022f1dfb01be110c1e6e6f7b07d78df649cf4b8aeba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynapseSparkPoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `google_spanner_instance`

Refer to the Terraform Registry for docs: [`google_spanner_instance`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance).
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


class SpannerInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance google_spanner_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        config: builtins.str,
        display_name: builtins.str,
        autoscaling_config: typing.Optional[typing.Union["SpannerInstanceAutoscalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_backup_schedule_type: typing.Optional[builtins.str] = None,
        edition: typing.Optional[builtins.str] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        num_nodes: typing.Optional[jsii.Number] = None,
        processing_units: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SpannerInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance google_spanner_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param config: The name of the instance's configuration (similar but not quite the same as a region) which defines the geographic placement and replication of your databases in this instance. It determines where your data is stored. Values are typically of the form 'regional-europe-west1' , 'us-central' etc. In order to obtain a valid list please consult the `Configuration section of the docs <https://cloud.google.com/spanner/docs/instances>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#config SpannerInstance#config}
        :param display_name: The descriptive name for this instance as it appears in UIs. Must be unique per project and between 4 and 30 characters in length. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#display_name SpannerInstance#display_name}
        :param autoscaling_config: autoscaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#autoscaling_config SpannerInstance#autoscaling_config}
        :param default_backup_schedule_type: Controls the default backup behavior for new databases within the instance. Note that 'AUTOMATIC' is not permitted for free instances, as backups and backup schedules are not allowed for free instances. if unset or NONE, no default backup schedule will be created for new databases within the instance. Possible values: ["NONE", "AUTOMATIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#default_backup_schedule_type SpannerInstance#default_backup_schedule_type}
        :param edition: The edition selected for this instance. Different editions provide different capabilities at different price points. Possible values: ["EDITION_UNSPECIFIED", "STANDARD", "ENTERPRISE", "ENTERPRISE_PLUS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#edition SpannerInstance#edition}
        :param force_destroy: When deleting a spanner instance, this boolean option will delete all backups of this instance. This must be set to true if you created a backup manually in the console. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#force_destroy SpannerInstance#force_destroy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#id SpannerInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_type: The type of this instance. The type can be used to distinguish product variants, that can affect aspects like: usage restrictions, quotas and billing. Currently this is used to distinguish FREE_INSTANCE vs PROVISIONED instances. When configured as FREE_INSTANCE, the field 'edition' should not be configured. Possible values: ["PROVISIONED", "FREE_INSTANCE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#instance_type SpannerInstance#instance_type}
        :param labels: An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#labels SpannerInstance#labels}
        :param name: A unique identifier for the instance, which cannot be changed after the instance is created. The name must be between 6 and 30 characters in length. If not provided, a random string starting with 'tf-' will be selected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#name SpannerInstance#name}
        :param num_nodes: The number of nodes allocated to this instance. Exactly one of either num_nodes, processing_units or autoscaling_config must be present in terraform except when instance_type = FREE_INSTANCE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#num_nodes SpannerInstance#num_nodes}
        :param processing_units: The number of processing units allocated to this instance. Exactly one of either num_nodes, processing_units or autoscaling_config must be present in terraform except when instance_type = FREE_INSTANCE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#processing_units SpannerInstance#processing_units}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#project SpannerInstance#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#timeouts SpannerInstance#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380c5721ee80df673aad762c971eecd3881a6a5c9aa74e5c48bdf276e77ca26a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = SpannerInstanceConfig(
            config=config,
            display_name=display_name,
            autoscaling_config=autoscaling_config,
            default_backup_schedule_type=default_backup_schedule_type,
            edition=edition,
            force_destroy=force_destroy,
            id=id,
            instance_type=instance_type,
            labels=labels,
            name=name,
            num_nodes=num_nodes,
            processing_units=processing_units,
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

        jsii.create(self.__class__, self, [scope, id_, config_])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a SpannerInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SpannerInstance to import.
        :param import_from_id: The id of the existing SpannerInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SpannerInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75f292b6d38b380129aded8146ae88c9bc1adfe20bf51732269f62746144ae8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoscalingConfig")
    def put_autoscaling_config(
        self,
        *,
        asymmetric_autoscaling_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        autoscaling_limits: typing.Optional[typing.Union["SpannerInstanceAutoscalingConfigAutoscalingLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        autoscaling_targets: typing.Optional[typing.Union["SpannerInstanceAutoscalingConfigAutoscalingTargets", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param asymmetric_autoscaling_options: asymmetric_autoscaling_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#asymmetric_autoscaling_options SpannerInstance#asymmetric_autoscaling_options}
        :param autoscaling_limits: autoscaling_limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#autoscaling_limits SpannerInstance#autoscaling_limits}
        :param autoscaling_targets: autoscaling_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#autoscaling_targets SpannerInstance#autoscaling_targets}
        '''
        value = SpannerInstanceAutoscalingConfig(
            asymmetric_autoscaling_options=asymmetric_autoscaling_options,
            autoscaling_limits=autoscaling_limits,
            autoscaling_targets=autoscaling_targets,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscalingConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#create SpannerInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#delete SpannerInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#update SpannerInstance#update}.
        '''
        value = SpannerInstanceTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutoscalingConfig")
    def reset_autoscaling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingConfig", []))

    @jsii.member(jsii_name="resetDefaultBackupScheduleType")
    def reset_default_backup_schedule_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultBackupScheduleType", []))

    @jsii.member(jsii_name="resetEdition")
    def reset_edition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdition", []))

    @jsii.member(jsii_name="resetForceDestroy")
    def reset_force_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDestroy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNumNodes")
    def reset_num_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumNodes", []))

    @jsii.member(jsii_name="resetProcessingUnits")
    def reset_processing_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessingUnits", []))

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
    @jsii.member(jsii_name="autoscalingConfig")
    def autoscaling_config(self) -> "SpannerInstanceAutoscalingConfigOutputReference":
        return typing.cast("SpannerInstanceAutoscalingConfigOutputReference", jsii.get(self, "autoscalingConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

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
    def timeouts(self) -> "SpannerInstanceTimeoutsOutputReference":
        return typing.cast("SpannerInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingConfigInput")
    def autoscaling_config_input(
        self,
    ) -> typing.Optional["SpannerInstanceAutoscalingConfig"]:
        return typing.cast(typing.Optional["SpannerInstanceAutoscalingConfig"], jsii.get(self, "autoscalingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultBackupScheduleTypeInput")
    def default_backup_schedule_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultBackupScheduleTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="editionInput")
    def edition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "editionInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDestroyInput")
    def force_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="numNodesInput")
    def num_nodes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="processingUnitsInput")
    def processing_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "processingUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SpannerInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SpannerInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "config"))

    @config.setter
    def config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6797470e536d05ebb40fa2a7ad06ce8cabd6c7dead20bd3420ed0442721295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "config", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultBackupScheduleType")
    def default_backup_schedule_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBackupScheduleType"))

    @default_backup_schedule_type.setter
    def default_backup_schedule_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c778ab13459f16109ea75076e590eb39e804adc5f8d3881f80031b800e59261b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultBackupScheduleType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8927dd8d3a2ad2ca72dce60ddfb61c613556924dbe0c71021813f9e22572926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edition")
    def edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edition"))

    @edition.setter
    def edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93cfee99c4d826244133d76e500eefc22db694ad061d7d2484a802e2a85cf008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceDestroy")
    def force_destroy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceDestroy"))

    @force_destroy.setter
    def force_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e182fee054c81811d0643fe3bced1bbd1f9065a9fbacd4bfdf44f17e227e59fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b4faebfa62148102d96db738b9d276b40f9d27449d85e39dedd4d291392776)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13b65d5fc99be59a716b154a84293dc6495ce5df4321f7444e13f3e60c982208)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bbb004b28b48fa6c919c087c17cc521229343616f8decf9d867d4a330eb43e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b460b6875222dfa01ce15f0e263a05c1ec3405035a02647de2b9e5d822cab58b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numNodes")
    def num_nodes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numNodes"))

    @num_nodes.setter
    def num_nodes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__817f9c30943e43892ae5801356e7ab8c0ef477cc2c41885029593b97882584a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="processingUnits")
    def processing_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "processingUnits"))

    @processing_units.setter
    def processing_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d5c98b87400c78014ec4c184e03e5b4f5e2c7444c9921573193cae8fe615d17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "processingUnits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6262ed7a4c0cf6134e3e2a01ba2d47a52b859613045e3f6ff8a88a3f045564f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceAutoscalingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "asymmetric_autoscaling_options": "asymmetricAutoscalingOptions",
        "autoscaling_limits": "autoscalingLimits",
        "autoscaling_targets": "autoscalingTargets",
    },
)
class SpannerInstanceAutoscalingConfig:
    def __init__(
        self,
        *,
        asymmetric_autoscaling_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        autoscaling_limits: typing.Optional[typing.Union["SpannerInstanceAutoscalingConfigAutoscalingLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        autoscaling_targets: typing.Optional[typing.Union["SpannerInstanceAutoscalingConfigAutoscalingTargets", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param asymmetric_autoscaling_options: asymmetric_autoscaling_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#asymmetric_autoscaling_options SpannerInstance#asymmetric_autoscaling_options}
        :param autoscaling_limits: autoscaling_limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#autoscaling_limits SpannerInstance#autoscaling_limits}
        :param autoscaling_targets: autoscaling_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#autoscaling_targets SpannerInstance#autoscaling_targets}
        '''
        if isinstance(autoscaling_limits, dict):
            autoscaling_limits = SpannerInstanceAutoscalingConfigAutoscalingLimits(**autoscaling_limits)
        if isinstance(autoscaling_targets, dict):
            autoscaling_targets = SpannerInstanceAutoscalingConfigAutoscalingTargets(**autoscaling_targets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__369ef5e84fceb2829fe8e55a3d0936b043b7968165a2bdd2e97e9834155984d6)
            check_type(argname="argument asymmetric_autoscaling_options", value=asymmetric_autoscaling_options, expected_type=type_hints["asymmetric_autoscaling_options"])
            check_type(argname="argument autoscaling_limits", value=autoscaling_limits, expected_type=type_hints["autoscaling_limits"])
            check_type(argname="argument autoscaling_targets", value=autoscaling_targets, expected_type=type_hints["autoscaling_targets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if asymmetric_autoscaling_options is not None:
            self._values["asymmetric_autoscaling_options"] = asymmetric_autoscaling_options
        if autoscaling_limits is not None:
            self._values["autoscaling_limits"] = autoscaling_limits
        if autoscaling_targets is not None:
            self._values["autoscaling_targets"] = autoscaling_targets

    @builtins.property
    def asymmetric_autoscaling_options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions"]]]:
        '''asymmetric_autoscaling_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#asymmetric_autoscaling_options SpannerInstance#asymmetric_autoscaling_options}
        '''
        result = self._values.get("asymmetric_autoscaling_options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions"]]], result)

    @builtins.property
    def autoscaling_limits(
        self,
    ) -> typing.Optional["SpannerInstanceAutoscalingConfigAutoscalingLimits"]:
        '''autoscaling_limits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#autoscaling_limits SpannerInstance#autoscaling_limits}
        '''
        result = self._values.get("autoscaling_limits")
        return typing.cast(typing.Optional["SpannerInstanceAutoscalingConfigAutoscalingLimits"], result)

    @builtins.property
    def autoscaling_targets(
        self,
    ) -> typing.Optional["SpannerInstanceAutoscalingConfigAutoscalingTargets"]:
        '''autoscaling_targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#autoscaling_targets SpannerInstance#autoscaling_targets}
        '''
        result = self._values.get("autoscaling_targets")
        return typing.cast(typing.Optional["SpannerInstanceAutoscalingConfigAutoscalingTargets"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerInstanceAutoscalingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions",
    jsii_struct_bases=[],
    name_mapping={"overrides": "overrides", "replica_selection": "replicaSelection"},
)
class SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions:
    def __init__(
        self,
        *,
        overrides: typing.Union["SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverrides", typing.Dict[builtins.str, typing.Any]],
        replica_selection: typing.Union["SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelection", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param overrides: overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#overrides SpannerInstance#overrides}
        :param replica_selection: replica_selection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#replica_selection SpannerInstance#replica_selection}
        '''
        if isinstance(overrides, dict):
            overrides = SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverrides(**overrides)
        if isinstance(replica_selection, dict):
            replica_selection = SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelection(**replica_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24bf8ef539f0f4a2d1742d095a061040221ae561af4c486313860b049a9c04ff)
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument replica_selection", value=replica_selection, expected_type=type_hints["replica_selection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "overrides": overrides,
            "replica_selection": replica_selection,
        }

    @builtins.property
    def overrides(
        self,
    ) -> "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverrides":
        '''overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#overrides SpannerInstance#overrides}
        '''
        result = self._values.get("overrides")
        assert result is not None, "Required property 'overrides' is missing"
        return typing.cast("SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverrides", result)

    @builtins.property
    def replica_selection(
        self,
    ) -> "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelection":
        '''replica_selection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#replica_selection SpannerInstance#replica_selection}
        '''
        result = self._values.get("replica_selection")
        assert result is not None, "Required property 'replica_selection' is missing"
        return typing.cast("SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelection", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec35384e197983705cfe00426d476ab6f1b1576bdb95a8085b59f45f3e59db2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd0b720fcc854fe7c6bbee7cd8b4d632d0bbce73002888a43618d6bf41f3459e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e05c9e0897f9196ea687fbe57d9405d772778f332d364f183f3319e441dfee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb4f2f7418b18a8d9d2f75efa1454a24d22650532f523ed21cc864ac584f69bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8052446af8331ae14660f59c6bd47ddab26437ccf581f27c237217a25f8e561a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88bd6ee8ba9ef9c6a8232d4b8935910c48f31da263c2794a6b73da4d3034fcd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d54c8c045955328f23106cce5f62df82d1068bffb25dd054e7d3254d767f12da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putOverrides")
    def put_overrides(
        self,
        *,
        autoscaling_limits: typing.Union["SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimits", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param autoscaling_limits: autoscaling_limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#autoscaling_limits SpannerInstance#autoscaling_limits}
        '''
        value = SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverrides(
            autoscaling_limits=autoscaling_limits
        )

        return typing.cast(None, jsii.invoke(self, "putOverrides", [value]))

    @jsii.member(jsii_name="putReplicaSelection")
    def put_replica_selection(self, *, location: builtins.str) -> None:
        '''
        :param location: The location of the replica to apply asymmetric autoscaling options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#location SpannerInstance#location}
        '''
        value = SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelection(
            location=location
        )

        return typing.cast(None, jsii.invoke(self, "putReplicaSelection", [value]))

    @builtins.property
    @jsii.member(jsii_name="overrides")
    def overrides(
        self,
    ) -> "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesOutputReference":
        return typing.cast("SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesOutputReference", jsii.get(self, "overrides"))

    @builtins.property
    @jsii.member(jsii_name="replicaSelection")
    def replica_selection(
        self,
    ) -> "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelectionOutputReference":
        return typing.cast("SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelectionOutputReference", jsii.get(self, "replicaSelection"))

    @builtins.property
    @jsii.member(jsii_name="overridesInput")
    def overrides_input(
        self,
    ) -> typing.Optional["SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverrides"]:
        return typing.cast(typing.Optional["SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverrides"], jsii.get(self, "overridesInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaSelectionInput")
    def replica_selection_input(
        self,
    ) -> typing.Optional["SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelection"]:
        return typing.cast(typing.Optional["SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelection"], jsii.get(self, "replicaSelectionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03e3d9c726e6472354524c32c22ec8f205346fe4836180adb7549db3b644254d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverrides",
    jsii_struct_bases=[],
    name_mapping={"autoscaling_limits": "autoscalingLimits"},
)
class SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverrides:
    def __init__(
        self,
        *,
        autoscaling_limits: typing.Union["SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimits", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param autoscaling_limits: autoscaling_limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#autoscaling_limits SpannerInstance#autoscaling_limits}
        '''
        if isinstance(autoscaling_limits, dict):
            autoscaling_limits = SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimits(**autoscaling_limits)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a122ce0b62ea0749d4d2d5652af2e70b62afd06ad431fafddceb324637b163)
            check_type(argname="argument autoscaling_limits", value=autoscaling_limits, expected_type=type_hints["autoscaling_limits"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "autoscaling_limits": autoscaling_limits,
        }

    @builtins.property
    def autoscaling_limits(
        self,
    ) -> "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimits":
        '''autoscaling_limits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#autoscaling_limits SpannerInstance#autoscaling_limits}
        '''
        result = self._values.get("autoscaling_limits")
        assert result is not None, "Required property 'autoscaling_limits' is missing"
        return typing.cast("SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimits", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimits",
    jsii_struct_bases=[],
    name_mapping={"max_nodes": "maxNodes", "min_nodes": "minNodes"},
)
class SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimits:
    def __init__(self, *, max_nodes: jsii.Number, min_nodes: jsii.Number) -> None:
        '''
        :param max_nodes: The maximum number of nodes for this specific replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#max_nodes SpannerInstance#max_nodes}
        :param min_nodes: The minimum number of nodes for this specific replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#min_nodes SpannerInstance#min_nodes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2945ee64d5f4ca0cb254d9c90d8279c730f16f44a9d2449a17cdb18ad15da74b)
            check_type(argname="argument max_nodes", value=max_nodes, expected_type=type_hints["max_nodes"])
            check_type(argname="argument min_nodes", value=min_nodes, expected_type=type_hints["min_nodes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_nodes": max_nodes,
            "min_nodes": min_nodes,
        }

    @builtins.property
    def max_nodes(self) -> jsii.Number:
        '''The maximum number of nodes for this specific replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#max_nodes SpannerInstance#max_nodes}
        '''
        result = self._values.get("max_nodes")
        assert result is not None, "Required property 'max_nodes' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_nodes(self) -> jsii.Number:
        '''The minimum number of nodes for this specific replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#min_nodes SpannerInstance#min_nodes}
        '''
        result = self._values.get("min_nodes")
        assert result is not None, "Required property 'min_nodes' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd3ab30715322455c2233aca491cf5589e3ed95c51bda8dc97831a4acafe5c6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maxNodesInput")
    def max_nodes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="minNodesInput")
    def min_nodes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNodes")
    def max_nodes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNodes"))

    @max_nodes.setter
    def max_nodes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc8e2c98a6d6e5de31e01aa4921e41e4c74971e4cb1cde5dd61f76340ab0c6a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodes")
    def min_nodes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodes"))

    @min_nodes.setter
    def min_nodes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb6208fcfa990611cd3b8f248603a49b4a5fd7d179060ea5ef3add2e6fbed6cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimits]:
        return typing.cast(typing.Optional[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimits],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc53ce5a652fef610edca619ecf9e3eb55bdef367c0092ee01d80f46b1ab683c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfb835b226fcae1c39382616c838040f3d25f8edf4f9e799ddd110dbc0992b73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscalingLimits")
    def put_autoscaling_limits(
        self,
        *,
        max_nodes: jsii.Number,
        min_nodes: jsii.Number,
    ) -> None:
        '''
        :param max_nodes: The maximum number of nodes for this specific replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#max_nodes SpannerInstance#max_nodes}
        :param min_nodes: The minimum number of nodes for this specific replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#min_nodes SpannerInstance#min_nodes}
        '''
        value = SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimits(
            max_nodes=max_nodes, min_nodes=min_nodes
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscalingLimits", [value]))

    @builtins.property
    @jsii.member(jsii_name="autoscalingLimits")
    def autoscaling_limits(
        self,
    ) -> SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimitsOutputReference:
        return typing.cast(SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimitsOutputReference, jsii.get(self, "autoscalingLimits"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingLimitsInput")
    def autoscaling_limits_input(
        self,
    ) -> typing.Optional[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimits]:
        return typing.cast(typing.Optional[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimits], jsii.get(self, "autoscalingLimitsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverrides]:
        return typing.cast(typing.Optional[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverrides], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverrides],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e26d60ff76aeceb0264e545bd8ad293e27ff0f5c8793dd9b0359f3dd8a95e770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelection",
    jsii_struct_bases=[],
    name_mapping={"location": "location"},
)
class SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelection:
    def __init__(self, *, location: builtins.str) -> None:
        '''
        :param location: The location of the replica to apply asymmetric autoscaling options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#location SpannerInstance#location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f2dbcab548b6d1bf3bdcd87e69ba916ec38f6afcf8bb830be86dacd69283e28)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
        }

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the replica to apply asymmetric autoscaling options.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#location SpannerInstance#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62c2c40180e90458744488800888036536334a9ffa858ce50d18bfc30a44a68f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df5bdc7206c240798b76c8c343e05cf9fa35f5519bf1f90483dec3b7fc0f1d41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelection]:
        return typing.cast(typing.Optional[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cda949eb20a3bbc117692a994fff5336acabb760702d1278155f9ee5ade5d74d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceAutoscalingConfigAutoscalingLimits",
    jsii_struct_bases=[],
    name_mapping={
        "max_nodes": "maxNodes",
        "max_processing_units": "maxProcessingUnits",
        "min_nodes": "minNodes",
        "min_processing_units": "minProcessingUnits",
    },
)
class SpannerInstanceAutoscalingConfigAutoscalingLimits:
    def __init__(
        self,
        *,
        max_nodes: typing.Optional[jsii.Number] = None,
        max_processing_units: typing.Optional[jsii.Number] = None,
        min_nodes: typing.Optional[jsii.Number] = None,
        min_processing_units: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_nodes: Specifies maximum number of nodes allocated to the instance. If set, this number should be greater than or equal to min_nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#max_nodes SpannerInstance#max_nodes}
        :param max_processing_units: Specifies maximum number of processing units allocated to the instance. If set, this number should be multiples of 1000 and be greater than or equal to min_processing_units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#max_processing_units SpannerInstance#max_processing_units}
        :param min_nodes: Specifies number of nodes allocated to the instance. If set, this number should be greater than or equal to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#min_nodes SpannerInstance#min_nodes}
        :param min_processing_units: Specifies minimum number of processing units allocated to the instance. If set, this number should be multiples of 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#min_processing_units SpannerInstance#min_processing_units}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9553282bc74e82b2d4dcbe3c5f5afe1fbbb02ab39b6e334776f94e29753b1b7)
            check_type(argname="argument max_nodes", value=max_nodes, expected_type=type_hints["max_nodes"])
            check_type(argname="argument max_processing_units", value=max_processing_units, expected_type=type_hints["max_processing_units"])
            check_type(argname="argument min_nodes", value=min_nodes, expected_type=type_hints["min_nodes"])
            check_type(argname="argument min_processing_units", value=min_processing_units, expected_type=type_hints["min_processing_units"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_nodes is not None:
            self._values["max_nodes"] = max_nodes
        if max_processing_units is not None:
            self._values["max_processing_units"] = max_processing_units
        if min_nodes is not None:
            self._values["min_nodes"] = min_nodes
        if min_processing_units is not None:
            self._values["min_processing_units"] = min_processing_units

    @builtins.property
    def max_nodes(self) -> typing.Optional[jsii.Number]:
        '''Specifies maximum number of nodes allocated to the instance.

        If set, this number
        should be greater than or equal to min_nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#max_nodes SpannerInstance#max_nodes}
        '''
        result = self._values.get("max_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_processing_units(self) -> typing.Optional[jsii.Number]:
        '''Specifies maximum number of processing units allocated to the instance.

        If set, this number should be multiples of 1000 and be greater than or equal to
        min_processing_units.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#max_processing_units SpannerInstance#max_processing_units}
        '''
        result = self._values.get("max_processing_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_nodes(self) -> typing.Optional[jsii.Number]:
        '''Specifies number of nodes allocated to the instance. If set, this number should be greater than or equal to 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#min_nodes SpannerInstance#min_nodes}
        '''
        result = self._values.get("min_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_processing_units(self) -> typing.Optional[jsii.Number]:
        '''Specifies minimum number of processing units allocated to the instance. If set, this number should be multiples of 1000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#min_processing_units SpannerInstance#min_processing_units}
        '''
        result = self._values.get("min_processing_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerInstanceAutoscalingConfigAutoscalingLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpannerInstanceAutoscalingConfigAutoscalingLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceAutoscalingConfigAutoscalingLimitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b315ffb101ec14cd6685c0d86e9d50258b58d0c139a53254d0daae347ad74fd3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxNodes")
    def reset_max_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxNodes", []))

    @jsii.member(jsii_name="resetMaxProcessingUnits")
    def reset_max_processing_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxProcessingUnits", []))

    @jsii.member(jsii_name="resetMinNodes")
    def reset_min_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinNodes", []))

    @jsii.member(jsii_name="resetMinProcessingUnits")
    def reset_min_processing_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinProcessingUnits", []))

    @builtins.property
    @jsii.member(jsii_name="maxNodesInput")
    def max_nodes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxProcessingUnitsInput")
    def max_processing_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxProcessingUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="minNodesInput")
    def min_nodes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="minProcessingUnitsInput")
    def min_processing_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minProcessingUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNodes")
    def max_nodes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNodes"))

    @max_nodes.setter
    def max_nodes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6233fecc8120b24fe399e95c7e4915fae50a10bda00d1817b25ddaa314ce4a9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxProcessingUnits")
    def max_processing_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxProcessingUnits"))

    @max_processing_units.setter
    def max_processing_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deba06b5282f5906e68d734212f95896b7312e05eac64e16742545ec47b32304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxProcessingUnits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodes")
    def min_nodes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodes"))

    @min_nodes.setter
    def min_nodes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__959c20bc5402c21c7f492263b9527f3e7862fd8492c3a5b425a9bc48b838fada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minProcessingUnits")
    def min_processing_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minProcessingUnits"))

    @min_processing_units.setter
    def min_processing_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d967d119cffc0035598df4c89c2fc9e98defb0af2486089cbf595f620b39ede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minProcessingUnits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SpannerInstanceAutoscalingConfigAutoscalingLimits]:
        return typing.cast(typing.Optional[SpannerInstanceAutoscalingConfigAutoscalingLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpannerInstanceAutoscalingConfigAutoscalingLimits],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9a35ea023b9c7a32ffa90a274fc79df35fe39705e303597b42b0d18a7c4dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceAutoscalingConfigAutoscalingTargets",
    jsii_struct_bases=[],
    name_mapping={
        "high_priority_cpu_utilization_percent": "highPriorityCpuUtilizationPercent",
        "storage_utilization_percent": "storageUtilizationPercent",
    },
)
class SpannerInstanceAutoscalingConfigAutoscalingTargets:
    def __init__(
        self,
        *,
        high_priority_cpu_utilization_percent: typing.Optional[jsii.Number] = None,
        storage_utilization_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param high_priority_cpu_utilization_percent: Specifies the target high priority cpu utilization percentage that the autoscaler should be trying to achieve for the instance. This number is on a scale from 0 (no utilization) to 100 (full utilization).. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#high_priority_cpu_utilization_percent SpannerInstance#high_priority_cpu_utilization_percent}
        :param storage_utilization_percent: Specifies the target storage utilization percentage that the autoscaler should be trying to achieve for the instance. This number is on a scale from 0 (no utilization) to 100 (full utilization). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#storage_utilization_percent SpannerInstance#storage_utilization_percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef839a006be4982aae0221804dd84e81c139fda09578b9467182ed7a5cc47f9d)
            check_type(argname="argument high_priority_cpu_utilization_percent", value=high_priority_cpu_utilization_percent, expected_type=type_hints["high_priority_cpu_utilization_percent"])
            check_type(argname="argument storage_utilization_percent", value=storage_utilization_percent, expected_type=type_hints["storage_utilization_percent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if high_priority_cpu_utilization_percent is not None:
            self._values["high_priority_cpu_utilization_percent"] = high_priority_cpu_utilization_percent
        if storage_utilization_percent is not None:
            self._values["storage_utilization_percent"] = storage_utilization_percent

    @builtins.property
    def high_priority_cpu_utilization_percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies the target high priority cpu utilization percentage that the autoscaler should be trying to achieve for the instance.

        This number is on a scale from 0 (no utilization) to 100 (full utilization)..

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#high_priority_cpu_utilization_percent SpannerInstance#high_priority_cpu_utilization_percent}
        '''
        result = self._values.get("high_priority_cpu_utilization_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_utilization_percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies the target storage utilization percentage that the autoscaler should be trying to achieve for the instance.

        This number is on a scale from 0 (no utilization) to 100 (full utilization).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#storage_utilization_percent SpannerInstance#storage_utilization_percent}
        '''
        result = self._values.get("storage_utilization_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerInstanceAutoscalingConfigAutoscalingTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpannerInstanceAutoscalingConfigAutoscalingTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceAutoscalingConfigAutoscalingTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c17652c7e6a4fe6d755dec704d35d920abf684ff83efe8a034ba5a70f923e29b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHighPriorityCpuUtilizationPercent")
    def reset_high_priority_cpu_utilization_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHighPriorityCpuUtilizationPercent", []))

    @jsii.member(jsii_name="resetStorageUtilizationPercent")
    def reset_storage_utilization_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageUtilizationPercent", []))

    @builtins.property
    @jsii.member(jsii_name="highPriorityCpuUtilizationPercentInput")
    def high_priority_cpu_utilization_percent_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "highPriorityCpuUtilizationPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="storageUtilizationPercentInput")
    def storage_utilization_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageUtilizationPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="highPriorityCpuUtilizationPercent")
    def high_priority_cpu_utilization_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "highPriorityCpuUtilizationPercent"))

    @high_priority_cpu_utilization_percent.setter
    def high_priority_cpu_utilization_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__646ce11e43533cc4b35a614e683df8be044a17805e1348249d78aabba0e1f3a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "highPriorityCpuUtilizationPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageUtilizationPercent")
    def storage_utilization_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageUtilizationPercent"))

    @storage_utilization_percent.setter
    def storage_utilization_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9dd6c2f06849c53d09e4ed235e73712bdfa485b91b93984187ccd82d0f7c9c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageUtilizationPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SpannerInstanceAutoscalingConfigAutoscalingTargets]:
        return typing.cast(typing.Optional[SpannerInstanceAutoscalingConfigAutoscalingTargets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpannerInstanceAutoscalingConfigAutoscalingTargets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264491d906c348428d09a308e4e89c5467071978e378ae4469395d6654299b2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SpannerInstanceAutoscalingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceAutoscalingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34a5a20ceac108dd2aa37bd99479c6d78bd31279e26b6f48569affb743431f9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAsymmetricAutoscalingOptions")
    def put_asymmetric_autoscaling_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__972a4c74e3674066fec90f8c67651a594fd5b64ff2cf3fa89c0ae4116a2ab0ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAsymmetricAutoscalingOptions", [value]))

    @jsii.member(jsii_name="putAutoscalingLimits")
    def put_autoscaling_limits(
        self,
        *,
        max_nodes: typing.Optional[jsii.Number] = None,
        max_processing_units: typing.Optional[jsii.Number] = None,
        min_nodes: typing.Optional[jsii.Number] = None,
        min_processing_units: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_nodes: Specifies maximum number of nodes allocated to the instance. If set, this number should be greater than or equal to min_nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#max_nodes SpannerInstance#max_nodes}
        :param max_processing_units: Specifies maximum number of processing units allocated to the instance. If set, this number should be multiples of 1000 and be greater than or equal to min_processing_units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#max_processing_units SpannerInstance#max_processing_units}
        :param min_nodes: Specifies number of nodes allocated to the instance. If set, this number should be greater than or equal to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#min_nodes SpannerInstance#min_nodes}
        :param min_processing_units: Specifies minimum number of processing units allocated to the instance. If set, this number should be multiples of 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#min_processing_units SpannerInstance#min_processing_units}
        '''
        value = SpannerInstanceAutoscalingConfigAutoscalingLimits(
            max_nodes=max_nodes,
            max_processing_units=max_processing_units,
            min_nodes=min_nodes,
            min_processing_units=min_processing_units,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscalingLimits", [value]))

    @jsii.member(jsii_name="putAutoscalingTargets")
    def put_autoscaling_targets(
        self,
        *,
        high_priority_cpu_utilization_percent: typing.Optional[jsii.Number] = None,
        storage_utilization_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param high_priority_cpu_utilization_percent: Specifies the target high priority cpu utilization percentage that the autoscaler should be trying to achieve for the instance. This number is on a scale from 0 (no utilization) to 100 (full utilization).. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#high_priority_cpu_utilization_percent SpannerInstance#high_priority_cpu_utilization_percent}
        :param storage_utilization_percent: Specifies the target storage utilization percentage that the autoscaler should be trying to achieve for the instance. This number is on a scale from 0 (no utilization) to 100 (full utilization). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#storage_utilization_percent SpannerInstance#storage_utilization_percent}
        '''
        value = SpannerInstanceAutoscalingConfigAutoscalingTargets(
            high_priority_cpu_utilization_percent=high_priority_cpu_utilization_percent,
            storage_utilization_percent=storage_utilization_percent,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscalingTargets", [value]))

    @jsii.member(jsii_name="resetAsymmetricAutoscalingOptions")
    def reset_asymmetric_autoscaling_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAsymmetricAutoscalingOptions", []))

    @jsii.member(jsii_name="resetAutoscalingLimits")
    def reset_autoscaling_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingLimits", []))

    @jsii.member(jsii_name="resetAutoscalingTargets")
    def reset_autoscaling_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingTargets", []))

    @builtins.property
    @jsii.member(jsii_name="asymmetricAutoscalingOptions")
    def asymmetric_autoscaling_options(
        self,
    ) -> SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsList:
        return typing.cast(SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsList, jsii.get(self, "asymmetricAutoscalingOptions"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingLimits")
    def autoscaling_limits(
        self,
    ) -> SpannerInstanceAutoscalingConfigAutoscalingLimitsOutputReference:
        return typing.cast(SpannerInstanceAutoscalingConfigAutoscalingLimitsOutputReference, jsii.get(self, "autoscalingLimits"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingTargets")
    def autoscaling_targets(
        self,
    ) -> SpannerInstanceAutoscalingConfigAutoscalingTargetsOutputReference:
        return typing.cast(SpannerInstanceAutoscalingConfigAutoscalingTargetsOutputReference, jsii.get(self, "autoscalingTargets"))

    @builtins.property
    @jsii.member(jsii_name="asymmetricAutoscalingOptionsInput")
    def asymmetric_autoscaling_options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions]]], jsii.get(self, "asymmetricAutoscalingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingLimitsInput")
    def autoscaling_limits_input(
        self,
    ) -> typing.Optional[SpannerInstanceAutoscalingConfigAutoscalingLimits]:
        return typing.cast(typing.Optional[SpannerInstanceAutoscalingConfigAutoscalingLimits], jsii.get(self, "autoscalingLimitsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingTargetsInput")
    def autoscaling_targets_input(
        self,
    ) -> typing.Optional[SpannerInstanceAutoscalingConfigAutoscalingTargets]:
        return typing.cast(typing.Optional[SpannerInstanceAutoscalingConfigAutoscalingTargets], jsii.get(self, "autoscalingTargetsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SpannerInstanceAutoscalingConfig]:
        return typing.cast(typing.Optional[SpannerInstanceAutoscalingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpannerInstanceAutoscalingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d048a94de371fd4bbc94720b1db3caa83d3407421a4dbf97f5e5da01ef885d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "config": "config",
        "display_name": "displayName",
        "autoscaling_config": "autoscalingConfig",
        "default_backup_schedule_type": "defaultBackupScheduleType",
        "edition": "edition",
        "force_destroy": "forceDestroy",
        "id": "id",
        "instance_type": "instanceType",
        "labels": "labels",
        "name": "name",
        "num_nodes": "numNodes",
        "processing_units": "processingUnits",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class SpannerInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        config: builtins.str,
        display_name: builtins.str,
        autoscaling_config: typing.Optional[typing.Union[SpannerInstanceAutoscalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        default_backup_schedule_type: typing.Optional[builtins.str] = None,
        edition: typing.Optional[builtins.str] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        num_nodes: typing.Optional[jsii.Number] = None,
        processing_units: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SpannerInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param config: The name of the instance's configuration (similar but not quite the same as a region) which defines the geographic placement and replication of your databases in this instance. It determines where your data is stored. Values are typically of the form 'regional-europe-west1' , 'us-central' etc. In order to obtain a valid list please consult the `Configuration section of the docs <https://cloud.google.com/spanner/docs/instances>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#config SpannerInstance#config}
        :param display_name: The descriptive name for this instance as it appears in UIs. Must be unique per project and between 4 and 30 characters in length. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#display_name SpannerInstance#display_name}
        :param autoscaling_config: autoscaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#autoscaling_config SpannerInstance#autoscaling_config}
        :param default_backup_schedule_type: Controls the default backup behavior for new databases within the instance. Note that 'AUTOMATIC' is not permitted for free instances, as backups and backup schedules are not allowed for free instances. if unset or NONE, no default backup schedule will be created for new databases within the instance. Possible values: ["NONE", "AUTOMATIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#default_backup_schedule_type SpannerInstance#default_backup_schedule_type}
        :param edition: The edition selected for this instance. Different editions provide different capabilities at different price points. Possible values: ["EDITION_UNSPECIFIED", "STANDARD", "ENTERPRISE", "ENTERPRISE_PLUS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#edition SpannerInstance#edition}
        :param force_destroy: When deleting a spanner instance, this boolean option will delete all backups of this instance. This must be set to true if you created a backup manually in the console. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#force_destroy SpannerInstance#force_destroy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#id SpannerInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_type: The type of this instance. The type can be used to distinguish product variants, that can affect aspects like: usage restrictions, quotas and billing. Currently this is used to distinguish FREE_INSTANCE vs PROVISIONED instances. When configured as FREE_INSTANCE, the field 'edition' should not be configured. Possible values: ["PROVISIONED", "FREE_INSTANCE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#instance_type SpannerInstance#instance_type}
        :param labels: An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#labels SpannerInstance#labels}
        :param name: A unique identifier for the instance, which cannot be changed after the instance is created. The name must be between 6 and 30 characters in length. If not provided, a random string starting with 'tf-' will be selected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#name SpannerInstance#name}
        :param num_nodes: The number of nodes allocated to this instance. Exactly one of either num_nodes, processing_units or autoscaling_config must be present in terraform except when instance_type = FREE_INSTANCE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#num_nodes SpannerInstance#num_nodes}
        :param processing_units: The number of processing units allocated to this instance. Exactly one of either num_nodes, processing_units or autoscaling_config must be present in terraform except when instance_type = FREE_INSTANCE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#processing_units SpannerInstance#processing_units}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#project SpannerInstance#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#timeouts SpannerInstance#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscaling_config, dict):
            autoscaling_config = SpannerInstanceAutoscalingConfig(**autoscaling_config)
        if isinstance(timeouts, dict):
            timeouts = SpannerInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d52737019f351c0484e1abc99e331c584fdd2a113bc60098f9bd0c2aa92b1d2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument autoscaling_config", value=autoscaling_config, expected_type=type_hints["autoscaling_config"])
            check_type(argname="argument default_backup_schedule_type", value=default_backup_schedule_type, expected_type=type_hints["default_backup_schedule_type"])
            check_type(argname="argument edition", value=edition, expected_type=type_hints["edition"])
            check_type(argname="argument force_destroy", value=force_destroy, expected_type=type_hints["force_destroy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument num_nodes", value=num_nodes, expected_type=type_hints["num_nodes"])
            check_type(argname="argument processing_units", value=processing_units, expected_type=type_hints["processing_units"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config": config,
            "display_name": display_name,
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
        if autoscaling_config is not None:
            self._values["autoscaling_config"] = autoscaling_config
        if default_backup_schedule_type is not None:
            self._values["default_backup_schedule_type"] = default_backup_schedule_type
        if edition is not None:
            self._values["edition"] = edition
        if force_destroy is not None:
            self._values["force_destroy"] = force_destroy
        if id is not None:
            self._values["id"] = id
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if labels is not None:
            self._values["labels"] = labels
        if name is not None:
            self._values["name"] = name
        if num_nodes is not None:
            self._values["num_nodes"] = num_nodes
        if processing_units is not None:
            self._values["processing_units"] = processing_units
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
    def config(self) -> builtins.str:
        '''The name of the instance's configuration (similar but not quite the same as a region) which defines the geographic placement and replication of your databases in this instance.

        It determines where your data
        is stored. Values are typically of the form 'regional-europe-west1' , 'us-central' etc.
        In order to obtain a valid list please consult the
        `Configuration section of the docs <https://cloud.google.com/spanner/docs/instances>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#config SpannerInstance#config}
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The descriptive name for this instance as it appears in UIs.

        Must be
        unique per project and between 4 and 30 characters in length.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#display_name SpannerInstance#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscaling_config(self) -> typing.Optional[SpannerInstanceAutoscalingConfig]:
        '''autoscaling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#autoscaling_config SpannerInstance#autoscaling_config}
        '''
        result = self._values.get("autoscaling_config")
        return typing.cast(typing.Optional[SpannerInstanceAutoscalingConfig], result)

    @builtins.property
    def default_backup_schedule_type(self) -> typing.Optional[builtins.str]:
        '''Controls the default backup behavior for new databases within the instance.

        Note that 'AUTOMATIC' is not permitted for free instances, as backups and backup schedules are not allowed for free instances.
        if unset or NONE, no default backup schedule will be created for new databases within the instance. Possible values: ["NONE", "AUTOMATIC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#default_backup_schedule_type SpannerInstance#default_backup_schedule_type}
        '''
        result = self._values.get("default_backup_schedule_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edition(self) -> typing.Optional[builtins.str]:
        '''The edition selected for this instance.

        Different editions provide different capabilities at different price points. Possible values: ["EDITION_UNSPECIFIED", "STANDARD", "ENTERPRISE", "ENTERPRISE_PLUS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#edition SpannerInstance#edition}
        '''
        result = self._values.get("edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When deleting a spanner instance, this boolean option will delete all backups of this instance.

        This must be set to true if you created a backup manually in the console.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#force_destroy SpannerInstance#force_destroy}
        '''
        result = self._values.get("force_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#id SpannerInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''The type of this instance.

        The type can be used to distinguish product variants, that can affect aspects like:
        usage restrictions, quotas and billing. Currently this is used to distinguish FREE_INSTANCE vs PROVISIONED instances.
        When configured as FREE_INSTANCE, the field 'edition' should not be configured. Possible values: ["PROVISIONED", "FREE_INSTANCE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#instance_type SpannerInstance#instance_type}
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#labels SpannerInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for the instance, which cannot be changed after the instance is created.

        The name must be between 6 and 30 characters
        in length.
        If not provided, a random string starting with 'tf-' will be selected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#name SpannerInstance#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_nodes(self) -> typing.Optional[jsii.Number]:
        '''The number of nodes allocated to this instance.

        Exactly one of either num_nodes, processing_units or
        autoscaling_config must be present in terraform except when instance_type = FREE_INSTANCE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#num_nodes SpannerInstance#num_nodes}
        '''
        result = self._values.get("num_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def processing_units(self) -> typing.Optional[jsii.Number]:
        '''The number of processing units allocated to this instance.

        Exactly one of either num_nodes,
        processing_units or autoscaling_config must be present in terraform except when instance_type = FREE_INSTANCE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#processing_units SpannerInstance#processing_units}
        '''
        result = self._values.get("processing_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#project SpannerInstance#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SpannerInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#timeouts SpannerInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SpannerInstanceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class SpannerInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#create SpannerInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#delete SpannerInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#update SpannerInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f091423093be104f8f57784003b8177568a94e7ba23876bc8ad5ebc393aad820)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#create SpannerInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#delete SpannerInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_instance#update SpannerInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpannerInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerInstance.SpannerInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07b95adec92a7c6222506193afef6e6289099b818e27ff52f3617aad697bdb16)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8d66ab76a0e0e16e1edb6198d9208c418ebf986ca652cc1bb723c2cb1e07276)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2fb2638f2c79705a0000b670b0b3a993e018759f8c569be5aae688c2162815a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4568b6d46ccfcc8bd336683914434fe297663a365ea97cb46c4bd2726b2b9929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpannerInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpannerInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpannerInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b18fa64056e18cebbbed5508a10453365055812daa96d027e01f0c2ec3fe26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SpannerInstance",
    "SpannerInstanceAutoscalingConfig",
    "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions",
    "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsList",
    "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOutputReference",
    "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverrides",
    "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimits",
    "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimitsOutputReference",
    "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesOutputReference",
    "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelection",
    "SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelectionOutputReference",
    "SpannerInstanceAutoscalingConfigAutoscalingLimits",
    "SpannerInstanceAutoscalingConfigAutoscalingLimitsOutputReference",
    "SpannerInstanceAutoscalingConfigAutoscalingTargets",
    "SpannerInstanceAutoscalingConfigAutoscalingTargetsOutputReference",
    "SpannerInstanceAutoscalingConfigOutputReference",
    "SpannerInstanceConfig",
    "SpannerInstanceTimeouts",
    "SpannerInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__380c5721ee80df673aad762c971eecd3881a6a5c9aa74e5c48bdf276e77ca26a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    config: builtins.str,
    display_name: builtins.str,
    autoscaling_config: typing.Optional[typing.Union[SpannerInstanceAutoscalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_backup_schedule_type: typing.Optional[builtins.str] = None,
    edition: typing.Optional[builtins.str] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    num_nodes: typing.Optional[jsii.Number] = None,
    processing_units: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SpannerInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d75f292b6d38b380129aded8146ae88c9bc1adfe20bf51732269f62746144ae8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6797470e536d05ebb40fa2a7ad06ce8cabd6c7dead20bd3420ed0442721295(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c778ab13459f16109ea75076e590eb39e804adc5f8d3881f80031b800e59261b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8927dd8d3a2ad2ca72dce60ddfb61c613556924dbe0c71021813f9e22572926(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93cfee99c4d826244133d76e500eefc22db694ad061d7d2484a802e2a85cf008(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e182fee054c81811d0643fe3bced1bbd1f9065a9fbacd4bfdf44f17e227e59fc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b4faebfa62148102d96db738b9d276b40f9d27449d85e39dedd4d291392776(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b65d5fc99be59a716b154a84293dc6495ce5df4321f7444e13f3e60c982208(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbb004b28b48fa6c919c087c17cc521229343616f8decf9d867d4a330eb43e9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b460b6875222dfa01ce15f0e263a05c1ec3405035a02647de2b9e5d822cab58b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__817f9c30943e43892ae5801356e7ab8c0ef477cc2c41885029593b97882584a8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5c98b87400c78014ec4c184e03e5b4f5e2c7444c9921573193cae8fe615d17(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6262ed7a4c0cf6134e3e2a01ba2d47a52b859613045e3f6ff8a88a3f045564f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__369ef5e84fceb2829fe8e55a3d0936b043b7968165a2bdd2e97e9834155984d6(
    *,
    asymmetric_autoscaling_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    autoscaling_limits: typing.Optional[typing.Union[SpannerInstanceAutoscalingConfigAutoscalingLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    autoscaling_targets: typing.Optional[typing.Union[SpannerInstanceAutoscalingConfigAutoscalingTargets, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24bf8ef539f0f4a2d1742d095a061040221ae561af4c486313860b049a9c04ff(
    *,
    overrides: typing.Union[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverrides, typing.Dict[builtins.str, typing.Any]],
    replica_selection: typing.Union[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelection, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec35384e197983705cfe00426d476ab6f1b1576bdb95a8085b59f45f3e59db2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0b720fcc854fe7c6bbee7cd8b4d632d0bbce73002888a43618d6bf41f3459e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e05c9e0897f9196ea687fbe57d9405d772778f332d364f183f3319e441dfee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4f2f7418b18a8d9d2f75efa1454a24d22650532f523ed21cc864ac584f69bd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8052446af8331ae14660f59c6bd47ddab26437ccf581f27c237217a25f8e561a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88bd6ee8ba9ef9c6a8232d4b8935910c48f31da263c2794a6b73da4d3034fcd7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54c8c045955328f23106cce5f62df82d1068bffb25dd054e7d3254d767f12da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e3d9c726e6472354524c32c22ec8f205346fe4836180adb7549db3b644254d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a122ce0b62ea0749d4d2d5652af2e70b62afd06ad431fafddceb324637b163(
    *,
    autoscaling_limits: typing.Union[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimits, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2945ee64d5f4ca0cb254d9c90d8279c730f16f44a9d2449a17cdb18ad15da74b(
    *,
    max_nodes: jsii.Number,
    min_nodes: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3ab30715322455c2233aca491cf5589e3ed95c51bda8dc97831a4acafe5c6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc8e2c98a6d6e5de31e01aa4921e41e4c74971e4cb1cde5dd61f76340ab0c6a5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb6208fcfa990611cd3b8f248603a49b4a5fd7d179060ea5ef3add2e6fbed6cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc53ce5a652fef610edca619ecf9e3eb55bdef367c0092ee01d80f46b1ab683c(
    value: typing.Optional[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverridesAutoscalingLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb835b226fcae1c39382616c838040f3d25f8edf4f9e799ddd110dbc0992b73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26d60ff76aeceb0264e545bd8ad293e27ff0f5c8793dd9b0359f3dd8a95e770(
    value: typing.Optional[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsOverrides],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f2dbcab548b6d1bf3bdcd87e69ba916ec38f6afcf8bb830be86dacd69283e28(
    *,
    location: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c2c40180e90458744488800888036536334a9ffa858ce50d18bfc30a44a68f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5bdc7206c240798b76c8c343e05cf9fa35f5519bf1f90483dec3b7fc0f1d41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda949eb20a3bbc117692a994fff5336acabb760702d1278155f9ee5ade5d74d(
    value: typing.Optional[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptionsReplicaSelection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9553282bc74e82b2d4dcbe3c5f5afe1fbbb02ab39b6e334776f94e29753b1b7(
    *,
    max_nodes: typing.Optional[jsii.Number] = None,
    max_processing_units: typing.Optional[jsii.Number] = None,
    min_nodes: typing.Optional[jsii.Number] = None,
    min_processing_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b315ffb101ec14cd6685c0d86e9d50258b58d0c139a53254d0daae347ad74fd3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6233fecc8120b24fe399e95c7e4915fae50a10bda00d1817b25ddaa314ce4a9e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deba06b5282f5906e68d734212f95896b7312e05eac64e16742545ec47b32304(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959c20bc5402c21c7f492263b9527f3e7862fd8492c3a5b425a9bc48b838fada(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d967d119cffc0035598df4c89c2fc9e98defb0af2486089cbf595f620b39ede(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9a35ea023b9c7a32ffa90a274fc79df35fe39705e303597b42b0d18a7c4dca(
    value: typing.Optional[SpannerInstanceAutoscalingConfigAutoscalingLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef839a006be4982aae0221804dd84e81c139fda09578b9467182ed7a5cc47f9d(
    *,
    high_priority_cpu_utilization_percent: typing.Optional[jsii.Number] = None,
    storage_utilization_percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c17652c7e6a4fe6d755dec704d35d920abf684ff83efe8a034ba5a70f923e29b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__646ce11e43533cc4b35a614e683df8be044a17805e1348249d78aabba0e1f3a7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9dd6c2f06849c53d09e4ed235e73712bdfa485b91b93984187ccd82d0f7c9c3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264491d906c348428d09a308e4e89c5467071978e378ae4469395d6654299b2f(
    value: typing.Optional[SpannerInstanceAutoscalingConfigAutoscalingTargets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a5a20ceac108dd2aa37bd99479c6d78bd31279e26b6f48569affb743431f9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972a4c74e3674066fec90f8c67651a594fd5b64ff2cf3fa89c0ae4116a2ab0ef(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SpannerInstanceAutoscalingConfigAsymmetricAutoscalingOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d048a94de371fd4bbc94720b1db3caa83d3407421a4dbf97f5e5da01ef885d4(
    value: typing.Optional[SpannerInstanceAutoscalingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d52737019f351c0484e1abc99e331c584fdd2a113bc60098f9bd0c2aa92b1d2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    config: builtins.str,
    display_name: builtins.str,
    autoscaling_config: typing.Optional[typing.Union[SpannerInstanceAutoscalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_backup_schedule_type: typing.Optional[builtins.str] = None,
    edition: typing.Optional[builtins.str] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    num_nodes: typing.Optional[jsii.Number] = None,
    processing_units: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SpannerInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f091423093be104f8f57784003b8177568a94e7ba23876bc8ad5ebc393aad820(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b95adec92a7c6222506193afef6e6289099b818e27ff52f3617aad697bdb16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d66ab76a0e0e16e1edb6198d9208c418ebf986ca652cc1bb723c2cb1e07276(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2fb2638f2c79705a0000b670b0b3a993e018759f8c569be5aae688c2162815a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4568b6d46ccfcc8bd336683914434fe297663a365ea97cb46c4bd2726b2b9929(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b18fa64056e18cebbbed5508a10453365055812daa96d027e01f0c2ec3fe26(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpannerInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

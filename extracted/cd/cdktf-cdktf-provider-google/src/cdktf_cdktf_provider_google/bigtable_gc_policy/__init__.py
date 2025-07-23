r'''
# `google_bigtable_gc_policy`

Refer to the Terraform Registry for docs: [`google_bigtable_gc_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy).
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


class BigtableGcPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableGcPolicy.BigtableGcPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy google_bigtable_gc_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        column_family: builtins.str,
        instance_name: builtins.str,
        table: builtins.str,
        deletion_policy: typing.Optional[builtins.str] = None,
        gc_rules: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_warnings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_age: typing.Optional[typing.Union["BigtableGcPolicyMaxAge", typing.Dict[builtins.str, typing.Any]]] = None,
        max_version: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigtableGcPolicyMaxVersion", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mode: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BigtableGcPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy google_bigtable_gc_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param column_family: The name of the column family. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#column_family BigtableGcPolicy#column_family}
        :param instance_name: The name of the Bigtable instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#instance_name BigtableGcPolicy#instance_name}
        :param table: The name of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#table BigtableGcPolicy#table}
        :param deletion_policy: The deletion policy for the GC policy. Setting ABANDON allows the resource to be abandoned rather than deleted. This is useful for GC policy as it cannot be deleted in a replicated instance. Possible values are: "ABANDON". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#deletion_policy BigtableGcPolicy#deletion_policy}
        :param gc_rules: Serialized JSON string for garbage collection policy. Conflicts with "mode", "max_age" and "max_version". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#gc_rules BigtableGcPolicy#gc_rules}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#id BigtableGcPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_warnings: Allows ignoring warnings when updating the GC policy. This can be used to increase the gc policy on replicated clusters. Doing this may make clusters be inconsistent for a longer period of time, before using this make sure you understand the risks listed at https://cloud.google.com/bigtable/docs/garbage-collection#increasing Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#ignore_warnings BigtableGcPolicy#ignore_warnings}
        :param max_age: max_age block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#max_age BigtableGcPolicy#max_age}
        :param max_version: max_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#max_version BigtableGcPolicy#max_version}
        :param mode: NOTE: 'gc_rules' is more flexible, and should be preferred over this field for new resources. This field may be deprecated in the future. If multiple policies are set, you should choose between UNION OR INTERSECTION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#mode BigtableGcPolicy#mode}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#project BigtableGcPolicy#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#timeouts BigtableGcPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc8673dd33c650f89931ecc34a9ea4a170f6eb4bd9b2857896b05e59e0abce5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BigtableGcPolicyConfig(
            column_family=column_family,
            instance_name=instance_name,
            table=table,
            deletion_policy=deletion_policy,
            gc_rules=gc_rules,
            id=id,
            ignore_warnings=ignore_warnings,
            max_age=max_age,
            max_version=max_version,
            mode=mode,
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
        '''Generates CDKTF code for importing a BigtableGcPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BigtableGcPolicy to import.
        :param import_from_id: The id of the existing BigtableGcPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BigtableGcPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__982384b5621d7a3d612132ca18e1a2cfbbb9414afc50992a59642d53c367b6b1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMaxAge")
    def put_max_age(
        self,
        *,
        days: typing.Optional[jsii.Number] = None,
        duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param days: Number of days before applying GC policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#days BigtableGcPolicy#days}
        :param duration: Duration before applying GC policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#duration BigtableGcPolicy#duration}
        '''
        value = BigtableGcPolicyMaxAge(days=days, duration=duration)

        return typing.cast(None, jsii.invoke(self, "putMaxAge", [value]))

    @jsii.member(jsii_name="putMaxVersion")
    def put_max_version(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigtableGcPolicyMaxVersion", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0788f36fae0182294a47b837a6967e8979f503de217a74539356989a40fbc670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMaxVersion", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#create BigtableGcPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#delete BigtableGcPolicy#delete}.
        '''
        value = BigtableGcPolicyTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDeletionPolicy")
    def reset_deletion_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionPolicy", []))

    @jsii.member(jsii_name="resetGcRules")
    def reset_gc_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcRules", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIgnoreWarnings")
    def reset_ignore_warnings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreWarnings", []))

    @jsii.member(jsii_name="resetMaxAge")
    def reset_max_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAge", []))

    @jsii.member(jsii_name="resetMaxVersion")
    def reset_max_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxVersion", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

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
    @jsii.member(jsii_name="maxAge")
    def max_age(self) -> "BigtableGcPolicyMaxAgeOutputReference":
        return typing.cast("BigtableGcPolicyMaxAgeOutputReference", jsii.get(self, "maxAge"))

    @builtins.property
    @jsii.member(jsii_name="maxVersion")
    def max_version(self) -> "BigtableGcPolicyMaxVersionList":
        return typing.cast("BigtableGcPolicyMaxVersionList", jsii.get(self, "maxVersion"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BigtableGcPolicyTimeoutsOutputReference":
        return typing.cast("BigtableGcPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="columnFamilyInput")
    def column_family_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnFamilyInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionPolicyInput")
    def deletion_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deletionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="gcRulesInput")
    def gc_rules_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreWarningsInput")
    def ignore_warnings_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreWarningsInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceNameInput")
    def instance_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAgeInput")
    def max_age_input(self) -> typing.Optional["BigtableGcPolicyMaxAge"]:
        return typing.cast(typing.Optional["BigtableGcPolicyMaxAge"], jsii.get(self, "maxAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxVersionInput")
    def max_version_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigtableGcPolicyMaxVersion"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigtableGcPolicyMaxVersion"]]], jsii.get(self, "maxVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigtableGcPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigtableGcPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="columnFamily")
    def column_family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnFamily"))

    @column_family.setter
    def column_family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57164b36ad7b2ad2fa1a8b87a57e26f983a3685405f0ddd340a7780f6afc45a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnFamily", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionPolicy")
    def deletion_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionPolicy"))

    @deletion_policy.setter
    def deletion_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a3f14d253332dcb2d278c3876256bb26ea807de1cc48b492b6a17d022566ee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcRules")
    def gc_rules(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcRules"))

    @gc_rules.setter
    def gc_rules(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bad8d335bc50d89e132aa59777f92cf1773a1e640148ab5eda5c247fd3d8bdc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcRules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1229dcb57d94836e0f79f0282bcd673eacc93e569e783a59c098c2ac8faa266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreWarnings")
    def ignore_warnings(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreWarnings"))

    @ignore_warnings.setter
    def ignore_warnings(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9811c76673a84482c9269b6866a7a102db8a69fd688e209cc10fbfae6c7bb81d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreWarnings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceName")
    def instance_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceName"))

    @instance_name.setter
    def instance_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7b94341da2b107c9e04ad89132efcf917a3ad05bb1b2239f0e28d0f6ba9ac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a99dc79227b28f4c38be3bcd8da00f0902cb229200e3819ca440c510c0287b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be1e5896d4114d0a763253a875c5d088d2900b04f6067ca2cb4f6e537fee335a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "table"))

    @table.setter
    def table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f3271fe1b0112b5177239dac7733afc1ff696f4720ad994d4a08272e4548906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigtableGcPolicy.BigtableGcPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "column_family": "columnFamily",
        "instance_name": "instanceName",
        "table": "table",
        "deletion_policy": "deletionPolicy",
        "gc_rules": "gcRules",
        "id": "id",
        "ignore_warnings": "ignoreWarnings",
        "max_age": "maxAge",
        "max_version": "maxVersion",
        "mode": "mode",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class BigtableGcPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        column_family: builtins.str,
        instance_name: builtins.str,
        table: builtins.str,
        deletion_policy: typing.Optional[builtins.str] = None,
        gc_rules: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_warnings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_age: typing.Optional[typing.Union["BigtableGcPolicyMaxAge", typing.Dict[builtins.str, typing.Any]]] = None,
        max_version: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigtableGcPolicyMaxVersion", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mode: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BigtableGcPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param column_family: The name of the column family. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#column_family BigtableGcPolicy#column_family}
        :param instance_name: The name of the Bigtable instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#instance_name BigtableGcPolicy#instance_name}
        :param table: The name of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#table BigtableGcPolicy#table}
        :param deletion_policy: The deletion policy for the GC policy. Setting ABANDON allows the resource to be abandoned rather than deleted. This is useful for GC policy as it cannot be deleted in a replicated instance. Possible values are: "ABANDON". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#deletion_policy BigtableGcPolicy#deletion_policy}
        :param gc_rules: Serialized JSON string for garbage collection policy. Conflicts with "mode", "max_age" and "max_version". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#gc_rules BigtableGcPolicy#gc_rules}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#id BigtableGcPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_warnings: Allows ignoring warnings when updating the GC policy. This can be used to increase the gc policy on replicated clusters. Doing this may make clusters be inconsistent for a longer period of time, before using this make sure you understand the risks listed at https://cloud.google.com/bigtable/docs/garbage-collection#increasing Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#ignore_warnings BigtableGcPolicy#ignore_warnings}
        :param max_age: max_age block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#max_age BigtableGcPolicy#max_age}
        :param max_version: max_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#max_version BigtableGcPolicy#max_version}
        :param mode: NOTE: 'gc_rules' is more flexible, and should be preferred over this field for new resources. This field may be deprecated in the future. If multiple policies are set, you should choose between UNION OR INTERSECTION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#mode BigtableGcPolicy#mode}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#project BigtableGcPolicy#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#timeouts BigtableGcPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(max_age, dict):
            max_age = BigtableGcPolicyMaxAge(**max_age)
        if isinstance(timeouts, dict):
            timeouts = BigtableGcPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffc65a17c52c9127dc1632f1d1028103821a119df8423a762941697022d860e3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument column_family", value=column_family, expected_type=type_hints["column_family"])
            check_type(argname="argument instance_name", value=instance_name, expected_type=type_hints["instance_name"])
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument deletion_policy", value=deletion_policy, expected_type=type_hints["deletion_policy"])
            check_type(argname="argument gc_rules", value=gc_rules, expected_type=type_hints["gc_rules"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ignore_warnings", value=ignore_warnings, expected_type=type_hints["ignore_warnings"])
            check_type(argname="argument max_age", value=max_age, expected_type=type_hints["max_age"])
            check_type(argname="argument max_version", value=max_version, expected_type=type_hints["max_version"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_family": column_family,
            "instance_name": instance_name,
            "table": table,
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
        if deletion_policy is not None:
            self._values["deletion_policy"] = deletion_policy
        if gc_rules is not None:
            self._values["gc_rules"] = gc_rules
        if id is not None:
            self._values["id"] = id
        if ignore_warnings is not None:
            self._values["ignore_warnings"] = ignore_warnings
        if max_age is not None:
            self._values["max_age"] = max_age
        if max_version is not None:
            self._values["max_version"] = max_version
        if mode is not None:
            self._values["mode"] = mode
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
    def column_family(self) -> builtins.str:
        '''The name of the column family.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#column_family BigtableGcPolicy#column_family}
        '''
        result = self._values.get("column_family")
        assert result is not None, "Required property 'column_family' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_name(self) -> builtins.str:
        '''The name of the Bigtable instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#instance_name BigtableGcPolicy#instance_name}
        '''
        result = self._values.get("instance_name")
        assert result is not None, "Required property 'instance_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table(self) -> builtins.str:
        '''The name of the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#table BigtableGcPolicy#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deletion_policy(self) -> typing.Optional[builtins.str]:
        '''The deletion policy for the GC policy.

        Setting ABANDON allows the resource
        to be abandoned rather than deleted. This is useful for GC policy as it cannot be deleted
        in a replicated instance. Possible values are: "ABANDON".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#deletion_policy BigtableGcPolicy#deletion_policy}
        '''
        result = self._values.get("deletion_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gc_rules(self) -> typing.Optional[builtins.str]:
        '''Serialized JSON string for garbage collection policy. Conflicts with "mode", "max_age" and "max_version".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#gc_rules BigtableGcPolicy#gc_rules}
        '''
        result = self._values.get("gc_rules")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#id BigtableGcPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_warnings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows ignoring warnings when updating the GC policy.

        This can be used
        to increase the gc policy on replicated clusters. Doing this may make clusters be
        inconsistent for a longer period of time, before using this make sure you understand
        the risks listed at https://cloud.google.com/bigtable/docs/garbage-collection#increasing

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#ignore_warnings BigtableGcPolicy#ignore_warnings}
        '''
        result = self._values.get("ignore_warnings")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_age(self) -> typing.Optional["BigtableGcPolicyMaxAge"]:
        '''max_age block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#max_age BigtableGcPolicy#max_age}
        '''
        result = self._values.get("max_age")
        return typing.cast(typing.Optional["BigtableGcPolicyMaxAge"], result)

    @builtins.property
    def max_version(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigtableGcPolicyMaxVersion"]]]:
        '''max_version block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#max_version BigtableGcPolicy#max_version}
        '''
        result = self._values.get("max_version")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigtableGcPolicyMaxVersion"]]], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''NOTE: 'gc_rules' is more flexible, and should be preferred over this field for new resources.

        This field may be deprecated in the future. If multiple policies are set, you should choose between UNION OR INTERSECTION.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#mode BigtableGcPolicy#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#project BigtableGcPolicy#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BigtableGcPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#timeouts BigtableGcPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BigtableGcPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigtableGcPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigtableGcPolicy.BigtableGcPolicyMaxAge",
    jsii_struct_bases=[],
    name_mapping={"days": "days", "duration": "duration"},
)
class BigtableGcPolicyMaxAge:
    def __init__(
        self,
        *,
        days: typing.Optional[jsii.Number] = None,
        duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param days: Number of days before applying GC policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#days BigtableGcPolicy#days}
        :param duration: Duration before applying GC policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#duration BigtableGcPolicy#duration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c752d9e192a89aa473dedccbcd5032c22f973ea14dac7790110ec6862e84964)
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if days is not None:
            self._values["days"] = days
        if duration is not None:
            self._values["duration"] = duration

    @builtins.property
    def days(self) -> typing.Optional[jsii.Number]:
        '''Number of days before applying GC policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#days BigtableGcPolicy#days}
        '''
        result = self._values.get("days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def duration(self) -> typing.Optional[builtins.str]:
        '''Duration before applying GC policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#duration BigtableGcPolicy#duration}
        '''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigtableGcPolicyMaxAge(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigtableGcPolicyMaxAgeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableGcPolicy.BigtableGcPolicyMaxAgeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__288f3de87ad3161c6160eb9a507e5c654d0fbb37ed122a31ac9d11ee513e4cfe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDays")
    def reset_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDays", []))

    @jsii.member(jsii_name="resetDuration")
    def reset_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuration", []))

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "days"))

    @days.setter
    def days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00608415379d6c7874d3093de50131fc66a757f56e8268db320e780e5978ddc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb568562948e7c4770a87eca99d9b8282ea44ca8d50f0deaa8aaf16a2a986077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigtableGcPolicyMaxAge]:
        return typing.cast(typing.Optional[BigtableGcPolicyMaxAge], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BigtableGcPolicyMaxAge]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e9de0596ccab35e810be4fde8510c19eca70a07c128f1578833ca89f3ec0d1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigtableGcPolicy.BigtableGcPolicyMaxVersion",
    jsii_struct_bases=[],
    name_mapping={"number": "number"},
)
class BigtableGcPolicyMaxVersion:
    def __init__(self, *, number: jsii.Number) -> None:
        '''
        :param number: Number of version before applying the GC policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#number BigtableGcPolicy#number}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9e17dd5e708b9f78097e7b355ee89c77a7c09b3f148b7b78a594001d957e2c)
            check_type(argname="argument number", value=number, expected_type=type_hints["number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "number": number,
        }

    @builtins.property
    def number(self) -> jsii.Number:
        '''Number of version before applying the GC policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#number BigtableGcPolicy#number}
        '''
        result = self._values.get("number")
        assert result is not None, "Required property 'number' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigtableGcPolicyMaxVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigtableGcPolicyMaxVersionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableGcPolicy.BigtableGcPolicyMaxVersionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8761875614994e4a900ef82bdabab04bd45116a79779e73548c7ae4ca5090b5e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BigtableGcPolicyMaxVersionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__173afe7a7590054a3dde3df24928a6bdc9a30f041ed0373743aa9bc0c7644181)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BigtableGcPolicyMaxVersionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a2e932568d82c1cf9ef0dcad9200258f3dde1c612f4b946776124279282d176)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b2d701f6e5112abd705fe3caa6bd7dd26d472b934a743e6897baf93f3ce6dd9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54ff4756bc51f5a885e0d92fd78eb90d226bf35181685e6158c421597159bfeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigtableGcPolicyMaxVersion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigtableGcPolicyMaxVersion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigtableGcPolicyMaxVersion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51eeb8a5ec4cf45dde211bc19131cc7eb75a941d81a49e082793ea4c9ad18294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigtableGcPolicyMaxVersionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableGcPolicy.BigtableGcPolicyMaxVersionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__433096dd885663c7d7a3b6d025b44e153d1473bace9c9db0fb331ffa8a0f7243)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="numberInput")
    def number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberInput"))

    @builtins.property
    @jsii.member(jsii_name="number")
    def number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "number"))

    @number.setter
    def number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7211b5524556560fc535f17414f00b87926d6815fad88d90d093ff8b4d443c26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "number", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableGcPolicyMaxVersion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableGcPolicyMaxVersion]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableGcPolicyMaxVersion]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cdea75ef6ec8f351aaaaf2e696342a0bb2f1de2086d1af6a37aa0f3d02a306a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigtableGcPolicy.BigtableGcPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class BigtableGcPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#create BigtableGcPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#delete BigtableGcPolicy#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff3ef7f160129e6090767b2352a6466b71dd2063bedf591d8019722e3d42264)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#create BigtableGcPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_gc_policy#delete BigtableGcPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigtableGcPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigtableGcPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableGcPolicy.BigtableGcPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e7d8fc81ff7b02ad21faf2889e7c3efa8d73dd869e6795076402c117fe7ef7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e413dfe2fa04f6dc3dbc938ff3665e5555d04b3243a4e9163420afb33ec30e16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f793e6c2f83ac37f60c9e36677b586ecb9c07d1149259dac3eb7bbbaa0e4192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableGcPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableGcPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableGcPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__122b2b00e7c8fefecb904bd68de7f53ac8977f305ae5bc797408f1b4c7f6c223)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BigtableGcPolicy",
    "BigtableGcPolicyConfig",
    "BigtableGcPolicyMaxAge",
    "BigtableGcPolicyMaxAgeOutputReference",
    "BigtableGcPolicyMaxVersion",
    "BigtableGcPolicyMaxVersionList",
    "BigtableGcPolicyMaxVersionOutputReference",
    "BigtableGcPolicyTimeouts",
    "BigtableGcPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4fc8673dd33c650f89931ecc34a9ea4a170f6eb4bd9b2857896b05e59e0abce5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    column_family: builtins.str,
    instance_name: builtins.str,
    table: builtins.str,
    deletion_policy: typing.Optional[builtins.str] = None,
    gc_rules: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_warnings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_age: typing.Optional[typing.Union[BigtableGcPolicyMaxAge, typing.Dict[builtins.str, typing.Any]]] = None,
    max_version: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigtableGcPolicyMaxVersion, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mode: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BigtableGcPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__982384b5621d7a3d612132ca18e1a2cfbbb9414afc50992a59642d53c367b6b1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0788f36fae0182294a47b837a6967e8979f503de217a74539356989a40fbc670(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigtableGcPolicyMaxVersion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57164b36ad7b2ad2fa1a8b87a57e26f983a3685405f0ddd340a7780f6afc45a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3f14d253332dcb2d278c3876256bb26ea807de1cc48b492b6a17d022566ee6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bad8d335bc50d89e132aa59777f92cf1773a1e640148ab5eda5c247fd3d8bdc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1229dcb57d94836e0f79f0282bcd673eacc93e569e783a59c098c2ac8faa266(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9811c76673a84482c9269b6866a7a102db8a69fd688e209cc10fbfae6c7bb81d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7b94341da2b107c9e04ad89132efcf917a3ad05bb1b2239f0e28d0f6ba9ac6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99dc79227b28f4c38be3bcd8da00f0902cb229200e3819ca440c510c0287b64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1e5896d4114d0a763253a875c5d088d2900b04f6067ca2cb4f6e537fee335a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f3271fe1b0112b5177239dac7733afc1ff696f4720ad994d4a08272e4548906(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc65a17c52c9127dc1632f1d1028103821a119df8423a762941697022d860e3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    column_family: builtins.str,
    instance_name: builtins.str,
    table: builtins.str,
    deletion_policy: typing.Optional[builtins.str] = None,
    gc_rules: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_warnings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_age: typing.Optional[typing.Union[BigtableGcPolicyMaxAge, typing.Dict[builtins.str, typing.Any]]] = None,
    max_version: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigtableGcPolicyMaxVersion, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mode: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BigtableGcPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c752d9e192a89aa473dedccbcd5032c22f973ea14dac7790110ec6862e84964(
    *,
    days: typing.Optional[jsii.Number] = None,
    duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288f3de87ad3161c6160eb9a507e5c654d0fbb37ed122a31ac9d11ee513e4cfe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00608415379d6c7874d3093de50131fc66a757f56e8268db320e780e5978ddc3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb568562948e7c4770a87eca99d9b8282ea44ca8d50f0deaa8aaf16a2a986077(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9de0596ccab35e810be4fde8510c19eca70a07c128f1578833ca89f3ec0d1d(
    value: typing.Optional[BigtableGcPolicyMaxAge],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9e17dd5e708b9f78097e7b355ee89c77a7c09b3f148b7b78a594001d957e2c(
    *,
    number: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8761875614994e4a900ef82bdabab04bd45116a79779e73548c7ae4ca5090b5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173afe7a7590054a3dde3df24928a6bdc9a30f041ed0373743aa9bc0c7644181(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2e932568d82c1cf9ef0dcad9200258f3dde1c612f4b946776124279282d176(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2d701f6e5112abd705fe3caa6bd7dd26d472b934a743e6897baf93f3ce6dd9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ff4756bc51f5a885e0d92fd78eb90d226bf35181685e6158c421597159bfeb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51eeb8a5ec4cf45dde211bc19131cc7eb75a941d81a49e082793ea4c9ad18294(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigtableGcPolicyMaxVersion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433096dd885663c7d7a3b6d025b44e153d1473bace9c9db0fb331ffa8a0f7243(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7211b5524556560fc535f17414f00b87926d6815fad88d90d093ff8b4d443c26(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cdea75ef6ec8f351aaaaf2e696342a0bb2f1de2086d1af6a37aa0f3d02a306a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableGcPolicyMaxVersion]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff3ef7f160129e6090767b2352a6466b71dd2063bedf591d8019722e3d42264(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7d8fc81ff7b02ad21faf2889e7c3efa8d73dd869e6795076402c117fe7ef7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e413dfe2fa04f6dc3dbc938ff3665e5555d04b3243a4e9163420afb33ec30e16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f793e6c2f83ac37f60c9e36677b586ecb9c07d1149259dac3eb7bbbaa0e4192(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__122b2b00e7c8fefecb904bd68de7f53ac8977f305ae5bc797408f1b4c7f6c223(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableGcPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

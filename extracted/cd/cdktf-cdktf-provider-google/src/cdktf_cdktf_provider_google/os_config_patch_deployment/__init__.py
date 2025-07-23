r'''
# `google_os_config_patch_deployment`

Refer to the Terraform Registry for docs: [`google_os_config_patch_deployment`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment).
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


class OsConfigPatchDeployment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeployment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment google_os_config_patch_deployment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        instance_filter: typing.Union["OsConfigPatchDeploymentInstanceFilter", typing.Dict[builtins.str, typing.Any]],
        patch_deployment_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        duration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        one_time_schedule: typing.Optional[typing.Union["OsConfigPatchDeploymentOneTimeSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        patch_config: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        recurring_schedule: typing.Optional[typing.Union["OsConfigPatchDeploymentRecurringSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        rollout: typing.Optional[typing.Union["OsConfigPatchDeploymentRollout", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["OsConfigPatchDeploymentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment google_os_config_patch_deployment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param instance_filter: instance_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#instance_filter OsConfigPatchDeployment#instance_filter}
        :param patch_deployment_id: A name for the patch deployment in the project. When creating a name the following rules apply: - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#patch_deployment_id OsConfigPatchDeployment#patch_deployment_id}
        :param description: Description of the patch deployment. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#description OsConfigPatchDeployment#description}
        :param duration: Duration of the patch. After the duration ends, the patch times out. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#duration OsConfigPatchDeployment#duration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#id OsConfigPatchDeployment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param one_time_schedule: one_time_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#one_time_schedule OsConfigPatchDeployment#one_time_schedule}
        :param patch_config: patch_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#patch_config OsConfigPatchDeployment#patch_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#project OsConfigPatchDeployment#project}.
        :param recurring_schedule: recurring_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#recurring_schedule OsConfigPatchDeployment#recurring_schedule}
        :param rollout: rollout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#rollout OsConfigPatchDeployment#rollout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#timeouts OsConfigPatchDeployment#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__943ab19be923e9acd31661d5dda9109c4f13c63b6c16132d5df4fd9424eb1065)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OsConfigPatchDeploymentConfig(
            instance_filter=instance_filter,
            patch_deployment_id=patch_deployment_id,
            description=description,
            duration=duration,
            id=id,
            one_time_schedule=one_time_schedule,
            patch_config=patch_config,
            project=project,
            recurring_schedule=recurring_schedule,
            rollout=rollout,
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
        '''Generates CDKTF code for importing a OsConfigPatchDeployment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OsConfigPatchDeployment to import.
        :param import_from_id: The id of the existing OsConfigPatchDeployment that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OsConfigPatchDeployment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb8d73ba51fe651b94e8d24db7ca085898ec9526b99b0d523e7d50a4874e8f7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putInstanceFilter")
    def put_instance_filter(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigPatchDeploymentInstanceFilterGroupLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        instance_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param all: Target all VM instances in the project. If true, no other criteria is permitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#all OsConfigPatchDeployment#all}
        :param group_labels: group_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#group_labels OsConfigPatchDeployment#group_labels}
        :param instance_name_prefixes: Targets VMs whose name starts with one of these prefixes. Similar to labels, this is another way to group VMs when targeting configs, for example prefix="prod-". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#instance_name_prefixes OsConfigPatchDeployment#instance_name_prefixes}
        :param instances: Targets any of the VM instances specified. Instances are specified by their URI in the 'form zones/{{zone}}/instances/{{instance_name}}', 'projects/{{project_id}}/zones/{{zone}}/instances/{{instance_name}}', or 'https://www.googleapis.com/compute/v1/projects/{{project_id}}/zones/{{zone}}/instances/{{instance_name}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#instances OsConfigPatchDeployment#instances}
        :param zones: Targets VM instances in ANY of these zones. Leave empty to target VM instances in any zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#zones OsConfigPatchDeployment#zones}
        '''
        value = OsConfigPatchDeploymentInstanceFilter(
            all=all,
            group_labels=group_labels,
            instance_name_prefixes=instance_name_prefixes,
            instances=instances,
            zones=zones,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceFilter", [value]))

    @jsii.member(jsii_name="putOneTimeSchedule")
    def put_one_time_schedule(self, *, execute_time: builtins.str) -> None:
        '''
        :param execute_time: The desired patch job execution time. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#execute_time OsConfigPatchDeployment#execute_time}
        '''
        value = OsConfigPatchDeploymentOneTimeSchedule(execute_time=execute_time)

        return typing.cast(None, jsii.invoke(self, "putOneTimeSchedule", [value]))

    @jsii.member(jsii_name="putPatchConfig")
    def put_patch_config(
        self,
        *,
        apt: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigApt", typing.Dict[builtins.str, typing.Any]]] = None,
        goo: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigGoo", typing.Dict[builtins.str, typing.Any]]] = None,
        mig_instances_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        post_step: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPostStep", typing.Dict[builtins.str, typing.Any]]] = None,
        pre_step: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPreStep", typing.Dict[builtins.str, typing.Any]]] = None,
        reboot_config: typing.Optional[builtins.str] = None,
        windows_update: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigWindowsUpdate", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#apt OsConfigPatchDeployment#apt}
        :param goo: goo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#goo OsConfigPatchDeployment#goo}
        :param mig_instances_allowed: Allows the patch job to run on Managed instance groups (MIGs). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#mig_instances_allowed OsConfigPatchDeployment#mig_instances_allowed}
        :param post_step: post_step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#post_step OsConfigPatchDeployment#post_step}
        :param pre_step: pre_step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#pre_step OsConfigPatchDeployment#pre_step}
        :param reboot_config: Post-patch reboot settings. Possible values: ["DEFAULT", "ALWAYS", "NEVER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#reboot_config OsConfigPatchDeployment#reboot_config}
        :param windows_update: windows_update block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#windows_update OsConfigPatchDeployment#windows_update}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#yum OsConfigPatchDeployment#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#zypper OsConfigPatchDeployment#zypper}
        '''
        value = OsConfigPatchDeploymentPatchConfig(
            apt=apt,
            goo=goo,
            mig_instances_allowed=mig_instances_allowed,
            post_step=post_step,
            pre_step=pre_step,
            reboot_config=reboot_config,
            windows_update=windows_update,
            yum=yum,
            zypper=zypper,
        )

        return typing.cast(None, jsii.invoke(self, "putPatchConfig", [value]))

    @jsii.member(jsii_name="putRecurringSchedule")
    def put_recurring_schedule(
        self,
        *,
        time_of_day: typing.Union["OsConfigPatchDeploymentRecurringScheduleTimeOfDay", typing.Dict[builtins.str, typing.Any]],
        time_zone: typing.Union["OsConfigPatchDeploymentRecurringScheduleTimeZone", typing.Dict[builtins.str, typing.Any]],
        end_time: typing.Optional[builtins.str] = None,
        monthly: typing.Optional[typing.Union["OsConfigPatchDeploymentRecurringScheduleMonthly", typing.Dict[builtins.str, typing.Any]]] = None,
        start_time: typing.Optional[builtins.str] = None,
        weekly: typing.Optional[typing.Union["OsConfigPatchDeploymentRecurringScheduleWeekly", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param time_of_day: time_of_day block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#time_of_day OsConfigPatchDeployment#time_of_day}
        :param time_zone: time_zone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#time_zone OsConfigPatchDeployment#time_zone}
        :param end_time: The end time at which a recurring patch deployment schedule is no longer active. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#end_time OsConfigPatchDeployment#end_time}
        :param monthly: monthly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#monthly OsConfigPatchDeployment#monthly}
        :param start_time: The time that the recurring schedule becomes effective. Defaults to createTime of the patch deployment. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#start_time OsConfigPatchDeployment#start_time}
        :param weekly: weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#weekly OsConfigPatchDeployment#weekly}
        '''
        value = OsConfigPatchDeploymentRecurringSchedule(
            time_of_day=time_of_day,
            time_zone=time_zone,
            end_time=end_time,
            monthly=monthly,
            start_time=start_time,
            weekly=weekly,
        )

        return typing.cast(None, jsii.invoke(self, "putRecurringSchedule", [value]))

    @jsii.member(jsii_name="putRollout")
    def put_rollout(
        self,
        *,
        disruption_budget: typing.Union["OsConfigPatchDeploymentRolloutDisruptionBudget", typing.Dict[builtins.str, typing.Any]],
        mode: builtins.str,
    ) -> None:
        '''
        :param disruption_budget: disruption_budget block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#disruption_budget OsConfigPatchDeployment#disruption_budget}
        :param mode: Mode of the patch rollout. Possible values: ["ZONE_BY_ZONE", "CONCURRENT_ZONES"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#mode OsConfigPatchDeployment#mode}
        '''
        value = OsConfigPatchDeploymentRollout(
            disruption_budget=disruption_budget, mode=mode
        )

        return typing.cast(None, jsii.invoke(self, "putRollout", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#create OsConfigPatchDeployment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#delete OsConfigPatchDeployment#delete}.
        '''
        value = OsConfigPatchDeploymentTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDuration")
    def reset_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOneTimeSchedule")
    def reset_one_time_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOneTimeSchedule", []))

    @jsii.member(jsii_name="resetPatchConfig")
    def reset_patch_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPatchConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRecurringSchedule")
    def reset_recurring_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurringSchedule", []))

    @jsii.member(jsii_name="resetRollout")
    def reset_rollout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRollout", []))

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
    @jsii.member(jsii_name="instanceFilter")
    def instance_filter(self) -> "OsConfigPatchDeploymentInstanceFilterOutputReference":
        return typing.cast("OsConfigPatchDeploymentInstanceFilterOutputReference", jsii.get(self, "instanceFilter"))

    @builtins.property
    @jsii.member(jsii_name="lastExecuteTime")
    def last_execute_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastExecuteTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="oneTimeSchedule")
    def one_time_schedule(
        self,
    ) -> "OsConfigPatchDeploymentOneTimeScheduleOutputReference":
        return typing.cast("OsConfigPatchDeploymentOneTimeScheduleOutputReference", jsii.get(self, "oneTimeSchedule"))

    @builtins.property
    @jsii.member(jsii_name="patchConfig")
    def patch_config(self) -> "OsConfigPatchDeploymentPatchConfigOutputReference":
        return typing.cast("OsConfigPatchDeploymentPatchConfigOutputReference", jsii.get(self, "patchConfig"))

    @builtins.property
    @jsii.member(jsii_name="recurringSchedule")
    def recurring_schedule(
        self,
    ) -> "OsConfigPatchDeploymentRecurringScheduleOutputReference":
        return typing.cast("OsConfigPatchDeploymentRecurringScheduleOutputReference", jsii.get(self, "recurringSchedule"))

    @builtins.property
    @jsii.member(jsii_name="rollout")
    def rollout(self) -> "OsConfigPatchDeploymentRolloutOutputReference":
        return typing.cast("OsConfigPatchDeploymentRolloutOutputReference", jsii.get(self, "rollout"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "OsConfigPatchDeploymentTimeoutsOutputReference":
        return typing.cast("OsConfigPatchDeploymentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceFilterInput")
    def instance_filter_input(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentInstanceFilter"]:
        return typing.cast(typing.Optional["OsConfigPatchDeploymentInstanceFilter"], jsii.get(self, "instanceFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="oneTimeScheduleInput")
    def one_time_schedule_input(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentOneTimeSchedule"]:
        return typing.cast(typing.Optional["OsConfigPatchDeploymentOneTimeSchedule"], jsii.get(self, "oneTimeScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="patchConfigInput")
    def patch_config_input(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentPatchConfig"]:
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfig"], jsii.get(self, "patchConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="patchDeploymentIdInput")
    def patch_deployment_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patchDeploymentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="recurringScheduleInput")
    def recurring_schedule_input(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentRecurringSchedule"]:
        return typing.cast(typing.Optional["OsConfigPatchDeploymentRecurringSchedule"], jsii.get(self, "recurringScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="rolloutInput")
    def rollout_input(self) -> typing.Optional["OsConfigPatchDeploymentRollout"]:
        return typing.cast(typing.Optional["OsConfigPatchDeploymentRollout"], jsii.get(self, "rolloutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OsConfigPatchDeploymentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OsConfigPatchDeploymentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a79eb875b5eddd55022dfaef75ef0b133f2863140f903b57982b654ad58edcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8bb25ac71c9ccd6715342eaa22fd0fae143a6a521c62db5abb7186debbfda80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c2bf16d0de8cfdc0eb7340912516c71f07db29a4c39c49b42c843580ca683b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="patchDeploymentId")
    def patch_deployment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "patchDeploymentId"))

    @patch_deployment_id.setter
    def patch_deployment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88658321593b9d4e0ba646a9e0c715a0bd30b5f8227e24d0687f42aa9a5c2521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "patchDeploymentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7601cf0772e60ef2af7b011222a3e080fd26eb01407b0cd9aeb151d46a13085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "instance_filter": "instanceFilter",
        "patch_deployment_id": "patchDeploymentId",
        "description": "description",
        "duration": "duration",
        "id": "id",
        "one_time_schedule": "oneTimeSchedule",
        "patch_config": "patchConfig",
        "project": "project",
        "recurring_schedule": "recurringSchedule",
        "rollout": "rollout",
        "timeouts": "timeouts",
    },
)
class OsConfigPatchDeploymentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        instance_filter: typing.Union["OsConfigPatchDeploymentInstanceFilter", typing.Dict[builtins.str, typing.Any]],
        patch_deployment_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        duration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        one_time_schedule: typing.Optional[typing.Union["OsConfigPatchDeploymentOneTimeSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        patch_config: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        recurring_schedule: typing.Optional[typing.Union["OsConfigPatchDeploymentRecurringSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        rollout: typing.Optional[typing.Union["OsConfigPatchDeploymentRollout", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["OsConfigPatchDeploymentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param instance_filter: instance_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#instance_filter OsConfigPatchDeployment#instance_filter}
        :param patch_deployment_id: A name for the patch deployment in the project. When creating a name the following rules apply: - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#patch_deployment_id OsConfigPatchDeployment#patch_deployment_id}
        :param description: Description of the patch deployment. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#description OsConfigPatchDeployment#description}
        :param duration: Duration of the patch. After the duration ends, the patch times out. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#duration OsConfigPatchDeployment#duration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#id OsConfigPatchDeployment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param one_time_schedule: one_time_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#one_time_schedule OsConfigPatchDeployment#one_time_schedule}
        :param patch_config: patch_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#patch_config OsConfigPatchDeployment#patch_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#project OsConfigPatchDeployment#project}.
        :param recurring_schedule: recurring_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#recurring_schedule OsConfigPatchDeployment#recurring_schedule}
        :param rollout: rollout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#rollout OsConfigPatchDeployment#rollout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#timeouts OsConfigPatchDeployment#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(instance_filter, dict):
            instance_filter = OsConfigPatchDeploymentInstanceFilter(**instance_filter)
        if isinstance(one_time_schedule, dict):
            one_time_schedule = OsConfigPatchDeploymentOneTimeSchedule(**one_time_schedule)
        if isinstance(patch_config, dict):
            patch_config = OsConfigPatchDeploymentPatchConfig(**patch_config)
        if isinstance(recurring_schedule, dict):
            recurring_schedule = OsConfigPatchDeploymentRecurringSchedule(**recurring_schedule)
        if isinstance(rollout, dict):
            rollout = OsConfigPatchDeploymentRollout(**rollout)
        if isinstance(timeouts, dict):
            timeouts = OsConfigPatchDeploymentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6efb0b2adcf625fce1e74b0093d770ab7f7e24f4efdc4632378cb7203471985c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument instance_filter", value=instance_filter, expected_type=type_hints["instance_filter"])
            check_type(argname="argument patch_deployment_id", value=patch_deployment_id, expected_type=type_hints["patch_deployment_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument one_time_schedule", value=one_time_schedule, expected_type=type_hints["one_time_schedule"])
            check_type(argname="argument patch_config", value=patch_config, expected_type=type_hints["patch_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument recurring_schedule", value=recurring_schedule, expected_type=type_hints["recurring_schedule"])
            check_type(argname="argument rollout", value=rollout, expected_type=type_hints["rollout"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_filter": instance_filter,
            "patch_deployment_id": patch_deployment_id,
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
        if duration is not None:
            self._values["duration"] = duration
        if id is not None:
            self._values["id"] = id
        if one_time_schedule is not None:
            self._values["one_time_schedule"] = one_time_schedule
        if patch_config is not None:
            self._values["patch_config"] = patch_config
        if project is not None:
            self._values["project"] = project
        if recurring_schedule is not None:
            self._values["recurring_schedule"] = recurring_schedule
        if rollout is not None:
            self._values["rollout"] = rollout
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
    def instance_filter(self) -> "OsConfigPatchDeploymentInstanceFilter":
        '''instance_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#instance_filter OsConfigPatchDeployment#instance_filter}
        '''
        result = self._values.get("instance_filter")
        assert result is not None, "Required property 'instance_filter' is missing"
        return typing.cast("OsConfigPatchDeploymentInstanceFilter", result)

    @builtins.property
    def patch_deployment_id(self) -> builtins.str:
        '''A name for the patch deployment in the project.

        When creating a name the following rules apply:

        - Must contain only lowercase letters, numbers, and hyphens.
        - Must start with a letter.
        - Must be between 1-63 characters.
        - Must end with a number or a letter.
        - Must be unique within the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#patch_deployment_id OsConfigPatchDeployment#patch_deployment_id}
        '''
        result = self._values.get("patch_deployment_id")
        assert result is not None, "Required property 'patch_deployment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the patch deployment. Length of the description is limited to 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#description OsConfigPatchDeployment#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def duration(self) -> typing.Optional[builtins.str]:
        '''Duration of the patch.

        After the duration ends, the patch times out.
        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#duration OsConfigPatchDeployment#duration}
        '''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#id OsConfigPatchDeployment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def one_time_schedule(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentOneTimeSchedule"]:
        '''one_time_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#one_time_schedule OsConfigPatchDeployment#one_time_schedule}
        '''
        result = self._values.get("one_time_schedule")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentOneTimeSchedule"], result)

    @builtins.property
    def patch_config(self) -> typing.Optional["OsConfigPatchDeploymentPatchConfig"]:
        '''patch_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#patch_config OsConfigPatchDeployment#patch_config}
        '''
        result = self._values.get("patch_config")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#project OsConfigPatchDeployment#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recurring_schedule(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentRecurringSchedule"]:
        '''recurring_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#recurring_schedule OsConfigPatchDeployment#recurring_schedule}
        '''
        result = self._values.get("recurring_schedule")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentRecurringSchedule"], result)

    @builtins.property
    def rollout(self) -> typing.Optional["OsConfigPatchDeploymentRollout"]:
        '''rollout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#rollout OsConfigPatchDeployment#rollout}
        '''
        result = self._values.get("rollout")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentRollout"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["OsConfigPatchDeploymentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#timeouts OsConfigPatchDeployment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentInstanceFilter",
    jsii_struct_bases=[],
    name_mapping={
        "all": "all",
        "group_labels": "groupLabels",
        "instance_name_prefixes": "instanceNamePrefixes",
        "instances": "instances",
        "zones": "zones",
    },
)
class OsConfigPatchDeploymentInstanceFilter:
    def __init__(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigPatchDeploymentInstanceFilterGroupLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        instance_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param all: Target all VM instances in the project. If true, no other criteria is permitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#all OsConfigPatchDeployment#all}
        :param group_labels: group_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#group_labels OsConfigPatchDeployment#group_labels}
        :param instance_name_prefixes: Targets VMs whose name starts with one of these prefixes. Similar to labels, this is another way to group VMs when targeting configs, for example prefix="prod-". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#instance_name_prefixes OsConfigPatchDeployment#instance_name_prefixes}
        :param instances: Targets any of the VM instances specified. Instances are specified by their URI in the 'form zones/{{zone}}/instances/{{instance_name}}', 'projects/{{project_id}}/zones/{{zone}}/instances/{{instance_name}}', or 'https://www.googleapis.com/compute/v1/projects/{{project_id}}/zones/{{zone}}/instances/{{instance_name}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#instances OsConfigPatchDeployment#instances}
        :param zones: Targets VM instances in ANY of these zones. Leave empty to target VM instances in any zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#zones OsConfigPatchDeployment#zones}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643761843ed240dce48982d376cdd4eb89781c7e0d2bc366f5b9770032bd6d32)
            check_type(argname="argument all", value=all, expected_type=type_hints["all"])
            check_type(argname="argument group_labels", value=group_labels, expected_type=type_hints["group_labels"])
            check_type(argname="argument instance_name_prefixes", value=instance_name_prefixes, expected_type=type_hints["instance_name_prefixes"])
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
            check_type(argname="argument zones", value=zones, expected_type=type_hints["zones"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all is not None:
            self._values["all"] = all
        if group_labels is not None:
            self._values["group_labels"] = group_labels
        if instance_name_prefixes is not None:
            self._values["instance_name_prefixes"] = instance_name_prefixes
        if instances is not None:
            self._values["instances"] = instances
        if zones is not None:
            self._values["zones"] = zones

    @builtins.property
    def all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Target all VM instances in the project. If true, no other criteria is permitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#all OsConfigPatchDeployment#all}
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def group_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigPatchDeploymentInstanceFilterGroupLabels"]]]:
        '''group_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#group_labels OsConfigPatchDeployment#group_labels}
        '''
        result = self._values.get("group_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigPatchDeploymentInstanceFilterGroupLabels"]]], result)

    @builtins.property
    def instance_name_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Targets VMs whose name starts with one of these prefixes.

        Similar to labels, this is another way to group
        VMs when targeting configs, for example prefix="prod-".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#instance_name_prefixes OsConfigPatchDeployment#instance_name_prefixes}
        '''
        result = self._values.get("instance_name_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def instances(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Targets any of the VM instances specified. Instances are specified by their URI in the 'form zones/{{zone}}/instances/{{instance_name}}', 'projects/{{project_id}}/zones/{{zone}}/instances/{{instance_name}}', or 'https://www.googleapis.com/compute/v1/projects/{{project_id}}/zones/{{zone}}/instances/{{instance_name}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#instances OsConfigPatchDeployment#instances}
        '''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Targets VM instances in ANY of these zones. Leave empty to target VM instances in any zone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#zones OsConfigPatchDeployment#zones}
        '''
        result = self._values.get("zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentInstanceFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentInstanceFilterGroupLabels",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels"},
)
class OsConfigPatchDeploymentInstanceFilterGroupLabels:
    def __init__(self, *, labels: typing.Mapping[builtins.str, builtins.str]) -> None:
        '''
        :param labels: Compute Engine instance labels that must be present for a VM instance to be targeted by this filter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#labels OsConfigPatchDeployment#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a1d228bda81d279106aef70d2e69ccb5bac2105841dbb3d5241a2ea5579939)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "labels": labels,
        }

    @builtins.property
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Compute Engine instance labels that must be present for a VM instance to be targeted by this filter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#labels OsConfigPatchDeployment#labels}
        '''
        result = self._values.get("labels")
        assert result is not None, "Required property 'labels' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentInstanceFilterGroupLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentInstanceFilterGroupLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentInstanceFilterGroupLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfd9e6c32b248832554544eb3978cdb5b1a92eedcde14c44e22be8f8f432ea57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigPatchDeploymentInstanceFilterGroupLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7830fe07de60efe12f7751df7a054b11f1feefd84d8a69ac93ddba7160a603)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigPatchDeploymentInstanceFilterGroupLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e6a443de228257746ec543fd3635340836a226b6fe8dd258e80e96b5a04eceb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f27909db9958713211a73fc64fd0f58619d6ec4d5c00b5d163afcd33a0c09112)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b202679fff2ceaae9123bde2ed8e9b4f5dd54848c5c78ede885f38a9a430f7da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigPatchDeploymentInstanceFilterGroupLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigPatchDeploymentInstanceFilterGroupLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigPatchDeploymentInstanceFilterGroupLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f91815ca685d813e0cb90d033667c9e6c465f06ecb8b5ef26a8ef985457bb44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigPatchDeploymentInstanceFilterGroupLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentInstanceFilterGroupLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d95eca9229d83ac8505d17c5eddb062e341278bffcc6d14c46232264bacac1c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c43fac9ff0cb4d8e5ed2b8bcd3e10383ba5a8f422b1e796aa95b1af4a89d46fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigPatchDeploymentInstanceFilterGroupLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigPatchDeploymentInstanceFilterGroupLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigPatchDeploymentInstanceFilterGroupLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e6b2bf4bb31cd734bb22178ebf793d19f14c16e9a7cc76fb6a13b474e1586c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigPatchDeploymentInstanceFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentInstanceFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fb82a21735f0f639961df306ca7d25576dd3cd481c03898af4ff98bccb489af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGroupLabels")
    def put_group_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigPatchDeploymentInstanceFilterGroupLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bea60b351c5afff7271c36be730ca7f43f71ac040a8978943f30aa78716ccf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGroupLabels", [value]))

    @jsii.member(jsii_name="resetAll")
    def reset_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAll", []))

    @jsii.member(jsii_name="resetGroupLabels")
    def reset_group_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupLabels", []))

    @jsii.member(jsii_name="resetInstanceNamePrefixes")
    def reset_instance_name_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceNamePrefixes", []))

    @jsii.member(jsii_name="resetInstances")
    def reset_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstances", []))

    @jsii.member(jsii_name="resetZones")
    def reset_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZones", []))

    @builtins.property
    @jsii.member(jsii_name="groupLabels")
    def group_labels(self) -> OsConfigPatchDeploymentInstanceFilterGroupLabelsList:
        return typing.cast(OsConfigPatchDeploymentInstanceFilterGroupLabelsList, jsii.get(self, "groupLabels"))

    @builtins.property
    @jsii.member(jsii_name="allInput")
    def all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allInput"))

    @builtins.property
    @jsii.member(jsii_name="groupLabelsInput")
    def group_labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigPatchDeploymentInstanceFilterGroupLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigPatchDeploymentInstanceFilterGroupLabels]]], jsii.get(self, "groupLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceNamePrefixesInput")
    def instance_name_prefixes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "instanceNamePrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="instancesInput")
    def instances_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "instancesInput"))

    @builtins.property
    @jsii.member(jsii_name="zonesInput")
    def zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "zonesInput"))

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "all"))

    @all.setter
    def all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__814bd8c0dc74f44e9758df2a1041228951986f5ef52a75857f7a883f2f4956b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceNamePrefixes")
    def instance_name_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceNamePrefixes"))

    @instance_name_prefixes.setter
    def instance_name_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfd712a76b354cb628c71dfdc61c1a6fcdf95b893f69dedaa179e46eaa0eb1fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceNamePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instances")
    def instances(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instances"))

    @instances.setter
    def instances(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d6b83cf63a10346ceec2e9d42319c5dba20c5d88728a77b7d923f4b6451b7a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "zones"))

    @zones.setter
    def zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ef2c09be8c396a531d432e9549d31f419a463ee673bc18f99fbc4b881396c61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OsConfigPatchDeploymentInstanceFilter]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentInstanceFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentInstanceFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__432feb539c619cb2680e4ed04f061d57818fcbe8cf368edbbf01247ac5527696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentOneTimeSchedule",
    jsii_struct_bases=[],
    name_mapping={"execute_time": "executeTime"},
)
class OsConfigPatchDeploymentOneTimeSchedule:
    def __init__(self, *, execute_time: builtins.str) -> None:
        '''
        :param execute_time: The desired patch job execution time. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#execute_time OsConfigPatchDeployment#execute_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9dbe85b65c0d561045f6a544540ed306de4feae8d20a70a336202f18fea9c1d)
            check_type(argname="argument execute_time", value=execute_time, expected_type=type_hints["execute_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execute_time": execute_time,
        }

    @builtins.property
    def execute_time(self) -> builtins.str:
        '''The desired patch job execution time. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#execute_time OsConfigPatchDeployment#execute_time}
        '''
        result = self._values.get("execute_time")
        assert result is not None, "Required property 'execute_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentOneTimeSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentOneTimeScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentOneTimeScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3da09f03f27e66efc1ff4801da5acd312348b4d15316968b54ba57f24a5d796)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="executeTimeInput")
    def execute_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executeTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="executeTime")
    def execute_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executeTime"))

    @execute_time.setter
    def execute_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f0379ae4b174467af47bf0116f537540e512f1efb3a133caf75aa44eba1ee9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executeTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OsConfigPatchDeploymentOneTimeSchedule]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentOneTimeSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentOneTimeSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a55549f359f2533bc2e5f91e969f0e323ad88e87cae9d6072ae9f2b1cf8c10e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfig",
    jsii_struct_bases=[],
    name_mapping={
        "apt": "apt",
        "goo": "goo",
        "mig_instances_allowed": "migInstancesAllowed",
        "post_step": "postStep",
        "pre_step": "preStep",
        "reboot_config": "rebootConfig",
        "windows_update": "windowsUpdate",
        "yum": "yum",
        "zypper": "zypper",
    },
)
class OsConfigPatchDeploymentPatchConfig:
    def __init__(
        self,
        *,
        apt: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigApt", typing.Dict[builtins.str, typing.Any]]] = None,
        goo: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigGoo", typing.Dict[builtins.str, typing.Any]]] = None,
        mig_instances_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        post_step: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPostStep", typing.Dict[builtins.str, typing.Any]]] = None,
        pre_step: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPreStep", typing.Dict[builtins.str, typing.Any]]] = None,
        reboot_config: typing.Optional[builtins.str] = None,
        windows_update: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigWindowsUpdate", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#apt OsConfigPatchDeployment#apt}
        :param goo: goo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#goo OsConfigPatchDeployment#goo}
        :param mig_instances_allowed: Allows the patch job to run on Managed instance groups (MIGs). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#mig_instances_allowed OsConfigPatchDeployment#mig_instances_allowed}
        :param post_step: post_step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#post_step OsConfigPatchDeployment#post_step}
        :param pre_step: pre_step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#pre_step OsConfigPatchDeployment#pre_step}
        :param reboot_config: Post-patch reboot settings. Possible values: ["DEFAULT", "ALWAYS", "NEVER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#reboot_config OsConfigPatchDeployment#reboot_config}
        :param windows_update: windows_update block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#windows_update OsConfigPatchDeployment#windows_update}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#yum OsConfigPatchDeployment#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#zypper OsConfigPatchDeployment#zypper}
        '''
        if isinstance(apt, dict):
            apt = OsConfigPatchDeploymentPatchConfigApt(**apt)
        if isinstance(goo, dict):
            goo = OsConfigPatchDeploymentPatchConfigGoo(**goo)
        if isinstance(post_step, dict):
            post_step = OsConfigPatchDeploymentPatchConfigPostStep(**post_step)
        if isinstance(pre_step, dict):
            pre_step = OsConfigPatchDeploymentPatchConfigPreStep(**pre_step)
        if isinstance(windows_update, dict):
            windows_update = OsConfigPatchDeploymentPatchConfigWindowsUpdate(**windows_update)
        if isinstance(yum, dict):
            yum = OsConfigPatchDeploymentPatchConfigYum(**yum)
        if isinstance(zypper, dict):
            zypper = OsConfigPatchDeploymentPatchConfigZypper(**zypper)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ddcbb161eb21d7c13581851bcbfd5c04c0eb7eb1b3775d41ac0ebae208d292)
            check_type(argname="argument apt", value=apt, expected_type=type_hints["apt"])
            check_type(argname="argument goo", value=goo, expected_type=type_hints["goo"])
            check_type(argname="argument mig_instances_allowed", value=mig_instances_allowed, expected_type=type_hints["mig_instances_allowed"])
            check_type(argname="argument post_step", value=post_step, expected_type=type_hints["post_step"])
            check_type(argname="argument pre_step", value=pre_step, expected_type=type_hints["pre_step"])
            check_type(argname="argument reboot_config", value=reboot_config, expected_type=type_hints["reboot_config"])
            check_type(argname="argument windows_update", value=windows_update, expected_type=type_hints["windows_update"])
            check_type(argname="argument yum", value=yum, expected_type=type_hints["yum"])
            check_type(argname="argument zypper", value=zypper, expected_type=type_hints["zypper"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if apt is not None:
            self._values["apt"] = apt
        if goo is not None:
            self._values["goo"] = goo
        if mig_instances_allowed is not None:
            self._values["mig_instances_allowed"] = mig_instances_allowed
        if post_step is not None:
            self._values["post_step"] = post_step
        if pre_step is not None:
            self._values["pre_step"] = pre_step
        if reboot_config is not None:
            self._values["reboot_config"] = reboot_config
        if windows_update is not None:
            self._values["windows_update"] = windows_update
        if yum is not None:
            self._values["yum"] = yum
        if zypper is not None:
            self._values["zypper"] = zypper

    @builtins.property
    def apt(self) -> typing.Optional["OsConfigPatchDeploymentPatchConfigApt"]:
        '''apt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#apt OsConfigPatchDeployment#apt}
        '''
        result = self._values.get("apt")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigApt"], result)

    @builtins.property
    def goo(self) -> typing.Optional["OsConfigPatchDeploymentPatchConfigGoo"]:
        '''goo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#goo OsConfigPatchDeployment#goo}
        '''
        result = self._values.get("goo")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigGoo"], result)

    @builtins.property
    def mig_instances_allowed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows the patch job to run on Managed instance groups (MIGs).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#mig_instances_allowed OsConfigPatchDeployment#mig_instances_allowed}
        '''
        result = self._values.get("mig_instances_allowed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def post_step(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentPatchConfigPostStep"]:
        '''post_step block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#post_step OsConfigPatchDeployment#post_step}
        '''
        result = self._values.get("post_step")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigPostStep"], result)

    @builtins.property
    def pre_step(self) -> typing.Optional["OsConfigPatchDeploymentPatchConfigPreStep"]:
        '''pre_step block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#pre_step OsConfigPatchDeployment#pre_step}
        '''
        result = self._values.get("pre_step")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigPreStep"], result)

    @builtins.property
    def reboot_config(self) -> typing.Optional[builtins.str]:
        '''Post-patch reboot settings. Possible values: ["DEFAULT", "ALWAYS", "NEVER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#reboot_config OsConfigPatchDeployment#reboot_config}
        '''
        result = self._values.get("reboot_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def windows_update(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentPatchConfigWindowsUpdate"]:
        '''windows_update block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#windows_update OsConfigPatchDeployment#windows_update}
        '''
        result = self._values.get("windows_update")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigWindowsUpdate"], result)

    @builtins.property
    def yum(self) -> typing.Optional["OsConfigPatchDeploymentPatchConfigYum"]:
        '''yum block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#yum OsConfigPatchDeployment#yum}
        '''
        result = self._values.get("yum")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigYum"], result)

    @builtins.property
    def zypper(self) -> typing.Optional["OsConfigPatchDeploymentPatchConfigZypper"]:
        '''zypper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#zypper OsConfigPatchDeployment#zypper}
        '''
        result = self._values.get("zypper")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigZypper"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentPatchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigApt",
    jsii_struct_bases=[],
    name_mapping={
        "excludes": "excludes",
        "exclusive_packages": "exclusivePackages",
        "type": "type",
    },
)
class OsConfigPatchDeploymentPatchConfigApt:
    def __init__(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclusive_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param excludes: List of packages to exclude from update. These packages will be excluded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#excludes OsConfigPatchDeployment#excludes}
        :param exclusive_packages: An exclusive list of packages to be updated. These are the only packages that will be updated. If these packages are not installed, they will be ignored. This field cannot be specified with any other patch configuration fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#exclusive_packages OsConfigPatchDeployment#exclusive_packages}
        :param type: By changing the type to DIST, the patching is performed using apt-get dist-upgrade instead. Possible values: ["DIST", "UPGRADE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#type OsConfigPatchDeployment#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11255c0d071c1b7cd27fd0938b2106edda776a3cbb23c96f884b7f9540c9158e)
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument exclusive_packages", value=exclusive_packages, expected_type=type_hints["exclusive_packages"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excludes is not None:
            self._values["excludes"] = excludes
        if exclusive_packages is not None:
            self._values["exclusive_packages"] = exclusive_packages
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of packages to exclude from update. These packages will be excluded.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#excludes OsConfigPatchDeployment#excludes}
        '''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclusive_packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An exclusive list of packages to be updated.

        These are the only packages that will be updated.
        If these packages are not installed, they will be ignored. This field cannot be specified with
        any other patch configuration fields.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#exclusive_packages OsConfigPatchDeployment#exclusive_packages}
        '''
        result = self._values.get("exclusive_packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''By changing the type to DIST, the patching is performed using apt-get dist-upgrade instead. Possible values: ["DIST", "UPGRADE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#type OsConfigPatchDeployment#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentPatchConfigApt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentPatchConfigAptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigAptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef4b29da9ed6942268a1d3fe70db35d287e62aec29c072af11752ec287dc050b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludes")
    def reset_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludes", []))

    @jsii.member(jsii_name="resetExclusivePackages")
    def reset_exclusive_packages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusivePackages", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="excludesInput")
    def excludes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludesInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusivePackagesInput")
    def exclusive_packages_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exclusivePackagesInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludes"))

    @excludes.setter
    def excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9157649bef42030157398392ec0ad5f0ad6d3a17b739d1ed877fdf7561ef86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusivePackages")
    def exclusive_packages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusivePackages"))

    @exclusive_packages.setter
    def exclusive_packages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca82a1f19e0245412b515f66bb41ee48ef86abb2b25dcb5c7eb8b1f8420cd4c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusivePackages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a8d49191a36f5eece0c481dab76078069bbd456edb569399c4fa0c75a98c93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OsConfigPatchDeploymentPatchConfigApt]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigApt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentPatchConfigApt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80968c8924fa5d215051fd6536260477c1a73f2a56f0d75f4a17eaf764f8f8f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigGoo",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class OsConfigPatchDeploymentPatchConfigGoo:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: goo update settings. Use this setting to override the default goo patch rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#enabled OsConfigPatchDeployment#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9321de7c7730696f9408f19bfa409b27d9de3d644c2e6f9156606a7458fa7d9f)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''goo update settings. Use this setting to override the default goo patch rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#enabled OsConfigPatchDeployment#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentPatchConfigGoo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentPatchConfigGooOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigGooOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32c594a83b91a91924c498b3d7bc2588ce9a1f74caf6e61d00f72fc70ef6745d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__dc69e4378f0139732675532ceb7f9e66b15e80b4240877bca00c6a62f08bd11a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OsConfigPatchDeploymentPatchConfigGoo]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigGoo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentPatchConfigGoo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6543491fca539d077b56937454721dd8ff0e6a1506807373f38b88f240e00910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigPatchDeploymentPatchConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3845e42500292db065fab65d375aab2379b2e02285071dd3f88833c10baa7a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApt")
    def put_apt(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclusive_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param excludes: List of packages to exclude from update. These packages will be excluded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#excludes OsConfigPatchDeployment#excludes}
        :param exclusive_packages: An exclusive list of packages to be updated. These are the only packages that will be updated. If these packages are not installed, they will be ignored. This field cannot be specified with any other patch configuration fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#exclusive_packages OsConfigPatchDeployment#exclusive_packages}
        :param type: By changing the type to DIST, the patching is performed using apt-get dist-upgrade instead. Possible values: ["DIST", "UPGRADE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#type OsConfigPatchDeployment#type}
        '''
        value = OsConfigPatchDeploymentPatchConfigApt(
            excludes=excludes, exclusive_packages=exclusive_packages, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putApt", [value]))

    @jsii.member(jsii_name="putGoo")
    def put_goo(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: goo update settings. Use this setting to override the default goo patch rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#enabled OsConfigPatchDeployment#enabled}
        '''
        value = OsConfigPatchDeploymentPatchConfigGoo(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putGoo", [value]))

    @jsii.member(jsii_name="putPostStep")
    def put_post_step(
        self,
        *,
        linux_exec_step_config: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        windows_exec_step_config: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param linux_exec_step_config: linux_exec_step_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#linux_exec_step_config OsConfigPatchDeployment#linux_exec_step_config}
        :param windows_exec_step_config: windows_exec_step_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#windows_exec_step_config OsConfigPatchDeployment#windows_exec_step_config}
        '''
        value = OsConfigPatchDeploymentPatchConfigPostStep(
            linux_exec_step_config=linux_exec_step_config,
            windows_exec_step_config=windows_exec_step_config,
        )

        return typing.cast(None, jsii.invoke(self, "putPostStep", [value]))

    @jsii.member(jsii_name="putPreStep")
    def put_pre_step(
        self,
        *,
        linux_exec_step_config: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        windows_exec_step_config: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param linux_exec_step_config: linux_exec_step_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#linux_exec_step_config OsConfigPatchDeployment#linux_exec_step_config}
        :param windows_exec_step_config: windows_exec_step_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#windows_exec_step_config OsConfigPatchDeployment#windows_exec_step_config}
        '''
        value = OsConfigPatchDeploymentPatchConfigPreStep(
            linux_exec_step_config=linux_exec_step_config,
            windows_exec_step_config=windows_exec_step_config,
        )

        return typing.cast(None, jsii.invoke(self, "putPreStep", [value]))

    @jsii.member(jsii_name="putWindowsUpdate")
    def put_windows_update(
        self,
        *,
        classifications: typing.Optional[typing.Sequence[builtins.str]] = None,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclusive_patches: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param classifications: Only apply updates of these windows update classifications. If empty, all updates are applied. Possible values: ["CRITICAL", "SECURITY", "DEFINITION", "DRIVER", "FEATURE_PACK", "SERVICE_PACK", "TOOL", "UPDATE_ROLLUP", "UPDATE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#classifications OsConfigPatchDeployment#classifications}
        :param excludes: List of KBs to exclude from update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#excludes OsConfigPatchDeployment#excludes}
        :param exclusive_patches: An exclusive list of kbs to be updated. These are the only patches that will be updated. This field must not be used with other patch configurations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#exclusive_patches OsConfigPatchDeployment#exclusive_patches}
        '''
        value = OsConfigPatchDeploymentPatchConfigWindowsUpdate(
            classifications=classifications,
            excludes=excludes,
            exclusive_patches=exclusive_patches,
        )

        return typing.cast(None, jsii.invoke(self, "putWindowsUpdate", [value]))

    @jsii.member(jsii_name="putYum")
    def put_yum(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclusive_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        minimal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param excludes: List of packages to exclude from update. These packages will be excluded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#excludes OsConfigPatchDeployment#excludes}
        :param exclusive_packages: An exclusive list of packages to be updated. These are the only packages that will be updated. If these packages are not installed, they will be ignored. This field cannot be specified with any other patch configuration fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#exclusive_packages OsConfigPatchDeployment#exclusive_packages}
        :param minimal: Will cause patch to run yum update-minimal instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#minimal OsConfigPatchDeployment#minimal}
        :param security: Adds the --security flag to yum update. Not supported on all platforms. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#security OsConfigPatchDeployment#security}
        '''
        value = OsConfigPatchDeploymentPatchConfigYum(
            excludes=excludes,
            exclusive_packages=exclusive_packages,
            minimal=minimal,
            security=security,
        )

        return typing.cast(None, jsii.invoke(self, "putYum", [value]))

    @jsii.member(jsii_name="putZypper")
    def put_zypper(
        self,
        *,
        categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclusive_patches: typing.Optional[typing.Sequence[builtins.str]] = None,
        severities: typing.Optional[typing.Sequence[builtins.str]] = None,
        with_optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        with_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param categories: Install only patches with these categories. Common categories include security, recommended, and feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#categories OsConfigPatchDeployment#categories}
        :param excludes: List of packages to exclude from update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#excludes OsConfigPatchDeployment#excludes}
        :param exclusive_patches: An exclusive list of patches to be updated. These are the only patches that will be installed using 'zypper patch patch:' command. This field must not be used with any other patch configuration fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#exclusive_patches OsConfigPatchDeployment#exclusive_patches}
        :param severities: Install only patches with these severities. Common severities include critical, important, moderate, and low. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#severities OsConfigPatchDeployment#severities}
        :param with_optional: Adds the --with-optional flag to zypper patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#with_optional OsConfigPatchDeployment#with_optional}
        :param with_update: Adds the --with-update flag, to zypper patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#with_update OsConfigPatchDeployment#with_update}
        '''
        value = OsConfigPatchDeploymentPatchConfigZypper(
            categories=categories,
            excludes=excludes,
            exclusive_patches=exclusive_patches,
            severities=severities,
            with_optional=with_optional,
            with_update=with_update,
        )

        return typing.cast(None, jsii.invoke(self, "putZypper", [value]))

    @jsii.member(jsii_name="resetApt")
    def reset_apt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApt", []))

    @jsii.member(jsii_name="resetGoo")
    def reset_goo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoo", []))

    @jsii.member(jsii_name="resetMigInstancesAllowed")
    def reset_mig_instances_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMigInstancesAllowed", []))

    @jsii.member(jsii_name="resetPostStep")
    def reset_post_step(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostStep", []))

    @jsii.member(jsii_name="resetPreStep")
    def reset_pre_step(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreStep", []))

    @jsii.member(jsii_name="resetRebootConfig")
    def reset_reboot_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRebootConfig", []))

    @jsii.member(jsii_name="resetWindowsUpdate")
    def reset_windows_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowsUpdate", []))

    @jsii.member(jsii_name="resetYum")
    def reset_yum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYum", []))

    @jsii.member(jsii_name="resetZypper")
    def reset_zypper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZypper", []))

    @builtins.property
    @jsii.member(jsii_name="apt")
    def apt(self) -> OsConfigPatchDeploymentPatchConfigAptOutputReference:
        return typing.cast(OsConfigPatchDeploymentPatchConfigAptOutputReference, jsii.get(self, "apt"))

    @builtins.property
    @jsii.member(jsii_name="goo")
    def goo(self) -> OsConfigPatchDeploymentPatchConfigGooOutputReference:
        return typing.cast(OsConfigPatchDeploymentPatchConfigGooOutputReference, jsii.get(self, "goo"))

    @builtins.property
    @jsii.member(jsii_name="postStep")
    def post_step(self) -> "OsConfigPatchDeploymentPatchConfigPostStepOutputReference":
        return typing.cast("OsConfigPatchDeploymentPatchConfigPostStepOutputReference", jsii.get(self, "postStep"))

    @builtins.property
    @jsii.member(jsii_name="preStep")
    def pre_step(self) -> "OsConfigPatchDeploymentPatchConfigPreStepOutputReference":
        return typing.cast("OsConfigPatchDeploymentPatchConfigPreStepOutputReference", jsii.get(self, "preStep"))

    @builtins.property
    @jsii.member(jsii_name="windowsUpdate")
    def windows_update(
        self,
    ) -> "OsConfigPatchDeploymentPatchConfigWindowsUpdateOutputReference":
        return typing.cast("OsConfigPatchDeploymentPatchConfigWindowsUpdateOutputReference", jsii.get(self, "windowsUpdate"))

    @builtins.property
    @jsii.member(jsii_name="yum")
    def yum(self) -> "OsConfigPatchDeploymentPatchConfigYumOutputReference":
        return typing.cast("OsConfigPatchDeploymentPatchConfigYumOutputReference", jsii.get(self, "yum"))

    @builtins.property
    @jsii.member(jsii_name="zypper")
    def zypper(self) -> "OsConfigPatchDeploymentPatchConfigZypperOutputReference":
        return typing.cast("OsConfigPatchDeploymentPatchConfigZypperOutputReference", jsii.get(self, "zypper"))

    @builtins.property
    @jsii.member(jsii_name="aptInput")
    def apt_input(self) -> typing.Optional[OsConfigPatchDeploymentPatchConfigApt]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigApt], jsii.get(self, "aptInput"))

    @builtins.property
    @jsii.member(jsii_name="gooInput")
    def goo_input(self) -> typing.Optional[OsConfigPatchDeploymentPatchConfigGoo]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigGoo], jsii.get(self, "gooInput"))

    @builtins.property
    @jsii.member(jsii_name="migInstancesAllowedInput")
    def mig_instances_allowed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "migInstancesAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="postStepInput")
    def post_step_input(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentPatchConfigPostStep"]:
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigPostStep"], jsii.get(self, "postStepInput"))

    @builtins.property
    @jsii.member(jsii_name="preStepInput")
    def pre_step_input(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentPatchConfigPreStep"]:
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigPreStep"], jsii.get(self, "preStepInput"))

    @builtins.property
    @jsii.member(jsii_name="rebootConfigInput")
    def reboot_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rebootConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsUpdateInput")
    def windows_update_input(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentPatchConfigWindowsUpdate"]:
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigWindowsUpdate"], jsii.get(self, "windowsUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="yumInput")
    def yum_input(self) -> typing.Optional["OsConfigPatchDeploymentPatchConfigYum"]:
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigYum"], jsii.get(self, "yumInput"))

    @builtins.property
    @jsii.member(jsii_name="zypperInput")
    def zypper_input(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentPatchConfigZypper"]:
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigZypper"], jsii.get(self, "zypperInput"))

    @builtins.property
    @jsii.member(jsii_name="migInstancesAllowed")
    def mig_instances_allowed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "migInstancesAllowed"))

    @mig_instances_allowed.setter
    def mig_instances_allowed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c3aa090438d34940a745aee137dd5a2f40895fad49e08d68b5245cf453b7410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "migInstancesAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rebootConfig")
    def reboot_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rebootConfig"))

    @reboot_config.setter
    def reboot_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862eae0f29edf93f0f8056d7651cc6e559328cbc1890b7e3c862113193144352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rebootConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OsConfigPatchDeploymentPatchConfig]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentPatchConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d2d58999548cf5ae4af8eed0a538d6d7aa71bbea572481471a364a54b4ef2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPostStep",
    jsii_struct_bases=[],
    name_mapping={
        "linux_exec_step_config": "linuxExecStepConfig",
        "windows_exec_step_config": "windowsExecStepConfig",
    },
)
class OsConfigPatchDeploymentPatchConfigPostStep:
    def __init__(
        self,
        *,
        linux_exec_step_config: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        windows_exec_step_config: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param linux_exec_step_config: linux_exec_step_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#linux_exec_step_config OsConfigPatchDeployment#linux_exec_step_config}
        :param windows_exec_step_config: windows_exec_step_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#windows_exec_step_config OsConfigPatchDeployment#windows_exec_step_config}
        '''
        if isinstance(linux_exec_step_config, dict):
            linux_exec_step_config = OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig(**linux_exec_step_config)
        if isinstance(windows_exec_step_config, dict):
            windows_exec_step_config = OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig(**windows_exec_step_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b747341b5aa29940aa4d149f6d2431b9c644319938091470c712157d6eac662)
            check_type(argname="argument linux_exec_step_config", value=linux_exec_step_config, expected_type=type_hints["linux_exec_step_config"])
            check_type(argname="argument windows_exec_step_config", value=windows_exec_step_config, expected_type=type_hints["windows_exec_step_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if linux_exec_step_config is not None:
            self._values["linux_exec_step_config"] = linux_exec_step_config
        if windows_exec_step_config is not None:
            self._values["windows_exec_step_config"] = windows_exec_step_config

    @builtins.property
    def linux_exec_step_config(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig"]:
        '''linux_exec_step_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#linux_exec_step_config OsConfigPatchDeployment#linux_exec_step_config}
        '''
        result = self._values.get("linux_exec_step_config")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig"], result)

    @builtins.property
    def windows_exec_step_config(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig"]:
        '''windows_exec_step_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#windows_exec_step_config OsConfigPatchDeployment#windows_exec_step_config}
        '''
        result = self._values.get("windows_exec_step_config")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentPatchConfigPostStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_success_codes": "allowedSuccessCodes",
        "gcs_object": "gcsObject",
        "interpreter": "interpreter",
        "local_path": "localPath",
    },
)
class OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig:
    def __init__(
        self,
        *,
        allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        gcs_object: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject", typing.Dict[builtins.str, typing.Any]]] = None,
        interpreter: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_success_codes: Defaults to [0]. A list of possible return values that the execution can return to indicate a success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#allowed_success_codes OsConfigPatchDeployment#allowed_success_codes}
        :param gcs_object: gcs_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#gcs_object OsConfigPatchDeployment#gcs_object}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script will be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#interpreter OsConfigPatchDeployment#interpreter}
        :param local_path: An absolute path to the executable on the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#local_path OsConfigPatchDeployment#local_path}
        '''
        if isinstance(gcs_object, dict):
            gcs_object = OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject(**gcs_object)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49cf02daf973a2560fb1c33e6b0da27bca99178661501b7e40d77bc08ca102e9)
            check_type(argname="argument allowed_success_codes", value=allowed_success_codes, expected_type=type_hints["allowed_success_codes"])
            check_type(argname="argument gcs_object", value=gcs_object, expected_type=type_hints["gcs_object"])
            check_type(argname="argument interpreter", value=interpreter, expected_type=type_hints["interpreter"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_success_codes is not None:
            self._values["allowed_success_codes"] = allowed_success_codes
        if gcs_object is not None:
            self._values["gcs_object"] = gcs_object
        if interpreter is not None:
            self._values["interpreter"] = interpreter
        if local_path is not None:
            self._values["local_path"] = local_path

    @builtins.property
    def allowed_success_codes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Defaults to [0]. A list of possible return values that the execution can return to indicate a success.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#allowed_success_codes OsConfigPatchDeployment#allowed_success_codes}
        '''
        result = self._values.get("allowed_success_codes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def gcs_object(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject"]:
        '''gcs_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#gcs_object OsConfigPatchDeployment#gcs_object}
        '''
        result = self._values.get("gcs_object")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject"], result)

    @builtins.property
    def interpreter(self) -> typing.Optional[builtins.str]:
        '''The script interpreter to use to run the script.

        If no interpreter is specified the script will
        be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#interpreter OsConfigPatchDeployment#interpreter}
        '''
        result = self._values.get("interpreter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''An absolute path to the executable on the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#local_path OsConfigPatchDeployment#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "generation_number": "generationNumber",
        "object": "object",
    },
)
class OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        generation_number: builtins.str,
        object: builtins.str,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#bucket OsConfigPatchDeployment#bucket}
        :param generation_number: Generation number of the Cloud Storage object. This is used to ensure that the ExecStep specified by this PatchJob does not change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#generation_number OsConfigPatchDeployment#generation_number}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#object OsConfigPatchDeployment#object}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f096eb0b609678712f2533f34918805a49fbe4813398724bf16947585cf509cc)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument generation_number", value=generation_number, expected_type=type_hints["generation_number"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "generation_number": generation_number,
            "object": object,
        }

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Bucket of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#bucket OsConfigPatchDeployment#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation_number(self) -> builtins.str:
        '''Generation number of the Cloud Storage object.

        This is used to ensure that the ExecStep specified by this PatchJob does not change.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#generation_number OsConfigPatchDeployment#generation_number}
        '''
        result = self._values.get("generation_number")
        assert result is not None, "Required property 'generation_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#object OsConfigPatchDeployment#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b07391f575c91e3a93a60211c5b051e7a70fb00857b8b06287f8ee0aca7a1eb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="generationNumberInput")
    def generation_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "generationNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac031972290e61c228ea00c120c800578ae6df5622e0eaa8f877ed2c697182b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generationNumber")
    def generation_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generationNumber"))

    @generation_number.setter
    def generation_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea0a3cebb5470018ca58c6af5c8153f889b1ea37e6e7971aa911555a769e71c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generationNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__987f86f62096532e2b3e8b9d53e7f8bdf8d1818486fe6bcd23688e848cfc91cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fef46345114b8d603b6deef9b9620427101510645dd13a784aba91c123cbe1df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6b35079d3ca19ed9e2b4da0cde8b5755398415b12ac2717c142da74d93256b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcsObject")
    def put_gcs_object(
        self,
        *,
        bucket: builtins.str,
        generation_number: builtins.str,
        object: builtins.str,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#bucket OsConfigPatchDeployment#bucket}
        :param generation_number: Generation number of the Cloud Storage object. This is used to ensure that the ExecStep specified by this PatchJob does not change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#generation_number OsConfigPatchDeployment#generation_number}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#object OsConfigPatchDeployment#object}
        '''
        value = OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject(
            bucket=bucket, generation_number=generation_number, object=object
        )

        return typing.cast(None, jsii.invoke(self, "putGcsObject", [value]))

    @jsii.member(jsii_name="resetAllowedSuccessCodes")
    def reset_allowed_success_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedSuccessCodes", []))

    @jsii.member(jsii_name="resetGcsObject")
    def reset_gcs_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsObject", []))

    @jsii.member(jsii_name="resetInterpreter")
    def reset_interpreter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterpreter", []))

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @builtins.property
    @jsii.member(jsii_name="gcsObject")
    def gcs_object(
        self,
    ) -> OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObjectOutputReference:
        return typing.cast(OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObjectOutputReference, jsii.get(self, "gcsObject"))

    @builtins.property
    @jsii.member(jsii_name="allowedSuccessCodesInput")
    def allowed_success_codes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "allowedSuccessCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsObjectInput")
    def gcs_object_input(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject], jsii.get(self, "gcsObjectInput"))

    @builtins.property
    @jsii.member(jsii_name="interpreterInput")
    def interpreter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interpreterInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedSuccessCodes")
    def allowed_success_codes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "allowedSuccessCodes"))

    @allowed_success_codes.setter
    def allowed_success_codes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01abafd70d88bf3bad297863de93599e0e528d7841d79aef8cb20066ef8c9264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedSuccessCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa6c3bd1278cb7a5732f15aa506f26cddc07f1a7f631cbc1028a9fb975fb7ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1491b90c429a77e156c69e59977a10df9c5f1172a87cf1cffed4ab198a88c71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a42accbd12d5e00d36a8653a10ab3b6fc3b7be5e8bce7e681e335e65ab55b5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigPatchDeploymentPatchConfigPostStepOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPostStepOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__519d755934909d8dd94403dafa456280fd9af1f22454dbfaa47862c81367ba20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLinuxExecStepConfig")
    def put_linux_exec_step_config(
        self,
        *,
        allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        gcs_object: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject, typing.Dict[builtins.str, typing.Any]]] = None,
        interpreter: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_success_codes: Defaults to [0]. A list of possible return values that the execution can return to indicate a success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#allowed_success_codes OsConfigPatchDeployment#allowed_success_codes}
        :param gcs_object: gcs_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#gcs_object OsConfigPatchDeployment#gcs_object}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script will be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#interpreter OsConfigPatchDeployment#interpreter}
        :param local_path: An absolute path to the executable on the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#local_path OsConfigPatchDeployment#local_path}
        '''
        value = OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig(
            allowed_success_codes=allowed_success_codes,
            gcs_object=gcs_object,
            interpreter=interpreter,
            local_path=local_path,
        )

        return typing.cast(None, jsii.invoke(self, "putLinuxExecStepConfig", [value]))

    @jsii.member(jsii_name="putWindowsExecStepConfig")
    def put_windows_exec_step_config(
        self,
        *,
        allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        gcs_object: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject", typing.Dict[builtins.str, typing.Any]]] = None,
        interpreter: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_success_codes: Defaults to [0]. A list of possible return values that the execution can return to indicate a success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#allowed_success_codes OsConfigPatchDeployment#allowed_success_codes}
        :param gcs_object: gcs_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#gcs_object OsConfigPatchDeployment#gcs_object}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script will be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#interpreter OsConfigPatchDeployment#interpreter}
        :param local_path: An absolute path to the executable on the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#local_path OsConfigPatchDeployment#local_path}
        '''
        value = OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig(
            allowed_success_codes=allowed_success_codes,
            gcs_object=gcs_object,
            interpreter=interpreter,
            local_path=local_path,
        )

        return typing.cast(None, jsii.invoke(self, "putWindowsExecStepConfig", [value]))

    @jsii.member(jsii_name="resetLinuxExecStepConfig")
    def reset_linux_exec_step_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinuxExecStepConfig", []))

    @jsii.member(jsii_name="resetWindowsExecStepConfig")
    def reset_windows_exec_step_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowsExecStepConfig", []))

    @builtins.property
    @jsii.member(jsii_name="linuxExecStepConfig")
    def linux_exec_step_config(
        self,
    ) -> OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigOutputReference:
        return typing.cast(OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigOutputReference, jsii.get(self, "linuxExecStepConfig"))

    @builtins.property
    @jsii.member(jsii_name="windowsExecStepConfig")
    def windows_exec_step_config(
        self,
    ) -> "OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigOutputReference":
        return typing.cast("OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigOutputReference", jsii.get(self, "windowsExecStepConfig"))

    @builtins.property
    @jsii.member(jsii_name="linuxExecStepConfigInput")
    def linux_exec_step_config_input(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig], jsii.get(self, "linuxExecStepConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsExecStepConfigInput")
    def windows_exec_step_config_input(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig"]:
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig"], jsii.get(self, "windowsExecStepConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigPostStep]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigPostStep], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentPatchConfigPostStep],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__074047a49c2bcf5d8ce14ce58b6e5b4eaaf80003ec7a8d48293bed5b07d3372a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_success_codes": "allowedSuccessCodes",
        "gcs_object": "gcsObject",
        "interpreter": "interpreter",
        "local_path": "localPath",
    },
)
class OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig:
    def __init__(
        self,
        *,
        allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        gcs_object: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject", typing.Dict[builtins.str, typing.Any]]] = None,
        interpreter: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_success_codes: Defaults to [0]. A list of possible return values that the execution can return to indicate a success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#allowed_success_codes OsConfigPatchDeployment#allowed_success_codes}
        :param gcs_object: gcs_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#gcs_object OsConfigPatchDeployment#gcs_object}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script will be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#interpreter OsConfigPatchDeployment#interpreter}
        :param local_path: An absolute path to the executable on the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#local_path OsConfigPatchDeployment#local_path}
        '''
        if isinstance(gcs_object, dict):
            gcs_object = OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject(**gcs_object)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e6a0c42e69dbc99343e82b95ffef7e04d5e2aa786a4fa7fbc8a1b155c1f1249)
            check_type(argname="argument allowed_success_codes", value=allowed_success_codes, expected_type=type_hints["allowed_success_codes"])
            check_type(argname="argument gcs_object", value=gcs_object, expected_type=type_hints["gcs_object"])
            check_type(argname="argument interpreter", value=interpreter, expected_type=type_hints["interpreter"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_success_codes is not None:
            self._values["allowed_success_codes"] = allowed_success_codes
        if gcs_object is not None:
            self._values["gcs_object"] = gcs_object
        if interpreter is not None:
            self._values["interpreter"] = interpreter
        if local_path is not None:
            self._values["local_path"] = local_path

    @builtins.property
    def allowed_success_codes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Defaults to [0]. A list of possible return values that the execution can return to indicate a success.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#allowed_success_codes OsConfigPatchDeployment#allowed_success_codes}
        '''
        result = self._values.get("allowed_success_codes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def gcs_object(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject"]:
        '''gcs_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#gcs_object OsConfigPatchDeployment#gcs_object}
        '''
        result = self._values.get("gcs_object")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject"], result)

    @builtins.property
    def interpreter(self) -> typing.Optional[builtins.str]:
        '''The script interpreter to use to run the script.

        If no interpreter is specified the script will
        be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#interpreter OsConfigPatchDeployment#interpreter}
        '''
        result = self._values.get("interpreter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''An absolute path to the executable on the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#local_path OsConfigPatchDeployment#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "generation_number": "generationNumber",
        "object": "object",
    },
)
class OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        generation_number: builtins.str,
        object: builtins.str,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#bucket OsConfigPatchDeployment#bucket}
        :param generation_number: Generation number of the Cloud Storage object. This is used to ensure that the ExecStep specified by this PatchJob does not change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#generation_number OsConfigPatchDeployment#generation_number}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#object OsConfigPatchDeployment#object}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca05eba3f92d223cc80e96e1bde2222b17e31dec5b022565124174ecb9b0f22d)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument generation_number", value=generation_number, expected_type=type_hints["generation_number"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "generation_number": generation_number,
            "object": object,
        }

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Bucket of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#bucket OsConfigPatchDeployment#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation_number(self) -> builtins.str:
        '''Generation number of the Cloud Storage object.

        This is used to ensure that the ExecStep specified by this PatchJob does not change.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#generation_number OsConfigPatchDeployment#generation_number}
        '''
        result = self._values.get("generation_number")
        assert result is not None, "Required property 'generation_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#object OsConfigPatchDeployment#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7779f205d29fcbc271c05ae041c98164cc9bde754bb5b94ba3d0a0a529c784f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="generationNumberInput")
    def generation_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "generationNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9d67ff35d5b94146e5433d259f9a4f8c9009e99679cb1faac0d6266fbf40c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generationNumber")
    def generation_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generationNumber"))

    @generation_number.setter
    def generation_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb0066307e6addef255c6860be6f6c2a527bd8ca61c1e77c871cc848065c446c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generationNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c30366a7f407cf95adae9c4946de36fe005bb778367c5380f947e8413cedac84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f1bde4e24cbee09062e6ea3643c43117a47ae2b4bb2901602acd7df849a05d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01feb26f838a44f68c1a0e8a145541484300e8a51dbe2ada9b2938cde19aade8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcsObject")
    def put_gcs_object(
        self,
        *,
        bucket: builtins.str,
        generation_number: builtins.str,
        object: builtins.str,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#bucket OsConfigPatchDeployment#bucket}
        :param generation_number: Generation number of the Cloud Storage object. This is used to ensure that the ExecStep specified by this PatchJob does not change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#generation_number OsConfigPatchDeployment#generation_number}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#object OsConfigPatchDeployment#object}
        '''
        value = OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject(
            bucket=bucket, generation_number=generation_number, object=object
        )

        return typing.cast(None, jsii.invoke(self, "putGcsObject", [value]))

    @jsii.member(jsii_name="resetAllowedSuccessCodes")
    def reset_allowed_success_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedSuccessCodes", []))

    @jsii.member(jsii_name="resetGcsObject")
    def reset_gcs_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsObject", []))

    @jsii.member(jsii_name="resetInterpreter")
    def reset_interpreter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterpreter", []))

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @builtins.property
    @jsii.member(jsii_name="gcsObject")
    def gcs_object(
        self,
    ) -> OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObjectOutputReference:
        return typing.cast(OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObjectOutputReference, jsii.get(self, "gcsObject"))

    @builtins.property
    @jsii.member(jsii_name="allowedSuccessCodesInput")
    def allowed_success_codes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "allowedSuccessCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsObjectInput")
    def gcs_object_input(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject], jsii.get(self, "gcsObjectInput"))

    @builtins.property
    @jsii.member(jsii_name="interpreterInput")
    def interpreter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interpreterInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedSuccessCodes")
    def allowed_success_codes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "allowedSuccessCodes"))

    @allowed_success_codes.setter
    def allowed_success_codes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d78586a4aa17b2adecafbc7ca242d23126ba01cb0201e94cbb982ba7bf7c1b9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedSuccessCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e60669c30c236e339421478ca9f5d5d24a9e4a780e828907746dc2e7004be0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e54c37779ba435d7981985c79a4c5119f5f972047d1e340b076c0421751ecc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08dfed580351bfb0174a85434d579ac3358361f05050f127039dcca6456a1699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPreStep",
    jsii_struct_bases=[],
    name_mapping={
        "linux_exec_step_config": "linuxExecStepConfig",
        "windows_exec_step_config": "windowsExecStepConfig",
    },
)
class OsConfigPatchDeploymentPatchConfigPreStep:
    def __init__(
        self,
        *,
        linux_exec_step_config: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        windows_exec_step_config: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param linux_exec_step_config: linux_exec_step_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#linux_exec_step_config OsConfigPatchDeployment#linux_exec_step_config}
        :param windows_exec_step_config: windows_exec_step_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#windows_exec_step_config OsConfigPatchDeployment#windows_exec_step_config}
        '''
        if isinstance(linux_exec_step_config, dict):
            linux_exec_step_config = OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig(**linux_exec_step_config)
        if isinstance(windows_exec_step_config, dict):
            windows_exec_step_config = OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig(**windows_exec_step_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12f73bcfd3aad79ab1cd0cb853490db4c5a0305649368901927ee8023017fd8e)
            check_type(argname="argument linux_exec_step_config", value=linux_exec_step_config, expected_type=type_hints["linux_exec_step_config"])
            check_type(argname="argument windows_exec_step_config", value=windows_exec_step_config, expected_type=type_hints["windows_exec_step_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if linux_exec_step_config is not None:
            self._values["linux_exec_step_config"] = linux_exec_step_config
        if windows_exec_step_config is not None:
            self._values["windows_exec_step_config"] = windows_exec_step_config

    @builtins.property
    def linux_exec_step_config(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig"]:
        '''linux_exec_step_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#linux_exec_step_config OsConfigPatchDeployment#linux_exec_step_config}
        '''
        result = self._values.get("linux_exec_step_config")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig"], result)

    @builtins.property
    def windows_exec_step_config(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig"]:
        '''windows_exec_step_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#windows_exec_step_config OsConfigPatchDeployment#windows_exec_step_config}
        '''
        result = self._values.get("windows_exec_step_config")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentPatchConfigPreStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_success_codes": "allowedSuccessCodes",
        "gcs_object": "gcsObject",
        "interpreter": "interpreter",
        "local_path": "localPath",
    },
)
class OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig:
    def __init__(
        self,
        *,
        allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        gcs_object: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject", typing.Dict[builtins.str, typing.Any]]] = None,
        interpreter: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_success_codes: Defaults to [0]. A list of possible return values that the execution can return to indicate a success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#allowed_success_codes OsConfigPatchDeployment#allowed_success_codes}
        :param gcs_object: gcs_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#gcs_object OsConfigPatchDeployment#gcs_object}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script will be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#interpreter OsConfigPatchDeployment#interpreter}
        :param local_path: An absolute path to the executable on the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#local_path OsConfigPatchDeployment#local_path}
        '''
        if isinstance(gcs_object, dict):
            gcs_object = OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject(**gcs_object)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70404ba3603a61108ffdd7ef3c6f6b94bb6c600e90b4086bf3ae168fedff4a2d)
            check_type(argname="argument allowed_success_codes", value=allowed_success_codes, expected_type=type_hints["allowed_success_codes"])
            check_type(argname="argument gcs_object", value=gcs_object, expected_type=type_hints["gcs_object"])
            check_type(argname="argument interpreter", value=interpreter, expected_type=type_hints["interpreter"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_success_codes is not None:
            self._values["allowed_success_codes"] = allowed_success_codes
        if gcs_object is not None:
            self._values["gcs_object"] = gcs_object
        if interpreter is not None:
            self._values["interpreter"] = interpreter
        if local_path is not None:
            self._values["local_path"] = local_path

    @builtins.property
    def allowed_success_codes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Defaults to [0]. A list of possible return values that the execution can return to indicate a success.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#allowed_success_codes OsConfigPatchDeployment#allowed_success_codes}
        '''
        result = self._values.get("allowed_success_codes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def gcs_object(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject"]:
        '''gcs_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#gcs_object OsConfigPatchDeployment#gcs_object}
        '''
        result = self._values.get("gcs_object")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject"], result)

    @builtins.property
    def interpreter(self) -> typing.Optional[builtins.str]:
        '''The script interpreter to use to run the script.

        If no interpreter is specified the script will
        be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#interpreter OsConfigPatchDeployment#interpreter}
        '''
        result = self._values.get("interpreter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''An absolute path to the executable on the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#local_path OsConfigPatchDeployment#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "generation_number": "generationNumber",
        "object": "object",
    },
)
class OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        generation_number: builtins.str,
        object: builtins.str,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#bucket OsConfigPatchDeployment#bucket}
        :param generation_number: Generation number of the Cloud Storage object. This is used to ensure that the ExecStep specified by this PatchJob does not change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#generation_number OsConfigPatchDeployment#generation_number}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#object OsConfigPatchDeployment#object}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a0917744929797d205a183dfa9915d742d094bb312f84980b53e89d67762885)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument generation_number", value=generation_number, expected_type=type_hints["generation_number"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "generation_number": generation_number,
            "object": object,
        }

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Bucket of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#bucket OsConfigPatchDeployment#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation_number(self) -> builtins.str:
        '''Generation number of the Cloud Storage object.

        This is used to ensure that the ExecStep specified by this PatchJob does not change.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#generation_number OsConfigPatchDeployment#generation_number}
        '''
        result = self._values.get("generation_number")
        assert result is not None, "Required property 'generation_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#object OsConfigPatchDeployment#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc8d4a3b1a0bdfb21fba979015d277b3b6d01e18c1fb3bd371687f0201bb0090)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="generationNumberInput")
    def generation_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "generationNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ab94e3d045e6fd1c8b491f473abd238a177c7059fa235424426a2b106d8d827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generationNumber")
    def generation_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generationNumber"))

    @generation_number.setter
    def generation_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d39e7f38d047236cac27445399af39450a99668797e67d0ff8d0ad473838c21e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generationNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae932e6aebf076dc854cee0dafc69f9a1402febfde42034cc33409a1c44b83d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8af32373e7458bb47e10b92eaeb61b252806469bd52206095bc40bc6f0cee04d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afce9a7f3ddce3e1524c5ab2d59176421e34f5948ca1dcd6ecc23d1d4d99b0f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcsObject")
    def put_gcs_object(
        self,
        *,
        bucket: builtins.str,
        generation_number: builtins.str,
        object: builtins.str,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#bucket OsConfigPatchDeployment#bucket}
        :param generation_number: Generation number of the Cloud Storage object. This is used to ensure that the ExecStep specified by this PatchJob does not change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#generation_number OsConfigPatchDeployment#generation_number}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#object OsConfigPatchDeployment#object}
        '''
        value = OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject(
            bucket=bucket, generation_number=generation_number, object=object
        )

        return typing.cast(None, jsii.invoke(self, "putGcsObject", [value]))

    @jsii.member(jsii_name="resetAllowedSuccessCodes")
    def reset_allowed_success_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedSuccessCodes", []))

    @jsii.member(jsii_name="resetGcsObject")
    def reset_gcs_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsObject", []))

    @jsii.member(jsii_name="resetInterpreter")
    def reset_interpreter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterpreter", []))

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @builtins.property
    @jsii.member(jsii_name="gcsObject")
    def gcs_object(
        self,
    ) -> OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObjectOutputReference:
        return typing.cast(OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObjectOutputReference, jsii.get(self, "gcsObject"))

    @builtins.property
    @jsii.member(jsii_name="allowedSuccessCodesInput")
    def allowed_success_codes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "allowedSuccessCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsObjectInput")
    def gcs_object_input(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject], jsii.get(self, "gcsObjectInput"))

    @builtins.property
    @jsii.member(jsii_name="interpreterInput")
    def interpreter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interpreterInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedSuccessCodes")
    def allowed_success_codes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "allowedSuccessCodes"))

    @allowed_success_codes.setter
    def allowed_success_codes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f6a1f14621b88186cbd0d6495365d92527752798f99616a3b85a22c37d71fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedSuccessCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30fb11f0eef4e7d92588ca20c38b839ebf314ac27128dc6aaf69cc4dda25d56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44caa7cd97a2eb0662bcf6890b2a341b3456a9f214bad1c43f75fdb61e637bb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__222e4eca7204263c9c71033b22509c08376ec54c6293b4a0e3b2bf9135d18766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigPatchDeploymentPatchConfigPreStepOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPreStepOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b3d78d1093b3fb85330873ccf03bf99544bd50165897bba521bc8cf5b9e471d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLinuxExecStepConfig")
    def put_linux_exec_step_config(
        self,
        *,
        allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        gcs_object: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject, typing.Dict[builtins.str, typing.Any]]] = None,
        interpreter: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_success_codes: Defaults to [0]. A list of possible return values that the execution can return to indicate a success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#allowed_success_codes OsConfigPatchDeployment#allowed_success_codes}
        :param gcs_object: gcs_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#gcs_object OsConfigPatchDeployment#gcs_object}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script will be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#interpreter OsConfigPatchDeployment#interpreter}
        :param local_path: An absolute path to the executable on the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#local_path OsConfigPatchDeployment#local_path}
        '''
        value = OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig(
            allowed_success_codes=allowed_success_codes,
            gcs_object=gcs_object,
            interpreter=interpreter,
            local_path=local_path,
        )

        return typing.cast(None, jsii.invoke(self, "putLinuxExecStepConfig", [value]))

    @jsii.member(jsii_name="putWindowsExecStepConfig")
    def put_windows_exec_step_config(
        self,
        *,
        allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        gcs_object: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject", typing.Dict[builtins.str, typing.Any]]] = None,
        interpreter: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_success_codes: Defaults to [0]. A list of possible return values that the execution can return to indicate a success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#allowed_success_codes OsConfigPatchDeployment#allowed_success_codes}
        :param gcs_object: gcs_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#gcs_object OsConfigPatchDeployment#gcs_object}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script will be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#interpreter OsConfigPatchDeployment#interpreter}
        :param local_path: An absolute path to the executable on the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#local_path OsConfigPatchDeployment#local_path}
        '''
        value = OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig(
            allowed_success_codes=allowed_success_codes,
            gcs_object=gcs_object,
            interpreter=interpreter,
            local_path=local_path,
        )

        return typing.cast(None, jsii.invoke(self, "putWindowsExecStepConfig", [value]))

    @jsii.member(jsii_name="resetLinuxExecStepConfig")
    def reset_linux_exec_step_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinuxExecStepConfig", []))

    @jsii.member(jsii_name="resetWindowsExecStepConfig")
    def reset_windows_exec_step_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowsExecStepConfig", []))

    @builtins.property
    @jsii.member(jsii_name="linuxExecStepConfig")
    def linux_exec_step_config(
        self,
    ) -> OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigOutputReference:
        return typing.cast(OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigOutputReference, jsii.get(self, "linuxExecStepConfig"))

    @builtins.property
    @jsii.member(jsii_name="windowsExecStepConfig")
    def windows_exec_step_config(
        self,
    ) -> "OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigOutputReference":
        return typing.cast("OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigOutputReference", jsii.get(self, "windowsExecStepConfig"))

    @builtins.property
    @jsii.member(jsii_name="linuxExecStepConfigInput")
    def linux_exec_step_config_input(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig], jsii.get(self, "linuxExecStepConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsExecStepConfigInput")
    def windows_exec_step_config_input(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig"]:
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig"], jsii.get(self, "windowsExecStepConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigPreStep]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigPreStep], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentPatchConfigPreStep],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff447cea012eb5a42b4eaa8fd02f536c735b146913554457f65a378e6eb2e37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_success_codes": "allowedSuccessCodes",
        "gcs_object": "gcsObject",
        "interpreter": "interpreter",
        "local_path": "localPath",
    },
)
class OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig:
    def __init__(
        self,
        *,
        allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        gcs_object: typing.Optional[typing.Union["OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject", typing.Dict[builtins.str, typing.Any]]] = None,
        interpreter: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_success_codes: Defaults to [0]. A list of possible return values that the execution can return to indicate a success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#allowed_success_codes OsConfigPatchDeployment#allowed_success_codes}
        :param gcs_object: gcs_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#gcs_object OsConfigPatchDeployment#gcs_object}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script will be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#interpreter OsConfigPatchDeployment#interpreter}
        :param local_path: An absolute path to the executable on the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#local_path OsConfigPatchDeployment#local_path}
        '''
        if isinstance(gcs_object, dict):
            gcs_object = OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject(**gcs_object)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac5879d46f17ff21ac4553d4c6e88ea6cd666506a0d6335072a097aa26021eb)
            check_type(argname="argument allowed_success_codes", value=allowed_success_codes, expected_type=type_hints["allowed_success_codes"])
            check_type(argname="argument gcs_object", value=gcs_object, expected_type=type_hints["gcs_object"])
            check_type(argname="argument interpreter", value=interpreter, expected_type=type_hints["interpreter"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_success_codes is not None:
            self._values["allowed_success_codes"] = allowed_success_codes
        if gcs_object is not None:
            self._values["gcs_object"] = gcs_object
        if interpreter is not None:
            self._values["interpreter"] = interpreter
        if local_path is not None:
            self._values["local_path"] = local_path

    @builtins.property
    def allowed_success_codes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Defaults to [0]. A list of possible return values that the execution can return to indicate a success.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#allowed_success_codes OsConfigPatchDeployment#allowed_success_codes}
        '''
        result = self._values.get("allowed_success_codes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def gcs_object(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject"]:
        '''gcs_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#gcs_object OsConfigPatchDeployment#gcs_object}
        '''
        result = self._values.get("gcs_object")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject"], result)

    @builtins.property
    def interpreter(self) -> typing.Optional[builtins.str]:
        '''The script interpreter to use to run the script.

        If no interpreter is specified the script will
        be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#interpreter OsConfigPatchDeployment#interpreter}
        '''
        result = self._values.get("interpreter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''An absolute path to the executable on the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#local_path OsConfigPatchDeployment#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "generation_number": "generationNumber",
        "object": "object",
    },
)
class OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        generation_number: builtins.str,
        object: builtins.str,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#bucket OsConfigPatchDeployment#bucket}
        :param generation_number: Generation number of the Cloud Storage object. This is used to ensure that the ExecStep specified by this PatchJob does not change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#generation_number OsConfigPatchDeployment#generation_number}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#object OsConfigPatchDeployment#object}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb3321bcc0e01bcda266f1f28564684ded295ba56c0b807178b14b4ab1a2571)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument generation_number", value=generation_number, expected_type=type_hints["generation_number"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "generation_number": generation_number,
            "object": object,
        }

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Bucket of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#bucket OsConfigPatchDeployment#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation_number(self) -> builtins.str:
        '''Generation number of the Cloud Storage object.

        This is used to ensure that the ExecStep specified by this PatchJob does not change.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#generation_number OsConfigPatchDeployment#generation_number}
        '''
        result = self._values.get("generation_number")
        assert result is not None, "Required property 'generation_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#object OsConfigPatchDeployment#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f304598356ac7fe4220ddb13030f4d1eae7ee32a22fb78266518eb4c28dd863)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="generationNumberInput")
    def generation_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "generationNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c9af9bd324526e81cedb047760a93eb9fdc67d08e14fbf5a2b29e1fa88caab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generationNumber")
    def generation_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generationNumber"))

    @generation_number.setter
    def generation_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3978570381b92a56d4e9ad7d8e27964415856769a50f804faab87b4e0be4110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generationNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d39a0c0790308c1fb03520e20f882fa4db5a9a26500f3d52afa6ca3ea612c580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccd3f11ab1515e98946ca527e2823ff78b8450efed55f9fb74111fdda9a5f6d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff709820452bb925bfdb0d4962363845794d62c96a6dc6edddb28f82c8c03e76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcsObject")
    def put_gcs_object(
        self,
        *,
        bucket: builtins.str,
        generation_number: builtins.str,
        object: builtins.str,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#bucket OsConfigPatchDeployment#bucket}
        :param generation_number: Generation number of the Cloud Storage object. This is used to ensure that the ExecStep specified by this PatchJob does not change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#generation_number OsConfigPatchDeployment#generation_number}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#object OsConfigPatchDeployment#object}
        '''
        value = OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject(
            bucket=bucket, generation_number=generation_number, object=object
        )

        return typing.cast(None, jsii.invoke(self, "putGcsObject", [value]))

    @jsii.member(jsii_name="resetAllowedSuccessCodes")
    def reset_allowed_success_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedSuccessCodes", []))

    @jsii.member(jsii_name="resetGcsObject")
    def reset_gcs_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsObject", []))

    @jsii.member(jsii_name="resetInterpreter")
    def reset_interpreter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterpreter", []))

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @builtins.property
    @jsii.member(jsii_name="gcsObject")
    def gcs_object(
        self,
    ) -> OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObjectOutputReference:
        return typing.cast(OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObjectOutputReference, jsii.get(self, "gcsObject"))

    @builtins.property
    @jsii.member(jsii_name="allowedSuccessCodesInput")
    def allowed_success_codes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "allowedSuccessCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsObjectInput")
    def gcs_object_input(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject], jsii.get(self, "gcsObjectInput"))

    @builtins.property
    @jsii.member(jsii_name="interpreterInput")
    def interpreter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interpreterInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedSuccessCodes")
    def allowed_success_codes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "allowedSuccessCodes"))

    @allowed_success_codes.setter
    def allowed_success_codes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fff6b73e4507eab2f8aec3729f940a92c5ab7a19a0b8f325aaa26634562b199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedSuccessCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d77a062dc40adfce26a55f78cd6374f2adb771ccbcdca339e3dd9f45297b2c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca4b2b3bffa7b9d2d2e157aa7038032b498fef51ba4aafac4f62d3f52391f42d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f26cc02f80ddc6d01e4b93c2caac7b32514c5a75036d370d85b7473315e94cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigWindowsUpdate",
    jsii_struct_bases=[],
    name_mapping={
        "classifications": "classifications",
        "excludes": "excludes",
        "exclusive_patches": "exclusivePatches",
    },
)
class OsConfigPatchDeploymentPatchConfigWindowsUpdate:
    def __init__(
        self,
        *,
        classifications: typing.Optional[typing.Sequence[builtins.str]] = None,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclusive_patches: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param classifications: Only apply updates of these windows update classifications. If empty, all updates are applied. Possible values: ["CRITICAL", "SECURITY", "DEFINITION", "DRIVER", "FEATURE_PACK", "SERVICE_PACK", "TOOL", "UPDATE_ROLLUP", "UPDATE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#classifications OsConfigPatchDeployment#classifications}
        :param excludes: List of KBs to exclude from update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#excludes OsConfigPatchDeployment#excludes}
        :param exclusive_patches: An exclusive list of kbs to be updated. These are the only patches that will be updated. This field must not be used with other patch configurations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#exclusive_patches OsConfigPatchDeployment#exclusive_patches}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8df8d3945accab44bfb2f6e2b014fb0d993f09c43a15870431f001d7118e88f)
            check_type(argname="argument classifications", value=classifications, expected_type=type_hints["classifications"])
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument exclusive_patches", value=exclusive_patches, expected_type=type_hints["exclusive_patches"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if classifications is not None:
            self._values["classifications"] = classifications
        if excludes is not None:
            self._values["excludes"] = excludes
        if exclusive_patches is not None:
            self._values["exclusive_patches"] = exclusive_patches

    @builtins.property
    def classifications(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Only apply updates of these windows update classifications.

        If empty, all updates are applied. Possible values: ["CRITICAL", "SECURITY", "DEFINITION", "DRIVER", "FEATURE_PACK", "SERVICE_PACK", "TOOL", "UPDATE_ROLLUP", "UPDATE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#classifications OsConfigPatchDeployment#classifications}
        '''
        result = self._values.get("classifications")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of KBs to exclude from update.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#excludes OsConfigPatchDeployment#excludes}
        '''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclusive_patches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An exclusive list of kbs to be updated.

        These are the only patches that will be updated.
        This field must not be used with other patch configurations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#exclusive_patches OsConfigPatchDeployment#exclusive_patches}
        '''
        result = self._values.get("exclusive_patches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentPatchConfigWindowsUpdate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentPatchConfigWindowsUpdateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigWindowsUpdateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7703f88560236f179b84a62a7b5f687c646735bed26033d2a5c1c016813f5037)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClassifications")
    def reset_classifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClassifications", []))

    @jsii.member(jsii_name="resetExcludes")
    def reset_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludes", []))

    @jsii.member(jsii_name="resetExclusivePatches")
    def reset_exclusive_patches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusivePatches", []))

    @builtins.property
    @jsii.member(jsii_name="classificationsInput")
    def classifications_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "classificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludesInput")
    def excludes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludesInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusivePatchesInput")
    def exclusive_patches_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exclusivePatchesInput"))

    @builtins.property
    @jsii.member(jsii_name="classifications")
    def classifications(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "classifications"))

    @classifications.setter
    def classifications(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb4d962e605f776dc484b7d8e332d855f8fd894d67b7b1e56cd1f34856f8de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classifications", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludes"))

    @excludes.setter
    def excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4255ec252885871c3c98731380104d58b830511d97cfaa55016583b41aa5a6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusivePatches")
    def exclusive_patches(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusivePatches"))

    @exclusive_patches.setter
    def exclusive_patches(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5506ec424385d9b32caedec134f41cf717d87f91b746a81da538a94f744a3cf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusivePatches", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigWindowsUpdate]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigWindowsUpdate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentPatchConfigWindowsUpdate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bd887e1629594e14ae8a447d43e1bfc8efdf646a28ab7a19bbaeb7dee263d3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigYum",
    jsii_struct_bases=[],
    name_mapping={
        "excludes": "excludes",
        "exclusive_packages": "exclusivePackages",
        "minimal": "minimal",
        "security": "security",
    },
)
class OsConfigPatchDeploymentPatchConfigYum:
    def __init__(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclusive_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        minimal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param excludes: List of packages to exclude from update. These packages will be excluded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#excludes OsConfigPatchDeployment#excludes}
        :param exclusive_packages: An exclusive list of packages to be updated. These are the only packages that will be updated. If these packages are not installed, they will be ignored. This field cannot be specified with any other patch configuration fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#exclusive_packages OsConfigPatchDeployment#exclusive_packages}
        :param minimal: Will cause patch to run yum update-minimal instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#minimal OsConfigPatchDeployment#minimal}
        :param security: Adds the --security flag to yum update. Not supported on all platforms. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#security OsConfigPatchDeployment#security}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80bb0ee099a30cf96b61b289378fab5117a915efb02f411a59f25520433be49c)
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument exclusive_packages", value=exclusive_packages, expected_type=type_hints["exclusive_packages"])
            check_type(argname="argument minimal", value=minimal, expected_type=type_hints["minimal"])
            check_type(argname="argument security", value=security, expected_type=type_hints["security"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excludes is not None:
            self._values["excludes"] = excludes
        if exclusive_packages is not None:
            self._values["exclusive_packages"] = exclusive_packages
        if minimal is not None:
            self._values["minimal"] = minimal
        if security is not None:
            self._values["security"] = security

    @builtins.property
    def excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of packages to exclude from update. These packages will be excluded.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#excludes OsConfigPatchDeployment#excludes}
        '''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclusive_packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An exclusive list of packages to be updated.

        These are the only packages that will be updated.
        If these packages are not installed, they will be ignored. This field cannot be specified with
        any other patch configuration fields.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#exclusive_packages OsConfigPatchDeployment#exclusive_packages}
        '''
        result = self._values.get("exclusive_packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def minimal(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Will cause patch to run yum update-minimal instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#minimal OsConfigPatchDeployment#minimal}
        '''
        result = self._values.get("minimal")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def security(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Adds the --security flag to yum update. Not supported on all platforms.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#security OsConfigPatchDeployment#security}
        '''
        result = self._values.get("security")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentPatchConfigYum(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentPatchConfigYumOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigYumOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98ffdf8f1c3b795df246b256c6a449fb906a1682d6901092ad8cb167db20fd17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludes")
    def reset_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludes", []))

    @jsii.member(jsii_name="resetExclusivePackages")
    def reset_exclusive_packages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusivePackages", []))

    @jsii.member(jsii_name="resetMinimal")
    def reset_minimal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimal", []))

    @jsii.member(jsii_name="resetSecurity")
    def reset_security(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurity", []))

    @builtins.property
    @jsii.member(jsii_name="excludesInput")
    def excludes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludesInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusivePackagesInput")
    def exclusive_packages_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exclusivePackagesInput"))

    @builtins.property
    @jsii.member(jsii_name="minimalInput")
    def minimal_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "minimalInput"))

    @builtins.property
    @jsii.member(jsii_name="securityInput")
    def security_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "securityInput"))

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludes"))

    @excludes.setter
    def excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e75dfdd4115b8f8e7222400a4a9e5733ba80b6c360b70a7be79a008f48ed80f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusivePackages")
    def exclusive_packages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusivePackages"))

    @exclusive_packages.setter
    def exclusive_packages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37fefa99c975c7345ccfdc80ce6a84d45bd5e1e8299f3e5881bd2c1e3d8d2460)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusivePackages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimal")
    def minimal(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "minimal"))

    @minimal.setter
    def minimal(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a16d8969f83b396f03ca769fa81510be85de28d785ab2ba812bde62540ba88d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="security")
    def security(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "security"))

    @security.setter
    def security(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7983800e49453a73e09f5383c7cf655d406c40539e33116b398682c0b44681a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "security", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OsConfigPatchDeploymentPatchConfigYum]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigYum], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentPatchConfigYum],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__345eeba2f4cdc96b3fad5336841a16811a1861c5443edcf4b568d43d23c9308b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigZypper",
    jsii_struct_bases=[],
    name_mapping={
        "categories": "categories",
        "excludes": "excludes",
        "exclusive_patches": "exclusivePatches",
        "severities": "severities",
        "with_optional": "withOptional",
        "with_update": "withUpdate",
    },
)
class OsConfigPatchDeploymentPatchConfigZypper:
    def __init__(
        self,
        *,
        categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclusive_patches: typing.Optional[typing.Sequence[builtins.str]] = None,
        severities: typing.Optional[typing.Sequence[builtins.str]] = None,
        with_optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        with_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param categories: Install only patches with these categories. Common categories include security, recommended, and feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#categories OsConfigPatchDeployment#categories}
        :param excludes: List of packages to exclude from update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#excludes OsConfigPatchDeployment#excludes}
        :param exclusive_patches: An exclusive list of patches to be updated. These are the only patches that will be installed using 'zypper patch patch:' command. This field must not be used with any other patch configuration fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#exclusive_patches OsConfigPatchDeployment#exclusive_patches}
        :param severities: Install only patches with these severities. Common severities include critical, important, moderate, and low. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#severities OsConfigPatchDeployment#severities}
        :param with_optional: Adds the --with-optional flag to zypper patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#with_optional OsConfigPatchDeployment#with_optional}
        :param with_update: Adds the --with-update flag, to zypper patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#with_update OsConfigPatchDeployment#with_update}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8a92e1e3ed254f0af63c4bf7739783129b4fa8dec1082b754f4e2b3e478b91a)
            check_type(argname="argument categories", value=categories, expected_type=type_hints["categories"])
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument exclusive_patches", value=exclusive_patches, expected_type=type_hints["exclusive_patches"])
            check_type(argname="argument severities", value=severities, expected_type=type_hints["severities"])
            check_type(argname="argument with_optional", value=with_optional, expected_type=type_hints["with_optional"])
            check_type(argname="argument with_update", value=with_update, expected_type=type_hints["with_update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if categories is not None:
            self._values["categories"] = categories
        if excludes is not None:
            self._values["excludes"] = excludes
        if exclusive_patches is not None:
            self._values["exclusive_patches"] = exclusive_patches
        if severities is not None:
            self._values["severities"] = severities
        if with_optional is not None:
            self._values["with_optional"] = with_optional
        if with_update is not None:
            self._values["with_update"] = with_update

    @builtins.property
    def categories(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Install only patches with these categories. Common categories include security, recommended, and feature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#categories OsConfigPatchDeployment#categories}
        '''
        result = self._values.get("categories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of packages to exclude from update.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#excludes OsConfigPatchDeployment#excludes}
        '''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclusive_patches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An exclusive list of patches to be updated.

        These are the only patches that will be installed using 'zypper patch patch:' command.
        This field must not be used with any other patch configuration fields.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#exclusive_patches OsConfigPatchDeployment#exclusive_patches}
        '''
        result = self._values.get("exclusive_patches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def severities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Install only patches with these severities. Common severities include critical, important, moderate, and low.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#severities OsConfigPatchDeployment#severities}
        '''
        result = self._values.get("severities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def with_optional(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Adds the --with-optional flag to zypper patch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#with_optional OsConfigPatchDeployment#with_optional}
        '''
        result = self._values.get("with_optional")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def with_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Adds the --with-update flag, to zypper patch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#with_update OsConfigPatchDeployment#with_update}
        '''
        result = self._values.get("with_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentPatchConfigZypper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentPatchConfigZypperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentPatchConfigZypperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21b2a661d5575c488ec2817c3dbae1b8ce3321545faf5a79ed6b2160fe0ab664)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCategories")
    def reset_categories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCategories", []))

    @jsii.member(jsii_name="resetExcludes")
    def reset_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludes", []))

    @jsii.member(jsii_name="resetExclusivePatches")
    def reset_exclusive_patches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusivePatches", []))

    @jsii.member(jsii_name="resetSeverities")
    def reset_severities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverities", []))

    @jsii.member(jsii_name="resetWithOptional")
    def reset_with_optional(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithOptional", []))

    @jsii.member(jsii_name="resetWithUpdate")
    def reset_with_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="categoriesInput")
    def categories_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "categoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludesInput")
    def excludes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludesInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusivePatchesInput")
    def exclusive_patches_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exclusivePatchesInput"))

    @builtins.property
    @jsii.member(jsii_name="severitiesInput")
    def severities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "severitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="withOptionalInput")
    def with_optional_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withOptionalInput"))

    @builtins.property
    @jsii.member(jsii_name="withUpdateInput")
    def with_update_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="categories")
    def categories(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "categories"))

    @categories.setter
    def categories(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b66290a195e9774aaa3a6ad322b472f07a08c012513a75044953b7575c9066e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "categories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludes"))

    @excludes.setter
    def excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a952ce192da371286705d302850201c1d21205ec051a49bfe737e3f3629f9c5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusivePatches")
    def exclusive_patches(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusivePatches"))

    @exclusive_patches.setter
    def exclusive_patches(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe67097d31f42b7d76f0be3a0560aed0053d03d35d3eeb1f75c13300f64e5561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusivePatches", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severities")
    def severities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "severities"))

    @severities.setter
    def severities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38218f1465049568a1b82644aee2ebe537632b1feb9c2f90b766de75e334661a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withOptional")
    def with_optional(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "withOptional"))

    @with_optional.setter
    def with_optional(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b9b2141488c74b2e5af950e7f42eb670ebdf8a8951a884cb08df70d5a56cfc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withOptional", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withUpdate")
    def with_update(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "withUpdate"))

    @with_update.setter
    def with_update(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43fe10db6fe5eb85bd97a533f6ccb626cacba4008c230135fa19b12670fb1351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentPatchConfigZypper]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentPatchConfigZypper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentPatchConfigZypper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1b549d504977e968629683615f3ea0d5dc2d3f6a219aecf7467ddf9b1e41df0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentRecurringSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "time_of_day": "timeOfDay",
        "time_zone": "timeZone",
        "end_time": "endTime",
        "monthly": "monthly",
        "start_time": "startTime",
        "weekly": "weekly",
    },
)
class OsConfigPatchDeploymentRecurringSchedule:
    def __init__(
        self,
        *,
        time_of_day: typing.Union["OsConfigPatchDeploymentRecurringScheduleTimeOfDay", typing.Dict[builtins.str, typing.Any]],
        time_zone: typing.Union["OsConfigPatchDeploymentRecurringScheduleTimeZone", typing.Dict[builtins.str, typing.Any]],
        end_time: typing.Optional[builtins.str] = None,
        monthly: typing.Optional[typing.Union["OsConfigPatchDeploymentRecurringScheduleMonthly", typing.Dict[builtins.str, typing.Any]]] = None,
        start_time: typing.Optional[builtins.str] = None,
        weekly: typing.Optional[typing.Union["OsConfigPatchDeploymentRecurringScheduleWeekly", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param time_of_day: time_of_day block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#time_of_day OsConfigPatchDeployment#time_of_day}
        :param time_zone: time_zone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#time_zone OsConfigPatchDeployment#time_zone}
        :param end_time: The end time at which a recurring patch deployment schedule is no longer active. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#end_time OsConfigPatchDeployment#end_time}
        :param monthly: monthly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#monthly OsConfigPatchDeployment#monthly}
        :param start_time: The time that the recurring schedule becomes effective. Defaults to createTime of the patch deployment. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#start_time OsConfigPatchDeployment#start_time}
        :param weekly: weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#weekly OsConfigPatchDeployment#weekly}
        '''
        if isinstance(time_of_day, dict):
            time_of_day = OsConfigPatchDeploymentRecurringScheduleTimeOfDay(**time_of_day)
        if isinstance(time_zone, dict):
            time_zone = OsConfigPatchDeploymentRecurringScheduleTimeZone(**time_zone)
        if isinstance(monthly, dict):
            monthly = OsConfigPatchDeploymentRecurringScheduleMonthly(**monthly)
        if isinstance(weekly, dict):
            weekly = OsConfigPatchDeploymentRecurringScheduleWeekly(**weekly)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c2fb3d2babe9bf4340c4571955491cfae5db04185ca185c6e76e2e33d9a3d8)
            check_type(argname="argument time_of_day", value=time_of_day, expected_type=type_hints["time_of_day"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument monthly", value=monthly, expected_type=type_hints["monthly"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument weekly", value=weekly, expected_type=type_hints["weekly"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "time_of_day": time_of_day,
            "time_zone": time_zone,
        }
        if end_time is not None:
            self._values["end_time"] = end_time
        if monthly is not None:
            self._values["monthly"] = monthly
        if start_time is not None:
            self._values["start_time"] = start_time
        if weekly is not None:
            self._values["weekly"] = weekly

    @builtins.property
    def time_of_day(self) -> "OsConfigPatchDeploymentRecurringScheduleTimeOfDay":
        '''time_of_day block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#time_of_day OsConfigPatchDeployment#time_of_day}
        '''
        result = self._values.get("time_of_day")
        assert result is not None, "Required property 'time_of_day' is missing"
        return typing.cast("OsConfigPatchDeploymentRecurringScheduleTimeOfDay", result)

    @builtins.property
    def time_zone(self) -> "OsConfigPatchDeploymentRecurringScheduleTimeZone":
        '''time_zone block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#time_zone OsConfigPatchDeployment#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast("OsConfigPatchDeploymentRecurringScheduleTimeZone", result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''The end time at which a recurring patch deployment schedule is no longer active.

        A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#end_time OsConfigPatchDeployment#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monthly(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentRecurringScheduleMonthly"]:
        '''monthly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#monthly OsConfigPatchDeployment#monthly}
        '''
        result = self._values.get("monthly")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentRecurringScheduleMonthly"], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The time that the recurring schedule becomes effective.

        Defaults to createTime of the patch deployment.
        A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#start_time OsConfigPatchDeployment#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weekly(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentRecurringScheduleWeekly"]:
        '''weekly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#weekly OsConfigPatchDeployment#weekly}
        '''
        result = self._values.get("weekly")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentRecurringScheduleWeekly"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentRecurringSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentRecurringScheduleMonthly",
    jsii_struct_bases=[],
    name_mapping={"month_day": "monthDay", "week_day_of_month": "weekDayOfMonth"},
)
class OsConfigPatchDeploymentRecurringScheduleMonthly:
    def __init__(
        self,
        *,
        month_day: typing.Optional[jsii.Number] = None,
        week_day_of_month: typing.Optional[typing.Union["OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param month_day: One day of the month. 1-31 indicates the 1st to the 31st day. -1 indicates the last day of the month. Months without the target day will be skipped. For example, a schedule to run "every month on the 31st" will not run in February, April, June, etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#month_day OsConfigPatchDeployment#month_day}
        :param week_day_of_month: week_day_of_month block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#week_day_of_month OsConfigPatchDeployment#week_day_of_month}
        '''
        if isinstance(week_day_of_month, dict):
            week_day_of_month = OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth(**week_day_of_month)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a33ad52bb5d86e5838811bdbfd6577d7345edcee4025edfaaa38a5b1397dc6e)
            check_type(argname="argument month_day", value=month_day, expected_type=type_hints["month_day"])
            check_type(argname="argument week_day_of_month", value=week_day_of_month, expected_type=type_hints["week_day_of_month"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if month_day is not None:
            self._values["month_day"] = month_day
        if week_day_of_month is not None:
            self._values["week_day_of_month"] = week_day_of_month

    @builtins.property
    def month_day(self) -> typing.Optional[jsii.Number]:
        '''One day of the month.

        1-31 indicates the 1st to the 31st day. -1 indicates the last day of the month.
        Months without the target day will be skipped. For example, a schedule to run "every month on the 31st"
        will not run in February, April, June, etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#month_day OsConfigPatchDeployment#month_day}
        '''
        result = self._values.get("month_day")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def week_day_of_month(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth"]:
        '''week_day_of_month block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#week_day_of_month OsConfigPatchDeployment#week_day_of_month}
        '''
        result = self._values.get("week_day_of_month")
        return typing.cast(typing.Optional["OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentRecurringScheduleMonthly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentRecurringScheduleMonthlyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentRecurringScheduleMonthlyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d14ec0545683cfea1d08bdce23b4fab826e8a82de001d547119eaba2199f46eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWeekDayOfMonth")
    def put_week_day_of_month(
        self,
        *,
        day_of_week: builtins.str,
        week_ordinal: jsii.Number,
        day_offset: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day_of_week: A day of the week. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#day_of_week OsConfigPatchDeployment#day_of_week}
        :param week_ordinal: Week number in a month. 1-4 indicates the 1st to 4th week of the month. -1 indicates the last week of the month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#week_ordinal OsConfigPatchDeployment#week_ordinal}
        :param day_offset: Represents the number of days before or after the given week day of month that the patch deployment is scheduled for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#day_offset OsConfigPatchDeployment#day_offset}
        '''
        value = OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth(
            day_of_week=day_of_week, week_ordinal=week_ordinal, day_offset=day_offset
        )

        return typing.cast(None, jsii.invoke(self, "putWeekDayOfMonth", [value]))

    @jsii.member(jsii_name="resetMonthDay")
    def reset_month_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthDay", []))

    @jsii.member(jsii_name="resetWeekDayOfMonth")
    def reset_week_day_of_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekDayOfMonth", []))

    @builtins.property
    @jsii.member(jsii_name="weekDayOfMonth")
    def week_day_of_month(
        self,
    ) -> "OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonthOutputReference":
        return typing.cast("OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonthOutputReference", jsii.get(self, "weekDayOfMonth"))

    @builtins.property
    @jsii.member(jsii_name="monthDayInput")
    def month_day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthDayInput"))

    @builtins.property
    @jsii.member(jsii_name="weekDayOfMonthInput")
    def week_day_of_month_input(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth"]:
        return typing.cast(typing.Optional["OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth"], jsii.get(self, "weekDayOfMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="monthDay")
    def month_day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "monthDay"))

    @month_day.setter
    def month_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8adfbbe30372da2d9cb27e707f4d7f638e6214d870acf9cb32ea96053cd6eff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentRecurringScheduleMonthly]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentRecurringScheduleMonthly], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentRecurringScheduleMonthly],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c756789114051ecdd7c6e4ecbc0481cad9099676aafd13dac542f63b39b86ed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth",
    jsii_struct_bases=[],
    name_mapping={
        "day_of_week": "dayOfWeek",
        "week_ordinal": "weekOrdinal",
        "day_offset": "dayOffset",
    },
)
class OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth:
    def __init__(
        self,
        *,
        day_of_week: builtins.str,
        week_ordinal: jsii.Number,
        day_offset: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day_of_week: A day of the week. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#day_of_week OsConfigPatchDeployment#day_of_week}
        :param week_ordinal: Week number in a month. 1-4 indicates the 1st to 4th week of the month. -1 indicates the last week of the month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#week_ordinal OsConfigPatchDeployment#week_ordinal}
        :param day_offset: Represents the number of days before or after the given week day of month that the patch deployment is scheduled for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#day_offset OsConfigPatchDeployment#day_offset}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0800e3ff81f9f33896c5fe23d5a04ea8f510c3d954891b13620cf656a73d54d)
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument week_ordinal", value=week_ordinal, expected_type=type_hints["week_ordinal"])
            check_type(argname="argument day_offset", value=day_offset, expected_type=type_hints["day_offset"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_week": day_of_week,
            "week_ordinal": week_ordinal,
        }
        if day_offset is not None:
            self._values["day_offset"] = day_offset

    @builtins.property
    def day_of_week(self) -> builtins.str:
        '''A day of the week. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#day_of_week OsConfigPatchDeployment#day_of_week}
        '''
        result = self._values.get("day_of_week")
        assert result is not None, "Required property 'day_of_week' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def week_ordinal(self) -> jsii.Number:
        '''Week number in a month.

        1-4 indicates the 1st to 4th week of the month. -1 indicates the last week of the month.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#week_ordinal OsConfigPatchDeployment#week_ordinal}
        '''
        result = self._values.get("week_ordinal")
        assert result is not None, "Required property 'week_ordinal' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def day_offset(self) -> typing.Optional[jsii.Number]:
        '''Represents the number of days before or after the given week day of month that the patch deployment is scheduled for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#day_offset OsConfigPatchDeployment#day_offset}
        '''
        result = self._values.get("day_offset")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__880238f6079773b7887e569e9dcada19c821796d9f3aaf463653f0a4a2d87949)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDayOffset")
    def reset_day_offset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDayOffset", []))

    @builtins.property
    @jsii.member(jsii_name="dayOffsetInput")
    def day_offset_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayOffsetInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekInput")
    def day_of_week_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="weekOrdinalInput")
    def week_ordinal_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weekOrdinalInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOffset")
    def day_offset(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dayOffset"))

    @day_offset.setter
    def day_offset(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e4fe426e1a72be57eeed8753437b73d6dc7eefea7ed2a7160732aae8972a8d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfWeek"))

    @day_of_week.setter
    def day_of_week(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f045a14d728b8e7deed807656a57c9ff89b7df2679d29e2c550f105a4b159ed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekOrdinal")
    def week_ordinal(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weekOrdinal"))

    @week_ordinal.setter
    def week_ordinal(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__323ece42727fac786f23bb9cea31c7e53d8b4a15c80a1931510fb3cb4a89c509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekOrdinal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1c910002e070e2f1852d4628658ff3623baa5311aba476e631cd0fb6786b36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigPatchDeploymentRecurringScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentRecurringScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15b19b5db97019150db622c2944df1f5095770c6ef6fc42590c053b0143b64a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMonthly")
    def put_monthly(
        self,
        *,
        month_day: typing.Optional[jsii.Number] = None,
        week_day_of_month: typing.Optional[typing.Union[OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param month_day: One day of the month. 1-31 indicates the 1st to the 31st day. -1 indicates the last day of the month. Months without the target day will be skipped. For example, a schedule to run "every month on the 31st" will not run in February, April, June, etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#month_day OsConfigPatchDeployment#month_day}
        :param week_day_of_month: week_day_of_month block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#week_day_of_month OsConfigPatchDeployment#week_day_of_month}
        '''
        value = OsConfigPatchDeploymentRecurringScheduleMonthly(
            month_day=month_day, week_day_of_month=week_day_of_month
        )

        return typing.cast(None, jsii.invoke(self, "putMonthly", [value]))

    @jsii.member(jsii_name="putTimeOfDay")
    def put_time_of_day(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#hours OsConfigPatchDeployment#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#minutes OsConfigPatchDeployment#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#nanos OsConfigPatchDeployment#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#seconds OsConfigPatchDeployment#seconds}
        '''
        value = OsConfigPatchDeploymentRecurringScheduleTimeOfDay(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putTimeOfDay", [value]))

    @jsii.member(jsii_name="putTimeZone")
    def put_time_zone(
        self,
        *,
        id: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: IANA Time Zone Database time zone, e.g. "America/New_York". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#id OsConfigPatchDeployment#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param version: IANA Time Zone Database version number, e.g. "2019a". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#version OsConfigPatchDeployment#version}
        '''
        value = OsConfigPatchDeploymentRecurringScheduleTimeZone(
            id=id, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putTimeZone", [value]))

    @jsii.member(jsii_name="putWeekly")
    def put_weekly(self, *, day_of_week: builtins.str) -> None:
        '''
        :param day_of_week: IANA Time Zone Database time zone, e.g. "America/New_York". Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#day_of_week OsConfigPatchDeployment#day_of_week}
        '''
        value = OsConfigPatchDeploymentRecurringScheduleWeekly(day_of_week=day_of_week)

        return typing.cast(None, jsii.invoke(self, "putWeekly", [value]))

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetMonthly")
    def reset_monthly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthly", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @jsii.member(jsii_name="resetWeekly")
    def reset_weekly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekly", []))

    @builtins.property
    @jsii.member(jsii_name="lastExecuteTime")
    def last_execute_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastExecuteTime"))

    @builtins.property
    @jsii.member(jsii_name="monthly")
    def monthly(self) -> OsConfigPatchDeploymentRecurringScheduleMonthlyOutputReference:
        return typing.cast(OsConfigPatchDeploymentRecurringScheduleMonthlyOutputReference, jsii.get(self, "monthly"))

    @builtins.property
    @jsii.member(jsii_name="nextExecuteTime")
    def next_execute_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextExecuteTime"))

    @builtins.property
    @jsii.member(jsii_name="timeOfDay")
    def time_of_day(
        self,
    ) -> "OsConfigPatchDeploymentRecurringScheduleTimeOfDayOutputReference":
        return typing.cast("OsConfigPatchDeploymentRecurringScheduleTimeOfDayOutputReference", jsii.get(self, "timeOfDay"))

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(
        self,
    ) -> "OsConfigPatchDeploymentRecurringScheduleTimeZoneOutputReference":
        return typing.cast("OsConfigPatchDeploymentRecurringScheduleTimeZoneOutputReference", jsii.get(self, "timeZone"))

    @builtins.property
    @jsii.member(jsii_name="weekly")
    def weekly(self) -> "OsConfigPatchDeploymentRecurringScheduleWeeklyOutputReference":
        return typing.cast("OsConfigPatchDeploymentRecurringScheduleWeeklyOutputReference", jsii.get(self, "weekly"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="monthlyInput")
    def monthly_input(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentRecurringScheduleMonthly]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentRecurringScheduleMonthly], jsii.get(self, "monthlyInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeOfDayInput")
    def time_of_day_input(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentRecurringScheduleTimeOfDay"]:
        return typing.cast(typing.Optional["OsConfigPatchDeploymentRecurringScheduleTimeOfDay"], jsii.get(self, "timeOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentRecurringScheduleTimeZone"]:
        return typing.cast(typing.Optional["OsConfigPatchDeploymentRecurringScheduleTimeZone"], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyInput")
    def weekly_input(
        self,
    ) -> typing.Optional["OsConfigPatchDeploymentRecurringScheduleWeekly"]:
        return typing.cast(typing.Optional["OsConfigPatchDeploymentRecurringScheduleWeekly"], jsii.get(self, "weeklyInput"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d88bf87e6b3c1fa30d119c8d9124ff18990fb5dbbac18f0d2e3419e32f4e6d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__533af2411b09e2ee0b50971396819bb0b8a25cf62994db75946fa7ff292b1995)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentRecurringSchedule]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentRecurringSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentRecurringSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604acc929422986e69d1da9bd73dc339a730e4dbb909b6ba4dfd9aeda0c8c3f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentRecurringScheduleTimeOfDay",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class OsConfigPatchDeploymentRecurringScheduleTimeOfDay:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#hours OsConfigPatchDeployment#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#minutes OsConfigPatchDeployment#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#nanos OsConfigPatchDeployment#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#seconds OsConfigPatchDeployment#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe7e8e156e8d5c4af56684d3f1bd35b0ee787ce5c6b9529f79b09d8b39976e3)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hours is not None:
            self._values["hours"] = hours
        if minutes is not None:
            self._values["minutes"] = minutes
        if nanos is not None:
            self._values["nanos"] = nanos
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def hours(self) -> typing.Optional[jsii.Number]:
        '''Hours of day in 24 hour format.

        Should be from 0 to 23.
        An API may choose to allow the value "24:00:00" for scenarios like business closing time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#hours OsConfigPatchDeployment#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day. Must be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#minutes OsConfigPatchDeployment#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#nanos OsConfigPatchDeployment#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time.

        Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#seconds OsConfigPatchDeployment#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentRecurringScheduleTimeOfDay(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentRecurringScheduleTimeOfDayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentRecurringScheduleTimeOfDayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c66fda7fd08ac38eb402515035e20244b54a57efbf4766405acfff15c48c01b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHours")
    def reset_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHours", []))

    @jsii.member(jsii_name="resetMinutes")
    def reset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinutes", []))

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @jsii.member(jsii_name="resetSeconds")
    def reset_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d376b4874478d6848bea1312d9a22c1dd0bbf61e83f3cd1a397b93c7c57e3937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e703bee7c03cdc23466cfa7639fb4a2dddfe14eaf9041b8e2f9eb0172f304da9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3453b027a5a8cb67a010bb88cb51b73ab11b7e11b3bbf7d9a3a0e02a89d4cad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c5937f75233fb173eb66a062e3e358a3494574fcf60cf667eccbbc409ed1a57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentRecurringScheduleTimeOfDay]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentRecurringScheduleTimeOfDay], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentRecurringScheduleTimeOfDay],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d7339f0b06ac03db821102a2080deb9db24e92c7ddf93a0f4022b9b038fd01a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentRecurringScheduleTimeZone",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "version": "version"},
)
class OsConfigPatchDeploymentRecurringScheduleTimeZone:
    def __init__(
        self,
        *,
        id: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: IANA Time Zone Database time zone, e.g. "America/New_York". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#id OsConfigPatchDeployment#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param version: IANA Time Zone Database version number, e.g. "2019a". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#version OsConfigPatchDeployment#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce6145a19c78ddc31bca64182264c34fa02ce3a3aa7e8fe1e7165577fb404bd)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def id(self) -> builtins.str:
        '''IANA Time Zone Database time zone, e.g. "America/New_York".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#id OsConfigPatchDeployment#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''IANA Time Zone Database version number, e.g. "2019a".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#version OsConfigPatchDeployment#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentRecurringScheduleTimeZone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentRecurringScheduleTimeZoneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentRecurringScheduleTimeZoneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7d7ccb90ad48a8cf242bb6376e563e219fa88602d3d72d62090cfd7d7b2b020)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ebe1f95637d8b3e900f4785091f3f706067ef0ee5c5957848d7c3e6d41b547d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1688402f0c951aa0681b7ef57455575e7e6c6a0bdff789f868a56f038177a005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentRecurringScheduleTimeZone]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentRecurringScheduleTimeZone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentRecurringScheduleTimeZone],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ee91f93ac0546b1445ca5ca54818fe6a481916b7e02cf84c54a0fe11f019b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentRecurringScheduleWeekly",
    jsii_struct_bases=[],
    name_mapping={"day_of_week": "dayOfWeek"},
)
class OsConfigPatchDeploymentRecurringScheduleWeekly:
    def __init__(self, *, day_of_week: builtins.str) -> None:
        '''
        :param day_of_week: IANA Time Zone Database time zone, e.g. "America/New_York". Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#day_of_week OsConfigPatchDeployment#day_of_week}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8d486747a9f9b9bf976db94116eb08c6911655101b746e0278a0cdb3700dfb9)
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_week": day_of_week,
        }

    @builtins.property
    def day_of_week(self) -> builtins.str:
        '''IANA Time Zone Database time zone, e.g. "America/New_York". Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#day_of_week OsConfigPatchDeployment#day_of_week}
        '''
        result = self._values.get("day_of_week")
        assert result is not None, "Required property 'day_of_week' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentRecurringScheduleWeekly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentRecurringScheduleWeeklyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentRecurringScheduleWeeklyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b616820ac11d6d695e157d96db207c5862d16b101f157653a956254b779e07df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekInput")
    def day_of_week_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfWeek"))

    @day_of_week.setter
    def day_of_week(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b50958d920a5b626f311eaf3bf09d528a2d72acd02fd2b68e9ce08a305351c01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentRecurringScheduleWeekly]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentRecurringScheduleWeekly], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentRecurringScheduleWeekly],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69da3001d8637f7fc6760eeb605af1394afa534b32212ad520173179cf7d3020)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentRollout",
    jsii_struct_bases=[],
    name_mapping={"disruption_budget": "disruptionBudget", "mode": "mode"},
)
class OsConfigPatchDeploymentRollout:
    def __init__(
        self,
        *,
        disruption_budget: typing.Union["OsConfigPatchDeploymentRolloutDisruptionBudget", typing.Dict[builtins.str, typing.Any]],
        mode: builtins.str,
    ) -> None:
        '''
        :param disruption_budget: disruption_budget block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#disruption_budget OsConfigPatchDeployment#disruption_budget}
        :param mode: Mode of the patch rollout. Possible values: ["ZONE_BY_ZONE", "CONCURRENT_ZONES"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#mode OsConfigPatchDeployment#mode}
        '''
        if isinstance(disruption_budget, dict):
            disruption_budget = OsConfigPatchDeploymentRolloutDisruptionBudget(**disruption_budget)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d35802201772d52172a97b87a0cfd09dc33be1dd67a10c6681933265b4da40f5)
            check_type(argname="argument disruption_budget", value=disruption_budget, expected_type=type_hints["disruption_budget"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disruption_budget": disruption_budget,
            "mode": mode,
        }

    @builtins.property
    def disruption_budget(self) -> "OsConfigPatchDeploymentRolloutDisruptionBudget":
        '''disruption_budget block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#disruption_budget OsConfigPatchDeployment#disruption_budget}
        '''
        result = self._values.get("disruption_budget")
        assert result is not None, "Required property 'disruption_budget' is missing"
        return typing.cast("OsConfigPatchDeploymentRolloutDisruptionBudget", result)

    @builtins.property
    def mode(self) -> builtins.str:
        '''Mode of the patch rollout. Possible values: ["ZONE_BY_ZONE", "CONCURRENT_ZONES"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#mode OsConfigPatchDeployment#mode}
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentRollout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentRolloutDisruptionBudget",
    jsii_struct_bases=[],
    name_mapping={"fixed": "fixed", "percentage": "percentage"},
)
class OsConfigPatchDeploymentRolloutDisruptionBudget:
    def __init__(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: Specifies a fixed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#fixed OsConfigPatchDeployment#fixed}
        :param percentage: Specifies the relative value defined as a percentage, which will be multiplied by a reference value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#percentage OsConfigPatchDeployment#percentage}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b886dcc4ec44777c744b11e56fb0c3aaa0a169810942fe1c6f6dfd45a580f45)
            check_type(argname="argument fixed", value=fixed, expected_type=type_hints["fixed"])
            check_type(argname="argument percentage", value=percentage, expected_type=type_hints["percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fixed is not None:
            self._values["fixed"] = fixed
        if percentage is not None:
            self._values["percentage"] = percentage

    @builtins.property
    def fixed(self) -> typing.Optional[jsii.Number]:
        '''Specifies a fixed value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#fixed OsConfigPatchDeployment#fixed}
        '''
        result = self._values.get("fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percentage(self) -> typing.Optional[jsii.Number]:
        '''Specifies the relative value defined as a percentage, which will be multiplied by a reference value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#percentage OsConfigPatchDeployment#percentage}
        '''
        result = self._values.get("percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentRolloutDisruptionBudget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentRolloutDisruptionBudgetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentRolloutDisruptionBudgetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af1c21b3cc2af22d87fe191e9a4a31e7d9c3dcbb66951a8302a7c804945f6868)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFixed")
    def reset_fixed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixed", []))

    @jsii.member(jsii_name="resetPercentage")
    def reset_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPercentage", []))

    @builtins.property
    @jsii.member(jsii_name="fixedInput")
    def fixed_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fixedInput"))

    @builtins.property
    @jsii.member(jsii_name="percentageInput")
    def percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentageInput"))

    @builtins.property
    @jsii.member(jsii_name="fixed")
    def fixed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fixed"))

    @fixed.setter
    def fixed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b24703f08ffdfe204fd8837eecff033018911c88905d4495c6c1b874ffce13e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percentage")
    def percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentage"))

    @percentage.setter
    def percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deafc7e6ade61be5de13a5cda1229b3a61e3de348a0c1f042d864209a96176f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentRolloutDisruptionBudget]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentRolloutDisruptionBudget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentRolloutDisruptionBudget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61cc1228a17a3e6f79c32776163fe77a97baf341c3d5af31dcfd3de2fd204206)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigPatchDeploymentRolloutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentRolloutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a72a493ae62d68bb53622abf0ee4d2d7cb2a521174321bb521b4d5d087ec9204)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDisruptionBudget")
    def put_disruption_budget(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: Specifies a fixed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#fixed OsConfigPatchDeployment#fixed}
        :param percentage: Specifies the relative value defined as a percentage, which will be multiplied by a reference value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#percentage OsConfigPatchDeployment#percentage}
        '''
        value = OsConfigPatchDeploymentRolloutDisruptionBudget(
            fixed=fixed, percentage=percentage
        )

        return typing.cast(None, jsii.invoke(self, "putDisruptionBudget", [value]))

    @builtins.property
    @jsii.member(jsii_name="disruptionBudget")
    def disruption_budget(
        self,
    ) -> OsConfigPatchDeploymentRolloutDisruptionBudgetOutputReference:
        return typing.cast(OsConfigPatchDeploymentRolloutDisruptionBudgetOutputReference, jsii.get(self, "disruptionBudget"))

    @builtins.property
    @jsii.member(jsii_name="disruptionBudgetInput")
    def disruption_budget_input(
        self,
    ) -> typing.Optional[OsConfigPatchDeploymentRolloutDisruptionBudget]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentRolloutDisruptionBudget], jsii.get(self, "disruptionBudgetInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__249d9632693a153142fedd92b305bc1759401fbc232d51ac6f7a096f19703d6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OsConfigPatchDeploymentRollout]:
        return typing.cast(typing.Optional[OsConfigPatchDeploymentRollout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigPatchDeploymentRollout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f20e32e152596b91b9aa96a8f2f4fdb926e3e28f3de7755b2180c7e7b0cfae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class OsConfigPatchDeploymentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#create OsConfigPatchDeployment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#delete OsConfigPatchDeployment#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d27a2fe66b40fbf92e64f89974a40019c480a0afae2179bdda025dac0e69fd47)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#create OsConfigPatchDeployment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_patch_deployment#delete OsConfigPatchDeployment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigPatchDeploymentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigPatchDeploymentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigPatchDeployment.OsConfigPatchDeploymentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5bc02d16638ebecfd3842810a25720f1c7257b85bb49606dc45e25dd7f4ff99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a95a993d95465f89de04091a56539c9bd9ad2766b9047d3d6b58e39a72d5a605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2d9ce3054a8a18eac08b6e725ac2f20612fa2aceea1fe9fec0d91a9c223d48a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigPatchDeploymentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigPatchDeploymentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigPatchDeploymentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__164b845709754d29002e01933cd44ab1b15ac09486c53e7e4c011c9ebcfdcf91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OsConfigPatchDeployment",
    "OsConfigPatchDeploymentConfig",
    "OsConfigPatchDeploymentInstanceFilter",
    "OsConfigPatchDeploymentInstanceFilterGroupLabels",
    "OsConfigPatchDeploymentInstanceFilterGroupLabelsList",
    "OsConfigPatchDeploymentInstanceFilterGroupLabelsOutputReference",
    "OsConfigPatchDeploymentInstanceFilterOutputReference",
    "OsConfigPatchDeploymentOneTimeSchedule",
    "OsConfigPatchDeploymentOneTimeScheduleOutputReference",
    "OsConfigPatchDeploymentPatchConfig",
    "OsConfigPatchDeploymentPatchConfigApt",
    "OsConfigPatchDeploymentPatchConfigAptOutputReference",
    "OsConfigPatchDeploymentPatchConfigGoo",
    "OsConfigPatchDeploymentPatchConfigGooOutputReference",
    "OsConfigPatchDeploymentPatchConfigOutputReference",
    "OsConfigPatchDeploymentPatchConfigPostStep",
    "OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig",
    "OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject",
    "OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObjectOutputReference",
    "OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigOutputReference",
    "OsConfigPatchDeploymentPatchConfigPostStepOutputReference",
    "OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig",
    "OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject",
    "OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObjectOutputReference",
    "OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigOutputReference",
    "OsConfigPatchDeploymentPatchConfigPreStep",
    "OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig",
    "OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject",
    "OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObjectOutputReference",
    "OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigOutputReference",
    "OsConfigPatchDeploymentPatchConfigPreStepOutputReference",
    "OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig",
    "OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject",
    "OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObjectOutputReference",
    "OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigOutputReference",
    "OsConfigPatchDeploymentPatchConfigWindowsUpdate",
    "OsConfigPatchDeploymentPatchConfigWindowsUpdateOutputReference",
    "OsConfigPatchDeploymentPatchConfigYum",
    "OsConfigPatchDeploymentPatchConfigYumOutputReference",
    "OsConfigPatchDeploymentPatchConfigZypper",
    "OsConfigPatchDeploymentPatchConfigZypperOutputReference",
    "OsConfigPatchDeploymentRecurringSchedule",
    "OsConfigPatchDeploymentRecurringScheduleMonthly",
    "OsConfigPatchDeploymentRecurringScheduleMonthlyOutputReference",
    "OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth",
    "OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonthOutputReference",
    "OsConfigPatchDeploymentRecurringScheduleOutputReference",
    "OsConfigPatchDeploymentRecurringScheduleTimeOfDay",
    "OsConfigPatchDeploymentRecurringScheduleTimeOfDayOutputReference",
    "OsConfigPatchDeploymentRecurringScheduleTimeZone",
    "OsConfigPatchDeploymentRecurringScheduleTimeZoneOutputReference",
    "OsConfigPatchDeploymentRecurringScheduleWeekly",
    "OsConfigPatchDeploymentRecurringScheduleWeeklyOutputReference",
    "OsConfigPatchDeploymentRollout",
    "OsConfigPatchDeploymentRolloutDisruptionBudget",
    "OsConfigPatchDeploymentRolloutDisruptionBudgetOutputReference",
    "OsConfigPatchDeploymentRolloutOutputReference",
    "OsConfigPatchDeploymentTimeouts",
    "OsConfigPatchDeploymentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__943ab19be923e9acd31661d5dda9109c4f13c63b6c16132d5df4fd9424eb1065(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    instance_filter: typing.Union[OsConfigPatchDeploymentInstanceFilter, typing.Dict[builtins.str, typing.Any]],
    patch_deployment_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    duration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    one_time_schedule: typing.Optional[typing.Union[OsConfigPatchDeploymentOneTimeSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    patch_config: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    recurring_schedule: typing.Optional[typing.Union[OsConfigPatchDeploymentRecurringSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    rollout: typing.Optional[typing.Union[OsConfigPatchDeploymentRollout, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[OsConfigPatchDeploymentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4eb8d73ba51fe651b94e8d24db7ca085898ec9526b99b0d523e7d50a4874e8f7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a79eb875b5eddd55022dfaef75ef0b133f2863140f903b57982b654ad58edcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8bb25ac71c9ccd6715342eaa22fd0fae143a6a521c62db5abb7186debbfda80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c2bf16d0de8cfdc0eb7340912516c71f07db29a4c39c49b42c843580ca683b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88658321593b9d4e0ba646a9e0c715a0bd30b5f8227e24d0687f42aa9a5c2521(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7601cf0772e60ef2af7b011222a3e080fd26eb01407b0cd9aeb151d46a13085(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6efb0b2adcf625fce1e74b0093d770ab7f7e24f4efdc4632378cb7203471985c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_filter: typing.Union[OsConfigPatchDeploymentInstanceFilter, typing.Dict[builtins.str, typing.Any]],
    patch_deployment_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    duration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    one_time_schedule: typing.Optional[typing.Union[OsConfigPatchDeploymentOneTimeSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    patch_config: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    recurring_schedule: typing.Optional[typing.Union[OsConfigPatchDeploymentRecurringSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    rollout: typing.Optional[typing.Union[OsConfigPatchDeploymentRollout, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[OsConfigPatchDeploymentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643761843ed240dce48982d376cdd4eb89781c7e0d2bc366f5b9770032bd6d32(
    *,
    all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    group_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigPatchDeploymentInstanceFilterGroupLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    instances: typing.Optional[typing.Sequence[builtins.str]] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a1d228bda81d279106aef70d2e69ccb5bac2105841dbb3d5241a2ea5579939(
    *,
    labels: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd9e6c32b248832554544eb3978cdb5b1a92eedcde14c44e22be8f8f432ea57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7830fe07de60efe12f7751df7a054b11f1feefd84d8a69ac93ddba7160a603(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6a443de228257746ec543fd3635340836a226b6fe8dd258e80e96b5a04eceb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27909db9958713211a73fc64fd0f58619d6ec4d5c00b5d163afcd33a0c09112(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b202679fff2ceaae9123bde2ed8e9b4f5dd54848c5c78ede885f38a9a430f7da(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f91815ca685d813e0cb90d033667c9e6c465f06ecb8b5ef26a8ef985457bb44(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigPatchDeploymentInstanceFilterGroupLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d95eca9229d83ac8505d17c5eddb062e341278bffcc6d14c46232264bacac1c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43fac9ff0cb4d8e5ed2b8bcd3e10383ba5a8f422b1e796aa95b1af4a89d46fb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e6b2bf4bb31cd734bb22178ebf793d19f14c16e9a7cc76fb6a13b474e1586c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigPatchDeploymentInstanceFilterGroupLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fb82a21735f0f639961df306ca7d25576dd3cd481c03898af4ff98bccb489af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bea60b351c5afff7271c36be730ca7f43f71ac040a8978943f30aa78716ccf6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigPatchDeploymentInstanceFilterGroupLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__814bd8c0dc74f44e9758df2a1041228951986f5ef52a75857f7a883f2f4956b3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd712a76b354cb628c71dfdc61c1a6fcdf95b893f69dedaa179e46eaa0eb1fa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d6b83cf63a10346ceec2e9d42319c5dba20c5d88728a77b7d923f4b6451b7a5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef2c09be8c396a531d432e9549d31f419a463ee673bc18f99fbc4b881396c61(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432feb539c619cb2680e4ed04f061d57818fcbe8cf368edbbf01247ac5527696(
    value: typing.Optional[OsConfigPatchDeploymentInstanceFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9dbe85b65c0d561045f6a544540ed306de4feae8d20a70a336202f18fea9c1d(
    *,
    execute_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3da09f03f27e66efc1ff4801da5acd312348b4d15316968b54ba57f24a5d796(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f0379ae4b174467af47bf0116f537540e512f1efb3a133caf75aa44eba1ee9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a55549f359f2533bc2e5f91e969f0e323ad88e87cae9d6072ae9f2b1cf8c10e(
    value: typing.Optional[OsConfigPatchDeploymentOneTimeSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ddcbb161eb21d7c13581851bcbfd5c04c0eb7eb1b3775d41ac0ebae208d292(
    *,
    apt: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfigApt, typing.Dict[builtins.str, typing.Any]]] = None,
    goo: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfigGoo, typing.Dict[builtins.str, typing.Any]]] = None,
    mig_instances_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    post_step: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfigPostStep, typing.Dict[builtins.str, typing.Any]]] = None,
    pre_step: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfigPreStep, typing.Dict[builtins.str, typing.Any]]] = None,
    reboot_config: typing.Optional[builtins.str] = None,
    windows_update: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfigWindowsUpdate, typing.Dict[builtins.str, typing.Any]]] = None,
    yum: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfigYum, typing.Dict[builtins.str, typing.Any]]] = None,
    zypper: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfigZypper, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11255c0d071c1b7cd27fd0938b2106edda776a3cbb23c96f884b7f9540c9158e(
    *,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclusive_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef4b29da9ed6942268a1d3fe70db35d287e62aec29c072af11752ec287dc050b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9157649bef42030157398392ec0ad5f0ad6d3a17b739d1ed877fdf7561ef86(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca82a1f19e0245412b515f66bb41ee48ef86abb2b25dcb5c7eb8b1f8420cd4c1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a8d49191a36f5eece0c481dab76078069bbd456edb569399c4fa0c75a98c93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80968c8924fa5d215051fd6536260477c1a73f2a56f0d75f4a17eaf764f8f8f4(
    value: typing.Optional[OsConfigPatchDeploymentPatchConfigApt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9321de7c7730696f9408f19bfa409b27d9de3d644c2e6f9156606a7458fa7d9f(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c594a83b91a91924c498b3d7bc2588ce9a1f74caf6e61d00f72fc70ef6745d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc69e4378f0139732675532ceb7f9e66b15e80b4240877bca00c6a62f08bd11a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6543491fca539d077b56937454721dd8ff0e6a1506807373f38b88f240e00910(
    value: typing.Optional[OsConfigPatchDeploymentPatchConfigGoo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3845e42500292db065fab65d375aab2379b2e02285071dd3f88833c10baa7a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c3aa090438d34940a745aee137dd5a2f40895fad49e08d68b5245cf453b7410(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862eae0f29edf93f0f8056d7651cc6e559328cbc1890b7e3c862113193144352(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d2d58999548cf5ae4af8eed0a538d6d7aa71bbea572481471a364a54b4ef2d(
    value: typing.Optional[OsConfigPatchDeploymentPatchConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b747341b5aa29940aa4d149f6d2431b9c644319938091470c712157d6eac662(
    *,
    linux_exec_step_config: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    windows_exec_step_config: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49cf02daf973a2560fb1c33e6b0da27bca99178661501b7e40d77bc08ca102e9(
    *,
    allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    gcs_object: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject, typing.Dict[builtins.str, typing.Any]]] = None,
    interpreter: typing.Optional[builtins.str] = None,
    local_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f096eb0b609678712f2533f34918805a49fbe4813398724bf16947585cf509cc(
    *,
    bucket: builtins.str,
    generation_number: builtins.str,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07391f575c91e3a93a60211c5b051e7a70fb00857b8b06287f8ee0aca7a1eb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac031972290e61c228ea00c120c800578ae6df5622e0eaa8f877ed2c697182b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea0a3cebb5470018ca58c6af5c8153f889b1ea37e6e7971aa911555a769e71c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__987f86f62096532e2b3e8b9d53e7f8bdf8d1818486fe6bcd23688e848cfc91cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef46345114b8d603b6deef9b9620427101510645dd13a784aba91c123cbe1df(
    value: typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b35079d3ca19ed9e2b4da0cde8b5755398415b12ac2717c142da74d93256b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01abafd70d88bf3bad297863de93599e0e528d7841d79aef8cb20066ef8c9264(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6c3bd1278cb7a5732f15aa506f26cddc07f1a7f631cbc1028a9fb975fb7ae0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1491b90c429a77e156c69e59977a10df9c5f1172a87cf1cffed4ab198a88c71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a42accbd12d5e00d36a8653a10ab3b6fc3b7be5e8bce7e681e335e65ab55b5e(
    value: typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519d755934909d8dd94403dafa456280fd9af1f22454dbfaa47862c81367ba20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__074047a49c2bcf5d8ce14ce58b6e5b4eaaf80003ec7a8d48293bed5b07d3372a(
    value: typing.Optional[OsConfigPatchDeploymentPatchConfigPostStep],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6a0c42e69dbc99343e82b95ffef7e04d5e2aa786a4fa7fbc8a1b155c1f1249(
    *,
    allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    gcs_object: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject, typing.Dict[builtins.str, typing.Any]]] = None,
    interpreter: typing.Optional[builtins.str] = None,
    local_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca05eba3f92d223cc80e96e1bde2222b17e31dec5b022565124174ecb9b0f22d(
    *,
    bucket: builtins.str,
    generation_number: builtins.str,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7779f205d29fcbc271c05ae041c98164cc9bde754bb5b94ba3d0a0a529c784f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9d67ff35d5b94146e5433d259f9a4f8c9009e99679cb1faac0d6266fbf40c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb0066307e6addef255c6860be6f6c2a527bd8ca61c1e77c871cc848065c446c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c30366a7f407cf95adae9c4946de36fe005bb778367c5380f947e8413cedac84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f1bde4e24cbee09062e6ea3643c43117a47ae2b4bb2901602acd7df849a05d5(
    value: typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01feb26f838a44f68c1a0e8a145541484300e8a51dbe2ada9b2938cde19aade8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d78586a4aa17b2adecafbc7ca242d23126ba01cb0201e94cbb982ba7bf7c1b9a(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e60669c30c236e339421478ca9f5d5d24a9e4a780e828907746dc2e7004be0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e54c37779ba435d7981985c79a4c5119f5f972047d1e340b076c0421751ecc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08dfed580351bfb0174a85434d579ac3358361f05050f127039dcca6456a1699(
    value: typing.Optional[OsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f73bcfd3aad79ab1cd0cb853490db4c5a0305649368901927ee8023017fd8e(
    *,
    linux_exec_step_config: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    windows_exec_step_config: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70404ba3603a61108ffdd7ef3c6f6b94bb6c600e90b4086bf3ae168fedff4a2d(
    *,
    allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    gcs_object: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject, typing.Dict[builtins.str, typing.Any]]] = None,
    interpreter: typing.Optional[builtins.str] = None,
    local_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0917744929797d205a183dfa9915d742d094bb312f84980b53e89d67762885(
    *,
    bucket: builtins.str,
    generation_number: builtins.str,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc8d4a3b1a0bdfb21fba979015d277b3b6d01e18c1fb3bd371687f0201bb0090(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab94e3d045e6fd1c8b491f473abd238a177c7059fa235424426a2b106d8d827(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39e7f38d047236cac27445399af39450a99668797e67d0ff8d0ad473838c21e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae932e6aebf076dc854cee0dafc69f9a1402febfde42034cc33409a1c44b83d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8af32373e7458bb47e10b92eaeb61b252806469bd52206095bc40bc6f0cee04d(
    value: typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afce9a7f3ddce3e1524c5ab2d59176421e34f5948ca1dcd6ecc23d1d4d99b0f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f6a1f14621b88186cbd0d6495365d92527752798f99616a3b85a22c37d71fa(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30fb11f0eef4e7d92588ca20c38b839ebf314ac27128dc6aaf69cc4dda25d56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44caa7cd97a2eb0662bcf6890b2a341b3456a9f214bad1c43f75fdb61e637bb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222e4eca7204263c9c71033b22509c08376ec54c6293b4a0e3b2bf9135d18766(
    value: typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3d78d1093b3fb85330873ccf03bf99544bd50165897bba521bc8cf5b9e471d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff447cea012eb5a42b4eaa8fd02f536c735b146913554457f65a378e6eb2e37(
    value: typing.Optional[OsConfigPatchDeploymentPatchConfigPreStep],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac5879d46f17ff21ac4553d4c6e88ea6cd666506a0d6335072a097aa26021eb(
    *,
    allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    gcs_object: typing.Optional[typing.Union[OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject, typing.Dict[builtins.str, typing.Any]]] = None,
    interpreter: typing.Optional[builtins.str] = None,
    local_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb3321bcc0e01bcda266f1f28564684ded295ba56c0b807178b14b4ab1a2571(
    *,
    bucket: builtins.str,
    generation_number: builtins.str,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f304598356ac7fe4220ddb13030f4d1eae7ee32a22fb78266518eb4c28dd863(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c9af9bd324526e81cedb047760a93eb9fdc67d08e14fbf5a2b29e1fa88caab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3978570381b92a56d4e9ad7d8e27964415856769a50f804faab87b4e0be4110(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39a0c0790308c1fb03520e20f882fa4db5a9a26500f3d52afa6ca3ea612c580(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd3f11ab1515e98946ca527e2823ff78b8450efed55f9fb74111fdda9a5f6d5(
    value: typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff709820452bb925bfdb0d4962363845794d62c96a6dc6edddb28f82c8c03e76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fff6b73e4507eab2f8aec3729f940a92c5ab7a19a0b8f325aaa26634562b199(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d77a062dc40adfce26a55f78cd6374f2adb771ccbcdca339e3dd9f45297b2c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4b2b3bffa7b9d2d2e157aa7038032b498fef51ba4aafac4f62d3f52391f42d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26cc02f80ddc6d01e4b93c2caac7b32514c5a75036d370d85b7473315e94cfc(
    value: typing.Optional[OsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8df8d3945accab44bfb2f6e2b014fb0d993f09c43a15870431f001d7118e88f(
    *,
    classifications: typing.Optional[typing.Sequence[builtins.str]] = None,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclusive_patches: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7703f88560236f179b84a62a7b5f687c646735bed26033d2a5c1c016813f5037(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb4d962e605f776dc484b7d8e332d855f8fd894d67b7b1e56cd1f34856f8de0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4255ec252885871c3c98731380104d58b830511d97cfaa55016583b41aa5a6b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5506ec424385d9b32caedec134f41cf717d87f91b746a81da538a94f744a3cf5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd887e1629594e14ae8a447d43e1bfc8efdf646a28ab7a19bbaeb7dee263d3d(
    value: typing.Optional[OsConfigPatchDeploymentPatchConfigWindowsUpdate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80bb0ee099a30cf96b61b289378fab5117a915efb02f411a59f25520433be49c(
    *,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclusive_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    minimal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ffdf8f1c3b795df246b256c6a449fb906a1682d6901092ad8cb167db20fd17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75dfdd4115b8f8e7222400a4a9e5733ba80b6c360b70a7be79a008f48ed80f2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fefa99c975c7345ccfdc80ce6a84d45bd5e1e8299f3e5881bd2c1e3d8d2460(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a16d8969f83b396f03ca769fa81510be85de28d785ab2ba812bde62540ba88d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7983800e49453a73e09f5383c7cf655d406c40539e33116b398682c0b44681a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345eeba2f4cdc96b3fad5336841a16811a1861c5443edcf4b568d43d23c9308b(
    value: typing.Optional[OsConfigPatchDeploymentPatchConfigYum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a92e1e3ed254f0af63c4bf7739783129b4fa8dec1082b754f4e2b3e478b91a(
    *,
    categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclusive_patches: typing.Optional[typing.Sequence[builtins.str]] = None,
    severities: typing.Optional[typing.Sequence[builtins.str]] = None,
    with_optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    with_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b2a661d5575c488ec2817c3dbae1b8ce3321545faf5a79ed6b2160fe0ab664(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66290a195e9774aaa3a6ad322b472f07a08c012513a75044953b7575c9066e8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a952ce192da371286705d302850201c1d21205ec051a49bfe737e3f3629f9c5c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe67097d31f42b7d76f0be3a0560aed0053d03d35d3eeb1f75c13300f64e5561(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38218f1465049568a1b82644aee2ebe537632b1feb9c2f90b766de75e334661a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b9b2141488c74b2e5af950e7f42eb670ebdf8a8951a884cb08df70d5a56cfc6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fe10db6fe5eb85bd97a533f6ccb626cacba4008c230135fa19b12670fb1351(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b549d504977e968629683615f3ea0d5dc2d3f6a219aecf7467ddf9b1e41df0(
    value: typing.Optional[OsConfigPatchDeploymentPatchConfigZypper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c2fb3d2babe9bf4340c4571955491cfae5db04185ca185c6e76e2e33d9a3d8(
    *,
    time_of_day: typing.Union[OsConfigPatchDeploymentRecurringScheduleTimeOfDay, typing.Dict[builtins.str, typing.Any]],
    time_zone: typing.Union[OsConfigPatchDeploymentRecurringScheduleTimeZone, typing.Dict[builtins.str, typing.Any]],
    end_time: typing.Optional[builtins.str] = None,
    monthly: typing.Optional[typing.Union[OsConfigPatchDeploymentRecurringScheduleMonthly, typing.Dict[builtins.str, typing.Any]]] = None,
    start_time: typing.Optional[builtins.str] = None,
    weekly: typing.Optional[typing.Union[OsConfigPatchDeploymentRecurringScheduleWeekly, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a33ad52bb5d86e5838811bdbfd6577d7345edcee4025edfaaa38a5b1397dc6e(
    *,
    month_day: typing.Optional[jsii.Number] = None,
    week_day_of_month: typing.Optional[typing.Union[OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d14ec0545683cfea1d08bdce23b4fab826e8a82de001d547119eaba2199f46eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8adfbbe30372da2d9cb27e707f4d7f638e6214d870acf9cb32ea96053cd6eff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c756789114051ecdd7c6e4ecbc0481cad9099676aafd13dac542f63b39b86ed0(
    value: typing.Optional[OsConfigPatchDeploymentRecurringScheduleMonthly],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0800e3ff81f9f33896c5fe23d5a04ea8f510c3d954891b13620cf656a73d54d(
    *,
    day_of_week: builtins.str,
    week_ordinal: jsii.Number,
    day_offset: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880238f6079773b7887e569e9dcada19c821796d9f3aaf463653f0a4a2d87949(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e4fe426e1a72be57eeed8753437b73d6dc7eefea7ed2a7160732aae8972a8d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f045a14d728b8e7deed807656a57c9ff89b7df2679d29e2c550f105a4b159ed0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323ece42727fac786f23bb9cea31c7e53d8b4a15c80a1931510fb3cb4a89c509(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1c910002e070e2f1852d4628658ff3623baa5311aba476e631cd0fb6786b36(
    value: typing.Optional[OsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b19b5db97019150db622c2944df1f5095770c6ef6fc42590c053b0143b64a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d88bf87e6b3c1fa30d119c8d9124ff18990fb5dbbac18f0d2e3419e32f4e6d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533af2411b09e2ee0b50971396819bb0b8a25cf62994db75946fa7ff292b1995(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604acc929422986e69d1da9bd73dc339a730e4dbb909b6ba4dfd9aeda0c8c3f1(
    value: typing.Optional[OsConfigPatchDeploymentRecurringSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe7e8e156e8d5c4af56684d3f1bd35b0ee787ce5c6b9529f79b09d8b39976e3(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c66fda7fd08ac38eb402515035e20244b54a57efbf4766405acfff15c48c01b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d376b4874478d6848bea1312d9a22c1dd0bbf61e83f3cd1a397b93c7c57e3937(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e703bee7c03cdc23466cfa7639fb4a2dddfe14eaf9041b8e2f9eb0172f304da9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3453b027a5a8cb67a010bb88cb51b73ab11b7e11b3bbf7d9a3a0e02a89d4cad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5937f75233fb173eb66a062e3e358a3494574fcf60cf667eccbbc409ed1a57(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7339f0b06ac03db821102a2080deb9db24e92c7ddf93a0f4022b9b038fd01a(
    value: typing.Optional[OsConfigPatchDeploymentRecurringScheduleTimeOfDay],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce6145a19c78ddc31bca64182264c34fa02ce3a3aa7e8fe1e7165577fb404bd(
    *,
    id: builtins.str,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d7ccb90ad48a8cf242bb6376e563e219fa88602d3d72d62090cfd7d7b2b020(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ebe1f95637d8b3e900f4785091f3f706067ef0ee5c5957848d7c3e6d41b547d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1688402f0c951aa0681b7ef57455575e7e6c6a0bdff789f868a56f038177a005(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ee91f93ac0546b1445ca5ca54818fe6a481916b7e02cf84c54a0fe11f019b4(
    value: typing.Optional[OsConfigPatchDeploymentRecurringScheduleTimeZone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d486747a9f9b9bf976db94116eb08c6911655101b746e0278a0cdb3700dfb9(
    *,
    day_of_week: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b616820ac11d6d695e157d96db207c5862d16b101f157653a956254b779e07df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50958d920a5b626f311eaf3bf09d528a2d72acd02fd2b68e9ce08a305351c01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69da3001d8637f7fc6760eeb605af1394afa534b32212ad520173179cf7d3020(
    value: typing.Optional[OsConfigPatchDeploymentRecurringScheduleWeekly],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35802201772d52172a97b87a0cfd09dc33be1dd67a10c6681933265b4da40f5(
    *,
    disruption_budget: typing.Union[OsConfigPatchDeploymentRolloutDisruptionBudget, typing.Dict[builtins.str, typing.Any]],
    mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b886dcc4ec44777c744b11e56fb0c3aaa0a169810942fe1c6f6dfd45a580f45(
    *,
    fixed: typing.Optional[jsii.Number] = None,
    percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1c21b3cc2af22d87fe191e9a4a31e7d9c3dcbb66951a8302a7c804945f6868(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24703f08ffdfe204fd8837eecff033018911c88905d4495c6c1b874ffce13e9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deafc7e6ade61be5de13a5cda1229b3a61e3de348a0c1f042d864209a96176f8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61cc1228a17a3e6f79c32776163fe77a97baf341c3d5af31dcfd3de2fd204206(
    value: typing.Optional[OsConfigPatchDeploymentRolloutDisruptionBudget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72a493ae62d68bb53622abf0ee4d2d7cb2a521174321bb521b4d5d087ec9204(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__249d9632693a153142fedd92b305bc1759401fbc232d51ac6f7a096f19703d6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f20e32e152596b91b9aa96a8f2f4fdb926e3e28f3de7755b2180c7e7b0cfae4(
    value: typing.Optional[OsConfigPatchDeploymentRollout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d27a2fe66b40fbf92e64f89974a40019c480a0afae2179bdda025dac0e69fd47(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5bc02d16638ebecfd3842810a25720f1c7257b85bb49606dc45e25dd7f4ff99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95a993d95465f89de04091a56539c9bd9ad2766b9047d3d6b58e39a72d5a605(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d9ce3054a8a18eac08b6e725ac2f20612fa2aceea1fe9fec0d91a9c223d48a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164b845709754d29002e01933cd44ab1b15ac09486c53e7e4c011c9ebcfdcf91(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigPatchDeploymentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

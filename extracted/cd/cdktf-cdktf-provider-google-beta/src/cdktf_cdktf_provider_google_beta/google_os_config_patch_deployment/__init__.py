r'''
# `google_os_config_patch_deployment`

Refer to the Terraform Registry for docs: [`google_os_config_patch_deployment`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment).
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


class GoogleOsConfigPatchDeployment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeployment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment google_os_config_patch_deployment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        instance_filter: typing.Union["GoogleOsConfigPatchDeploymentInstanceFilter", typing.Dict[builtins.str, typing.Any]],
        patch_deployment_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        duration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        one_time_schedule: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentOneTimeSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        patch_config: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        recurring_schedule: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentRecurringSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        rollout: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentRollout", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment google_os_config_patch_deployment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param instance_filter: instance_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#instance_filter GoogleOsConfigPatchDeployment#instance_filter}
        :param patch_deployment_id: A name for the patch deployment in the project. When creating a name the following rules apply: - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#patch_deployment_id GoogleOsConfigPatchDeployment#patch_deployment_id}
        :param description: Description of the patch deployment. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#description GoogleOsConfigPatchDeployment#description}
        :param duration: Duration of the patch. After the duration ends, the patch times out. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#duration GoogleOsConfigPatchDeployment#duration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#id GoogleOsConfigPatchDeployment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param one_time_schedule: one_time_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#one_time_schedule GoogleOsConfigPatchDeployment#one_time_schedule}
        :param patch_config: patch_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#patch_config GoogleOsConfigPatchDeployment#patch_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#project GoogleOsConfigPatchDeployment#project}.
        :param recurring_schedule: recurring_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#recurring_schedule GoogleOsConfigPatchDeployment#recurring_schedule}
        :param rollout: rollout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#rollout GoogleOsConfigPatchDeployment#rollout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#timeouts GoogleOsConfigPatchDeployment#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__342dc78866a3ce27e317642fd0e2d3572e4a0ea4534a872315cc8fb564821cb9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleOsConfigPatchDeploymentConfig(
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
        '''Generates CDKTF code for importing a GoogleOsConfigPatchDeployment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleOsConfigPatchDeployment to import.
        :param import_from_id: The id of the existing GoogleOsConfigPatchDeployment that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleOsConfigPatchDeployment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8504aa2edc8af77745c1c3fdc29bc636ba5f1c7486d545c99ecec7b28a615ed)
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
        group_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        instance_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param all: Target all VM instances in the project. If true, no other criteria is permitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#all GoogleOsConfigPatchDeployment#all}
        :param group_labels: group_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#group_labels GoogleOsConfigPatchDeployment#group_labels}
        :param instance_name_prefixes: Targets VMs whose name starts with one of these prefixes. Similar to labels, this is another way to group VMs when targeting configs, for example prefix="prod-". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#instance_name_prefixes GoogleOsConfigPatchDeployment#instance_name_prefixes}
        :param instances: Targets any of the VM instances specified. Instances are specified by their URI in the 'form zones/{{zone}}/instances/{{instance_name}}', 'projects/{{project_id}}/zones/{{zone}}/instances/{{instance_name}}', or 'https://www.googleapis.com/compute/v1/projects/{{project_id}}/zones/{{zone}}/instances/{{instance_name}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#instances GoogleOsConfigPatchDeployment#instances}
        :param zones: Targets VM instances in ANY of these zones. Leave empty to target VM instances in any zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#zones GoogleOsConfigPatchDeployment#zones}
        '''
        value = GoogleOsConfigPatchDeploymentInstanceFilter(
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
        :param execute_time: The desired patch job execution time. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#execute_time GoogleOsConfigPatchDeployment#execute_time}
        '''
        value = GoogleOsConfigPatchDeploymentOneTimeSchedule(execute_time=execute_time)

        return typing.cast(None, jsii.invoke(self, "putOneTimeSchedule", [value]))

    @jsii.member(jsii_name="putPatchConfig")
    def put_patch_config(
        self,
        *,
        apt: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigApt", typing.Dict[builtins.str, typing.Any]]] = None,
        goo: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigGoo", typing.Dict[builtins.str, typing.Any]]] = None,
        mig_instances_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        post_step: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPostStep", typing.Dict[builtins.str, typing.Any]]] = None,
        pre_step: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPreStep", typing.Dict[builtins.str, typing.Any]]] = None,
        reboot_config: typing.Optional[builtins.str] = None,
        windows_update: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdate", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#apt GoogleOsConfigPatchDeployment#apt}
        :param goo: goo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#goo GoogleOsConfigPatchDeployment#goo}
        :param mig_instances_allowed: Allows the patch job to run on Managed instance groups (MIGs). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#mig_instances_allowed GoogleOsConfigPatchDeployment#mig_instances_allowed}
        :param post_step: post_step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#post_step GoogleOsConfigPatchDeployment#post_step}
        :param pre_step: pre_step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#pre_step GoogleOsConfigPatchDeployment#pre_step}
        :param reboot_config: Post-patch reboot settings. Possible values: ["DEFAULT", "ALWAYS", "NEVER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#reboot_config GoogleOsConfigPatchDeployment#reboot_config}
        :param windows_update: windows_update block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#windows_update GoogleOsConfigPatchDeployment#windows_update}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#yum GoogleOsConfigPatchDeployment#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#zypper GoogleOsConfigPatchDeployment#zypper}
        '''
        value = GoogleOsConfigPatchDeploymentPatchConfig(
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
        time_of_day: typing.Union["GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDay", typing.Dict[builtins.str, typing.Any]],
        time_zone: typing.Union["GoogleOsConfigPatchDeploymentRecurringScheduleTimeZone", typing.Dict[builtins.str, typing.Any]],
        end_time: typing.Optional[builtins.str] = None,
        monthly: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentRecurringScheduleMonthly", typing.Dict[builtins.str, typing.Any]]] = None,
        start_time: typing.Optional[builtins.str] = None,
        weekly: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentRecurringScheduleWeekly", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param time_of_day: time_of_day block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#time_of_day GoogleOsConfigPatchDeployment#time_of_day}
        :param time_zone: time_zone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#time_zone GoogleOsConfigPatchDeployment#time_zone}
        :param end_time: The end time at which a recurring patch deployment schedule is no longer active. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#end_time GoogleOsConfigPatchDeployment#end_time}
        :param monthly: monthly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#monthly GoogleOsConfigPatchDeployment#monthly}
        :param start_time: The time that the recurring schedule becomes effective. Defaults to createTime of the patch deployment. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#start_time GoogleOsConfigPatchDeployment#start_time}
        :param weekly: weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#weekly GoogleOsConfigPatchDeployment#weekly}
        '''
        value = GoogleOsConfigPatchDeploymentRecurringSchedule(
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
        disruption_budget: typing.Union["GoogleOsConfigPatchDeploymentRolloutDisruptionBudget", typing.Dict[builtins.str, typing.Any]],
        mode: builtins.str,
    ) -> None:
        '''
        :param disruption_budget: disruption_budget block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#disruption_budget GoogleOsConfigPatchDeployment#disruption_budget}
        :param mode: Mode of the patch rollout. Possible values: ["ZONE_BY_ZONE", "CONCURRENT_ZONES"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#mode GoogleOsConfigPatchDeployment#mode}
        '''
        value = GoogleOsConfigPatchDeploymentRollout(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#create GoogleOsConfigPatchDeployment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#delete GoogleOsConfigPatchDeployment#delete}.
        '''
        value = GoogleOsConfigPatchDeploymentTimeouts(create=create, delete=delete)

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
    def instance_filter(
        self,
    ) -> "GoogleOsConfigPatchDeploymentInstanceFilterOutputReference":
        return typing.cast("GoogleOsConfigPatchDeploymentInstanceFilterOutputReference", jsii.get(self, "instanceFilter"))

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
    ) -> "GoogleOsConfigPatchDeploymentOneTimeScheduleOutputReference":
        return typing.cast("GoogleOsConfigPatchDeploymentOneTimeScheduleOutputReference", jsii.get(self, "oneTimeSchedule"))

    @builtins.property
    @jsii.member(jsii_name="patchConfig")
    def patch_config(self) -> "GoogleOsConfigPatchDeploymentPatchConfigOutputReference":
        return typing.cast("GoogleOsConfigPatchDeploymentPatchConfigOutputReference", jsii.get(self, "patchConfig"))

    @builtins.property
    @jsii.member(jsii_name="recurringSchedule")
    def recurring_schedule(
        self,
    ) -> "GoogleOsConfigPatchDeploymentRecurringScheduleOutputReference":
        return typing.cast("GoogleOsConfigPatchDeploymentRecurringScheduleOutputReference", jsii.get(self, "recurringSchedule"))

    @builtins.property
    @jsii.member(jsii_name="rollout")
    def rollout(self) -> "GoogleOsConfigPatchDeploymentRolloutOutputReference":
        return typing.cast("GoogleOsConfigPatchDeploymentRolloutOutputReference", jsii.get(self, "rollout"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleOsConfigPatchDeploymentTimeoutsOutputReference":
        return typing.cast("GoogleOsConfigPatchDeploymentTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentInstanceFilter"]:
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentInstanceFilter"], jsii.get(self, "instanceFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="oneTimeScheduleInput")
    def one_time_schedule_input(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentOneTimeSchedule"]:
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentOneTimeSchedule"], jsii.get(self, "oneTimeScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="patchConfigInput")
    def patch_config_input(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfig"]:
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfig"], jsii.get(self, "patchConfigInput"))

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
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentRecurringSchedule"]:
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentRecurringSchedule"], jsii.get(self, "recurringScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="rolloutInput")
    def rollout_input(self) -> typing.Optional["GoogleOsConfigPatchDeploymentRollout"]:
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentRollout"], jsii.get(self, "rolloutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleOsConfigPatchDeploymentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleOsConfigPatchDeploymentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd5fbf800bb05da942bc8ee60696ea76f34fe7257a63eae1845fe5c85831846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59d366d4407faa182e18497f1f6332fc7566e31e86c498cb59ed3d2119952428)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2d9df4b9547945f5fff037838f82ee0f62b81d0f0a8373341db9db92cf459b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="patchDeploymentId")
    def patch_deployment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "patchDeploymentId"))

    @patch_deployment_id.setter
    def patch_deployment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d3a28a12265a7e2d6055b2db02665874c76b1d49d69588ffa99c6d83d513dc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "patchDeploymentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed5df337f6ac52099f40affd08836c8c438ec0ddd5dbbe283b90b0851975205c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentConfig",
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
class GoogleOsConfigPatchDeploymentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        instance_filter: typing.Union["GoogleOsConfigPatchDeploymentInstanceFilter", typing.Dict[builtins.str, typing.Any]],
        patch_deployment_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        duration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        one_time_schedule: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentOneTimeSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        patch_config: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        recurring_schedule: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentRecurringSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        rollout: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentRollout", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param instance_filter: instance_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#instance_filter GoogleOsConfigPatchDeployment#instance_filter}
        :param patch_deployment_id: A name for the patch deployment in the project. When creating a name the following rules apply: - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#patch_deployment_id GoogleOsConfigPatchDeployment#patch_deployment_id}
        :param description: Description of the patch deployment. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#description GoogleOsConfigPatchDeployment#description}
        :param duration: Duration of the patch. After the duration ends, the patch times out. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#duration GoogleOsConfigPatchDeployment#duration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#id GoogleOsConfigPatchDeployment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param one_time_schedule: one_time_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#one_time_schedule GoogleOsConfigPatchDeployment#one_time_schedule}
        :param patch_config: patch_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#patch_config GoogleOsConfigPatchDeployment#patch_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#project GoogleOsConfigPatchDeployment#project}.
        :param recurring_schedule: recurring_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#recurring_schedule GoogleOsConfigPatchDeployment#recurring_schedule}
        :param rollout: rollout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#rollout GoogleOsConfigPatchDeployment#rollout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#timeouts GoogleOsConfigPatchDeployment#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(instance_filter, dict):
            instance_filter = GoogleOsConfigPatchDeploymentInstanceFilter(**instance_filter)
        if isinstance(one_time_schedule, dict):
            one_time_schedule = GoogleOsConfigPatchDeploymentOneTimeSchedule(**one_time_schedule)
        if isinstance(patch_config, dict):
            patch_config = GoogleOsConfigPatchDeploymentPatchConfig(**patch_config)
        if isinstance(recurring_schedule, dict):
            recurring_schedule = GoogleOsConfigPatchDeploymentRecurringSchedule(**recurring_schedule)
        if isinstance(rollout, dict):
            rollout = GoogleOsConfigPatchDeploymentRollout(**rollout)
        if isinstance(timeouts, dict):
            timeouts = GoogleOsConfigPatchDeploymentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__531544c18bb539618c5c4b8b7e75cf1ce86e442f715a8693b2b4bead42fc3027)
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
    def instance_filter(self) -> "GoogleOsConfigPatchDeploymentInstanceFilter":
        '''instance_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#instance_filter GoogleOsConfigPatchDeployment#instance_filter}
        '''
        result = self._values.get("instance_filter")
        assert result is not None, "Required property 'instance_filter' is missing"
        return typing.cast("GoogleOsConfigPatchDeploymentInstanceFilter", result)

    @builtins.property
    def patch_deployment_id(self) -> builtins.str:
        '''A name for the patch deployment in the project.

        When creating a name the following rules apply:

        - Must contain only lowercase letters, numbers, and hyphens.
        - Must start with a letter.
        - Must be between 1-63 characters.
        - Must end with a number or a letter.
        - Must be unique within the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#patch_deployment_id GoogleOsConfigPatchDeployment#patch_deployment_id}
        '''
        result = self._values.get("patch_deployment_id")
        assert result is not None, "Required property 'patch_deployment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the patch deployment. Length of the description is limited to 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#description GoogleOsConfigPatchDeployment#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def duration(self) -> typing.Optional[builtins.str]:
        '''Duration of the patch.

        After the duration ends, the patch times out.
        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#duration GoogleOsConfigPatchDeployment#duration}
        '''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#id GoogleOsConfigPatchDeployment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def one_time_schedule(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentOneTimeSchedule"]:
        '''one_time_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#one_time_schedule GoogleOsConfigPatchDeployment#one_time_schedule}
        '''
        result = self._values.get("one_time_schedule")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentOneTimeSchedule"], result)

    @builtins.property
    def patch_config(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfig"]:
        '''patch_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#patch_config GoogleOsConfigPatchDeployment#patch_config}
        '''
        result = self._values.get("patch_config")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#project GoogleOsConfigPatchDeployment#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recurring_schedule(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentRecurringSchedule"]:
        '''recurring_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#recurring_schedule GoogleOsConfigPatchDeployment#recurring_schedule}
        '''
        result = self._values.get("recurring_schedule")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentRecurringSchedule"], result)

    @builtins.property
    def rollout(self) -> typing.Optional["GoogleOsConfigPatchDeploymentRollout"]:
        '''rollout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#rollout GoogleOsConfigPatchDeployment#rollout}
        '''
        result = self._values.get("rollout")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentRollout"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleOsConfigPatchDeploymentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#timeouts GoogleOsConfigPatchDeployment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentInstanceFilter",
    jsii_struct_bases=[],
    name_mapping={
        "all": "all",
        "group_labels": "groupLabels",
        "instance_name_prefixes": "instanceNamePrefixes",
        "instances": "instances",
        "zones": "zones",
    },
)
class GoogleOsConfigPatchDeploymentInstanceFilter:
    def __init__(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        instance_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param all: Target all VM instances in the project. If true, no other criteria is permitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#all GoogleOsConfigPatchDeployment#all}
        :param group_labels: group_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#group_labels GoogleOsConfigPatchDeployment#group_labels}
        :param instance_name_prefixes: Targets VMs whose name starts with one of these prefixes. Similar to labels, this is another way to group VMs when targeting configs, for example prefix="prod-". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#instance_name_prefixes GoogleOsConfigPatchDeployment#instance_name_prefixes}
        :param instances: Targets any of the VM instances specified. Instances are specified by their URI in the 'form zones/{{zone}}/instances/{{instance_name}}', 'projects/{{project_id}}/zones/{{zone}}/instances/{{instance_name}}', or 'https://www.googleapis.com/compute/v1/projects/{{project_id}}/zones/{{zone}}/instances/{{instance_name}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#instances GoogleOsConfigPatchDeployment#instances}
        :param zones: Targets VM instances in ANY of these zones. Leave empty to target VM instances in any zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#zones GoogleOsConfigPatchDeployment#zones}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c27fcfc19550645c95f19db9d7a028449427202b2711299eb7b41e91f51aed0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#all GoogleOsConfigPatchDeployment#all}
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def group_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels"]]]:
        '''group_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#group_labels GoogleOsConfigPatchDeployment#group_labels}
        '''
        result = self._values.get("group_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels"]]], result)

    @builtins.property
    def instance_name_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Targets VMs whose name starts with one of these prefixes.

        Similar to labels, this is another way to group
        VMs when targeting configs, for example prefix="prod-".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#instance_name_prefixes GoogleOsConfigPatchDeployment#instance_name_prefixes}
        '''
        result = self._values.get("instance_name_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def instances(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Targets any of the VM instances specified. Instances are specified by their URI in the 'form zones/{{zone}}/instances/{{instance_name}}', 'projects/{{project_id}}/zones/{{zone}}/instances/{{instance_name}}', or 'https://www.googleapis.com/compute/v1/projects/{{project_id}}/zones/{{zone}}/instances/{{instance_name}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#instances GoogleOsConfigPatchDeployment#instances}
        '''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Targets VM instances in ANY of these zones. Leave empty to target VM instances in any zone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#zones GoogleOsConfigPatchDeployment#zones}
        '''
        result = self._values.get("zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentInstanceFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels"},
)
class GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels:
    def __init__(self, *, labels: typing.Mapping[builtins.str, builtins.str]) -> None:
        '''
        :param labels: Compute Engine instance labels that must be present for a VM instance to be targeted by this filter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#labels GoogleOsConfigPatchDeployment#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab3627c7ba02a6762baf21e62959d8441dd064f3d329279439d163ca8d315f51)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "labels": labels,
        }

    @builtins.property
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Compute Engine instance labels that must be present for a VM instance to be targeted by this filter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#labels GoogleOsConfigPatchDeployment#labels}
        '''
        result = self._values.get("labels")
        assert result is not None, "Required property 'labels' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentInstanceFilterGroupLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentInstanceFilterGroupLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__693589310bc12df90095ff27a9cb116c7c9b4acc7fa114e4cf1416da65db30f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigPatchDeploymentInstanceFilterGroupLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af81991b9948b3ae9794ec80c352c8edb481314ece06a1caf4a795bc3a36e32)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigPatchDeploymentInstanceFilterGroupLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c8fc7f14c147444f2faba28d4dce18c64a54ffbf2a1ef7cd1a8803ff96c31c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef953b14e9abdc6c20125891717b95da46619c1af7af466a84cdfa51cda5bf5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5afc7d2755fc71139717463fbbb3e2111357c48bfb5df697fee72eb38855a8db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60563f3769e71a350e0e34209fd215b408564d02ce7ab6c8043b17fa1c90bc1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigPatchDeploymentInstanceFilterGroupLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentInstanceFilterGroupLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9939f599fb430895cce09b3d7e47004ee98f75213c3a2a5885256124eb51713)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f927094185e5eb0c869763c83d67237c59ead77a826d8bd5ce84691a5276d15b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb0dca0e1503ba44797a578b8ffe6c3e1a88ee6bb289d754176240cee8daec99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigPatchDeploymentInstanceFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentInstanceFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df53a22e2a7a6904e6d93a057d99bdabe0ce10c3867edacb411343417442aa74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGroupLabels")
    def put_group_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62671af91a83bba9a9406b5521973b8079c414bca52c360b36db871946fab1e8)
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
    def group_labels(
        self,
    ) -> GoogleOsConfigPatchDeploymentInstanceFilterGroupLabelsList:
        return typing.cast(GoogleOsConfigPatchDeploymentInstanceFilterGroupLabelsList, jsii.get(self, "groupLabels"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels]]], jsii.get(self, "groupLabelsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9fdf3418dcf80f262591426fd672666fb5dd3832968c457c1ecef24bc59299af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceNamePrefixes")
    def instance_name_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceNamePrefixes"))

    @instance_name_prefixes.setter
    def instance_name_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55a478463346a02ff924603a45922c3feb33e784c9589463b15b93cc89db6051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceNamePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instances")
    def instances(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instances"))

    @instances.setter
    def instances(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4e7651761a998a0ab4ed089f640b2d39e890c96e2a1738bd41939a9cb89203d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "zones"))

    @zones.setter
    def zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9220e3042707c5453a5402402aa11a4f5cff3d2957f3d20f14c168fb9f717808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentInstanceFilter]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentInstanceFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentInstanceFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62ca72c660b0249f8a5b3bbbe7f5aebd70a3b49b04b76427f8cfb6ca58904ebe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentOneTimeSchedule",
    jsii_struct_bases=[],
    name_mapping={"execute_time": "executeTime"},
)
class GoogleOsConfigPatchDeploymentOneTimeSchedule:
    def __init__(self, *, execute_time: builtins.str) -> None:
        '''
        :param execute_time: The desired patch job execution time. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#execute_time GoogleOsConfigPatchDeployment#execute_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6917def58d7386f6397dc744cee9ed9f830a5a38e452161b1f67047d51030b28)
            check_type(argname="argument execute_time", value=execute_time, expected_type=type_hints["execute_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execute_time": execute_time,
        }

    @builtins.property
    def execute_time(self) -> builtins.str:
        '''The desired patch job execution time. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#execute_time GoogleOsConfigPatchDeployment#execute_time}
        '''
        result = self._values.get("execute_time")
        assert result is not None, "Required property 'execute_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentOneTimeSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentOneTimeScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentOneTimeScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecc6174f1393324c5262cc1919ebc8e602d3b2ef3aa755c0af1eee2d23b6be29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18253a63ab362bad6dd8bdaceede1d01bd3b37144548cda8deb1afe761fafded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executeTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentOneTimeSchedule]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentOneTimeSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentOneTimeSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a8b2bca0b965dda097e724f2838bbeebf8e85033e14f1b0613b0d24d1967e89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfig",
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
class GoogleOsConfigPatchDeploymentPatchConfig:
    def __init__(
        self,
        *,
        apt: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigApt", typing.Dict[builtins.str, typing.Any]]] = None,
        goo: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigGoo", typing.Dict[builtins.str, typing.Any]]] = None,
        mig_instances_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        post_step: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPostStep", typing.Dict[builtins.str, typing.Any]]] = None,
        pre_step: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPreStep", typing.Dict[builtins.str, typing.Any]]] = None,
        reboot_config: typing.Optional[builtins.str] = None,
        windows_update: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdate", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#apt GoogleOsConfigPatchDeployment#apt}
        :param goo: goo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#goo GoogleOsConfigPatchDeployment#goo}
        :param mig_instances_allowed: Allows the patch job to run on Managed instance groups (MIGs). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#mig_instances_allowed GoogleOsConfigPatchDeployment#mig_instances_allowed}
        :param post_step: post_step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#post_step GoogleOsConfigPatchDeployment#post_step}
        :param pre_step: pre_step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#pre_step GoogleOsConfigPatchDeployment#pre_step}
        :param reboot_config: Post-patch reboot settings. Possible values: ["DEFAULT", "ALWAYS", "NEVER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#reboot_config GoogleOsConfigPatchDeployment#reboot_config}
        :param windows_update: windows_update block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#windows_update GoogleOsConfigPatchDeployment#windows_update}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#yum GoogleOsConfigPatchDeployment#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#zypper GoogleOsConfigPatchDeployment#zypper}
        '''
        if isinstance(apt, dict):
            apt = GoogleOsConfigPatchDeploymentPatchConfigApt(**apt)
        if isinstance(goo, dict):
            goo = GoogleOsConfigPatchDeploymentPatchConfigGoo(**goo)
        if isinstance(post_step, dict):
            post_step = GoogleOsConfigPatchDeploymentPatchConfigPostStep(**post_step)
        if isinstance(pre_step, dict):
            pre_step = GoogleOsConfigPatchDeploymentPatchConfigPreStep(**pre_step)
        if isinstance(windows_update, dict):
            windows_update = GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdate(**windows_update)
        if isinstance(yum, dict):
            yum = GoogleOsConfigPatchDeploymentPatchConfigYum(**yum)
        if isinstance(zypper, dict):
            zypper = GoogleOsConfigPatchDeploymentPatchConfigZypper(**zypper)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c27dd6db3cd26d082fbf2c694727e7e802582274af9ab557826d7995e363f0f)
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
    def apt(self) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigApt"]:
        '''apt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#apt GoogleOsConfigPatchDeployment#apt}
        '''
        result = self._values.get("apt")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigApt"], result)

    @builtins.property
    def goo(self) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigGoo"]:
        '''goo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#goo GoogleOsConfigPatchDeployment#goo}
        '''
        result = self._values.get("goo")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigGoo"], result)

    @builtins.property
    def mig_instances_allowed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows the patch job to run on Managed instance groups (MIGs).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#mig_instances_allowed GoogleOsConfigPatchDeployment#mig_instances_allowed}
        '''
        result = self._values.get("mig_instances_allowed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def post_step(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPostStep"]:
        '''post_step block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#post_step GoogleOsConfigPatchDeployment#post_step}
        '''
        result = self._values.get("post_step")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPostStep"], result)

    @builtins.property
    def pre_step(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPreStep"]:
        '''pre_step block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#pre_step GoogleOsConfigPatchDeployment#pre_step}
        '''
        result = self._values.get("pre_step")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPreStep"], result)

    @builtins.property
    def reboot_config(self) -> typing.Optional[builtins.str]:
        '''Post-patch reboot settings. Possible values: ["DEFAULT", "ALWAYS", "NEVER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#reboot_config GoogleOsConfigPatchDeployment#reboot_config}
        '''
        result = self._values.get("reboot_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def windows_update(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdate"]:
        '''windows_update block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#windows_update GoogleOsConfigPatchDeployment#windows_update}
        '''
        result = self._values.get("windows_update")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdate"], result)

    @builtins.property
    def yum(self) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigYum"]:
        '''yum block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#yum GoogleOsConfigPatchDeployment#yum}
        '''
        result = self._values.get("yum")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigYum"], result)

    @builtins.property
    def zypper(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigZypper"]:
        '''zypper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#zypper GoogleOsConfigPatchDeployment#zypper}
        '''
        result = self._values.get("zypper")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigZypper"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentPatchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigApt",
    jsii_struct_bases=[],
    name_mapping={
        "excludes": "excludes",
        "exclusive_packages": "exclusivePackages",
        "type": "type",
    },
)
class GoogleOsConfigPatchDeploymentPatchConfigApt:
    def __init__(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclusive_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param excludes: List of packages to exclude from update. These packages will be excluded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#excludes GoogleOsConfigPatchDeployment#excludes}
        :param exclusive_packages: An exclusive list of packages to be updated. These are the only packages that will be updated. If these packages are not installed, they will be ignored. This field cannot be specified with any other patch configuration fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#exclusive_packages GoogleOsConfigPatchDeployment#exclusive_packages}
        :param type: By changing the type to DIST, the patching is performed using apt-get dist-upgrade instead. Possible values: ["DIST", "UPGRADE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#type GoogleOsConfigPatchDeployment#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07e4273b232a4916f608d54753bf2d830827716e611caec9f4c3d1cc20531d8f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#excludes GoogleOsConfigPatchDeployment#excludes}
        '''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclusive_packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An exclusive list of packages to be updated.

        These are the only packages that will be updated.
        If these packages are not installed, they will be ignored. This field cannot be specified with
        any other patch configuration fields.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#exclusive_packages GoogleOsConfigPatchDeployment#exclusive_packages}
        '''
        result = self._values.get("exclusive_packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''By changing the type to DIST, the patching is performed using apt-get dist-upgrade instead. Possible values: ["DIST", "UPGRADE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#type GoogleOsConfigPatchDeployment#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentPatchConfigApt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentPatchConfigAptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigAptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4aadec446c8a6c7b17730db65354e90fd9de9450aca1ca347ebedd83971ba484)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7003d0e7eabdf04118c8aa82b2eca76cb46fe736582b8c1a6e70d88f0d3ec68d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusivePackages")
    def exclusive_packages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusivePackages"))

    @exclusive_packages.setter
    def exclusive_packages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c2078b7ee477b839add23adc2f7f27c4679339b953d0dadf8c04b55076ebadb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusivePackages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16af05329170a3a4a9336bc6cd895ee8fbcd06c518805e1ce412fb0502004f27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigApt]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigApt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigApt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283561595999e07a46f2d66014d2348af65801cb9facb68d00e7f718539bd283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigGoo",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleOsConfigPatchDeploymentPatchConfigGoo:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: goo update settings. Use this setting to override the default goo patch rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#enabled GoogleOsConfigPatchDeployment#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65d6ee1bf5437ed4be4fe996ae08e036068473e6e44bf8f924223c80e71ab2be)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''goo update settings. Use this setting to override the default goo patch rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#enabled GoogleOsConfigPatchDeployment#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentPatchConfigGoo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentPatchConfigGooOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigGooOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52eb439494c77a9869a23d5e98479f96af81af79af3430386b1b8a794576eb18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0088f709b70356e0b8f90d38eacb93db932648095515963f41567d3bc53e59a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigGoo]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigGoo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigGoo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45616959eb38791724e4e60be80fbce28f86bd62d1c85290c2e5d42c603e5ff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigPatchDeploymentPatchConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b256f7bee76d0815ad5326085da54c6f46f965e2b67d54255bd3d04a14ba9abe)
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
        :param excludes: List of packages to exclude from update. These packages will be excluded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#excludes GoogleOsConfigPatchDeployment#excludes}
        :param exclusive_packages: An exclusive list of packages to be updated. These are the only packages that will be updated. If these packages are not installed, they will be ignored. This field cannot be specified with any other patch configuration fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#exclusive_packages GoogleOsConfigPatchDeployment#exclusive_packages}
        :param type: By changing the type to DIST, the patching is performed using apt-get dist-upgrade instead. Possible values: ["DIST", "UPGRADE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#type GoogleOsConfigPatchDeployment#type}
        '''
        value = GoogleOsConfigPatchDeploymentPatchConfigApt(
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
        :param enabled: goo update settings. Use this setting to override the default goo patch rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#enabled GoogleOsConfigPatchDeployment#enabled}
        '''
        value = GoogleOsConfigPatchDeploymentPatchConfigGoo(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putGoo", [value]))

    @jsii.member(jsii_name="putPostStep")
    def put_post_step(
        self,
        *,
        linux_exec_step_config: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        windows_exec_step_config: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param linux_exec_step_config: linux_exec_step_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#linux_exec_step_config GoogleOsConfigPatchDeployment#linux_exec_step_config}
        :param windows_exec_step_config: windows_exec_step_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#windows_exec_step_config GoogleOsConfigPatchDeployment#windows_exec_step_config}
        '''
        value = GoogleOsConfigPatchDeploymentPatchConfigPostStep(
            linux_exec_step_config=linux_exec_step_config,
            windows_exec_step_config=windows_exec_step_config,
        )

        return typing.cast(None, jsii.invoke(self, "putPostStep", [value]))

    @jsii.member(jsii_name="putPreStep")
    def put_pre_step(
        self,
        *,
        linux_exec_step_config: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        windows_exec_step_config: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param linux_exec_step_config: linux_exec_step_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#linux_exec_step_config GoogleOsConfigPatchDeployment#linux_exec_step_config}
        :param windows_exec_step_config: windows_exec_step_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#windows_exec_step_config GoogleOsConfigPatchDeployment#windows_exec_step_config}
        '''
        value = GoogleOsConfigPatchDeploymentPatchConfigPreStep(
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
        :param classifications: Only apply updates of these windows update classifications. If empty, all updates are applied. Possible values: ["CRITICAL", "SECURITY", "DEFINITION", "DRIVER", "FEATURE_PACK", "SERVICE_PACK", "TOOL", "UPDATE_ROLLUP", "UPDATE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#classifications GoogleOsConfigPatchDeployment#classifications}
        :param excludes: List of KBs to exclude from update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#excludes GoogleOsConfigPatchDeployment#excludes}
        :param exclusive_patches: An exclusive list of kbs to be updated. These are the only patches that will be updated. This field must not be used with other patch configurations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#exclusive_patches GoogleOsConfigPatchDeployment#exclusive_patches}
        '''
        value = GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdate(
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
        :param excludes: List of packages to exclude from update. These packages will be excluded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#excludes GoogleOsConfigPatchDeployment#excludes}
        :param exclusive_packages: An exclusive list of packages to be updated. These are the only packages that will be updated. If these packages are not installed, they will be ignored. This field cannot be specified with any other patch configuration fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#exclusive_packages GoogleOsConfigPatchDeployment#exclusive_packages}
        :param minimal: Will cause patch to run yum update-minimal instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#minimal GoogleOsConfigPatchDeployment#minimal}
        :param security: Adds the --security flag to yum update. Not supported on all platforms. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#security GoogleOsConfigPatchDeployment#security}
        '''
        value = GoogleOsConfigPatchDeploymentPatchConfigYum(
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
        :param categories: Install only patches with these categories. Common categories include security, recommended, and feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#categories GoogleOsConfigPatchDeployment#categories}
        :param excludes: List of packages to exclude from update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#excludes GoogleOsConfigPatchDeployment#excludes}
        :param exclusive_patches: An exclusive list of patches to be updated. These are the only patches that will be installed using 'zypper patch patch:' command. This field must not be used with any other patch configuration fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#exclusive_patches GoogleOsConfigPatchDeployment#exclusive_patches}
        :param severities: Install only patches with these severities. Common severities include critical, important, moderate, and low. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#severities GoogleOsConfigPatchDeployment#severities}
        :param with_optional: Adds the --with-optional flag to zypper patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#with_optional GoogleOsConfigPatchDeployment#with_optional}
        :param with_update: Adds the --with-update flag, to zypper patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#with_update GoogleOsConfigPatchDeployment#with_update}
        '''
        value = GoogleOsConfigPatchDeploymentPatchConfigZypper(
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
    def apt(self) -> GoogleOsConfigPatchDeploymentPatchConfigAptOutputReference:
        return typing.cast(GoogleOsConfigPatchDeploymentPatchConfigAptOutputReference, jsii.get(self, "apt"))

    @builtins.property
    @jsii.member(jsii_name="goo")
    def goo(self) -> GoogleOsConfigPatchDeploymentPatchConfigGooOutputReference:
        return typing.cast(GoogleOsConfigPatchDeploymentPatchConfigGooOutputReference, jsii.get(self, "goo"))

    @builtins.property
    @jsii.member(jsii_name="postStep")
    def post_step(
        self,
    ) -> "GoogleOsConfigPatchDeploymentPatchConfigPostStepOutputReference":
        return typing.cast("GoogleOsConfigPatchDeploymentPatchConfigPostStepOutputReference", jsii.get(self, "postStep"))

    @builtins.property
    @jsii.member(jsii_name="preStep")
    def pre_step(
        self,
    ) -> "GoogleOsConfigPatchDeploymentPatchConfigPreStepOutputReference":
        return typing.cast("GoogleOsConfigPatchDeploymentPatchConfigPreStepOutputReference", jsii.get(self, "preStep"))

    @builtins.property
    @jsii.member(jsii_name="windowsUpdate")
    def windows_update(
        self,
    ) -> "GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdateOutputReference":
        return typing.cast("GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdateOutputReference", jsii.get(self, "windowsUpdate"))

    @builtins.property
    @jsii.member(jsii_name="yum")
    def yum(self) -> "GoogleOsConfigPatchDeploymentPatchConfigYumOutputReference":
        return typing.cast("GoogleOsConfigPatchDeploymentPatchConfigYumOutputReference", jsii.get(self, "yum"))

    @builtins.property
    @jsii.member(jsii_name="zypper")
    def zypper(self) -> "GoogleOsConfigPatchDeploymentPatchConfigZypperOutputReference":
        return typing.cast("GoogleOsConfigPatchDeploymentPatchConfigZypperOutputReference", jsii.get(self, "zypper"))

    @builtins.property
    @jsii.member(jsii_name="aptInput")
    def apt_input(self) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigApt]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigApt], jsii.get(self, "aptInput"))

    @builtins.property
    @jsii.member(jsii_name="gooInput")
    def goo_input(self) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigGoo]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigGoo], jsii.get(self, "gooInput"))

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
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPostStep"]:
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPostStep"], jsii.get(self, "postStepInput"))

    @builtins.property
    @jsii.member(jsii_name="preStepInput")
    def pre_step_input(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPreStep"]:
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPreStep"], jsii.get(self, "preStepInput"))

    @builtins.property
    @jsii.member(jsii_name="rebootConfigInput")
    def reboot_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rebootConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsUpdateInput")
    def windows_update_input(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdate"]:
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdate"], jsii.get(self, "windowsUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="yumInput")
    def yum_input(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigYum"]:
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigYum"], jsii.get(self, "yumInput"))

    @builtins.property
    @jsii.member(jsii_name="zypperInput")
    def zypper_input(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigZypper"]:
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigZypper"], jsii.get(self, "zypperInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ef20cb23666a125543170be6a31fb8e8bf827b3319ed243b6564256cc234f693)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "migInstancesAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rebootConfig")
    def reboot_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rebootConfig"))

    @reboot_config.setter
    def reboot_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae8071fabb4a6c5edf4075e12ff043faaeb5830daf9d5bea24ae0601748139d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rebootConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfig]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__750523a2616a0373ce85a91305126c69822d65ede77792db1d000c9e7b0cad36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPostStep",
    jsii_struct_bases=[],
    name_mapping={
        "linux_exec_step_config": "linuxExecStepConfig",
        "windows_exec_step_config": "windowsExecStepConfig",
    },
)
class GoogleOsConfigPatchDeploymentPatchConfigPostStep:
    def __init__(
        self,
        *,
        linux_exec_step_config: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        windows_exec_step_config: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param linux_exec_step_config: linux_exec_step_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#linux_exec_step_config GoogleOsConfigPatchDeployment#linux_exec_step_config}
        :param windows_exec_step_config: windows_exec_step_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#windows_exec_step_config GoogleOsConfigPatchDeployment#windows_exec_step_config}
        '''
        if isinstance(linux_exec_step_config, dict):
            linux_exec_step_config = GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig(**linux_exec_step_config)
        if isinstance(windows_exec_step_config, dict):
            windows_exec_step_config = GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig(**windows_exec_step_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__981cebd952ca34a7d9992ea1fef2b213d518458885c46a1032ab73b0c756ab99)
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
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig"]:
        '''linux_exec_step_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#linux_exec_step_config GoogleOsConfigPatchDeployment#linux_exec_step_config}
        '''
        result = self._values.get("linux_exec_step_config")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig"], result)

    @builtins.property
    def windows_exec_step_config(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig"]:
        '''windows_exec_step_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#windows_exec_step_config GoogleOsConfigPatchDeployment#windows_exec_step_config}
        '''
        result = self._values.get("windows_exec_step_config")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentPatchConfigPostStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_success_codes": "allowedSuccessCodes",
        "gcs_object": "gcsObject",
        "interpreter": "interpreter",
        "local_path": "localPath",
    },
)
class GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig:
    def __init__(
        self,
        *,
        allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        gcs_object: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject", typing.Dict[builtins.str, typing.Any]]] = None,
        interpreter: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_success_codes: Defaults to [0]. A list of possible return values that the execution can return to indicate a success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#allowed_success_codes GoogleOsConfigPatchDeployment#allowed_success_codes}
        :param gcs_object: gcs_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#gcs_object GoogleOsConfigPatchDeployment#gcs_object}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script will be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#interpreter GoogleOsConfigPatchDeployment#interpreter}
        :param local_path: An absolute path to the executable on the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#local_path GoogleOsConfigPatchDeployment#local_path}
        '''
        if isinstance(gcs_object, dict):
            gcs_object = GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject(**gcs_object)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0419035405579cbbf340791334d1d0a3a00085d25c4a86d19ab34aa5f7c6844)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#allowed_success_codes GoogleOsConfigPatchDeployment#allowed_success_codes}
        '''
        result = self._values.get("allowed_success_codes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def gcs_object(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject"]:
        '''gcs_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#gcs_object GoogleOsConfigPatchDeployment#gcs_object}
        '''
        result = self._values.get("gcs_object")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject"], result)

    @builtins.property
    def interpreter(self) -> typing.Optional[builtins.str]:
        '''The script interpreter to use to run the script.

        If no interpreter is specified the script will
        be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#interpreter GoogleOsConfigPatchDeployment#interpreter}
        '''
        result = self._values.get("interpreter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''An absolute path to the executable on the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#local_path GoogleOsConfigPatchDeployment#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "generation_number": "generationNumber",
        "object": "object",
    },
)
class GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        generation_number: builtins.str,
        object: builtins.str,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#bucket GoogleOsConfigPatchDeployment#bucket}
        :param generation_number: Generation number of the Cloud Storage object. This is used to ensure that the ExecStep specified by this PatchJob does not change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#generation_number GoogleOsConfigPatchDeployment#generation_number}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#object GoogleOsConfigPatchDeployment#object}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c02d0247d4d58ef5ddad21a4aebd59bf2bbeac19b9918e064c6b2a74712ff1c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#bucket GoogleOsConfigPatchDeployment#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation_number(self) -> builtins.str:
        '''Generation number of the Cloud Storage object.

        This is used to ensure that the ExecStep specified by this PatchJob does not change.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#generation_number GoogleOsConfigPatchDeployment#generation_number}
        '''
        result = self._values.get("generation_number")
        assert result is not None, "Required property 'generation_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#object GoogleOsConfigPatchDeployment#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__298fd53e743bbb6ed96553858609f075dffaff4147708380b21d96f8dd692370)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb94b7dc1bb525fcd9b4053ca73aa66bc63738174330c1abbdc797a70af622b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generationNumber")
    def generation_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generationNumber"))

    @generation_number.setter
    def generation_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dafc5b8745dd49572eeb1f30aab7140051083738c009b84e432effa66ff8d0c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generationNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0700e60841144ecdba9bc0f0c16b265683c5380e425bf3bdab52fe0a1b6572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860b737380e6a4a348d5df6eee386024ebed00161f8bc140b5c72d7b7ec19426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da8846bc30c0e4d6ad57024425219ffbb3f4151ba17caaeb3d8e7f0222ac18d2)
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
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#bucket GoogleOsConfigPatchDeployment#bucket}
        :param generation_number: Generation number of the Cloud Storage object. This is used to ensure that the ExecStep specified by this PatchJob does not change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#generation_number GoogleOsConfigPatchDeployment#generation_number}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#object GoogleOsConfigPatchDeployment#object}
        '''
        value = GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject(
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
    ) -> GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObjectOutputReference:
        return typing.cast(GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObjectOutputReference, jsii.get(self, "gcsObject"))

    @builtins.property
    @jsii.member(jsii_name="allowedSuccessCodesInput")
    def allowed_success_codes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "allowedSuccessCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsObjectInput")
    def gcs_object_input(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject], jsii.get(self, "gcsObjectInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0eb11b76737c04dfa218660250e6ebeef18bc105350294e7aecc5b7607579f8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedSuccessCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ac4b717d2de3512a03cec444cd92bd8c51ba7d8c06c4513bd293bf3107b84a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54cd5b591aefa75b8d4dec82e62214617e758e86d994858c6036bdfcf440dfb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a361a29e496491fb1b36986f800445395f362bad708ec2f00177181246dd65d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigPatchDeploymentPatchConfigPostStepOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPostStepOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__591f4dc64e0a380721f28579f5faa69489cf522ccadfe6e32b15126b8e5baa15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLinuxExecStepConfig")
    def put_linux_exec_step_config(
        self,
        *,
        allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        gcs_object: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject, typing.Dict[builtins.str, typing.Any]]] = None,
        interpreter: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_success_codes: Defaults to [0]. A list of possible return values that the execution can return to indicate a success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#allowed_success_codes GoogleOsConfigPatchDeployment#allowed_success_codes}
        :param gcs_object: gcs_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#gcs_object GoogleOsConfigPatchDeployment#gcs_object}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script will be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#interpreter GoogleOsConfigPatchDeployment#interpreter}
        :param local_path: An absolute path to the executable on the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#local_path GoogleOsConfigPatchDeployment#local_path}
        '''
        value = GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig(
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
        gcs_object: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject", typing.Dict[builtins.str, typing.Any]]] = None,
        interpreter: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_success_codes: Defaults to [0]. A list of possible return values that the execution can return to indicate a success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#allowed_success_codes GoogleOsConfigPatchDeployment#allowed_success_codes}
        :param gcs_object: gcs_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#gcs_object GoogleOsConfigPatchDeployment#gcs_object}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script will be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#interpreter GoogleOsConfigPatchDeployment#interpreter}
        :param local_path: An absolute path to the executable on the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#local_path GoogleOsConfigPatchDeployment#local_path}
        '''
        value = GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig(
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
    ) -> GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigOutputReference:
        return typing.cast(GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigOutputReference, jsii.get(self, "linuxExecStepConfig"))

    @builtins.property
    @jsii.member(jsii_name="windowsExecStepConfig")
    def windows_exec_step_config(
        self,
    ) -> "GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigOutputReference":
        return typing.cast("GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigOutputReference", jsii.get(self, "windowsExecStepConfig"))

    @builtins.property
    @jsii.member(jsii_name="linuxExecStepConfigInput")
    def linux_exec_step_config_input(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig], jsii.get(self, "linuxExecStepConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsExecStepConfigInput")
    def windows_exec_step_config_input(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig"]:
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig"], jsii.get(self, "windowsExecStepConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStep]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStep], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStep],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9009886f20f4e19e73a768461add96fe1cfbf5281b4fc2c14783e6dded1cdbb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_success_codes": "allowedSuccessCodes",
        "gcs_object": "gcsObject",
        "interpreter": "interpreter",
        "local_path": "localPath",
    },
)
class GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig:
    def __init__(
        self,
        *,
        allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        gcs_object: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject", typing.Dict[builtins.str, typing.Any]]] = None,
        interpreter: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_success_codes: Defaults to [0]. A list of possible return values that the execution can return to indicate a success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#allowed_success_codes GoogleOsConfigPatchDeployment#allowed_success_codes}
        :param gcs_object: gcs_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#gcs_object GoogleOsConfigPatchDeployment#gcs_object}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script will be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#interpreter GoogleOsConfigPatchDeployment#interpreter}
        :param local_path: An absolute path to the executable on the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#local_path GoogleOsConfigPatchDeployment#local_path}
        '''
        if isinstance(gcs_object, dict):
            gcs_object = GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject(**gcs_object)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb80cc2520c45631838c8c74dd23707fe7a4a2d27c78c7a081e34a2aa1eebf17)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#allowed_success_codes GoogleOsConfigPatchDeployment#allowed_success_codes}
        '''
        result = self._values.get("allowed_success_codes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def gcs_object(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject"]:
        '''gcs_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#gcs_object GoogleOsConfigPatchDeployment#gcs_object}
        '''
        result = self._values.get("gcs_object")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject"], result)

    @builtins.property
    def interpreter(self) -> typing.Optional[builtins.str]:
        '''The script interpreter to use to run the script.

        If no interpreter is specified the script will
        be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#interpreter GoogleOsConfigPatchDeployment#interpreter}
        '''
        result = self._values.get("interpreter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''An absolute path to the executable on the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#local_path GoogleOsConfigPatchDeployment#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "generation_number": "generationNumber",
        "object": "object",
    },
)
class GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        generation_number: builtins.str,
        object: builtins.str,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#bucket GoogleOsConfigPatchDeployment#bucket}
        :param generation_number: Generation number of the Cloud Storage object. This is used to ensure that the ExecStep specified by this PatchJob does not change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#generation_number GoogleOsConfigPatchDeployment#generation_number}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#object GoogleOsConfigPatchDeployment#object}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6319e3c3758220a66ef6324b3a764b52281e93b5dfb53314b388cb2a72b5025)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#bucket GoogleOsConfigPatchDeployment#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation_number(self) -> builtins.str:
        '''Generation number of the Cloud Storage object.

        This is used to ensure that the ExecStep specified by this PatchJob does not change.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#generation_number GoogleOsConfigPatchDeployment#generation_number}
        '''
        result = self._values.get("generation_number")
        assert result is not None, "Required property 'generation_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#object GoogleOsConfigPatchDeployment#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c667a68c0d784fab45846fe728657e8fe179e1ce59072d8fb17c64b554abe0d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55c3888a063dc2bddc998d92c72a644b59b329a925f51aa9af44d0a87c3be238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generationNumber")
    def generation_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generationNumber"))

    @generation_number.setter
    def generation_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__709d991a1b4595663ed09265564e7cd969c21137abb5fd9de2e13a0157ae3941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generationNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c11417d1966af434bb57fe502f339a0ab4d8f1108b9fef3285e36fd7d1aae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63093a2e44ef89ba5e4c547fd8f8fc0337973f2322208fb611a6a6576e47a940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9307c81a87128009a3905aa1fef61176a45643b5548c78984d9238a8289251a8)
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
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#bucket GoogleOsConfigPatchDeployment#bucket}
        :param generation_number: Generation number of the Cloud Storage object. This is used to ensure that the ExecStep specified by this PatchJob does not change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#generation_number GoogleOsConfigPatchDeployment#generation_number}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#object GoogleOsConfigPatchDeployment#object}
        '''
        value = GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject(
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
    ) -> GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObjectOutputReference:
        return typing.cast(GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObjectOutputReference, jsii.get(self, "gcsObject"))

    @builtins.property
    @jsii.member(jsii_name="allowedSuccessCodesInput")
    def allowed_success_codes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "allowedSuccessCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsObjectInput")
    def gcs_object_input(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject], jsii.get(self, "gcsObjectInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c38069acfce1d53f3e47f5ab0046ef8317bd47945109c7a8bac8d4c65c45a821)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedSuccessCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6ccbb47932214f6416e9760890fc3f8264cd680f0881707f17468e81390a157)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe8f2a2cf39f28f7f4bc80a161a07227e2753448fd90548e28985e1b2b01821d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e30e25a27273327b2284a5a6ffd252a186232731a1255a42bb91faf426e6d68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPreStep",
    jsii_struct_bases=[],
    name_mapping={
        "linux_exec_step_config": "linuxExecStepConfig",
        "windows_exec_step_config": "windowsExecStepConfig",
    },
)
class GoogleOsConfigPatchDeploymentPatchConfigPreStep:
    def __init__(
        self,
        *,
        linux_exec_step_config: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        windows_exec_step_config: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param linux_exec_step_config: linux_exec_step_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#linux_exec_step_config GoogleOsConfigPatchDeployment#linux_exec_step_config}
        :param windows_exec_step_config: windows_exec_step_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#windows_exec_step_config GoogleOsConfigPatchDeployment#windows_exec_step_config}
        '''
        if isinstance(linux_exec_step_config, dict):
            linux_exec_step_config = GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig(**linux_exec_step_config)
        if isinstance(windows_exec_step_config, dict):
            windows_exec_step_config = GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig(**windows_exec_step_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71606c462ca0a16bdbdccf6e99fe66fbd0005db82ddc6938d18c9797c6178a38)
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
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig"]:
        '''linux_exec_step_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#linux_exec_step_config GoogleOsConfigPatchDeployment#linux_exec_step_config}
        '''
        result = self._values.get("linux_exec_step_config")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig"], result)

    @builtins.property
    def windows_exec_step_config(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig"]:
        '''windows_exec_step_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#windows_exec_step_config GoogleOsConfigPatchDeployment#windows_exec_step_config}
        '''
        result = self._values.get("windows_exec_step_config")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentPatchConfigPreStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_success_codes": "allowedSuccessCodes",
        "gcs_object": "gcsObject",
        "interpreter": "interpreter",
        "local_path": "localPath",
    },
)
class GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig:
    def __init__(
        self,
        *,
        allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        gcs_object: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject", typing.Dict[builtins.str, typing.Any]]] = None,
        interpreter: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_success_codes: Defaults to [0]. A list of possible return values that the execution can return to indicate a success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#allowed_success_codes GoogleOsConfigPatchDeployment#allowed_success_codes}
        :param gcs_object: gcs_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#gcs_object GoogleOsConfigPatchDeployment#gcs_object}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script will be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#interpreter GoogleOsConfigPatchDeployment#interpreter}
        :param local_path: An absolute path to the executable on the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#local_path GoogleOsConfigPatchDeployment#local_path}
        '''
        if isinstance(gcs_object, dict):
            gcs_object = GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject(**gcs_object)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc715959e0884e1cefd3ba12c284e4975970fdb3550a2043e197996f33d5ea8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#allowed_success_codes GoogleOsConfigPatchDeployment#allowed_success_codes}
        '''
        result = self._values.get("allowed_success_codes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def gcs_object(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject"]:
        '''gcs_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#gcs_object GoogleOsConfigPatchDeployment#gcs_object}
        '''
        result = self._values.get("gcs_object")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject"], result)

    @builtins.property
    def interpreter(self) -> typing.Optional[builtins.str]:
        '''The script interpreter to use to run the script.

        If no interpreter is specified the script will
        be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#interpreter GoogleOsConfigPatchDeployment#interpreter}
        '''
        result = self._values.get("interpreter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''An absolute path to the executable on the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#local_path GoogleOsConfigPatchDeployment#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "generation_number": "generationNumber",
        "object": "object",
    },
)
class GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        generation_number: builtins.str,
        object: builtins.str,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#bucket GoogleOsConfigPatchDeployment#bucket}
        :param generation_number: Generation number of the Cloud Storage object. This is used to ensure that the ExecStep specified by this PatchJob does not change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#generation_number GoogleOsConfigPatchDeployment#generation_number}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#object GoogleOsConfigPatchDeployment#object}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f43bbccf381aae7d197f5a3f70a78aacbd165c86fec8ef32e96ab508fd6bd00f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#bucket GoogleOsConfigPatchDeployment#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation_number(self) -> builtins.str:
        '''Generation number of the Cloud Storage object.

        This is used to ensure that the ExecStep specified by this PatchJob does not change.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#generation_number GoogleOsConfigPatchDeployment#generation_number}
        '''
        result = self._values.get("generation_number")
        assert result is not None, "Required property 'generation_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#object GoogleOsConfigPatchDeployment#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__420c482b8820c86ef869fbb0c7ba04951781246eb43ee814950450339556ce79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9bf24a0445ffe5a249a5fbe0ed8cd688dcc91a65ae47d9b619135476e38e266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generationNumber")
    def generation_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generationNumber"))

    @generation_number.setter
    def generation_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac84806a603ad30b51388ec07706c7dee7d86873b6e5b24d0311850722fc192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generationNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186e54dac222bf4a02a8886cda8756fc81c66e029ead01050bf18247c45aa74c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37ecb411f9eec459293e820619c57cd90bef19fe692d1fda6794b6a973fc77d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cad1b929b39cafdc14c083e6e6ca62f2dbe28b988998e77a784c4871128faadf)
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
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#bucket GoogleOsConfigPatchDeployment#bucket}
        :param generation_number: Generation number of the Cloud Storage object. This is used to ensure that the ExecStep specified by this PatchJob does not change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#generation_number GoogleOsConfigPatchDeployment#generation_number}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#object GoogleOsConfigPatchDeployment#object}
        '''
        value = GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject(
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
    ) -> GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObjectOutputReference:
        return typing.cast(GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObjectOutputReference, jsii.get(self, "gcsObject"))

    @builtins.property
    @jsii.member(jsii_name="allowedSuccessCodesInput")
    def allowed_success_codes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "allowedSuccessCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsObjectInput")
    def gcs_object_input(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject], jsii.get(self, "gcsObjectInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__156253b769bc975d49b327522cb9466ebff3c39efeb7cb886fe8c081a6e8608a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedSuccessCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e5b74674431d423485ad39ddc3253a8135346210d4b7f06a745fa723b49af5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ad4553771baed1bf53a0944b2478ae8b1ae062e83943b3fc9cae1aa98aa7b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc40d3b9246234c4a4bcf17cfd354df891f74043c2fe02ff308bba9e5449b770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigPatchDeploymentPatchConfigPreStepOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPreStepOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4a71cca7e6a5f7a6ef6d7bab0e54f04a225d3580fe2d33170d7839b299f0ffb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLinuxExecStepConfig")
    def put_linux_exec_step_config(
        self,
        *,
        allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        gcs_object: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject, typing.Dict[builtins.str, typing.Any]]] = None,
        interpreter: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_success_codes: Defaults to [0]. A list of possible return values that the execution can return to indicate a success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#allowed_success_codes GoogleOsConfigPatchDeployment#allowed_success_codes}
        :param gcs_object: gcs_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#gcs_object GoogleOsConfigPatchDeployment#gcs_object}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script will be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#interpreter GoogleOsConfigPatchDeployment#interpreter}
        :param local_path: An absolute path to the executable on the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#local_path GoogleOsConfigPatchDeployment#local_path}
        '''
        value = GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig(
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
        gcs_object: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject", typing.Dict[builtins.str, typing.Any]]] = None,
        interpreter: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_success_codes: Defaults to [0]. A list of possible return values that the execution can return to indicate a success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#allowed_success_codes GoogleOsConfigPatchDeployment#allowed_success_codes}
        :param gcs_object: gcs_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#gcs_object GoogleOsConfigPatchDeployment#gcs_object}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script will be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#interpreter GoogleOsConfigPatchDeployment#interpreter}
        :param local_path: An absolute path to the executable on the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#local_path GoogleOsConfigPatchDeployment#local_path}
        '''
        value = GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig(
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
    ) -> GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigOutputReference:
        return typing.cast(GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigOutputReference, jsii.get(self, "linuxExecStepConfig"))

    @builtins.property
    @jsii.member(jsii_name="windowsExecStepConfig")
    def windows_exec_step_config(
        self,
    ) -> "GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigOutputReference":
        return typing.cast("GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigOutputReference", jsii.get(self, "windowsExecStepConfig"))

    @builtins.property
    @jsii.member(jsii_name="linuxExecStepConfigInput")
    def linux_exec_step_config_input(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig], jsii.get(self, "linuxExecStepConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsExecStepConfigInput")
    def windows_exec_step_config_input(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig"]:
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig"], jsii.get(self, "windowsExecStepConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStep]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStep], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStep],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1461fe14be8d16bd48da4e8f8256901fae7c8cf7a363dd4f354ea8a854262008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_success_codes": "allowedSuccessCodes",
        "gcs_object": "gcsObject",
        "interpreter": "interpreter",
        "local_path": "localPath",
    },
)
class GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig:
    def __init__(
        self,
        *,
        allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        gcs_object: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject", typing.Dict[builtins.str, typing.Any]]] = None,
        interpreter: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_success_codes: Defaults to [0]. A list of possible return values that the execution can return to indicate a success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#allowed_success_codes GoogleOsConfigPatchDeployment#allowed_success_codes}
        :param gcs_object: gcs_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#gcs_object GoogleOsConfigPatchDeployment#gcs_object}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script will be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#interpreter GoogleOsConfigPatchDeployment#interpreter}
        :param local_path: An absolute path to the executable on the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#local_path GoogleOsConfigPatchDeployment#local_path}
        '''
        if isinstance(gcs_object, dict):
            gcs_object = GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject(**gcs_object)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49c737598e58d66d06954e07604ca98a0bb08fba91ac741e64ec475284f9f25c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#allowed_success_codes GoogleOsConfigPatchDeployment#allowed_success_codes}
        '''
        result = self._values.get("allowed_success_codes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def gcs_object(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject"]:
        '''gcs_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#gcs_object GoogleOsConfigPatchDeployment#gcs_object}
        '''
        result = self._values.get("gcs_object")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject"], result)

    @builtins.property
    def interpreter(self) -> typing.Optional[builtins.str]:
        '''The script interpreter to use to run the script.

        If no interpreter is specified the script will
        be executed directly, which will likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#interpreter GoogleOsConfigPatchDeployment#interpreter}
        '''
        result = self._values.get("interpreter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''An absolute path to the executable on the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#local_path GoogleOsConfigPatchDeployment#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "generation_number": "generationNumber",
        "object": "object",
    },
)
class GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        generation_number: builtins.str,
        object: builtins.str,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#bucket GoogleOsConfigPatchDeployment#bucket}
        :param generation_number: Generation number of the Cloud Storage object. This is used to ensure that the ExecStep specified by this PatchJob does not change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#generation_number GoogleOsConfigPatchDeployment#generation_number}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#object GoogleOsConfigPatchDeployment#object}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417d76a53b26f40320bc23c90c33915c8de2e271a59976ec6ca1ab542774a13c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#bucket GoogleOsConfigPatchDeployment#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation_number(self) -> builtins.str:
        '''Generation number of the Cloud Storage object.

        This is used to ensure that the ExecStep specified by this PatchJob does not change.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#generation_number GoogleOsConfigPatchDeployment#generation_number}
        '''
        result = self._values.get("generation_number")
        assert result is not None, "Required property 'generation_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#object GoogleOsConfigPatchDeployment#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74f54bf8c188f919a2e7140c280f1816e0e930c0e40081d9e928197c8826e4a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de4359ccf4de9e013ae042a41c92edb955a2d58f2c4af1b071265e5006910e1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generationNumber")
    def generation_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generationNumber"))

    @generation_number.setter
    def generation_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ef8a47afc07213138dd534bfe00cde63194159285b32bdb6938e61c11269a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generationNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac1980007e85f2c13d12764bfa61fc0759f11b153f66e0bb998e2c5c773909b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31e91e8706ada93ce3cf2f53ecbf759e305311417036b4486327b1665b47c68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4693d8a68241682d3a4271b39fe7b1723210c855982cade7a185851a6a00ff23)
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
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#bucket GoogleOsConfigPatchDeployment#bucket}
        :param generation_number: Generation number of the Cloud Storage object. This is used to ensure that the ExecStep specified by this PatchJob does not change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#generation_number GoogleOsConfigPatchDeployment#generation_number}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#object GoogleOsConfigPatchDeployment#object}
        '''
        value = GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject(
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
    ) -> GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObjectOutputReference:
        return typing.cast(GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObjectOutputReference, jsii.get(self, "gcsObject"))

    @builtins.property
    @jsii.member(jsii_name="allowedSuccessCodesInput")
    def allowed_success_codes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "allowedSuccessCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsObjectInput")
    def gcs_object_input(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject], jsii.get(self, "gcsObjectInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9b067da1492524bcdd07f9bf3f0f6b91d0cc1cce6a65a6a3e916bb40433ba327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedSuccessCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3a5744a8f5b84f0013506a97c3d020576297ef35e4f1b1aef6eddb6b30561e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2507e65bef3faf48f49c7bc75d81faf87de44c12693ad7d9bf1a63df0850d551)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c231ce73b7c80e48bfe8fe0cfd3bafe689deadc286b5f5a75731593f31fa2a64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdate",
    jsii_struct_bases=[],
    name_mapping={
        "classifications": "classifications",
        "excludes": "excludes",
        "exclusive_patches": "exclusivePatches",
    },
)
class GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdate:
    def __init__(
        self,
        *,
        classifications: typing.Optional[typing.Sequence[builtins.str]] = None,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclusive_patches: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param classifications: Only apply updates of these windows update classifications. If empty, all updates are applied. Possible values: ["CRITICAL", "SECURITY", "DEFINITION", "DRIVER", "FEATURE_PACK", "SERVICE_PACK", "TOOL", "UPDATE_ROLLUP", "UPDATE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#classifications GoogleOsConfigPatchDeployment#classifications}
        :param excludes: List of KBs to exclude from update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#excludes GoogleOsConfigPatchDeployment#excludes}
        :param exclusive_patches: An exclusive list of kbs to be updated. These are the only patches that will be updated. This field must not be used with other patch configurations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#exclusive_patches GoogleOsConfigPatchDeployment#exclusive_patches}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59fc94b7fd06bc95b925e3822c0aff1cc9c96b8e4f9d890090e72638ce53d00e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#classifications GoogleOsConfigPatchDeployment#classifications}
        '''
        result = self._values.get("classifications")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of KBs to exclude from update.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#excludes GoogleOsConfigPatchDeployment#excludes}
        '''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclusive_patches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An exclusive list of kbs to be updated.

        These are the only patches that will be updated.
        This field must not be used with other patch configurations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#exclusive_patches GoogleOsConfigPatchDeployment#exclusive_patches}
        '''
        result = self._values.get("exclusive_patches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__868959277575240d89e021edb6b88fc8aa1edd1ff5eade0bd03f0ad5a82fd298)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34ddcfb130e9c555150ef7044aa3066d0039d4a81ee0a767bbdf89fc4e9cde34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classifications", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludes"))

    @excludes.setter
    def excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1b53543b32f64311606f3653db978b9c5f38bcc5c5ca3136e106294d4f50074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusivePatches")
    def exclusive_patches(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusivePatches"))

    @exclusive_patches.setter
    def exclusive_patches(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1fbad604353bc752a002a61abab2fe7787a1b6a079e688e0460facae3a9e424)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusivePatches", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdate]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363ba4d0b447a1d42aa3de67b74dd995262efaf8506aceee606bc3e6de9da7c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigYum",
    jsii_struct_bases=[],
    name_mapping={
        "excludes": "excludes",
        "exclusive_packages": "exclusivePackages",
        "minimal": "minimal",
        "security": "security",
    },
)
class GoogleOsConfigPatchDeploymentPatchConfigYum:
    def __init__(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclusive_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        minimal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param excludes: List of packages to exclude from update. These packages will be excluded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#excludes GoogleOsConfigPatchDeployment#excludes}
        :param exclusive_packages: An exclusive list of packages to be updated. These are the only packages that will be updated. If these packages are not installed, they will be ignored. This field cannot be specified with any other patch configuration fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#exclusive_packages GoogleOsConfigPatchDeployment#exclusive_packages}
        :param minimal: Will cause patch to run yum update-minimal instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#minimal GoogleOsConfigPatchDeployment#minimal}
        :param security: Adds the --security flag to yum update. Not supported on all platforms. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#security GoogleOsConfigPatchDeployment#security}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db34eda09ebfc9603af2c854d6e992aec410358f94d142d65529d9a5d0d5d791)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#excludes GoogleOsConfigPatchDeployment#excludes}
        '''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclusive_packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An exclusive list of packages to be updated.

        These are the only packages that will be updated.
        If these packages are not installed, they will be ignored. This field cannot be specified with
        any other patch configuration fields.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#exclusive_packages GoogleOsConfigPatchDeployment#exclusive_packages}
        '''
        result = self._values.get("exclusive_packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def minimal(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Will cause patch to run yum update-minimal instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#minimal GoogleOsConfigPatchDeployment#minimal}
        '''
        result = self._values.get("minimal")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def security(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Adds the --security flag to yum update. Not supported on all platforms.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#security GoogleOsConfigPatchDeployment#security}
        '''
        result = self._values.get("security")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentPatchConfigYum(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentPatchConfigYumOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigYumOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d94281220fe074b7ec6351498aeff8f5c818874c9c01435e6dac3d4b003e7bc3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a353e2f115b51d9fe4c7382de9dcad1bf389d49a9583d24d10e8c69e53a6551)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusivePackages")
    def exclusive_packages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusivePackages"))

    @exclusive_packages.setter
    def exclusive_packages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6bbd49670bc0366dc666ea79b918a402dc7a2dc210885aac435298110cccc3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbae9bde030a7ace4f37821ed5455e9d7e8e189b9ecf1e874e0136340b0dfcc5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__edcdc99ab3986a4c0d00da67becccd54458450d0eac75556bf591e777d3839e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "security", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigYum]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigYum], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigYum],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60c4b4d181fa8075b1b7fa98cdb75a4a59201006c347c6e0dcf3d4d1c83453cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigZypper",
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
class GoogleOsConfigPatchDeploymentPatchConfigZypper:
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
        :param categories: Install only patches with these categories. Common categories include security, recommended, and feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#categories GoogleOsConfigPatchDeployment#categories}
        :param excludes: List of packages to exclude from update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#excludes GoogleOsConfigPatchDeployment#excludes}
        :param exclusive_patches: An exclusive list of patches to be updated. These are the only patches that will be installed using 'zypper patch patch:' command. This field must not be used with any other patch configuration fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#exclusive_patches GoogleOsConfigPatchDeployment#exclusive_patches}
        :param severities: Install only patches with these severities. Common severities include critical, important, moderate, and low. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#severities GoogleOsConfigPatchDeployment#severities}
        :param with_optional: Adds the --with-optional flag to zypper patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#with_optional GoogleOsConfigPatchDeployment#with_optional}
        :param with_update: Adds the --with-update flag, to zypper patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#with_update GoogleOsConfigPatchDeployment#with_update}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731e3f36297a4273712882bbad41c82acc5a24c775c810f46dedf3e64e38aec5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#categories GoogleOsConfigPatchDeployment#categories}
        '''
        result = self._values.get("categories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of packages to exclude from update.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#excludes GoogleOsConfigPatchDeployment#excludes}
        '''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclusive_patches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An exclusive list of patches to be updated.

        These are the only patches that will be installed using 'zypper patch patch:' command.
        This field must not be used with any other patch configuration fields.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#exclusive_patches GoogleOsConfigPatchDeployment#exclusive_patches}
        '''
        result = self._values.get("exclusive_patches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def severities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Install only patches with these severities. Common severities include critical, important, moderate, and low.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#severities GoogleOsConfigPatchDeployment#severities}
        '''
        result = self._values.get("severities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def with_optional(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Adds the --with-optional flag to zypper patch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#with_optional GoogleOsConfigPatchDeployment#with_optional}
        '''
        result = self._values.get("with_optional")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def with_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Adds the --with-update flag, to zypper patch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#with_update GoogleOsConfigPatchDeployment#with_update}
        '''
        result = self._values.get("with_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentPatchConfigZypper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentPatchConfigZypperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentPatchConfigZypperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac7f825b9c00bc917eb99acdf8dc085e990801f396037af8aa1f0bac43997da4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b4d7116aa2ba5437ac958cd56b77047c1cc048974bd05f04219ae6c3da73204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "categories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludes"))

    @excludes.setter
    def excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f363541d8363b1c40f9e8d99e190c67f3202227770d519a3549b733a3b7cad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusivePatches")
    def exclusive_patches(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusivePatches"))

    @exclusive_patches.setter
    def exclusive_patches(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e36bd05627cb3fbda0a6937a72bcb85f492656039f70239906781e1f6618e536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusivePatches", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severities")
    def severities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "severities"))

    @severities.setter
    def severities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c353e06b24524a72e3be5d640459d604c8afc4aaa183f05a3e1ea1be5a7994)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c51c2c32059617ae92538f5bed20ce158b43b34a5c8316828d187b2a4eca9b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75987891c749ee779a01caba8641dc3e5d7d4a6086367fa1cf037dd4d3ec9836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigZypper]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigZypper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigZypper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e808f777e93b65146091e61719cd692f20f3593f225fd6f7d8911be65beb34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentRecurringSchedule",
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
class GoogleOsConfigPatchDeploymentRecurringSchedule:
    def __init__(
        self,
        *,
        time_of_day: typing.Union["GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDay", typing.Dict[builtins.str, typing.Any]],
        time_zone: typing.Union["GoogleOsConfigPatchDeploymentRecurringScheduleTimeZone", typing.Dict[builtins.str, typing.Any]],
        end_time: typing.Optional[builtins.str] = None,
        monthly: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentRecurringScheduleMonthly", typing.Dict[builtins.str, typing.Any]]] = None,
        start_time: typing.Optional[builtins.str] = None,
        weekly: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentRecurringScheduleWeekly", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param time_of_day: time_of_day block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#time_of_day GoogleOsConfigPatchDeployment#time_of_day}
        :param time_zone: time_zone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#time_zone GoogleOsConfigPatchDeployment#time_zone}
        :param end_time: The end time at which a recurring patch deployment schedule is no longer active. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#end_time GoogleOsConfigPatchDeployment#end_time}
        :param monthly: monthly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#monthly GoogleOsConfigPatchDeployment#monthly}
        :param start_time: The time that the recurring schedule becomes effective. Defaults to createTime of the patch deployment. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#start_time GoogleOsConfigPatchDeployment#start_time}
        :param weekly: weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#weekly GoogleOsConfigPatchDeployment#weekly}
        '''
        if isinstance(time_of_day, dict):
            time_of_day = GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDay(**time_of_day)
        if isinstance(time_zone, dict):
            time_zone = GoogleOsConfigPatchDeploymentRecurringScheduleTimeZone(**time_zone)
        if isinstance(monthly, dict):
            monthly = GoogleOsConfigPatchDeploymentRecurringScheduleMonthly(**monthly)
        if isinstance(weekly, dict):
            weekly = GoogleOsConfigPatchDeploymentRecurringScheduleWeekly(**weekly)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c23e5575224ca594a1e42cf4235d1b07e222fc76ebd7fc5b6b767dc41610b278)
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
    def time_of_day(self) -> "GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDay":
        '''time_of_day block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#time_of_day GoogleOsConfigPatchDeployment#time_of_day}
        '''
        result = self._values.get("time_of_day")
        assert result is not None, "Required property 'time_of_day' is missing"
        return typing.cast("GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDay", result)

    @builtins.property
    def time_zone(self) -> "GoogleOsConfigPatchDeploymentRecurringScheduleTimeZone":
        '''time_zone block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#time_zone GoogleOsConfigPatchDeployment#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast("GoogleOsConfigPatchDeploymentRecurringScheduleTimeZone", result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''The end time at which a recurring patch deployment schedule is no longer active.

        A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#end_time GoogleOsConfigPatchDeployment#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monthly(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentRecurringScheduleMonthly"]:
        '''monthly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#monthly GoogleOsConfigPatchDeployment#monthly}
        '''
        result = self._values.get("monthly")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentRecurringScheduleMonthly"], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The time that the recurring schedule becomes effective.

        Defaults to createTime of the patch deployment.
        A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#start_time GoogleOsConfigPatchDeployment#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weekly(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentRecurringScheduleWeekly"]:
        '''weekly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#weekly GoogleOsConfigPatchDeployment#weekly}
        '''
        result = self._values.get("weekly")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentRecurringScheduleWeekly"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentRecurringSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentRecurringScheduleMonthly",
    jsii_struct_bases=[],
    name_mapping={"month_day": "monthDay", "week_day_of_month": "weekDayOfMonth"},
)
class GoogleOsConfigPatchDeploymentRecurringScheduleMonthly:
    def __init__(
        self,
        *,
        month_day: typing.Optional[jsii.Number] = None,
        week_day_of_month: typing.Optional[typing.Union["GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param month_day: One day of the month. 1-31 indicates the 1st to the 31st day. -1 indicates the last day of the month. Months without the target day will be skipped. For example, a schedule to run "every month on the 31st" will not run in February, April, June, etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#month_day GoogleOsConfigPatchDeployment#month_day}
        :param week_day_of_month: week_day_of_month block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#week_day_of_month GoogleOsConfigPatchDeployment#week_day_of_month}
        '''
        if isinstance(week_day_of_month, dict):
            week_day_of_month = GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth(**week_day_of_month)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6bda1909019fb03018db678321cae8db1531116f2eac7dafb48537be6ede2ad)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#month_day GoogleOsConfigPatchDeployment#month_day}
        '''
        result = self._values.get("month_day")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def week_day_of_month(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth"]:
        '''week_day_of_month block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#week_day_of_month GoogleOsConfigPatchDeployment#week_day_of_month}
        '''
        result = self._values.get("week_day_of_month")
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentRecurringScheduleMonthly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ab04552a3f75637dfaddda9df761944640e804b9f541cf9aed6ac97d7729087)
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
        :param day_of_week: A day of the week. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#day_of_week GoogleOsConfigPatchDeployment#day_of_week}
        :param week_ordinal: Week number in a month. 1-4 indicates the 1st to 4th week of the month. -1 indicates the last week of the month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#week_ordinal GoogleOsConfigPatchDeployment#week_ordinal}
        :param day_offset: Represents the number of days before or after the given week day of month that the patch deployment is scheduled for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#day_offset GoogleOsConfigPatchDeployment#day_offset}
        '''
        value = GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth(
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
    ) -> "GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonthOutputReference":
        return typing.cast("GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonthOutputReference", jsii.get(self, "weekDayOfMonth"))

    @builtins.property
    @jsii.member(jsii_name="monthDayInput")
    def month_day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthDayInput"))

    @builtins.property
    @jsii.member(jsii_name="weekDayOfMonthInput")
    def week_day_of_month_input(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth"]:
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth"], jsii.get(self, "weekDayOfMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="monthDay")
    def month_day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "monthDay"))

    @month_day.setter
    def month_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8764e1babe72056c9238963764b65e0f24f24e9a927f8159fd2880c25a789714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleMonthly]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleMonthly], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleMonthly],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e8629c562b6fbea56f35fd79869c1f06b28256aba0713dad115fb8a32c616d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth",
    jsii_struct_bases=[],
    name_mapping={
        "day_of_week": "dayOfWeek",
        "week_ordinal": "weekOrdinal",
        "day_offset": "dayOffset",
    },
)
class GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth:
    def __init__(
        self,
        *,
        day_of_week: builtins.str,
        week_ordinal: jsii.Number,
        day_offset: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day_of_week: A day of the week. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#day_of_week GoogleOsConfigPatchDeployment#day_of_week}
        :param week_ordinal: Week number in a month. 1-4 indicates the 1st to 4th week of the month. -1 indicates the last week of the month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#week_ordinal GoogleOsConfigPatchDeployment#week_ordinal}
        :param day_offset: Represents the number of days before or after the given week day of month that the patch deployment is scheduled for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#day_offset GoogleOsConfigPatchDeployment#day_offset}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce994e0f56865e32838f6cc5892813d90abaf92f4c36634610b31e0b2d923204)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#day_of_week GoogleOsConfigPatchDeployment#day_of_week}
        '''
        result = self._values.get("day_of_week")
        assert result is not None, "Required property 'day_of_week' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def week_ordinal(self) -> jsii.Number:
        '''Week number in a month.

        1-4 indicates the 1st to 4th week of the month. -1 indicates the last week of the month.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#week_ordinal GoogleOsConfigPatchDeployment#week_ordinal}
        '''
        result = self._values.get("week_ordinal")
        assert result is not None, "Required property 'week_ordinal' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def day_offset(self) -> typing.Optional[jsii.Number]:
        '''Represents the number of days before or after the given week day of month that the patch deployment is scheduled for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#day_offset GoogleOsConfigPatchDeployment#day_offset}
        '''
        result = self._values.get("day_offset")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c5958d1ec48cd5f24d496c18b07078a31e0b2bcbac9735eb27fd53a7f5d5ebb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__580c39558a6785071874f7dba117ced72dc3eba20e6fea6ef7015f807d362e6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfWeek"))

    @day_of_week.setter
    def day_of_week(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__069e15fe611fd716f6489681be79c79f73f653a61e74630db628c44d3cb760a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekOrdinal")
    def week_ordinal(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weekOrdinal"))

    @week_ordinal.setter
    def week_ordinal(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b9c71840edde6c165bed2ad8be2fe6db6b158f89b79a712476d78e7237858fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekOrdinal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fbbe27ea3e0aaa44498cc672d6ecdd7e6d8913813739dd4cdc404929d9775be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigPatchDeploymentRecurringScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentRecurringScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd89b973958bf8087232122fe1aeb9f35ab3e4d4753592702d4cd5626b14df7d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMonthly")
    def put_monthly(
        self,
        *,
        month_day: typing.Optional[jsii.Number] = None,
        week_day_of_month: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param month_day: One day of the month. 1-31 indicates the 1st to the 31st day. -1 indicates the last day of the month. Months without the target day will be skipped. For example, a schedule to run "every month on the 31st" will not run in February, April, June, etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#month_day GoogleOsConfigPatchDeployment#month_day}
        :param week_day_of_month: week_day_of_month block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#week_day_of_month GoogleOsConfigPatchDeployment#week_day_of_month}
        '''
        value = GoogleOsConfigPatchDeploymentRecurringScheduleMonthly(
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
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#hours GoogleOsConfigPatchDeployment#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#minutes GoogleOsConfigPatchDeployment#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#nanos GoogleOsConfigPatchDeployment#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#seconds GoogleOsConfigPatchDeployment#seconds}
        '''
        value = GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDay(
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
        :param id: IANA Time Zone Database time zone, e.g. "America/New_York". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#id GoogleOsConfigPatchDeployment#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param version: IANA Time Zone Database version number, e.g. "2019a". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#version GoogleOsConfigPatchDeployment#version}
        '''
        value = GoogleOsConfigPatchDeploymentRecurringScheduleTimeZone(
            id=id, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putTimeZone", [value]))

    @jsii.member(jsii_name="putWeekly")
    def put_weekly(self, *, day_of_week: builtins.str) -> None:
        '''
        :param day_of_week: IANA Time Zone Database time zone, e.g. "America/New_York". Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#day_of_week GoogleOsConfigPatchDeployment#day_of_week}
        '''
        value = GoogleOsConfigPatchDeploymentRecurringScheduleWeekly(
            day_of_week=day_of_week
        )

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
    def monthly(
        self,
    ) -> GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyOutputReference:
        return typing.cast(GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyOutputReference, jsii.get(self, "monthly"))

    @builtins.property
    @jsii.member(jsii_name="nextExecuteTime")
    def next_execute_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextExecuteTime"))

    @builtins.property
    @jsii.member(jsii_name="timeOfDay")
    def time_of_day(
        self,
    ) -> "GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDayOutputReference":
        return typing.cast("GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDayOutputReference", jsii.get(self, "timeOfDay"))

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(
        self,
    ) -> "GoogleOsConfigPatchDeploymentRecurringScheduleTimeZoneOutputReference":
        return typing.cast("GoogleOsConfigPatchDeploymentRecurringScheduleTimeZoneOutputReference", jsii.get(self, "timeZone"))

    @builtins.property
    @jsii.member(jsii_name="weekly")
    def weekly(
        self,
    ) -> "GoogleOsConfigPatchDeploymentRecurringScheduleWeeklyOutputReference":
        return typing.cast("GoogleOsConfigPatchDeploymentRecurringScheduleWeeklyOutputReference", jsii.get(self, "weekly"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="monthlyInput")
    def monthly_input(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleMonthly]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleMonthly], jsii.get(self, "monthlyInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeOfDayInput")
    def time_of_day_input(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDay"]:
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDay"], jsii.get(self, "timeOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentRecurringScheduleTimeZone"]:
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentRecurringScheduleTimeZone"], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyInput")
    def weekly_input(
        self,
    ) -> typing.Optional["GoogleOsConfigPatchDeploymentRecurringScheduleWeekly"]:
        return typing.cast(typing.Optional["GoogleOsConfigPatchDeploymentRecurringScheduleWeekly"], jsii.get(self, "weeklyInput"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e59bfe6f170fac216b2ee052927aa0d13aa29b4ddcf6124f07b1f437369723c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42b5ec490b5e51b044e1f19a336f94f7be7358c4d820b8d7cad2d49766974150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentRecurringSchedule]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentRecurringSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentRecurringSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f26fd81a967902c1738229b52c3ad1e9ae1d14768f6ead70bb829ff78e5833)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDay",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDay:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#hours GoogleOsConfigPatchDeployment#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#minutes GoogleOsConfigPatchDeployment#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#nanos GoogleOsConfigPatchDeployment#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#seconds GoogleOsConfigPatchDeployment#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef58dafc09f6ec96b8caba4cfea08e01e1aee725002c5324a585274d751489e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#hours GoogleOsConfigPatchDeployment#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day. Must be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#minutes GoogleOsConfigPatchDeployment#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#nanos GoogleOsConfigPatchDeployment#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time.

        Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#seconds GoogleOsConfigPatchDeployment#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDay(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1519f6237846148b2845fdfaf9723d12115d572b4efc36772dbab32ba608db8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f73a147bec8d8ea45a2fba0428ade30f654e3a8593b859e71e74748a5a8286d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddc4e5ce30fc65f3428cb274d76b9e68d95db17b655bf22a8f7de03368afdd27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19a0e036d4dba4e53f5d3e43926a3a97675213646a7c926b2e16013cd70c98e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__893e992d3b9337232f043f9dd38930a02562a93ea0d990c20caf03546a9a4835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDay]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDay], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDay],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c60f6094e55d62565e8b851fecb1e5cb1b88269509acefe88ad32b0e63a106c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentRecurringScheduleTimeZone",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "version": "version"},
)
class GoogleOsConfigPatchDeploymentRecurringScheduleTimeZone:
    def __init__(
        self,
        *,
        id: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: IANA Time Zone Database time zone, e.g. "America/New_York". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#id GoogleOsConfigPatchDeployment#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param version: IANA Time Zone Database version number, e.g. "2019a". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#version GoogleOsConfigPatchDeployment#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c4f4de42509fed97c3ed53dd8934d09da82dfecdbb4608b09640b365a01b6fd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#id GoogleOsConfigPatchDeployment#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''IANA Time Zone Database version number, e.g. "2019a".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#version GoogleOsConfigPatchDeployment#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentRecurringScheduleTimeZone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentRecurringScheduleTimeZoneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentRecurringScheduleTimeZoneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75137fc65db26da5e1083c435b778b69ff029ee084de5d49fc8bbdd3d2a62547)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6e26941288cb282c4064c4bfe954916696ca477bd8ee86b430cbb9fb27d1b95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__729ca5d5baee574bef31485261f767a11ae10010d89bbc03cf2593974f433485)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleTimeZone]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleTimeZone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleTimeZone],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf98bd30dade67e52c6275ecf38e968b09504ba6d63737dda2cf1d209865755a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentRecurringScheduleWeekly",
    jsii_struct_bases=[],
    name_mapping={"day_of_week": "dayOfWeek"},
)
class GoogleOsConfigPatchDeploymentRecurringScheduleWeekly:
    def __init__(self, *, day_of_week: builtins.str) -> None:
        '''
        :param day_of_week: IANA Time Zone Database time zone, e.g. "America/New_York". Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#day_of_week GoogleOsConfigPatchDeployment#day_of_week}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5517cad2ffd3c5554382386f1a4e4523c9482440a95182f1a8913bc4af0c5ce3)
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_week": day_of_week,
        }

    @builtins.property
    def day_of_week(self) -> builtins.str:
        '''IANA Time Zone Database time zone, e.g. "America/New_York". Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#day_of_week GoogleOsConfigPatchDeployment#day_of_week}
        '''
        result = self._values.get("day_of_week")
        assert result is not None, "Required property 'day_of_week' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentRecurringScheduleWeekly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentRecurringScheduleWeeklyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentRecurringScheduleWeeklyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc5fb4e0d0d95f8ecb358ec128a2f29f4feac6fc5f73b1f090848b68e495d6c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ecf841fbac454b6a7b5736d818ccd84241033ada478b2eaf1467b04f18e3244)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleWeekly]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleWeekly], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleWeekly],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ecca301bf2be7a3400455d8bfe5bd5e4058bd080fafe2cdf3b06699c452f279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentRollout",
    jsii_struct_bases=[],
    name_mapping={"disruption_budget": "disruptionBudget", "mode": "mode"},
)
class GoogleOsConfigPatchDeploymentRollout:
    def __init__(
        self,
        *,
        disruption_budget: typing.Union["GoogleOsConfigPatchDeploymentRolloutDisruptionBudget", typing.Dict[builtins.str, typing.Any]],
        mode: builtins.str,
    ) -> None:
        '''
        :param disruption_budget: disruption_budget block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#disruption_budget GoogleOsConfigPatchDeployment#disruption_budget}
        :param mode: Mode of the patch rollout. Possible values: ["ZONE_BY_ZONE", "CONCURRENT_ZONES"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#mode GoogleOsConfigPatchDeployment#mode}
        '''
        if isinstance(disruption_budget, dict):
            disruption_budget = GoogleOsConfigPatchDeploymentRolloutDisruptionBudget(**disruption_budget)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b440ca909996f157bc970232d7b43b9938ed7873b88943c3887b52e31b1183f)
            check_type(argname="argument disruption_budget", value=disruption_budget, expected_type=type_hints["disruption_budget"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disruption_budget": disruption_budget,
            "mode": mode,
        }

    @builtins.property
    def disruption_budget(
        self,
    ) -> "GoogleOsConfigPatchDeploymentRolloutDisruptionBudget":
        '''disruption_budget block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#disruption_budget GoogleOsConfigPatchDeployment#disruption_budget}
        '''
        result = self._values.get("disruption_budget")
        assert result is not None, "Required property 'disruption_budget' is missing"
        return typing.cast("GoogleOsConfigPatchDeploymentRolloutDisruptionBudget", result)

    @builtins.property
    def mode(self) -> builtins.str:
        '''Mode of the patch rollout. Possible values: ["ZONE_BY_ZONE", "CONCURRENT_ZONES"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#mode GoogleOsConfigPatchDeployment#mode}
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentRollout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentRolloutDisruptionBudget",
    jsii_struct_bases=[],
    name_mapping={"fixed": "fixed", "percentage": "percentage"},
)
class GoogleOsConfigPatchDeploymentRolloutDisruptionBudget:
    def __init__(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: Specifies a fixed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#fixed GoogleOsConfigPatchDeployment#fixed}
        :param percentage: Specifies the relative value defined as a percentage, which will be multiplied by a reference value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#percentage GoogleOsConfigPatchDeployment#percentage}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c851851f502fbd58e28e09f6ebed10d6e4309730fa0d8cad871822f15a22c39)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#fixed GoogleOsConfigPatchDeployment#fixed}
        '''
        result = self._values.get("fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percentage(self) -> typing.Optional[jsii.Number]:
        '''Specifies the relative value defined as a percentage, which will be multiplied by a reference value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#percentage GoogleOsConfigPatchDeployment#percentage}
        '''
        result = self._values.get("percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentRolloutDisruptionBudget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentRolloutDisruptionBudgetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentRolloutDisruptionBudgetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94f26f8d71ccc6e187a9fbe1c1b022eefcf80ddca257fad7cf7878bbd0a7eb97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__656e47c66886545d2eb8bac660eb14f6b22aa9ba2805e7e133dd8cdaab1bebb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percentage")
    def percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentage"))

    @percentage.setter
    def percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__041817194af7387e7959817aaaebc36cb49e65d19212c9d8d561bd2e9cbd3efb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentRolloutDisruptionBudget]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentRolloutDisruptionBudget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentRolloutDisruptionBudget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cd4e30bbc0f5a8c66bf2b5a6c3c14d65959111af175e3992b837946b62e6131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigPatchDeploymentRolloutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentRolloutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09a04f47956f8f7e308a716c72339513b790ecbdaed3ef1c93747a8e3cf310bd)
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
        :param fixed: Specifies a fixed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#fixed GoogleOsConfigPatchDeployment#fixed}
        :param percentage: Specifies the relative value defined as a percentage, which will be multiplied by a reference value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#percentage GoogleOsConfigPatchDeployment#percentage}
        '''
        value = GoogleOsConfigPatchDeploymentRolloutDisruptionBudget(
            fixed=fixed, percentage=percentage
        )

        return typing.cast(None, jsii.invoke(self, "putDisruptionBudget", [value]))

    @builtins.property
    @jsii.member(jsii_name="disruptionBudget")
    def disruption_budget(
        self,
    ) -> GoogleOsConfigPatchDeploymentRolloutDisruptionBudgetOutputReference:
        return typing.cast(GoogleOsConfigPatchDeploymentRolloutDisruptionBudgetOutputReference, jsii.get(self, "disruptionBudget"))

    @builtins.property
    @jsii.member(jsii_name="disruptionBudgetInput")
    def disruption_budget_input(
        self,
    ) -> typing.Optional[GoogleOsConfigPatchDeploymentRolloutDisruptionBudget]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentRolloutDisruptionBudget], jsii.get(self, "disruptionBudgetInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__bf95e7ebc4f29377f2bca1fd0ec89a016bba36271b9600c4f5c9ef4c88942e0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleOsConfigPatchDeploymentRollout]:
        return typing.cast(typing.Optional[GoogleOsConfigPatchDeploymentRollout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigPatchDeploymentRollout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c2d0474d680758b70207e892cc411a822807296a6352b7a0f4c096210f6388)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class GoogleOsConfigPatchDeploymentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#create GoogleOsConfigPatchDeployment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#delete GoogleOsConfigPatchDeployment#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333b9aa61f1d0f6c7275ff0c7c3b58a988e13ed777c51104c69ac6d01a9c325a)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#create GoogleOsConfigPatchDeployment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_patch_deployment#delete GoogleOsConfigPatchDeployment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigPatchDeploymentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigPatchDeploymentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigPatchDeployment.GoogleOsConfigPatchDeploymentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee67cf4159e1dae4db55af5525a93ff5a0fe832b5659bc1156dcccaea761ebc6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cd94c0a509ca23f8dbf2b9bec852f979f2735fdc1c2ac89b324858746bf63dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f694984cd7be59ebe717fd389ca6110ec99875844f8e31e72b17cc1cc714c968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigPatchDeploymentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigPatchDeploymentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigPatchDeploymentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe803d25d801a6c5817523fb182646eebe78f1c54ec842d63c73864b4579b68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleOsConfigPatchDeployment",
    "GoogleOsConfigPatchDeploymentConfig",
    "GoogleOsConfigPatchDeploymentInstanceFilter",
    "GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels",
    "GoogleOsConfigPatchDeploymentInstanceFilterGroupLabelsList",
    "GoogleOsConfigPatchDeploymentInstanceFilterGroupLabelsOutputReference",
    "GoogleOsConfigPatchDeploymentInstanceFilterOutputReference",
    "GoogleOsConfigPatchDeploymentOneTimeSchedule",
    "GoogleOsConfigPatchDeploymentOneTimeScheduleOutputReference",
    "GoogleOsConfigPatchDeploymentPatchConfig",
    "GoogleOsConfigPatchDeploymentPatchConfigApt",
    "GoogleOsConfigPatchDeploymentPatchConfigAptOutputReference",
    "GoogleOsConfigPatchDeploymentPatchConfigGoo",
    "GoogleOsConfigPatchDeploymentPatchConfigGooOutputReference",
    "GoogleOsConfigPatchDeploymentPatchConfigOutputReference",
    "GoogleOsConfigPatchDeploymentPatchConfigPostStep",
    "GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig",
    "GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject",
    "GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObjectOutputReference",
    "GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigOutputReference",
    "GoogleOsConfigPatchDeploymentPatchConfigPostStepOutputReference",
    "GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig",
    "GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject",
    "GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObjectOutputReference",
    "GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigOutputReference",
    "GoogleOsConfigPatchDeploymentPatchConfigPreStep",
    "GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig",
    "GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject",
    "GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObjectOutputReference",
    "GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigOutputReference",
    "GoogleOsConfigPatchDeploymentPatchConfigPreStepOutputReference",
    "GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig",
    "GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject",
    "GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObjectOutputReference",
    "GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigOutputReference",
    "GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdate",
    "GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdateOutputReference",
    "GoogleOsConfigPatchDeploymentPatchConfigYum",
    "GoogleOsConfigPatchDeploymentPatchConfigYumOutputReference",
    "GoogleOsConfigPatchDeploymentPatchConfigZypper",
    "GoogleOsConfigPatchDeploymentPatchConfigZypperOutputReference",
    "GoogleOsConfigPatchDeploymentRecurringSchedule",
    "GoogleOsConfigPatchDeploymentRecurringScheduleMonthly",
    "GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyOutputReference",
    "GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth",
    "GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonthOutputReference",
    "GoogleOsConfigPatchDeploymentRecurringScheduleOutputReference",
    "GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDay",
    "GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDayOutputReference",
    "GoogleOsConfigPatchDeploymentRecurringScheduleTimeZone",
    "GoogleOsConfigPatchDeploymentRecurringScheduleTimeZoneOutputReference",
    "GoogleOsConfigPatchDeploymentRecurringScheduleWeekly",
    "GoogleOsConfigPatchDeploymentRecurringScheduleWeeklyOutputReference",
    "GoogleOsConfigPatchDeploymentRollout",
    "GoogleOsConfigPatchDeploymentRolloutDisruptionBudget",
    "GoogleOsConfigPatchDeploymentRolloutDisruptionBudgetOutputReference",
    "GoogleOsConfigPatchDeploymentRolloutOutputReference",
    "GoogleOsConfigPatchDeploymentTimeouts",
    "GoogleOsConfigPatchDeploymentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__342dc78866a3ce27e317642fd0e2d3572e4a0ea4534a872315cc8fb564821cb9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    instance_filter: typing.Union[GoogleOsConfigPatchDeploymentInstanceFilter, typing.Dict[builtins.str, typing.Any]],
    patch_deployment_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    duration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    one_time_schedule: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentOneTimeSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    patch_config: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    recurring_schedule: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentRecurringSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    rollout: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentRollout, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a8504aa2edc8af77745c1c3fdc29bc636ba5f1c7486d545c99ecec7b28a615ed(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd5fbf800bb05da942bc8ee60696ea76f34fe7257a63eae1845fe5c85831846(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d366d4407faa182e18497f1f6332fc7566e31e86c498cb59ed3d2119952428(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d9df4b9547945f5fff037838f82ee0f62b81d0f0a8373341db9db92cf459b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3a28a12265a7e2d6055b2db02665874c76b1d49d69588ffa99c6d83d513dc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5df337f6ac52099f40affd08836c8c438ec0ddd5dbbe283b90b0851975205c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__531544c18bb539618c5c4b8b7e75cf1ce86e442f715a8693b2b4bead42fc3027(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_filter: typing.Union[GoogleOsConfigPatchDeploymentInstanceFilter, typing.Dict[builtins.str, typing.Any]],
    patch_deployment_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    duration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    one_time_schedule: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentOneTimeSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    patch_config: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    recurring_schedule: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentRecurringSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    rollout: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentRollout, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c27fcfc19550645c95f19db9d7a028449427202b2711299eb7b41e91f51aed0(
    *,
    all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    group_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    instances: typing.Optional[typing.Sequence[builtins.str]] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab3627c7ba02a6762baf21e62959d8441dd064f3d329279439d163ca8d315f51(
    *,
    labels: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693589310bc12df90095ff27a9cb116c7c9b4acc7fa114e4cf1416da65db30f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af81991b9948b3ae9794ec80c352c8edb481314ece06a1caf4a795bc3a36e32(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c8fc7f14c147444f2faba28d4dce18c64a54ffbf2a1ef7cd1a8803ff96c31c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef953b14e9abdc6c20125891717b95da46619c1af7af466a84cdfa51cda5bf5b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5afc7d2755fc71139717463fbbb3e2111357c48bfb5df697fee72eb38855a8db(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60563f3769e71a350e0e34209fd215b408564d02ce7ab6c8043b17fa1c90bc1c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9939f599fb430895cce09b3d7e47004ee98f75213c3a2a5885256124eb51713(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f927094185e5eb0c869763c83d67237c59ead77a826d8bd5ce84691a5276d15b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb0dca0e1503ba44797a578b8ffe6c3e1a88ee6bb289d754176240cee8daec99(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df53a22e2a7a6904e6d93a057d99bdabe0ce10c3867edacb411343417442aa74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62671af91a83bba9a9406b5521973b8079c414bca52c360b36db871946fab1e8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigPatchDeploymentInstanceFilterGroupLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fdf3418dcf80f262591426fd672666fb5dd3832968c457c1ecef24bc59299af(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a478463346a02ff924603a45922c3feb33e784c9589463b15b93cc89db6051(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4e7651761a998a0ab4ed089f640b2d39e890c96e2a1738bd41939a9cb89203d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9220e3042707c5453a5402402aa11a4f5cff3d2957f3d20f14c168fb9f717808(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ca72c660b0249f8a5b3bbbe7f5aebd70a3b49b04b76427f8cfb6ca58904ebe(
    value: typing.Optional[GoogleOsConfigPatchDeploymentInstanceFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6917def58d7386f6397dc744cee9ed9f830a5a38e452161b1f67047d51030b28(
    *,
    execute_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc6174f1393324c5262cc1919ebc8e602d3b2ef3aa755c0af1eee2d23b6be29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18253a63ab362bad6dd8bdaceede1d01bd3b37144548cda8deb1afe761fafded(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8b2bca0b965dda097e724f2838bbeebf8e85033e14f1b0613b0d24d1967e89(
    value: typing.Optional[GoogleOsConfigPatchDeploymentOneTimeSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c27dd6db3cd26d082fbf2c694727e7e802582274af9ab557826d7995e363f0f(
    *,
    apt: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfigApt, typing.Dict[builtins.str, typing.Any]]] = None,
    goo: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfigGoo, typing.Dict[builtins.str, typing.Any]]] = None,
    mig_instances_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    post_step: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfigPostStep, typing.Dict[builtins.str, typing.Any]]] = None,
    pre_step: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfigPreStep, typing.Dict[builtins.str, typing.Any]]] = None,
    reboot_config: typing.Optional[builtins.str] = None,
    windows_update: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdate, typing.Dict[builtins.str, typing.Any]]] = None,
    yum: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfigYum, typing.Dict[builtins.str, typing.Any]]] = None,
    zypper: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfigZypper, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07e4273b232a4916f608d54753bf2d830827716e611caec9f4c3d1cc20531d8f(
    *,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclusive_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aadec446c8a6c7b17730db65354e90fd9de9450aca1ca347ebedd83971ba484(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7003d0e7eabdf04118c8aa82b2eca76cb46fe736582b8c1a6e70d88f0d3ec68d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2078b7ee477b839add23adc2f7f27c4679339b953d0dadf8c04b55076ebadb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16af05329170a3a4a9336bc6cd895ee8fbcd06c518805e1ce412fb0502004f27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283561595999e07a46f2d66014d2348af65801cb9facb68d00e7f718539bd283(
    value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigApt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d6ee1bf5437ed4be4fe996ae08e036068473e6e44bf8f924223c80e71ab2be(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52eb439494c77a9869a23d5e98479f96af81af79af3430386b1b8a794576eb18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0088f709b70356e0b8f90d38eacb93db932648095515963f41567d3bc53e59a2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45616959eb38791724e4e60be80fbce28f86bd62d1c85290c2e5d42c603e5ff0(
    value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigGoo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b256f7bee76d0815ad5326085da54c6f46f965e2b67d54255bd3d04a14ba9abe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef20cb23666a125543170be6a31fb8e8bf827b3319ed243b6564256cc234f693(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae8071fabb4a6c5edf4075e12ff043faaeb5830daf9d5bea24ae0601748139d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750523a2616a0373ce85a91305126c69822d65ede77792db1d000c9e7b0cad36(
    value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981cebd952ca34a7d9992ea1fef2b213d518458885c46a1032ab73b0c756ab99(
    *,
    linux_exec_step_config: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    windows_exec_step_config: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0419035405579cbbf340791334d1d0a3a00085d25c4a86d19ab34aa5f7c6844(
    *,
    allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    gcs_object: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject, typing.Dict[builtins.str, typing.Any]]] = None,
    interpreter: typing.Optional[builtins.str] = None,
    local_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c02d0247d4d58ef5ddad21a4aebd59bf2bbeac19b9918e064c6b2a74712ff1c(
    *,
    bucket: builtins.str,
    generation_number: builtins.str,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__298fd53e743bbb6ed96553858609f075dffaff4147708380b21d96f8dd692370(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb94b7dc1bb525fcd9b4053ca73aa66bc63738174330c1abbdc797a70af622b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dafc5b8745dd49572eeb1f30aab7140051083738c009b84e432effa66ff8d0c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0700e60841144ecdba9bc0f0c16b265683c5380e425bf3bdab52fe0a1b6572(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860b737380e6a4a348d5df6eee386024ebed00161f8bc140b5c72d7b7ec19426(
    value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfigGcsObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8846bc30c0e4d6ad57024425219ffbb3f4151ba17caaeb3d8e7f0222ac18d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb11b76737c04dfa218660250e6ebeef18bc105350294e7aecc5b7607579f8a(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac4b717d2de3512a03cec444cd92bd8c51ba7d8c06c4513bd293bf3107b84a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54cd5b591aefa75b8d4dec82e62214617e758e86d994858c6036bdfcf440dfb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a361a29e496491fb1b36986f800445395f362bad708ec2f00177181246dd65d3(
    value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepLinuxExecStepConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591f4dc64e0a380721f28579f5faa69489cf522ccadfe6e32b15126b8e5baa15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9009886f20f4e19e73a768461add96fe1cfbf5281b4fc2c14783e6dded1cdbb6(
    value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStep],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb80cc2520c45631838c8c74dd23707fe7a4a2d27c78c7a081e34a2aa1eebf17(
    *,
    allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    gcs_object: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject, typing.Dict[builtins.str, typing.Any]]] = None,
    interpreter: typing.Optional[builtins.str] = None,
    local_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6319e3c3758220a66ef6324b3a764b52281e93b5dfb53314b388cb2a72b5025(
    *,
    bucket: builtins.str,
    generation_number: builtins.str,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c667a68c0d784fab45846fe728657e8fe179e1ce59072d8fb17c64b554abe0d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55c3888a063dc2bddc998d92c72a644b59b329a925f51aa9af44d0a87c3be238(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709d991a1b4595663ed09265564e7cd969c21137abb5fd9de2e13a0157ae3941(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c11417d1966af434bb57fe502f339a0ab4d8f1108b9fef3285e36fd7d1aae7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63093a2e44ef89ba5e4c547fd8f8fc0337973f2322208fb611a6a6576e47a940(
    value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfigGcsObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9307c81a87128009a3905aa1fef61176a45643b5548c78984d9238a8289251a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c38069acfce1d53f3e47f5ab0046ef8317bd47945109c7a8bac8d4c65c45a821(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ccbb47932214f6416e9760890fc3f8264cd680f0881707f17468e81390a157(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe8f2a2cf39f28f7f4bc80a161a07227e2753448fd90548e28985e1b2b01821d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e30e25a27273327b2284a5a6ffd252a186232731a1255a42bb91faf426e6d68(
    value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPostStepWindowsExecStepConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71606c462ca0a16bdbdccf6e99fe66fbd0005db82ddc6938d18c9797c6178a38(
    *,
    linux_exec_step_config: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    windows_exec_step_config: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc715959e0884e1cefd3ba12c284e4975970fdb3550a2043e197996f33d5ea8(
    *,
    allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    gcs_object: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject, typing.Dict[builtins.str, typing.Any]]] = None,
    interpreter: typing.Optional[builtins.str] = None,
    local_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f43bbccf381aae7d197f5a3f70a78aacbd165c86fec8ef32e96ab508fd6bd00f(
    *,
    bucket: builtins.str,
    generation_number: builtins.str,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420c482b8820c86ef869fbb0c7ba04951781246eb43ee814950450339556ce79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9bf24a0445ffe5a249a5fbe0ed8cd688dcc91a65ae47d9b619135476e38e266(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac84806a603ad30b51388ec07706c7dee7d86873b6e5b24d0311850722fc192(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186e54dac222bf4a02a8886cda8756fc81c66e029ead01050bf18247c45aa74c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37ecb411f9eec459293e820619c57cd90bef19fe692d1fda6794b6a973fc77d9(
    value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfigGcsObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad1b929b39cafdc14c083e6e6ca62f2dbe28b988998e77a784c4871128faadf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__156253b769bc975d49b327522cb9466ebff3c39efeb7cb886fe8c081a6e8608a(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e5b74674431d423485ad39ddc3253a8135346210d4b7f06a745fa723b49af5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ad4553771baed1bf53a0944b2478ae8b1ae062e83943b3fc9cae1aa98aa7b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc40d3b9246234c4a4bcf17cfd354df891f74043c2fe02ff308bba9e5449b770(
    value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepLinuxExecStepConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a71cca7e6a5f7a6ef6d7bab0e54f04a225d3580fe2d33170d7839b299f0ffb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1461fe14be8d16bd48da4e8f8256901fae7c8cf7a363dd4f354ea8a854262008(
    value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStep],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c737598e58d66d06954e07604ca98a0bb08fba91ac741e64ec475284f9f25c(
    *,
    allowed_success_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    gcs_object: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject, typing.Dict[builtins.str, typing.Any]]] = None,
    interpreter: typing.Optional[builtins.str] = None,
    local_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417d76a53b26f40320bc23c90c33915c8de2e271a59976ec6ca1ab542774a13c(
    *,
    bucket: builtins.str,
    generation_number: builtins.str,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f54bf8c188f919a2e7140c280f1816e0e930c0e40081d9e928197c8826e4a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de4359ccf4de9e013ae042a41c92edb955a2d58f2c4af1b071265e5006910e1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ef8a47afc07213138dd534bfe00cde63194159285b32bdb6938e61c11269a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1980007e85f2c13d12764bfa61fc0759f11b153f66e0bb998e2c5c773909b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31e91e8706ada93ce3cf2f53ecbf759e305311417036b4486327b1665b47c68(
    value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfigGcsObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4693d8a68241682d3a4271b39fe7b1723210c855982cade7a185851a6a00ff23(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b067da1492524bcdd07f9bf3f0f6b91d0cc1cce6a65a6a3e916bb40433ba327(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3a5744a8f5b84f0013506a97c3d020576297ef35e4f1b1aef6eddb6b30561e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2507e65bef3faf48f49c7bc75d81faf87de44c12693ad7d9bf1a63df0850d551(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c231ce73b7c80e48bfe8fe0cfd3bafe689deadc286b5f5a75731593f31fa2a64(
    value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigPreStepWindowsExecStepConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59fc94b7fd06bc95b925e3822c0aff1cc9c96b8e4f9d890090e72638ce53d00e(
    *,
    classifications: typing.Optional[typing.Sequence[builtins.str]] = None,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclusive_patches: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868959277575240d89e021edb6b88fc8aa1edd1ff5eade0bd03f0ad5a82fd298(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ddcfb130e9c555150ef7044aa3066d0039d4a81ee0a767bbdf89fc4e9cde34(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b53543b32f64311606f3653db978b9c5f38bcc5c5ca3136e106294d4f50074(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1fbad604353bc752a002a61abab2fe7787a1b6a079e688e0460facae3a9e424(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363ba4d0b447a1d42aa3de67b74dd995262efaf8506aceee606bc3e6de9da7c4(
    value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigWindowsUpdate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db34eda09ebfc9603af2c854d6e992aec410358f94d142d65529d9a5d0d5d791(
    *,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclusive_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    minimal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d94281220fe074b7ec6351498aeff8f5c818874c9c01435e6dac3d4b003e7bc3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a353e2f115b51d9fe4c7382de9dcad1bf389d49a9583d24d10e8c69e53a6551(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6bbd49670bc0366dc666ea79b918a402dc7a2dc210885aac435298110cccc3c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbae9bde030a7ace4f37821ed5455e9d7e8e189b9ecf1e874e0136340b0dfcc5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edcdc99ab3986a4c0d00da67becccd54458450d0eac75556bf591e777d3839e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c4b4d181fa8075b1b7fa98cdb75a4a59201006c347c6e0dcf3d4d1c83453cb(
    value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigYum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731e3f36297a4273712882bbad41c82acc5a24c775c810f46dedf3e64e38aec5(
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

def _typecheckingstub__ac7f825b9c00bc917eb99acdf8dc085e990801f396037af8aa1f0bac43997da4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4d7116aa2ba5437ac958cd56b77047c1cc048974bd05f04219ae6c3da73204(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f363541d8363b1c40f9e8d99e190c67f3202227770d519a3549b733a3b7cad(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36bd05627cb3fbda0a6937a72bcb85f492656039f70239906781e1f6618e536(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c353e06b24524a72e3be5d640459d604c8afc4aaa183f05a3e1ea1be5a7994(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c51c2c32059617ae92538f5bed20ce158b43b34a5c8316828d187b2a4eca9b6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75987891c749ee779a01caba8641dc3e5d7d4a6086367fa1cf037dd4d3ec9836(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e808f777e93b65146091e61719cd692f20f3593f225fd6f7d8911be65beb34(
    value: typing.Optional[GoogleOsConfigPatchDeploymentPatchConfigZypper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c23e5575224ca594a1e42cf4235d1b07e222fc76ebd7fc5b6b767dc41610b278(
    *,
    time_of_day: typing.Union[GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDay, typing.Dict[builtins.str, typing.Any]],
    time_zone: typing.Union[GoogleOsConfigPatchDeploymentRecurringScheduleTimeZone, typing.Dict[builtins.str, typing.Any]],
    end_time: typing.Optional[builtins.str] = None,
    monthly: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentRecurringScheduleMonthly, typing.Dict[builtins.str, typing.Any]]] = None,
    start_time: typing.Optional[builtins.str] = None,
    weekly: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentRecurringScheduleWeekly, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6bda1909019fb03018db678321cae8db1531116f2eac7dafb48537be6ede2ad(
    *,
    month_day: typing.Optional[jsii.Number] = None,
    week_day_of_month: typing.Optional[typing.Union[GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab04552a3f75637dfaddda9df761944640e804b9f541cf9aed6ac97d7729087(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8764e1babe72056c9238963764b65e0f24f24e9a927f8159fd2880c25a789714(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e8629c562b6fbea56f35fd79869c1f06b28256aba0713dad115fb8a32c616d(
    value: typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleMonthly],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce994e0f56865e32838f6cc5892813d90abaf92f4c36634610b31e0b2d923204(
    *,
    day_of_week: builtins.str,
    week_ordinal: jsii.Number,
    day_offset: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5958d1ec48cd5f24d496c18b07078a31e0b2bcbac9735eb27fd53a7f5d5ebb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580c39558a6785071874f7dba117ced72dc3eba20e6fea6ef7015f807d362e6c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069e15fe611fd716f6489681be79c79f73f653a61e74630db628c44d3cb760a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9c71840edde6c165bed2ad8be2fe6db6b158f89b79a712476d78e7237858fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fbbe27ea3e0aaa44498cc672d6ecdd7e6d8913813739dd4cdc404929d9775be(
    value: typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleMonthlyWeekDayOfMonth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd89b973958bf8087232122fe1aeb9f35ab3e4d4753592702d4cd5626b14df7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59bfe6f170fac216b2ee052927aa0d13aa29b4ddcf6124f07b1f437369723c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b5ec490b5e51b044e1f19a336f94f7be7358c4d820b8d7cad2d49766974150(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f26fd81a967902c1738229b52c3ad1e9ae1d14768f6ead70bb829ff78e5833(
    value: typing.Optional[GoogleOsConfigPatchDeploymentRecurringSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef58dafc09f6ec96b8caba4cfea08e01e1aee725002c5324a585274d751489e(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1519f6237846148b2845fdfaf9723d12115d572b4efc36772dbab32ba608db8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f73a147bec8d8ea45a2fba0428ade30f654e3a8593b859e71e74748a5a8286d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc4e5ce30fc65f3428cb274d76b9e68d95db17b655bf22a8f7de03368afdd27(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a0e036d4dba4e53f5d3e43926a3a97675213646a7c926b2e16013cd70c98e4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__893e992d3b9337232f043f9dd38930a02562a93ea0d990c20caf03546a9a4835(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c60f6094e55d62565e8b851fecb1e5cb1b88269509acefe88ad32b0e63a106c7(
    value: typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleTimeOfDay],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4f4de42509fed97c3ed53dd8934d09da82dfecdbb4608b09640b365a01b6fd(
    *,
    id: builtins.str,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75137fc65db26da5e1083c435b778b69ff029ee084de5d49fc8bbdd3d2a62547(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6e26941288cb282c4064c4bfe954916696ca477bd8ee86b430cbb9fb27d1b95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__729ca5d5baee574bef31485261f767a11ae10010d89bbc03cf2593974f433485(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf98bd30dade67e52c6275ecf38e968b09504ba6d63737dda2cf1d209865755a(
    value: typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleTimeZone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5517cad2ffd3c5554382386f1a4e4523c9482440a95182f1a8913bc4af0c5ce3(
    *,
    day_of_week: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc5fb4e0d0d95f8ecb358ec128a2f29f4feac6fc5f73b1f090848b68e495d6c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecf841fbac454b6a7b5736d818ccd84241033ada478b2eaf1467b04f18e3244(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ecca301bf2be7a3400455d8bfe5bd5e4058bd080fafe2cdf3b06699c452f279(
    value: typing.Optional[GoogleOsConfigPatchDeploymentRecurringScheduleWeekly],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b440ca909996f157bc970232d7b43b9938ed7873b88943c3887b52e31b1183f(
    *,
    disruption_budget: typing.Union[GoogleOsConfigPatchDeploymentRolloutDisruptionBudget, typing.Dict[builtins.str, typing.Any]],
    mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c851851f502fbd58e28e09f6ebed10d6e4309730fa0d8cad871822f15a22c39(
    *,
    fixed: typing.Optional[jsii.Number] = None,
    percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f26f8d71ccc6e187a9fbe1c1b022eefcf80ddca257fad7cf7878bbd0a7eb97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__656e47c66886545d2eb8bac660eb14f6b22aa9ba2805e7e133dd8cdaab1bebb1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041817194af7387e7959817aaaebc36cb49e65d19212c9d8d561bd2e9cbd3efb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd4e30bbc0f5a8c66bf2b5a6c3c14d65959111af175e3992b837946b62e6131(
    value: typing.Optional[GoogleOsConfigPatchDeploymentRolloutDisruptionBudget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a04f47956f8f7e308a716c72339513b790ecbdaed3ef1c93747a8e3cf310bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf95e7ebc4f29377f2bca1fd0ec89a016bba36271b9600c4f5c9ef4c88942e0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c2d0474d680758b70207e892cc411a822807296a6352b7a0f4c096210f6388(
    value: typing.Optional[GoogleOsConfigPatchDeploymentRollout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333b9aa61f1d0f6c7275ff0c7c3b58a988e13ed777c51104c69ac6d01a9c325a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee67cf4159e1dae4db55af5525a93ff5a0fe832b5659bc1156dcccaea761ebc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cd94c0a509ca23f8dbf2b9bec852f979f2735fdc1c2ac89b324858746bf63dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f694984cd7be59ebe717fd389ca6110ec99875844f8e31e72b17cc1cc714c968(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe803d25d801a6c5817523fb182646eebe78f1c54ec842d63c73864b4579b68(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigPatchDeploymentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `azurerm_automation_software_update_configuration`

Refer to the Terraform Registry for docs: [`azurerm_automation_software_update_configuration`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration).
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


class AutomationSoftwareUpdateConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration azurerm_automation_software_update_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        automation_account_id: builtins.str,
        name: builtins.str,
        schedule: typing.Union["AutomationSoftwareUpdateConfigurationSchedule", typing.Dict[builtins.str, typing.Any]],
        duration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        linux: typing.Optional[typing.Union["AutomationSoftwareUpdateConfigurationLinux", typing.Dict[builtins.str, typing.Any]]] = None,
        non_azure_computer_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        post_task: typing.Optional[typing.Union["AutomationSoftwareUpdateConfigurationPostTask", typing.Dict[builtins.str, typing.Any]]] = None,
        pre_task: typing.Optional[typing.Union["AutomationSoftwareUpdateConfigurationPreTask", typing.Dict[builtins.str, typing.Any]]] = None,
        target: typing.Optional[typing.Union["AutomationSoftwareUpdateConfigurationTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["AutomationSoftwareUpdateConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        windows: typing.Optional[typing.Union["AutomationSoftwareUpdateConfigurationWindows", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration azurerm_automation_software_update_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param automation_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#automation_account_id AutomationSoftwareUpdateConfiguration#automation_account_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#name AutomationSoftwareUpdateConfiguration#name}.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#schedule AutomationSoftwareUpdateConfiguration#schedule}
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#duration AutomationSoftwareUpdateConfiguration#duration}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#id AutomationSoftwareUpdateConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param linux: linux block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#linux AutomationSoftwareUpdateConfiguration#linux}
        :param non_azure_computer_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#non_azure_computer_names AutomationSoftwareUpdateConfiguration#non_azure_computer_names}.
        :param post_task: post_task block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#post_task AutomationSoftwareUpdateConfiguration#post_task}
        :param pre_task: pre_task block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#pre_task AutomationSoftwareUpdateConfiguration#pre_task}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#target AutomationSoftwareUpdateConfiguration#target}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#timeouts AutomationSoftwareUpdateConfiguration#timeouts}
        :param virtual_machine_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#virtual_machine_ids AutomationSoftwareUpdateConfiguration#virtual_machine_ids}.
        :param windows: windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#windows AutomationSoftwareUpdateConfiguration#windows}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ebf73eff841fc40a68d40998a7cc9b471767b03e3c3f92df120b5ef821f48be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AutomationSoftwareUpdateConfigurationConfig(
            automation_account_id=automation_account_id,
            name=name,
            schedule=schedule,
            duration=duration,
            id=id,
            linux=linux,
            non_azure_computer_names=non_azure_computer_names,
            post_task=post_task,
            pre_task=pre_task,
            target=target,
            timeouts=timeouts,
            virtual_machine_ids=virtual_machine_ids,
            windows=windows,
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
        '''Generates CDKTF code for importing a AutomationSoftwareUpdateConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AutomationSoftwareUpdateConfiguration to import.
        :param import_from_id: The id of the existing AutomationSoftwareUpdateConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AutomationSoftwareUpdateConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f22c0671220f860a6cbf2eddd65910852ace84f08defc7ddcc69d3a3607d104)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLinux")
    def put_linux(
        self,
        *,
        classifications_included: typing.Sequence[builtins.str],
        excluded_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        reboot: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param classifications_included: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#classifications_included AutomationSoftwareUpdateConfiguration#classifications_included}.
        :param excluded_packages: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#excluded_packages AutomationSoftwareUpdateConfiguration#excluded_packages}.
        :param included_packages: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#included_packages AutomationSoftwareUpdateConfiguration#included_packages}.
        :param reboot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#reboot AutomationSoftwareUpdateConfiguration#reboot}.
        '''
        value = AutomationSoftwareUpdateConfigurationLinux(
            classifications_included=classifications_included,
            excluded_packages=excluded_packages,
            included_packages=included_packages,
            reboot=reboot,
        )

        return typing.cast(None, jsii.invoke(self, "putLinux", [value]))

    @jsii.member(jsii_name="putPostTask")
    def put_post_task(
        self,
        *,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#parameters AutomationSoftwareUpdateConfiguration#parameters}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#source AutomationSoftwareUpdateConfiguration#source}.
        '''
        value = AutomationSoftwareUpdateConfigurationPostTask(
            parameters=parameters, source=source
        )

        return typing.cast(None, jsii.invoke(self, "putPostTask", [value]))

    @jsii.member(jsii_name="putPreTask")
    def put_pre_task(
        self,
        *,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#parameters AutomationSoftwareUpdateConfiguration#parameters}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#source AutomationSoftwareUpdateConfiguration#source}.
        '''
        value = AutomationSoftwareUpdateConfigurationPreTask(
            parameters=parameters, source=source
        )

        return typing.cast(None, jsii.invoke(self, "putPreTask", [value]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        frequency: builtins.str,
        advanced_month_days: typing.Optional[typing.Sequence[jsii.Number]] = None,
        advanced_week_days: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        expiry_time: typing.Optional[builtins.str] = None,
        expiry_time_offset_minutes: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monthly_occurrence: typing.Optional[typing.Union["AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrence", typing.Dict[builtins.str, typing.Any]]] = None,
        next_run: typing.Optional[builtins.str] = None,
        next_run_offset_minutes: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[builtins.str] = None,
        start_time_offset_minutes: typing.Optional[jsii.Number] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#frequency AutomationSoftwareUpdateConfiguration#frequency}.
        :param advanced_month_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#advanced_month_days AutomationSoftwareUpdateConfiguration#advanced_month_days}.
        :param advanced_week_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#advanced_week_days AutomationSoftwareUpdateConfiguration#advanced_week_days}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#description AutomationSoftwareUpdateConfiguration#description}.
        :param expiry_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#expiry_time AutomationSoftwareUpdateConfiguration#expiry_time}.
        :param expiry_time_offset_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#expiry_time_offset_minutes AutomationSoftwareUpdateConfiguration#expiry_time_offset_minutes}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#interval AutomationSoftwareUpdateConfiguration#interval}.
        :param is_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#is_enabled AutomationSoftwareUpdateConfiguration#is_enabled}.
        :param monthly_occurrence: monthly_occurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#monthly_occurrence AutomationSoftwareUpdateConfiguration#monthly_occurrence}
        :param next_run: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#next_run AutomationSoftwareUpdateConfiguration#next_run}.
        :param next_run_offset_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#next_run_offset_minutes AutomationSoftwareUpdateConfiguration#next_run_offset_minutes}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#start_time AutomationSoftwareUpdateConfiguration#start_time}.
        :param start_time_offset_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#start_time_offset_minutes AutomationSoftwareUpdateConfiguration#start_time_offset_minutes}.
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#time_zone AutomationSoftwareUpdateConfiguration#time_zone}.
        '''
        value = AutomationSoftwareUpdateConfigurationSchedule(
            frequency=frequency,
            advanced_month_days=advanced_month_days,
            advanced_week_days=advanced_week_days,
            description=description,
            expiry_time=expiry_time,
            expiry_time_offset_minutes=expiry_time_offset_minutes,
            interval=interval,
            is_enabled=is_enabled,
            monthly_occurrence=monthly_occurrence,
            next_run=next_run,
            next_run_offset_minutes=next_run_offset_minutes,
            start_time=start_time,
            start_time_offset_minutes=start_time_offset_minutes,
            time_zone=time_zone,
        )

        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        azure_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AutomationSoftwareUpdateConfigurationTargetAzureQuery", typing.Dict[builtins.str, typing.Any]]]]] = None,
        non_azure_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AutomationSoftwareUpdateConfigurationTargetNonAzureQuery", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param azure_query: azure_query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#azure_query AutomationSoftwareUpdateConfiguration#azure_query}
        :param non_azure_query: non_azure_query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#non_azure_query AutomationSoftwareUpdateConfiguration#non_azure_query}
        '''
        value = AutomationSoftwareUpdateConfigurationTarget(
            azure_query=azure_query, non_azure_query=non_azure_query
        )

        return typing.cast(None, jsii.invoke(self, "putTarget", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#create AutomationSoftwareUpdateConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#delete AutomationSoftwareUpdateConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#read AutomationSoftwareUpdateConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#update AutomationSoftwareUpdateConfiguration#update}.
        '''
        value = AutomationSoftwareUpdateConfigurationTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWindows")
    def put_windows(
        self,
        *,
        classifications_included: typing.Sequence[builtins.str],
        excluded_knowledge_base_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_knowledge_base_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
        reboot: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param classifications_included: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#classifications_included AutomationSoftwareUpdateConfiguration#classifications_included}.
        :param excluded_knowledge_base_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#excluded_knowledge_base_numbers AutomationSoftwareUpdateConfiguration#excluded_knowledge_base_numbers}.
        :param included_knowledge_base_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#included_knowledge_base_numbers AutomationSoftwareUpdateConfiguration#included_knowledge_base_numbers}.
        :param reboot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#reboot AutomationSoftwareUpdateConfiguration#reboot}.
        '''
        value = AutomationSoftwareUpdateConfigurationWindows(
            classifications_included=classifications_included,
            excluded_knowledge_base_numbers=excluded_knowledge_base_numbers,
            included_knowledge_base_numbers=included_knowledge_base_numbers,
            reboot=reboot,
        )

        return typing.cast(None, jsii.invoke(self, "putWindows", [value]))

    @jsii.member(jsii_name="resetDuration")
    def reset_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLinux")
    def reset_linux(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinux", []))

    @jsii.member(jsii_name="resetNonAzureComputerNames")
    def reset_non_azure_computer_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNonAzureComputerNames", []))

    @jsii.member(jsii_name="resetPostTask")
    def reset_post_task(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostTask", []))

    @jsii.member(jsii_name="resetPreTask")
    def reset_pre_task(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreTask", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVirtualMachineIds")
    def reset_virtual_machine_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualMachineIds", []))

    @jsii.member(jsii_name="resetWindows")
    def reset_windows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindows", []))

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
    @jsii.member(jsii_name="errorCode")
    def error_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorCode"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="linux")
    def linux(self) -> "AutomationSoftwareUpdateConfigurationLinuxOutputReference":
        return typing.cast("AutomationSoftwareUpdateConfigurationLinuxOutputReference", jsii.get(self, "linux"))

    @builtins.property
    @jsii.member(jsii_name="postTask")
    def post_task(
        self,
    ) -> "AutomationSoftwareUpdateConfigurationPostTaskOutputReference":
        return typing.cast("AutomationSoftwareUpdateConfigurationPostTaskOutputReference", jsii.get(self, "postTask"))

    @builtins.property
    @jsii.member(jsii_name="preTask")
    def pre_task(self) -> "AutomationSoftwareUpdateConfigurationPreTaskOutputReference":
        return typing.cast("AutomationSoftwareUpdateConfigurationPreTaskOutputReference", jsii.get(self, "preTask"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> "AutomationSoftwareUpdateConfigurationScheduleOutputReference":
        return typing.cast("AutomationSoftwareUpdateConfigurationScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "AutomationSoftwareUpdateConfigurationTargetOutputReference":
        return typing.cast("AutomationSoftwareUpdateConfigurationTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "AutomationSoftwareUpdateConfigurationTimeoutsOutputReference":
        return typing.cast("AutomationSoftwareUpdateConfigurationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="windows")
    def windows(self) -> "AutomationSoftwareUpdateConfigurationWindowsOutputReference":
        return typing.cast("AutomationSoftwareUpdateConfigurationWindowsOutputReference", jsii.get(self, "windows"))

    @builtins.property
    @jsii.member(jsii_name="automationAccountIdInput")
    def automation_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "automationAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="linuxInput")
    def linux_input(
        self,
    ) -> typing.Optional["AutomationSoftwareUpdateConfigurationLinux"]:
        return typing.cast(typing.Optional["AutomationSoftwareUpdateConfigurationLinux"], jsii.get(self, "linuxInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nonAzureComputerNamesInput")
    def non_azure_computer_names_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "nonAzureComputerNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="postTaskInput")
    def post_task_input(
        self,
    ) -> typing.Optional["AutomationSoftwareUpdateConfigurationPostTask"]:
        return typing.cast(typing.Optional["AutomationSoftwareUpdateConfigurationPostTask"], jsii.get(self, "postTaskInput"))

    @builtins.property
    @jsii.member(jsii_name="preTaskInput")
    def pre_task_input(
        self,
    ) -> typing.Optional["AutomationSoftwareUpdateConfigurationPreTask"]:
        return typing.cast(typing.Optional["AutomationSoftwareUpdateConfigurationPreTask"], jsii.get(self, "preTaskInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional["AutomationSoftwareUpdateConfigurationSchedule"]:
        return typing.cast(typing.Optional["AutomationSoftwareUpdateConfigurationSchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["AutomationSoftwareUpdateConfigurationTarget"]:
        return typing.cast(typing.Optional["AutomationSoftwareUpdateConfigurationTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AutomationSoftwareUpdateConfigurationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AutomationSoftwareUpdateConfigurationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineIdsInput")
    def virtual_machine_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "virtualMachineIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsInput")
    def windows_input(
        self,
    ) -> typing.Optional["AutomationSoftwareUpdateConfigurationWindows"]:
        return typing.cast(typing.Optional["AutomationSoftwareUpdateConfigurationWindows"], jsii.get(self, "windowsInput"))

    @builtins.property
    @jsii.member(jsii_name="automationAccountId")
    def automation_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "automationAccountId"))

    @automation_account_id.setter
    def automation_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7772c2854853e6d780827e4a6190839170b3ed096169461da351d0de0f1dd67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automationAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a6b87b80ca57bc194224fafd1a741fc9dc5ba892fbe99d0084d0756f717d8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a06010833339ff60218c55a078a9130e44485cb604539988472b5e597323f6c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bffae33b6d1e76e7e64dd8a5eaa4b0af8b2d8bea2a783472f1c062f7a47db925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nonAzureComputerNames")
    def non_azure_computer_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "nonAzureComputerNames"))

    @non_azure_computer_names.setter
    def non_azure_computer_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b242e1936b469a6a6d4a3414c58855b703deb187ae173769c87e0f842e2e55e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nonAzureComputerNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualMachineIds")
    def virtual_machine_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "virtualMachineIds"))

    @virtual_machine_ids.setter
    def virtual_machine_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ece8ebc04fa7934c0a6108c3cc525b37d5b75e253505f4352fd7cef9b1e3236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualMachineIds", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "automation_account_id": "automationAccountId",
        "name": "name",
        "schedule": "schedule",
        "duration": "duration",
        "id": "id",
        "linux": "linux",
        "non_azure_computer_names": "nonAzureComputerNames",
        "post_task": "postTask",
        "pre_task": "preTask",
        "target": "target",
        "timeouts": "timeouts",
        "virtual_machine_ids": "virtualMachineIds",
        "windows": "windows",
    },
)
class AutomationSoftwareUpdateConfigurationConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        automation_account_id: builtins.str,
        name: builtins.str,
        schedule: typing.Union["AutomationSoftwareUpdateConfigurationSchedule", typing.Dict[builtins.str, typing.Any]],
        duration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        linux: typing.Optional[typing.Union["AutomationSoftwareUpdateConfigurationLinux", typing.Dict[builtins.str, typing.Any]]] = None,
        non_azure_computer_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        post_task: typing.Optional[typing.Union["AutomationSoftwareUpdateConfigurationPostTask", typing.Dict[builtins.str, typing.Any]]] = None,
        pre_task: typing.Optional[typing.Union["AutomationSoftwareUpdateConfigurationPreTask", typing.Dict[builtins.str, typing.Any]]] = None,
        target: typing.Optional[typing.Union["AutomationSoftwareUpdateConfigurationTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["AutomationSoftwareUpdateConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        windows: typing.Optional[typing.Union["AutomationSoftwareUpdateConfigurationWindows", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param automation_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#automation_account_id AutomationSoftwareUpdateConfiguration#automation_account_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#name AutomationSoftwareUpdateConfiguration#name}.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#schedule AutomationSoftwareUpdateConfiguration#schedule}
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#duration AutomationSoftwareUpdateConfiguration#duration}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#id AutomationSoftwareUpdateConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param linux: linux block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#linux AutomationSoftwareUpdateConfiguration#linux}
        :param non_azure_computer_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#non_azure_computer_names AutomationSoftwareUpdateConfiguration#non_azure_computer_names}.
        :param post_task: post_task block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#post_task AutomationSoftwareUpdateConfiguration#post_task}
        :param pre_task: pre_task block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#pre_task AutomationSoftwareUpdateConfiguration#pre_task}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#target AutomationSoftwareUpdateConfiguration#target}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#timeouts AutomationSoftwareUpdateConfiguration#timeouts}
        :param virtual_machine_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#virtual_machine_ids AutomationSoftwareUpdateConfiguration#virtual_machine_ids}.
        :param windows: windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#windows AutomationSoftwareUpdateConfiguration#windows}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(schedule, dict):
            schedule = AutomationSoftwareUpdateConfigurationSchedule(**schedule)
        if isinstance(linux, dict):
            linux = AutomationSoftwareUpdateConfigurationLinux(**linux)
        if isinstance(post_task, dict):
            post_task = AutomationSoftwareUpdateConfigurationPostTask(**post_task)
        if isinstance(pre_task, dict):
            pre_task = AutomationSoftwareUpdateConfigurationPreTask(**pre_task)
        if isinstance(target, dict):
            target = AutomationSoftwareUpdateConfigurationTarget(**target)
        if isinstance(timeouts, dict):
            timeouts = AutomationSoftwareUpdateConfigurationTimeouts(**timeouts)
        if isinstance(windows, dict):
            windows = AutomationSoftwareUpdateConfigurationWindows(**windows)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__282d37b958d5c9973367d2c1d5d4ec7975d6eb7400fb8bf4efe9d33ba3ae997b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument automation_account_id", value=automation_account_id, expected_type=type_hints["automation_account_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument linux", value=linux, expected_type=type_hints["linux"])
            check_type(argname="argument non_azure_computer_names", value=non_azure_computer_names, expected_type=type_hints["non_azure_computer_names"])
            check_type(argname="argument post_task", value=post_task, expected_type=type_hints["post_task"])
            check_type(argname="argument pre_task", value=pre_task, expected_type=type_hints["pre_task"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument virtual_machine_ids", value=virtual_machine_ids, expected_type=type_hints["virtual_machine_ids"])
            check_type(argname="argument windows", value=windows, expected_type=type_hints["windows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "automation_account_id": automation_account_id,
            "name": name,
            "schedule": schedule,
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
        if duration is not None:
            self._values["duration"] = duration
        if id is not None:
            self._values["id"] = id
        if linux is not None:
            self._values["linux"] = linux
        if non_azure_computer_names is not None:
            self._values["non_azure_computer_names"] = non_azure_computer_names
        if post_task is not None:
            self._values["post_task"] = post_task
        if pre_task is not None:
            self._values["pre_task"] = pre_task
        if target is not None:
            self._values["target"] = target
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if virtual_machine_ids is not None:
            self._values["virtual_machine_ids"] = virtual_machine_ids
        if windows is not None:
            self._values["windows"] = windows

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
    def automation_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#automation_account_id AutomationSoftwareUpdateConfiguration#automation_account_id}.'''
        result = self._values.get("automation_account_id")
        assert result is not None, "Required property 'automation_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#name AutomationSoftwareUpdateConfiguration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(self) -> "AutomationSoftwareUpdateConfigurationSchedule":
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#schedule AutomationSoftwareUpdateConfiguration#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast("AutomationSoftwareUpdateConfigurationSchedule", result)

    @builtins.property
    def duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#duration AutomationSoftwareUpdateConfiguration#duration}.'''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#id AutomationSoftwareUpdateConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def linux(self) -> typing.Optional["AutomationSoftwareUpdateConfigurationLinux"]:
        '''linux block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#linux AutomationSoftwareUpdateConfiguration#linux}
        '''
        result = self._values.get("linux")
        return typing.cast(typing.Optional["AutomationSoftwareUpdateConfigurationLinux"], result)

    @builtins.property
    def non_azure_computer_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#non_azure_computer_names AutomationSoftwareUpdateConfiguration#non_azure_computer_names}.'''
        result = self._values.get("non_azure_computer_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def post_task(
        self,
    ) -> typing.Optional["AutomationSoftwareUpdateConfigurationPostTask"]:
        '''post_task block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#post_task AutomationSoftwareUpdateConfiguration#post_task}
        '''
        result = self._values.get("post_task")
        return typing.cast(typing.Optional["AutomationSoftwareUpdateConfigurationPostTask"], result)

    @builtins.property
    def pre_task(
        self,
    ) -> typing.Optional["AutomationSoftwareUpdateConfigurationPreTask"]:
        '''pre_task block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#pre_task AutomationSoftwareUpdateConfiguration#pre_task}
        '''
        result = self._values.get("pre_task")
        return typing.cast(typing.Optional["AutomationSoftwareUpdateConfigurationPreTask"], result)

    @builtins.property
    def target(self) -> typing.Optional["AutomationSoftwareUpdateConfigurationTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#target AutomationSoftwareUpdateConfiguration#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["AutomationSoftwareUpdateConfigurationTarget"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["AutomationSoftwareUpdateConfigurationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#timeouts AutomationSoftwareUpdateConfiguration#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AutomationSoftwareUpdateConfigurationTimeouts"], result)

    @builtins.property
    def virtual_machine_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#virtual_machine_ids AutomationSoftwareUpdateConfiguration#virtual_machine_ids}.'''
        result = self._values.get("virtual_machine_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def windows(
        self,
    ) -> typing.Optional["AutomationSoftwareUpdateConfigurationWindows"]:
        '''windows block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#windows AutomationSoftwareUpdateConfiguration#windows}
        '''
        result = self._values.get("windows")
        return typing.cast(typing.Optional["AutomationSoftwareUpdateConfigurationWindows"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomationSoftwareUpdateConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationLinux",
    jsii_struct_bases=[],
    name_mapping={
        "classifications_included": "classificationsIncluded",
        "excluded_packages": "excludedPackages",
        "included_packages": "includedPackages",
        "reboot": "reboot",
    },
)
class AutomationSoftwareUpdateConfigurationLinux:
    def __init__(
        self,
        *,
        classifications_included: typing.Sequence[builtins.str],
        excluded_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        reboot: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param classifications_included: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#classifications_included AutomationSoftwareUpdateConfiguration#classifications_included}.
        :param excluded_packages: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#excluded_packages AutomationSoftwareUpdateConfiguration#excluded_packages}.
        :param included_packages: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#included_packages AutomationSoftwareUpdateConfiguration#included_packages}.
        :param reboot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#reboot AutomationSoftwareUpdateConfiguration#reboot}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32df5f2508dcfc6496351c348730bb23ac11565a8b52806ce6417597e13f258a)
            check_type(argname="argument classifications_included", value=classifications_included, expected_type=type_hints["classifications_included"])
            check_type(argname="argument excluded_packages", value=excluded_packages, expected_type=type_hints["excluded_packages"])
            check_type(argname="argument included_packages", value=included_packages, expected_type=type_hints["included_packages"])
            check_type(argname="argument reboot", value=reboot, expected_type=type_hints["reboot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "classifications_included": classifications_included,
        }
        if excluded_packages is not None:
            self._values["excluded_packages"] = excluded_packages
        if included_packages is not None:
            self._values["included_packages"] = included_packages
        if reboot is not None:
            self._values["reboot"] = reboot

    @builtins.property
    def classifications_included(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#classifications_included AutomationSoftwareUpdateConfiguration#classifications_included}.'''
        result = self._values.get("classifications_included")
        assert result is not None, "Required property 'classifications_included' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def excluded_packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#excluded_packages AutomationSoftwareUpdateConfiguration#excluded_packages}.'''
        result = self._values.get("excluded_packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#included_packages AutomationSoftwareUpdateConfiguration#included_packages}.'''
        result = self._values.get("included_packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def reboot(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#reboot AutomationSoftwareUpdateConfiguration#reboot}.'''
        result = self._values.get("reboot")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomationSoftwareUpdateConfigurationLinux(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomationSoftwareUpdateConfigurationLinuxOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationLinuxOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a10505503bf9e0718247aa728bece41fd7695dcb42e91c8eb3c56d868a31195d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludedPackages")
    def reset_excluded_packages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedPackages", []))

    @jsii.member(jsii_name="resetIncludedPackages")
    def reset_included_packages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedPackages", []))

    @jsii.member(jsii_name="resetReboot")
    def reset_reboot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReboot", []))

    @builtins.property
    @jsii.member(jsii_name="classificationsIncludedInput")
    def classifications_included_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "classificationsIncludedInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedPackagesInput")
    def excluded_packages_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedPackagesInput"))

    @builtins.property
    @jsii.member(jsii_name="includedPackagesInput")
    def included_packages_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedPackagesInput"))

    @builtins.property
    @jsii.member(jsii_name="rebootInput")
    def reboot_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rebootInput"))

    @builtins.property
    @jsii.member(jsii_name="classificationsIncluded")
    def classifications_included(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "classificationsIncluded"))

    @classifications_included.setter
    def classifications_included(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc17f93f99220842aa4f3f5d79b6dae62589044526ce4cbb7fe9d6d6bb08a38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classificationsIncluded", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedPackages")
    def excluded_packages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedPackages"))

    @excluded_packages.setter
    def excluded_packages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfce571bb2a870d6a3215d2c7c6b36f15a89686a4a4e9575f6a69a4f9d187f9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedPackages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedPackages")
    def included_packages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedPackages"))

    @included_packages.setter
    def included_packages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa724957bf7096a78fb6a6a44bcf47355e7fade8f54e913d3bc7225dbe9599b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedPackages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reboot")
    def reboot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reboot"))

    @reboot.setter
    def reboot(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc95d1bdf9374857179c5f79b82e30e8b0c9ffa7c0f0f545a402ed865cfad945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reboot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AutomationSoftwareUpdateConfigurationLinux]:
        return typing.cast(typing.Optional[AutomationSoftwareUpdateConfigurationLinux], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomationSoftwareUpdateConfigurationLinux],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__567f1b4bb711853758f95622f2de8449c3567d0ba5660028db81055c51c97a0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationPostTask",
    jsii_struct_bases=[],
    name_mapping={"parameters": "parameters", "source": "source"},
)
class AutomationSoftwareUpdateConfigurationPostTask:
    def __init__(
        self,
        *,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#parameters AutomationSoftwareUpdateConfiguration#parameters}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#source AutomationSoftwareUpdateConfiguration#source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e5f6d37ffcff754ab84e18d7bd056e5a17f7c8d31d7613b9abd089c6a1e22f)
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if parameters is not None:
            self._values["parameters"] = parameters
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#parameters AutomationSoftwareUpdateConfiguration#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#source AutomationSoftwareUpdateConfiguration#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomationSoftwareUpdateConfigurationPostTask(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomationSoftwareUpdateConfigurationPostTaskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationPostTaskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe901174a7ec47277b4552243500d08e5ad4d60cad33f41c2033c706054da0e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4170dfa10d63113db660b803205f0a10786f220ebe4df893b1e0cfebdf24234c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27379006bb5887006fc1b985e3fd12327c7820ae209aecd85ef049158461886e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AutomationSoftwareUpdateConfigurationPostTask]:
        return typing.cast(typing.Optional[AutomationSoftwareUpdateConfigurationPostTask], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomationSoftwareUpdateConfigurationPostTask],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c29b4322efb7bebd0932a6b20c033d40c2639cf98cabeafb32e49361f741615d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationPreTask",
    jsii_struct_bases=[],
    name_mapping={"parameters": "parameters", "source": "source"},
)
class AutomationSoftwareUpdateConfigurationPreTask:
    def __init__(
        self,
        *,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#parameters AutomationSoftwareUpdateConfiguration#parameters}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#source AutomationSoftwareUpdateConfiguration#source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0da824885269830e599198325601384abee7854b567426167f187da3a9afafa)
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if parameters is not None:
            self._values["parameters"] = parameters
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#parameters AutomationSoftwareUpdateConfiguration#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#source AutomationSoftwareUpdateConfiguration#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomationSoftwareUpdateConfigurationPreTask(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomationSoftwareUpdateConfigurationPreTaskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationPreTaskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba50d8b58791cb24e2e151cf6e57a84e23c15601485915b70682f24f86b7ce46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc35683f993bf9468c81954d762c3ad18a57d41ab237c50f283f0eaaf102f8c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3afc6f9710d4d5bb4e391609663b62bb1f691e52bf87132c17a41f9fa58b5b81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AutomationSoftwareUpdateConfigurationPreTask]:
        return typing.cast(typing.Optional[AutomationSoftwareUpdateConfigurationPreTask], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomationSoftwareUpdateConfigurationPreTask],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12e54bbaaee91742312632960b29bf14f50f0b3ba2b7160f6660f80c30a4d7c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "frequency": "frequency",
        "advanced_month_days": "advancedMonthDays",
        "advanced_week_days": "advancedWeekDays",
        "description": "description",
        "expiry_time": "expiryTime",
        "expiry_time_offset_minutes": "expiryTimeOffsetMinutes",
        "interval": "interval",
        "is_enabled": "isEnabled",
        "monthly_occurrence": "monthlyOccurrence",
        "next_run": "nextRun",
        "next_run_offset_minutes": "nextRunOffsetMinutes",
        "start_time": "startTime",
        "start_time_offset_minutes": "startTimeOffsetMinutes",
        "time_zone": "timeZone",
    },
)
class AutomationSoftwareUpdateConfigurationSchedule:
    def __init__(
        self,
        *,
        frequency: builtins.str,
        advanced_month_days: typing.Optional[typing.Sequence[jsii.Number]] = None,
        advanced_week_days: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        expiry_time: typing.Optional[builtins.str] = None,
        expiry_time_offset_minutes: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monthly_occurrence: typing.Optional[typing.Union["AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrence", typing.Dict[builtins.str, typing.Any]]] = None,
        next_run: typing.Optional[builtins.str] = None,
        next_run_offset_minutes: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[builtins.str] = None,
        start_time_offset_minutes: typing.Optional[jsii.Number] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#frequency AutomationSoftwareUpdateConfiguration#frequency}.
        :param advanced_month_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#advanced_month_days AutomationSoftwareUpdateConfiguration#advanced_month_days}.
        :param advanced_week_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#advanced_week_days AutomationSoftwareUpdateConfiguration#advanced_week_days}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#description AutomationSoftwareUpdateConfiguration#description}.
        :param expiry_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#expiry_time AutomationSoftwareUpdateConfiguration#expiry_time}.
        :param expiry_time_offset_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#expiry_time_offset_minutes AutomationSoftwareUpdateConfiguration#expiry_time_offset_minutes}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#interval AutomationSoftwareUpdateConfiguration#interval}.
        :param is_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#is_enabled AutomationSoftwareUpdateConfiguration#is_enabled}.
        :param monthly_occurrence: monthly_occurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#monthly_occurrence AutomationSoftwareUpdateConfiguration#monthly_occurrence}
        :param next_run: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#next_run AutomationSoftwareUpdateConfiguration#next_run}.
        :param next_run_offset_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#next_run_offset_minutes AutomationSoftwareUpdateConfiguration#next_run_offset_minutes}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#start_time AutomationSoftwareUpdateConfiguration#start_time}.
        :param start_time_offset_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#start_time_offset_minutes AutomationSoftwareUpdateConfiguration#start_time_offset_minutes}.
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#time_zone AutomationSoftwareUpdateConfiguration#time_zone}.
        '''
        if isinstance(monthly_occurrence, dict):
            monthly_occurrence = AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrence(**monthly_occurrence)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35f7f227ee314c8e22a680913c7be4eb0f0d3c3cd17ca6d6b0b14979ece5ff3a)
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument advanced_month_days", value=advanced_month_days, expected_type=type_hints["advanced_month_days"])
            check_type(argname="argument advanced_week_days", value=advanced_week_days, expected_type=type_hints["advanced_week_days"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument expiry_time", value=expiry_time, expected_type=type_hints["expiry_time"])
            check_type(argname="argument expiry_time_offset_minutes", value=expiry_time_offset_minutes, expected_type=type_hints["expiry_time_offset_minutes"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument monthly_occurrence", value=monthly_occurrence, expected_type=type_hints["monthly_occurrence"])
            check_type(argname="argument next_run", value=next_run, expected_type=type_hints["next_run"])
            check_type(argname="argument next_run_offset_minutes", value=next_run_offset_minutes, expected_type=type_hints["next_run_offset_minutes"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument start_time_offset_minutes", value=start_time_offset_minutes, expected_type=type_hints["start_time_offset_minutes"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frequency": frequency,
        }
        if advanced_month_days is not None:
            self._values["advanced_month_days"] = advanced_month_days
        if advanced_week_days is not None:
            self._values["advanced_week_days"] = advanced_week_days
        if description is not None:
            self._values["description"] = description
        if expiry_time is not None:
            self._values["expiry_time"] = expiry_time
        if expiry_time_offset_minutes is not None:
            self._values["expiry_time_offset_minutes"] = expiry_time_offset_minutes
        if interval is not None:
            self._values["interval"] = interval
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if monthly_occurrence is not None:
            self._values["monthly_occurrence"] = monthly_occurrence
        if next_run is not None:
            self._values["next_run"] = next_run
        if next_run_offset_minutes is not None:
            self._values["next_run_offset_minutes"] = next_run_offset_minutes
        if start_time is not None:
            self._values["start_time"] = start_time
        if start_time_offset_minutes is not None:
            self._values["start_time_offset_minutes"] = start_time_offset_minutes
        if time_zone is not None:
            self._values["time_zone"] = time_zone

    @builtins.property
    def frequency(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#frequency AutomationSoftwareUpdateConfiguration#frequency}.'''
        result = self._values.get("frequency")
        assert result is not None, "Required property 'frequency' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_month_days(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#advanced_month_days AutomationSoftwareUpdateConfiguration#advanced_month_days}.'''
        result = self._values.get("advanced_month_days")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def advanced_week_days(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#advanced_week_days AutomationSoftwareUpdateConfiguration#advanced_week_days}.'''
        result = self._values.get("advanced_week_days")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#description AutomationSoftwareUpdateConfiguration#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiry_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#expiry_time AutomationSoftwareUpdateConfiguration#expiry_time}.'''
        result = self._values.get("expiry_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiry_time_offset_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#expiry_time_offset_minutes AutomationSoftwareUpdateConfiguration#expiry_time_offset_minutes}.'''
        result = self._values.get("expiry_time_offset_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#interval AutomationSoftwareUpdateConfiguration#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#is_enabled AutomationSoftwareUpdateConfiguration#is_enabled}.'''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monthly_occurrence(
        self,
    ) -> typing.Optional["AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrence"]:
        '''monthly_occurrence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#monthly_occurrence AutomationSoftwareUpdateConfiguration#monthly_occurrence}
        '''
        result = self._values.get("monthly_occurrence")
        return typing.cast(typing.Optional["AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrence"], result)

    @builtins.property
    def next_run(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#next_run AutomationSoftwareUpdateConfiguration#next_run}.'''
        result = self._values.get("next_run")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_run_offset_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#next_run_offset_minutes AutomationSoftwareUpdateConfiguration#next_run_offset_minutes}.'''
        result = self._values.get("next_run_offset_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#start_time AutomationSoftwareUpdateConfiguration#start_time}.'''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time_offset_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#start_time_offset_minutes AutomationSoftwareUpdateConfiguration#start_time_offset_minutes}.'''
        result = self._values.get("start_time_offset_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#time_zone AutomationSoftwareUpdateConfiguration#time_zone}.'''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomationSoftwareUpdateConfigurationSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrence",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "occurrence": "occurrence"},
)
class AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrence:
    def __init__(self, *, day: builtins.str, occurrence: jsii.Number) -> None:
        '''
        :param day: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#day AutomationSoftwareUpdateConfiguration#day}.
        :param occurrence: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#occurrence AutomationSoftwareUpdateConfiguration#occurrence}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d2bbb27231d9b524d2d9b5f72fb0149de5e3315d86139ae1e6d901b61972e7)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument occurrence", value=occurrence, expected_type=type_hints["occurrence"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day": day,
            "occurrence": occurrence,
        }

    @builtins.property
    def day(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#day AutomationSoftwareUpdateConfiguration#day}.'''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def occurrence(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#occurrence AutomationSoftwareUpdateConfiguration#occurrence}.'''
        result = self._values.get("occurrence")
        assert result is not None, "Required property 'occurrence' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1ae6ff952a6f6e383bba064ae666d4789db1fb9bffc0901acb10f012f6b4ce1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="occurrenceInput")
    def occurrence_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "occurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "day"))

    @day.setter
    def day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b390a8fe1bb83e104e3c0793cb14b027ad608ab48d270401f173343776d78c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="occurrence")
    def occurrence(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "occurrence"))

    @occurrence.setter
    def occurrence(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0d8db927d2c03990dc8dbaba97319bd3a21cc26dd84776de93f6ca49d631ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "occurrence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrence]:
        return typing.cast(typing.Optional[AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__426f421f2ca074cfcbf6f8546cb48c324072c8377d8dce56b5217f7066d3b7ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AutomationSoftwareUpdateConfigurationScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3738c1e305b2c7312a399354720219b4fcd52b204555dddd4aa77d499dd72209)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMonthlyOccurrence")
    def put_monthly_occurrence(
        self,
        *,
        day: builtins.str,
        occurrence: jsii.Number,
    ) -> None:
        '''
        :param day: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#day AutomationSoftwareUpdateConfiguration#day}.
        :param occurrence: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#occurrence AutomationSoftwareUpdateConfiguration#occurrence}.
        '''
        value = AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrence(
            day=day, occurrence=occurrence
        )

        return typing.cast(None, jsii.invoke(self, "putMonthlyOccurrence", [value]))

    @jsii.member(jsii_name="resetAdvancedMonthDays")
    def reset_advanced_month_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedMonthDays", []))

    @jsii.member(jsii_name="resetAdvancedWeekDays")
    def reset_advanced_week_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedWeekDays", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExpiryTime")
    def reset_expiry_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiryTime", []))

    @jsii.member(jsii_name="resetExpiryTimeOffsetMinutes")
    def reset_expiry_time_offset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiryTimeOffsetMinutes", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetMonthlyOccurrence")
    def reset_monthly_occurrence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthlyOccurrence", []))

    @jsii.member(jsii_name="resetNextRun")
    def reset_next_run(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNextRun", []))

    @jsii.member(jsii_name="resetNextRunOffsetMinutes")
    def reset_next_run_offset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNextRunOffsetMinutes", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @jsii.member(jsii_name="resetStartTimeOffsetMinutes")
    def reset_start_time_offset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTimeOffsetMinutes", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

    @builtins.property
    @jsii.member(jsii_name="creationTime")
    def creation_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTime"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedTime")
    def last_modified_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifiedTime"))

    @builtins.property
    @jsii.member(jsii_name="monthlyOccurrence")
    def monthly_occurrence(
        self,
    ) -> AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrenceOutputReference:
        return typing.cast(AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrenceOutputReference, jsii.get(self, "monthlyOccurrence"))

    @builtins.property
    @jsii.member(jsii_name="advancedMonthDaysInput")
    def advanced_month_days_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "advancedMonthDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedWeekDaysInput")
    def advanced_week_days_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "advancedWeekDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="expiryTimeInput")
    def expiry_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expiryTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="expiryTimeOffsetMinutesInput")
    def expiry_time_offset_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expiryTimeOffsetMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="monthlyOccurrenceInput")
    def monthly_occurrence_input(
        self,
    ) -> typing.Optional[AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrence]:
        return typing.cast(typing.Optional[AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrence], jsii.get(self, "monthlyOccurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="nextRunInput")
    def next_run_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nextRunInput"))

    @builtins.property
    @jsii.member(jsii_name="nextRunOffsetMinutesInput")
    def next_run_offset_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nextRunOffsetMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeOffsetMinutesInput")
    def start_time_offset_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startTimeOffsetMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedMonthDays")
    def advanced_month_days(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "advancedMonthDays"))

    @advanced_month_days.setter
    def advanced_month_days(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c128065189e2bddfc5b81623cd6f71f621cfc6b87e85df5e60cd9d189445cfef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advancedMonthDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="advancedWeekDays")
    def advanced_week_days(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "advancedWeekDays"))

    @advanced_week_days.setter
    def advanced_week_days(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb9dbd83f57fbe55aa3ddb419981073d3cbfec9baf35fdf862846a1851e6a322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advancedWeekDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7863da8fe38065997f52c986a6e281f7303bba42b44a493418cbe47fbb67229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expiryTime")
    def expiry_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiryTime"))

    @expiry_time.setter
    def expiry_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b752c5947ec977c193c877f7fd4abab6d70bcf15f1cc3d35c4051ada2b05ad4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiryTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expiryTimeOffsetMinutes")
    def expiry_time_offset_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expiryTimeOffsetMinutes"))

    @expiry_time_offset_minutes.setter
    def expiry_time_offset_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0218b564c1b1b0a2ce7a30edacc7576080e6fc8a24325c9b8d9076fca79e2cf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiryTimeOffsetMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95ef5c22cae34cc37b6043400fc940f02bf6a1da53d041fb5257862a052f4447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74465b907f02019b9ed08980986ac037c6b9d6079d4c9212e30a5a0951498320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e60feb2c1a24a546fbd110f0d3ee3d871e6254fa633f34ea7c4850b80cebeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nextRun")
    def next_run(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextRun"))

    @next_run.setter
    def next_run(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a05229ea7275f8ca2d05478fa1e5aea1e757e03077d4e098ee92510f58d16d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextRun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nextRunOffsetMinutes")
    def next_run_offset_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nextRunOffsetMinutes"))

    @next_run_offset_minutes.setter
    def next_run_offset_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb7ec8392f063e9e1f82605ecd5910a512288a2da28fb296b614379d34713fe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextRunOffsetMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80cb695b4fdc605ac15bc0acfc9502789dafe869d57a51c3ff4029de1c5a664e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTimeOffsetMinutes")
    def start_time_offset_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startTimeOffsetMinutes"))

    @start_time_offset_minutes.setter
    def start_time_offset_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc877935a56f802257066275232bb8d31bfbd7d5083d12098725bf87032c2441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTimeOffsetMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d906cf50f3599af7e8fd9a094fdc6c955891b66bc7cdcf3fb7bab855707f3c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AutomationSoftwareUpdateConfigurationSchedule]:
        return typing.cast(typing.Optional[AutomationSoftwareUpdateConfigurationSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomationSoftwareUpdateConfigurationSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4ee2144e1c5ee76a1fa02a8726111d31be4f0b07d042d94fc3755a7671ab14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationTarget",
    jsii_struct_bases=[],
    name_mapping={"azure_query": "azureQuery", "non_azure_query": "nonAzureQuery"},
)
class AutomationSoftwareUpdateConfigurationTarget:
    def __init__(
        self,
        *,
        azure_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AutomationSoftwareUpdateConfigurationTargetAzureQuery", typing.Dict[builtins.str, typing.Any]]]]] = None,
        non_azure_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AutomationSoftwareUpdateConfigurationTargetNonAzureQuery", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param azure_query: azure_query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#azure_query AutomationSoftwareUpdateConfiguration#azure_query}
        :param non_azure_query: non_azure_query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#non_azure_query AutomationSoftwareUpdateConfiguration#non_azure_query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc80542d6c18cd79de5c93656d4a4bf0b1dfbeaa0f62fc84a4aab0204b16ada4)
            check_type(argname="argument azure_query", value=azure_query, expected_type=type_hints["azure_query"])
            check_type(argname="argument non_azure_query", value=non_azure_query, expected_type=type_hints["non_azure_query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if azure_query is not None:
            self._values["azure_query"] = azure_query
        if non_azure_query is not None:
            self._values["non_azure_query"] = non_azure_query

    @builtins.property
    def azure_query(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AutomationSoftwareUpdateConfigurationTargetAzureQuery"]]]:
        '''azure_query block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#azure_query AutomationSoftwareUpdateConfiguration#azure_query}
        '''
        result = self._values.get("azure_query")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AutomationSoftwareUpdateConfigurationTargetAzureQuery"]]], result)

    @builtins.property
    def non_azure_query(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AutomationSoftwareUpdateConfigurationTargetNonAzureQuery"]]]:
        '''non_azure_query block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#non_azure_query AutomationSoftwareUpdateConfiguration#non_azure_query}
        '''
        result = self._values.get("non_azure_query")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AutomationSoftwareUpdateConfigurationTargetNonAzureQuery"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomationSoftwareUpdateConfigurationTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationTargetAzureQuery",
    jsii_struct_bases=[],
    name_mapping={
        "locations": "locations",
        "scope": "scope",
        "tag_filter": "tagFilter",
        "tags": "tags",
    },
)
class AutomationSoftwareUpdateConfigurationTargetAzureQuery:
    def __init__(
        self,
        *,
        locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        scope: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_filter: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AutomationSoftwareUpdateConfigurationTargetAzureQueryTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param locations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#locations AutomationSoftwareUpdateConfiguration#locations}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#scope AutomationSoftwareUpdateConfiguration#scope}.
        :param tag_filter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#tag_filter AutomationSoftwareUpdateConfiguration#tag_filter}.
        :param tags: tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#tags AutomationSoftwareUpdateConfiguration#tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cf82c9297fc6d7d10df71fc8dbffc2721965d644e5e3fec0c96d0b2b959c4f6)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument tag_filter", value=tag_filter, expected_type=type_hints["tag_filter"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if locations is not None:
            self._values["locations"] = locations
        if scope is not None:
            self._values["scope"] = scope
        if tag_filter is not None:
            self._values["tag_filter"] = tag_filter
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#locations AutomationSoftwareUpdateConfiguration#locations}.'''
        result = self._values.get("locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def scope(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#scope AutomationSoftwareUpdateConfiguration#scope}.'''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_filter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#tag_filter AutomationSoftwareUpdateConfiguration#tag_filter}.'''
        result = self._values.get("tag_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AutomationSoftwareUpdateConfigurationTargetAzureQueryTags"]]]:
        '''tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#tags AutomationSoftwareUpdateConfiguration#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AutomationSoftwareUpdateConfigurationTargetAzureQueryTags"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomationSoftwareUpdateConfigurationTargetAzureQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomationSoftwareUpdateConfigurationTargetAzureQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationTargetAzureQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f556801ed5f839784d17faea666af0e3b004bd17fe5be13d47fff67bad7f5e8a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AutomationSoftwareUpdateConfigurationTargetAzureQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e1fec52cac6612dbd0370206899e52775ca59c97e6e5006d0aadfc66c09b4f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AutomationSoftwareUpdateConfigurationTargetAzureQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__516f366eadd49a1712db7c5609caaaf08db3227718457c869977cdc7593816da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f862724483681d0bfab45322662bcb6f3d432c16375e638e0fc5de8b53d4eb0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2d77dd48509b0f4ebacb8da981606c7e4cc30a0a9b888dfac42030f7a20011b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutomationSoftwareUpdateConfigurationTargetAzureQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutomationSoftwareUpdateConfigurationTargetAzureQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutomationSoftwareUpdateConfigurationTargetAzureQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c369e2f3e3791c573203ef7ca383b96bc9a37a071df024958bbdf1a4454e87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AutomationSoftwareUpdateConfigurationTargetAzureQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationTargetAzureQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a54b257b9c107c00143398a81e61725e0440305c848cd90cf2d8a8e49a6cd4e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTags")
    def put_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AutomationSoftwareUpdateConfigurationTargetAzureQueryTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c056e9d97e9a510ddefebafdd57f83556826f1b6809820aa234d202ad5f0cb18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTags", [value]))

    @jsii.member(jsii_name="resetLocations")
    def reset_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocations", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @jsii.member(jsii_name="resetTagFilter")
    def reset_tag_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagFilter", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "AutomationSoftwareUpdateConfigurationTargetAzureQueryTagsList":
        return typing.cast("AutomationSoftwareUpdateConfigurationTargetAzureQueryTagsList", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="locationsInput")
    def locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "locationsInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagFilterInput")
    def tag_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AutomationSoftwareUpdateConfigurationTargetAzureQueryTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AutomationSoftwareUpdateConfigurationTargetAzureQueryTags"]]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="locations")
    def locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "locations"))

    @locations.setter
    def locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9054f85136fc6773df10170d28dedc7e1913af81dd41e7a384e0b917ccdc3121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16239c1692a90ea72cb383dfe13d1e455d03200fc05b9eee351c215e40e65d3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagFilter")
    def tag_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagFilter"))

    @tag_filter.setter
    def tag_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d30455f423e030a044a8163d17af37d3bafa28852bac853627cc68093b5a115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomationSoftwareUpdateConfigurationTargetAzureQuery]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomationSoftwareUpdateConfigurationTargetAzureQuery]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomationSoftwareUpdateConfigurationTargetAzureQuery]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e8cf42967174d47f12a13e245af53f8e69296deff12279d6798b0ec49c111ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationTargetAzureQueryTags",
    jsii_struct_bases=[],
    name_mapping={"tag": "tag", "values": "values"},
)
class AutomationSoftwareUpdateConfigurationTargetAzureQueryTags:
    def __init__(
        self,
        *,
        tag: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#tag AutomationSoftwareUpdateConfiguration#tag}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#values AutomationSoftwareUpdateConfiguration#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9afb97001b6a447b68067bd4af18ca50b92d68bc122aa51d10eb700b8171509f)
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tag": tag,
            "values": values,
        }

    @builtins.property
    def tag(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#tag AutomationSoftwareUpdateConfiguration#tag}.'''
        result = self._values.get("tag")
        assert result is not None, "Required property 'tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#values AutomationSoftwareUpdateConfiguration#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomationSoftwareUpdateConfigurationTargetAzureQueryTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomationSoftwareUpdateConfigurationTargetAzureQueryTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationTargetAzureQueryTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3d255bd7d3c8f7fe0a72a2758c3126251436f750c738d1a2edc3990b9491cc0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AutomationSoftwareUpdateConfigurationTargetAzureQueryTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eadf1c0f665bc4290e23d099f82a428d0dbd655fe489170340b30f1ad6351a8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AutomationSoftwareUpdateConfigurationTargetAzureQueryTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da01cb3a30d82ed0d2316a475b95e174182ca7042128af01ed19372718115052)
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
            type_hints = typing.get_type_hints(_typecheckingstub__530fd250264d6355c3e43a117c27c00b06f828c540d50eec41516f3a7214a1b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__759faddc51db90757386ed8fec0240abb41329fa1626cea74561fb3131360170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutomationSoftwareUpdateConfigurationTargetAzureQueryTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutomationSoftwareUpdateConfigurationTargetAzureQueryTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutomationSoftwareUpdateConfigurationTargetAzureQueryTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47660798ea7db03a9a28aa2b0db47693ff8a0e581ab165403260fea999fdd2de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AutomationSoftwareUpdateConfigurationTargetAzureQueryTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationTargetAzureQueryTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__952e76aab118338f10cd5681c5daf07a296c4b0809e5964339501001228426ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d06c8ab6b2b66ad94174b84a74ec528bf3b84986e93676b9d72357191ca47f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8c74ef8e7d343582a424523ff24a1cab8329d6a8210a23319dd6feb57721954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomationSoftwareUpdateConfigurationTargetAzureQueryTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomationSoftwareUpdateConfigurationTargetAzureQueryTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomationSoftwareUpdateConfigurationTargetAzureQueryTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ad3cfa91eb6a809f999f8b63d0e9dc50bd4656895d321c772ce22ab27ba7e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationTargetNonAzureQuery",
    jsii_struct_bases=[],
    name_mapping={"function_alias": "functionAlias", "workspace_id": "workspaceId"},
)
class AutomationSoftwareUpdateConfigurationTargetNonAzureQuery:
    def __init__(
        self,
        *,
        function_alias: typing.Optional[builtins.str] = None,
        workspace_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param function_alias: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#function_alias AutomationSoftwareUpdateConfiguration#function_alias}.
        :param workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#workspace_id AutomationSoftwareUpdateConfiguration#workspace_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a812f427e52d15cc1658db5481a8d7ef866fb30f88eb232e9b55e423f41b3c)
            check_type(argname="argument function_alias", value=function_alias, expected_type=type_hints["function_alias"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if function_alias is not None:
            self._values["function_alias"] = function_alias
        if workspace_id is not None:
            self._values["workspace_id"] = workspace_id

    @builtins.property
    def function_alias(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#function_alias AutomationSoftwareUpdateConfiguration#function_alias}.'''
        result = self._values.get("function_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#workspace_id AutomationSoftwareUpdateConfiguration#workspace_id}.'''
        result = self._values.get("workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomationSoftwareUpdateConfigurationTargetNonAzureQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomationSoftwareUpdateConfigurationTargetNonAzureQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationTargetNonAzureQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__860443d8f38abe35e0700fcbd158a3252dc93ae9ea7ba951306bb7864ca53271)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AutomationSoftwareUpdateConfigurationTargetNonAzureQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69226edeb83b342c5f0c68232ae47f9021fa59ed6449534a9a7bcc72f96c223)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AutomationSoftwareUpdateConfigurationTargetNonAzureQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54697897ce050bb556ef2fb7ff4e440d35887ce4e7a6c1542a579172b6dc5c79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__521630375cf329371b4acb13ba4c7b4b17b85c7c5fc6d31abdbd37075d556c49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed70b5e98268931b38a58043ecb8b235be3c723e6f2c1dfbbc41216c85c2707c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutomationSoftwareUpdateConfigurationTargetNonAzureQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutomationSoftwareUpdateConfigurationTargetNonAzureQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutomationSoftwareUpdateConfigurationTargetNonAzureQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c95095642e9b4a11182b320f84a4c408babec1b211e9c05b2bad34a343bef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AutomationSoftwareUpdateConfigurationTargetNonAzureQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationTargetNonAzureQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c6164b85761b0adf841892781f2b80a2a5a3cc50e469cea2a261c022b9ed6b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFunctionAlias")
    def reset_function_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctionAlias", []))

    @jsii.member(jsii_name="resetWorkspaceId")
    def reset_workspace_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkspaceId", []))

    @builtins.property
    @jsii.member(jsii_name="functionAliasInput")
    def function_alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionAliasInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceIdInput")
    def workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="functionAlias")
    def function_alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionAlias"))

    @function_alias.setter
    def function_alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832a8e436c62c78749a2dbcaee92769a786c373fcc0a8dcc654773cd2079c369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionAlias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b73bb77c42693c5cc87cff78b3b3bfd3bed6cbf589d11f1a8ba892ef51f70b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomationSoftwareUpdateConfigurationTargetNonAzureQuery]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomationSoftwareUpdateConfigurationTargetNonAzureQuery]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomationSoftwareUpdateConfigurationTargetNonAzureQuery]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10313f614952d74b310d40107b3c3814b34dc82880d534624f660be1801105ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AutomationSoftwareUpdateConfigurationTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73c75a14d0f52968da25d43e557ccd040354e6cc52d494fd584174849eca4d15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAzureQuery")
    def put_azure_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AutomationSoftwareUpdateConfigurationTargetAzureQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b244acf7faa35feb6858d148e8093db66a31be30747e6ffb141193da792723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAzureQuery", [value]))

    @jsii.member(jsii_name="putNonAzureQuery")
    def put_non_azure_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AutomationSoftwareUpdateConfigurationTargetNonAzureQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f75d4b941c82e2056f060b0b30d9752ffa2cb8164f419a6b8346cdd0b49601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNonAzureQuery", [value]))

    @jsii.member(jsii_name="resetAzureQuery")
    def reset_azure_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureQuery", []))

    @jsii.member(jsii_name="resetNonAzureQuery")
    def reset_non_azure_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNonAzureQuery", []))

    @builtins.property
    @jsii.member(jsii_name="azureQuery")
    def azure_query(self) -> AutomationSoftwareUpdateConfigurationTargetAzureQueryList:
        return typing.cast(AutomationSoftwareUpdateConfigurationTargetAzureQueryList, jsii.get(self, "azureQuery"))

    @builtins.property
    @jsii.member(jsii_name="nonAzureQuery")
    def non_azure_query(
        self,
    ) -> AutomationSoftwareUpdateConfigurationTargetNonAzureQueryList:
        return typing.cast(AutomationSoftwareUpdateConfigurationTargetNonAzureQueryList, jsii.get(self, "nonAzureQuery"))

    @builtins.property
    @jsii.member(jsii_name="azureQueryInput")
    def azure_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutomationSoftwareUpdateConfigurationTargetAzureQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutomationSoftwareUpdateConfigurationTargetAzureQuery]]], jsii.get(self, "azureQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="nonAzureQueryInput")
    def non_azure_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutomationSoftwareUpdateConfigurationTargetNonAzureQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutomationSoftwareUpdateConfigurationTargetNonAzureQuery]]], jsii.get(self, "nonAzureQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AutomationSoftwareUpdateConfigurationTarget]:
        return typing.cast(typing.Optional[AutomationSoftwareUpdateConfigurationTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomationSoftwareUpdateConfigurationTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__139f8b6b7ee14e44b87b8754bd9c327b89041af1b303d2b6cb961a1eab579e4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class AutomationSoftwareUpdateConfigurationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#create AutomationSoftwareUpdateConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#delete AutomationSoftwareUpdateConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#read AutomationSoftwareUpdateConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#update AutomationSoftwareUpdateConfiguration#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3422cf5bc425dfe77ff239b045d364f822caedc01cb4c29dec8b149df65bdc)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#create AutomationSoftwareUpdateConfiguration#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#delete AutomationSoftwareUpdateConfiguration#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#read AutomationSoftwareUpdateConfiguration#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#update AutomationSoftwareUpdateConfiguration#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomationSoftwareUpdateConfigurationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomationSoftwareUpdateConfigurationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e7fd081d772b3494b47619fa91e69fd450c5ca7c5287338d09919333c999633)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7255b060d068739cd8c559b17fd13f5aaf680e1495099e1439ab3d93c65944c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e918baa681b22e90626656dbefb9194d6fdc440c2384e568e5ae4f6e17fd865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__756a73c5064ec2d8a63b85878f805cdf49a897753f38f3f2fe3993b603b75245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a51e7e71f887c5e692a0a343dffe54e5d1bacc471805e7bfd81a5e0ebcdf893)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomationSoftwareUpdateConfigurationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomationSoftwareUpdateConfigurationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomationSoftwareUpdateConfigurationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce83f6f1f136ac09eb0301ccb39d5d8fb35bcc18ab017f56bcfccb7190b5896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationWindows",
    jsii_struct_bases=[],
    name_mapping={
        "classifications_included": "classificationsIncluded",
        "excluded_knowledge_base_numbers": "excludedKnowledgeBaseNumbers",
        "included_knowledge_base_numbers": "includedKnowledgeBaseNumbers",
        "reboot": "reboot",
    },
)
class AutomationSoftwareUpdateConfigurationWindows:
    def __init__(
        self,
        *,
        classifications_included: typing.Sequence[builtins.str],
        excluded_knowledge_base_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_knowledge_base_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
        reboot: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param classifications_included: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#classifications_included AutomationSoftwareUpdateConfiguration#classifications_included}.
        :param excluded_knowledge_base_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#excluded_knowledge_base_numbers AutomationSoftwareUpdateConfiguration#excluded_knowledge_base_numbers}.
        :param included_knowledge_base_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#included_knowledge_base_numbers AutomationSoftwareUpdateConfiguration#included_knowledge_base_numbers}.
        :param reboot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#reboot AutomationSoftwareUpdateConfiguration#reboot}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__521f4328b66b0e0b6af623a41a9b9a72b5d67a60343035464e316b0630d4a6ad)
            check_type(argname="argument classifications_included", value=classifications_included, expected_type=type_hints["classifications_included"])
            check_type(argname="argument excluded_knowledge_base_numbers", value=excluded_knowledge_base_numbers, expected_type=type_hints["excluded_knowledge_base_numbers"])
            check_type(argname="argument included_knowledge_base_numbers", value=included_knowledge_base_numbers, expected_type=type_hints["included_knowledge_base_numbers"])
            check_type(argname="argument reboot", value=reboot, expected_type=type_hints["reboot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "classifications_included": classifications_included,
        }
        if excluded_knowledge_base_numbers is not None:
            self._values["excluded_knowledge_base_numbers"] = excluded_knowledge_base_numbers
        if included_knowledge_base_numbers is not None:
            self._values["included_knowledge_base_numbers"] = included_knowledge_base_numbers
        if reboot is not None:
            self._values["reboot"] = reboot

    @builtins.property
    def classifications_included(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#classifications_included AutomationSoftwareUpdateConfiguration#classifications_included}.'''
        result = self._values.get("classifications_included")
        assert result is not None, "Required property 'classifications_included' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def excluded_knowledge_base_numbers(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#excluded_knowledge_base_numbers AutomationSoftwareUpdateConfiguration#excluded_knowledge_base_numbers}.'''
        result = self._values.get("excluded_knowledge_base_numbers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_knowledge_base_numbers(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#included_knowledge_base_numbers AutomationSoftwareUpdateConfiguration#included_knowledge_base_numbers}.'''
        result = self._values.get("included_knowledge_base_numbers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def reboot(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/automation_software_update_configuration#reboot AutomationSoftwareUpdateConfiguration#reboot}.'''
        result = self._values.get("reboot")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomationSoftwareUpdateConfigurationWindows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomationSoftwareUpdateConfigurationWindowsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.automationSoftwareUpdateConfiguration.AutomationSoftwareUpdateConfigurationWindowsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ccdb4351ba36cffe67d6ace7c170ea891266197b3eca6aa1d76a3f226ac71cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludedKnowledgeBaseNumbers")
    def reset_excluded_knowledge_base_numbers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedKnowledgeBaseNumbers", []))

    @jsii.member(jsii_name="resetIncludedKnowledgeBaseNumbers")
    def reset_included_knowledge_base_numbers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedKnowledgeBaseNumbers", []))

    @jsii.member(jsii_name="resetReboot")
    def reset_reboot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReboot", []))

    @builtins.property
    @jsii.member(jsii_name="classificationsIncludedInput")
    def classifications_included_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "classificationsIncludedInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedKnowledgeBaseNumbersInput")
    def excluded_knowledge_base_numbers_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedKnowledgeBaseNumbersInput"))

    @builtins.property
    @jsii.member(jsii_name="includedKnowledgeBaseNumbersInput")
    def included_knowledge_base_numbers_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedKnowledgeBaseNumbersInput"))

    @builtins.property
    @jsii.member(jsii_name="rebootInput")
    def reboot_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rebootInput"))

    @builtins.property
    @jsii.member(jsii_name="classificationsIncluded")
    def classifications_included(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "classificationsIncluded"))

    @classifications_included.setter
    def classifications_included(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b268e6600c529f9d76793326884513c2bfbcbf076756883ecd1a93e3bc2d45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classificationsIncluded", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedKnowledgeBaseNumbers")
    def excluded_knowledge_base_numbers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedKnowledgeBaseNumbers"))

    @excluded_knowledge_base_numbers.setter
    def excluded_knowledge_base_numbers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__488117d3a3a63dae23e271b040fd0e21409f517b59a980f7ebc6fdec9392ce40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedKnowledgeBaseNumbers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedKnowledgeBaseNumbers")
    def included_knowledge_base_numbers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedKnowledgeBaseNumbers"))

    @included_knowledge_base_numbers.setter
    def included_knowledge_base_numbers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3e2b60f77c0b7b81f8d83481ec0b648757f7257c54cc1f1d1821f923ee67fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedKnowledgeBaseNumbers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reboot")
    def reboot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reboot"))

    @reboot.setter
    def reboot(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09e0a9d2816d6dca8d14952bac3208244b27538ae6c92a16591dbe6eb31bfbb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reboot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AutomationSoftwareUpdateConfigurationWindows]:
        return typing.cast(typing.Optional[AutomationSoftwareUpdateConfigurationWindows], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomationSoftwareUpdateConfigurationWindows],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2af388cab5cd6a7830b488c8512899039908f1a493c72de81d20c7423421184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AutomationSoftwareUpdateConfiguration",
    "AutomationSoftwareUpdateConfigurationConfig",
    "AutomationSoftwareUpdateConfigurationLinux",
    "AutomationSoftwareUpdateConfigurationLinuxOutputReference",
    "AutomationSoftwareUpdateConfigurationPostTask",
    "AutomationSoftwareUpdateConfigurationPostTaskOutputReference",
    "AutomationSoftwareUpdateConfigurationPreTask",
    "AutomationSoftwareUpdateConfigurationPreTaskOutputReference",
    "AutomationSoftwareUpdateConfigurationSchedule",
    "AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrence",
    "AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrenceOutputReference",
    "AutomationSoftwareUpdateConfigurationScheduleOutputReference",
    "AutomationSoftwareUpdateConfigurationTarget",
    "AutomationSoftwareUpdateConfigurationTargetAzureQuery",
    "AutomationSoftwareUpdateConfigurationTargetAzureQueryList",
    "AutomationSoftwareUpdateConfigurationTargetAzureQueryOutputReference",
    "AutomationSoftwareUpdateConfigurationTargetAzureQueryTags",
    "AutomationSoftwareUpdateConfigurationTargetAzureQueryTagsList",
    "AutomationSoftwareUpdateConfigurationTargetAzureQueryTagsOutputReference",
    "AutomationSoftwareUpdateConfigurationTargetNonAzureQuery",
    "AutomationSoftwareUpdateConfigurationTargetNonAzureQueryList",
    "AutomationSoftwareUpdateConfigurationTargetNonAzureQueryOutputReference",
    "AutomationSoftwareUpdateConfigurationTargetOutputReference",
    "AutomationSoftwareUpdateConfigurationTimeouts",
    "AutomationSoftwareUpdateConfigurationTimeoutsOutputReference",
    "AutomationSoftwareUpdateConfigurationWindows",
    "AutomationSoftwareUpdateConfigurationWindowsOutputReference",
]

publication.publish()

def _typecheckingstub__5ebf73eff841fc40a68d40998a7cc9b471767b03e3c3f92df120b5ef821f48be(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    automation_account_id: builtins.str,
    name: builtins.str,
    schedule: typing.Union[AutomationSoftwareUpdateConfigurationSchedule, typing.Dict[builtins.str, typing.Any]],
    duration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    linux: typing.Optional[typing.Union[AutomationSoftwareUpdateConfigurationLinux, typing.Dict[builtins.str, typing.Any]]] = None,
    non_azure_computer_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    post_task: typing.Optional[typing.Union[AutomationSoftwareUpdateConfigurationPostTask, typing.Dict[builtins.str, typing.Any]]] = None,
    pre_task: typing.Optional[typing.Union[AutomationSoftwareUpdateConfigurationPreTask, typing.Dict[builtins.str, typing.Any]]] = None,
    target: typing.Optional[typing.Union[AutomationSoftwareUpdateConfigurationTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[AutomationSoftwareUpdateConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    windows: typing.Optional[typing.Union[AutomationSoftwareUpdateConfigurationWindows, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5f22c0671220f860a6cbf2eddd65910852ace84f08defc7ddcc69d3a3607d104(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7772c2854853e6d780827e4a6190839170b3ed096169461da351d0de0f1dd67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a6b87b80ca57bc194224fafd1a741fc9dc5ba892fbe99d0084d0756f717d8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06010833339ff60218c55a078a9130e44485cb604539988472b5e597323f6c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bffae33b6d1e76e7e64dd8a5eaa4b0af8b2d8bea2a783472f1c062f7a47db925(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b242e1936b469a6a6d4a3414c58855b703deb187ae173769c87e0f842e2e55e2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ece8ebc04fa7934c0a6108c3cc525b37d5b75e253505f4352fd7cef9b1e3236(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282d37b958d5c9973367d2c1d5d4ec7975d6eb7400fb8bf4efe9d33ba3ae997b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    automation_account_id: builtins.str,
    name: builtins.str,
    schedule: typing.Union[AutomationSoftwareUpdateConfigurationSchedule, typing.Dict[builtins.str, typing.Any]],
    duration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    linux: typing.Optional[typing.Union[AutomationSoftwareUpdateConfigurationLinux, typing.Dict[builtins.str, typing.Any]]] = None,
    non_azure_computer_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    post_task: typing.Optional[typing.Union[AutomationSoftwareUpdateConfigurationPostTask, typing.Dict[builtins.str, typing.Any]]] = None,
    pre_task: typing.Optional[typing.Union[AutomationSoftwareUpdateConfigurationPreTask, typing.Dict[builtins.str, typing.Any]]] = None,
    target: typing.Optional[typing.Union[AutomationSoftwareUpdateConfigurationTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[AutomationSoftwareUpdateConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    windows: typing.Optional[typing.Union[AutomationSoftwareUpdateConfigurationWindows, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32df5f2508dcfc6496351c348730bb23ac11565a8b52806ce6417597e13f258a(
    *,
    classifications_included: typing.Sequence[builtins.str],
    excluded_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    reboot: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10505503bf9e0718247aa728bece41fd7695dcb42e91c8eb3c56d868a31195d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc17f93f99220842aa4f3f5d79b6dae62589044526ce4cbb7fe9d6d6bb08a38(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfce571bb2a870d6a3215d2c7c6b36f15a89686a4a4e9575f6a69a4f9d187f9b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa724957bf7096a78fb6a6a44bcf47355e7fade8f54e913d3bc7225dbe9599b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc95d1bdf9374857179c5f79b82e30e8b0c9ffa7c0f0f545a402ed865cfad945(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567f1b4bb711853758f95622f2de8449c3567d0ba5660028db81055c51c97a0d(
    value: typing.Optional[AutomationSoftwareUpdateConfigurationLinux],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e5f6d37ffcff754ab84e18d7bd056e5a17f7c8d31d7613b9abd089c6a1e22f(
    *,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe901174a7ec47277b4552243500d08e5ad4d60cad33f41c2033c706054da0e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4170dfa10d63113db660b803205f0a10786f220ebe4df893b1e0cfebdf24234c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27379006bb5887006fc1b985e3fd12327c7820ae209aecd85ef049158461886e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c29b4322efb7bebd0932a6b20c033d40c2639cf98cabeafb32e49361f741615d(
    value: typing.Optional[AutomationSoftwareUpdateConfigurationPostTask],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0da824885269830e599198325601384abee7854b567426167f187da3a9afafa(
    *,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba50d8b58791cb24e2e151cf6e57a84e23c15601485915b70682f24f86b7ce46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc35683f993bf9468c81954d762c3ad18a57d41ab237c50f283f0eaaf102f8c4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3afc6f9710d4d5bb4e391609663b62bb1f691e52bf87132c17a41f9fa58b5b81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e54bbaaee91742312632960b29bf14f50f0b3ba2b7160f6660f80c30a4d7c5(
    value: typing.Optional[AutomationSoftwareUpdateConfigurationPreTask],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f7f227ee314c8e22a680913c7be4eb0f0d3c3cd17ca6d6b0b14979ece5ff3a(
    *,
    frequency: builtins.str,
    advanced_month_days: typing.Optional[typing.Sequence[jsii.Number]] = None,
    advanced_week_days: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    expiry_time: typing.Optional[builtins.str] = None,
    expiry_time_offset_minutes: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monthly_occurrence: typing.Optional[typing.Union[AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrence, typing.Dict[builtins.str, typing.Any]]] = None,
    next_run: typing.Optional[builtins.str] = None,
    next_run_offset_minutes: typing.Optional[jsii.Number] = None,
    start_time: typing.Optional[builtins.str] = None,
    start_time_offset_minutes: typing.Optional[jsii.Number] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d2bbb27231d9b524d2d9b5f72fb0149de5e3315d86139ae1e6d901b61972e7(
    *,
    day: builtins.str,
    occurrence: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ae6ff952a6f6e383bba064ae666d4789db1fb9bffc0901acb10f012f6b4ce1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b390a8fe1bb83e104e3c0793cb14b027ad608ab48d270401f173343776d78c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0d8db927d2c03990dc8dbaba97319bd3a21cc26dd84776de93f6ca49d631ec5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426f421f2ca074cfcbf6f8546cb48c324072c8377d8dce56b5217f7066d3b7ce(
    value: typing.Optional[AutomationSoftwareUpdateConfigurationScheduleMonthlyOccurrence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3738c1e305b2c7312a399354720219b4fcd52b204555dddd4aa77d499dd72209(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c128065189e2bddfc5b81623cd6f71f621cfc6b87e85df5e60cd9d189445cfef(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9dbd83f57fbe55aa3ddb419981073d3cbfec9baf35fdf862846a1851e6a322(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7863da8fe38065997f52c986a6e281f7303bba42b44a493418cbe47fbb67229(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b752c5947ec977c193c877f7fd4abab6d70bcf15f1cc3d35c4051ada2b05ad4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0218b564c1b1b0a2ce7a30edacc7576080e6fc8a24325c9b8d9076fca79e2cf4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ef5c22cae34cc37b6043400fc940f02bf6a1da53d041fb5257862a052f4447(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74465b907f02019b9ed08980986ac037c6b9d6079d4c9212e30a5a0951498320(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e60feb2c1a24a546fbd110f0d3ee3d871e6254fa633f34ea7c4850b80cebeb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a05229ea7275f8ca2d05478fa1e5aea1e757e03077d4e098ee92510f58d16d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb7ec8392f063e9e1f82605ecd5910a512288a2da28fb296b614379d34713fe8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80cb695b4fdc605ac15bc0acfc9502789dafe869d57a51c3ff4029de1c5a664e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc877935a56f802257066275232bb8d31bfbd7d5083d12098725bf87032c2441(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d906cf50f3599af7e8fd9a094fdc6c955891b66bc7cdcf3fb7bab855707f3c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4ee2144e1c5ee76a1fa02a8726111d31be4f0b07d042d94fc3755a7671ab14(
    value: typing.Optional[AutomationSoftwareUpdateConfigurationSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc80542d6c18cd79de5c93656d4a4bf0b1dfbeaa0f62fc84a4aab0204b16ada4(
    *,
    azure_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AutomationSoftwareUpdateConfigurationTargetAzureQuery, typing.Dict[builtins.str, typing.Any]]]]] = None,
    non_azure_query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AutomationSoftwareUpdateConfigurationTargetNonAzureQuery, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cf82c9297fc6d7d10df71fc8dbffc2721965d644e5e3fec0c96d0b2b959c4f6(
    *,
    locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    scope: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_filter: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AutomationSoftwareUpdateConfigurationTargetAzureQueryTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f556801ed5f839784d17faea666af0e3b004bd17fe5be13d47fff67bad7f5e8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e1fec52cac6612dbd0370206899e52775ca59c97e6e5006d0aadfc66c09b4f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__516f366eadd49a1712db7c5609caaaf08db3227718457c869977cdc7593816da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f862724483681d0bfab45322662bcb6f3d432c16375e638e0fc5de8b53d4eb0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d77dd48509b0f4ebacb8da981606c7e4cc30a0a9b888dfac42030f7a20011b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c369e2f3e3791c573203ef7ca383b96bc9a37a071df024958bbdf1a4454e87(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutomationSoftwareUpdateConfigurationTargetAzureQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54b257b9c107c00143398a81e61725e0440305c848cd90cf2d8a8e49a6cd4e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c056e9d97e9a510ddefebafdd57f83556826f1b6809820aa234d202ad5f0cb18(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AutomationSoftwareUpdateConfigurationTargetAzureQueryTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9054f85136fc6773df10170d28dedc7e1913af81dd41e7a384e0b917ccdc3121(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16239c1692a90ea72cb383dfe13d1e455d03200fc05b9eee351c215e40e65d3a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d30455f423e030a044a8163d17af37d3bafa28852bac853627cc68093b5a115(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e8cf42967174d47f12a13e245af53f8e69296deff12279d6798b0ec49c111ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomationSoftwareUpdateConfigurationTargetAzureQuery]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9afb97001b6a447b68067bd4af18ca50b92d68bc122aa51d10eb700b8171509f(
    *,
    tag: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d255bd7d3c8f7fe0a72a2758c3126251436f750c738d1a2edc3990b9491cc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eadf1c0f665bc4290e23d099f82a428d0dbd655fe489170340b30f1ad6351a8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da01cb3a30d82ed0d2316a475b95e174182ca7042128af01ed19372718115052(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530fd250264d6355c3e43a117c27c00b06f828c540d50eec41516f3a7214a1b4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759faddc51db90757386ed8fec0240abb41329fa1626cea74561fb3131360170(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47660798ea7db03a9a28aa2b0db47693ff8a0e581ab165403260fea999fdd2de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutomationSoftwareUpdateConfigurationTargetAzureQueryTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__952e76aab118338f10cd5681c5daf07a296c4b0809e5964339501001228426ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d06c8ab6b2b66ad94174b84a74ec528bf3b84986e93676b9d72357191ca47f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c74ef8e7d343582a424523ff24a1cab8329d6a8210a23319dd6feb57721954(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ad3cfa91eb6a809f999f8b63d0e9dc50bd4656895d321c772ce22ab27ba7e9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomationSoftwareUpdateConfigurationTargetAzureQueryTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a812f427e52d15cc1658db5481a8d7ef866fb30f88eb232e9b55e423f41b3c(
    *,
    function_alias: typing.Optional[builtins.str] = None,
    workspace_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860443d8f38abe35e0700fcbd158a3252dc93ae9ea7ba951306bb7864ca53271(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69226edeb83b342c5f0c68232ae47f9021fa59ed6449534a9a7bcc72f96c223(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54697897ce050bb556ef2fb7ff4e440d35887ce4e7a6c1542a579172b6dc5c79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__521630375cf329371b4acb13ba4c7b4b17b85c7c5fc6d31abdbd37075d556c49(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed70b5e98268931b38a58043ecb8b235be3c723e6f2c1dfbbc41216c85c2707c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c95095642e9b4a11182b320f84a4c408babec1b211e9c05b2bad34a343bef2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutomationSoftwareUpdateConfigurationTargetNonAzureQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6164b85761b0adf841892781f2b80a2a5a3cc50e469cea2a261c022b9ed6b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832a8e436c62c78749a2dbcaee92769a786c373fcc0a8dcc654773cd2079c369(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b73bb77c42693c5cc87cff78b3b3bfd3bed6cbf589d11f1a8ba892ef51f70b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10313f614952d74b310d40107b3c3814b34dc82880d534624f660be1801105ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomationSoftwareUpdateConfigurationTargetNonAzureQuery]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c75a14d0f52968da25d43e557ccd040354e6cc52d494fd584174849eca4d15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b244acf7faa35feb6858d148e8093db66a31be30747e6ffb141193da792723(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AutomationSoftwareUpdateConfigurationTargetAzureQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f75d4b941c82e2056f060b0b30d9752ffa2cb8164f419a6b8346cdd0b49601(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AutomationSoftwareUpdateConfigurationTargetNonAzureQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139f8b6b7ee14e44b87b8754bd9c327b89041af1b303d2b6cb961a1eab579e4e(
    value: typing.Optional[AutomationSoftwareUpdateConfigurationTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3422cf5bc425dfe77ff239b045d364f822caedc01cb4c29dec8b149df65bdc(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7fd081d772b3494b47619fa91e69fd450c5ca7c5287338d09919333c999633(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7255b060d068739cd8c559b17fd13f5aaf680e1495099e1439ab3d93c65944c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e918baa681b22e90626656dbefb9194d6fdc440c2384e568e5ae4f6e17fd865(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__756a73c5064ec2d8a63b85878f805cdf49a897753f38f3f2fe3993b603b75245(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a51e7e71f887c5e692a0a343dffe54e5d1bacc471805e7bfd81a5e0ebcdf893(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce83f6f1f136ac09eb0301ccb39d5d8fb35bcc18ab017f56bcfccb7190b5896(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AutomationSoftwareUpdateConfigurationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__521f4328b66b0e0b6af623a41a9b9a72b5d67a60343035464e316b0630d4a6ad(
    *,
    classifications_included: typing.Sequence[builtins.str],
    excluded_knowledge_base_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_knowledge_base_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
    reboot: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ccdb4351ba36cffe67d6ace7c170ea891266197b3eca6aa1d76a3f226ac71cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b268e6600c529f9d76793326884513c2bfbcbf076756883ecd1a93e3bc2d45(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488117d3a3a63dae23e271b040fd0e21409f517b59a980f7ebc6fdec9392ce40(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3e2b60f77c0b7b81f8d83481ec0b648757f7257c54cc1f1d1821f923ee67fb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e0a9d2816d6dca8d14952bac3208244b27538ae6c92a16591dbe6eb31bfbb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2af388cab5cd6a7830b488c8512899039908f1a493c72de81d20c7423421184(
    value: typing.Optional[AutomationSoftwareUpdateConfigurationWindows],
) -> None:
    """Type checking stubs"""
    pass

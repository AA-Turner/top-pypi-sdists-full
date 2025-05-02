r'''
# `aws_codedeploy_deployment_group`

Refer to the Terraform Registry for docs: [`aws_codedeploy_deployment_group`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group).
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


class CodedeployDeploymentGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroup",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group aws_codedeploy_deployment_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        app_name: builtins.str,
        deployment_group_name: builtins.str,
        service_role_arn: builtins.str,
        alarm_configuration: typing.Optional[typing.Union["CodedeployDeploymentGroupAlarmConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_rollback_configuration: typing.Optional[typing.Union["CodedeployDeploymentGroupAutoRollbackConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        autoscaling_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        blue_green_deployment_config: typing.Optional[typing.Union["CodedeployDeploymentGroupBlueGreenDeploymentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_config_name: typing.Optional[builtins.str] = None,
        deployment_style: typing.Optional[typing.Union["CodedeployDeploymentGroupDeploymentStyle", typing.Dict[builtins.str, typing.Any]]] = None,
        ec2_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupEc2TagFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ec2_tag_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupEc2TagSet", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ecs_service: typing.Optional[typing.Union["CodedeployDeploymentGroupEcsService", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancer_info: typing.Optional[typing.Union["CodedeployDeploymentGroupLoadBalancerInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        on_premises_instance_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupOnPremisesInstanceTagFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        outdated_instances_strategy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_hook_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trigger_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupTriggerConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group aws_codedeploy_deployment_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param app_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#app_name CodedeployDeploymentGroup#app_name}.
        :param deployment_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_group_name CodedeployDeploymentGroup#deployment_group_name}.
        :param service_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#service_role_arn CodedeployDeploymentGroup#service_role_arn}.
        :param alarm_configuration: alarm_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#alarm_configuration CodedeployDeploymentGroup#alarm_configuration}
        :param auto_rollback_configuration: auto_rollback_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#auto_rollback_configuration CodedeployDeploymentGroup#auto_rollback_configuration}
        :param autoscaling_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#autoscaling_groups CodedeployDeploymentGroup#autoscaling_groups}.
        :param blue_green_deployment_config: blue_green_deployment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#blue_green_deployment_config CodedeployDeploymentGroup#blue_green_deployment_config}
        :param deployment_config_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_config_name CodedeployDeploymentGroup#deployment_config_name}.
        :param deployment_style: deployment_style block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_style CodedeployDeploymentGroup#deployment_style}
        :param ec2_tag_filter: ec2_tag_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#ec2_tag_filter CodedeployDeploymentGroup#ec2_tag_filter}
        :param ec2_tag_set: ec2_tag_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#ec2_tag_set CodedeployDeploymentGroup#ec2_tag_set}
        :param ecs_service: ecs_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#ecs_service CodedeployDeploymentGroup#ecs_service}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#id CodedeployDeploymentGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancer_info: load_balancer_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#load_balancer_info CodedeployDeploymentGroup#load_balancer_info}
        :param on_premises_instance_tag_filter: on_premises_instance_tag_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#on_premises_instance_tag_filter CodedeployDeploymentGroup#on_premises_instance_tag_filter}
        :param outdated_instances_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#outdated_instances_strategy CodedeployDeploymentGroup#outdated_instances_strategy}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#tags CodedeployDeploymentGroup#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#tags_all CodedeployDeploymentGroup#tags_all}.
        :param termination_hook_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#termination_hook_enabled CodedeployDeploymentGroup#termination_hook_enabled}.
        :param trigger_configuration: trigger_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#trigger_configuration CodedeployDeploymentGroup#trigger_configuration}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4966d5ccbabdbcbbc2521d95655c311099840b2bd9de28b051f7a7e76584506)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CodedeployDeploymentGroupConfig(
            app_name=app_name,
            deployment_group_name=deployment_group_name,
            service_role_arn=service_role_arn,
            alarm_configuration=alarm_configuration,
            auto_rollback_configuration=auto_rollback_configuration,
            autoscaling_groups=autoscaling_groups,
            blue_green_deployment_config=blue_green_deployment_config,
            deployment_config_name=deployment_config_name,
            deployment_style=deployment_style,
            ec2_tag_filter=ec2_tag_filter,
            ec2_tag_set=ec2_tag_set,
            ecs_service=ecs_service,
            id=id,
            load_balancer_info=load_balancer_info,
            on_premises_instance_tag_filter=on_premises_instance_tag_filter,
            outdated_instances_strategy=outdated_instances_strategy,
            tags=tags,
            tags_all=tags_all,
            termination_hook_enabled=termination_hook_enabled,
            trigger_configuration=trigger_configuration,
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
        '''Generates CDKTF code for importing a CodedeployDeploymentGroup resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CodedeployDeploymentGroup to import.
        :param import_from_id: The id of the existing CodedeployDeploymentGroup that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CodedeployDeploymentGroup to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00f2f4f75d186365a586bcca5b342c8961b1e29e1959f84c162f460e52256a02)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAlarmConfiguration")
    def put_alarm_configuration(
        self,
        *,
        alarms: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore_poll_alarm_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param alarms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#alarms CodedeployDeploymentGroup#alarms}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#enabled CodedeployDeploymentGroup#enabled}.
        :param ignore_poll_alarm_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#ignore_poll_alarm_failure CodedeployDeploymentGroup#ignore_poll_alarm_failure}.
        '''
        value = CodedeployDeploymentGroupAlarmConfiguration(
            alarms=alarms,
            enabled=enabled,
            ignore_poll_alarm_failure=ignore_poll_alarm_failure,
        )

        return typing.cast(None, jsii.invoke(self, "putAlarmConfiguration", [value]))

    @jsii.member(jsii_name="putAutoRollbackConfiguration")
    def put_auto_rollback_configuration(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        events: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#enabled CodedeployDeploymentGroup#enabled}.
        :param events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#events CodedeployDeploymentGroup#events}.
        '''
        value = CodedeployDeploymentGroupAutoRollbackConfiguration(
            enabled=enabled, events=events
        )

        return typing.cast(None, jsii.invoke(self, "putAutoRollbackConfiguration", [value]))

    @jsii.member(jsii_name="putBlueGreenDeploymentConfig")
    def put_blue_green_deployment_config(
        self,
        *,
        deployment_ready_option: typing.Optional[typing.Union["CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption", typing.Dict[builtins.str, typing.Any]]] = None,
        green_fleet_provisioning_option: typing.Optional[typing.Union["CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption", typing.Dict[builtins.str, typing.Any]]] = None,
        terminate_blue_instances_on_deployment_success: typing.Optional[typing.Union["CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param deployment_ready_option: deployment_ready_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_ready_option CodedeployDeploymentGroup#deployment_ready_option}
        :param green_fleet_provisioning_option: green_fleet_provisioning_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#green_fleet_provisioning_option CodedeployDeploymentGroup#green_fleet_provisioning_option}
        :param terminate_blue_instances_on_deployment_success: terminate_blue_instances_on_deployment_success block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#terminate_blue_instances_on_deployment_success CodedeployDeploymentGroup#terminate_blue_instances_on_deployment_success}
        '''
        value = CodedeployDeploymentGroupBlueGreenDeploymentConfig(
            deployment_ready_option=deployment_ready_option,
            green_fleet_provisioning_option=green_fleet_provisioning_option,
            terminate_blue_instances_on_deployment_success=terminate_blue_instances_on_deployment_success,
        )

        return typing.cast(None, jsii.invoke(self, "putBlueGreenDeploymentConfig", [value]))

    @jsii.member(jsii_name="putDeploymentStyle")
    def put_deployment_style(
        self,
        *,
        deployment_option: typing.Optional[builtins.str] = None,
        deployment_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deployment_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_option CodedeployDeploymentGroup#deployment_option}.
        :param deployment_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_type CodedeployDeploymentGroup#deployment_type}.
        '''
        value = CodedeployDeploymentGroupDeploymentStyle(
            deployment_option=deployment_option, deployment_type=deployment_type
        )

        return typing.cast(None, jsii.invoke(self, "putDeploymentStyle", [value]))

    @jsii.member(jsii_name="putEc2TagFilter")
    def put_ec2_tag_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupEc2TagFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ee5b23ed8dc76afd8422c65b9b475b66c437b38232816b4182f977681ac756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEc2TagFilter", [value]))

    @jsii.member(jsii_name="putEc2TagSet")
    def put_ec2_tag_set(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupEc2TagSet", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac5b08b862e66cd2ebee51957c288fabc116d978239bd6c552a0a337cdc122d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEc2TagSet", [value]))

    @jsii.member(jsii_name="putEcsService")
    def put_ecs_service(
        self,
        *,
        cluster_name: builtins.str,
        service_name: builtins.str,
    ) -> None:
        '''
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#cluster_name CodedeployDeploymentGroup#cluster_name}.
        :param service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#service_name CodedeployDeploymentGroup#service_name}.
        '''
        value = CodedeployDeploymentGroupEcsService(
            cluster_name=cluster_name, service_name=service_name
        )

        return typing.cast(None, jsii.invoke(self, "putEcsService", [value]))

    @jsii.member(jsii_name="putLoadBalancerInfo")
    def put_load_balancer_info(
        self,
        *,
        elb_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoElbInfo", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_group_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_group_pair_info: typing.Optional[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param elb_info: elb_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#elb_info CodedeployDeploymentGroup#elb_info}
        :param target_group_info: target_group_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#target_group_info CodedeployDeploymentGroup#target_group_info}
        :param target_group_pair_info: target_group_pair_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#target_group_pair_info CodedeployDeploymentGroup#target_group_pair_info}
        '''
        value = CodedeployDeploymentGroupLoadBalancerInfo(
            elb_info=elb_info,
            target_group_info=target_group_info,
            target_group_pair_info=target_group_pair_info,
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancerInfo", [value]))

    @jsii.member(jsii_name="putOnPremisesInstanceTagFilter")
    def put_on_premises_instance_tag_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupOnPremisesInstanceTagFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cdfcd1a37c3a764d056fa519501f4a900086783e516e748d601118dfe856744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOnPremisesInstanceTagFilter", [value]))

    @jsii.member(jsii_name="putTriggerConfiguration")
    def put_trigger_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupTriggerConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74aeb02cb491ee9f4320e0804f8e937f2498b81b117220a3e9584d304edba48d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTriggerConfiguration", [value]))

    @jsii.member(jsii_name="resetAlarmConfiguration")
    def reset_alarm_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlarmConfiguration", []))

    @jsii.member(jsii_name="resetAutoRollbackConfiguration")
    def reset_auto_rollback_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoRollbackConfiguration", []))

    @jsii.member(jsii_name="resetAutoscalingGroups")
    def reset_autoscaling_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingGroups", []))

    @jsii.member(jsii_name="resetBlueGreenDeploymentConfig")
    def reset_blue_green_deployment_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlueGreenDeploymentConfig", []))

    @jsii.member(jsii_name="resetDeploymentConfigName")
    def reset_deployment_config_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentConfigName", []))

    @jsii.member(jsii_name="resetDeploymentStyle")
    def reset_deployment_style(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentStyle", []))

    @jsii.member(jsii_name="resetEc2TagFilter")
    def reset_ec2_tag_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEc2TagFilter", []))

    @jsii.member(jsii_name="resetEc2TagSet")
    def reset_ec2_tag_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEc2TagSet", []))

    @jsii.member(jsii_name="resetEcsService")
    def reset_ecs_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEcsService", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLoadBalancerInfo")
    def reset_load_balancer_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerInfo", []))

    @jsii.member(jsii_name="resetOnPremisesInstanceTagFilter")
    def reset_on_premises_instance_tag_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnPremisesInstanceTagFilter", []))

    @jsii.member(jsii_name="resetOutdatedInstancesStrategy")
    def reset_outdated_instances_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutdatedInstancesStrategy", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTerminationHookEnabled")
    def reset_termination_hook_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminationHookEnabled", []))

    @jsii.member(jsii_name="resetTriggerConfiguration")
    def reset_trigger_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerConfiguration", []))

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
    @jsii.member(jsii_name="alarmConfiguration")
    def alarm_configuration(
        self,
    ) -> "CodedeployDeploymentGroupAlarmConfigurationOutputReference":
        return typing.cast("CodedeployDeploymentGroupAlarmConfigurationOutputReference", jsii.get(self, "alarmConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="autoRollbackConfiguration")
    def auto_rollback_configuration(
        self,
    ) -> "CodedeployDeploymentGroupAutoRollbackConfigurationOutputReference":
        return typing.cast("CodedeployDeploymentGroupAutoRollbackConfigurationOutputReference", jsii.get(self, "autoRollbackConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="blueGreenDeploymentConfig")
    def blue_green_deployment_config(
        self,
    ) -> "CodedeployDeploymentGroupBlueGreenDeploymentConfigOutputReference":
        return typing.cast("CodedeployDeploymentGroupBlueGreenDeploymentConfigOutputReference", jsii.get(self, "blueGreenDeploymentConfig"))

    @builtins.property
    @jsii.member(jsii_name="computePlatform")
    def compute_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computePlatform"))

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupId")
    def deployment_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupId"))

    @builtins.property
    @jsii.member(jsii_name="deploymentStyle")
    def deployment_style(
        self,
    ) -> "CodedeployDeploymentGroupDeploymentStyleOutputReference":
        return typing.cast("CodedeployDeploymentGroupDeploymentStyleOutputReference", jsii.get(self, "deploymentStyle"))

    @builtins.property
    @jsii.member(jsii_name="ec2TagFilter")
    def ec2_tag_filter(self) -> "CodedeployDeploymentGroupEc2TagFilterList":
        return typing.cast("CodedeployDeploymentGroupEc2TagFilterList", jsii.get(self, "ec2TagFilter"))

    @builtins.property
    @jsii.member(jsii_name="ec2TagSet")
    def ec2_tag_set(self) -> "CodedeployDeploymentGroupEc2TagSetList":
        return typing.cast("CodedeployDeploymentGroupEc2TagSetList", jsii.get(self, "ec2TagSet"))

    @builtins.property
    @jsii.member(jsii_name="ecsService")
    def ecs_service(self) -> "CodedeployDeploymentGroupEcsServiceOutputReference":
        return typing.cast("CodedeployDeploymentGroupEcsServiceOutputReference", jsii.get(self, "ecsService"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerInfo")
    def load_balancer_info(
        self,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoOutputReference":
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoOutputReference", jsii.get(self, "loadBalancerInfo"))

    @builtins.property
    @jsii.member(jsii_name="onPremisesInstanceTagFilter")
    def on_premises_instance_tag_filter(
        self,
    ) -> "CodedeployDeploymentGroupOnPremisesInstanceTagFilterList":
        return typing.cast("CodedeployDeploymentGroupOnPremisesInstanceTagFilterList", jsii.get(self, "onPremisesInstanceTagFilter"))

    @builtins.property
    @jsii.member(jsii_name="triggerConfiguration")
    def trigger_configuration(
        self,
    ) -> "CodedeployDeploymentGroupTriggerConfigurationList":
        return typing.cast("CodedeployDeploymentGroupTriggerConfigurationList", jsii.get(self, "triggerConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="alarmConfigurationInput")
    def alarm_configuration_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupAlarmConfiguration"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupAlarmConfiguration"], jsii.get(self, "alarmConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="appNameInput")
    def app_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appNameInput"))

    @builtins.property
    @jsii.member(jsii_name="autoRollbackConfigurationInput")
    def auto_rollback_configuration_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupAutoRollbackConfiguration"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupAutoRollbackConfiguration"], jsii.get(self, "autoRollbackConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingGroupsInput")
    def autoscaling_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "autoscalingGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="blueGreenDeploymentConfigInput")
    def blue_green_deployment_config_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfig"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfig"], jsii.get(self, "blueGreenDeploymentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigNameInput")
    def deployment_config_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentConfigNameInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupNameInput")
    def deployment_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentStyleInput")
    def deployment_style_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupDeploymentStyle"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupDeploymentStyle"], jsii.get(self, "deploymentStyleInput"))

    @builtins.property
    @jsii.member(jsii_name="ec2TagFilterInput")
    def ec2_tag_filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagFilter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagFilter"]]], jsii.get(self, "ec2TagFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="ec2TagSetInput")
    def ec2_tag_set_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagSet"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagSet"]]], jsii.get(self, "ec2TagSetInput"))

    @builtins.property
    @jsii.member(jsii_name="ecsServiceInput")
    def ecs_service_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupEcsService"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupEcsService"], jsii.get(self, "ecsServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerInfoInput")
    def load_balancer_info_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupLoadBalancerInfo"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupLoadBalancerInfo"], jsii.get(self, "loadBalancerInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="onPremisesInstanceTagFilterInput")
    def on_premises_instance_tag_filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupOnPremisesInstanceTagFilter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupOnPremisesInstanceTagFilter"]]], jsii.get(self, "onPremisesInstanceTagFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="outdatedInstancesStrategyInput")
    def outdated_instances_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outdatedInstancesStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceRoleArnInput")
    def service_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="terminationHookEnabledInput")
    def termination_hook_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "terminationHookEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerConfigurationInput")
    def trigger_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupTriggerConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupTriggerConfiguration"]]], jsii.get(self, "triggerConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="appName")
    def app_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appName"))

    @app_name.setter
    def app_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ebdac24272931d293d7d288284be40016291b13adc1e0b5ab9cc97fa96896c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoscalingGroups")
    def autoscaling_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "autoscalingGroups"))

    @autoscaling_groups.setter
    def autoscaling_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c176f8bb62f87bcad224cf36fd3b508ed1239775e052e3b97649cfae0508e767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoscalingGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigName"))

    @deployment_config_name.setter
    def deployment_config_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828aef8734de6f6e22a08d07a67357333a94276a67008688136f8488bbeb52de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentConfigName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupName"))

    @deployment_group_name.setter
    def deployment_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc81e745351105adc1647386897100ff034be1b7f2cba0d56d948d0cde422d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d865cc35f995bf13111409a6ba4c3e90fb182b68c67a4f2ee98abb37aef5a8e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outdatedInstancesStrategy")
    def outdated_instances_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outdatedInstancesStrategy"))

    @outdated_instances_strategy.setter
    def outdated_instances_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf1a5ae66bc26ad1a35be6a6f627408d7a7ac555543cbab94d39bb93578abd70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outdatedInstancesStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceRoleArn")
    def service_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceRoleArn"))

    @service_role_arn.setter
    def service_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80030f017678f4a46a6ac3ea4024e64158dc1c3995a767d262625b6fd0af11e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b0734ff37d9fc9354196e139f2e3045b9f1c691becdf0a96496300194baebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afad902f7eb76c7afcd470e23b78b22d4d6aa68174c2abe5488fdbb2dea30d69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terminationHookEnabled")
    def termination_hook_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "terminationHookEnabled"))

    @termination_hook_enabled.setter
    def termination_hook_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d84394e1010636ed0faeb54cfebe102f159a87b620fbde53f8e8939329ae9e36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminationHookEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupAlarmConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "alarms": "alarms",
        "enabled": "enabled",
        "ignore_poll_alarm_failure": "ignorePollAlarmFailure",
    },
)
class CodedeployDeploymentGroupAlarmConfiguration:
    def __init__(
        self,
        *,
        alarms: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore_poll_alarm_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param alarms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#alarms CodedeployDeploymentGroup#alarms}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#enabled CodedeployDeploymentGroup#enabled}.
        :param ignore_poll_alarm_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#ignore_poll_alarm_failure CodedeployDeploymentGroup#ignore_poll_alarm_failure}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43adba8b8a5c016f1be62f484e83f1624e6aeeaae069eb79fb0e8adf1b4f733c)
            check_type(argname="argument alarms", value=alarms, expected_type=type_hints["alarms"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument ignore_poll_alarm_failure", value=ignore_poll_alarm_failure, expected_type=type_hints["ignore_poll_alarm_failure"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarms is not None:
            self._values["alarms"] = alarms
        if enabled is not None:
            self._values["enabled"] = enabled
        if ignore_poll_alarm_failure is not None:
            self._values["ignore_poll_alarm_failure"] = ignore_poll_alarm_failure

    @builtins.property
    def alarms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#alarms CodedeployDeploymentGroup#alarms}.'''
        result = self._values.get("alarms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#enabled CodedeployDeploymentGroup#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ignore_poll_alarm_failure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#ignore_poll_alarm_failure CodedeployDeploymentGroup#ignore_poll_alarm_failure}.'''
        result = self._values.get("ignore_poll_alarm_failure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupAlarmConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupAlarmConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupAlarmConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fc4073362b5098ae2bcf5e765ee0a1fd9ce21f0eefc7ae2d7b5a5a645c8c15f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAlarms")
    def reset_alarms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlarms", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetIgnorePollAlarmFailure")
    def reset_ignore_poll_alarm_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnorePollAlarmFailure", []))

    @builtins.property
    @jsii.member(jsii_name="alarmsInput")
    def alarms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "alarmsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ignorePollAlarmFailureInput")
    def ignore_poll_alarm_failure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignorePollAlarmFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="alarms")
    def alarms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "alarms"))

    @alarms.setter
    def alarms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43ecd171ffd4a615248a2bdce4e0d61881c42e35574355f2d82d0b8f22e3176a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarms", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__14d13e82a520163e3202a2f91ee07f4cc64047f09c8b18d6ee7206c796ce3180)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignorePollAlarmFailure")
    def ignore_poll_alarm_failure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignorePollAlarmFailure"))

    @ignore_poll_alarm_failure.setter
    def ignore_poll_alarm_failure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82120c79b7524e01ecd4d6da302875e874f2592094d15d583d042c2e64f1bdf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignorePollAlarmFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupAlarmConfiguration]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupAlarmConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupAlarmConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb7bd91e7be038a4435d03dd78d22fd454442efc0544d0b2086161c8e3ca21e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupAutoRollbackConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "events": "events"},
)
class CodedeployDeploymentGroupAutoRollbackConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        events: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#enabled CodedeployDeploymentGroup#enabled}.
        :param events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#events CodedeployDeploymentGroup#events}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baa42a1d6ba822b9079166a9a68a25a2de0b4779a57f8b7b7254b1bc313a743f)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if events is not None:
            self._values["events"] = events

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#enabled CodedeployDeploymentGroup#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def events(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#events CodedeployDeploymentGroup#events}.'''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupAutoRollbackConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupAutoRollbackConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupAutoRollbackConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a18ad3947c17d9f2965cefd10dd5c410f3db0be15e1fa8f04ff76f5828f943c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEvents")
    def reset_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvents", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="eventsInput")
    def events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "eventsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6424b37bedff30a85c5d2db72683c3e95657467b5446429f024073b697f15e05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="events")
    def events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "events"))

    @events.setter
    def events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2c767a13133d810f456feba7be4bb7d0a08e6fedfc79263b917b0a68adcdf68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "events", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupAutoRollbackConfiguration]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupAutoRollbackConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupAutoRollbackConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b1ee3309ec8b078951394cc20e6db5128f9f860b29757d26a1603bd8eba27b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupBlueGreenDeploymentConfig",
    jsii_struct_bases=[],
    name_mapping={
        "deployment_ready_option": "deploymentReadyOption",
        "green_fleet_provisioning_option": "greenFleetProvisioningOption",
        "terminate_blue_instances_on_deployment_success": "terminateBlueInstancesOnDeploymentSuccess",
    },
)
class CodedeployDeploymentGroupBlueGreenDeploymentConfig:
    def __init__(
        self,
        *,
        deployment_ready_option: typing.Optional[typing.Union["CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption", typing.Dict[builtins.str, typing.Any]]] = None,
        green_fleet_provisioning_option: typing.Optional[typing.Union["CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption", typing.Dict[builtins.str, typing.Any]]] = None,
        terminate_blue_instances_on_deployment_success: typing.Optional[typing.Union["CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param deployment_ready_option: deployment_ready_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_ready_option CodedeployDeploymentGroup#deployment_ready_option}
        :param green_fleet_provisioning_option: green_fleet_provisioning_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#green_fleet_provisioning_option CodedeployDeploymentGroup#green_fleet_provisioning_option}
        :param terminate_blue_instances_on_deployment_success: terminate_blue_instances_on_deployment_success block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#terminate_blue_instances_on_deployment_success CodedeployDeploymentGroup#terminate_blue_instances_on_deployment_success}
        '''
        if isinstance(deployment_ready_option, dict):
            deployment_ready_option = CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption(**deployment_ready_option)
        if isinstance(green_fleet_provisioning_option, dict):
            green_fleet_provisioning_option = CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption(**green_fleet_provisioning_option)
        if isinstance(terminate_blue_instances_on_deployment_success, dict):
            terminate_blue_instances_on_deployment_success = CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess(**terminate_blue_instances_on_deployment_success)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad808aa10c35f06fd44e2f136e9ce6e8f62a1ebf4e49ea7098dbe6b17d7f1d8f)
            check_type(argname="argument deployment_ready_option", value=deployment_ready_option, expected_type=type_hints["deployment_ready_option"])
            check_type(argname="argument green_fleet_provisioning_option", value=green_fleet_provisioning_option, expected_type=type_hints["green_fleet_provisioning_option"])
            check_type(argname="argument terminate_blue_instances_on_deployment_success", value=terminate_blue_instances_on_deployment_success, expected_type=type_hints["terminate_blue_instances_on_deployment_success"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deployment_ready_option is not None:
            self._values["deployment_ready_option"] = deployment_ready_option
        if green_fleet_provisioning_option is not None:
            self._values["green_fleet_provisioning_option"] = green_fleet_provisioning_option
        if terminate_blue_instances_on_deployment_success is not None:
            self._values["terminate_blue_instances_on_deployment_success"] = terminate_blue_instances_on_deployment_success

    @builtins.property
    def deployment_ready_option(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption"]:
        '''deployment_ready_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_ready_option CodedeployDeploymentGroup#deployment_ready_option}
        '''
        result = self._values.get("deployment_ready_option")
        return typing.cast(typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption"], result)

    @builtins.property
    def green_fleet_provisioning_option(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption"]:
        '''green_fleet_provisioning_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#green_fleet_provisioning_option CodedeployDeploymentGroup#green_fleet_provisioning_option}
        '''
        result = self._values.get("green_fleet_provisioning_option")
        return typing.cast(typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption"], result)

    @builtins.property
    def terminate_blue_instances_on_deployment_success(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess"]:
        '''terminate_blue_instances_on_deployment_success block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#terminate_blue_instances_on_deployment_success CodedeployDeploymentGroup#terminate_blue_instances_on_deployment_success}
        '''
        result = self._values.get("terminate_blue_instances_on_deployment_success")
        return typing.cast(typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupBlueGreenDeploymentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption",
    jsii_struct_bases=[],
    name_mapping={
        "action_on_timeout": "actionOnTimeout",
        "wait_time_in_minutes": "waitTimeInMinutes",
    },
)
class CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption:
    def __init__(
        self,
        *,
        action_on_timeout: typing.Optional[builtins.str] = None,
        wait_time_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param action_on_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#action_on_timeout CodedeployDeploymentGroup#action_on_timeout}.
        :param wait_time_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#wait_time_in_minutes CodedeployDeploymentGroup#wait_time_in_minutes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2e6dbaa67308c9ddec15ad272f4e53b79164f9015630754e219d30a87a3200d)
            check_type(argname="argument action_on_timeout", value=action_on_timeout, expected_type=type_hints["action_on_timeout"])
            check_type(argname="argument wait_time_in_minutes", value=wait_time_in_minutes, expected_type=type_hints["wait_time_in_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action_on_timeout is not None:
            self._values["action_on_timeout"] = action_on_timeout
        if wait_time_in_minutes is not None:
            self._values["wait_time_in_minutes"] = wait_time_in_minutes

    @builtins.property
    def action_on_timeout(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#action_on_timeout CodedeployDeploymentGroup#action_on_timeout}.'''
        result = self._values.get("action_on_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wait_time_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#wait_time_in_minutes CodedeployDeploymentGroup#wait_time_in_minutes}.'''
        result = self._values.get("wait_time_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__564a02f40c812a433b50221f968f9496a5ac800bb149f95dde03d6ce5126a780)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetActionOnTimeout")
    def reset_action_on_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionOnTimeout", []))

    @jsii.member(jsii_name="resetWaitTimeInMinutes")
    def reset_wait_time_in_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWaitTimeInMinutes", []))

    @builtins.property
    @jsii.member(jsii_name="actionOnTimeoutInput")
    def action_on_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionOnTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="waitTimeInMinutesInput")
    def wait_time_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "waitTimeInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="actionOnTimeout")
    def action_on_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionOnTimeout"))

    @action_on_timeout.setter
    def action_on_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b3c30d530e65c0109bd9931737b184b91ca47d8a8e2dd4ef31ba340a04b288)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionOnTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitTimeInMinutes")
    def wait_time_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "waitTimeInMinutes"))

    @wait_time_in_minutes.setter
    def wait_time_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eae557a3f137e418579f28fcf979bca0e9619ba1cd454fdacda9e9c2277d834b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitTimeInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f66861e3ab7914f6dc521545f5acb72d10f958d021c0819f59e87759e44f6e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption",
    jsii_struct_bases=[],
    name_mapping={"action": "action"},
)
class CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption:
    def __init__(self, *, action: typing.Optional[builtins.str] = None) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#action CodedeployDeploymentGroup#action}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c0de3ab024894b4fd2af378912898747b48c2f23caad68e7fd7992b52b98f62)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#action CodedeployDeploymentGroup#action}.'''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__237428eb9b2bb1da8953dc8c98f0419cad4aca4fe6e9518a39d1d2a86a5f708a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8011603bbc81750d3b3795bbb6cc3a656ef64f9e8fad8ad988a21b134074d18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3009a366516b5375ab47204d228f9d62a3b12cabd2d00e3cb82a7d6c67cbd406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupBlueGreenDeploymentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupBlueGreenDeploymentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c091c88d8d4886852d7b03777d92f44891530626d0a55d607a3ea1cef3d2eb1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeploymentReadyOption")
    def put_deployment_ready_option(
        self,
        *,
        action_on_timeout: typing.Optional[builtins.str] = None,
        wait_time_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param action_on_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#action_on_timeout CodedeployDeploymentGroup#action_on_timeout}.
        :param wait_time_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#wait_time_in_minutes CodedeployDeploymentGroup#wait_time_in_minutes}.
        '''
        value = CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption(
            action_on_timeout=action_on_timeout,
            wait_time_in_minutes=wait_time_in_minutes,
        )

        return typing.cast(None, jsii.invoke(self, "putDeploymentReadyOption", [value]))

    @jsii.member(jsii_name="putGreenFleetProvisioningOption")
    def put_green_fleet_provisioning_option(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#action CodedeployDeploymentGroup#action}.
        '''
        value = CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption(
            action=action
        )

        return typing.cast(None, jsii.invoke(self, "putGreenFleetProvisioningOption", [value]))

    @jsii.member(jsii_name="putTerminateBlueInstancesOnDeploymentSuccess")
    def put_terminate_blue_instances_on_deployment_success(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        termination_wait_time_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#action CodedeployDeploymentGroup#action}.
        :param termination_wait_time_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#termination_wait_time_in_minutes CodedeployDeploymentGroup#termination_wait_time_in_minutes}.
        '''
        value = CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess(
            action=action,
            termination_wait_time_in_minutes=termination_wait_time_in_minutes,
        )

        return typing.cast(None, jsii.invoke(self, "putTerminateBlueInstancesOnDeploymentSuccess", [value]))

    @jsii.member(jsii_name="resetDeploymentReadyOption")
    def reset_deployment_ready_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentReadyOption", []))

    @jsii.member(jsii_name="resetGreenFleetProvisioningOption")
    def reset_green_fleet_provisioning_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGreenFleetProvisioningOption", []))

    @jsii.member(jsii_name="resetTerminateBlueInstancesOnDeploymentSuccess")
    def reset_terminate_blue_instances_on_deployment_success(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminateBlueInstancesOnDeploymentSuccess", []))

    @builtins.property
    @jsii.member(jsii_name="deploymentReadyOption")
    def deployment_ready_option(
        self,
    ) -> CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOptionOutputReference:
        return typing.cast(CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOptionOutputReference, jsii.get(self, "deploymentReadyOption"))

    @builtins.property
    @jsii.member(jsii_name="greenFleetProvisioningOption")
    def green_fleet_provisioning_option(
        self,
    ) -> CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOptionOutputReference:
        return typing.cast(CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOptionOutputReference, jsii.get(self, "greenFleetProvisioningOption"))

    @builtins.property
    @jsii.member(jsii_name="terminateBlueInstancesOnDeploymentSuccess")
    def terminate_blue_instances_on_deployment_success(
        self,
    ) -> "CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccessOutputReference":
        return typing.cast("CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccessOutputReference", jsii.get(self, "terminateBlueInstancesOnDeploymentSuccess"))

    @builtins.property
    @jsii.member(jsii_name="deploymentReadyOptionInput")
    def deployment_ready_option_input(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption], jsii.get(self, "deploymentReadyOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="greenFleetProvisioningOptionInput")
    def green_fleet_provisioning_option_input(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption], jsii.get(self, "greenFleetProvisioningOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="terminateBlueInstancesOnDeploymentSuccessInput")
    def terminate_blue_instances_on_deployment_success_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess"], jsii.get(self, "terminateBlueInstancesOnDeploymentSuccessInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfig]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ad71baad3ad5e556a627e7f6239d184cd77c0e6d26d738f29c4f3f16d8cb22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "termination_wait_time_in_minutes": "terminationWaitTimeInMinutes",
    },
)
class CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess:
    def __init__(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        termination_wait_time_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#action CodedeployDeploymentGroup#action}.
        :param termination_wait_time_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#termination_wait_time_in_minutes CodedeployDeploymentGroup#termination_wait_time_in_minutes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0626fcdb819dc69e998ec69563df6862f94c40ad7266de1d003c86411fc7adb2)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument termination_wait_time_in_minutes", value=termination_wait_time_in_minutes, expected_type=type_hints["termination_wait_time_in_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if termination_wait_time_in_minutes is not None:
            self._values["termination_wait_time_in_minutes"] = termination_wait_time_in_minutes

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#action CodedeployDeploymentGroup#action}.'''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def termination_wait_time_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#termination_wait_time_in_minutes CodedeployDeploymentGroup#termination_wait_time_in_minutes}.'''
        result = self._values.get("termination_wait_time_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e10cc4ab398ec68d517c023b5edd8b1034e70a1acb2216c19f750edab45a3825)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetTerminationWaitTimeInMinutes")
    def reset_termination_wait_time_in_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminationWaitTimeInMinutes", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="terminationWaitTimeInMinutesInput")
    def termination_wait_time_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "terminationWaitTimeInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9bffc08efc9078f27110a4a1e0a57074eeab7a5717e46d62f145818f1a2b90f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terminationWaitTimeInMinutes")
    def termination_wait_time_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "terminationWaitTimeInMinutes"))

    @termination_wait_time_in_minutes.setter
    def termination_wait_time_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7250bde1261fa6b03814db337892fffa5489c6d2a9a680acba08a789a26ece9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminationWaitTimeInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce8b3265581d7b3624a872b7a40b1ee386b6f3bd6a5323b4c9c6f807bf3eea6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "app_name": "appName",
        "deployment_group_name": "deploymentGroupName",
        "service_role_arn": "serviceRoleArn",
        "alarm_configuration": "alarmConfiguration",
        "auto_rollback_configuration": "autoRollbackConfiguration",
        "autoscaling_groups": "autoscalingGroups",
        "blue_green_deployment_config": "blueGreenDeploymentConfig",
        "deployment_config_name": "deploymentConfigName",
        "deployment_style": "deploymentStyle",
        "ec2_tag_filter": "ec2TagFilter",
        "ec2_tag_set": "ec2TagSet",
        "ecs_service": "ecsService",
        "id": "id",
        "load_balancer_info": "loadBalancerInfo",
        "on_premises_instance_tag_filter": "onPremisesInstanceTagFilter",
        "outdated_instances_strategy": "outdatedInstancesStrategy",
        "tags": "tags",
        "tags_all": "tagsAll",
        "termination_hook_enabled": "terminationHookEnabled",
        "trigger_configuration": "triggerConfiguration",
    },
)
class CodedeployDeploymentGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        app_name: builtins.str,
        deployment_group_name: builtins.str,
        service_role_arn: builtins.str,
        alarm_configuration: typing.Optional[typing.Union[CodedeployDeploymentGroupAlarmConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_rollback_configuration: typing.Optional[typing.Union[CodedeployDeploymentGroupAutoRollbackConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        autoscaling_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        blue_green_deployment_config: typing.Optional[typing.Union[CodedeployDeploymentGroupBlueGreenDeploymentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_config_name: typing.Optional[builtins.str] = None,
        deployment_style: typing.Optional[typing.Union["CodedeployDeploymentGroupDeploymentStyle", typing.Dict[builtins.str, typing.Any]]] = None,
        ec2_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupEc2TagFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ec2_tag_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupEc2TagSet", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ecs_service: typing.Optional[typing.Union["CodedeployDeploymentGroupEcsService", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancer_info: typing.Optional[typing.Union["CodedeployDeploymentGroupLoadBalancerInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        on_premises_instance_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupOnPremisesInstanceTagFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        outdated_instances_strategy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_hook_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trigger_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupTriggerConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param app_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#app_name CodedeployDeploymentGroup#app_name}.
        :param deployment_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_group_name CodedeployDeploymentGroup#deployment_group_name}.
        :param service_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#service_role_arn CodedeployDeploymentGroup#service_role_arn}.
        :param alarm_configuration: alarm_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#alarm_configuration CodedeployDeploymentGroup#alarm_configuration}
        :param auto_rollback_configuration: auto_rollback_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#auto_rollback_configuration CodedeployDeploymentGroup#auto_rollback_configuration}
        :param autoscaling_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#autoscaling_groups CodedeployDeploymentGroup#autoscaling_groups}.
        :param blue_green_deployment_config: blue_green_deployment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#blue_green_deployment_config CodedeployDeploymentGroup#blue_green_deployment_config}
        :param deployment_config_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_config_name CodedeployDeploymentGroup#deployment_config_name}.
        :param deployment_style: deployment_style block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_style CodedeployDeploymentGroup#deployment_style}
        :param ec2_tag_filter: ec2_tag_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#ec2_tag_filter CodedeployDeploymentGroup#ec2_tag_filter}
        :param ec2_tag_set: ec2_tag_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#ec2_tag_set CodedeployDeploymentGroup#ec2_tag_set}
        :param ecs_service: ecs_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#ecs_service CodedeployDeploymentGroup#ecs_service}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#id CodedeployDeploymentGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancer_info: load_balancer_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#load_balancer_info CodedeployDeploymentGroup#load_balancer_info}
        :param on_premises_instance_tag_filter: on_premises_instance_tag_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#on_premises_instance_tag_filter CodedeployDeploymentGroup#on_premises_instance_tag_filter}
        :param outdated_instances_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#outdated_instances_strategy CodedeployDeploymentGroup#outdated_instances_strategy}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#tags CodedeployDeploymentGroup#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#tags_all CodedeployDeploymentGroup#tags_all}.
        :param termination_hook_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#termination_hook_enabled CodedeployDeploymentGroup#termination_hook_enabled}.
        :param trigger_configuration: trigger_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#trigger_configuration CodedeployDeploymentGroup#trigger_configuration}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(alarm_configuration, dict):
            alarm_configuration = CodedeployDeploymentGroupAlarmConfiguration(**alarm_configuration)
        if isinstance(auto_rollback_configuration, dict):
            auto_rollback_configuration = CodedeployDeploymentGroupAutoRollbackConfiguration(**auto_rollback_configuration)
        if isinstance(blue_green_deployment_config, dict):
            blue_green_deployment_config = CodedeployDeploymentGroupBlueGreenDeploymentConfig(**blue_green_deployment_config)
        if isinstance(deployment_style, dict):
            deployment_style = CodedeployDeploymentGroupDeploymentStyle(**deployment_style)
        if isinstance(ecs_service, dict):
            ecs_service = CodedeployDeploymentGroupEcsService(**ecs_service)
        if isinstance(load_balancer_info, dict):
            load_balancer_info = CodedeployDeploymentGroupLoadBalancerInfo(**load_balancer_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70a08659a2c5dfa1a9dc7747a0f987940cec65f408e079759662082b32e0fc62)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument app_name", value=app_name, expected_type=type_hints["app_name"])
            check_type(argname="argument deployment_group_name", value=deployment_group_name, expected_type=type_hints["deployment_group_name"])
            check_type(argname="argument service_role_arn", value=service_role_arn, expected_type=type_hints["service_role_arn"])
            check_type(argname="argument alarm_configuration", value=alarm_configuration, expected_type=type_hints["alarm_configuration"])
            check_type(argname="argument auto_rollback_configuration", value=auto_rollback_configuration, expected_type=type_hints["auto_rollback_configuration"])
            check_type(argname="argument autoscaling_groups", value=autoscaling_groups, expected_type=type_hints["autoscaling_groups"])
            check_type(argname="argument blue_green_deployment_config", value=blue_green_deployment_config, expected_type=type_hints["blue_green_deployment_config"])
            check_type(argname="argument deployment_config_name", value=deployment_config_name, expected_type=type_hints["deployment_config_name"])
            check_type(argname="argument deployment_style", value=deployment_style, expected_type=type_hints["deployment_style"])
            check_type(argname="argument ec2_tag_filter", value=ec2_tag_filter, expected_type=type_hints["ec2_tag_filter"])
            check_type(argname="argument ec2_tag_set", value=ec2_tag_set, expected_type=type_hints["ec2_tag_set"])
            check_type(argname="argument ecs_service", value=ecs_service, expected_type=type_hints["ecs_service"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument load_balancer_info", value=load_balancer_info, expected_type=type_hints["load_balancer_info"])
            check_type(argname="argument on_premises_instance_tag_filter", value=on_premises_instance_tag_filter, expected_type=type_hints["on_premises_instance_tag_filter"])
            check_type(argname="argument outdated_instances_strategy", value=outdated_instances_strategy, expected_type=type_hints["outdated_instances_strategy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument termination_hook_enabled", value=termination_hook_enabled, expected_type=type_hints["termination_hook_enabled"])
            check_type(argname="argument trigger_configuration", value=trigger_configuration, expected_type=type_hints["trigger_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_name": app_name,
            "deployment_group_name": deployment_group_name,
            "service_role_arn": service_role_arn,
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
        if alarm_configuration is not None:
            self._values["alarm_configuration"] = alarm_configuration
        if auto_rollback_configuration is not None:
            self._values["auto_rollback_configuration"] = auto_rollback_configuration
        if autoscaling_groups is not None:
            self._values["autoscaling_groups"] = autoscaling_groups
        if blue_green_deployment_config is not None:
            self._values["blue_green_deployment_config"] = blue_green_deployment_config
        if deployment_config_name is not None:
            self._values["deployment_config_name"] = deployment_config_name
        if deployment_style is not None:
            self._values["deployment_style"] = deployment_style
        if ec2_tag_filter is not None:
            self._values["ec2_tag_filter"] = ec2_tag_filter
        if ec2_tag_set is not None:
            self._values["ec2_tag_set"] = ec2_tag_set
        if ecs_service is not None:
            self._values["ecs_service"] = ecs_service
        if id is not None:
            self._values["id"] = id
        if load_balancer_info is not None:
            self._values["load_balancer_info"] = load_balancer_info
        if on_premises_instance_tag_filter is not None:
            self._values["on_premises_instance_tag_filter"] = on_premises_instance_tag_filter
        if outdated_instances_strategy is not None:
            self._values["outdated_instances_strategy"] = outdated_instances_strategy
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if termination_hook_enabled is not None:
            self._values["termination_hook_enabled"] = termination_hook_enabled
        if trigger_configuration is not None:
            self._values["trigger_configuration"] = trigger_configuration

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
    def app_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#app_name CodedeployDeploymentGroup#app_name}.'''
        result = self._values.get("app_name")
        assert result is not None, "Required property 'app_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_group_name CodedeployDeploymentGroup#deployment_group_name}.'''
        result = self._values.get("deployment_group_name")
        assert result is not None, "Required property 'deployment_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#service_role_arn CodedeployDeploymentGroup#service_role_arn}.'''
        result = self._values.get("service_role_arn")
        assert result is not None, "Required property 'service_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alarm_configuration(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupAlarmConfiguration]:
        '''alarm_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#alarm_configuration CodedeployDeploymentGroup#alarm_configuration}
        '''
        result = self._values.get("alarm_configuration")
        return typing.cast(typing.Optional[CodedeployDeploymentGroupAlarmConfiguration], result)

    @builtins.property
    def auto_rollback_configuration(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupAutoRollbackConfiguration]:
        '''auto_rollback_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#auto_rollback_configuration CodedeployDeploymentGroup#auto_rollback_configuration}
        '''
        result = self._values.get("auto_rollback_configuration")
        return typing.cast(typing.Optional[CodedeployDeploymentGroupAutoRollbackConfiguration], result)

    @builtins.property
    def autoscaling_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#autoscaling_groups CodedeployDeploymentGroup#autoscaling_groups}.'''
        result = self._values.get("autoscaling_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def blue_green_deployment_config(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfig]:
        '''blue_green_deployment_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#blue_green_deployment_config CodedeployDeploymentGroup#blue_green_deployment_config}
        '''
        result = self._values.get("blue_green_deployment_config")
        return typing.cast(typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfig], result)

    @builtins.property
    def deployment_config_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_config_name CodedeployDeploymentGroup#deployment_config_name}.'''
        result = self._values.get("deployment_config_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_style(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupDeploymentStyle"]:
        '''deployment_style block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_style CodedeployDeploymentGroup#deployment_style}
        '''
        result = self._values.get("deployment_style")
        return typing.cast(typing.Optional["CodedeployDeploymentGroupDeploymentStyle"], result)

    @builtins.property
    def ec2_tag_filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagFilter"]]]:
        '''ec2_tag_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#ec2_tag_filter CodedeployDeploymentGroup#ec2_tag_filter}
        '''
        result = self._values.get("ec2_tag_filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagFilter"]]], result)

    @builtins.property
    def ec2_tag_set(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagSet"]]]:
        '''ec2_tag_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#ec2_tag_set CodedeployDeploymentGroup#ec2_tag_set}
        '''
        result = self._values.get("ec2_tag_set")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagSet"]]], result)

    @builtins.property
    def ecs_service(self) -> typing.Optional["CodedeployDeploymentGroupEcsService"]:
        '''ecs_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#ecs_service CodedeployDeploymentGroup#ecs_service}
        '''
        result = self._values.get("ecs_service")
        return typing.cast(typing.Optional["CodedeployDeploymentGroupEcsService"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#id CodedeployDeploymentGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_info(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupLoadBalancerInfo"]:
        '''load_balancer_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#load_balancer_info CodedeployDeploymentGroup#load_balancer_info}
        '''
        result = self._values.get("load_balancer_info")
        return typing.cast(typing.Optional["CodedeployDeploymentGroupLoadBalancerInfo"], result)

    @builtins.property
    def on_premises_instance_tag_filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupOnPremisesInstanceTagFilter"]]]:
        '''on_premises_instance_tag_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#on_premises_instance_tag_filter CodedeployDeploymentGroup#on_premises_instance_tag_filter}
        '''
        result = self._values.get("on_premises_instance_tag_filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupOnPremisesInstanceTagFilter"]]], result)

    @builtins.property
    def outdated_instances_strategy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#outdated_instances_strategy CodedeployDeploymentGroup#outdated_instances_strategy}.'''
        result = self._values.get("outdated_instances_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#tags CodedeployDeploymentGroup#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#tags_all CodedeployDeploymentGroup#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def termination_hook_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#termination_hook_enabled CodedeployDeploymentGroup#termination_hook_enabled}.'''
        result = self._values.get("termination_hook_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def trigger_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupTriggerConfiguration"]]]:
        '''trigger_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#trigger_configuration CodedeployDeploymentGroup#trigger_configuration}
        '''
        result = self._values.get("trigger_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupTriggerConfiguration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupDeploymentStyle",
    jsii_struct_bases=[],
    name_mapping={
        "deployment_option": "deploymentOption",
        "deployment_type": "deploymentType",
    },
)
class CodedeployDeploymentGroupDeploymentStyle:
    def __init__(
        self,
        *,
        deployment_option: typing.Optional[builtins.str] = None,
        deployment_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deployment_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_option CodedeployDeploymentGroup#deployment_option}.
        :param deployment_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_type CodedeployDeploymentGroup#deployment_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaeccf9adf3f39a435a03b49a74b2496aa96b9826fdd136f668ef12ab57679c0)
            check_type(argname="argument deployment_option", value=deployment_option, expected_type=type_hints["deployment_option"])
            check_type(argname="argument deployment_type", value=deployment_type, expected_type=type_hints["deployment_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deployment_option is not None:
            self._values["deployment_option"] = deployment_option
        if deployment_type is not None:
            self._values["deployment_type"] = deployment_type

    @builtins.property
    def deployment_option(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_option CodedeployDeploymentGroup#deployment_option}.'''
        result = self._values.get("deployment_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#deployment_type CodedeployDeploymentGroup#deployment_type}.'''
        result = self._values.get("deployment_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupDeploymentStyle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupDeploymentStyleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupDeploymentStyleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56dc2e01a3a32e73e281298b55d55f51df7b96862f083fc29dd9fab4ee1fed83)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDeploymentOption")
    def reset_deployment_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentOption", []))

    @jsii.member(jsii_name="resetDeploymentType")
    def reset_deployment_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentType", []))

    @builtins.property
    @jsii.member(jsii_name="deploymentOptionInput")
    def deployment_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentTypeInput")
    def deployment_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentOption")
    def deployment_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentOption"))

    @deployment_option.setter
    def deployment_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6d32f8bd2533ff404c74a4cd534bc812eb04cb6fa438594df69553ec744cab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentType")
    def deployment_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentType"))

    @deployment_type.setter
    def deployment_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c70dc5918fe4b4e6decbf858a2a3de3bd8395bb9f87080bb61fc58ba071fd25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupDeploymentStyle]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupDeploymentStyle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupDeploymentStyle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43e5fdc9da2ff804101c11f250beb37356264b45d1478203d10f3fb9f242622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagFilter",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "type": "type", "value": "value"},
)
class CodedeployDeploymentGroupEc2TagFilter:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#key CodedeployDeploymentGroup#key}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#type CodedeployDeploymentGroup#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#value CodedeployDeploymentGroup#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec9a27d72bf01985f0d0e200833c0cb4a8b1967d3fee497803b689ec30b35457)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#key CodedeployDeploymentGroup#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#type CodedeployDeploymentGroup#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#value CodedeployDeploymentGroup#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupEc2TagFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupEc2TagFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ae88845855f664f08412ef654c47b1a3a3b6b47e2af1020c0cac7bf85d38d19)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodedeployDeploymentGroupEc2TagFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21cc3e51f4a9c61a18087e19a5e6afa5aaad67814c2372c88bb4ff6ba18eb70b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodedeployDeploymentGroupEc2TagFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b97d17ce3f53f45ad203f9e3dfcd7db756b5fa56902e72b925aa8d4444defe44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3405c5aeaecc11e37f9e007c7ff57eb37c319caa3e19635e5647ed64ae9702e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__774a78acd087220082adb2fd75f45927249fc9a4c48a247a81771d854c5fa489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acc23c39530268c865a2477113ed029b98787ca7595abc2372fe99f86be650b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupEc2TagFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c43f3c5b5166126889f98bd585cdb4036b18966928c0088b8b01ee56b8966efc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d592a0ffea59afb23a81b933028f0326906b137354c8fb30cdfd75dfa0c7110a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5237a618fe4d049ca71b56e42eb4848f4a858968e9a2cb1f979c6baa2ddae937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6448253a38716b9852ba8b16b38c166589bbdb03825084dbb9cfd1a1c6df24b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba3fdb4aca37606e88a54b1af2c00b7a3afef7218e6ea8292c168e137457305c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagSet",
    jsii_struct_bases=[],
    name_mapping={"ec2_tag_filter": "ec2TagFilter"},
)
class CodedeployDeploymentGroupEc2TagSet:
    def __init__(
        self,
        *,
        ec2_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupEc2TagSetEc2TagFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param ec2_tag_filter: ec2_tag_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#ec2_tag_filter CodedeployDeploymentGroup#ec2_tag_filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc0e14ad179a85e874a651bdabb5f4f8df26a7f83f0017826c15e7229dd51b4)
            check_type(argname="argument ec2_tag_filter", value=ec2_tag_filter, expected_type=type_hints["ec2_tag_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ec2_tag_filter is not None:
            self._values["ec2_tag_filter"] = ec2_tag_filter

    @builtins.property
    def ec2_tag_filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagSetEc2TagFilter"]]]:
        '''ec2_tag_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#ec2_tag_filter CodedeployDeploymentGroup#ec2_tag_filter}
        '''
        result = self._values.get("ec2_tag_filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupEc2TagSetEc2TagFilter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupEc2TagSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagSetEc2TagFilter",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "type": "type", "value": "value"},
)
class CodedeployDeploymentGroupEc2TagSetEc2TagFilter:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#key CodedeployDeploymentGroup#key}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#type CodedeployDeploymentGroup#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#value CodedeployDeploymentGroup#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee0fa3d898a78c742305d77d110cc77830a7dffa27e5ee4db723b98a2fbdc38e)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#key CodedeployDeploymentGroup#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#type CodedeployDeploymentGroup#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#value CodedeployDeploymentGroup#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupEc2TagSetEc2TagFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupEc2TagSetEc2TagFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagSetEc2TagFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c6cd42c87887fbba8a32df22bcb1f3ce2dba7575dc8a9db2c1ba9d6956c416c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodedeployDeploymentGroupEc2TagSetEc2TagFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e80af3974a0eb558ed6cfb1e84411b20a551f748ee03318cf417221d3624bed8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodedeployDeploymentGroupEc2TagSetEc2TagFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0683da8c5e5ee29fa7d71e7bc9999d77d11e1e35bbcb2ad2f9ef7ab958daea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9691809bcee967e8d22c28a53bf11ed1516bac0cfd3288fde7c1d6dbef9f8ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__067f4aba3a9d441143d85faac92624be048e0c5614bdf14fd2b9626f37c27cc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSetEc2TagFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSetEc2TagFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSetEc2TagFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff419bcb7bfab7c6ccd9ce998a2582099cb27bad7861b8cf017332845de42984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupEc2TagSetEc2TagFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagSetEc2TagFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c52a3820866403722742df7b39dc300e7f228f6b168aba7a8ce5ca3e42a4f2b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__905d89b5d614418fac92a6d35cb93056182a8bb4626003762ac2cbeae000a97b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb436ef94e4ccf90ccf39ffec5ac552080f0a64d82aee706ca17f562acc9e46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa2ab22a78886a72de6fe578f61b8dc97e1c80ec094adec884cf3383252bc68e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagSetEc2TagFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagSetEc2TagFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagSetEc2TagFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f164b91c70009461701b8e7147594f055427e60bc0312fe5cb16f14858ebe34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupEc2TagSetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagSetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c663f402f9cfe929def8f2dd7e85bcf439d944869fa673c67b95fc09eef87bb4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodedeployDeploymentGroupEc2TagSetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d907e498f37fd2a5e49c9098aa0ee094591bdde2ae48060e1f0382f03a79ba)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodedeployDeploymentGroupEc2TagSetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09c1674bd7c8264d43d24c94a3782c59dfe64169040d933973e148a05fc8472a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96c64083212f5855ccffd3b9d89e0539450e7a085086389c35609641e90b0334)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7c4b352f3352920f6967791d60e9fde2a621ee2a1e3ca29182f45ba0c18dbfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSet]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSet]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSet]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0c604f387eca41a492e1bfbb727894175cc3d84150cb5118730d5de8cb772bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupEc2TagSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEc2TagSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52cf9362bb2a15218c9dfc5d79c3afae2b6137ece85013abb5c366130bb54896)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEc2TagFilter")
    def put_ec2_tag_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagSetEc2TagFilter, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fbf0017b7a12660406bfdd050cb3b465cafa998715a1022ab37d5f996419797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEc2TagFilter", [value]))

    @jsii.member(jsii_name="resetEc2TagFilter")
    def reset_ec2_tag_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEc2TagFilter", []))

    @builtins.property
    @jsii.member(jsii_name="ec2TagFilter")
    def ec2_tag_filter(self) -> CodedeployDeploymentGroupEc2TagSetEc2TagFilterList:
        return typing.cast(CodedeployDeploymentGroupEc2TagSetEc2TagFilterList, jsii.get(self, "ec2TagFilter"))

    @builtins.property
    @jsii.member(jsii_name="ec2TagFilterInput")
    def ec2_tag_filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSetEc2TagFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSetEc2TagFilter]]], jsii.get(self, "ec2TagFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagSet]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagSet]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagSet]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4217c6a028762d627b79d984896745c1f3f2cbf595e7b74bcaf90da3775bc0fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEcsService",
    jsii_struct_bases=[],
    name_mapping={"cluster_name": "clusterName", "service_name": "serviceName"},
)
class CodedeployDeploymentGroupEcsService:
    def __init__(
        self,
        *,
        cluster_name: builtins.str,
        service_name: builtins.str,
    ) -> None:
        '''
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#cluster_name CodedeployDeploymentGroup#cluster_name}.
        :param service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#service_name CodedeployDeploymentGroup#service_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c865915a56ad1e94265800d2fe74e95e30b19a401a024ab4cb8cb82deaeaa465)
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_name": cluster_name,
            "service_name": service_name,
        }

    @builtins.property
    def cluster_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#cluster_name CodedeployDeploymentGroup#cluster_name}.'''
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#service_name CodedeployDeploymentGroup#service_name}.'''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupEcsService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupEcsServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupEcsServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcec2d7996557f0462dc29eb9e8532ea97ea85466cac7c08e13210712d5b4db7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5225433566c5d33922df2db664b1cb4b3eb55ed6af87627bf0a0510866149b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d749a78f40961840bfb147958a8524698774590b3dc2f923dc878ce77b3bf2b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CodedeployDeploymentGroupEcsService]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupEcsService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupEcsService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb532c161dc5732f1db41a84926d6c1d52f4e0547b7218f4b9fc32f2c150a7e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfo",
    jsii_struct_bases=[],
    name_mapping={
        "elb_info": "elbInfo",
        "target_group_info": "targetGroupInfo",
        "target_group_pair_info": "targetGroupPairInfo",
    },
)
class CodedeployDeploymentGroupLoadBalancerInfo:
    def __init__(
        self,
        *,
        elb_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoElbInfo", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_group_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_group_pair_info: typing.Optional[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param elb_info: elb_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#elb_info CodedeployDeploymentGroup#elb_info}
        :param target_group_info: target_group_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#target_group_info CodedeployDeploymentGroup#target_group_info}
        :param target_group_pair_info: target_group_pair_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#target_group_pair_info CodedeployDeploymentGroup#target_group_pair_info}
        '''
        if isinstance(target_group_pair_info, dict):
            target_group_pair_info = CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo(**target_group_pair_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a56f13d41b750d84e25748655bf373c202a65324c39c3d65749fb8ea3a81efc4)
            check_type(argname="argument elb_info", value=elb_info, expected_type=type_hints["elb_info"])
            check_type(argname="argument target_group_info", value=target_group_info, expected_type=type_hints["target_group_info"])
            check_type(argname="argument target_group_pair_info", value=target_group_pair_info, expected_type=type_hints["target_group_pair_info"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if elb_info is not None:
            self._values["elb_info"] = elb_info
        if target_group_info is not None:
            self._values["target_group_info"] = target_group_info
        if target_group_pair_info is not None:
            self._values["target_group_pair_info"] = target_group_pair_info

    @builtins.property
    def elb_info(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoElbInfo"]]]:
        '''elb_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#elb_info CodedeployDeploymentGroup#elb_info}
        '''
        result = self._values.get("elb_info")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoElbInfo"]]], result)

    @builtins.property
    def target_group_info(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo"]]]:
        '''target_group_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#target_group_info CodedeployDeploymentGroup#target_group_info}
        '''
        result = self._values.get("target_group_info")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo"]]], result)

    @builtins.property
    def target_group_pair_info(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo"]:
        '''target_group_pair_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#target_group_pair_info CodedeployDeploymentGroup#target_group_pair_info}
        '''
        result = self._values.get("target_group_pair_info")
        return typing.cast(typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupLoadBalancerInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoElbInfo",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class CodedeployDeploymentGroupLoadBalancerInfoElbInfo:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#name CodedeployDeploymentGroup#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7be0610f5c864934a24e053b3dc3e1fb312869caeed73c996554dadd71ea5a2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#name CodedeployDeploymentGroup#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupLoadBalancerInfoElbInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupLoadBalancerInfoElbInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoElbInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05edd99cde1bd57fb3e17f98fdc166cb17459f7e8cad3ca0e2d9b67d65aeda06)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoElbInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e22c9b0536ed8865be1ff7f54caa98a6803bcd0a8532f37874cd28d74f251f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoElbInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f651986725a24364827dad9c2b00b5ee07eca414a6e47355950b666c7f5cd3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca1a56ff0bc2923e9777f791ba67c1c9829b3128119abd90e3ecd7308781ce12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3390166e62c07d932973b7647faf63c0b920477108bd4313064a03f1577afc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoElbInfo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoElbInfo]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoElbInfo]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8ec1fc7a2137d26b8c9a86b4519eb5c0d5a22cb5dbe92101061e9f616820781)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupLoadBalancerInfoElbInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoElbInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__452719bbca2a22ff03967a40394a559ab930dee5fc13f44893da639c7ff05d57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae01b561d39a55e8968a315766e389e14f858ea418c43f7687ee627846e422c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoElbInfo]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoElbInfo]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoElbInfo]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8068c12ffcabda9d8bb559cfa600d8130fedcf793c823c9e9f1400b76108d36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupLoadBalancerInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cf1fee2db0673b8106950036d8e4eeba5eed51ed2eacb411353af9961feb8d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putElbInfo")
    def put_elb_info(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoElbInfo, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd74c91e1768744ca160e7f729e12f6eeb71a84112b527b344eed1a678e98233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putElbInfo", [value]))

    @jsii.member(jsii_name="putTargetGroupInfo")
    def put_target_group_info(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f82af5554eaf162b2045868d69ec23d688456f6d766028f6c90e42d6e6100ad0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargetGroupInfo", [value]))

    @jsii.member(jsii_name="putTargetGroupPairInfo")
    def put_target_group_pair_info(
        self,
        *,
        prod_traffic_route: typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute", typing.Dict[builtins.str, typing.Any]],
        target_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup", typing.Dict[builtins.str, typing.Any]]]],
        test_traffic_route: typing.Optional[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param prod_traffic_route: prod_traffic_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#prod_traffic_route CodedeployDeploymentGroup#prod_traffic_route}
        :param target_group: target_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#target_group CodedeployDeploymentGroup#target_group}
        :param test_traffic_route: test_traffic_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#test_traffic_route CodedeployDeploymentGroup#test_traffic_route}
        '''
        value = CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo(
            prod_traffic_route=prod_traffic_route,
            target_group=target_group,
            test_traffic_route=test_traffic_route,
        )

        return typing.cast(None, jsii.invoke(self, "putTargetGroupPairInfo", [value]))

    @jsii.member(jsii_name="resetElbInfo")
    def reset_elb_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElbInfo", []))

    @jsii.member(jsii_name="resetTargetGroupInfo")
    def reset_target_group_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetGroupInfo", []))

    @jsii.member(jsii_name="resetTargetGroupPairInfo")
    def reset_target_group_pair_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetGroupPairInfo", []))

    @builtins.property
    @jsii.member(jsii_name="elbInfo")
    def elb_info(self) -> CodedeployDeploymentGroupLoadBalancerInfoElbInfoList:
        return typing.cast(CodedeployDeploymentGroupLoadBalancerInfoElbInfoList, jsii.get(self, "elbInfo"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupInfo")
    def target_group_info(
        self,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoList":
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoList", jsii.get(self, "targetGroupInfo"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupPairInfo")
    def target_group_pair_info(
        self,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoOutputReference":
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoOutputReference", jsii.get(self, "targetGroupPairInfo"))

    @builtins.property
    @jsii.member(jsii_name="elbInfoInput")
    def elb_info_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoElbInfo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoElbInfo]]], jsii.get(self, "elbInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupInfoInput")
    def target_group_info_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo"]]], jsii.get(self, "targetGroupInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupPairInfoInput")
    def target_group_pair_info_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo"], jsii.get(self, "targetGroupPairInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupLoadBalancerInfo]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupLoadBalancerInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupLoadBalancerInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a93ffce3a37d53b4584dad2e8c4f6ee3199aceaff42446ae38c634f83fd12f42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#name CodedeployDeploymentGroup#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10892aeb1acd7ae95e7c07c165e75ec5201ccd018af58281678db34908d94648)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#name CodedeployDeploymentGroup#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__739ef9f48db93a94f7cb36c9a634982fe414c31543ea229dcd186de1d29def21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4c07d65f1d528b50094cf52e0f5cdbf6800c1b6ac3c3912e87adbf3407d5473)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6ffd39b32aad199ebe12f3dbe6f63388b1c75670222e6f336e484d4ec3a2a78)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43fb727b567f2d67d0f70c8cba304f391ef4a8e5d9623ecc05bffb5103907587)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95a0066ef1b54aab01c060774a386b0444ee30a94c65b9b9dfe820d8aa59fc4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d18532580a2c05ade9ad1400e0dc1dffb17c8de36889d1437ddfc45ec59b6b97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95a5458dabcf32fde4f8e9dc1429e5d0475e49f53fa31501a2aa7fb74b003bdd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3447f6e20fb1371b982e8fc2c5659322a59cc3cb492e6b7ab92dceefbd761f34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd148558c3f0f4ed5794a300a118c562b6894f71f72c4a6c2829993999d09cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo",
    jsii_struct_bases=[],
    name_mapping={
        "prod_traffic_route": "prodTrafficRoute",
        "target_group": "targetGroup",
        "test_traffic_route": "testTrafficRoute",
    },
)
class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo:
    def __init__(
        self,
        *,
        prod_traffic_route: typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute", typing.Dict[builtins.str, typing.Any]],
        target_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup", typing.Dict[builtins.str, typing.Any]]]],
        test_traffic_route: typing.Optional[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param prod_traffic_route: prod_traffic_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#prod_traffic_route CodedeployDeploymentGroup#prod_traffic_route}
        :param target_group: target_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#target_group CodedeployDeploymentGroup#target_group}
        :param test_traffic_route: test_traffic_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#test_traffic_route CodedeployDeploymentGroup#test_traffic_route}
        '''
        if isinstance(prod_traffic_route, dict):
            prod_traffic_route = CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute(**prod_traffic_route)
        if isinstance(test_traffic_route, dict):
            test_traffic_route = CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute(**test_traffic_route)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c57780b8caeee93b38a6e66150d896a8d9f0b7f0a0c23613eb026eb6b2dca8)
            check_type(argname="argument prod_traffic_route", value=prod_traffic_route, expected_type=type_hints["prod_traffic_route"])
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
            check_type(argname="argument test_traffic_route", value=test_traffic_route, expected_type=type_hints["test_traffic_route"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prod_traffic_route": prod_traffic_route,
            "target_group": target_group,
        }
        if test_traffic_route is not None:
            self._values["test_traffic_route"] = test_traffic_route

    @builtins.property
    def prod_traffic_route(
        self,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute":
        '''prod_traffic_route block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#prod_traffic_route CodedeployDeploymentGroup#prod_traffic_route}
        '''
        result = self._values.get("prod_traffic_route")
        assert result is not None, "Required property 'prod_traffic_route' is missing"
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute", result)

    @builtins.property
    def target_group(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup"]]:
        '''target_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#target_group CodedeployDeploymentGroup#target_group}
        '''
        result = self._values.get("target_group")
        assert result is not None, "Required property 'target_group' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup"]], result)

    @builtins.property
    def test_traffic_route(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute"]:
        '''test_traffic_route block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#test_traffic_route CodedeployDeploymentGroup#test_traffic_route}
        '''
        result = self._values.get("test_traffic_route")
        return typing.cast(typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__869a224bc76979306adf7b45faf455e226a802b05cde5d2c85f53c863d2352ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProdTrafficRoute")
    def put_prod_traffic_route(
        self,
        *,
        listener_arns: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param listener_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#listener_arns CodedeployDeploymentGroup#listener_arns}.
        '''
        value = CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute(
            listener_arns=listener_arns
        )

        return typing.cast(None, jsii.invoke(self, "putProdTrafficRoute", [value]))

    @jsii.member(jsii_name="putTargetGroup")
    def put_target_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83084809db2b90f2259800567865a3fe03219845d21ec238b76647f5cf55ba79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargetGroup", [value]))

    @jsii.member(jsii_name="putTestTrafficRoute")
    def put_test_traffic_route(
        self,
        *,
        listener_arns: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param listener_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#listener_arns CodedeployDeploymentGroup#listener_arns}.
        '''
        value = CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute(
            listener_arns=listener_arns
        )

        return typing.cast(None, jsii.invoke(self, "putTestTrafficRoute", [value]))

    @jsii.member(jsii_name="resetTestTrafficRoute")
    def reset_test_traffic_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTestTrafficRoute", []))

    @builtins.property
    @jsii.member(jsii_name="prodTrafficRoute")
    def prod_traffic_route(
        self,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRouteOutputReference":
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRouteOutputReference", jsii.get(self, "prodTrafficRoute"))

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(
        self,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupList":
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupList", jsii.get(self, "targetGroup"))

    @builtins.property
    @jsii.member(jsii_name="testTrafficRoute")
    def test_traffic_route(
        self,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRouteOutputReference":
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRouteOutputReference", jsii.get(self, "testTrafficRoute"))

    @builtins.property
    @jsii.member(jsii_name="prodTrafficRouteInput")
    def prod_traffic_route_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute"], jsii.get(self, "prodTrafficRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupInput")
    def target_group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup"]]], jsii.get(self, "targetGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="testTrafficRouteInput")
    def test_traffic_route_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute"]:
        return typing.cast(typing.Optional["CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute"], jsii.get(self, "testTrafficRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ab4ee59dc74e2b6a8d15ccc384508235ac75f70dc29f2bbbdf19b6b8a3af98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute",
    jsii_struct_bases=[],
    name_mapping={"listener_arns": "listenerArns"},
)
class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute:
    def __init__(self, *, listener_arns: typing.Sequence[builtins.str]) -> None:
        '''
        :param listener_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#listener_arns CodedeployDeploymentGroup#listener_arns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__109e8649b25a2447a67a7ed8cfe4da222fb3f63103e96c8efeb25efe079b9bed)
            check_type(argname="argument listener_arns", value=listener_arns, expected_type=type_hints["listener_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "listener_arns": listener_arns,
        }

    @builtins.property
    def listener_arns(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#listener_arns CodedeployDeploymentGroup#listener_arns}.'''
        result = self._values.get("listener_arns")
        assert result is not None, "Required property 'listener_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRouteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__588e934fe39211fb9057834654ffbb6bc872c3b3fd6468578f7b21078ad76672)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="listenerArnsInput")
    def listener_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "listenerArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="listenerArns")
    def listener_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "listenerArns"))

    @listener_arns.setter
    def listener_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0213b933157ed0a2fa90667a1243451ead53f1c465b9ff81919117d7444e2cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listenerArns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bb89e5454dc1e80ee31c1ef77f71e8e620e78a13fa7a576e8ce6bac42335db6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#name CodedeployDeploymentGroup#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6496684b4b59d57a44c541a1c9ab820b163c3f2c99cb544fa20b76bfa4152fd1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#name CodedeployDeploymentGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4129a2e7e021f865c5ccc0831581a1a04f39aa273c2378050fbbbcef024ecce0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c3931c7987466dc4f119e025e44ec3df2b1a1f55ca6b9345aeedb8f4d720bab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c091ccd69263a6c6f4224bf45e4511e7c85b9dbff4a10e951ba2b890ece335)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84511096b388cb22e41b88d76ae2abccb10d52f50662eac9c72f9341552abfcf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06271e1fd4585c2434d4f4fd8fe0e207f2f4761b5853783a353f466c8bbaa80c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e98eccde3d0401f8be43ead7866529cfa9906b40d64f3d0eae996008d0a7605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c53f8e330cb902ece017735aa175e7b89c15b3d8a00d7bcd1c3118afe010571d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c0415c50b92d96065dc7c891bfda565050e545a948b66c0295e24ea71eb7cf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3adb43529aca8cdb5543bcf5e1e1ff6f6d3e7971338811e193126a3cd71b72d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute",
    jsii_struct_bases=[],
    name_mapping={"listener_arns": "listenerArns"},
)
class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute:
    def __init__(self, *, listener_arns: typing.Sequence[builtins.str]) -> None:
        '''
        :param listener_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#listener_arns CodedeployDeploymentGroup#listener_arns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6858ea7ec90441f9a660cc1b091175006a2224fb8210b441c53cec8f04df436f)
            check_type(argname="argument listener_arns", value=listener_arns, expected_type=type_hints["listener_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "listener_arns": listener_arns,
        }

    @builtins.property
    def listener_arns(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#listener_arns CodedeployDeploymentGroup#listener_arns}.'''
        result = self._values.get("listener_arns")
        assert result is not None, "Required property 'listener_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRouteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1304a54d7588c2fb285697542a3aa9745165787175af23ec9841d3e59f60d69b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="listenerArnsInput")
    def listener_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "listenerArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="listenerArns")
    def listener_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "listenerArns"))

    @listener_arns.setter
    def listener_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9707de1ff39d2ebf346d48640a8e167304672919fae13310cd3da659c0737862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listenerArns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute]:
        return typing.cast(typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6dc04a6a59ce2df0dd9aa4668eeea6747724fdb0b0eb2aa5c0c0545bb6f0302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupOnPremisesInstanceTagFilter",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "type": "type", "value": "value"},
)
class CodedeployDeploymentGroupOnPremisesInstanceTagFilter:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#key CodedeployDeploymentGroup#key}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#type CodedeployDeploymentGroup#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#value CodedeployDeploymentGroup#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0fa86463e4a0d0c74f958c9116b731fbb3e76b5ced2dea220c30a0f229808ce)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#key CodedeployDeploymentGroup#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#type CodedeployDeploymentGroup#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#value CodedeployDeploymentGroup#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupOnPremisesInstanceTagFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupOnPremisesInstanceTagFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupOnPremisesInstanceTagFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b97c70cac5e101d1da2b7958ee35520641a0db190ec00a5f49aece15141eb968)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodedeployDeploymentGroupOnPremisesInstanceTagFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3eea6707ab3d0b0596d52fd962686a97e61887f4b5293886f7f5ba58f660336)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodedeployDeploymentGroupOnPremisesInstanceTagFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce12c9ee5f4b4c08ae9803fb2f78b32d9c2a009ead4c6da720fd88d281bd98f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aea40a32e4f043306cbe4dceb1b37949b4b33c5c7045e9ba42480f4dc4eaac3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ca0d289b493f2cfedcf8037fecdc4f6c33ade40ed07a335c866355cc2db880f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupOnPremisesInstanceTagFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupOnPremisesInstanceTagFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupOnPremisesInstanceTagFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffb43120a68cca4a5af70d2468d9deb8c80313c0a1df56cc537ff3741f644033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupOnPremisesInstanceTagFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupOnPremisesInstanceTagFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec8816fd28f04164aa537a709fff125085a6759259c941100e2b0e3441d5a205)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b6e1812d1d4f5d77775f22604becd6c24af28320383307cd4b0676a6e6aea11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6229e57af5696875f7f7dc1c6f135465614f63f903d40f1d56602c02f3ac9cde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d097ce9ec5f9825076dc193cd0a38c3bf049878517c221d13ff5a3807d4e0cf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupOnPremisesInstanceTagFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupOnPremisesInstanceTagFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupOnPremisesInstanceTagFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ad57e475df2f25bfa18a50a908693aeb841b441d41a932c100b84fbc35cfaa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupTriggerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "trigger_events": "triggerEvents",
        "trigger_name": "triggerName",
        "trigger_target_arn": "triggerTargetArn",
    },
)
class CodedeployDeploymentGroupTriggerConfiguration:
    def __init__(
        self,
        *,
        trigger_events: typing.Sequence[builtins.str],
        trigger_name: builtins.str,
        trigger_target_arn: builtins.str,
    ) -> None:
        '''
        :param trigger_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#trigger_events CodedeployDeploymentGroup#trigger_events}.
        :param trigger_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#trigger_name CodedeployDeploymentGroup#trigger_name}.
        :param trigger_target_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#trigger_target_arn CodedeployDeploymentGroup#trigger_target_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__838d9e588738572300e374dbceaebc33778768e7c4ade1cc66644748f01dd922)
            check_type(argname="argument trigger_events", value=trigger_events, expected_type=type_hints["trigger_events"])
            check_type(argname="argument trigger_name", value=trigger_name, expected_type=type_hints["trigger_name"])
            check_type(argname="argument trigger_target_arn", value=trigger_target_arn, expected_type=type_hints["trigger_target_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trigger_events": trigger_events,
            "trigger_name": trigger_name,
            "trigger_target_arn": trigger_target_arn,
        }

    @builtins.property
    def trigger_events(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#trigger_events CodedeployDeploymentGroup#trigger_events}.'''
        result = self._values.get("trigger_events")
        assert result is not None, "Required property 'trigger_events' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def trigger_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#trigger_name CodedeployDeploymentGroup#trigger_name}.'''
        result = self._values.get("trigger_name")
        assert result is not None, "Required property 'trigger_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_target_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_group#trigger_target_arn CodedeployDeploymentGroup#trigger_target_arn}.'''
        result = self._values.get("trigger_target_arn")
        assert result is not None, "Required property 'trigger_target_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentGroupTriggerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentGroupTriggerConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupTriggerConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e85dffcbd74a33fb4c95f8a63ee3e37abc511be3c02d4af104462ead57aa46d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodedeployDeploymentGroupTriggerConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e60f615ec5bb7ac53c3f752355682dc148e6172608aa78d7e56e159dc1e68ce8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodedeployDeploymentGroupTriggerConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c99297a9551f100435570b4ba00002728a1e1463d80c96ca13e9afbf795fd08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2499a73b97397bff7a46309522430c9951b40ca470c2e8d3cd8353719c102d94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2bf8839c058d24f262dff1c08919c1697244a5415169fe772144bf24ba84a80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupTriggerConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupTriggerConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupTriggerConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0176a4f8122bdfd55efbdb7be1a3012aae0d0e1c0a7a224ab1408f9db122691a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentGroupTriggerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentGroup.CodedeployDeploymentGroupTriggerConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93f4e4eb28e08eb0d439961a10ea3654a43057e3dd5d7c471d2215b4ced67498)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="triggerEventsInput")
    def trigger_events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "triggerEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerNameInput")
    def trigger_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerTargetArnInput")
    def trigger_target_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerTargetArnInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerEvents")
    def trigger_events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "triggerEvents"))

    @trigger_events.setter
    def trigger_events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f6382580d65f44296fd3c6713d5a12482c40b18699b49b81dc93a0ecaf2b91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerName")
    def trigger_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerName"))

    @trigger_name.setter
    def trigger_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e8be650a757af364fcd3a566c80d27a1dd9a740d380a8f53898a4662e7f745d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerTargetArn")
    def trigger_target_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerTargetArn"))

    @trigger_target_arn.setter
    def trigger_target_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5464da6e56c158993e530a193b795bf2ad1eed32fe6a881684e3e72d3f332fdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerTargetArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupTriggerConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupTriggerConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupTriggerConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__511911898f674828c3139c428fb115ecce1cd89b2a72b4d1f7ffc49fd004a015)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CodedeployDeploymentGroup",
    "CodedeployDeploymentGroupAlarmConfiguration",
    "CodedeployDeploymentGroupAlarmConfigurationOutputReference",
    "CodedeployDeploymentGroupAutoRollbackConfiguration",
    "CodedeployDeploymentGroupAutoRollbackConfigurationOutputReference",
    "CodedeployDeploymentGroupBlueGreenDeploymentConfig",
    "CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption",
    "CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOptionOutputReference",
    "CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption",
    "CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOptionOutputReference",
    "CodedeployDeploymentGroupBlueGreenDeploymentConfigOutputReference",
    "CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess",
    "CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccessOutputReference",
    "CodedeployDeploymentGroupConfig",
    "CodedeployDeploymentGroupDeploymentStyle",
    "CodedeployDeploymentGroupDeploymentStyleOutputReference",
    "CodedeployDeploymentGroupEc2TagFilter",
    "CodedeployDeploymentGroupEc2TagFilterList",
    "CodedeployDeploymentGroupEc2TagFilterOutputReference",
    "CodedeployDeploymentGroupEc2TagSet",
    "CodedeployDeploymentGroupEc2TagSetEc2TagFilter",
    "CodedeployDeploymentGroupEc2TagSetEc2TagFilterList",
    "CodedeployDeploymentGroupEc2TagSetEc2TagFilterOutputReference",
    "CodedeployDeploymentGroupEc2TagSetList",
    "CodedeployDeploymentGroupEc2TagSetOutputReference",
    "CodedeployDeploymentGroupEcsService",
    "CodedeployDeploymentGroupEcsServiceOutputReference",
    "CodedeployDeploymentGroupLoadBalancerInfo",
    "CodedeployDeploymentGroupLoadBalancerInfoElbInfo",
    "CodedeployDeploymentGroupLoadBalancerInfoElbInfoList",
    "CodedeployDeploymentGroupLoadBalancerInfoElbInfoOutputReference",
    "CodedeployDeploymentGroupLoadBalancerInfoOutputReference",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoList",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfoOutputReference",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoOutputReference",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRouteOutputReference",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupList",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupOutputReference",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute",
    "CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRouteOutputReference",
    "CodedeployDeploymentGroupOnPremisesInstanceTagFilter",
    "CodedeployDeploymentGroupOnPremisesInstanceTagFilterList",
    "CodedeployDeploymentGroupOnPremisesInstanceTagFilterOutputReference",
    "CodedeployDeploymentGroupTriggerConfiguration",
    "CodedeployDeploymentGroupTriggerConfigurationList",
    "CodedeployDeploymentGroupTriggerConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__b4966d5ccbabdbcbbc2521d95655c311099840b2bd9de28b051f7a7e76584506(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    app_name: builtins.str,
    deployment_group_name: builtins.str,
    service_role_arn: builtins.str,
    alarm_configuration: typing.Optional[typing.Union[CodedeployDeploymentGroupAlarmConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_rollback_configuration: typing.Optional[typing.Union[CodedeployDeploymentGroupAutoRollbackConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    autoscaling_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    blue_green_deployment_config: typing.Optional[typing.Union[CodedeployDeploymentGroupBlueGreenDeploymentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_config_name: typing.Optional[builtins.str] = None,
    deployment_style: typing.Optional[typing.Union[CodedeployDeploymentGroupDeploymentStyle, typing.Dict[builtins.str, typing.Any]]] = None,
    ec2_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ec2_tag_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagSet, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ecs_service: typing.Optional[typing.Union[CodedeployDeploymentGroupEcsService, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancer_info: typing.Optional[typing.Union[CodedeployDeploymentGroupLoadBalancerInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    on_premises_instance_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupOnPremisesInstanceTagFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    outdated_instances_strategy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_hook_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    trigger_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupTriggerConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__00f2f4f75d186365a586bcca5b342c8961b1e29e1959f84c162f460e52256a02(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ee5b23ed8dc76afd8422c65b9b475b66c437b38232816b4182f977681ac756(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5b08b862e66cd2ebee51957c288fabc116d978239bd6c552a0a337cdc122d6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagSet, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cdfcd1a37c3a764d056fa519501f4a900086783e516e748d601118dfe856744(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupOnPremisesInstanceTagFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74aeb02cb491ee9f4320e0804f8e937f2498b81b117220a3e9584d304edba48d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupTriggerConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebdac24272931d293d7d288284be40016291b13adc1e0b5ab9cc97fa96896c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c176f8bb62f87bcad224cf36fd3b508ed1239775e052e3b97649cfae0508e767(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828aef8734de6f6e22a08d07a67357333a94276a67008688136f8488bbeb52de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc81e745351105adc1647386897100ff034be1b7f2cba0d56d948d0cde422d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d865cc35f995bf13111409a6ba4c3e90fb182b68c67a4f2ee98abb37aef5a8e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf1a5ae66bc26ad1a35be6a6f627408d7a7ac555543cbab94d39bb93578abd70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80030f017678f4a46a6ac3ea4024e64158dc1c3995a767d262625b6fd0af11e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b0734ff37d9fc9354196e139f2e3045b9f1c691becdf0a96496300194baebf(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afad902f7eb76c7afcd470e23b78b22d4d6aa68174c2abe5488fdbb2dea30d69(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d84394e1010636ed0faeb54cfebe102f159a87b620fbde53f8e8939329ae9e36(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43adba8b8a5c016f1be62f484e83f1624e6aeeaae069eb79fb0e8adf1b4f733c(
    *,
    alarms: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ignore_poll_alarm_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc4073362b5098ae2bcf5e765ee0a1fd9ce21f0eefc7ae2d7b5a5a645c8c15f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ecd171ffd4a615248a2bdce4e0d61881c42e35574355f2d82d0b8f22e3176a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d13e82a520163e3202a2f91ee07f4cc64047f09c8b18d6ee7206c796ce3180(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82120c79b7524e01ecd4d6da302875e874f2592094d15d583d042c2e64f1bdf5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb7bd91e7be038a4435d03dd78d22fd454442efc0544d0b2086161c8e3ca21e(
    value: typing.Optional[CodedeployDeploymentGroupAlarmConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa42a1d6ba822b9079166a9a68a25a2de0b4779a57f8b7b7254b1bc313a743f(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    events: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18ad3947c17d9f2965cefd10dd5c410f3db0be15e1fa8f04ff76f5828f943c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6424b37bedff30a85c5d2db72683c3e95657467b5446429f024073b697f15e05(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c767a13133d810f456feba7be4bb7d0a08e6fedfc79263b917b0a68adcdf68(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b1ee3309ec8b078951394cc20e6db5128f9f860b29757d26a1603bd8eba27b(
    value: typing.Optional[CodedeployDeploymentGroupAutoRollbackConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad808aa10c35f06fd44e2f136e9ce6e8f62a1ebf4e49ea7098dbe6b17d7f1d8f(
    *,
    deployment_ready_option: typing.Optional[typing.Union[CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption, typing.Dict[builtins.str, typing.Any]]] = None,
    green_fleet_provisioning_option: typing.Optional[typing.Union[CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption, typing.Dict[builtins.str, typing.Any]]] = None,
    terminate_blue_instances_on_deployment_success: typing.Optional[typing.Union[CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2e6dbaa67308c9ddec15ad272f4e53b79164f9015630754e219d30a87a3200d(
    *,
    action_on_timeout: typing.Optional[builtins.str] = None,
    wait_time_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__564a02f40c812a433b50221f968f9496a5ac800bb149f95dde03d6ce5126a780(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b3c30d530e65c0109bd9931737b184b91ca47d8a8e2dd4ef31ba340a04b288(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae557a3f137e418579f28fcf979bca0e9619ba1cd454fdacda9e9c2277d834b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f66861e3ab7914f6dc521545f5acb72d10f958d021c0819f59e87759e44f6e3(
    value: typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c0de3ab024894b4fd2af378912898747b48c2f23caad68e7fd7992b52b98f62(
    *,
    action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237428eb9b2bb1da8953dc8c98f0419cad4aca4fe6e9518a39d1d2a86a5f708a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8011603bbc81750d3b3795bbb6cc3a656ef64f9e8fad8ad988a21b134074d18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3009a366516b5375ab47204d228f9d62a3b12cabd2d00e3cb82a7d6c67cbd406(
    value: typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c091c88d8d4886852d7b03777d92f44891530626d0a55d607a3ea1cef3d2eb1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ad71baad3ad5e556a627e7f6239d184cd77c0e6d26d738f29c4f3f16d8cb22(
    value: typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0626fcdb819dc69e998ec69563df6862f94c40ad7266de1d003c86411fc7adb2(
    *,
    action: typing.Optional[builtins.str] = None,
    termination_wait_time_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10cc4ab398ec68d517c023b5edd8b1034e70a1acb2216c19f750edab45a3825(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9bffc08efc9078f27110a4a1e0a57074eeab7a5717e46d62f145818f1a2b90f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7250bde1261fa6b03814db337892fffa5489c6d2a9a680acba08a789a26ece9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce8b3265581d7b3624a872b7a40b1ee386b6f3bd6a5323b4c9c6f807bf3eea6(
    value: typing.Optional[CodedeployDeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70a08659a2c5dfa1a9dc7747a0f987940cec65f408e079759662082b32e0fc62(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_name: builtins.str,
    deployment_group_name: builtins.str,
    service_role_arn: builtins.str,
    alarm_configuration: typing.Optional[typing.Union[CodedeployDeploymentGroupAlarmConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_rollback_configuration: typing.Optional[typing.Union[CodedeployDeploymentGroupAutoRollbackConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    autoscaling_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    blue_green_deployment_config: typing.Optional[typing.Union[CodedeployDeploymentGroupBlueGreenDeploymentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_config_name: typing.Optional[builtins.str] = None,
    deployment_style: typing.Optional[typing.Union[CodedeployDeploymentGroupDeploymentStyle, typing.Dict[builtins.str, typing.Any]]] = None,
    ec2_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ec2_tag_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagSet, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ecs_service: typing.Optional[typing.Union[CodedeployDeploymentGroupEcsService, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancer_info: typing.Optional[typing.Union[CodedeployDeploymentGroupLoadBalancerInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    on_premises_instance_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupOnPremisesInstanceTagFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    outdated_instances_strategy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_hook_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    trigger_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupTriggerConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaeccf9adf3f39a435a03b49a74b2496aa96b9826fdd136f668ef12ab57679c0(
    *,
    deployment_option: typing.Optional[builtins.str] = None,
    deployment_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56dc2e01a3a32e73e281298b55d55f51df7b96862f083fc29dd9fab4ee1fed83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6d32f8bd2533ff404c74a4cd534bc812eb04cb6fa438594df69553ec744cab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c70dc5918fe4b4e6decbf858a2a3de3bd8395bb9f87080bb61fc58ba071fd25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43e5fdc9da2ff804101c11f250beb37356264b45d1478203d10f3fb9f242622(
    value: typing.Optional[CodedeployDeploymentGroupDeploymentStyle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9a27d72bf01985f0d0e200833c0cb4a8b1967d3fee497803b689ec30b35457(
    *,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae88845855f664f08412ef654c47b1a3a3b6b47e2af1020c0cac7bf85d38d19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21cc3e51f4a9c61a18087e19a5e6afa5aaad67814c2372c88bb4ff6ba18eb70b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97d17ce3f53f45ad203f9e3dfcd7db756b5fa56902e72b925aa8d4444defe44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3405c5aeaecc11e37f9e007c7ff57eb37c319caa3e19635e5647ed64ae9702e9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774a78acd087220082adb2fd75f45927249fc9a4c48a247a81771d854c5fa489(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acc23c39530268c865a2477113ed029b98787ca7595abc2372fe99f86be650b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43f3c5b5166126889f98bd585cdb4036b18966928c0088b8b01ee56b8966efc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d592a0ffea59afb23a81b933028f0326906b137354c8fb30cdfd75dfa0c7110a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5237a618fe4d049ca71b56e42eb4848f4a858968e9a2cb1f979c6baa2ddae937(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6448253a38716b9852ba8b16b38c166589bbdb03825084dbb9cfd1a1c6df24b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3fdb4aca37606e88a54b1af2c00b7a3afef7218e6ea8292c168e137457305c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc0e14ad179a85e874a651bdabb5f4f8df26a7f83f0017826c15e7229dd51b4(
    *,
    ec2_tag_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagSetEc2TagFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0fa3d898a78c742305d77d110cc77830a7dffa27e5ee4db723b98a2fbdc38e(
    *,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6cd42c87887fbba8a32df22bcb1f3ce2dba7575dc8a9db2c1ba9d6956c416c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80af3974a0eb558ed6cfb1e84411b20a551f748ee03318cf417221d3624bed8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0683da8c5e5ee29fa7d71e7bc9999d77d11e1e35bbcb2ad2f9ef7ab958daea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9691809bcee967e8d22c28a53bf11ed1516bac0cfd3288fde7c1d6dbef9f8ff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067f4aba3a9d441143d85faac92624be048e0c5614bdf14fd2b9626f37c27cc3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff419bcb7bfab7c6ccd9ce998a2582099cb27bad7861b8cf017332845de42984(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSetEc2TagFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52a3820866403722742df7b39dc300e7f228f6b168aba7a8ce5ca3e42a4f2b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905d89b5d614418fac92a6d35cb93056182a8bb4626003762ac2cbeae000a97b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb436ef94e4ccf90ccf39ffec5ac552080f0a64d82aee706ca17f562acc9e46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2ab22a78886a72de6fe578f61b8dc97e1c80ec094adec884cf3383252bc68e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f164b91c70009461701b8e7147594f055427e60bc0312fe5cb16f14858ebe34(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagSetEc2TagFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c663f402f9cfe929def8f2dd7e85bcf439d944869fa673c67b95fc09eef87bb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d907e498f37fd2a5e49c9098aa0ee094591bdde2ae48060e1f0382f03a79ba(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c1674bd7c8264d43d24c94a3782c59dfe64169040d933973e148a05fc8472a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c64083212f5855ccffd3b9d89e0539450e7a085086389c35609641e90b0334(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c4b352f3352920f6967791d60e9fde2a621ee2a1e3ca29182f45ba0c18dbfa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0c604f387eca41a492e1bfbb727894175cc3d84150cb5118730d5de8cb772bd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupEc2TagSet]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52cf9362bb2a15218c9dfc5d79c3afae2b6137ece85013abb5c366130bb54896(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fbf0017b7a12660406bfdd050cb3b465cafa998715a1022ab37d5f996419797(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupEc2TagSetEc2TagFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4217c6a028762d627b79d984896745c1f3f2cbf595e7b74bcaf90da3775bc0fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupEc2TagSet]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c865915a56ad1e94265800d2fe74e95e30b19a401a024ab4cb8cb82deaeaa465(
    *,
    cluster_name: builtins.str,
    service_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcec2d7996557f0462dc29eb9e8532ea97ea85466cac7c08e13210712d5b4db7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5225433566c5d33922df2db664b1cb4b3eb55ed6af87627bf0a0510866149b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d749a78f40961840bfb147958a8524698774590b3dc2f923dc878ce77b3bf2b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb532c161dc5732f1db41a84926d6c1d52f4e0547b7218f4b9fc32f2c150a7e4(
    value: typing.Optional[CodedeployDeploymentGroupEcsService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a56f13d41b750d84e25748655bf373c202a65324c39c3d65749fb8ea3a81efc4(
    *,
    elb_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoElbInfo, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_group_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_group_pair_info: typing.Optional[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7be0610f5c864934a24e053b3dc3e1fb312869caeed73c996554dadd71ea5a2(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05edd99cde1bd57fb3e17f98fdc166cb17459f7e8cad3ca0e2d9b67d65aeda06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e22c9b0536ed8865be1ff7f54caa98a6803bcd0a8532f37874cd28d74f251f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f651986725a24364827dad9c2b00b5ee07eca414a6e47355950b666c7f5cd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca1a56ff0bc2923e9777f791ba67c1c9829b3128119abd90e3ecd7308781ce12(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3390166e62c07d932973b7647faf63c0b920477108bd4313064a03f1577afc8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ec1fc7a2137d26b8c9a86b4519eb5c0d5a22cb5dbe92101061e9f616820781(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoElbInfo]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__452719bbca2a22ff03967a40394a559ab930dee5fc13f44893da639c7ff05d57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae01b561d39a55e8968a315766e389e14f858ea418c43f7687ee627846e422c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8068c12ffcabda9d8bb559cfa600d8130fedcf793c823c9e9f1400b76108d36(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoElbInfo]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf1fee2db0673b8106950036d8e4eeba5eed51ed2eacb411353af9961feb8d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd74c91e1768744ca160e7f729e12f6eeb71a84112b527b344eed1a678e98233(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoElbInfo, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82af5554eaf162b2045868d69ec23d688456f6d766028f6c90e42d6e6100ad0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93ffce3a37d53b4584dad2e8c4f6ee3199aceaff42446ae38c634f83fd12f42(
    value: typing.Optional[CodedeployDeploymentGroupLoadBalancerInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10892aeb1acd7ae95e7c07c165e75ec5201ccd018af58281678db34908d94648(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739ef9f48db93a94f7cb36c9a634982fe414c31543ea229dcd186de1d29def21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c07d65f1d528b50094cf52e0f5cdbf6800c1b6ac3c3912e87adbf3407d5473(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ffd39b32aad199ebe12f3dbe6f63388b1c75670222e6f336e484d4ec3a2a78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fb727b567f2d67d0f70c8cba304f391ef4a8e5d9623ecc05bffb5103907587(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95a0066ef1b54aab01c060774a386b0444ee30a94c65b9b9dfe820d8aa59fc4b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d18532580a2c05ade9ad1400e0dc1dffb17c8de36889d1437ddfc45ec59b6b97(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95a5458dabcf32fde4f8e9dc1429e5d0475e49f53fa31501a2aa7fb74b003bdd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3447f6e20fb1371b982e8fc2c5659322a59cc3cb492e6b7ab92dceefbd761f34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd148558c3f0f4ed5794a300a118c562b6894f71f72c4a6c2829993999d09cc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoTargetGroupInfo]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c57780b8caeee93b38a6e66150d896a8d9f0b7f0a0c23613eb026eb6b2dca8(
    *,
    prod_traffic_route: typing.Union[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute, typing.Dict[builtins.str, typing.Any]],
    target_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup, typing.Dict[builtins.str, typing.Any]]]],
    test_traffic_route: typing.Optional[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__869a224bc76979306adf7b45faf455e226a802b05cde5d2c85f53c863d2352ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83084809db2b90f2259800567865a3fe03219845d21ec238b76647f5cf55ba79(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ab4ee59dc74e2b6a8d15ccc384508235ac75f70dc29f2bbbdf19b6b8a3af98(
    value: typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109e8649b25a2447a67a7ed8cfe4da222fb3f63103e96c8efeb25efe079b9bed(
    *,
    listener_arns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588e934fe39211fb9057834654ffbb6bc872c3b3fd6468578f7b21078ad76672(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0213b933157ed0a2fa90667a1243451ead53f1c465b9ff81919117d7444e2cc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb89e5454dc1e80ee31c1ef77f71e8e620e78a13fa7a576e8ce6bac42335db6(
    value: typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRoute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6496684b4b59d57a44c541a1c9ab820b163c3f2c99cb544fa20b76bfa4152fd1(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4129a2e7e021f865c5ccc0831581a1a04f39aa273c2378050fbbbcef024ecce0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c3931c7987466dc4f119e025e44ec3df2b1a1f55ca6b9345aeedb8f4d720bab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c091ccd69263a6c6f4224bf45e4511e7c85b9dbff4a10e951ba2b890ece335(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84511096b388cb22e41b88d76ae2abccb10d52f50662eac9c72f9341552abfcf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06271e1fd4585c2434d4f4fd8fe0e207f2f4761b5853783a353f466c8bbaa80c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e98eccde3d0401f8be43ead7866529cfa9906b40d64f3d0eae996008d0a7605(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c53f8e330cb902ece017735aa175e7b89c15b3d8a00d7bcd1c3118afe010571d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c0415c50b92d96065dc7c891bfda565050e545a948b66c0295e24ea71eb7cf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3adb43529aca8cdb5543bcf5e1e1ff6f6d3e7971338811e193126a3cd71b72d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroup]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6858ea7ec90441f9a660cc1b091175006a2224fb8210b441c53cec8f04df436f(
    *,
    listener_arns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1304a54d7588c2fb285697542a3aa9745165787175af23ec9841d3e59f60d69b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9707de1ff39d2ebf346d48640a8e167304672919fae13310cd3da659c0737862(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6dc04a6a59ce2df0dd9aa4668eeea6747724fdb0b0eb2aa5c0c0545bb6f0302(
    value: typing.Optional[CodedeployDeploymentGroupLoadBalancerInfoTargetGroupPairInfoTestTrafficRoute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0fa86463e4a0d0c74f958c9116b731fbb3e76b5ced2dea220c30a0f229808ce(
    *,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97c70cac5e101d1da2b7958ee35520641a0db190ec00a5f49aece15141eb968(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3eea6707ab3d0b0596d52fd962686a97e61887f4b5293886f7f5ba58f660336(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce12c9ee5f4b4c08ae9803fb2f78b32d9c2a009ead4c6da720fd88d281bd98f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea40a32e4f043306cbe4dceb1b37949b4b33c5c7045e9ba42480f4dc4eaac3e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca0d289b493f2cfedcf8037fecdc4f6c33ade40ed07a335c866355cc2db880f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb43120a68cca4a5af70d2468d9deb8c80313c0a1df56cc537ff3741f644033(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupOnPremisesInstanceTagFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec8816fd28f04164aa537a709fff125085a6759259c941100e2b0e3441d5a205(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b6e1812d1d4f5d77775f22604becd6c24af28320383307cd4b0676a6e6aea11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6229e57af5696875f7f7dc1c6f135465614f63f903d40f1d56602c02f3ac9cde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d097ce9ec5f9825076dc193cd0a38c3bf049878517c221d13ff5a3807d4e0cf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad57e475df2f25bfa18a50a908693aeb841b441d41a932c100b84fbc35cfaa2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupOnPremisesInstanceTagFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838d9e588738572300e374dbceaebc33778768e7c4ade1cc66644748f01dd922(
    *,
    trigger_events: typing.Sequence[builtins.str],
    trigger_name: builtins.str,
    trigger_target_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85dffcbd74a33fb4c95f8a63ee3e37abc511be3c02d4af104462ead57aa46d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60f615ec5bb7ac53c3f752355682dc148e6172608aa78d7e56e159dc1e68ce8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c99297a9551f100435570b4ba00002728a1e1463d80c96ca13e9afbf795fd08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2499a73b97397bff7a46309522430c9951b40ca470c2e8d3cd8353719c102d94(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2bf8839c058d24f262dff1c08919c1697244a5415169fe772144bf24ba84a80(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0176a4f8122bdfd55efbdb7be1a3012aae0d0e1c0a7a224ab1408f9db122691a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodedeployDeploymentGroupTriggerConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f4e4eb28e08eb0d439961a10ea3654a43057e3dd5d7c471d2215b4ced67498(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f6382580d65f44296fd3c6713d5a12482c40b18699b49b81dc93a0ecaf2b91(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e8be650a757af364fcd3a566c80d27a1dd9a740d380a8f53898a4662e7f745d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5464da6e56c158993e530a193b795bf2ad1eed32fe6a881684e3e72d3f332fdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511911898f674828c3139c428fb115ecce1cd89b2a72b4d1f7ffc49fd004a015(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodedeployDeploymentGroupTriggerConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

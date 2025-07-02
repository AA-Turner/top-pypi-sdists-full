r'''
# `azurerm_container_app_job`

Refer to the Terraform Registry for docs: [`azurerm_container_app_job`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job).
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


class ContainerAppJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job azurerm_container_app_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        container_app_environment_id: builtins.str,
        location: builtins.str,
        name: builtins.str,
        replica_timeout_in_seconds: jsii.Number,
        resource_group_name: builtins.str,
        template: typing.Union["ContainerAppJobTemplate", typing.Dict[builtins.str, typing.Any]],
        event_trigger_config: typing.Optional[typing.Union["ContainerAppJobEventTriggerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["ContainerAppJobIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        manual_trigger_config: typing.Optional[typing.Union["ContainerAppJobManualTriggerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        registry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobRegistry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        replica_retry_limit: typing.Optional[jsii.Number] = None,
        schedule_trigger_config: typing.Optional[typing.Union["ContainerAppJobScheduleTriggerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobSecret", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ContainerAppJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_profile_name: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job azurerm_container_app_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param container_app_environment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#container_app_environment_id ContainerAppJob#container_app_environment_id}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#location ContainerAppJob#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}.
        :param replica_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#replica_timeout_in_seconds ContainerAppJob#replica_timeout_in_seconds}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#resource_group_name ContainerAppJob#resource_group_name}.
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#template ContainerAppJob#template}
        :param event_trigger_config: event_trigger_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#event_trigger_config ContainerAppJob#event_trigger_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#id ContainerAppJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#identity ContainerAppJob#identity}
        :param manual_trigger_config: manual_trigger_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#manual_trigger_config ContainerAppJob#manual_trigger_config}
        :param registry: registry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#registry ContainerAppJob#registry}
        :param replica_retry_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#replica_retry_limit ContainerAppJob#replica_retry_limit}.
        :param schedule_trigger_config: schedule_trigger_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#schedule_trigger_config ContainerAppJob#schedule_trigger_config}
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#secret ContainerAppJob#secret}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#tags ContainerAppJob#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#timeouts ContainerAppJob#timeouts}
        :param workload_profile_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#workload_profile_name ContainerAppJob#workload_profile_name}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__662028df8d3c118a6e314382274d50cab629f275917bbcfed161936cb94a9ed2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ContainerAppJobConfig(
            container_app_environment_id=container_app_environment_id,
            location=location,
            name=name,
            replica_timeout_in_seconds=replica_timeout_in_seconds,
            resource_group_name=resource_group_name,
            template=template,
            event_trigger_config=event_trigger_config,
            id=id,
            identity=identity,
            manual_trigger_config=manual_trigger_config,
            registry=registry,
            replica_retry_limit=replica_retry_limit,
            schedule_trigger_config=schedule_trigger_config,
            secret=secret,
            tags=tags,
            timeouts=timeouts,
            workload_profile_name=workload_profile_name,
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
        '''Generates CDKTF code for importing a ContainerAppJob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ContainerAppJob to import.
        :param import_from_id: The id of the existing ContainerAppJob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ContainerAppJob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc3b69d29847fe38ba62b081905d0c3506ea7426d936ad06b009cb7b96aab3a6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEventTriggerConfig")
    def put_event_trigger_config(
        self,
        *,
        parallelism: typing.Optional[jsii.Number] = None,
        replica_completion_count: typing.Optional[jsii.Number] = None,
        scale: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobEventTriggerConfigScale", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param parallelism: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#parallelism ContainerAppJob#parallelism}.
        :param replica_completion_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#replica_completion_count ContainerAppJob#replica_completion_count}.
        :param scale: scale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#scale ContainerAppJob#scale}
        '''
        value = ContainerAppJobEventTriggerConfig(
            parallelism=parallelism,
            replica_completion_count=replica_completion_count,
            scale=scale,
        )

        return typing.cast(None, jsii.invoke(self, "putEventTriggerConfig", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#type ContainerAppJob#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#identity_ids ContainerAppJob#identity_ids}.
        '''
        value = ContainerAppJobIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putManualTriggerConfig")
    def put_manual_trigger_config(
        self,
        *,
        parallelism: typing.Optional[jsii.Number] = None,
        replica_completion_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param parallelism: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#parallelism ContainerAppJob#parallelism}.
        :param replica_completion_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#replica_completion_count ContainerAppJob#replica_completion_count}.
        '''
        value = ContainerAppJobManualTriggerConfig(
            parallelism=parallelism, replica_completion_count=replica_completion_count
        )

        return typing.cast(None, jsii.invoke(self, "putManualTriggerConfig", [value]))

    @jsii.member(jsii_name="putRegistry")
    def put_registry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobRegistry", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e5f2641976a41c9f140904a3e4c9322f10afa781572688551afb2b84df056b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRegistry", [value]))

    @jsii.member(jsii_name="putScheduleTriggerConfig")
    def put_schedule_trigger_config(
        self,
        *,
        cron_expression: builtins.str,
        parallelism: typing.Optional[jsii.Number] = None,
        replica_completion_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cron_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#cron_expression ContainerAppJob#cron_expression}.
        :param parallelism: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#parallelism ContainerAppJob#parallelism}.
        :param replica_completion_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#replica_completion_count ContainerAppJob#replica_completion_count}.
        '''
        value = ContainerAppJobScheduleTriggerConfig(
            cron_expression=cron_expression,
            parallelism=parallelism,
            replica_completion_count=replica_completion_count,
        )

        return typing.cast(None, jsii.invoke(self, "putScheduleTriggerConfig", [value]))

    @jsii.member(jsii_name="putSecret")
    def put_secret(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobSecret", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4f745f9207cebe83e079324ab350923a8064add69870736f94b09fe5c765164)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecret", [value]))

    @jsii.member(jsii_name="putTemplate")
    def put_template(
        self,
        *,
        container: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateContainer", typing.Dict[builtins.str, typing.Any]]]],
        init_container: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateInitContainer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        volume: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateVolume", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#container ContainerAppJob#container}
        :param init_container: init_container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#init_container ContainerAppJob#init_container}
        :param volume: volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#volume ContainerAppJob#volume}
        '''
        value = ContainerAppJobTemplate(
            container=container, init_container=init_container, volume=volume
        )

        return typing.cast(None, jsii.invoke(self, "putTemplate", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#create ContainerAppJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#delete ContainerAppJob#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#read ContainerAppJob#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#update ContainerAppJob#update}.
        '''
        value = ContainerAppJobTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetEventTriggerConfig")
    def reset_event_trigger_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventTriggerConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetManualTriggerConfig")
    def reset_manual_trigger_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualTriggerConfig", []))

    @jsii.member(jsii_name="resetRegistry")
    def reset_registry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistry", []))

    @jsii.member(jsii_name="resetReplicaRetryLimit")
    def reset_replica_retry_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicaRetryLimit", []))

    @jsii.member(jsii_name="resetScheduleTriggerConfig")
    def reset_schedule_trigger_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleTriggerConfig", []))

    @jsii.member(jsii_name="resetSecret")
    def reset_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecret", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWorkloadProfileName")
    def reset_workload_profile_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkloadProfileName", []))

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
    @jsii.member(jsii_name="eventStreamEndpoint")
    def event_stream_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventStreamEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="eventTriggerConfig")
    def event_trigger_config(
        self,
    ) -> "ContainerAppJobEventTriggerConfigOutputReference":
        return typing.cast("ContainerAppJobEventTriggerConfigOutputReference", jsii.get(self, "eventTriggerConfig"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "ContainerAppJobIdentityOutputReference":
        return typing.cast("ContainerAppJobIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="manualTriggerConfig")
    def manual_trigger_config(
        self,
    ) -> "ContainerAppJobManualTriggerConfigOutputReference":
        return typing.cast("ContainerAppJobManualTriggerConfigOutputReference", jsii.get(self, "manualTriggerConfig"))

    @builtins.property
    @jsii.member(jsii_name="outboundIpAddresses")
    def outbound_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outboundIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="registry")
    def registry(self) -> "ContainerAppJobRegistryList":
        return typing.cast("ContainerAppJobRegistryList", jsii.get(self, "registry"))

    @builtins.property
    @jsii.member(jsii_name="scheduleTriggerConfig")
    def schedule_trigger_config(
        self,
    ) -> "ContainerAppJobScheduleTriggerConfigOutputReference":
        return typing.cast("ContainerAppJobScheduleTriggerConfigOutputReference", jsii.get(self, "scheduleTriggerConfig"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> "ContainerAppJobSecretList":
        return typing.cast("ContainerAppJobSecretList", jsii.get(self, "secret"))

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> "ContainerAppJobTemplateOutputReference":
        return typing.cast("ContainerAppJobTemplateOutputReference", jsii.get(self, "template"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ContainerAppJobTimeoutsOutputReference":
        return typing.cast("ContainerAppJobTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="containerAppEnvironmentIdInput")
    def container_app_environment_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerAppEnvironmentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="eventTriggerConfigInput")
    def event_trigger_config_input(
        self,
    ) -> typing.Optional["ContainerAppJobEventTriggerConfig"]:
        return typing.cast(typing.Optional["ContainerAppJobEventTriggerConfig"], jsii.get(self, "eventTriggerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["ContainerAppJobIdentity"]:
        return typing.cast(typing.Optional["ContainerAppJobIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="manualTriggerConfigInput")
    def manual_trigger_config_input(
        self,
    ) -> typing.Optional["ContainerAppJobManualTriggerConfig"]:
        return typing.cast(typing.Optional["ContainerAppJobManualTriggerConfig"], jsii.get(self, "manualTriggerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="registryInput")
    def registry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobRegistry"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobRegistry"]]], jsii.get(self, "registryInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaRetryLimitInput")
    def replica_retry_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicaRetryLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaTimeoutInSecondsInput")
    def replica_timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicaTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleTriggerConfigInput")
    def schedule_trigger_config_input(
        self,
    ) -> typing.Optional["ContainerAppJobScheduleTriggerConfig"]:
        return typing.cast(typing.Optional["ContainerAppJobScheduleTriggerConfig"], jsii.get(self, "scheduleTriggerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobSecret"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobSecret"]]], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="templateInput")
    def template_input(self) -> typing.Optional["ContainerAppJobTemplate"]:
        return typing.cast(typing.Optional["ContainerAppJobTemplate"], jsii.get(self, "templateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAppJobTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAppJobTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadProfileNameInput")
    def workload_profile_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workloadProfileNameInput"))

    @builtins.property
    @jsii.member(jsii_name="containerAppEnvironmentId")
    def container_app_environment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerAppEnvironmentId"))

    @container_app_environment_id.setter
    def container_app_environment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffdda9b0b8f28ae59e0dbb5ae1ff5fdbe0bdeabdf6e3260fe3e774e79e11aafe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerAppEnvironmentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81d33376baa89f2521719bbef2502d69679503d1aeae76716877fcd86d40779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e95027b448d97df18d5d36c5ecb6626844410788adaecac831c5ab83a077644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7f7813df2a3372425c183f58fbcefad9392f370fecdea307bc5be679f1902c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaRetryLimit")
    def replica_retry_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicaRetryLimit"))

    @replica_retry_limit.setter
    def replica_retry_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cb1be5b4a8d8e3b8cf1eb8fe293a41400aedbd04dffcc2994c2ce3b3f90bab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaRetryLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaTimeoutInSeconds")
    def replica_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicaTimeoutInSeconds"))

    @replica_timeout_in_seconds.setter
    def replica_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10fcb3912722a5c0bd247e21b14192a2ea03c076859d538dca98cf4647fac486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c27c69a6ecce62ca2e6a7673a43d0f23949cf03ee562fbea22b8764578d44d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01eaf3c0278a1a07f8c98eac807489569c1269de253101bf9b37e99dae3f2713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadProfileName")
    def workload_profile_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workloadProfileName"))

    @workload_profile_name.setter
    def workload_profile_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d7b152d6fa0b45e1bd1c0fad6a9688f920f88004030595079565965522fe62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadProfileName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "container_app_environment_id": "containerAppEnvironmentId",
        "location": "location",
        "name": "name",
        "replica_timeout_in_seconds": "replicaTimeoutInSeconds",
        "resource_group_name": "resourceGroupName",
        "template": "template",
        "event_trigger_config": "eventTriggerConfig",
        "id": "id",
        "identity": "identity",
        "manual_trigger_config": "manualTriggerConfig",
        "registry": "registry",
        "replica_retry_limit": "replicaRetryLimit",
        "schedule_trigger_config": "scheduleTriggerConfig",
        "secret": "secret",
        "tags": "tags",
        "timeouts": "timeouts",
        "workload_profile_name": "workloadProfileName",
    },
)
class ContainerAppJobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        container_app_environment_id: builtins.str,
        location: builtins.str,
        name: builtins.str,
        replica_timeout_in_seconds: jsii.Number,
        resource_group_name: builtins.str,
        template: typing.Union["ContainerAppJobTemplate", typing.Dict[builtins.str, typing.Any]],
        event_trigger_config: typing.Optional[typing.Union["ContainerAppJobEventTriggerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["ContainerAppJobIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        manual_trigger_config: typing.Optional[typing.Union["ContainerAppJobManualTriggerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        registry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobRegistry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        replica_retry_limit: typing.Optional[jsii.Number] = None,
        schedule_trigger_config: typing.Optional[typing.Union["ContainerAppJobScheduleTriggerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobSecret", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ContainerAppJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_profile_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param container_app_environment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#container_app_environment_id ContainerAppJob#container_app_environment_id}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#location ContainerAppJob#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}.
        :param replica_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#replica_timeout_in_seconds ContainerAppJob#replica_timeout_in_seconds}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#resource_group_name ContainerAppJob#resource_group_name}.
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#template ContainerAppJob#template}
        :param event_trigger_config: event_trigger_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#event_trigger_config ContainerAppJob#event_trigger_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#id ContainerAppJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#identity ContainerAppJob#identity}
        :param manual_trigger_config: manual_trigger_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#manual_trigger_config ContainerAppJob#manual_trigger_config}
        :param registry: registry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#registry ContainerAppJob#registry}
        :param replica_retry_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#replica_retry_limit ContainerAppJob#replica_retry_limit}.
        :param schedule_trigger_config: schedule_trigger_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#schedule_trigger_config ContainerAppJob#schedule_trigger_config}
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#secret ContainerAppJob#secret}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#tags ContainerAppJob#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#timeouts ContainerAppJob#timeouts}
        :param workload_profile_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#workload_profile_name ContainerAppJob#workload_profile_name}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(template, dict):
            template = ContainerAppJobTemplate(**template)
        if isinstance(event_trigger_config, dict):
            event_trigger_config = ContainerAppJobEventTriggerConfig(**event_trigger_config)
        if isinstance(identity, dict):
            identity = ContainerAppJobIdentity(**identity)
        if isinstance(manual_trigger_config, dict):
            manual_trigger_config = ContainerAppJobManualTriggerConfig(**manual_trigger_config)
        if isinstance(schedule_trigger_config, dict):
            schedule_trigger_config = ContainerAppJobScheduleTriggerConfig(**schedule_trigger_config)
        if isinstance(timeouts, dict):
            timeouts = ContainerAppJobTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba4717d45bed68bc5736e98ab7f959f24eb6d691cf657154aebf6cec39fafbd2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument container_app_environment_id", value=container_app_environment_id, expected_type=type_hints["container_app_environment_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument replica_timeout_in_seconds", value=replica_timeout_in_seconds, expected_type=type_hints["replica_timeout_in_seconds"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
            check_type(argname="argument event_trigger_config", value=event_trigger_config, expected_type=type_hints["event_trigger_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument manual_trigger_config", value=manual_trigger_config, expected_type=type_hints["manual_trigger_config"])
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
            check_type(argname="argument replica_retry_limit", value=replica_retry_limit, expected_type=type_hints["replica_retry_limit"])
            check_type(argname="argument schedule_trigger_config", value=schedule_trigger_config, expected_type=type_hints["schedule_trigger_config"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument workload_profile_name", value=workload_profile_name, expected_type=type_hints["workload_profile_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_app_environment_id": container_app_environment_id,
            "location": location,
            "name": name,
            "replica_timeout_in_seconds": replica_timeout_in_seconds,
            "resource_group_name": resource_group_name,
            "template": template,
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
        if event_trigger_config is not None:
            self._values["event_trigger_config"] = event_trigger_config
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if manual_trigger_config is not None:
            self._values["manual_trigger_config"] = manual_trigger_config
        if registry is not None:
            self._values["registry"] = registry
        if replica_retry_limit is not None:
            self._values["replica_retry_limit"] = replica_retry_limit
        if schedule_trigger_config is not None:
            self._values["schedule_trigger_config"] = schedule_trigger_config
        if secret is not None:
            self._values["secret"] = secret
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if workload_profile_name is not None:
            self._values["workload_profile_name"] = workload_profile_name

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
    def container_app_environment_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#container_app_environment_id ContainerAppJob#container_app_environment_id}.'''
        result = self._values.get("container_app_environment_id")
        assert result is not None, "Required property 'container_app_environment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#location ContainerAppJob#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replica_timeout_in_seconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#replica_timeout_in_seconds ContainerAppJob#replica_timeout_in_seconds}.'''
        result = self._values.get("replica_timeout_in_seconds")
        assert result is not None, "Required property 'replica_timeout_in_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#resource_group_name ContainerAppJob#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template(self) -> "ContainerAppJobTemplate":
        '''template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#template ContainerAppJob#template}
        '''
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast("ContainerAppJobTemplate", result)

    @builtins.property
    def event_trigger_config(
        self,
    ) -> typing.Optional["ContainerAppJobEventTriggerConfig"]:
        '''event_trigger_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#event_trigger_config ContainerAppJob#event_trigger_config}
        '''
        result = self._values.get("event_trigger_config")
        return typing.cast(typing.Optional["ContainerAppJobEventTriggerConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#id ContainerAppJob#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["ContainerAppJobIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#identity ContainerAppJob#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["ContainerAppJobIdentity"], result)

    @builtins.property
    def manual_trigger_config(
        self,
    ) -> typing.Optional["ContainerAppJobManualTriggerConfig"]:
        '''manual_trigger_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#manual_trigger_config ContainerAppJob#manual_trigger_config}
        '''
        result = self._values.get("manual_trigger_config")
        return typing.cast(typing.Optional["ContainerAppJobManualTriggerConfig"], result)

    @builtins.property
    def registry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobRegistry"]]]:
        '''registry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#registry ContainerAppJob#registry}
        '''
        result = self._values.get("registry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobRegistry"]]], result)

    @builtins.property
    def replica_retry_limit(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#replica_retry_limit ContainerAppJob#replica_retry_limit}.'''
        result = self._values.get("replica_retry_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def schedule_trigger_config(
        self,
    ) -> typing.Optional["ContainerAppJobScheduleTriggerConfig"]:
        '''schedule_trigger_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#schedule_trigger_config ContainerAppJob#schedule_trigger_config}
        '''
        result = self._values.get("schedule_trigger_config")
        return typing.cast(typing.Optional["ContainerAppJobScheduleTriggerConfig"], result)

    @builtins.property
    def secret(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobSecret"]]]:
        '''secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#secret ContainerAppJob#secret}
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobSecret"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#tags ContainerAppJob#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ContainerAppJobTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#timeouts ContainerAppJob#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ContainerAppJobTimeouts"], result)

    @builtins.property
    def workload_profile_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#workload_profile_name ContainerAppJob#workload_profile_name}.'''
        result = self._values.get("workload_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobEventTriggerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "parallelism": "parallelism",
        "replica_completion_count": "replicaCompletionCount",
        "scale": "scale",
    },
)
class ContainerAppJobEventTriggerConfig:
    def __init__(
        self,
        *,
        parallelism: typing.Optional[jsii.Number] = None,
        replica_completion_count: typing.Optional[jsii.Number] = None,
        scale: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobEventTriggerConfigScale", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param parallelism: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#parallelism ContainerAppJob#parallelism}.
        :param replica_completion_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#replica_completion_count ContainerAppJob#replica_completion_count}.
        :param scale: scale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#scale ContainerAppJob#scale}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e602c6cfccce9a0a264d4b8b0676884df0c7b3f55e9be77227e38c75a3fa229)
            check_type(argname="argument parallelism", value=parallelism, expected_type=type_hints["parallelism"])
            check_type(argname="argument replica_completion_count", value=replica_completion_count, expected_type=type_hints["replica_completion_count"])
            check_type(argname="argument scale", value=scale, expected_type=type_hints["scale"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if parallelism is not None:
            self._values["parallelism"] = parallelism
        if replica_completion_count is not None:
            self._values["replica_completion_count"] = replica_completion_count
        if scale is not None:
            self._values["scale"] = scale

    @builtins.property
    def parallelism(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#parallelism ContainerAppJob#parallelism}.'''
        result = self._values.get("parallelism")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replica_completion_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#replica_completion_count ContainerAppJob#replica_completion_count}.'''
        result = self._values.get("replica_completion_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scale(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobEventTriggerConfigScale"]]]:
        '''scale block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#scale ContainerAppJob#scale}
        '''
        result = self._values.get("scale")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobEventTriggerConfigScale"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobEventTriggerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppJobEventTriggerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobEventTriggerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3d55a02723ddd9c2ef80684903e19ac60af5531982e1f3589e1ae062cb0df79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScale")
    def put_scale(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobEventTriggerConfigScale", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bef19c94ce44f9721cd7d33eab8fd7f603c75dc057980ec5e43da96260c1a146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScale", [value]))

    @jsii.member(jsii_name="resetParallelism")
    def reset_parallelism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelism", []))

    @jsii.member(jsii_name="resetReplicaCompletionCount")
    def reset_replica_completion_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicaCompletionCount", []))

    @jsii.member(jsii_name="resetScale")
    def reset_scale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScale", []))

    @builtins.property
    @jsii.member(jsii_name="scale")
    def scale(self) -> "ContainerAppJobEventTriggerConfigScaleList":
        return typing.cast("ContainerAppJobEventTriggerConfigScaleList", jsii.get(self, "scale"))

    @builtins.property
    @jsii.member(jsii_name="parallelismInput")
    def parallelism_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelismInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaCompletionCountInput")
    def replica_completion_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicaCompletionCountInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleInput")
    def scale_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobEventTriggerConfigScale"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobEventTriggerConfigScale"]]], jsii.get(self, "scaleInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelism")
    def parallelism(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parallelism"))

    @parallelism.setter
    def parallelism(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56973e9d3486a912df7c3fea6bb1ae277a40eeb0ec0384c80374b2f02b28c131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelism", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaCompletionCount")
    def replica_completion_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicaCompletionCount"))

    @replica_completion_count.setter
    def replica_completion_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5b6093c053dd3af146432260ce0e29025caccd9a997fa2f806dc8bd97109f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaCompletionCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAppJobEventTriggerConfig]:
        return typing.cast(typing.Optional[ContainerAppJobEventTriggerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAppJobEventTriggerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29c9db6823d96a69414e478987240987913ca29812473fe7b56a0082bc93d15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobEventTriggerConfigScale",
    jsii_struct_bases=[],
    name_mapping={
        "max_executions": "maxExecutions",
        "min_executions": "minExecutions",
        "polling_interval_in_seconds": "pollingIntervalInSeconds",
        "rules": "rules",
    },
)
class ContainerAppJobEventTriggerConfigScale:
    def __init__(
        self,
        *,
        max_executions: typing.Optional[jsii.Number] = None,
        min_executions: typing.Optional[jsii.Number] = None,
        polling_interval_in_seconds: typing.Optional[jsii.Number] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobEventTriggerConfigScaleRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param max_executions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#max_executions ContainerAppJob#max_executions}.
        :param min_executions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#min_executions ContainerAppJob#min_executions}.
        :param polling_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#polling_interval_in_seconds ContainerAppJob#polling_interval_in_seconds}.
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#rules ContainerAppJob#rules}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9f65391973dacdc729ae4eb3829f11be66ed0982bbf0ba61b491c802c8ea99a)
            check_type(argname="argument max_executions", value=max_executions, expected_type=type_hints["max_executions"])
            check_type(argname="argument min_executions", value=min_executions, expected_type=type_hints["min_executions"])
            check_type(argname="argument polling_interval_in_seconds", value=polling_interval_in_seconds, expected_type=type_hints["polling_interval_in_seconds"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_executions is not None:
            self._values["max_executions"] = max_executions
        if min_executions is not None:
            self._values["min_executions"] = min_executions
        if polling_interval_in_seconds is not None:
            self._values["polling_interval_in_seconds"] = polling_interval_in_seconds
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def max_executions(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#max_executions ContainerAppJob#max_executions}.'''
        result = self._values.get("max_executions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_executions(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#min_executions ContainerAppJob#min_executions}.'''
        result = self._values.get("min_executions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def polling_interval_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#polling_interval_in_seconds ContainerAppJob#polling_interval_in_seconds}.'''
        result = self._values.get("polling_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobEventTriggerConfigScaleRules"]]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#rules ContainerAppJob#rules}
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobEventTriggerConfigScaleRules"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobEventTriggerConfigScale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppJobEventTriggerConfigScaleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobEventTriggerConfigScaleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f83423d340651d4ac252411d48fbde5cc4ea9d44d5a77b719f197a92225e65c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppJobEventTriggerConfigScaleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc0120db52b69ddab589668870f5c6f1a6775b771a7e2670df875a72062e3d83)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobEventTriggerConfigScaleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39e4c250225349c79c05f1082560e49eca77a487b9fedeaa5b3d97e1b3e83cf0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b93c99b617cc649bc1d1346269771dce415eb251837240013a19cc4c68abb94e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3677fcc1f9f5c4a8ea0916ce402ef3eb166e7fc573cc07053729adf87165d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobEventTriggerConfigScale]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobEventTriggerConfigScale]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobEventTriggerConfigScale]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a5b978f648f4f08837aff3e7ff5b762b35017607db595d3646c5facb540b1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobEventTriggerConfigScaleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobEventTriggerConfigScaleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df4a94b1da15f9693aec878b9d2ebe49e626c78dec7434aaa241aa607ebf8201)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobEventTriggerConfigScaleRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5542b6b7e4edccba5cd02091677fc441ed04e0eccc69aac1d66ec3bb0bfbbbbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="resetMaxExecutions")
    def reset_max_executions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxExecutions", []))

    @jsii.member(jsii_name="resetMinExecutions")
    def reset_min_executions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinExecutions", []))

    @jsii.member(jsii_name="resetPollingIntervalInSeconds")
    def reset_polling_interval_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPollingIntervalInSeconds", []))

    @jsii.member(jsii_name="resetRules")
    def reset_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRules", []))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "ContainerAppJobEventTriggerConfigScaleRulesList":
        return typing.cast("ContainerAppJobEventTriggerConfigScaleRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="maxExecutionsInput")
    def max_executions_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxExecutionsInput"))

    @builtins.property
    @jsii.member(jsii_name="minExecutionsInput")
    def min_executions_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minExecutionsInput"))

    @builtins.property
    @jsii.member(jsii_name="pollingIntervalInSecondsInput")
    def polling_interval_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "pollingIntervalInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobEventTriggerConfigScaleRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobEventTriggerConfigScaleRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxExecutions")
    def max_executions(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxExecutions"))

    @max_executions.setter
    def max_executions(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9025ca7d1baec82ce4628f962cd7f085168d7cd1e9405bed060738d799e35385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxExecutions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minExecutions")
    def min_executions(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minExecutions"))

    @min_executions.setter
    def min_executions(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e88920f6d384aa16cd8ac044f2808beb1fe163a67fdab9ae7a1bd5ac15b45d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minExecutions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pollingIntervalInSeconds")
    def polling_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pollingIntervalInSeconds"))

    @polling_interval_in_seconds.setter
    def polling_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16602261121d6a9aafba7b71d2b8cc781b250e2adb278c7502e7e9f1a6da57af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pollingIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobEventTriggerConfigScale]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobEventTriggerConfigScale]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobEventTriggerConfigScale]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__167e957f1939d3a17a6a53ae4862c893b6456f4bb4fae9a5e084f848c337ae1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobEventTriggerConfigScaleRules",
    jsii_struct_bases=[],
    name_mapping={
        "custom_rule_type": "customRuleType",
        "metadata": "metadata",
        "name": "name",
        "authentication": "authentication",
    },
)
class ContainerAppJobEventTriggerConfigScaleRules:
    def __init__(
        self,
        *,
        custom_rule_type: builtins.str,
        metadata: typing.Mapping[builtins.str, builtins.str],
        name: builtins.str,
        authentication: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobEventTriggerConfigScaleRulesAuthentication", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param custom_rule_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#custom_rule_type ContainerAppJob#custom_rule_type}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#metadata ContainerAppJob#metadata}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}.
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#authentication ContainerAppJob#authentication}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0de69a9aa737340d23c5adb605411b74ea777ebba6935435a4872a4723c66e8)
            check_type(argname="argument custom_rule_type", value=custom_rule_type, expected_type=type_hints["custom_rule_type"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument authentication", value=authentication, expected_type=type_hints["authentication"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_rule_type": custom_rule_type,
            "metadata": metadata,
            "name": name,
        }
        if authentication is not None:
            self._values["authentication"] = authentication

    @builtins.property
    def custom_rule_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#custom_rule_type ContainerAppJob#custom_rule_type}.'''
        result = self._values.get("custom_rule_type")
        assert result is not None, "Required property 'custom_rule_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#metadata ContainerAppJob#metadata}.'''
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobEventTriggerConfigScaleRulesAuthentication"]]]:
        '''authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#authentication ContainerAppJob#authentication}
        '''
        result = self._values.get("authentication")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobEventTriggerConfigScaleRulesAuthentication"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobEventTriggerConfigScaleRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobEventTriggerConfigScaleRulesAuthentication",
    jsii_struct_bases=[],
    name_mapping={
        "secret_name": "secretName",
        "trigger_parameter": "triggerParameter",
    },
)
class ContainerAppJobEventTriggerConfigScaleRulesAuthentication:
    def __init__(
        self,
        *,
        secret_name: builtins.str,
        trigger_parameter: builtins.str,
    ) -> None:
        '''
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#secret_name ContainerAppJob#secret_name}.
        :param trigger_parameter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#trigger_parameter ContainerAppJob#trigger_parameter}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa94116e5b4030cdccb8b20b35ba1c2a269ae93b794c6de117030b3fe271eba)
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument trigger_parameter", value=trigger_parameter, expected_type=type_hints["trigger_parameter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_name": secret_name,
            "trigger_parameter": trigger_parameter,
        }

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#secret_name ContainerAppJob#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_parameter(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#trigger_parameter ContainerAppJob#trigger_parameter}.'''
        result = self._values.get("trigger_parameter")
        assert result is not None, "Required property 'trigger_parameter' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobEventTriggerConfigScaleRulesAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppJobEventTriggerConfigScaleRulesAuthenticationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobEventTriggerConfigScaleRulesAuthenticationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5deef196186b805caa4564502a4cb301388a9d115667006b62907f1e0036714)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppJobEventTriggerConfigScaleRulesAuthenticationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47d5604182bfa876fade26fb586569d85063afcf930c13076a466ffe3d3ff97)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobEventTriggerConfigScaleRulesAuthenticationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__566fee0253c15d0043e8eb79d3e86d1afcce1ac759d93a6126caad26f016252c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cd08519eb9687e88d5c194025b685d8e85ff8c51be7a86e4aea0ce45b4c718d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f27001ec8597f48dddaaa184c0ececdbcb4708da2aa439099612201c5aa8d21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobEventTriggerConfigScaleRulesAuthentication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobEventTriggerConfigScaleRulesAuthentication]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobEventTriggerConfigScaleRulesAuthentication]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0ec28318802a859937a9c540940125c55b3e62ddaead7b777c4a758c0561f56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobEventTriggerConfigScaleRulesAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobEventTriggerConfigScaleRulesAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5b1cbd7a8cd9ccc79a8622e3794fa7f7c3d5ce3d1b4c01127ddbaec6126b5fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerParameterInput")
    def trigger_parameter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d464b6ea42bbbc61a11da6b7af0746156009472f7613616b697dc30d6cfb98f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerParameter")
    def trigger_parameter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerParameter"))

    @trigger_parameter.setter
    def trigger_parameter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4be5f3b57760ace74eada3e5bded3a9dc9fc3b4167804ef147ae7a78b5aa7f57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerParameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobEventTriggerConfigScaleRulesAuthentication]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobEventTriggerConfigScaleRulesAuthentication]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobEventTriggerConfigScaleRulesAuthentication]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f886877324b66e26feacd7ab4061a90ec4524e92063911f53751c2118ddc97e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobEventTriggerConfigScaleRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobEventTriggerConfigScaleRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__128e9f33852e49d07aae17e97a1253798c8bb73bf0c3276c93912fea5dd9dc63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppJobEventTriggerConfigScaleRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcad71de8630ab4b50f53db2d55e6d361f5c4abb3b2f67b5662e075319cc1be2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobEventTriggerConfigScaleRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85dccfd6176e7664c6bf5ada235be1945aeba91e968db0f5de6c3fe79957de88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__647340710b16c4aa681e8f1de1fecfbf242c3f2a0f1c71c5f28ad4f8e6e38c06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f23a1c21a46815612a0d2eea5a4767151ddd5edb18370e77fdc7b01cb107efb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobEventTriggerConfigScaleRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobEventTriggerConfigScaleRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobEventTriggerConfigScaleRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8cbeab656bdc3c741b07b1edf4c9f2a010fc827fd419217054b111347b9925f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobEventTriggerConfigScaleRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobEventTriggerConfigScaleRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a13a9b9a6ed0ea2d909e89ca9c75e180828f02dde684997def94606d9afb184)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAuthentication")
    def put_authentication(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobEventTriggerConfigScaleRulesAuthentication, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19b06805988684f0c50ff86842434e768ee639ef8bc9dd8cbb9ef705b99ef3f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthentication", [value]))

    @jsii.member(jsii_name="resetAuthentication")
    def reset_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthentication", []))

    @builtins.property
    @jsii.member(jsii_name="authentication")
    def authentication(
        self,
    ) -> ContainerAppJobEventTriggerConfigScaleRulesAuthenticationList:
        return typing.cast(ContainerAppJobEventTriggerConfigScaleRulesAuthenticationList, jsii.get(self, "authentication"))

    @builtins.property
    @jsii.member(jsii_name="authenticationInput")
    def authentication_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobEventTriggerConfigScaleRulesAuthentication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobEventTriggerConfigScaleRulesAuthentication]]], jsii.get(self, "authenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="customRuleTypeInput")
    def custom_rule_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customRuleTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="customRuleType")
    def custom_rule_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customRuleType"))

    @custom_rule_type.setter
    def custom_rule_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__068b750df8ac6d15949b71b09dc9a9de252a8f0d6aab15bb76f2bb47c738c9c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customRuleType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf3d93c957964a88bd37bd4901aa8fa0e7c0378d3dea99bcf7882a328cb19b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b0c858867160f51f4c3cb8afe354d9235285bc66840a3f0cfb00bd9897789c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobEventTriggerConfigScaleRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobEventTriggerConfigScaleRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobEventTriggerConfigScaleRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e871513b366556882828554d38e07751e4e9f2b6a343e985de601096330f28f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class ContainerAppJobIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#type ContainerAppJob#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#identity_ids ContainerAppJob#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947fdeb755ba46776844cdd8e1fa4a563d0650bb969ebe2ccf8109409aa64d29)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#type ContainerAppJob#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#identity_ids ContainerAppJob#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppJobIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36ae3795a350b5439c49b716ab3c3e2182bd5767db606086121bab36f22eae0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdentityIds")
    def reset_identity_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityIds", []))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="identityIdsInput")
    def identity_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identityIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @identity_ids.setter
    def identity_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ccc9a20e6e07824a6fbea8575f71abbf7ebef42c5f837838e5d91ef09a8c677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a5632db6123601596a06a9d6e0be76bce30fe9e447f3daae74c241ee7d807c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAppJobIdentity]:
        return typing.cast(typing.Optional[ContainerAppJobIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ContainerAppJobIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc0485ea84ce3f4dad78014cbb83b0ccdcc7fffeacea9c810225e3ace1af233a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobManualTriggerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "parallelism": "parallelism",
        "replica_completion_count": "replicaCompletionCount",
    },
)
class ContainerAppJobManualTriggerConfig:
    def __init__(
        self,
        *,
        parallelism: typing.Optional[jsii.Number] = None,
        replica_completion_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param parallelism: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#parallelism ContainerAppJob#parallelism}.
        :param replica_completion_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#replica_completion_count ContainerAppJob#replica_completion_count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdffda81a73d59602c52dc29122111580ffa1833f3419e39dc3211682b9f620a)
            check_type(argname="argument parallelism", value=parallelism, expected_type=type_hints["parallelism"])
            check_type(argname="argument replica_completion_count", value=replica_completion_count, expected_type=type_hints["replica_completion_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if parallelism is not None:
            self._values["parallelism"] = parallelism
        if replica_completion_count is not None:
            self._values["replica_completion_count"] = replica_completion_count

    @builtins.property
    def parallelism(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#parallelism ContainerAppJob#parallelism}.'''
        result = self._values.get("parallelism")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replica_completion_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#replica_completion_count ContainerAppJob#replica_completion_count}.'''
        result = self._values.get("replica_completion_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobManualTriggerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppJobManualTriggerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobManualTriggerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60d2f6a5feba2b71723eebd4368fb1d9a720a2986f7160e37b3dc1442a111494)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParallelism")
    def reset_parallelism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelism", []))

    @jsii.member(jsii_name="resetReplicaCompletionCount")
    def reset_replica_completion_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicaCompletionCount", []))

    @builtins.property
    @jsii.member(jsii_name="parallelismInput")
    def parallelism_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelismInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaCompletionCountInput")
    def replica_completion_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicaCompletionCountInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelism")
    def parallelism(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parallelism"))

    @parallelism.setter
    def parallelism(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74204d7a48da02b67d33b1f5b824c6a95e3ab98b290d7d816212f171d2be32f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelism", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaCompletionCount")
    def replica_completion_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicaCompletionCount"))

    @replica_completion_count.setter
    def replica_completion_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d0ce222be89a8c12fc8b80cb97df2a903f1c794396a7952b6052c031ca0b8d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaCompletionCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAppJobManualTriggerConfig]:
        return typing.cast(typing.Optional[ContainerAppJobManualTriggerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAppJobManualTriggerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1379c41a37d3d038bdcf0ca46732ec020c18ac82c72bac8505be5f6c60e36db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobRegistry",
    jsii_struct_bases=[],
    name_mapping={
        "server": "server",
        "identity": "identity",
        "password_secret_name": "passwordSecretName",
        "username": "username",
    },
)
class ContainerAppJobRegistry:
    def __init__(
        self,
        *,
        server: builtins.str,
        identity: typing.Optional[builtins.str] = None,
        password_secret_name: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param server: The hostname for the Container Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#server ContainerAppJob#server}
        :param identity: ID of the System or User Managed Identity used to pull images from the Container Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#identity ContainerAppJob#identity}
        :param password_secret_name: The name of the Secret Reference containing the password value for this user on the Container Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#password_secret_name ContainerAppJob#password_secret_name}
        :param username: The username to use for this Container Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#username ContainerAppJob#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__399b5c1494f93a321703bb892b53ef82a96dd092eb61bbb45571745e96596778)
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument password_secret_name", value=password_secret_name, expected_type=type_hints["password_secret_name"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "server": server,
        }
        if identity is not None:
            self._values["identity"] = identity
        if password_secret_name is not None:
            self._values["password_secret_name"] = password_secret_name
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def server(self) -> builtins.str:
        '''The hostname for the Container Registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#server ContainerAppJob#server}
        '''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity(self) -> typing.Optional[builtins.str]:
        '''ID of the System or User Managed Identity used to pull images from the Container Registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#identity ContainerAppJob#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password_secret_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Secret Reference containing the password value for this user on the Container Registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#password_secret_name ContainerAppJob#password_secret_name}
        '''
        result = self._values.get("password_secret_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The username to use for this Container Registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#username ContainerAppJob#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobRegistry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppJobRegistryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobRegistryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc1f880c5d680af221a0e044762dbd1b7b7c6937706ba48987c7f2e9b58bf27a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ContainerAppJobRegistryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572b2649d3c0ab88d91117be4a323929b84b66566b2aa2c7f62fc3ca9e961fbf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobRegistryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b08f2730137d9314dbc515b0dca520a54f0d131d5aaf06dd24f6c9299c6418)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09546be777f3df69f9fbe5420bef010b7a1d170b835277ed1a7e3f4372f9ed1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00387da03b1a70918840fcb2602039648e88a41c7e77b9bfb272bc20908cd809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobRegistry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobRegistry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobRegistry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e823409c61d7670bf1211ee2d0add415ca4874e24527116e341bb42c5c79888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobRegistryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobRegistryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cd73f54bf791a6102984c0b7eaf3bab9bdc2b028399a85a7fe6069a8738c1a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetPasswordSecretName")
    def reset_password_secret_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordSecretName", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordSecretNameInput")
    def password_secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordSecretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serverInput")
    def server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identity"))

    @identity.setter
    def identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad2f52a576c026b5c65154cbed1e0db716c2da07a187b9ce97da31ec51a352f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordSecretName")
    def password_secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passwordSecretName"))

    @password_secret_name.setter
    def password_secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a369e8819a8ca22b8afd8730e9bc67b20b1ccdd84298178c4ecd5a134475c573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordSecretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa02a71e9cd5138d3aa41d21cc34a6975216f05dc61169dac824ce2a70d6be26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab0bdae4a954e3db581d00c7be6923a6a2e5c4b42163687879668a59ff0e4e89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobRegistry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobRegistry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobRegistry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10530b8c0e31b1527210e6b65baaf4d08941bffaa8e3252e182fd8a01d2fe6a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobScheduleTriggerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cron_expression": "cronExpression",
        "parallelism": "parallelism",
        "replica_completion_count": "replicaCompletionCount",
    },
)
class ContainerAppJobScheduleTriggerConfig:
    def __init__(
        self,
        *,
        cron_expression: builtins.str,
        parallelism: typing.Optional[jsii.Number] = None,
        replica_completion_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cron_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#cron_expression ContainerAppJob#cron_expression}.
        :param parallelism: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#parallelism ContainerAppJob#parallelism}.
        :param replica_completion_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#replica_completion_count ContainerAppJob#replica_completion_count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06721bb3db4b911ec41c64c41a0608d10f5011b2075d56ec99a53f616e638150)
            check_type(argname="argument cron_expression", value=cron_expression, expected_type=type_hints["cron_expression"])
            check_type(argname="argument parallelism", value=parallelism, expected_type=type_hints["parallelism"])
            check_type(argname="argument replica_completion_count", value=replica_completion_count, expected_type=type_hints["replica_completion_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cron_expression": cron_expression,
        }
        if parallelism is not None:
            self._values["parallelism"] = parallelism
        if replica_completion_count is not None:
            self._values["replica_completion_count"] = replica_completion_count

    @builtins.property
    def cron_expression(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#cron_expression ContainerAppJob#cron_expression}.'''
        result = self._values.get("cron_expression")
        assert result is not None, "Required property 'cron_expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parallelism(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#parallelism ContainerAppJob#parallelism}.'''
        result = self._values.get("parallelism")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replica_completion_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#replica_completion_count ContainerAppJob#replica_completion_count}.'''
        result = self._values.get("replica_completion_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobScheduleTriggerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppJobScheduleTriggerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobScheduleTriggerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc3a3d6cdb0e6bed5bc65d962c2e62338bbb203993a9ec41f4f124c6eebbd262)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParallelism")
    def reset_parallelism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelism", []))

    @jsii.member(jsii_name="resetReplicaCompletionCount")
    def reset_replica_completion_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicaCompletionCount", []))

    @builtins.property
    @jsii.member(jsii_name="cronExpressionInput")
    def cron_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelismInput")
    def parallelism_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelismInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaCompletionCountInput")
    def replica_completion_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicaCompletionCountInput"))

    @builtins.property
    @jsii.member(jsii_name="cronExpression")
    def cron_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cronExpression"))

    @cron_expression.setter
    def cron_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0b41dcdee636dde627a7fd10e9ee354e096da8f9c1ef71d854274a3a9ea4822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cronExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelism")
    def parallelism(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parallelism"))

    @parallelism.setter
    def parallelism(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b52633e763f7e36ef30cddef6b92508ee4bfe2dc3111685cb62ac1ac3ed9c541)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelism", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaCompletionCount")
    def replica_completion_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicaCompletionCount"))

    @replica_completion_count.setter
    def replica_completion_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51adf5d855171b89c22d6df6ff60aeb4081d025e65af52b292eb2d3341acc44c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaCompletionCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAppJobScheduleTriggerConfig]:
        return typing.cast(typing.Optional[ContainerAppJobScheduleTriggerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAppJobScheduleTriggerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832b69d4396c9d768a73caf9db1025962b0a8ebe17daf3adde8cb861c9454b91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobSecret",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "identity": "identity",
        "key_vault_secret_id": "keyVaultSecretId",
        "value": "value",
    },
)
class ContainerAppJobSecret:
    def __init__(
        self,
        *,
        name: builtins.str,
        identity: typing.Optional[builtins.str] = None,
        key_vault_secret_id: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The secret name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        :param identity: The identity to use for accessing key vault reference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#identity ContainerAppJob#identity}
        :param key_vault_secret_id: The Key Vault Secret ID. Could be either one of ``id`` or ``versionless_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#key_vault_secret_id ContainerAppJob#key_vault_secret_id}
        :param value: The value for this secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#value ContainerAppJob#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e227a8fa661e39c40c37f8cf4a187a8bf1fcd08196b281e8ce68e7d9ca6ab3d7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument key_vault_secret_id", value=key_vault_secret_id, expected_type=type_hints["key_vault_secret_id"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if identity is not None:
            self._values["identity"] = identity
        if key_vault_secret_id is not None:
            self._values["key_vault_secret_id"] = key_vault_secret_id
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> builtins.str:
        '''The secret name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity(self) -> typing.Optional[builtins.str]:
        '''The identity to use for accessing key vault reference.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#identity ContainerAppJob#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_secret_id(self) -> typing.Optional[builtins.str]:
        '''The Key Vault Secret ID. Could be either one of ``id`` or ``versionless_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#key_vault_secret_id ContainerAppJob#key_vault_secret_id}
        '''
        result = self._values.get("key_vault_secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The value for this secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#value ContainerAppJob#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppJobSecretList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobSecretList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__144eff62adeb66621c42e28619d1a8a8fd8cfbdf6323e08f5c65373a3230429c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ContainerAppJobSecretOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24ff8ebf9dc626ade6822a38a03e3dac93818441606989e089772e7448b740f4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobSecretOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5d0715828ca1a5cf0515743a4a69b6cf4d0996ce51d9891bab396338eea9852)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37e74d3fc1339bb656a7b64dcadedf0bb8106c5da48f3e0acb45c441d3d7ce71)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a3e2fda4849c0c17590fa2f3d794ec783139031af5f6c961048bc193a47579a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobSecret]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobSecret]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobSecret]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01026a83016b7b008c2e6b72d12c631f1feeb81b19060621cfa7c3d92c914ad4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41e538eb0d5f0a460ac0345c27906404cdd20c6df0143642c3eb9359573d2a83)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetKeyVaultSecretId")
    def reset_key_vault_secret_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultSecretId", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultSecretIdInput")
    def key_vault_secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultSecretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identity"))

    @identity.setter
    def identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f9dc6470f18e2e7ad35b1f49ed404caf66723023a06f3cf7c70221b5a526320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultSecretId")
    def key_vault_secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultSecretId"))

    @key_vault_secret_id.setter
    def key_vault_secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da60dd2cd64f50e3fd58ba1dbf096885c611de9fb3690a23c33753834d854875)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultSecretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f2fc3e1265f04dd419e26923309d776535476b950b88364b38a913f71cf67ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a78596ff651c8b06008b0d0ad8a29f43946f88b472c364c7de0e70c7bd2e9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobSecret]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobSecret]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobSecret]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6861794edd937caaff7ea2c3b5f3f093c99843a5ea34df0747d1dafff5cb75ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "container": "container",
        "init_container": "initContainer",
        "volume": "volume",
    },
)
class ContainerAppJobTemplate:
    def __init__(
        self,
        *,
        container: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateContainer", typing.Dict[builtins.str, typing.Any]]]],
        init_container: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateInitContainer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        volume: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateVolume", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#container ContainerAppJob#container}
        :param init_container: init_container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#init_container ContainerAppJob#init_container}
        :param volume: volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#volume ContainerAppJob#volume}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e5a155995b94e5f42f123c16a49474a038637e503f597abaa73185169799cc)
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument init_container", value=init_container, expected_type=type_hints["init_container"])
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container": container,
        }
        if init_container is not None:
            self._values["init_container"] = init_container
        if volume is not None:
            self._values["volume"] = volume

    @builtins.property
    def container(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainer"]]:
        '''container block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#container ContainerAppJob#container}
        '''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainer"]], result)

    @builtins.property
    def init_container(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateInitContainer"]]]:
        '''init_container block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#init_container ContainerAppJob#init_container}
        '''
        result = self._values.get("init_container")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateInitContainer"]]], result)

    @builtins.property
    def volume(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateVolume"]]]:
        '''volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#volume ContainerAppJob#volume}
        '''
        result = self._values.get("volume")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateVolume"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainer",
    jsii_struct_bases=[],
    name_mapping={
        "cpu": "cpu",
        "image": "image",
        "memory": "memory",
        "name": "name",
        "args": "args",
        "command": "command",
        "env": "env",
        "liveness_probe": "livenessProbe",
        "readiness_probe": "readinessProbe",
        "startup_probe": "startupProbe",
        "volume_mounts": "volumeMounts",
    },
)
class ContainerAppJobTemplateContainer:
    def __init__(
        self,
        *,
        cpu: jsii.Number,
        image: builtins.str,
        memory: builtins.str,
        name: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateContainerEnv", typing.Dict[builtins.str, typing.Any]]]]] = None,
        liveness_probe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateContainerLivenessProbe", typing.Dict[builtins.str, typing.Any]]]]] = None,
        readiness_probe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateContainerReadinessProbe", typing.Dict[builtins.str, typing.Any]]]]] = None,
        startup_probe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateContainerStartupProbe", typing.Dict[builtins.str, typing.Any]]]]] = None,
        volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateContainerVolumeMounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cpu: The amount of vCPU to allocate to the container. Possible values include ``0.25``, ``0.5``, ``0.75``, ``1.0``, ``1.25``, ``1.5``, ``1.75``, and ``2.0``. **NOTE:** ``cpu`` and ``memory`` must be specified in ``0.25'/'0.5Gi`` combination increments. e.g. ``1.0`` / ``2.0`` or ``0.5`` / ``1.0``. When there's a workload profile specified, there's no such constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#cpu ContainerAppJob#cpu}
        :param image: The image to use to create the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#image ContainerAppJob#image}
        :param memory: The amount of memory to allocate to the container. Possible values include ``0.5Gi``, ``1.0Gi``, ``1.5Gi``, ``2.0Gi``, ``2.5Gi``, ``3.0Gi``, ``3.5Gi``, and ``4.0Gi``. **NOTE:** ``cpu`` and ``memory`` must be specified in ``0.25'/'0.5Gi`` combination increments. e.g. ``1.25`` / ``2.5Gi`` or ``0.75`` / ``1.5Gi``. When there's a workload profile specified, there's no such constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#memory ContainerAppJob#memory}
        :param name: The name of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        :param args: A list of args to pass to the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#args ContainerAppJob#args}
        :param command: A command to pass to the container to override the default. This is provided as a list of command line elements without spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#command ContainerAppJob#command}
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#env ContainerAppJob#env}
        :param liveness_probe: liveness_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#liveness_probe ContainerAppJob#liveness_probe}
        :param readiness_probe: readiness_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#readiness_probe ContainerAppJob#readiness_probe}
        :param startup_probe: startup_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#startup_probe ContainerAppJob#startup_probe}
        :param volume_mounts: volume_mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#volume_mounts ContainerAppJob#volume_mounts}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37ef73afaa383f789916257ed2f08f9fc9481954f233657fc5228fa13a2d172)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument liveness_probe", value=liveness_probe, expected_type=type_hints["liveness_probe"])
            check_type(argname="argument readiness_probe", value=readiness_probe, expected_type=type_hints["readiness_probe"])
            check_type(argname="argument startup_probe", value=startup_probe, expected_type=type_hints["startup_probe"])
            check_type(argname="argument volume_mounts", value=volume_mounts, expected_type=type_hints["volume_mounts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cpu": cpu,
            "image": image,
            "memory": memory,
            "name": name,
        }
        if args is not None:
            self._values["args"] = args
        if command is not None:
            self._values["command"] = command
        if env is not None:
            self._values["env"] = env
        if liveness_probe is not None:
            self._values["liveness_probe"] = liveness_probe
        if readiness_probe is not None:
            self._values["readiness_probe"] = readiness_probe
        if startup_probe is not None:
            self._values["startup_probe"] = startup_probe
        if volume_mounts is not None:
            self._values["volume_mounts"] = volume_mounts

    @builtins.property
    def cpu(self) -> jsii.Number:
        '''The amount of vCPU to allocate to the container.

        Possible values include ``0.25``, ``0.5``, ``0.75``, ``1.0``, ``1.25``, ``1.5``, ``1.75``, and ``2.0``. **NOTE:** ``cpu`` and ``memory`` must be specified in ``0.25'/'0.5Gi`` combination increments. e.g. ``1.0`` / ``2.0`` or ``0.5`` / ``1.0``. When there's a workload profile specified, there's no such constraint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#cpu ContainerAppJob#cpu}
        '''
        result = self._values.get("cpu")
        assert result is not None, "Required property 'cpu' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def image(self) -> builtins.str:
        '''The image to use to create the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#image ContainerAppJob#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def memory(self) -> builtins.str:
        '''The amount of memory to allocate to the container.

        Possible values include ``0.5Gi``, ``1.0Gi``, ``1.5Gi``, ``2.0Gi``, ``2.5Gi``, ``3.0Gi``, ``3.5Gi``, and ``4.0Gi``. **NOTE:** ``cpu`` and ``memory`` must be specified in ``0.25'/'0.5Gi`` combination increments. e.g. ``1.25`` / ``2.5Gi`` or ``0.75`` / ``1.5Gi``. When there's a workload profile specified, there's no such constraint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#memory ContainerAppJob#memory}
        '''
        result = self._values.get("memory")
        assert result is not None, "Required property 'memory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of args to pass to the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#args ContainerAppJob#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A command to pass to the container to override the default.

        This is provided as a list of command line elements without spaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#command ContainerAppJob#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def env(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerEnv"]]]:
        '''env block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#env ContainerAppJob#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerEnv"]]], result)

    @builtins.property
    def liveness_probe(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerLivenessProbe"]]]:
        '''liveness_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#liveness_probe ContainerAppJob#liveness_probe}
        '''
        result = self._values.get("liveness_probe")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerLivenessProbe"]]], result)

    @builtins.property
    def readiness_probe(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerReadinessProbe"]]]:
        '''readiness_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#readiness_probe ContainerAppJob#readiness_probe}
        '''
        result = self._values.get("readiness_probe")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerReadinessProbe"]]], result)

    @builtins.property
    def startup_probe(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerStartupProbe"]]]:
        '''startup_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#startup_probe ContainerAppJob#startup_probe}
        '''
        result = self._values.get("startup_probe")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerStartupProbe"]]], result)

    @builtins.property
    def volume_mounts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerVolumeMounts"]]]:
        '''volume_mounts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#volume_mounts ContainerAppJob#volume_mounts}
        '''
        result = self._values.get("volume_mounts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerVolumeMounts"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobTemplateContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerEnv",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "secret_name": "secretName", "value": "value"},
)
class ContainerAppJobTemplateContainerEnv:
    def __init__(
        self,
        *,
        name: builtins.str,
        secret_name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the environment variable for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        :param secret_name: The name of the secret that contains the value for this environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#secret_name ContainerAppJob#secret_name}
        :param value: The value for this environment variable. **NOTE:** This value is ignored if ``secret_name`` is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#value ContainerAppJob#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d456ac7ca2ff351dab4d7e2ae62bedde123b48c1546957db861f994227df672)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if secret_name is not None:
            self._values["secret_name"] = secret_name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the environment variable for the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_name(self) -> typing.Optional[builtins.str]:
        '''The name of the secret that contains the value for this environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#secret_name ContainerAppJob#secret_name}
        '''
        result = self._values.get("secret_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The value for this environment variable. **NOTE:** This value is ignored if ``secret_name`` is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#value ContainerAppJob#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobTemplateContainerEnv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppJobTemplateContainerEnvList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerEnvList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6e13556b7198e7f0820e166cadb492f713cc17f2a129cc01d449f185c78ab17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppJobTemplateContainerEnvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9aa057ecac1326749f390e04efc64c981e6568a06fa982cc23198fcb8316bc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobTemplateContainerEnvOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc68ed3f67ef11e983823913fb723df90eca99a36b39a42f132b0222159d95a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2bca635987507f4b8574215105159140d1669c1f37f09591f271f558cb789e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45f1e25112b1668b317fbe63d5693a1f9d4352c4462aa6963bfab55ae1ebf69b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerEnv]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerEnv]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed24b070268effdeb23fc9edddacdd25dc4593fcaf2aaa9e1e98ccc36e15f56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateContainerEnvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerEnvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce44170ea981ea4169a7da9bd04c9496bc242930b2e8e0fa180f8c94fecd9530)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSecretName")
    def reset_secret_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce0edf1a61d182bda5c48a197b1f0ccb30d5d1f50b0b407a7a5356c29dba1eaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a7027211701b7e9ce9afbfcc5e7d50a0b2a486c4ae68190857a32091788c42a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed0e30aa4ed9525dca4eafe0f1eba8b6452f62cc7cd9097bf9968f2da25bab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerEnv]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerEnv]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerEnv]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__648af50d529d1df84cf0a7628cb3f99eb1ded5bd5d52c770a53d54a1890583c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateContainerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfefe53ab9eac66ad8aecb904a026b858d09d31b68f3baadfc75664fa9bafea6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppJobTemplateContainerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd6efdc5353e5ef5140401a642a12b1dc0eac4c1a7a3b1bb4ba03680b3db1464)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobTemplateContainerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d19b3ae793972c287b09f50f37153a6eeaef503eb11b55d9fcd7a908f5a17b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da7e56a27e4f086cd7526ce4c1c01fb191a0a2b9fc6d0d4aab4a1a91bf3fd781)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1190f30ee45715d3d901d430c0db39174796e40bc2c047ec78f02981d5238ee8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainer]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainer]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ea06e37b470d21af9fb832efcf95850739ad1797539a3b56722c140262cf90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerLivenessProbe",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "transport": "transport",
        "failure_count_threshold": "failureCountThreshold",
        "header": "header",
        "host": "host",
        "initial_delay": "initialDelay",
        "interval_seconds": "intervalSeconds",
        "path": "path",
        "timeout": "timeout",
    },
)
class ContainerAppJobTemplateContainerLivenessProbe:
    def __init__(
        self,
        *,
        port: jsii.Number,
        transport: builtins.str,
        failure_count_threshold: typing.Optional[jsii.Number] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateContainerLivenessProbeHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        host: typing.Optional[builtins.str] = None,
        initial_delay: typing.Optional[jsii.Number] = None,
        interval_seconds: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param port: The port number on which to connect. Possible values are between ``1`` and ``65535``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#port ContainerAppJob#port}
        :param transport: Type of probe. Possible values are ``TCP``, ``HTTP``, and ``HTTPS``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#transport ContainerAppJob#transport}
        :param failure_count_threshold: The number of consecutive failures required to consider this probe as failed. Possible values are between ``1`` and ``30``. Defaults to ``3``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#failure_count_threshold ContainerAppJob#failure_count_threshold}
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#header ContainerAppJob#header}
        :param host: The probe hostname. Defaults to the pod IP address. Setting a value for ``Host`` in ``headers`` can be used to override this for ``http`` and ``https`` type probes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#host ContainerAppJob#host}
        :param initial_delay: The number of seconds elapsed after the container has started before the probe is initiated. Possible values are between ``0`` and ``60``. Defaults to ``1`` seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#initial_delay ContainerAppJob#initial_delay}
        :param interval_seconds: How often, in seconds, the probe should run. Possible values are between ``1`` and ``240``. Defaults to ``10``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#interval_seconds ContainerAppJob#interval_seconds}
        :param path: The URI to use with the ``host`` for http type probes. Not valid for ``TCP`` type probes. Defaults to ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#path ContainerAppJob#path}
        :param timeout: Time in seconds after which the probe times out. Possible values are between ``1`` an ``240``. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#timeout ContainerAppJob#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ef3de46ec4fd17e398043191934d9b8ae1baf4e23b4c1ab8974f7644a730b95)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument transport", value=transport, expected_type=type_hints["transport"])
            check_type(argname="argument failure_count_threshold", value=failure_count_threshold, expected_type=type_hints["failure_count_threshold"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument initial_delay", value=initial_delay, expected_type=type_hints["initial_delay"])
            check_type(argname="argument interval_seconds", value=interval_seconds, expected_type=type_hints["interval_seconds"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "transport": transport,
        }
        if failure_count_threshold is not None:
            self._values["failure_count_threshold"] = failure_count_threshold
        if header is not None:
            self._values["header"] = header
        if host is not None:
            self._values["host"] = host
        if initial_delay is not None:
            self._values["initial_delay"] = initial_delay
        if interval_seconds is not None:
            self._values["interval_seconds"] = interval_seconds
        if path is not None:
            self._values["path"] = path
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port number on which to connect. Possible values are between ``1`` and ``65535``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#port ContainerAppJob#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def transport(self) -> builtins.str:
        '''Type of probe. Possible values are ``TCP``, ``HTTP``, and ``HTTPS``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#transport ContainerAppJob#transport}
        '''
        result = self._values.get("transport")
        assert result is not None, "Required property 'transport' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def failure_count_threshold(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive failures required to consider this probe as failed.

        Possible values are between ``1`` and ``30``. Defaults to ``3``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#failure_count_threshold ContainerAppJob#failure_count_threshold}
        '''
        result = self._values.get("failure_count_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerLivenessProbeHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#header ContainerAppJob#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerLivenessProbeHeader"]]], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''The probe hostname.

        Defaults to the pod IP address. Setting a value for ``Host`` in ``headers`` can be used to override this for ``http`` and ``https`` type probes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#host ContainerAppJob#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_delay(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds elapsed after the container has started before the probe is initiated.

        Possible values are between ``0`` and ``60``. Defaults to ``1`` seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#initial_delay ContainerAppJob#initial_delay}
        '''
        result = self._values.get("initial_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often, in seconds, the probe should run. Possible values are between ``1`` and ``240``. Defaults to ``10``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#interval_seconds ContainerAppJob#interval_seconds}
        '''
        result = self._values.get("interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The URI to use with the ``host`` for http type probes.

        Not valid for ``TCP`` type probes. Defaults to ``/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#path ContainerAppJob#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Time in seconds after which the probe times out. Possible values are between ``1`` an ``240``. Defaults to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#timeout ContainerAppJob#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobTemplateContainerLivenessProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerLivenessProbeHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ContainerAppJobTemplateContainerLivenessProbeHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: The HTTP Header Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        :param value: The HTTP Header value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#value ContainerAppJob#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef301633f66a2e1addc67b2010f895daaea7760b12295e4f15a4b053fe517730)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The HTTP Header Name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The HTTP Header value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#value ContainerAppJob#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobTemplateContainerLivenessProbeHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppJobTemplateContainerLivenessProbeHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerLivenessProbeHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de92bae77287a6f5043fd241d2e5c6f207f188799d53cc5f3a7b0afbadc4c91d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppJobTemplateContainerLivenessProbeHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66a55722508c4fe635451f6ffd54a7467920eb739710a9a365d676d8d91d99a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobTemplateContainerLivenessProbeHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21174c9134309c1f363303db7b2f75df7d39624ec6adcf47000e6525c9b6ad9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6c5d51537e4c0ee4391e58500c9b097117bb5652c8b0e45418cfe9e9c7792df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__131f6ef4676c6dcb64933aab6e6dc98720a4bc01fc730d27f0f897115dccefb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerLivenessProbeHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerLivenessProbeHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerLivenessProbeHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9119180f52baa718eef0d9afad49c3bbc5cfc874840f2c9647fa663a6976ccc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateContainerLivenessProbeHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerLivenessProbeHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2971df90d2abe0cef9607d7037ce1363fc2d5b13d097097c0cc406e6c950a7c)
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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__265540597bc992fb4e3c7a92a0fb600c877b36fd075c74c01b09d50fc0805f3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a98626ae4b4bdeca20f16de96157232f6452ae62e663ee216b7b7bcebce373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerLivenessProbeHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerLivenessProbeHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerLivenessProbeHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce09b9131aa93fd869b12806d12c34ae9ced7ff7809c3376dc2db3f423e35602)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateContainerLivenessProbeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerLivenessProbeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b78a673f08e3fcfe348a3161ef1d026cb45e8175c3b584714612175a043f129)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppJobTemplateContainerLivenessProbeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5699ba4fecea9f1a072ad64a3eedcb71b3dec15571e56de7b36e15a93115dcaa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobTemplateContainerLivenessProbeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b60a32e268c1d0b15fdbd7d72601cf0d80fcba4e3325e8f29e8dbec419c3c51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a478dcc643e075de1881618de2550cf507dfb83e961a0f76e793edaec0f4b01c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c9220ec80bd3673635e34dd657d093f9576d530966adaddcd6c6b2ae5b3210a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerLivenessProbe]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerLivenessProbe]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerLivenessProbe]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fbd51a78a06b40cb18ae158dbdb0d9fb4d9601cba455a1776addcceac0e6878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateContainerLivenessProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerLivenessProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a3dc43c4ce65ca06614e3d038e94771e041a688fd4a46400d02150b9d3f37d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerLivenessProbeHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e0e6a9ea78e317751c0ed894609dfd5439a46de308387c7526ce197cdb4a4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="resetFailureCountThreshold")
    def reset_failure_count_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureCountThreshold", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetInitialDelay")
    def reset_initial_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialDelay", []))

    @jsii.member(jsii_name="resetIntervalSeconds")
    def reset_interval_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalSeconds", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> ContainerAppJobTemplateContainerLivenessProbeHeaderList:
        return typing.cast(ContainerAppJobTemplateContainerLivenessProbeHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="terminationGracePeriodSeconds")
    def termination_grace_period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "terminationGracePeriodSeconds"))

    @builtins.property
    @jsii.member(jsii_name="failureCountThresholdInput")
    def failure_count_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureCountThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerLivenessProbeHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerLivenessProbeHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="initialDelayInput")
    def initial_delay_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalSecondsInput")
    def interval_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="transportInput")
    def transport_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transportInput"))

    @builtins.property
    @jsii.member(jsii_name="failureCountThreshold")
    def failure_count_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureCountThreshold"))

    @failure_count_threshold.setter
    def failure_count_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc8a4ae14ced2e87d96171b47a14b581e4eeac766ee28a804e81ad98802b5d68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureCountThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eadf80a89c10e30a7fa10ebb3c463d6bd2de9e86f60f0421fc0776cf3b12c6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelay")
    def initial_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelay"))

    @initial_delay.setter
    def initial_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f319bd47c500cbeed64436d6d5d92e20e2a35e9687e2b2a15010b7fc483467ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSeconds")
    def interval_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSeconds"))

    @interval_seconds.setter
    def interval_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9bd2324c9c7658491f6abecc8924071cdef2a28151dbc7561017c3dedea2480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e8cd203d2dd737472e248f298c669a6be5d3cffdba7d3e0dc32e1910087205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__684afbc0d475f2985424e4e2822b8ea1d6b452ea954e7637eedc6c2a94b32e80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f89df8ef3b99eb3a9cda3f5d6f7d1689d31253b49118f4bbc67e43fd2bf69048)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transport")
    def transport(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transport"))

    @transport.setter
    def transport(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04aeaa0683d3f63cf4f422909e5610389c967da01b21f27bfe9757fdc375534)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerLivenessProbe]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerLivenessProbe]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerLivenessProbe]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0be0cecc2f0e81fb239a1e70e205419fdabecc24c008301ff607c5525387caae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateContainerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e60e2fc12766b29c4a4cd64d62360fbab71343e113395bc11ec84143ca8fd583)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEnv")
    def put_env(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerEnv, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7809d7cce527923a0329df8137d18da8b0b7a75abd5785996ada09c9d3d029e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnv", [value]))

    @jsii.member(jsii_name="putLivenessProbe")
    def put_liveness_probe(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerLivenessProbe, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f47cce101d47471e68e3663d5f2541875f518d09fb59b90a4d5977b99bcdfb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLivenessProbe", [value]))

    @jsii.member(jsii_name="putReadinessProbe")
    def put_readiness_probe(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateContainerReadinessProbe", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f728d634a6a3afd4752308d7ffb3ec7be6ede530f9fb5f15100859e327f76d02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putReadinessProbe", [value]))

    @jsii.member(jsii_name="putStartupProbe")
    def put_startup_probe(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateContainerStartupProbe", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c706c37d2401f17663a1f39bc36e469b73a1031df37172f1b4edc6a5ae0e25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStartupProbe", [value]))

    @jsii.member(jsii_name="putVolumeMounts")
    def put_volume_mounts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateContainerVolumeMounts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b50dd9e26da5b5fcc69b48579ff25a96b03b611218952003ba92d4191ee7e5f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumeMounts", [value]))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetLivenessProbe")
    def reset_liveness_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLivenessProbe", []))

    @jsii.member(jsii_name="resetReadinessProbe")
    def reset_readiness_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadinessProbe", []))

    @jsii.member(jsii_name="resetStartupProbe")
    def reset_startup_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartupProbe", []))

    @jsii.member(jsii_name="resetVolumeMounts")
    def reset_volume_mounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeMounts", []))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> ContainerAppJobTemplateContainerEnvList:
        return typing.cast(ContainerAppJobTemplateContainerEnvList, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorage")
    def ephemeral_storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ephemeralStorage"))

    @builtins.property
    @jsii.member(jsii_name="livenessProbe")
    def liveness_probe(self) -> ContainerAppJobTemplateContainerLivenessProbeList:
        return typing.cast(ContainerAppJobTemplateContainerLivenessProbeList, jsii.get(self, "livenessProbe"))

    @builtins.property
    @jsii.member(jsii_name="readinessProbe")
    def readiness_probe(self) -> "ContainerAppJobTemplateContainerReadinessProbeList":
        return typing.cast("ContainerAppJobTemplateContainerReadinessProbeList", jsii.get(self, "readinessProbe"))

    @builtins.property
    @jsii.member(jsii_name="startupProbe")
    def startup_probe(self) -> "ContainerAppJobTemplateContainerStartupProbeList":
        return typing.cast("ContainerAppJobTemplateContainerStartupProbeList", jsii.get(self, "startupProbe"))

    @builtins.property
    @jsii.member(jsii_name="volumeMounts")
    def volume_mounts(self) -> "ContainerAppJobTemplateContainerVolumeMountsList":
        return typing.cast("ContainerAppJobTemplateContainerVolumeMountsList", jsii.get(self, "volumeMounts"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerEnv]]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="livenessProbeInput")
    def liveness_probe_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerLivenessProbe]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerLivenessProbe]]], jsii.get(self, "livenessProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="readinessProbeInput")
    def readiness_probe_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerReadinessProbe"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerReadinessProbe"]]], jsii.get(self, "readinessProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="startupProbeInput")
    def startup_probe_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerStartupProbe"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerStartupProbe"]]], jsii.get(self, "startupProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeMountsInput")
    def volume_mounts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerVolumeMounts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerVolumeMounts"]]], jsii.get(self, "volumeMountsInput"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36106b1a7093268db64f3d6de4d2e0b56608c79cec7010d3d24f8d69257a4416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0995132a33caca5310a971837fe88eb4e22a74204631bf5c742679251993939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__835c672185e658f210994772282eb2de6f6ca6c9d3ea3e0e8a81ada276409574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c06780b3419034886dd53d66f24d12935bf34837a092c898f1d458e2ad8ae498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__954ac0c8deeb7e980b82daf0ff4c3b2aab24069ff8fe69a6ac2b25133733bf92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28e1d65fe6cb95488d840864854db0845294faa32216302932002c06d9a312f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainer]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainer]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainer]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a7fdf46f6fbf72bd4b51b8e060a1c4b0fe6e9dde790ff66f5caa2be2c93afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerReadinessProbe",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "transport": "transport",
        "failure_count_threshold": "failureCountThreshold",
        "header": "header",
        "host": "host",
        "initial_delay": "initialDelay",
        "interval_seconds": "intervalSeconds",
        "path": "path",
        "success_count_threshold": "successCountThreshold",
        "timeout": "timeout",
    },
)
class ContainerAppJobTemplateContainerReadinessProbe:
    def __init__(
        self,
        *,
        port: jsii.Number,
        transport: builtins.str,
        failure_count_threshold: typing.Optional[jsii.Number] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateContainerReadinessProbeHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        host: typing.Optional[builtins.str] = None,
        initial_delay: typing.Optional[jsii.Number] = None,
        interval_seconds: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        success_count_threshold: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param port: The port number on which to connect. Possible values are between ``1`` and ``65535``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#port ContainerAppJob#port}
        :param transport: Type of probe. Possible values are ``TCP``, ``HTTP``, and ``HTTPS``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#transport ContainerAppJob#transport}
        :param failure_count_threshold: The number of consecutive failures required to consider this probe as failed. Possible values are between ``1`` and ``30``. Defaults to ``3``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#failure_count_threshold ContainerAppJob#failure_count_threshold}
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#header ContainerAppJob#header}
        :param host: The probe hostname. Defaults to the pod IP address. Setting a value for ``Host`` in ``headers`` can be used to override this for ``http`` and ``https`` type probes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#host ContainerAppJob#host}
        :param initial_delay: The number of seconds elapsed after the container has started before the probe is initiated. Possible values are between ``0`` and ``60``. Defaults to ``0`` seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#initial_delay ContainerAppJob#initial_delay}
        :param interval_seconds: How often, in seconds, the probe should run. Possible values are between ``1`` and ``240``. Defaults to ``10``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#interval_seconds ContainerAppJob#interval_seconds}
        :param path: The URI to use for http type probes. Not valid for ``TCP`` type probes. Defaults to ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#path ContainerAppJob#path}
        :param success_count_threshold: The number of consecutive successful responses required to consider this probe as successful. Possible values are between ``1`` and ``10``. Defaults to ``3``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#success_count_threshold ContainerAppJob#success_count_threshold}
        :param timeout: Time in seconds after which the probe times out. Possible values are between ``1`` an ``240``. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#timeout ContainerAppJob#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264a9b65f1b0b6cb9f1aae254e796d281afb62fd6c0508a6ce86fd6369a19059)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument transport", value=transport, expected_type=type_hints["transport"])
            check_type(argname="argument failure_count_threshold", value=failure_count_threshold, expected_type=type_hints["failure_count_threshold"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument initial_delay", value=initial_delay, expected_type=type_hints["initial_delay"])
            check_type(argname="argument interval_seconds", value=interval_seconds, expected_type=type_hints["interval_seconds"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument success_count_threshold", value=success_count_threshold, expected_type=type_hints["success_count_threshold"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "transport": transport,
        }
        if failure_count_threshold is not None:
            self._values["failure_count_threshold"] = failure_count_threshold
        if header is not None:
            self._values["header"] = header
        if host is not None:
            self._values["host"] = host
        if initial_delay is not None:
            self._values["initial_delay"] = initial_delay
        if interval_seconds is not None:
            self._values["interval_seconds"] = interval_seconds
        if path is not None:
            self._values["path"] = path
        if success_count_threshold is not None:
            self._values["success_count_threshold"] = success_count_threshold
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port number on which to connect. Possible values are between ``1`` and ``65535``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#port ContainerAppJob#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def transport(self) -> builtins.str:
        '''Type of probe. Possible values are ``TCP``, ``HTTP``, and ``HTTPS``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#transport ContainerAppJob#transport}
        '''
        result = self._values.get("transport")
        assert result is not None, "Required property 'transport' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def failure_count_threshold(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive failures required to consider this probe as failed.

        Possible values are between ``1`` and ``30``. Defaults to ``3``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#failure_count_threshold ContainerAppJob#failure_count_threshold}
        '''
        result = self._values.get("failure_count_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerReadinessProbeHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#header ContainerAppJob#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerReadinessProbeHeader"]]], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''The probe hostname.

        Defaults to the pod IP address. Setting a value for ``Host`` in ``headers`` can be used to override this for ``http`` and ``https`` type probes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#host ContainerAppJob#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_delay(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds elapsed after the container has started before the probe is initiated.

        Possible values are between ``0`` and ``60``. Defaults to ``0`` seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#initial_delay ContainerAppJob#initial_delay}
        '''
        result = self._values.get("initial_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often, in seconds, the probe should run. Possible values are between ``1`` and ``240``. Defaults to ``10``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#interval_seconds ContainerAppJob#interval_seconds}
        '''
        result = self._values.get("interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The URI to use for http type probes. Not valid for ``TCP`` type probes. Defaults to ``/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#path ContainerAppJob#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def success_count_threshold(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive successful responses required to consider this probe as successful.

        Possible values are between ``1`` and ``10``. Defaults to ``3``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#success_count_threshold ContainerAppJob#success_count_threshold}
        '''
        result = self._values.get("success_count_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Time in seconds after which the probe times out. Possible values are between ``1`` an ``240``. Defaults to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#timeout ContainerAppJob#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobTemplateContainerReadinessProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerReadinessProbeHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ContainerAppJobTemplateContainerReadinessProbeHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: The HTTP Header Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        :param value: The HTTP Header value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#value ContainerAppJob#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a455162272890bcf289098f120727c39bef548fd5f9f0d41485fbcbbb60529de)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The HTTP Header Name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The HTTP Header value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#value ContainerAppJob#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobTemplateContainerReadinessProbeHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppJobTemplateContainerReadinessProbeHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerReadinessProbeHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42ee13fdb769a744014576a097761ef2ecb7aa875d4c70e375580cb74929cb2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppJobTemplateContainerReadinessProbeHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d5f2ae9bc1eb27a23e2875c34557878b3348401ea541007817a93a039cba1a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobTemplateContainerReadinessProbeHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d8111c7df289bd5c52f6ac60281f2210bf1e371f9bc0698e33980746d173bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3526cfea8e56d6d63081b0d8036e3585f43e1642f65847da0eb33f38763bce3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5710c97895a4e7e0a5559f51fbdea3df53bb2e32e94e0d5c1b3f7ce6ad216f7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerReadinessProbeHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerReadinessProbeHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerReadinessProbeHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__914a1f5449740ca5e50b858359e46655ca5d350e8383fb06c5e71c40fbca1d4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateContainerReadinessProbeHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerReadinessProbeHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c7cad65ff8abc0c72f5b8cd196970c2b635b7e1c941394f360832a97e256402)
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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00193ca871919b3fb5842e5bec24885e9f80eaac88d6affc5bc3728612c9454e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f00159b0457100cc54ec84ff2edc86849cfa8cf076301531481c537bfa1ca716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerReadinessProbeHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerReadinessProbeHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerReadinessProbeHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d98d8bd139b54bd55f4f2eea0c1c5def72153580b63b26d065978ab9ff681d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateContainerReadinessProbeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerReadinessProbeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0745733ac81c72de96731c5717975d39cb8d2f61d64d79f2d8bda0ff90a6955)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppJobTemplateContainerReadinessProbeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe0e40b0480f9507e50a77aa2be364a79f5271d274a7d30e3a78069935e3b34a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobTemplateContainerReadinessProbeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67e68a0a090956511c4fc4c76f1622e59aff11b7fff09d18f9b2e64b0e59e101)
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
            type_hints = typing.get_type_hints(_typecheckingstub__557c57c17539227a18598ad4b7d4620e74dbead6cbf81883c7a159aead96d46d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed29a2ba14768e5e28d4cadcf3fe83f65c863030cc35a4802ac876e0bdf1d74c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerReadinessProbe]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerReadinessProbe]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerReadinessProbe]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5da69b2463ca253bb82fa4f082666bb0b7ec279167562681f67eab064e55cb7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateContainerReadinessProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerReadinessProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f0b2d600216a084adce29bfef9bf56a2e97485a0d850eaa4222974254c6ce17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerReadinessProbeHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60c5dd2a77ee35ac124b53f6bfe58fd0754e78330d48247da807fcb760ebb3d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="resetFailureCountThreshold")
    def reset_failure_count_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureCountThreshold", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetInitialDelay")
    def reset_initial_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialDelay", []))

    @jsii.member(jsii_name="resetIntervalSeconds")
    def reset_interval_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalSeconds", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetSuccessCountThreshold")
    def reset_success_count_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessCountThreshold", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> ContainerAppJobTemplateContainerReadinessProbeHeaderList:
        return typing.cast(ContainerAppJobTemplateContainerReadinessProbeHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="failureCountThresholdInput")
    def failure_count_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureCountThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerReadinessProbeHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerReadinessProbeHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="initialDelayInput")
    def initial_delay_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalSecondsInput")
    def interval_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="successCountThresholdInput")
    def success_count_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "successCountThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="transportInput")
    def transport_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transportInput"))

    @builtins.property
    @jsii.member(jsii_name="failureCountThreshold")
    def failure_count_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureCountThreshold"))

    @failure_count_threshold.setter
    def failure_count_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e63e432acff5f748cdb4b96ff87847385ecf53471c1673d4d6fe32b566a41717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureCountThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5492216632294d5a79a021694ae2aca748700d248d82bcbc42c75257cbc49e99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelay")
    def initial_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelay"))

    @initial_delay.setter
    def initial_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92606450fb5f3347ae355af444b793732b71fb910833f417120224655e84d32f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSeconds")
    def interval_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSeconds"))

    @interval_seconds.setter
    def interval_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba61bd342e785673d4f4dce364034cd5485abe62008f342b1ea4c6badf5b032b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aedbc8bf4496da9a0694d1d91cfc06e711292005f2567ba4b405d3a70b5c9241)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72838ae6f1fba9e20b7ac3851dffdee448667e9c30614c0cc1b08431ad611895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successCountThreshold")
    def success_count_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successCountThreshold"))

    @success_count_threshold.setter
    def success_count_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92e548c740e4e42149af3dbc8fcd7b87548d4809e166294055610ad124af38e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successCountThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ac364bc31abea46ab632106811a5ee9bec273f22fe62e82a7b1c1ab0b2d18e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transport")
    def transport(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transport"))

    @transport.setter
    def transport(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5053532de363378a089e4b84f5f89a87b58873f2c61e818483d985f4d4de681d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerReadinessProbe]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerReadinessProbe]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerReadinessProbe]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9083e202f2241b5e71e194308b4e1248387fb6abb172792f2a684c36ecd4509f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerStartupProbe",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "transport": "transport",
        "failure_count_threshold": "failureCountThreshold",
        "header": "header",
        "host": "host",
        "initial_delay": "initialDelay",
        "interval_seconds": "intervalSeconds",
        "path": "path",
        "timeout": "timeout",
    },
)
class ContainerAppJobTemplateContainerStartupProbe:
    def __init__(
        self,
        *,
        port: jsii.Number,
        transport: builtins.str,
        failure_count_threshold: typing.Optional[jsii.Number] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateContainerStartupProbeHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        host: typing.Optional[builtins.str] = None,
        initial_delay: typing.Optional[jsii.Number] = None,
        interval_seconds: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param port: The port number on which to connect. Possible values are between ``1`` and ``65535``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#port ContainerAppJob#port}
        :param transport: Type of probe. Possible values are ``TCP``, ``HTTP``, and ``HTTPS``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#transport ContainerAppJob#transport}
        :param failure_count_threshold: The number of consecutive failures required to consider this probe as failed. Possible values are between ``1`` and ``30``. Defaults to ``3``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#failure_count_threshold ContainerAppJob#failure_count_threshold}
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#header ContainerAppJob#header}
        :param host: The probe hostname. Defaults to the pod IP address. Setting a value for ``Host`` in ``headers`` can be used to override this for ``http`` and ``https`` type probes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#host ContainerAppJob#host}
        :param initial_delay: The number of seconds elapsed after the container has started before the probe is initiated. Possible values are between ``0`` and ``60``. Defaults to ``0`` seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#initial_delay ContainerAppJob#initial_delay}
        :param interval_seconds: How often, in seconds, the probe should run. Possible values are between ``1`` and ``240``. Defaults to ``10``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#interval_seconds ContainerAppJob#interval_seconds}
        :param path: The URI to use with the ``host`` for http type probes. Not valid for ``TCP`` type probes. Defaults to ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#path ContainerAppJob#path}
        :param timeout: Time in seconds after which the probe times out. Possible values are between ``1`` an ``240``. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#timeout ContainerAppJob#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7442fbe3a061998abe8d308e6a1350364fb10e7e70084ab081e93d9c4e9a5f9d)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument transport", value=transport, expected_type=type_hints["transport"])
            check_type(argname="argument failure_count_threshold", value=failure_count_threshold, expected_type=type_hints["failure_count_threshold"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument initial_delay", value=initial_delay, expected_type=type_hints["initial_delay"])
            check_type(argname="argument interval_seconds", value=interval_seconds, expected_type=type_hints["interval_seconds"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "transport": transport,
        }
        if failure_count_threshold is not None:
            self._values["failure_count_threshold"] = failure_count_threshold
        if header is not None:
            self._values["header"] = header
        if host is not None:
            self._values["host"] = host
        if initial_delay is not None:
            self._values["initial_delay"] = initial_delay
        if interval_seconds is not None:
            self._values["interval_seconds"] = interval_seconds
        if path is not None:
            self._values["path"] = path
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port number on which to connect. Possible values are between ``1`` and ``65535``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#port ContainerAppJob#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def transport(self) -> builtins.str:
        '''Type of probe. Possible values are ``TCP``, ``HTTP``, and ``HTTPS``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#transport ContainerAppJob#transport}
        '''
        result = self._values.get("transport")
        assert result is not None, "Required property 'transport' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def failure_count_threshold(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive failures required to consider this probe as failed.

        Possible values are between ``1`` and ``30``. Defaults to ``3``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#failure_count_threshold ContainerAppJob#failure_count_threshold}
        '''
        result = self._values.get("failure_count_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerStartupProbeHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#header ContainerAppJob#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateContainerStartupProbeHeader"]]], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''The probe hostname.

        Defaults to the pod IP address. Setting a value for ``Host`` in ``headers`` can be used to override this for ``http`` and ``https`` type probes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#host ContainerAppJob#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_delay(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds elapsed after the container has started before the probe is initiated.

        Possible values are between ``0`` and ``60``. Defaults to ``0`` seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#initial_delay ContainerAppJob#initial_delay}
        '''
        result = self._values.get("initial_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often, in seconds, the probe should run. Possible values are between ``1`` and ``240``. Defaults to ``10``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#interval_seconds ContainerAppJob#interval_seconds}
        '''
        result = self._values.get("interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The URI to use with the ``host`` for http type probes.

        Not valid for ``TCP`` type probes. Defaults to ``/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#path ContainerAppJob#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Time in seconds after which the probe times out. Possible values are between ``1`` an ``240``. Defaults to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#timeout ContainerAppJob#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobTemplateContainerStartupProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerStartupProbeHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ContainerAppJobTemplateContainerStartupProbeHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: The HTTP Header Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        :param value: The HTTP Header value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#value ContainerAppJob#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cfa8a3f018cf5d5857d290451541f92e44a2b2fc65fec1e84e45af244e1fdea)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The HTTP Header Name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The HTTP Header value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#value ContainerAppJob#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobTemplateContainerStartupProbeHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppJobTemplateContainerStartupProbeHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerStartupProbeHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c6768d004af77c4452b18ef99ca6b8ccc8b99713f9bc43c3f13bc6830196587)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppJobTemplateContainerStartupProbeHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077aa69e055640a88023dcb06a37a3662550a462da5500a787ee6681b90dc752)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobTemplateContainerStartupProbeHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae30b52c2c8779f8203fb43bca621bf43a212b7e17d53fa311a95a3b9222040)
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
            type_hints = typing.get_type_hints(_typecheckingstub__024547cf81ba43ab31ed7c7f44c75ebd2ebc34c0c2a4b8b190e9e00dbaee62fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__845e39d724badc3ec69c42688e2a3851fc1d4829a51f4bddb95f5b9786dd4f16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerStartupProbeHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerStartupProbeHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerStartupProbeHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2bbe0865e2872dce7395f43934f8a7fe119baffb29878a126eb21c36f7c3c8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateContainerStartupProbeHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerStartupProbeHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a98105fe84e05866b7438d33a4f423a7d907caa11c63d8c03da370416a36002)
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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ecf52170a578810d289dc0ceb4cee196589bd5faae12856d272d83c5b8084b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bfb9217091011a8ea88a1391281828841dd98a5f55a69521f0847156566be69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerStartupProbeHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerStartupProbeHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerStartupProbeHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__373fb4d7bb59270eb307715cf847b5d4ff835d2080fdef9c51708f1dae356819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateContainerStartupProbeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerStartupProbeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ba9323c84118513c2cc5bc767b250e3c8d6289739f16abeebd2eec060a8fe57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppJobTemplateContainerStartupProbeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d193bd0cf4f5490158a176c14dd9f2e21e530df76ab447429fd94ef579030fb5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobTemplateContainerStartupProbeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74463c48e5d66fcca9977b1477fa303ea56c5336f373306b216f1bb6ff7f5f1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65d5defd3b5f42fedc49ae272a11d7984a2701c52bb47c222aaf037eb4288477)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f69547dcfbe016c26b284ea90c39bb2c4ccbf8c93c9223c6b94326ea2710b96a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerStartupProbe]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerStartupProbe]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerStartupProbe]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__994f80b6237cfdac3111a9e10d12e9514d465a4891e8dcb23d8d5af943253610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateContainerStartupProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerStartupProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad6ae123e4d8bff93b4d47847e55547afda7b77a618bc7ddcea96ce2606a56e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerStartupProbeHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b86930a3cba691a41f16043cb7c488c1215f620c0e64f2df01702026ee942552)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="resetFailureCountThreshold")
    def reset_failure_count_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureCountThreshold", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetInitialDelay")
    def reset_initial_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialDelay", []))

    @jsii.member(jsii_name="resetIntervalSeconds")
    def reset_interval_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalSeconds", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> ContainerAppJobTemplateContainerStartupProbeHeaderList:
        return typing.cast(ContainerAppJobTemplateContainerStartupProbeHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="terminationGracePeriodSeconds")
    def termination_grace_period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "terminationGracePeriodSeconds"))

    @builtins.property
    @jsii.member(jsii_name="failureCountThresholdInput")
    def failure_count_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureCountThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerStartupProbeHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerStartupProbeHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="initialDelayInput")
    def initial_delay_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalSecondsInput")
    def interval_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="transportInput")
    def transport_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transportInput"))

    @builtins.property
    @jsii.member(jsii_name="failureCountThreshold")
    def failure_count_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureCountThreshold"))

    @failure_count_threshold.setter
    def failure_count_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6998d249463a7849aa7927ed3e2e3959a5bac1bf99c0a6ebbe1d600c98b2f141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureCountThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7c96f4a9f2dd485f945306dd0d3c66fe1e1d7a972735728fd262521ac1f88cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelay")
    def initial_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelay"))

    @initial_delay.setter
    def initial_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab899ff472bea6274d6570f0be05b3af0883b9ba0a65339d9f9f821933caf98c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSeconds")
    def interval_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSeconds"))

    @interval_seconds.setter
    def interval_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__502b6c55c83a3c113bf1ff4027588e3cc436846c89de8d3ecbb3f3861805e844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc1e46b49d85f67b834965339d85e744acef66c47a28be41e41caa6c80b773a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a200faa19f66b581df3c08e4469a2b74895c800d5e12e89cd559d2db2dce2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__954ebfe758d5aa28755f4a56d568ba0443a34a0be98fc7a0a91215dcd8ee6e15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transport")
    def transport(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transport"))

    @transport.setter
    def transport(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__188d9e2e41a909202cb565546f7cb456fbbeb51ca1fba58f16591f97a431ebc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerStartupProbe]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerStartupProbe]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerStartupProbe]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba2063877e22fd5b0b82a07ebcb2cb666d90c5685ce0454a0bcc1f908f831d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerVolumeMounts",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "sub_path": "subPath"},
)
class ContainerAppJobTemplateContainerVolumeMounts:
    def __init__(
        self,
        *,
        name: builtins.str,
        path: builtins.str,
        sub_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the Volume to be mounted in the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        :param path: The path in the container at which to mount this volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#path ContainerAppJob#path}
        :param sub_path: The sub path of the volume to be mounted in the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#sub_path ContainerAppJob#sub_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f026b81d18f038d1031d6bdb4dc34f323e036aee2a37cc8307c3818987e198e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument sub_path", value=sub_path, expected_type=type_hints["sub_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "path": path,
        }
        if sub_path is not None:
            self._values["sub_path"] = sub_path

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Volume to be mounted in the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The path in the container at which to mount this volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#path ContainerAppJob#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sub_path(self) -> typing.Optional[builtins.str]:
        '''The sub path of the volume to be mounted in the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#sub_path ContainerAppJob#sub_path}
        '''
        result = self._values.get("sub_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobTemplateContainerVolumeMounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppJobTemplateContainerVolumeMountsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerVolumeMountsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7d12a903356bb0af06f12aeebdb0ae326eab727b4635216e29d4112e927aaf9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppJobTemplateContainerVolumeMountsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5458f3e5e9449adcb264cce09e936adb328f9866807fc0ffd3c2ba7604ece285)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobTemplateContainerVolumeMountsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d81ad9b085769a6397048f86ec8ee631a65d51b811937540537a772f8e5925)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ed209e7eab1130f1d192abeed0bd7f0f521dbee5c07a1c24ac17fa24def6393)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49f45415ca0c6b7f931866e5ccc3a40d9b847c113cb87212c307dd230b4d02ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerVolumeMounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerVolumeMounts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerVolumeMounts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee6e4a8e0b4826b446d861d38eb8d062a632107f160eb15ffbfdb3ccc65cc67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateContainerVolumeMountsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateContainerVolumeMountsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d73fa996276efd5cce8302138bc9c208ffd6a51c9d32571bb72f3d10a61a021d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSubPath")
    def reset_sub_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubPath", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="subPathInput")
    def sub_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subPathInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b2e1dd696f1ada0dca55c0b26101ce768654feb7979e34d6cdbf6a0c07ce76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38bd58efe1a08cdc4758a60f06b9fa7d3ee6a4f4422f2250c1d5c9fc62a258f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subPath")
    def sub_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subPath"))

    @sub_path.setter
    def sub_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7113dfc841112c7dd8db3f0b9e972ec1387ab582332ed36e64a835be35e8aec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerVolumeMounts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerVolumeMounts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerVolumeMounts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab1d52b184eb9547bfc70f24085b33456c74f49f10496504dd1732e95cabcc76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateInitContainer",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "name": "name",
        "args": "args",
        "command": "command",
        "cpu": "cpu",
        "env": "env",
        "memory": "memory",
        "volume_mounts": "volumeMounts",
    },
)
class ContainerAppJobTemplateInitContainer:
    def __init__(
        self,
        *,
        image: builtins.str,
        name: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        cpu: typing.Optional[jsii.Number] = None,
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateInitContainerEnv", typing.Dict[builtins.str, typing.Any]]]]] = None,
        memory: typing.Optional[builtins.str] = None,
        volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateInitContainerVolumeMounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param image: The image to use to create the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#image ContainerAppJob#image}
        :param name: The name of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        :param args: A list of args to pass to the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#args ContainerAppJob#args}
        :param command: A command to pass to the container to override the default. This is provided as a list of command line elements without spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#command ContainerAppJob#command}
        :param cpu: The amount of vCPU to allocate to the container. Possible values include ``0.25``, ``0.5``, ``0.75``, ``1.0``, ``1.25``, ``1.5``, ``1.75``, and ``2.0``. **NOTE:** ``cpu`` and ``memory`` must be specified in ``0.25'/'0.5Gi`` combination increments. e.g. ``1.0`` / ``2.0`` or ``0.5`` / ``1.0``. When there's a workload profile specified, there's no such constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#cpu ContainerAppJob#cpu}
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#env ContainerAppJob#env}
        :param memory: The amount of memory to allocate to the container. Possible values include ``0.5Gi``, ``1.0Gi``, ``1.5Gi``, ``2.0Gi``, ``2.5Gi``, ``3.0Gi``, ``3.5Gi``, and ``4.0Gi``. **NOTE:** ``cpu`` and ``memory`` must be specified in ``0.25'/'0.5Gi`` combination increments. e.g. ``1.25`` / ``2.5Gi`` or ``0.75`` / ``1.5Gi``. When there's a workload profile specified, there's no such constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#memory ContainerAppJob#memory}
        :param volume_mounts: volume_mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#volume_mounts ContainerAppJob#volume_mounts}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5deac8fd878404d54f964e6c3580728b94fd6055492477d2d690de82d620b57d)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument volume_mounts", value=volume_mounts, expected_type=type_hints["volume_mounts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
            "name": name,
        }
        if args is not None:
            self._values["args"] = args
        if command is not None:
            self._values["command"] = command
        if cpu is not None:
            self._values["cpu"] = cpu
        if env is not None:
            self._values["env"] = env
        if memory is not None:
            self._values["memory"] = memory
        if volume_mounts is not None:
            self._values["volume_mounts"] = volume_mounts

    @builtins.property
    def image(self) -> builtins.str:
        '''The image to use to create the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#image ContainerAppJob#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of args to pass to the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#args ContainerAppJob#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A command to pass to the container to override the default.

        This is provided as a list of command line elements without spaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#command ContainerAppJob#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''The amount of vCPU to allocate to the container.

        Possible values include ``0.25``, ``0.5``, ``0.75``, ``1.0``, ``1.25``, ``1.5``, ``1.75``, and ``2.0``. **NOTE:** ``cpu`` and ``memory`` must be specified in ``0.25'/'0.5Gi`` combination increments. e.g. ``1.0`` / ``2.0`` or ``0.5`` / ``1.0``. When there's a workload profile specified, there's no such constraint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#cpu ContainerAppJob#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def env(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateInitContainerEnv"]]]:
        '''env block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#env ContainerAppJob#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateInitContainerEnv"]]], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''The amount of memory to allocate to the container.

        Possible values include ``0.5Gi``, ``1.0Gi``, ``1.5Gi``, ``2.0Gi``, ``2.5Gi``, ``3.0Gi``, ``3.5Gi``, and ``4.0Gi``. **NOTE:** ``cpu`` and ``memory`` must be specified in ``0.25'/'0.5Gi`` combination increments. e.g. ``1.25`` / ``2.5Gi`` or ``0.75`` / ``1.5Gi``. When there's a workload profile specified, there's no such constraint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#memory ContainerAppJob#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_mounts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateInitContainerVolumeMounts"]]]:
        '''volume_mounts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#volume_mounts ContainerAppJob#volume_mounts}
        '''
        result = self._values.get("volume_mounts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateInitContainerVolumeMounts"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobTemplateInitContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateInitContainerEnv",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "secret_name": "secretName", "value": "value"},
)
class ContainerAppJobTemplateInitContainerEnv:
    def __init__(
        self,
        *,
        name: builtins.str,
        secret_name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the environment variable for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        :param secret_name: The name of the secret that contains the value for this environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#secret_name ContainerAppJob#secret_name}
        :param value: The value for this environment variable. **NOTE:** This value is ignored if ``secret_name`` is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#value ContainerAppJob#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__103550d068e9d061ad0cd4c05371109edd386bd9ce685fc5d9bd50118e6baa60)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if secret_name is not None:
            self._values["secret_name"] = secret_name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the environment variable for the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_name(self) -> typing.Optional[builtins.str]:
        '''The name of the secret that contains the value for this environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#secret_name ContainerAppJob#secret_name}
        '''
        result = self._values.get("secret_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The value for this environment variable. **NOTE:** This value is ignored if ``secret_name`` is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#value ContainerAppJob#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobTemplateInitContainerEnv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppJobTemplateInitContainerEnvList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateInitContainerEnvList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f12a0275f3ffdb2c4e9f53ec5d5ed43428dae1879d3d3485d834bec666cc6234)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppJobTemplateInitContainerEnvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c30138055584ca2d3a90d6807ed390318a9a2bd59f05fc76765c8ebc0667a143)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobTemplateInitContainerEnvOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49959f0aba80191baaae7a40624815c484229129cbbb0a4dd55bb68ad4d593ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62ac71ec8ebd37e08987a65b1e118c7089c513970c4a227543fe0d4fcf8ed42a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d169e286c08b81fbf81a4af7d5f13373226942f562da8159269d5c2805c26a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateInitContainerEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateInitContainerEnv]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateInitContainerEnv]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145a706a5d8333ade09196fe04b4a636f412920fe762675dcb13ea96dd098f88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateInitContainerEnvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateInitContainerEnvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b86d9c308687b32f991f65371578809d3d9a05ccc3a0b3612916dcda3985869f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSecretName")
    def reset_secret_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b92f45516bd52d54acbcea5cda7f24cd0410279955f897310fda891756776107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af88efcea5cd2571233d9f0d7253778810fe448c226d511483a3b75f0277360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d0cbb458b92601b3fedcd66fd5a89a7d2697094739aa522052f253398df9de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateInitContainerEnv]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateInitContainerEnv]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateInitContainerEnv]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__055ebe3d7d3d0281302ecdf3d02febe28c1fd2d1016e493d50416ef4b9a2336e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateInitContainerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateInitContainerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c863d48557b4941d07c7820334b9729c57d7151b3c8579725a34909eb9696a4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppJobTemplateInitContainerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb29aef03905a707e672dd88e0dc5159fb25cae5c4aaa14ad174f386affdc27)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobTemplateInitContainerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90563857b8a352b49ca5bb469393cd0d917a1bc966feed916857c623d04fa00a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad1829bf4e61d405792e6fcd2d672b7b7e77c1326f0d440410e42b1ba843f476)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59fc6477e63a7b4eaefeb8765b309dc4115df8f2a759282e0945821de082622a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateInitContainer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateInitContainer]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateInitContainer]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__906bdd068b92f884f69fee29936a5ec4a45428e5414a884673fe5996fb7d43fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateInitContainerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateInitContainerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__076c810f0255ef66f12026dbc923c99c0c742446540675fdf032ddd9a515bb5d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEnv")
    def put_env(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateInitContainerEnv, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__735317d266a39e58909661f83ab5353e85ccabb095653bd12e986913757ac7c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnv", [value]))

    @jsii.member(jsii_name="putVolumeMounts")
    def put_volume_mounts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateInitContainerVolumeMounts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfa18f158deeb7e9821b5fb48aed6093f1c7515c4601e26db001fd02a889b922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumeMounts", [value]))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @jsii.member(jsii_name="resetVolumeMounts")
    def reset_volume_mounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeMounts", []))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> ContainerAppJobTemplateInitContainerEnvList:
        return typing.cast(ContainerAppJobTemplateInitContainerEnvList, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorage")
    def ephemeral_storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ephemeralStorage"))

    @builtins.property
    @jsii.member(jsii_name="volumeMounts")
    def volume_mounts(self) -> "ContainerAppJobTemplateInitContainerVolumeMountsList":
        return typing.cast("ContainerAppJobTemplateInitContainerVolumeMountsList", jsii.get(self, "volumeMounts"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateInitContainerEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateInitContainerEnv]]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeMountsInput")
    def volume_mounts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateInitContainerVolumeMounts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateInitContainerVolumeMounts"]]], jsii.get(self, "volumeMountsInput"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c13d2b1d2fd9d0401f1846238452766da60624102412122329505e840ba676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e130f3f51989873b7d9553c4b0b6855bea026e02cf749b0acbcb31fb6c56096f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5986ede0d5e1f3160fa348e55b9f3048c5d10a82109d981fca0713cab97088b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae7de880c40f2976cd3521d6c4ed9d7f40c70b64026243a86dd02979e8f23750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24bb3f58af9482c5a5313e93f2bd9579896158db65e3cba781c7c9bb92df9758)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9581dcf34246648ec6d608a5f95e0329a7f2a913b833a1aea473b7f088c9e57e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateInitContainer]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateInitContainer]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateInitContainer]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1955bf1816c1d5850000d33392f11eb9f504abd38affd2de76de1e8b96ed0034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateInitContainerVolumeMounts",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "sub_path": "subPath"},
)
class ContainerAppJobTemplateInitContainerVolumeMounts:
    def __init__(
        self,
        *,
        name: builtins.str,
        path: builtins.str,
        sub_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the Volume to be mounted in the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        :param path: The path in the container at which to mount this volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#path ContainerAppJob#path}
        :param sub_path: The sub path of the volume to be mounted in the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#sub_path ContainerAppJob#sub_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9a848fda985daa332434f949a0ab9167c2cb678ba93eea487ac6f849e37e8c6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument sub_path", value=sub_path, expected_type=type_hints["sub_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "path": path,
        }
        if sub_path is not None:
            self._values["sub_path"] = sub_path

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Volume to be mounted in the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The path in the container at which to mount this volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#path ContainerAppJob#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sub_path(self) -> typing.Optional[builtins.str]:
        '''The sub path of the volume to be mounted in the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#sub_path ContainerAppJob#sub_path}
        '''
        result = self._values.get("sub_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobTemplateInitContainerVolumeMounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppJobTemplateInitContainerVolumeMountsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateInitContainerVolumeMountsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__790332075bc529e40d12cc41d5718d7e3d5d3364f67f2657153a5452a393e381)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppJobTemplateInitContainerVolumeMountsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6d4e8b7c7b653e97586300ebb05014c8df20def92f3fcf79577263e307b6bb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobTemplateInitContainerVolumeMountsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52458865d22f121bcefcb5bf7dcee894ad572dcc32eead3f3d50f83948857c3f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa5792a397df84ed7a51da15efec45da203e31927515a89c2d92d8b889e8072f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b54b3dde98cf48a0c5eac7c9908f2d7d3e6947669d878e3e3d1745588845100e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateInitContainerVolumeMounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateInitContainerVolumeMounts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateInitContainerVolumeMounts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b596112a36e688873f62389c7bfeb0e4fbba755f5d5a8fb9e06d00f00be859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateInitContainerVolumeMountsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateInitContainerVolumeMountsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1efea6b25d689579c6447accd64403b67b40f6f3853bfbc74fd760be2a60eb82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSubPath")
    def reset_sub_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubPath", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="subPathInput")
    def sub_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subPathInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__419b5b904c8fcabff1e28746a06e2e238fd6692e7e5a6b651a22c04d4dfeb54e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42fffe2105a4da3d5e3a79359293484e19271dac22abead00969eca02f9b327c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subPath")
    def sub_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subPath"))

    @sub_path.setter
    def sub_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcad510a010d86bd7a1dc08b29b484be58d82396a67c9340836007e11b76051c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateInitContainerVolumeMounts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateInitContainerVolumeMounts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateInitContainerVolumeMounts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624daf760a4c30a0397dd8d77d9c1bf05d44b1f1aea416287c512f900592ee65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1334cc449964662fa04289928738e52cc5a4deeafd08890723fe49dddf72535a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContainer")
    def put_container(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainer, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e73fc2315ae15242bed23c3ca0f723e7551750444844630a087ecd6db06cf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainer", [value]))

    @jsii.member(jsii_name="putInitContainer")
    def put_init_container(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateInitContainer, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3312d31f86af86503a273e41c113ab39709557c8c48c25f7737b96616e524b6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInitContainer", [value]))

    @jsii.member(jsii_name="putVolume")
    def put_volume(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppJobTemplateVolume", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b0fab980c16738bc4393088d3e9ced11459ecf5465efb61b9cb1801ce47bf5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolume", [value]))

    @jsii.member(jsii_name="resetInitContainer")
    def reset_init_container(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitContainer", []))

    @jsii.member(jsii_name="resetVolume")
    def reset_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolume", []))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> ContainerAppJobTemplateContainerList:
        return typing.cast(ContainerAppJobTemplateContainerList, jsii.get(self, "container"))

    @builtins.property
    @jsii.member(jsii_name="initContainer")
    def init_container(self) -> ContainerAppJobTemplateInitContainerList:
        return typing.cast(ContainerAppJobTemplateInitContainerList, jsii.get(self, "initContainer"))

    @builtins.property
    @jsii.member(jsii_name="volume")
    def volume(self) -> "ContainerAppJobTemplateVolumeList":
        return typing.cast("ContainerAppJobTemplateVolumeList", jsii.get(self, "volume"))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainer]]], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="initContainerInput")
    def init_container_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateInitContainer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateInitContainer]]], jsii.get(self, "initContainerInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeInput")
    def volume_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateVolume"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppJobTemplateVolume"]]], jsii.get(self, "volumeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAppJobTemplate]:
        return typing.cast(typing.Optional[ContainerAppJobTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ContainerAppJobTemplate]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f277ce390c2adeda019796f6b49bd52cb022cdeb3875ff944c23e119be81ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateVolume",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "mount_options": "mountOptions",
        "storage_name": "storageName",
        "storage_type": "storageType",
    },
)
class ContainerAppJobTemplateVolume:
    def __init__(
        self,
        *,
        name: builtins.str,
        mount_options: typing.Optional[builtins.str] = None,
        storage_name: typing.Optional[builtins.str] = None,
        storage_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        :param mount_options: Mount options used while mounting the AzureFile. Must be a comma-separated string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#mount_options ContainerAppJob#mount_options}
        :param storage_name: The name of the ``AzureFile`` storage. Required when ``storage_type`` is ``AzureFile``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#storage_name ContainerAppJob#storage_name}
        :param storage_type: The type of storage volume. Possible values include ``AzureFile`` and ``EmptyDir``. Defaults to ``EmptyDir``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#storage_type ContainerAppJob#storage_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d929009b0101d464a87fa7a9f35847c1f07f7d88cae30f58b1d1d4812a7fde25)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
            check_type(argname="argument storage_name", value=storage_name, expected_type=type_hints["storage_name"])
            check_type(argname="argument storage_type", value=storage_type, expected_type=type_hints["storage_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if mount_options is not None:
            self._values["mount_options"] = mount_options
        if storage_name is not None:
            self._values["storage_name"] = storage_name
        if storage_type is not None:
            self._values["storage_type"] = storage_type

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#name ContainerAppJob#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mount_options(self) -> typing.Optional[builtins.str]:
        '''Mount options used while mounting the AzureFile. Must be a comma-separated string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#mount_options ContainerAppJob#mount_options}
        '''
        result = self._values.get("mount_options")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_name(self) -> typing.Optional[builtins.str]:
        '''The name of the ``AzureFile`` storage. Required when ``storage_type`` is ``AzureFile``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#storage_name ContainerAppJob#storage_name}
        '''
        result = self._values.get("storage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_type(self) -> typing.Optional[builtins.str]:
        '''The type of storage volume. Possible values include ``AzureFile`` and ``EmptyDir``. Defaults to ``EmptyDir``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#storage_type ContainerAppJob#storage_type}
        '''
        result = self._values.get("storage_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobTemplateVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppJobTemplateVolumeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateVolumeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f485d294f0c92b73d5ec513eba2d879a7aac8cf0adafffe87fe678be5a8a172)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ContainerAppJobTemplateVolumeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10b473ca7baa41120b836ec02f467b84f855b8bc39cd75d212d579cadb9cfa5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppJobTemplateVolumeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f6f271983d26da9fc0704f276b61d4e9aefec5f6c4a3159b83011c78b0e206)
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
            type_hints = typing.get_type_hints(_typecheckingstub__806d0d15fb7d5d1924e621b2648148a14e916779dcb1b3612b6fc0c9f3417d22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2860a2995dc8c3182c272a719a52bf7f835471901a62be9c3d37f2ede34425b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateVolume]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateVolume]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateVolume]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea9ac526cfd1a773a745a46468302718ae59f9a133bb80526eb22e68ec4754b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppJobTemplateVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTemplateVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6bb1a17aee58946aecb21c0574593217d1df662728bb0441babb555341f37ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMountOptions")
    def reset_mount_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMountOptions", []))

    @jsii.member(jsii_name="resetStorageName")
    def reset_storage_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageName", []))

    @jsii.member(jsii_name="resetStorageType")
    def reset_storage_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageType", []))

    @builtins.property
    @jsii.member(jsii_name="mountOptionsInput")
    def mount_options_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageNameInput")
    def storage_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageTypeInput")
    def storage_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="mountOptions")
    def mount_options(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountOptions"))

    @mount_options.setter
    def mount_options(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c02a51f4e75566d5ae4eb4ccba7ffef48088eb61233408e990dcb6a9ebe15ff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eda5ab4a0b564d996a9144d773bea7f5601caefcb2e505ef1b8e7b0b6cfc7197)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageName")
    def storage_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageName"))

    @storage_name.setter
    def storage_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc99586ba86250f4fde9d5624655f654cbeac46ebdc2a3a5b2cf74ba0178886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageType")
    def storage_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageType"))

    @storage_type.setter
    def storage_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9186a8bf76b712c1e6431bf811191531b118920c673c3e5537a5678bb0c99cd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateVolume]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateVolume]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateVolume]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49746f6da3221c2183b66158e6f7402eecd2fc05168e429d9070eae268875dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ContainerAppJobTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#create ContainerAppJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#delete ContainerAppJob#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#read ContainerAppJob#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#update ContainerAppJob#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8452f201b5703548483d9f6436e72c9aab71614fb5f130c1f0d9fe5bcf6a133b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#create ContainerAppJob#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#delete ContainerAppJob#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#read ContainerAppJob#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_job#update ContainerAppJob#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppJobTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppJobTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppJob.ContainerAppJobTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d866fa3f8627d59175983a08060a26c36b49fba9c9cc21f70fed03551eec6632)
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
            type_hints = typing.get_type_hints(_typecheckingstub__194d0646bda92ea76b97eee91d8dd1d9bf3d53cfcd48637ba8d979992bf25f24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0659ba569a0398cfb0ba3fdb744ec425f4a3bbe8b5452282b1617e6bfdfc8d87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e015ac8cd98dced3490e6d87705ae4601b24350d972f92da6f793eec21c4990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed68fc0f50b06e331c5e06407c9faa79c1c6a74be21c27101f088b129e1bfed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c9b80caef22af454a89d4f92f8bec91b3bab7d97a37c50b7b518a491bfcfa99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ContainerAppJob",
    "ContainerAppJobConfig",
    "ContainerAppJobEventTriggerConfig",
    "ContainerAppJobEventTriggerConfigOutputReference",
    "ContainerAppJobEventTriggerConfigScale",
    "ContainerAppJobEventTriggerConfigScaleList",
    "ContainerAppJobEventTriggerConfigScaleOutputReference",
    "ContainerAppJobEventTriggerConfigScaleRules",
    "ContainerAppJobEventTriggerConfigScaleRulesAuthentication",
    "ContainerAppJobEventTriggerConfigScaleRulesAuthenticationList",
    "ContainerAppJobEventTriggerConfigScaleRulesAuthenticationOutputReference",
    "ContainerAppJobEventTriggerConfigScaleRulesList",
    "ContainerAppJobEventTriggerConfigScaleRulesOutputReference",
    "ContainerAppJobIdentity",
    "ContainerAppJobIdentityOutputReference",
    "ContainerAppJobManualTriggerConfig",
    "ContainerAppJobManualTriggerConfigOutputReference",
    "ContainerAppJobRegistry",
    "ContainerAppJobRegistryList",
    "ContainerAppJobRegistryOutputReference",
    "ContainerAppJobScheduleTriggerConfig",
    "ContainerAppJobScheduleTriggerConfigOutputReference",
    "ContainerAppJobSecret",
    "ContainerAppJobSecretList",
    "ContainerAppJobSecretOutputReference",
    "ContainerAppJobTemplate",
    "ContainerAppJobTemplateContainer",
    "ContainerAppJobTemplateContainerEnv",
    "ContainerAppJobTemplateContainerEnvList",
    "ContainerAppJobTemplateContainerEnvOutputReference",
    "ContainerAppJobTemplateContainerList",
    "ContainerAppJobTemplateContainerLivenessProbe",
    "ContainerAppJobTemplateContainerLivenessProbeHeader",
    "ContainerAppJobTemplateContainerLivenessProbeHeaderList",
    "ContainerAppJobTemplateContainerLivenessProbeHeaderOutputReference",
    "ContainerAppJobTemplateContainerLivenessProbeList",
    "ContainerAppJobTemplateContainerLivenessProbeOutputReference",
    "ContainerAppJobTemplateContainerOutputReference",
    "ContainerAppJobTemplateContainerReadinessProbe",
    "ContainerAppJobTemplateContainerReadinessProbeHeader",
    "ContainerAppJobTemplateContainerReadinessProbeHeaderList",
    "ContainerAppJobTemplateContainerReadinessProbeHeaderOutputReference",
    "ContainerAppJobTemplateContainerReadinessProbeList",
    "ContainerAppJobTemplateContainerReadinessProbeOutputReference",
    "ContainerAppJobTemplateContainerStartupProbe",
    "ContainerAppJobTemplateContainerStartupProbeHeader",
    "ContainerAppJobTemplateContainerStartupProbeHeaderList",
    "ContainerAppJobTemplateContainerStartupProbeHeaderOutputReference",
    "ContainerAppJobTemplateContainerStartupProbeList",
    "ContainerAppJobTemplateContainerStartupProbeOutputReference",
    "ContainerAppJobTemplateContainerVolumeMounts",
    "ContainerAppJobTemplateContainerVolumeMountsList",
    "ContainerAppJobTemplateContainerVolumeMountsOutputReference",
    "ContainerAppJobTemplateInitContainer",
    "ContainerAppJobTemplateInitContainerEnv",
    "ContainerAppJobTemplateInitContainerEnvList",
    "ContainerAppJobTemplateInitContainerEnvOutputReference",
    "ContainerAppJobTemplateInitContainerList",
    "ContainerAppJobTemplateInitContainerOutputReference",
    "ContainerAppJobTemplateInitContainerVolumeMounts",
    "ContainerAppJobTemplateInitContainerVolumeMountsList",
    "ContainerAppJobTemplateInitContainerVolumeMountsOutputReference",
    "ContainerAppJobTemplateOutputReference",
    "ContainerAppJobTemplateVolume",
    "ContainerAppJobTemplateVolumeList",
    "ContainerAppJobTemplateVolumeOutputReference",
    "ContainerAppJobTimeouts",
    "ContainerAppJobTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__662028df8d3c118a6e314382274d50cab629f275917bbcfed161936cb94a9ed2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    container_app_environment_id: builtins.str,
    location: builtins.str,
    name: builtins.str,
    replica_timeout_in_seconds: jsii.Number,
    resource_group_name: builtins.str,
    template: typing.Union[ContainerAppJobTemplate, typing.Dict[builtins.str, typing.Any]],
    event_trigger_config: typing.Optional[typing.Union[ContainerAppJobEventTriggerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[ContainerAppJobIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    manual_trigger_config: typing.Optional[typing.Union[ContainerAppJobManualTriggerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    registry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobRegistry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    replica_retry_limit: typing.Optional[jsii.Number] = None,
    schedule_trigger_config: typing.Optional[typing.Union[ContainerAppJobScheduleTriggerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobSecret, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ContainerAppJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_profile_name: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__dc3b69d29847fe38ba62b081905d0c3506ea7426d936ad06b009cb7b96aab3a6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e5f2641976a41c9f140904a3e4c9322f10afa781572688551afb2b84df056b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobRegistry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4f745f9207cebe83e079324ab350923a8064add69870736f94b09fe5c765164(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobSecret, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffdda9b0b8f28ae59e0dbb5ae1ff5fdbe0bdeabdf6e3260fe3e774e79e11aafe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81d33376baa89f2521719bbef2502d69679503d1aeae76716877fcd86d40779(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e95027b448d97df18d5d36c5ecb6626844410788adaecac831c5ab83a077644(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7f7813df2a3372425c183f58fbcefad9392f370fecdea307bc5be679f1902c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cb1be5b4a8d8e3b8cf1eb8fe293a41400aedbd04dffcc2994c2ce3b3f90bab3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10fcb3912722a5c0bd247e21b14192a2ea03c076859d538dca98cf4647fac486(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c27c69a6ecce62ca2e6a7673a43d0f23949cf03ee562fbea22b8764578d44d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01eaf3c0278a1a07f8c98eac807489569c1269de253101bf9b37e99dae3f2713(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d7b152d6fa0b45e1bd1c0fad6a9688f920f88004030595079565965522fe62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba4717d45bed68bc5736e98ab7f959f24eb6d691cf657154aebf6cec39fafbd2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    container_app_environment_id: builtins.str,
    location: builtins.str,
    name: builtins.str,
    replica_timeout_in_seconds: jsii.Number,
    resource_group_name: builtins.str,
    template: typing.Union[ContainerAppJobTemplate, typing.Dict[builtins.str, typing.Any]],
    event_trigger_config: typing.Optional[typing.Union[ContainerAppJobEventTriggerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[ContainerAppJobIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    manual_trigger_config: typing.Optional[typing.Union[ContainerAppJobManualTriggerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    registry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobRegistry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    replica_retry_limit: typing.Optional[jsii.Number] = None,
    schedule_trigger_config: typing.Optional[typing.Union[ContainerAppJobScheduleTriggerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobSecret, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ContainerAppJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_profile_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e602c6cfccce9a0a264d4b8b0676884df0c7b3f55e9be77227e38c75a3fa229(
    *,
    parallelism: typing.Optional[jsii.Number] = None,
    replica_completion_count: typing.Optional[jsii.Number] = None,
    scale: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobEventTriggerConfigScale, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d55a02723ddd9c2ef80684903e19ac60af5531982e1f3589e1ae062cb0df79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef19c94ce44f9721cd7d33eab8fd7f603c75dc057980ec5e43da96260c1a146(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobEventTriggerConfigScale, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56973e9d3486a912df7c3fea6bb1ae277a40eeb0ec0384c80374b2f02b28c131(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5b6093c053dd3af146432260ce0e29025caccd9a997fa2f806dc8bd97109f2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29c9db6823d96a69414e478987240987913ca29812473fe7b56a0082bc93d15(
    value: typing.Optional[ContainerAppJobEventTriggerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f65391973dacdc729ae4eb3829f11be66ed0982bbf0ba61b491c802c8ea99a(
    *,
    max_executions: typing.Optional[jsii.Number] = None,
    min_executions: typing.Optional[jsii.Number] = None,
    polling_interval_in_seconds: typing.Optional[jsii.Number] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobEventTriggerConfigScaleRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83423d340651d4ac252411d48fbde5cc4ea9d44d5a77b719f197a92225e65c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0120db52b69ddab589668870f5c6f1a6775b771a7e2670df875a72062e3d83(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e4c250225349c79c05f1082560e49eca77a487b9fedeaa5b3d97e1b3e83cf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93c99b617cc649bc1d1346269771dce415eb251837240013a19cc4c68abb94e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3677fcc1f9f5c4a8ea0916ce402ef3eb166e7fc573cc07053729adf87165d1b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a5b978f648f4f08837aff3e7ff5b762b35017607db595d3646c5facb540b1a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobEventTriggerConfigScale]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4a94b1da15f9693aec878b9d2ebe49e626c78dec7434aaa241aa607ebf8201(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5542b6b7e4edccba5cd02091677fc441ed04e0eccc69aac1d66ec3bb0bfbbbbd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobEventTriggerConfigScaleRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9025ca7d1baec82ce4628f962cd7f085168d7cd1e9405bed060738d799e35385(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e88920f6d384aa16cd8ac044f2808beb1fe163a67fdab9ae7a1bd5ac15b45d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16602261121d6a9aafba7b71d2b8cc781b250e2adb278c7502e7e9f1a6da57af(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__167e957f1939d3a17a6a53ae4862c893b6456f4bb4fae9a5e084f848c337ae1f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobEventTriggerConfigScale]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0de69a9aa737340d23c5adb605411b74ea777ebba6935435a4872a4723c66e8(
    *,
    custom_rule_type: builtins.str,
    metadata: typing.Mapping[builtins.str, builtins.str],
    name: builtins.str,
    authentication: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobEventTriggerConfigScaleRulesAuthentication, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa94116e5b4030cdccb8b20b35ba1c2a269ae93b794c6de117030b3fe271eba(
    *,
    secret_name: builtins.str,
    trigger_parameter: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5deef196186b805caa4564502a4cb301388a9d115667006b62907f1e0036714(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47d5604182bfa876fade26fb586569d85063afcf930c13076a466ffe3d3ff97(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__566fee0253c15d0043e8eb79d3e86d1afcce1ac759d93a6126caad26f016252c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cd08519eb9687e88d5c194025b685d8e85ff8c51be7a86e4aea0ce45b4c718d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f27001ec8597f48dddaaa184c0ececdbcb4708da2aa439099612201c5aa8d21(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ec28318802a859937a9c540940125c55b3e62ddaead7b777c4a758c0561f56(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobEventTriggerConfigScaleRulesAuthentication]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b1cbd7a8cd9ccc79a8622e3794fa7f7c3d5ce3d1b4c01127ddbaec6126b5fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d464b6ea42bbbc61a11da6b7af0746156009472f7613616b697dc30d6cfb98f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be5f3b57760ace74eada3e5bded3a9dc9fc3b4167804ef147ae7a78b5aa7f57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f886877324b66e26feacd7ab4061a90ec4524e92063911f53751c2118ddc97e9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobEventTriggerConfigScaleRulesAuthentication]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__128e9f33852e49d07aae17e97a1253798c8bb73bf0c3276c93912fea5dd9dc63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcad71de8630ab4b50f53db2d55e6d361f5c4abb3b2f67b5662e075319cc1be2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85dccfd6176e7664c6bf5ada235be1945aeba91e968db0f5de6c3fe79957de88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647340710b16c4aa681e8f1de1fecfbf242c3f2a0f1c71c5f28ad4f8e6e38c06(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f23a1c21a46815612a0d2eea5a4767151ddd5edb18370e77fdc7b01cb107efb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8cbeab656bdc3c741b07b1edf4c9f2a010fc827fd419217054b111347b9925f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobEventTriggerConfigScaleRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a13a9b9a6ed0ea2d909e89ca9c75e180828f02dde684997def94606d9afb184(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b06805988684f0c50ff86842434e768ee639ef8bc9dd8cbb9ef705b99ef3f8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobEventTriggerConfigScaleRulesAuthentication, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068b750df8ac6d15949b71b09dc9a9de252a8f0d6aab15bb76f2bb47c738c9c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf3d93c957964a88bd37bd4901aa8fa0e7c0378d3dea99bcf7882a328cb19b6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b0c858867160f51f4c3cb8afe354d9235285bc66840a3f0cfb00bd9897789c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e871513b366556882828554d38e07751e4e9f2b6a343e985de601096330f28f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobEventTriggerConfigScaleRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947fdeb755ba46776844cdd8e1fa4a563d0650bb969ebe2ccf8109409aa64d29(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ae3795a350b5439c49b716ab3c3e2182bd5767db606086121bab36f22eae0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ccc9a20e6e07824a6fbea8575f71abbf7ebef42c5f837838e5d91ef09a8c677(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5632db6123601596a06a9d6e0be76bce30fe9e447f3daae74c241ee7d807c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0485ea84ce3f4dad78014cbb83b0ccdcc7fffeacea9c810225e3ace1af233a(
    value: typing.Optional[ContainerAppJobIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdffda81a73d59602c52dc29122111580ffa1833f3419e39dc3211682b9f620a(
    *,
    parallelism: typing.Optional[jsii.Number] = None,
    replica_completion_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d2f6a5feba2b71723eebd4368fb1d9a720a2986f7160e37b3dc1442a111494(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74204d7a48da02b67d33b1f5b824c6a95e3ab98b290d7d816212f171d2be32f1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d0ce222be89a8c12fc8b80cb97df2a903f1c794396a7952b6052c031ca0b8d8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1379c41a37d3d038bdcf0ca46732ec020c18ac82c72bac8505be5f6c60e36db(
    value: typing.Optional[ContainerAppJobManualTriggerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__399b5c1494f93a321703bb892b53ef82a96dd092eb61bbb45571745e96596778(
    *,
    server: builtins.str,
    identity: typing.Optional[builtins.str] = None,
    password_secret_name: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1f880c5d680af221a0e044762dbd1b7b7c6937706ba48987c7f2e9b58bf27a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572b2649d3c0ab88d91117be4a323929b84b66566b2aa2c7f62fc3ca9e961fbf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b08f2730137d9314dbc515b0dca520a54f0d131d5aaf06dd24f6c9299c6418(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09546be777f3df69f9fbe5420bef010b7a1d170b835277ed1a7e3f4372f9ed1b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00387da03b1a70918840fcb2602039648e88a41c7e77b9bfb272bc20908cd809(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e823409c61d7670bf1211ee2d0add415ca4874e24527116e341bb42c5c79888(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobRegistry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd73f54bf791a6102984c0b7eaf3bab9bdc2b028399a85a7fe6069a8738c1a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad2f52a576c026b5c65154cbed1e0db716c2da07a187b9ce97da31ec51a352f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a369e8819a8ca22b8afd8730e9bc67b20b1ccdd84298178c4ecd5a134475c573(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa02a71e9cd5138d3aa41d21cc34a6975216f05dc61169dac824ce2a70d6be26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab0bdae4a954e3db581d00c7be6923a6a2e5c4b42163687879668a59ff0e4e89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10530b8c0e31b1527210e6b65baaf4d08941bffaa8e3252e182fd8a01d2fe6a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobRegistry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06721bb3db4b911ec41c64c41a0608d10f5011b2075d56ec99a53f616e638150(
    *,
    cron_expression: builtins.str,
    parallelism: typing.Optional[jsii.Number] = None,
    replica_completion_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3a3d6cdb0e6bed5bc65d962c2e62338bbb203993a9ec41f4f124c6eebbd262(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0b41dcdee636dde627a7fd10e9ee354e096da8f9c1ef71d854274a3a9ea4822(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b52633e763f7e36ef30cddef6b92508ee4bfe2dc3111685cb62ac1ac3ed9c541(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51adf5d855171b89c22d6df6ff60aeb4081d025e65af52b292eb2d3341acc44c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832b69d4396c9d768a73caf9db1025962b0a8ebe17daf3adde8cb861c9454b91(
    value: typing.Optional[ContainerAppJobScheduleTriggerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e227a8fa661e39c40c37f8cf4a187a8bf1fcd08196b281e8ce68e7d9ca6ab3d7(
    *,
    name: builtins.str,
    identity: typing.Optional[builtins.str] = None,
    key_vault_secret_id: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144eff62adeb66621c42e28619d1a8a8fd8cfbdf6323e08f5c65373a3230429c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ff8ebf9dc626ade6822a38a03e3dac93818441606989e089772e7448b740f4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5d0715828ca1a5cf0515743a4a69b6cf4d0996ce51d9891bab396338eea9852(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e74d3fc1339bb656a7b64dcadedf0bb8106c5da48f3e0acb45c441d3d7ce71(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3e2fda4849c0c17590fa2f3d794ec783139031af5f6c961048bc193a47579a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01026a83016b7b008c2e6b72d12c631f1feeb81b19060621cfa7c3d92c914ad4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobSecret]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e538eb0d5f0a460ac0345c27906404cdd20c6df0143642c3eb9359573d2a83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f9dc6470f18e2e7ad35b1f49ed404caf66723023a06f3cf7c70221b5a526320(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da60dd2cd64f50e3fd58ba1dbf096885c611de9fb3690a23c33753834d854875(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f2fc3e1265f04dd419e26923309d776535476b950b88364b38a913f71cf67ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a78596ff651c8b06008b0d0ad8a29f43946f88b472c364c7de0e70c7bd2e9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6861794edd937caaff7ea2c3b5f3f093c99843a5ea34df0747d1dafff5cb75ac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobSecret]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e5a155995b94e5f42f123c16a49474a038637e503f597abaa73185169799cc(
    *,
    container: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainer, typing.Dict[builtins.str, typing.Any]]]],
    init_container: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateInitContainer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    volume: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateVolume, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37ef73afaa383f789916257ed2f08f9fc9481954f233657fc5228fa13a2d172(
    *,
    cpu: jsii.Number,
    image: builtins.str,
    memory: builtins.str,
    name: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerEnv, typing.Dict[builtins.str, typing.Any]]]]] = None,
    liveness_probe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerLivenessProbe, typing.Dict[builtins.str, typing.Any]]]]] = None,
    readiness_probe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerReadinessProbe, typing.Dict[builtins.str, typing.Any]]]]] = None,
    startup_probe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerStartupProbe, typing.Dict[builtins.str, typing.Any]]]]] = None,
    volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerVolumeMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d456ac7ca2ff351dab4d7e2ae62bedde123b48c1546957db861f994227df672(
    *,
    name: builtins.str,
    secret_name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e13556b7198e7f0820e166cadb492f713cc17f2a129cc01d449f185c78ab17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9aa057ecac1326749f390e04efc64c981e6568a06fa982cc23198fcb8316bc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc68ed3f67ef11e983823913fb723df90eca99a36b39a42f132b0222159d95a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2bca635987507f4b8574215105159140d1669c1f37f09591f271f558cb789e0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f1e25112b1668b317fbe63d5693a1f9d4352c4462aa6963bfab55ae1ebf69b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed24b070268effdeb23fc9edddacdd25dc4593fcaf2aaa9e1e98ccc36e15f56(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerEnv]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce44170ea981ea4169a7da9bd04c9496bc242930b2e8e0fa180f8c94fecd9530(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0edf1a61d182bda5c48a197b1f0ccb30d5d1f50b0b407a7a5356c29dba1eaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7027211701b7e9ce9afbfcc5e7d50a0b2a486c4ae68190857a32091788c42a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed0e30aa4ed9525dca4eafe0f1eba8b6452f62cc7cd9097bf9968f2da25bab2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648af50d529d1df84cf0a7628cb3f99eb1ded5bd5d52c770a53d54a1890583c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerEnv]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfefe53ab9eac66ad8aecb904a026b858d09d31b68f3baadfc75664fa9bafea6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd6efdc5353e5ef5140401a642a12b1dc0eac4c1a7a3b1bb4ba03680b3db1464(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d19b3ae793972c287b09f50f37153a6eeaef503eb11b55d9fcd7a908f5a17b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da7e56a27e4f086cd7526ce4c1c01fb191a0a2b9fc6d0d4aab4a1a91bf3fd781(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1190f30ee45715d3d901d430c0db39174796e40bc2c047ec78f02981d5238ee8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ea06e37b470d21af9fb832efcf95850739ad1797539a3b56722c140262cf90(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainer]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef3de46ec4fd17e398043191934d9b8ae1baf4e23b4c1ab8974f7644a730b95(
    *,
    port: jsii.Number,
    transport: builtins.str,
    failure_count_threshold: typing.Optional[jsii.Number] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerLivenessProbeHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    host: typing.Optional[builtins.str] = None,
    initial_delay: typing.Optional[jsii.Number] = None,
    interval_seconds: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef301633f66a2e1addc67b2010f895daaea7760b12295e4f15a4b053fe517730(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de92bae77287a6f5043fd241d2e5c6f207f188799d53cc5f3a7b0afbadc4c91d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66a55722508c4fe635451f6ffd54a7467920eb739710a9a365d676d8d91d99a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21174c9134309c1f363303db7b2f75df7d39624ec6adcf47000e6525c9b6ad9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c5d51537e4c0ee4391e58500c9b097117bb5652c8b0e45418cfe9e9c7792df(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131f6ef4676c6dcb64933aab6e6dc98720a4bc01fc730d27f0f897115dccefb1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9119180f52baa718eef0d9afad49c3bbc5cfc874840f2c9647fa663a6976ccc3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerLivenessProbeHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2971df90d2abe0cef9607d7037ce1363fc2d5b13d097097c0cc406e6c950a7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265540597bc992fb4e3c7a92a0fb600c877b36fd075c74c01b09d50fc0805f3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a98626ae4b4bdeca20f16de96157232f6452ae62e663ee216b7b7bcebce373(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce09b9131aa93fd869b12806d12c34ae9ced7ff7809c3376dc2db3f423e35602(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerLivenessProbeHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b78a673f08e3fcfe348a3161ef1d026cb45e8175c3b584714612175a043f129(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5699ba4fecea9f1a072ad64a3eedcb71b3dec15571e56de7b36e15a93115dcaa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b60a32e268c1d0b15fdbd7d72601cf0d80fcba4e3325e8f29e8dbec419c3c51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a478dcc643e075de1881618de2550cf507dfb83e961a0f76e793edaec0f4b01c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9220ec80bd3673635e34dd657d093f9576d530966adaddcd6c6b2ae5b3210a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fbd51a78a06b40cb18ae158dbdb0d9fb4d9601cba455a1776addcceac0e6878(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerLivenessProbe]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3dc43c4ce65ca06614e3d038e94771e041a688fd4a46400d02150b9d3f37d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e0e6a9ea78e317751c0ed894609dfd5439a46de308387c7526ce197cdb4a4d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerLivenessProbeHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8a4ae14ced2e87d96171b47a14b581e4eeac766ee28a804e81ad98802b5d68(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eadf80a89c10e30a7fa10ebb3c463d6bd2de9e86f60f0421fc0776cf3b12c6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f319bd47c500cbeed64436d6d5d92e20e2a35e9687e2b2a15010b7fc483467ea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9bd2324c9c7658491f6abecc8924071cdef2a28151dbc7561017c3dedea2480(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e8cd203d2dd737472e248f298c669a6be5d3cffdba7d3e0dc32e1910087205(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684afbc0d475f2985424e4e2822b8ea1d6b452ea954e7637eedc6c2a94b32e80(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89df8ef3b99eb3a9cda3f5d6f7d1689d31253b49118f4bbc67e43fd2bf69048(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04aeaa0683d3f63cf4f422909e5610389c967da01b21f27bfe9757fdc375534(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be0cecc2f0e81fb239a1e70e205419fdabecc24c008301ff607c5525387caae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerLivenessProbe]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60e2fc12766b29c4a4cd64d62360fbab71343e113395bc11ec84143ca8fd583(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7809d7cce527923a0329df8137d18da8b0b7a75abd5785996ada09c9d3d029e2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerEnv, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f47cce101d47471e68e3663d5f2541875f518d09fb59b90a4d5977b99bcdfb3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerLivenessProbe, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f728d634a6a3afd4752308d7ffb3ec7be6ede530f9fb5f15100859e327f76d02(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerReadinessProbe, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c706c37d2401f17663a1f39bc36e469b73a1031df37172f1b4edc6a5ae0e25(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerStartupProbe, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50dd9e26da5b5fcc69b48579ff25a96b03b611218952003ba92d4191ee7e5f6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerVolumeMounts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36106b1a7093268db64f3d6de4d2e0b56608c79cec7010d3d24f8d69257a4416(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0995132a33caca5310a971837fe88eb4e22a74204631bf5c742679251993939(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835c672185e658f210994772282eb2de6f6ca6c9d3ea3e0e8a81ada276409574(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c06780b3419034886dd53d66f24d12935bf34837a092c898f1d458e2ad8ae498(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954ac0c8deeb7e980b82daf0ff4c3b2aab24069ff8fe69a6ac2b25133733bf92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e1d65fe6cb95488d840864854db0845294faa32216302932002c06d9a312f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a7fdf46f6fbf72bd4b51b8e060a1c4b0fe6e9dde790ff66f5caa2be2c93afa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainer]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264a9b65f1b0b6cb9f1aae254e796d281afb62fd6c0508a6ce86fd6369a19059(
    *,
    port: jsii.Number,
    transport: builtins.str,
    failure_count_threshold: typing.Optional[jsii.Number] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerReadinessProbeHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    host: typing.Optional[builtins.str] = None,
    initial_delay: typing.Optional[jsii.Number] = None,
    interval_seconds: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    success_count_threshold: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a455162272890bcf289098f120727c39bef548fd5f9f0d41485fbcbbb60529de(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ee13fdb769a744014576a097761ef2ecb7aa875d4c70e375580cb74929cb2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d5f2ae9bc1eb27a23e2875c34557878b3348401ea541007817a93a039cba1a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d8111c7df289bd5c52f6ac60281f2210bf1e371f9bc0698e33980746d173bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3526cfea8e56d6d63081b0d8036e3585f43e1642f65847da0eb33f38763bce3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5710c97895a4e7e0a5559f51fbdea3df53bb2e32e94e0d5c1b3f7ce6ad216f7f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914a1f5449740ca5e50b858359e46655ca5d350e8383fb06c5e71c40fbca1d4d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerReadinessProbeHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7cad65ff8abc0c72f5b8cd196970c2b635b7e1c941394f360832a97e256402(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00193ca871919b3fb5842e5bec24885e9f80eaac88d6affc5bc3728612c9454e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00159b0457100cc54ec84ff2edc86849cfa8cf076301531481c537bfa1ca716(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d98d8bd139b54bd55f4f2eea0c1c5def72153580b63b26d065978ab9ff681d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerReadinessProbeHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0745733ac81c72de96731c5717975d39cb8d2f61d64d79f2d8bda0ff90a6955(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0e40b0480f9507e50a77aa2be364a79f5271d274a7d30e3a78069935e3b34a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67e68a0a090956511c4fc4c76f1622e59aff11b7fff09d18f9b2e64b0e59e101(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557c57c17539227a18598ad4b7d4620e74dbead6cbf81883c7a159aead96d46d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed29a2ba14768e5e28d4cadcf3fe83f65c863030cc35a4802ac876e0bdf1d74c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da69b2463ca253bb82fa4f082666bb0b7ec279167562681f67eab064e55cb7a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerReadinessProbe]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f0b2d600216a084adce29bfef9bf56a2e97485a0d850eaa4222974254c6ce17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c5dd2a77ee35ac124b53f6bfe58fd0754e78330d48247da807fcb760ebb3d2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerReadinessProbeHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63e432acff5f748cdb4b96ff87847385ecf53471c1673d4d6fe32b566a41717(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5492216632294d5a79a021694ae2aca748700d248d82bcbc42c75257cbc49e99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92606450fb5f3347ae355af444b793732b71fb910833f417120224655e84d32f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba61bd342e785673d4f4dce364034cd5485abe62008f342b1ea4c6badf5b032b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedbc8bf4496da9a0694d1d91cfc06e711292005f2567ba4b405d3a70b5c9241(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72838ae6f1fba9e20b7ac3851dffdee448667e9c30614c0cc1b08431ad611895(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92e548c740e4e42149af3dbc8fcd7b87548d4809e166294055610ad124af38e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ac364bc31abea46ab632106811a5ee9bec273f22fe62e82a7b1c1ab0b2d18e5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5053532de363378a089e4b84f5f89a87b58873f2c61e818483d985f4d4de681d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9083e202f2241b5e71e194308b4e1248387fb6abb172792f2a684c36ecd4509f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerReadinessProbe]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7442fbe3a061998abe8d308e6a1350364fb10e7e70084ab081e93d9c4e9a5f9d(
    *,
    port: jsii.Number,
    transport: builtins.str,
    failure_count_threshold: typing.Optional[jsii.Number] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerStartupProbeHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    host: typing.Optional[builtins.str] = None,
    initial_delay: typing.Optional[jsii.Number] = None,
    interval_seconds: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cfa8a3f018cf5d5857d290451541f92e44a2b2fc65fec1e84e45af244e1fdea(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6768d004af77c4452b18ef99ca6b8ccc8b99713f9bc43c3f13bc6830196587(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077aa69e055640a88023dcb06a37a3662550a462da5500a787ee6681b90dc752(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae30b52c2c8779f8203fb43bca621bf43a212b7e17d53fa311a95a3b9222040(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024547cf81ba43ab31ed7c7f44c75ebd2ebc34c0c2a4b8b190e9e00dbaee62fc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__845e39d724badc3ec69c42688e2a3851fc1d4829a51f4bddb95f5b9786dd4f16(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2bbe0865e2872dce7395f43934f8a7fe119baffb29878a126eb21c36f7c3c8c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerStartupProbeHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a98105fe84e05866b7438d33a4f423a7d907caa11c63d8c03da370416a36002(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ecf52170a578810d289dc0ceb4cee196589bd5faae12856d272d83c5b8084b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfb9217091011a8ea88a1391281828841dd98a5f55a69521f0847156566be69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373fb4d7bb59270eb307715cf847b5d4ff835d2080fdef9c51708f1dae356819(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerStartupProbeHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba9323c84118513c2cc5bc767b250e3c8d6289739f16abeebd2eec060a8fe57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d193bd0cf4f5490158a176c14dd9f2e21e530df76ab447429fd94ef579030fb5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74463c48e5d66fcca9977b1477fa303ea56c5336f373306b216f1bb6ff7f5f1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d5defd3b5f42fedc49ae272a11d7984a2701c52bb47c222aaf037eb4288477(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69547dcfbe016c26b284ea90c39bb2c4ccbf8c93c9223c6b94326ea2710b96a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__994f80b6237cfdac3111a9e10d12e9514d465a4891e8dcb23d8d5af943253610(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerStartupProbe]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6ae123e4d8bff93b4d47847e55547afda7b77a618bc7ddcea96ce2606a56e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86930a3cba691a41f16043cb7c488c1215f620c0e64f2df01702026ee942552(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainerStartupProbeHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6998d249463a7849aa7927ed3e2e3959a5bac1bf99c0a6ebbe1d600c98b2f141(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7c96f4a9f2dd485f945306dd0d3c66fe1e1d7a972735728fd262521ac1f88cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab899ff472bea6274d6570f0be05b3af0883b9ba0a65339d9f9f821933caf98c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502b6c55c83a3c113bf1ff4027588e3cc436846c89de8d3ecbb3f3861805e844(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1e46b49d85f67b834965339d85e744acef66c47a28be41e41caa6c80b773a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a200faa19f66b581df3c08e4469a2b74895c800d5e12e89cd559d2db2dce2a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954ebfe758d5aa28755f4a56d568ba0443a34a0be98fc7a0a91215dcd8ee6e15(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188d9e2e41a909202cb565546f7cb456fbbeb51ca1fba58f16591f97a431ebc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba2063877e22fd5b0b82a07ebcb2cb666d90c5685ce0454a0bcc1f908f831d1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerStartupProbe]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f026b81d18f038d1031d6bdb4dc34f323e036aee2a37cc8307c3818987e198e(
    *,
    name: builtins.str,
    path: builtins.str,
    sub_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d12a903356bb0af06f12aeebdb0ae326eab727b4635216e29d4112e927aaf9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5458f3e5e9449adcb264cce09e936adb328f9866807fc0ffd3c2ba7604ece285(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d81ad9b085769a6397048f86ec8ee631a65d51b811937540537a772f8e5925(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed209e7eab1130f1d192abeed0bd7f0f521dbee5c07a1c24ac17fa24def6393(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49f45415ca0c6b7f931866e5ccc3a40d9b847c113cb87212c307dd230b4d02ee(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee6e4a8e0b4826b446d861d38eb8d062a632107f160eb15ffbfdb3ccc65cc67(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateContainerVolumeMounts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73fa996276efd5cce8302138bc9c208ffd6a51c9d32571bb72f3d10a61a021d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b2e1dd696f1ada0dca55c0b26101ce768654feb7979e34d6cdbf6a0c07ce76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38bd58efe1a08cdc4758a60f06b9fa7d3ee6a4f4422f2250c1d5c9fc62a258f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7113dfc841112c7dd8db3f0b9e972ec1387ab582332ed36e64a835be35e8aec9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab1d52b184eb9547bfc70f24085b33456c74f49f10496504dd1732e95cabcc76(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateContainerVolumeMounts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5deac8fd878404d54f964e6c3580728b94fd6055492477d2d690de82d620b57d(
    *,
    image: builtins.str,
    name: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    cpu: typing.Optional[jsii.Number] = None,
    env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateInitContainerEnv, typing.Dict[builtins.str, typing.Any]]]]] = None,
    memory: typing.Optional[builtins.str] = None,
    volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateInitContainerVolumeMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103550d068e9d061ad0cd4c05371109edd386bd9ce685fc5d9bd50118e6baa60(
    *,
    name: builtins.str,
    secret_name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12a0275f3ffdb2c4e9f53ec5d5ed43428dae1879d3d3485d834bec666cc6234(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c30138055584ca2d3a90d6807ed390318a9a2bd59f05fc76765c8ebc0667a143(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49959f0aba80191baaae7a40624815c484229129cbbb0a4dd55bb68ad4d593ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ac71ec8ebd37e08987a65b1e118c7089c513970c4a227543fe0d4fcf8ed42a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d169e286c08b81fbf81a4af7d5f13373226942f562da8159269d5c2805c26a1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145a706a5d8333ade09196fe04b4a636f412920fe762675dcb13ea96dd098f88(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateInitContainerEnv]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86d9c308687b32f991f65371578809d3d9a05ccc3a0b3612916dcda3985869f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b92f45516bd52d54acbcea5cda7f24cd0410279955f897310fda891756776107(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af88efcea5cd2571233d9f0d7253778810fe448c226d511483a3b75f0277360(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d0cbb458b92601b3fedcd66fd5a89a7d2697094739aa522052f253398df9de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__055ebe3d7d3d0281302ecdf3d02febe28c1fd2d1016e493d50416ef4b9a2336e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateInitContainerEnv]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c863d48557b4941d07c7820334b9729c57d7151b3c8579725a34909eb9696a4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb29aef03905a707e672dd88e0dc5159fb25cae5c4aaa14ad174f386affdc27(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90563857b8a352b49ca5bb469393cd0d917a1bc966feed916857c623d04fa00a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1829bf4e61d405792e6fcd2d672b7b7e77c1326f0d440410e42b1ba843f476(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59fc6477e63a7b4eaefeb8765b309dc4115df8f2a759282e0945821de082622a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906bdd068b92f884f69fee29936a5ec4a45428e5414a884673fe5996fb7d43fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateInitContainer]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076c810f0255ef66f12026dbc923c99c0c742446540675fdf032ddd9a515bb5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735317d266a39e58909661f83ab5353e85ccabb095653bd12e986913757ac7c6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateInitContainerEnv, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa18f158deeb7e9821b5fb48aed6093f1c7515c4601e26db001fd02a889b922(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateInitContainerVolumeMounts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c13d2b1d2fd9d0401f1846238452766da60624102412122329505e840ba676(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e130f3f51989873b7d9553c4b0b6855bea026e02cf749b0acbcb31fb6c56096f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5986ede0d5e1f3160fa348e55b9f3048c5d10a82109d981fca0713cab97088b1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae7de880c40f2976cd3521d6c4ed9d7f40c70b64026243a86dd02979e8f23750(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24bb3f58af9482c5a5313e93f2bd9579896158db65e3cba781c7c9bb92df9758(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9581dcf34246648ec6d608a5f95e0329a7f2a913b833a1aea473b7f088c9e57e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1955bf1816c1d5850000d33392f11eb9f504abd38affd2de76de1e8b96ed0034(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateInitContainer]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a848fda985daa332434f949a0ab9167c2cb678ba93eea487ac6f849e37e8c6(
    *,
    name: builtins.str,
    path: builtins.str,
    sub_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__790332075bc529e40d12cc41d5718d7e3d5d3364f67f2657153a5452a393e381(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6d4e8b7c7b653e97586300ebb05014c8df20def92f3fcf79577263e307b6bb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52458865d22f121bcefcb5bf7dcee894ad572dcc32eead3f3d50f83948857c3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5792a397df84ed7a51da15efec45da203e31927515a89c2d92d8b889e8072f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54b3dde98cf48a0c5eac7c9908f2d7d3e6947669d878e3e3d1745588845100e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b596112a36e688873f62389c7bfeb0e4fbba755f5d5a8fb9e06d00f00be859(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateInitContainerVolumeMounts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1efea6b25d689579c6447accd64403b67b40f6f3853bfbc74fd760be2a60eb82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__419b5b904c8fcabff1e28746a06e2e238fd6692e7e5a6b651a22c04d4dfeb54e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42fffe2105a4da3d5e3a79359293484e19271dac22abead00969eca02f9b327c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcad510a010d86bd7a1dc08b29b484be58d82396a67c9340836007e11b76051c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624daf760a4c30a0397dd8d77d9c1bf05d44b1f1aea416287c512f900592ee65(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateInitContainerVolumeMounts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1334cc449964662fa04289928738e52cc5a4deeafd08890723fe49dddf72535a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e73fc2315ae15242bed23c3ca0f723e7551750444844630a087ecd6db06cf5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateContainer, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3312d31f86af86503a273e41c113ab39709557c8c48c25f7737b96616e524b6d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateInitContainer, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b0fab980c16738bc4393088d3e9ced11459ecf5465efb61b9cb1801ce47bf5c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppJobTemplateVolume, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f277ce390c2adeda019796f6b49bd52cb022cdeb3875ff944c23e119be81ee(
    value: typing.Optional[ContainerAppJobTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d929009b0101d464a87fa7a9f35847c1f07f7d88cae30f58b1d1d4812a7fde25(
    *,
    name: builtins.str,
    mount_options: typing.Optional[builtins.str] = None,
    storage_name: typing.Optional[builtins.str] = None,
    storage_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f485d294f0c92b73d5ec513eba2d879a7aac8cf0adafffe87fe678be5a8a172(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10b473ca7baa41120b836ec02f467b84f855b8bc39cd75d212d579cadb9cfa5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f6f271983d26da9fc0704f276b61d4e9aefec5f6c4a3159b83011c78b0e206(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806d0d15fb7d5d1924e621b2648148a14e916779dcb1b3612b6fc0c9f3417d22(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2860a2995dc8c3182c272a719a52bf7f835471901a62be9c3d37f2ede34425b3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea9ac526cfd1a773a745a46468302718ae59f9a133bb80526eb22e68ec4754b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppJobTemplateVolume]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6bb1a17aee58946aecb21c0574593217d1df662728bb0441babb555341f37ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c02a51f4e75566d5ae4eb4ccba7ffef48088eb61233408e990dcb6a9ebe15ff2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda5ab4a0b564d996a9144d773bea7f5601caefcb2e505ef1b8e7b0b6cfc7197(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc99586ba86250f4fde9d5624655f654cbeac46ebdc2a3a5b2cf74ba0178886(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9186a8bf76b712c1e6431bf811191531b118920c673c3e5537a5678bb0c99cd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49746f6da3221c2183b66158e6f7402eecd2fc05168e429d9070eae268875dbc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTemplateVolume]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8452f201b5703548483d9f6436e72c9aab71614fb5f130c1f0d9fe5bcf6a133b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d866fa3f8627d59175983a08060a26c36b49fba9c9cc21f70fed03551eec6632(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194d0646bda92ea76b97eee91d8dd1d9bf3d53cfcd48637ba8d979992bf25f24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0659ba569a0398cfb0ba3fdb744ec425f4a3bbe8b5452282b1617e6bfdfc8d87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e015ac8cd98dced3490e6d87705ae4601b24350d972f92da6f793eec21c4990(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed68fc0f50b06e331c5e06407c9faa79c1c6a74be21c27101f088b129e1bfed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9b80caef22af454a89d4f92f8bec91b3bab7d97a37c50b7b518a491bfcfa99(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppJobTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

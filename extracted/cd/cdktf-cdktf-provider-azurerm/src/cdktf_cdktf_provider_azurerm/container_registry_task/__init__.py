r'''
# `azurerm_container_registry_task`

Refer to the Terraform Registry for docs: [`azurerm_container_registry_task`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task).
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


class ContainerRegistryTask(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTask",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task azurerm_container_registry_task}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        container_registry_id: builtins.str,
        name: builtins.str,
        agent_pool_name: typing.Optional[builtins.str] = None,
        agent_setting: typing.Optional[typing.Union["ContainerRegistryTaskAgentSetting", typing.Dict[builtins.str, typing.Any]]] = None,
        base_image_trigger: typing.Optional[typing.Union["ContainerRegistryTaskBaseImageTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
        docker_step: typing.Optional[typing.Union["ContainerRegistryTaskDockerStep", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encoded_step: typing.Optional[typing.Union["ContainerRegistryTaskEncodedStep", typing.Dict[builtins.str, typing.Any]]] = None,
        file_step: typing.Optional[typing.Union["ContainerRegistryTaskFileStep", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["ContainerRegistryTaskIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        is_system_task: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_template: typing.Optional[builtins.str] = None,
        platform: typing.Optional[typing.Union["ContainerRegistryTaskPlatform", typing.Dict[builtins.str, typing.Any]]] = None,
        registry_credential: typing.Optional[typing.Union["ContainerRegistryTaskRegistryCredential", typing.Dict[builtins.str, typing.Any]]] = None,
        source_trigger: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerRegistryTaskSourceTrigger", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ContainerRegistryTaskTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timer_trigger: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerRegistryTaskTimerTrigger", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task azurerm_container_registry_task} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param container_registry_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#container_registry_id ContainerRegistryTask#container_registry_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#name ContainerRegistryTask#name}.
        :param agent_pool_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#agent_pool_name ContainerRegistryTask#agent_pool_name}.
        :param agent_setting: agent_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#agent_setting ContainerRegistryTask#agent_setting}
        :param base_image_trigger: base_image_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#base_image_trigger ContainerRegistryTask#base_image_trigger}
        :param docker_step: docker_step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#docker_step ContainerRegistryTask#docker_step}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#enabled ContainerRegistryTask#enabled}.
        :param encoded_step: encoded_step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#encoded_step ContainerRegistryTask#encoded_step}
        :param file_step: file_step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#file_step ContainerRegistryTask#file_step}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#id ContainerRegistryTask#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#identity ContainerRegistryTask#identity}
        :param is_system_task: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#is_system_task ContainerRegistryTask#is_system_task}.
        :param log_template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#log_template ContainerRegistryTask#log_template}.
        :param platform: platform block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#platform ContainerRegistryTask#platform}
        :param registry_credential: registry_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#registry_credential ContainerRegistryTask#registry_credential}
        :param source_trigger: source_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#source_trigger ContainerRegistryTask#source_trigger}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#tags ContainerRegistryTask#tags}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#timeout_in_seconds ContainerRegistryTask#timeout_in_seconds}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#timeouts ContainerRegistryTask#timeouts}
        :param timer_trigger: timer_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#timer_trigger ContainerRegistryTask#timer_trigger}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84d76540b87bc714f3b57e5324d46904e3119e827985f1e092f095a1c71658db)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ContainerRegistryTaskConfig(
            container_registry_id=container_registry_id,
            name=name,
            agent_pool_name=agent_pool_name,
            agent_setting=agent_setting,
            base_image_trigger=base_image_trigger,
            docker_step=docker_step,
            enabled=enabled,
            encoded_step=encoded_step,
            file_step=file_step,
            id=id,
            identity=identity,
            is_system_task=is_system_task,
            log_template=log_template,
            platform=platform,
            registry_credential=registry_credential,
            source_trigger=source_trigger,
            tags=tags,
            timeout_in_seconds=timeout_in_seconds,
            timeouts=timeouts,
            timer_trigger=timer_trigger,
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
        '''Generates CDKTF code for importing a ContainerRegistryTask resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ContainerRegistryTask to import.
        :param import_from_id: The id of the existing ContainerRegistryTask that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ContainerRegistryTask to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94e7fbd0331413dfa4163929492ecf41de3a150b3b22e6625bdb48c77b1bc189)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAgentSetting")
    def put_agent_setting(self, *, cpu: jsii.Number) -> None:
        '''
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#cpu ContainerRegistryTask#cpu}.
        '''
        value = ContainerRegistryTaskAgentSetting(cpu=cpu)

        return typing.cast(None, jsii.invoke(self, "putAgentSetting", [value]))

    @jsii.member(jsii_name="putBaseImageTrigger")
    def put_base_image_trigger(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        update_trigger_endpoint: typing.Optional[builtins.str] = None,
        update_trigger_payload_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#name ContainerRegistryTask#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#type ContainerRegistryTask#type}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#enabled ContainerRegistryTask#enabled}.
        :param update_trigger_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#update_trigger_endpoint ContainerRegistryTask#update_trigger_endpoint}.
        :param update_trigger_payload_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#update_trigger_payload_type ContainerRegistryTask#update_trigger_payload_type}.
        '''
        value = ContainerRegistryTaskBaseImageTrigger(
            name=name,
            type=type,
            enabled=enabled,
            update_trigger_endpoint=update_trigger_endpoint,
            update_trigger_payload_type=update_trigger_payload_type,
        )

        return typing.cast(None, jsii.invoke(self, "putBaseImageTrigger", [value]))

    @jsii.member(jsii_name="putDockerStep")
    def put_docker_step(
        self,
        *,
        context_access_token: builtins.str,
        context_path: builtins.str,
        dockerfile_path: builtins.str,
        arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        image_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        push_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param context_access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_access_token ContainerRegistryTask#context_access_token}.
        :param context_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_path ContainerRegistryTask#context_path}.
        :param dockerfile_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#dockerfile_path ContainerRegistryTask#dockerfile_path}.
        :param arguments: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#arguments ContainerRegistryTask#arguments}.
        :param cache_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#cache_enabled ContainerRegistryTask#cache_enabled}.
        :param image_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#image_names ContainerRegistryTask#image_names}.
        :param push_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#push_enabled ContainerRegistryTask#push_enabled}.
        :param secret_arguments: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#secret_arguments ContainerRegistryTask#secret_arguments}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#target ContainerRegistryTask#target}.
        '''
        value = ContainerRegistryTaskDockerStep(
            context_access_token=context_access_token,
            context_path=context_path,
            dockerfile_path=dockerfile_path,
            arguments=arguments,
            cache_enabled=cache_enabled,
            image_names=image_names,
            push_enabled=push_enabled,
            secret_arguments=secret_arguments,
            target=target,
        )

        return typing.cast(None, jsii.invoke(self, "putDockerStep", [value]))

    @jsii.member(jsii_name="putEncodedStep")
    def put_encoded_step(
        self,
        *,
        task_content: builtins.str,
        context_access_token: typing.Optional[builtins.str] = None,
        context_path: typing.Optional[builtins.str] = None,
        secret_values: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        value_content: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param task_content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#task_content ContainerRegistryTask#task_content}.
        :param context_access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_access_token ContainerRegistryTask#context_access_token}.
        :param context_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_path ContainerRegistryTask#context_path}.
        :param secret_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#secret_values ContainerRegistryTask#secret_values}.
        :param value_content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#value_content ContainerRegistryTask#value_content}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#values ContainerRegistryTask#values}.
        '''
        value = ContainerRegistryTaskEncodedStep(
            task_content=task_content,
            context_access_token=context_access_token,
            context_path=context_path,
            secret_values=secret_values,
            value_content=value_content,
            values=values,
        )

        return typing.cast(None, jsii.invoke(self, "putEncodedStep", [value]))

    @jsii.member(jsii_name="putFileStep")
    def put_file_step(
        self,
        *,
        task_file_path: builtins.str,
        context_access_token: typing.Optional[builtins.str] = None,
        context_path: typing.Optional[builtins.str] = None,
        secret_values: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        value_file_path: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param task_file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#task_file_path ContainerRegistryTask#task_file_path}.
        :param context_access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_access_token ContainerRegistryTask#context_access_token}.
        :param context_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_path ContainerRegistryTask#context_path}.
        :param secret_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#secret_values ContainerRegistryTask#secret_values}.
        :param value_file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#value_file_path ContainerRegistryTask#value_file_path}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#values ContainerRegistryTask#values}.
        '''
        value = ContainerRegistryTaskFileStep(
            task_file_path=task_file_path,
            context_access_token=context_access_token,
            context_path=context_path,
            secret_values=secret_values,
            value_file_path=value_file_path,
            values=values,
        )

        return typing.cast(None, jsii.invoke(self, "putFileStep", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#type ContainerRegistryTask#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#identity_ids ContainerRegistryTask#identity_ids}.
        '''
        value = ContainerRegistryTaskIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putPlatform")
    def put_platform(
        self,
        *,
        os: builtins.str,
        architecture: typing.Optional[builtins.str] = None,
        variant: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#os ContainerRegistryTask#os}.
        :param architecture: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#architecture ContainerRegistryTask#architecture}.
        :param variant: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#variant ContainerRegistryTask#variant}.
        '''
        value = ContainerRegistryTaskPlatform(
            os=os, architecture=architecture, variant=variant
        )

        return typing.cast(None, jsii.invoke(self, "putPlatform", [value]))

    @jsii.member(jsii_name="putRegistryCredential")
    def put_registry_credential(
        self,
        *,
        custom: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerRegistryTaskRegistryCredentialCustom", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source: typing.Optional[typing.Union["ContainerRegistryTaskRegistryCredentialSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom: custom block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#custom ContainerRegistryTask#custom}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#source ContainerRegistryTask#source}
        '''
        value = ContainerRegistryTaskRegistryCredential(custom=custom, source=source)

        return typing.cast(None, jsii.invoke(self, "putRegistryCredential", [value]))

    @jsii.member(jsii_name="putSourceTrigger")
    def put_source_trigger(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerRegistryTaskSourceTrigger", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea8b459b4a5764bce27d98cacdb0704299abd483f78d2858410c82fe37e61e47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSourceTrigger", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#create ContainerRegistryTask#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#delete ContainerRegistryTask#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#read ContainerRegistryTask#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#update ContainerRegistryTask#update}.
        '''
        value = ContainerRegistryTaskTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTimerTrigger")
    def put_timer_trigger(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerRegistryTaskTimerTrigger", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc0b91e4178d9c89c316227302753803d7227d4185829c6eb2b32bf33a521d93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTimerTrigger", [value]))

    @jsii.member(jsii_name="resetAgentPoolName")
    def reset_agent_pool_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgentPoolName", []))

    @jsii.member(jsii_name="resetAgentSetting")
    def reset_agent_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgentSetting", []))

    @jsii.member(jsii_name="resetBaseImageTrigger")
    def reset_base_image_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseImageTrigger", []))

    @jsii.member(jsii_name="resetDockerStep")
    def reset_docker_step(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerStep", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEncodedStep")
    def reset_encoded_step(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncodedStep", []))

    @jsii.member(jsii_name="resetFileStep")
    def reset_file_step(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileStep", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetIsSystemTask")
    def reset_is_system_task(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSystemTask", []))

    @jsii.member(jsii_name="resetLogTemplate")
    def reset_log_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogTemplate", []))

    @jsii.member(jsii_name="resetPlatform")
    def reset_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatform", []))

    @jsii.member(jsii_name="resetRegistryCredential")
    def reset_registry_credential(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistryCredential", []))

    @jsii.member(jsii_name="resetSourceTrigger")
    def reset_source_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceTrigger", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeoutInSeconds")
    def reset_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTimerTrigger")
    def reset_timer_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimerTrigger", []))

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
    @jsii.member(jsii_name="agentSetting")
    def agent_setting(self) -> "ContainerRegistryTaskAgentSettingOutputReference":
        return typing.cast("ContainerRegistryTaskAgentSettingOutputReference", jsii.get(self, "agentSetting"))

    @builtins.property
    @jsii.member(jsii_name="baseImageTrigger")
    def base_image_trigger(
        self,
    ) -> "ContainerRegistryTaskBaseImageTriggerOutputReference":
        return typing.cast("ContainerRegistryTaskBaseImageTriggerOutputReference", jsii.get(self, "baseImageTrigger"))

    @builtins.property
    @jsii.member(jsii_name="dockerStep")
    def docker_step(self) -> "ContainerRegistryTaskDockerStepOutputReference":
        return typing.cast("ContainerRegistryTaskDockerStepOutputReference", jsii.get(self, "dockerStep"))

    @builtins.property
    @jsii.member(jsii_name="encodedStep")
    def encoded_step(self) -> "ContainerRegistryTaskEncodedStepOutputReference":
        return typing.cast("ContainerRegistryTaskEncodedStepOutputReference", jsii.get(self, "encodedStep"))

    @builtins.property
    @jsii.member(jsii_name="fileStep")
    def file_step(self) -> "ContainerRegistryTaskFileStepOutputReference":
        return typing.cast("ContainerRegistryTaskFileStepOutputReference", jsii.get(self, "fileStep"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "ContainerRegistryTaskIdentityOutputReference":
        return typing.cast("ContainerRegistryTaskIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> "ContainerRegistryTaskPlatformOutputReference":
        return typing.cast("ContainerRegistryTaskPlatformOutputReference", jsii.get(self, "platform"))

    @builtins.property
    @jsii.member(jsii_name="registryCredential")
    def registry_credential(
        self,
    ) -> "ContainerRegistryTaskRegistryCredentialOutputReference":
        return typing.cast("ContainerRegistryTaskRegistryCredentialOutputReference", jsii.get(self, "registryCredential"))

    @builtins.property
    @jsii.member(jsii_name="sourceTrigger")
    def source_trigger(self) -> "ContainerRegistryTaskSourceTriggerList":
        return typing.cast("ContainerRegistryTaskSourceTriggerList", jsii.get(self, "sourceTrigger"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ContainerRegistryTaskTimeoutsOutputReference":
        return typing.cast("ContainerRegistryTaskTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="timerTrigger")
    def timer_trigger(self) -> "ContainerRegistryTaskTimerTriggerList":
        return typing.cast("ContainerRegistryTaskTimerTriggerList", jsii.get(self, "timerTrigger"))

    @builtins.property
    @jsii.member(jsii_name="agentPoolNameInput")
    def agent_pool_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentPoolNameInput"))

    @builtins.property
    @jsii.member(jsii_name="agentSettingInput")
    def agent_setting_input(
        self,
    ) -> typing.Optional["ContainerRegistryTaskAgentSetting"]:
        return typing.cast(typing.Optional["ContainerRegistryTaskAgentSetting"], jsii.get(self, "agentSettingInput"))

    @builtins.property
    @jsii.member(jsii_name="baseImageTriggerInput")
    def base_image_trigger_input(
        self,
    ) -> typing.Optional["ContainerRegistryTaskBaseImageTrigger"]:
        return typing.cast(typing.Optional["ContainerRegistryTaskBaseImageTrigger"], jsii.get(self, "baseImageTriggerInput"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryIdInput")
    def container_registry_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerRegistryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerStepInput")
    def docker_step_input(self) -> typing.Optional["ContainerRegistryTaskDockerStep"]:
        return typing.cast(typing.Optional["ContainerRegistryTaskDockerStep"], jsii.get(self, "dockerStepInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="encodedStepInput")
    def encoded_step_input(self) -> typing.Optional["ContainerRegistryTaskEncodedStep"]:
        return typing.cast(typing.Optional["ContainerRegistryTaskEncodedStep"], jsii.get(self, "encodedStepInput"))

    @builtins.property
    @jsii.member(jsii_name="fileStepInput")
    def file_step_input(self) -> typing.Optional["ContainerRegistryTaskFileStep"]:
        return typing.cast(typing.Optional["ContainerRegistryTaskFileStep"], jsii.get(self, "fileStepInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["ContainerRegistryTaskIdentity"]:
        return typing.cast(typing.Optional["ContainerRegistryTaskIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isSystemTaskInput")
    def is_system_task_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isSystemTaskInput"))

    @builtins.property
    @jsii.member(jsii_name="logTemplateInput")
    def log_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="platformInput")
    def platform_input(self) -> typing.Optional["ContainerRegistryTaskPlatform"]:
        return typing.cast(typing.Optional["ContainerRegistryTaskPlatform"], jsii.get(self, "platformInput"))

    @builtins.property
    @jsii.member(jsii_name="registryCredentialInput")
    def registry_credential_input(
        self,
    ) -> typing.Optional["ContainerRegistryTaskRegistryCredential"]:
        return typing.cast(typing.Optional["ContainerRegistryTaskRegistryCredential"], jsii.get(self, "registryCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceTriggerInput")
    def source_trigger_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerRegistryTaskSourceTrigger"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerRegistryTaskSourceTrigger"]]], jsii.get(self, "sourceTriggerInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInSecondsInput")
    def timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerRegistryTaskTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerRegistryTaskTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timerTriggerInput")
    def timer_trigger_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerRegistryTaskTimerTrigger"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerRegistryTaskTimerTrigger"]]], jsii.get(self, "timerTriggerInput"))

    @builtins.property
    @jsii.member(jsii_name="agentPoolName")
    def agent_pool_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentPoolName"))

    @agent_pool_name.setter
    def agent_pool_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e7796325ecea6d876e46236cb820724cc246555ba017ca07a8fe3e3c76e8ca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentPoolName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerRegistryId")
    def container_registry_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerRegistryId"))

    @container_registry_id.setter
    def container_registry_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8325729a2176a6ecbcb611a1122aa3b57339d7768af20cdb9a25bb45fecddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerRegistryId", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__054614a43ad0985d4f9b712a0dbe64c42659c3129f650d3b6746dce52c73cf72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__855d66dbcd027b4920d33c6c386a2e21ae1d5175af43ca419ba5d1a79fd2d8fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSystemTask")
    def is_system_task(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isSystemTask"))

    @is_system_task.setter
    def is_system_task(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83dab352b2e7023d95bc6e2bf52b5d3be71332d5a4b325547286e3360e0ddbb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSystemTask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logTemplate")
    def log_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logTemplate"))

    @log_template.setter
    def log_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92adfefce0fab929a09cb15ed5b93502699b84f8c314d27e3f751d33712c47a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9107a9cf2c535455eb30dc50562bb8e154902eae4c13be7f89e3377159a0cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__346253141edd3929bebbade889b1c432407d21d71b1bb86b253d1d2a500b5bdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutInSeconds")
    def timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutInSeconds"))

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__203cfb5534e11ca1ae4b0ca2c58b014e21674975565c6225ecac98ddb3ace4e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutInSeconds", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskAgentSetting",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu"},
)
class ContainerRegistryTaskAgentSetting:
    def __init__(self, *, cpu: jsii.Number) -> None:
        '''
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#cpu ContainerRegistryTask#cpu}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__343ece96c41e09b502d179fc6cb9a6abb17414a4dad50b3cfad01049c32fa9ff)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cpu": cpu,
        }

    @builtins.property
    def cpu(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#cpu ContainerRegistryTask#cpu}.'''
        result = self._values.get("cpu")
        assert result is not None, "Required property 'cpu' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerRegistryTaskAgentSetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerRegistryTaskAgentSettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskAgentSettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbe6bb8979afd22abc815d39cae2f1b5872accecddf1d22528552936a7b71a14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c2f5db20de972eed4400b8143b5c82e345e568c91679ff14797e216fd502eba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerRegistryTaskAgentSetting]:
        return typing.cast(typing.Optional[ContainerRegistryTaskAgentSetting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerRegistryTaskAgentSetting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c700e84b87eb0daab8fc67b8583707e66cc29bd67d0a00fc23a8fb595b62a851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskBaseImageTrigger",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "type": "type",
        "enabled": "enabled",
        "update_trigger_endpoint": "updateTriggerEndpoint",
        "update_trigger_payload_type": "updateTriggerPayloadType",
    },
)
class ContainerRegistryTaskBaseImageTrigger:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        update_trigger_endpoint: typing.Optional[builtins.str] = None,
        update_trigger_payload_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#name ContainerRegistryTask#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#type ContainerRegistryTask#type}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#enabled ContainerRegistryTask#enabled}.
        :param update_trigger_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#update_trigger_endpoint ContainerRegistryTask#update_trigger_endpoint}.
        :param update_trigger_payload_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#update_trigger_payload_type ContainerRegistryTask#update_trigger_payload_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__941b5ab429c66cc7170d132ef15b827a0df8361d85527646bd5a7349f172fa77)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument update_trigger_endpoint", value=update_trigger_endpoint, expected_type=type_hints["update_trigger_endpoint"])
            check_type(argname="argument update_trigger_payload_type", value=update_trigger_payload_type, expected_type=type_hints["update_trigger_payload_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if update_trigger_endpoint is not None:
            self._values["update_trigger_endpoint"] = update_trigger_endpoint
        if update_trigger_payload_type is not None:
            self._values["update_trigger_payload_type"] = update_trigger_payload_type

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#name ContainerRegistryTask#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#type ContainerRegistryTask#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#enabled ContainerRegistryTask#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def update_trigger_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#update_trigger_endpoint ContainerRegistryTask#update_trigger_endpoint}.'''
        result = self._values.get("update_trigger_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update_trigger_payload_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#update_trigger_payload_type ContainerRegistryTask#update_trigger_payload_type}.'''
        result = self._values.get("update_trigger_payload_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerRegistryTaskBaseImageTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerRegistryTaskBaseImageTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskBaseImageTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d663788770f465f2050b3d5c3955f3bd9335f452c4f765e9c4037bdc1b08394)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetUpdateTriggerEndpoint")
    def reset_update_trigger_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateTriggerEndpoint", []))

    @jsii.member(jsii_name="resetUpdateTriggerPayloadType")
    def reset_update_trigger_payload_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateTriggerPayloadType", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="updateTriggerEndpointInput")
    def update_trigger_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateTriggerEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="updateTriggerPayloadTypeInput")
    def update_trigger_payload_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateTriggerPayloadTypeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__af52b25b6abde63b5682f41d45b4fdbbd529a7b45581b2005bf62554f6d1afce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9737e7c0f952e3daced42fb6b59be1deb07b8d2318b319e4d863073a3f02879f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5e68758b65a358cc2dd3b6a7c04c9897ab8f3eb2f1632656507f7430e52c963)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updateTriggerEndpoint")
    def update_trigger_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTriggerEndpoint"))

    @update_trigger_endpoint.setter
    def update_trigger_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b2689ae29e4e774c5bb41825e6f1f794ce231ad7a52e43ee003658d43a0424a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateTriggerEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updateTriggerPayloadType")
    def update_trigger_payload_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTriggerPayloadType"))

    @update_trigger_payload_type.setter
    def update_trigger_payload_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b003e42c832c900eb2999652f7dd7c8888b487db94edcf75382a3742af8c862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateTriggerPayloadType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerRegistryTaskBaseImageTrigger]:
        return typing.cast(typing.Optional[ContainerRegistryTaskBaseImageTrigger], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerRegistryTaskBaseImageTrigger],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__715f91d491c26800075275fc4b49d2c566410374f1756892772bd6f7ec3516ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "container_registry_id": "containerRegistryId",
        "name": "name",
        "agent_pool_name": "agentPoolName",
        "agent_setting": "agentSetting",
        "base_image_trigger": "baseImageTrigger",
        "docker_step": "dockerStep",
        "enabled": "enabled",
        "encoded_step": "encodedStep",
        "file_step": "fileStep",
        "id": "id",
        "identity": "identity",
        "is_system_task": "isSystemTask",
        "log_template": "logTemplate",
        "platform": "platform",
        "registry_credential": "registryCredential",
        "source_trigger": "sourceTrigger",
        "tags": "tags",
        "timeout_in_seconds": "timeoutInSeconds",
        "timeouts": "timeouts",
        "timer_trigger": "timerTrigger",
    },
)
class ContainerRegistryTaskConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        container_registry_id: builtins.str,
        name: builtins.str,
        agent_pool_name: typing.Optional[builtins.str] = None,
        agent_setting: typing.Optional[typing.Union[ContainerRegistryTaskAgentSetting, typing.Dict[builtins.str, typing.Any]]] = None,
        base_image_trigger: typing.Optional[typing.Union[ContainerRegistryTaskBaseImageTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_step: typing.Optional[typing.Union["ContainerRegistryTaskDockerStep", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encoded_step: typing.Optional[typing.Union["ContainerRegistryTaskEncodedStep", typing.Dict[builtins.str, typing.Any]]] = None,
        file_step: typing.Optional[typing.Union["ContainerRegistryTaskFileStep", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["ContainerRegistryTaskIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        is_system_task: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_template: typing.Optional[builtins.str] = None,
        platform: typing.Optional[typing.Union["ContainerRegistryTaskPlatform", typing.Dict[builtins.str, typing.Any]]] = None,
        registry_credential: typing.Optional[typing.Union["ContainerRegistryTaskRegistryCredential", typing.Dict[builtins.str, typing.Any]]] = None,
        source_trigger: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerRegistryTaskSourceTrigger", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ContainerRegistryTaskTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timer_trigger: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerRegistryTaskTimerTrigger", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param container_registry_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#container_registry_id ContainerRegistryTask#container_registry_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#name ContainerRegistryTask#name}.
        :param agent_pool_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#agent_pool_name ContainerRegistryTask#agent_pool_name}.
        :param agent_setting: agent_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#agent_setting ContainerRegistryTask#agent_setting}
        :param base_image_trigger: base_image_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#base_image_trigger ContainerRegistryTask#base_image_trigger}
        :param docker_step: docker_step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#docker_step ContainerRegistryTask#docker_step}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#enabled ContainerRegistryTask#enabled}.
        :param encoded_step: encoded_step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#encoded_step ContainerRegistryTask#encoded_step}
        :param file_step: file_step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#file_step ContainerRegistryTask#file_step}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#id ContainerRegistryTask#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#identity ContainerRegistryTask#identity}
        :param is_system_task: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#is_system_task ContainerRegistryTask#is_system_task}.
        :param log_template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#log_template ContainerRegistryTask#log_template}.
        :param platform: platform block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#platform ContainerRegistryTask#platform}
        :param registry_credential: registry_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#registry_credential ContainerRegistryTask#registry_credential}
        :param source_trigger: source_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#source_trigger ContainerRegistryTask#source_trigger}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#tags ContainerRegistryTask#tags}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#timeout_in_seconds ContainerRegistryTask#timeout_in_seconds}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#timeouts ContainerRegistryTask#timeouts}
        :param timer_trigger: timer_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#timer_trigger ContainerRegistryTask#timer_trigger}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(agent_setting, dict):
            agent_setting = ContainerRegistryTaskAgentSetting(**agent_setting)
        if isinstance(base_image_trigger, dict):
            base_image_trigger = ContainerRegistryTaskBaseImageTrigger(**base_image_trigger)
        if isinstance(docker_step, dict):
            docker_step = ContainerRegistryTaskDockerStep(**docker_step)
        if isinstance(encoded_step, dict):
            encoded_step = ContainerRegistryTaskEncodedStep(**encoded_step)
        if isinstance(file_step, dict):
            file_step = ContainerRegistryTaskFileStep(**file_step)
        if isinstance(identity, dict):
            identity = ContainerRegistryTaskIdentity(**identity)
        if isinstance(platform, dict):
            platform = ContainerRegistryTaskPlatform(**platform)
        if isinstance(registry_credential, dict):
            registry_credential = ContainerRegistryTaskRegistryCredential(**registry_credential)
        if isinstance(timeouts, dict):
            timeouts = ContainerRegistryTaskTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9748c8b9d697cdf87d8e15e227dd5baffac2b3cc49949f9708cf9cf085b534)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument container_registry_id", value=container_registry_id, expected_type=type_hints["container_registry_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument agent_pool_name", value=agent_pool_name, expected_type=type_hints["agent_pool_name"])
            check_type(argname="argument agent_setting", value=agent_setting, expected_type=type_hints["agent_setting"])
            check_type(argname="argument base_image_trigger", value=base_image_trigger, expected_type=type_hints["base_image_trigger"])
            check_type(argname="argument docker_step", value=docker_step, expected_type=type_hints["docker_step"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument encoded_step", value=encoded_step, expected_type=type_hints["encoded_step"])
            check_type(argname="argument file_step", value=file_step, expected_type=type_hints["file_step"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument is_system_task", value=is_system_task, expected_type=type_hints["is_system_task"])
            check_type(argname="argument log_template", value=log_template, expected_type=type_hints["log_template"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument registry_credential", value=registry_credential, expected_type=type_hints["registry_credential"])
            check_type(argname="argument source_trigger", value=source_trigger, expected_type=type_hints["source_trigger"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument timer_trigger", value=timer_trigger, expected_type=type_hints["timer_trigger"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_registry_id": container_registry_id,
            "name": name,
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
        if agent_pool_name is not None:
            self._values["agent_pool_name"] = agent_pool_name
        if agent_setting is not None:
            self._values["agent_setting"] = agent_setting
        if base_image_trigger is not None:
            self._values["base_image_trigger"] = base_image_trigger
        if docker_step is not None:
            self._values["docker_step"] = docker_step
        if enabled is not None:
            self._values["enabled"] = enabled
        if encoded_step is not None:
            self._values["encoded_step"] = encoded_step
        if file_step is not None:
            self._values["file_step"] = file_step
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if is_system_task is not None:
            self._values["is_system_task"] = is_system_task
        if log_template is not None:
            self._values["log_template"] = log_template
        if platform is not None:
            self._values["platform"] = platform
        if registry_credential is not None:
            self._values["registry_credential"] = registry_credential
        if source_trigger is not None:
            self._values["source_trigger"] = source_trigger
        if tags is not None:
            self._values["tags"] = tags
        if timeout_in_seconds is not None:
            self._values["timeout_in_seconds"] = timeout_in_seconds
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if timer_trigger is not None:
            self._values["timer_trigger"] = timer_trigger

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
    def container_registry_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#container_registry_id ContainerRegistryTask#container_registry_id}.'''
        result = self._values.get("container_registry_id")
        assert result is not None, "Required property 'container_registry_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#name ContainerRegistryTask#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_pool_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#agent_pool_name ContainerRegistryTask#agent_pool_name}.'''
        result = self._values.get("agent_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def agent_setting(self) -> typing.Optional[ContainerRegistryTaskAgentSetting]:
        '''agent_setting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#agent_setting ContainerRegistryTask#agent_setting}
        '''
        result = self._values.get("agent_setting")
        return typing.cast(typing.Optional[ContainerRegistryTaskAgentSetting], result)

    @builtins.property
    def base_image_trigger(
        self,
    ) -> typing.Optional[ContainerRegistryTaskBaseImageTrigger]:
        '''base_image_trigger block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#base_image_trigger ContainerRegistryTask#base_image_trigger}
        '''
        result = self._values.get("base_image_trigger")
        return typing.cast(typing.Optional[ContainerRegistryTaskBaseImageTrigger], result)

    @builtins.property
    def docker_step(self) -> typing.Optional["ContainerRegistryTaskDockerStep"]:
        '''docker_step block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#docker_step ContainerRegistryTask#docker_step}
        '''
        result = self._values.get("docker_step")
        return typing.cast(typing.Optional["ContainerRegistryTaskDockerStep"], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#enabled ContainerRegistryTask#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encoded_step(self) -> typing.Optional["ContainerRegistryTaskEncodedStep"]:
        '''encoded_step block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#encoded_step ContainerRegistryTask#encoded_step}
        '''
        result = self._values.get("encoded_step")
        return typing.cast(typing.Optional["ContainerRegistryTaskEncodedStep"], result)

    @builtins.property
    def file_step(self) -> typing.Optional["ContainerRegistryTaskFileStep"]:
        '''file_step block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#file_step ContainerRegistryTask#file_step}
        '''
        result = self._values.get("file_step")
        return typing.cast(typing.Optional["ContainerRegistryTaskFileStep"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#id ContainerRegistryTask#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["ContainerRegistryTaskIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#identity ContainerRegistryTask#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["ContainerRegistryTaskIdentity"], result)

    @builtins.property
    def is_system_task(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#is_system_task ContainerRegistryTask#is_system_task}.'''
        result = self._values.get("is_system_task")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#log_template ContainerRegistryTask#log_template}.'''
        result = self._values.get("log_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform(self) -> typing.Optional["ContainerRegistryTaskPlatform"]:
        '''platform block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#platform ContainerRegistryTask#platform}
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional["ContainerRegistryTaskPlatform"], result)

    @builtins.property
    def registry_credential(
        self,
    ) -> typing.Optional["ContainerRegistryTaskRegistryCredential"]:
        '''registry_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#registry_credential ContainerRegistryTask#registry_credential}
        '''
        result = self._values.get("registry_credential")
        return typing.cast(typing.Optional["ContainerRegistryTaskRegistryCredential"], result)

    @builtins.property
    def source_trigger(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerRegistryTaskSourceTrigger"]]]:
        '''source_trigger block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#source_trigger ContainerRegistryTask#source_trigger}
        '''
        result = self._values.get("source_trigger")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerRegistryTaskSourceTrigger"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#tags ContainerRegistryTask#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#timeout_in_seconds ContainerRegistryTask#timeout_in_seconds}.'''
        result = self._values.get("timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ContainerRegistryTaskTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#timeouts ContainerRegistryTask#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ContainerRegistryTaskTimeouts"], result)

    @builtins.property
    def timer_trigger(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerRegistryTaskTimerTrigger"]]]:
        '''timer_trigger block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#timer_trigger ContainerRegistryTask#timer_trigger}
        '''
        result = self._values.get("timer_trigger")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerRegistryTaskTimerTrigger"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerRegistryTaskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskDockerStep",
    jsii_struct_bases=[],
    name_mapping={
        "context_access_token": "contextAccessToken",
        "context_path": "contextPath",
        "dockerfile_path": "dockerfilePath",
        "arguments": "arguments",
        "cache_enabled": "cacheEnabled",
        "image_names": "imageNames",
        "push_enabled": "pushEnabled",
        "secret_arguments": "secretArguments",
        "target": "target",
    },
)
class ContainerRegistryTaskDockerStep:
    def __init__(
        self,
        *,
        context_access_token: builtins.str,
        context_path: builtins.str,
        dockerfile_path: builtins.str,
        arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        image_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        push_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param context_access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_access_token ContainerRegistryTask#context_access_token}.
        :param context_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_path ContainerRegistryTask#context_path}.
        :param dockerfile_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#dockerfile_path ContainerRegistryTask#dockerfile_path}.
        :param arguments: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#arguments ContainerRegistryTask#arguments}.
        :param cache_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#cache_enabled ContainerRegistryTask#cache_enabled}.
        :param image_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#image_names ContainerRegistryTask#image_names}.
        :param push_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#push_enabled ContainerRegistryTask#push_enabled}.
        :param secret_arguments: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#secret_arguments ContainerRegistryTask#secret_arguments}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#target ContainerRegistryTask#target}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81a4cddb725f0ec00f75aa8ad68cd2a21e3c8c426e5aba67907ec3eb31b06c80)
            check_type(argname="argument context_access_token", value=context_access_token, expected_type=type_hints["context_access_token"])
            check_type(argname="argument context_path", value=context_path, expected_type=type_hints["context_path"])
            check_type(argname="argument dockerfile_path", value=dockerfile_path, expected_type=type_hints["dockerfile_path"])
            check_type(argname="argument arguments", value=arguments, expected_type=type_hints["arguments"])
            check_type(argname="argument cache_enabled", value=cache_enabled, expected_type=type_hints["cache_enabled"])
            check_type(argname="argument image_names", value=image_names, expected_type=type_hints["image_names"])
            check_type(argname="argument push_enabled", value=push_enabled, expected_type=type_hints["push_enabled"])
            check_type(argname="argument secret_arguments", value=secret_arguments, expected_type=type_hints["secret_arguments"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "context_access_token": context_access_token,
            "context_path": context_path,
            "dockerfile_path": dockerfile_path,
        }
        if arguments is not None:
            self._values["arguments"] = arguments
        if cache_enabled is not None:
            self._values["cache_enabled"] = cache_enabled
        if image_names is not None:
            self._values["image_names"] = image_names
        if push_enabled is not None:
            self._values["push_enabled"] = push_enabled
        if secret_arguments is not None:
            self._values["secret_arguments"] = secret_arguments
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def context_access_token(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_access_token ContainerRegistryTask#context_access_token}.'''
        result = self._values.get("context_access_token")
        assert result is not None, "Required property 'context_access_token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def context_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_path ContainerRegistryTask#context_path}.'''
        result = self._values.get("context_path")
        assert result is not None, "Required property 'context_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dockerfile_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#dockerfile_path ContainerRegistryTask#dockerfile_path}.'''
        result = self._values.get("dockerfile_path")
        assert result is not None, "Required property 'dockerfile_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arguments(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#arguments ContainerRegistryTask#arguments}.'''
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def cache_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#cache_enabled ContainerRegistryTask#cache_enabled}.'''
        result = self._values.get("cache_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def image_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#image_names ContainerRegistryTask#image_names}.'''
        result = self._values.get("image_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def push_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#push_enabled ContainerRegistryTask#push_enabled}.'''
        result = self._values.get("push_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secret_arguments(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#secret_arguments ContainerRegistryTask#secret_arguments}.'''
        result = self._values.get("secret_arguments")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#target ContainerRegistryTask#target}.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerRegistryTaskDockerStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerRegistryTaskDockerStepOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskDockerStepOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3df1e3e4035aaa58865b1d322f11e79b620573de732ad7177d446c7d16c88c55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArguments")
    def reset_arguments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArguments", []))

    @jsii.member(jsii_name="resetCacheEnabled")
    def reset_cache_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheEnabled", []))

    @jsii.member(jsii_name="resetImageNames")
    def reset_image_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageNames", []))

    @jsii.member(jsii_name="resetPushEnabled")
    def reset_push_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPushEnabled", []))

    @jsii.member(jsii_name="resetSecretArguments")
    def reset_secret_arguments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretArguments", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="argumentsInput")
    def arguments_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "argumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheEnabledInput")
    def cache_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cacheEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="contextAccessTokenInput")
    def context_access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextAccessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="contextPathInput")
    def context_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextPathInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerfilePathInput")
    def dockerfile_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerfilePathInput"))

    @builtins.property
    @jsii.member(jsii_name="imageNamesInput")
    def image_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "imageNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="pushEnabledInput")
    def push_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pushEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="secretArgumentsInput")
    def secret_arguments_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "secretArgumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="arguments")
    def arguments(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "arguments"))

    @arguments.setter
    def arguments(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84dff7e27c0f9ab55771adf7fd42473f6a52078f66cc1f37e6cc10f5c175d7c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arguments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cacheEnabled")
    def cache_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cacheEnabled"))

    @cache_enabled.setter
    def cache_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70d2b95c162e33dd51216857d0fd17b323cddf33be5cee0974a18a8a46cb3f34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contextAccessToken")
    def context_access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextAccessToken"))

    @context_access_token.setter
    def context_access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b63da8f22dd115d4ccfee84e911edad7471cc57c42ce2171b281392f585e129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextAccessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contextPath")
    def context_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextPath"))

    @context_path.setter
    def context_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b97c3b8f02e042cc0baaf80a05e076b8d5b590e670cf7a600150a7b3e936916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dockerfilePath")
    def dockerfile_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dockerfilePath"))

    @dockerfile_path.setter
    def dockerfile_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c34db1b3f87b5392bc5fc2c00a464c7a535a33996bf064d85cdf4d2118a83a1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerfilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageNames")
    def image_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "imageNames"))

    @image_names.setter
    def image_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819c5ff978e1c6c4689d22accd802aca839d4f5f4cbb769f199a4b7103512373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pushEnabled")
    def push_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pushEnabled"))

    @push_enabled.setter
    def push_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eddd9c3dd0f702c2e56869ffb4b73dc09452ff042a703a9b5ba78cac94508fd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pushEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretArguments")
    def secret_arguments(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "secretArguments"))

    @secret_arguments.setter
    def secret_arguments(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c934edf8deeee60e4fdaa670b698d26b83ed3e762e928c3fb40352ab775f741)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretArguments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b81a42c5c01bea7e84cfe7ecb305944db2292ac4c5400a35291ba96c9247d8bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerRegistryTaskDockerStep]:
        return typing.cast(typing.Optional[ContainerRegistryTaskDockerStep], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerRegistryTaskDockerStep],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__473c8845743fca7d2e729594640055cfe30f933c8855937911deb291bfe85aba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskEncodedStep",
    jsii_struct_bases=[],
    name_mapping={
        "task_content": "taskContent",
        "context_access_token": "contextAccessToken",
        "context_path": "contextPath",
        "secret_values": "secretValues",
        "value_content": "valueContent",
        "values": "values",
    },
)
class ContainerRegistryTaskEncodedStep:
    def __init__(
        self,
        *,
        task_content: builtins.str,
        context_access_token: typing.Optional[builtins.str] = None,
        context_path: typing.Optional[builtins.str] = None,
        secret_values: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        value_content: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param task_content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#task_content ContainerRegistryTask#task_content}.
        :param context_access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_access_token ContainerRegistryTask#context_access_token}.
        :param context_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_path ContainerRegistryTask#context_path}.
        :param secret_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#secret_values ContainerRegistryTask#secret_values}.
        :param value_content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#value_content ContainerRegistryTask#value_content}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#values ContainerRegistryTask#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd2d7c7b2a9deeb58a460b41eadc1bb8e5944b06aee0c85557cdde3d6b6c51e2)
            check_type(argname="argument task_content", value=task_content, expected_type=type_hints["task_content"])
            check_type(argname="argument context_access_token", value=context_access_token, expected_type=type_hints["context_access_token"])
            check_type(argname="argument context_path", value=context_path, expected_type=type_hints["context_path"])
            check_type(argname="argument secret_values", value=secret_values, expected_type=type_hints["secret_values"])
            check_type(argname="argument value_content", value=value_content, expected_type=type_hints["value_content"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "task_content": task_content,
        }
        if context_access_token is not None:
            self._values["context_access_token"] = context_access_token
        if context_path is not None:
            self._values["context_path"] = context_path
        if secret_values is not None:
            self._values["secret_values"] = secret_values
        if value_content is not None:
            self._values["value_content"] = value_content
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def task_content(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#task_content ContainerRegistryTask#task_content}.'''
        result = self._values.get("task_content")
        assert result is not None, "Required property 'task_content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def context_access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_access_token ContainerRegistryTask#context_access_token}.'''
        result = self._values.get("context_access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def context_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_path ContainerRegistryTask#context_path}.'''
        result = self._values.get("context_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_values(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#secret_values ContainerRegistryTask#secret_values}.'''
        result = self._values.get("secret_values")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def value_content(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#value_content ContainerRegistryTask#value_content}.'''
        result = self._values.get("value_content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#values ContainerRegistryTask#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerRegistryTaskEncodedStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerRegistryTaskEncodedStepOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskEncodedStepOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51fd0acda3101463afc04a7d0fa312cd40f2cb434f5fc5e9e9838df3f5d52028)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContextAccessToken")
    def reset_context_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContextAccessToken", []))

    @jsii.member(jsii_name="resetContextPath")
    def reset_context_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContextPath", []))

    @jsii.member(jsii_name="resetSecretValues")
    def reset_secret_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretValues", []))

    @jsii.member(jsii_name="resetValueContent")
    def reset_value_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueContent", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="contextAccessTokenInput")
    def context_access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextAccessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="contextPathInput")
    def context_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextPathInput"))

    @builtins.property
    @jsii.member(jsii_name="secretValuesInput")
    def secret_values_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "secretValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="taskContentInput")
    def task_content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskContentInput"))

    @builtins.property
    @jsii.member(jsii_name="valueContentInput")
    def value_content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueContentInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="contextAccessToken")
    def context_access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextAccessToken"))

    @context_access_token.setter
    def context_access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3af728da44b0831e9de0868d266e02658d3d679495695086f64c8ff3eb407bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextAccessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contextPath")
    def context_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextPath"))

    @context_path.setter
    def context_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b227dd435296b678e65bc438175e555a59b65f4a4f5f352b67cf344f19d9d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretValues")
    def secret_values(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "secretValues"))

    @secret_values.setter
    def secret_values(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c45f51271efa452d2fa138faabe827da3492e7d7d1d68717866721909242815c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskContent")
    def task_content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskContent"))

    @task_content.setter
    def task_content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__089e35cd520d02593fc2b6709efd9fbbd6a693d41c6e1683e5ddea3bd3de3ee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskContent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueContent")
    def value_content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueContent"))

    @value_content.setter
    def value_content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2896eb28c0ac662110489142153526d187055c193ead6c202b694da5cc909386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueContent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e784306dde41735d4bc8a1c29b5670e5abdcd6f44ac4adcfb5e00cfee1e2074b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerRegistryTaskEncodedStep]:
        return typing.cast(typing.Optional[ContainerRegistryTaskEncodedStep], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerRegistryTaskEncodedStep],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d01825f6207bce3eb5b66e80c58e6e5908c94e10823a7863ae22f9f345450c6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskFileStep",
    jsii_struct_bases=[],
    name_mapping={
        "task_file_path": "taskFilePath",
        "context_access_token": "contextAccessToken",
        "context_path": "contextPath",
        "secret_values": "secretValues",
        "value_file_path": "valueFilePath",
        "values": "values",
    },
)
class ContainerRegistryTaskFileStep:
    def __init__(
        self,
        *,
        task_file_path: builtins.str,
        context_access_token: typing.Optional[builtins.str] = None,
        context_path: typing.Optional[builtins.str] = None,
        secret_values: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        value_file_path: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param task_file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#task_file_path ContainerRegistryTask#task_file_path}.
        :param context_access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_access_token ContainerRegistryTask#context_access_token}.
        :param context_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_path ContainerRegistryTask#context_path}.
        :param secret_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#secret_values ContainerRegistryTask#secret_values}.
        :param value_file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#value_file_path ContainerRegistryTask#value_file_path}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#values ContainerRegistryTask#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eeeaf8c0e78e74b0c2bc4afa4b08526974bab3d2a8d75f96617ca19e03be1c3)
            check_type(argname="argument task_file_path", value=task_file_path, expected_type=type_hints["task_file_path"])
            check_type(argname="argument context_access_token", value=context_access_token, expected_type=type_hints["context_access_token"])
            check_type(argname="argument context_path", value=context_path, expected_type=type_hints["context_path"])
            check_type(argname="argument secret_values", value=secret_values, expected_type=type_hints["secret_values"])
            check_type(argname="argument value_file_path", value=value_file_path, expected_type=type_hints["value_file_path"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "task_file_path": task_file_path,
        }
        if context_access_token is not None:
            self._values["context_access_token"] = context_access_token
        if context_path is not None:
            self._values["context_path"] = context_path
        if secret_values is not None:
            self._values["secret_values"] = secret_values
        if value_file_path is not None:
            self._values["value_file_path"] = value_file_path
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def task_file_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#task_file_path ContainerRegistryTask#task_file_path}.'''
        result = self._values.get("task_file_path")
        assert result is not None, "Required property 'task_file_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def context_access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_access_token ContainerRegistryTask#context_access_token}.'''
        result = self._values.get("context_access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def context_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#context_path ContainerRegistryTask#context_path}.'''
        result = self._values.get("context_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_values(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#secret_values ContainerRegistryTask#secret_values}.'''
        result = self._values.get("secret_values")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def value_file_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#value_file_path ContainerRegistryTask#value_file_path}.'''
        result = self._values.get("value_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#values ContainerRegistryTask#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerRegistryTaskFileStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerRegistryTaskFileStepOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskFileStepOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6157be53d0b513b57da7e783ecdb60e90e5225a38d63b5de4dc2a1d62c3d814)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContextAccessToken")
    def reset_context_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContextAccessToken", []))

    @jsii.member(jsii_name="resetContextPath")
    def reset_context_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContextPath", []))

    @jsii.member(jsii_name="resetSecretValues")
    def reset_secret_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretValues", []))

    @jsii.member(jsii_name="resetValueFilePath")
    def reset_value_file_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueFilePath", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="contextAccessTokenInput")
    def context_access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextAccessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="contextPathInput")
    def context_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextPathInput"))

    @builtins.property
    @jsii.member(jsii_name="secretValuesInput")
    def secret_values_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "secretValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="taskFilePathInput")
    def task_file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskFilePathInput"))

    @builtins.property
    @jsii.member(jsii_name="valueFilePathInput")
    def value_file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueFilePathInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="contextAccessToken")
    def context_access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextAccessToken"))

    @context_access_token.setter
    def context_access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb0dcd836a902545ee051ff09f866412fa01aa0ef7d25222efa3e3b0bd93f5dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextAccessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contextPath")
    def context_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextPath"))

    @context_path.setter
    def context_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3020e990fad310f79d4b085e3a995d2eddc55cf21265474fd74bda4aa69e42b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretValues")
    def secret_values(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "secretValues"))

    @secret_values.setter
    def secret_values(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ea7b67ff0a573cf969d933fc87a0d40614ca1f5600f1087ac1ed9b8d740ff12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskFilePath")
    def task_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskFilePath"))

    @task_file_path.setter
    def task_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76f783ce7bd178532ebf2496b768ce7d4f8d6c2b025b571dbf0e4869fbd20aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueFilePath")
    def value_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueFilePath"))

    @value_file_path.setter
    def value_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d516a74883f19233cdecc8fcfe4835a261291f6cdb6ff7d1e4a40ad36f0d0c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07ac71282db81fcedba408de1b835e116787be535f2ce9fb6f55de61caa311e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerRegistryTaskFileStep]:
        return typing.cast(typing.Optional[ContainerRegistryTaskFileStep], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerRegistryTaskFileStep],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ddd0fa7f037fd29d6e91cfd975346092b1932290c0525a597de7e42dc172508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class ContainerRegistryTaskIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#type ContainerRegistryTask#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#identity_ids ContainerRegistryTask#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac8e5f6d04d631c02393ce2724036db15a37bd219baf1fc17e8d8a8eae7bb13e)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#type ContainerRegistryTask#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#identity_ids ContainerRegistryTask#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerRegistryTaskIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerRegistryTaskIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4378c811bfd0802cad7199ad07bf2b00251f4dc60e31436f2fd783a588f5e69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ec69d2fa46af1af503bcde190a3d30663bec3c15379c11eb0c3bbccf8eaa535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d60a701c3cf4f3f85e5cc816b80f63f6f175846ffa24e5055feda4f1121463e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerRegistryTaskIdentity]:
        return typing.cast(typing.Optional[ContainerRegistryTaskIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerRegistryTaskIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cb0d76a9be638d198608853b55903481271320a8bd24aec4b6b2cfdbd9120e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskPlatform",
    jsii_struct_bases=[],
    name_mapping={"os": "os", "architecture": "architecture", "variant": "variant"},
)
class ContainerRegistryTaskPlatform:
    def __init__(
        self,
        *,
        os: builtins.str,
        architecture: typing.Optional[builtins.str] = None,
        variant: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#os ContainerRegistryTask#os}.
        :param architecture: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#architecture ContainerRegistryTask#architecture}.
        :param variant: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#variant ContainerRegistryTask#variant}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c88ff75fb6e805833fce44040ab0ac810672d9031ae20ed06773c9538b44519)
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument variant", value=variant, expected_type=type_hints["variant"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "os": os,
        }
        if architecture is not None:
            self._values["architecture"] = architecture
        if variant is not None:
            self._values["variant"] = variant

    @builtins.property
    def os(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#os ContainerRegistryTask#os}.'''
        result = self._values.get("os")
        assert result is not None, "Required property 'os' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#architecture ContainerRegistryTask#architecture}.'''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variant(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#variant ContainerRegistryTask#variant}.'''
        result = self._values.get("variant")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerRegistryTaskPlatform(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerRegistryTaskPlatformOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskPlatformOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b414f46314d9f03ce75a09a854aa488c09fbdf88b192150924ebd0da688f04df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArchitecture")
    def reset_architecture(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchitecture", []))

    @jsii.member(jsii_name="resetVariant")
    def reset_variant(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariant", []))

    @builtins.property
    @jsii.member(jsii_name="architectureInput")
    def architecture_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "architectureInput"))

    @builtins.property
    @jsii.member(jsii_name="osInput")
    def os_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osInput"))

    @builtins.property
    @jsii.member(jsii_name="variantInput")
    def variant_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "variantInput"))

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "architecture"))

    @architecture.setter
    def architecture(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9d7e9c6ec684ad163368250964b8246f8a2b674d945699940385b231b4420bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "architecture", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="os")
    def os(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "os"))

    @os.setter
    def os(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f34816951c09d3cc3d5976c8b4dabe72d366736c760d136b37bb81f2b2f71bdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "os", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="variant")
    def variant(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "variant"))

    @variant.setter
    def variant(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b3dce7c5597a1176e1025b5ef7d5c57b3728a8158aefd9498be91be8e1a8ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variant", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerRegistryTaskPlatform]:
        return typing.cast(typing.Optional[ContainerRegistryTaskPlatform], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerRegistryTaskPlatform],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64211bad1b363371798af08f46183d04709afccfa7b33b6f5fa67baa844af05b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskRegistryCredential",
    jsii_struct_bases=[],
    name_mapping={"custom": "custom", "source": "source"},
)
class ContainerRegistryTaskRegistryCredential:
    def __init__(
        self,
        *,
        custom: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerRegistryTaskRegistryCredentialCustom", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source: typing.Optional[typing.Union["ContainerRegistryTaskRegistryCredentialSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom: custom block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#custom ContainerRegistryTask#custom}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#source ContainerRegistryTask#source}
        '''
        if isinstance(source, dict):
            source = ContainerRegistryTaskRegistryCredentialSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4199a3d1a43bf503481270d4db4901809e6134d3b75bb772314b8674880fb4e)
            check_type(argname="argument custom", value=custom, expected_type=type_hints["custom"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom is not None:
            self._values["custom"] = custom
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def custom(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerRegistryTaskRegistryCredentialCustom"]]]:
        '''custom block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#custom ContainerRegistryTask#custom}
        '''
        result = self._values.get("custom")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerRegistryTaskRegistryCredentialCustom"]]], result)

    @builtins.property
    def source(
        self,
    ) -> typing.Optional["ContainerRegistryTaskRegistryCredentialSource"]:
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#source ContainerRegistryTask#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional["ContainerRegistryTaskRegistryCredentialSource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerRegistryTaskRegistryCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskRegistryCredentialCustom",
    jsii_struct_bases=[],
    name_mapping={
        "login_server": "loginServer",
        "identity": "identity",
        "password": "password",
        "username": "username",
    },
)
class ContainerRegistryTaskRegistryCredentialCustom:
    def __init__(
        self,
        *,
        login_server: builtins.str,
        identity: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param login_server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#login_server ContainerRegistryTask#login_server}.
        :param identity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#identity ContainerRegistryTask#identity}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#password ContainerRegistryTask#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#username ContainerRegistryTask#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__974ab38de78f589875ef1aff9507b870958437372140761f797166246588f461)
            check_type(argname="argument login_server", value=login_server, expected_type=type_hints["login_server"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "login_server": login_server,
        }
        if identity is not None:
            self._values["identity"] = identity
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def login_server(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#login_server ContainerRegistryTask#login_server}.'''
        result = self._values.get("login_server")
        assert result is not None, "Required property 'login_server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#identity ContainerRegistryTask#identity}.'''
        result = self._values.get("identity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#password ContainerRegistryTask#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#username ContainerRegistryTask#username}.'''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerRegistryTaskRegistryCredentialCustom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerRegistryTaskRegistryCredentialCustomList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskRegistryCredentialCustomList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__071d2c60e9655d03f2f1f118bf2a3aa482a7b6977feca52a5eec8d52fcbe3073)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerRegistryTaskRegistryCredentialCustomOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edfdb943dad8af20c2ba990e5603bae1e17e8fa49e2500751e4d8ac9bd30ca7a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerRegistryTaskRegistryCredentialCustomOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8582dd94b6f4b8fb2b70302faefd926516b19d52e40f9757b9b10f2a77293f2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__111f1de7c07ded26abcfb74383670c4fb05847ed1a748f73173fb3e247406f12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d2ca799343fb752ba234d200bb00b10f2e76792578492013166af607b9f0dcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerRegistryTaskRegistryCredentialCustom]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerRegistryTaskRegistryCredentialCustom]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerRegistryTaskRegistryCredentialCustom]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d563b349548c26f7c1a915ba7e589d67407d03979365d3418b8b4ebb52fd410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerRegistryTaskRegistryCredentialCustomOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskRegistryCredentialCustomOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a8122b6ff42c14471ceda741d3a840632536985886d8dfa2aa4ff2082c119f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="loginServerInput")
    def login_server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loginServerInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ee634af9087e37aa172cab04ef19e5f16229d9cb4ea310168b737a5c83e6002b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loginServer")
    def login_server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginServer"))

    @login_server.setter
    def login_server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e7cc69eeb80d8097af695a1bce71280fbf8e0b32531442d1579cf91f41d2a52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginServer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f04283c7d89d6f713c0578346bf13d3b0e6a4f3874fb83d02ac5e2c1e2d8493d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35c3d896d4a19aa8d13db3004d0a2946ed5f6246f0ef2b1cb620622ca0f19ee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerRegistryTaskRegistryCredentialCustom]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerRegistryTaskRegistryCredentialCustom]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerRegistryTaskRegistryCredentialCustom]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c53f103e2a6e1af9c7603a9ad4cbbe948fe9d5feb0d452ac909ba0983660447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerRegistryTaskRegistryCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskRegistryCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3b97b9f1649574a6dd3fd0a06abfd06b01c0a4acca86fb08a82c9bf76610309)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustom")
    def put_custom(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerRegistryTaskRegistryCredentialCustom, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__527d496ce09b8871d45a9b0b8610dcfa8122c872c130a471ab5d6283906265a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustom", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(self, *, login_mode: builtins.str) -> None:
        '''
        :param login_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#login_mode ContainerRegistryTask#login_mode}.
        '''
        value = ContainerRegistryTaskRegistryCredentialSource(login_mode=login_mode)

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="resetCustom")
    def reset_custom(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustom", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="custom")
    def custom(self) -> ContainerRegistryTaskRegistryCredentialCustomList:
        return typing.cast(ContainerRegistryTaskRegistryCredentialCustomList, jsii.get(self, "custom"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "ContainerRegistryTaskRegistryCredentialSourceOutputReference":
        return typing.cast("ContainerRegistryTaskRegistryCredentialSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="customInput")
    def custom_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerRegistryTaskRegistryCredentialCustom]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerRegistryTaskRegistryCredentialCustom]]], jsii.get(self, "customInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(
        self,
    ) -> typing.Optional["ContainerRegistryTaskRegistryCredentialSource"]:
        return typing.cast(typing.Optional["ContainerRegistryTaskRegistryCredentialSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerRegistryTaskRegistryCredential]:
        return typing.cast(typing.Optional[ContainerRegistryTaskRegistryCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerRegistryTaskRegistryCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b89b22f147aef23f77e0be811e0be0450207aa361b36ec22dc0d170e14fa189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskRegistryCredentialSource",
    jsii_struct_bases=[],
    name_mapping={"login_mode": "loginMode"},
)
class ContainerRegistryTaskRegistryCredentialSource:
    def __init__(self, *, login_mode: builtins.str) -> None:
        '''
        :param login_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#login_mode ContainerRegistryTask#login_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__249aa9db1270b19364f7a1f0897ce303d30a0b2be875511d79608cc795bec4fb)
            check_type(argname="argument login_mode", value=login_mode, expected_type=type_hints["login_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "login_mode": login_mode,
        }

    @builtins.property
    def login_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#login_mode ContainerRegistryTask#login_mode}.'''
        result = self._values.get("login_mode")
        assert result is not None, "Required property 'login_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerRegistryTaskRegistryCredentialSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerRegistryTaskRegistryCredentialSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskRegistryCredentialSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e679989f4bd5ac8e045c014ac35223cf08f75a77edf2ec9e0fd119f11f960573)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="loginModeInput")
    def login_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loginModeInput"))

    @builtins.property
    @jsii.member(jsii_name="loginMode")
    def login_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginMode"))

    @login_mode.setter
    def login_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e9367f25ec2c819a66c91b17bc80b89ab4da9e56f72cc564adb61e814f9b05c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerRegistryTaskRegistryCredentialSource]:
        return typing.cast(typing.Optional[ContainerRegistryTaskRegistryCredentialSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerRegistryTaskRegistryCredentialSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3feaf5e82bad79f43b3121344a4985dff6f39358ae70d8c14d5ad4e5ee4e30f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskSourceTrigger",
    jsii_struct_bases=[],
    name_mapping={
        "events": "events",
        "name": "name",
        "repository_url": "repositoryUrl",
        "source_type": "sourceType",
        "authentication": "authentication",
        "branch": "branch",
        "enabled": "enabled",
    },
)
class ContainerRegistryTaskSourceTrigger:
    def __init__(
        self,
        *,
        events: typing.Sequence[builtins.str],
        name: builtins.str,
        repository_url: builtins.str,
        source_type: builtins.str,
        authentication: typing.Optional[typing.Union["ContainerRegistryTaskSourceTriggerAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        branch: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#events ContainerRegistryTask#events}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#name ContainerRegistryTask#name}.
        :param repository_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#repository_url ContainerRegistryTask#repository_url}.
        :param source_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#source_type ContainerRegistryTask#source_type}.
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#authentication ContainerRegistryTask#authentication}
        :param branch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#branch ContainerRegistryTask#branch}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#enabled ContainerRegistryTask#enabled}.
        '''
        if isinstance(authentication, dict):
            authentication = ContainerRegistryTaskSourceTriggerAuthentication(**authentication)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c50750f641cf5f1707c39d05c7201d6a1265ece2a3fbe644305b4a3df3da1b)
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument repository_url", value=repository_url, expected_type=type_hints["repository_url"])
            check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            check_type(argname="argument authentication", value=authentication, expected_type=type_hints["authentication"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "events": events,
            "name": name,
            "repository_url": repository_url,
            "source_type": source_type,
        }
        if authentication is not None:
            self._values["authentication"] = authentication
        if branch is not None:
            self._values["branch"] = branch
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def events(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#events ContainerRegistryTask#events}.'''
        result = self._values.get("events")
        assert result is not None, "Required property 'events' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#name ContainerRegistryTask#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#repository_url ContainerRegistryTask#repository_url}.'''
        result = self._values.get("repository_url")
        assert result is not None, "Required property 'repository_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#source_type ContainerRegistryTask#source_type}.'''
        result = self._values.get("source_type")
        assert result is not None, "Required property 'source_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication(
        self,
    ) -> typing.Optional["ContainerRegistryTaskSourceTriggerAuthentication"]:
        '''authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#authentication ContainerRegistryTask#authentication}
        '''
        result = self._values.get("authentication")
        return typing.cast(typing.Optional["ContainerRegistryTaskSourceTriggerAuthentication"], result)

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#branch ContainerRegistryTask#branch}.'''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#enabled ContainerRegistryTask#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerRegistryTaskSourceTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskSourceTriggerAuthentication",
    jsii_struct_bases=[],
    name_mapping={
        "token": "token",
        "token_type": "tokenType",
        "expire_in_seconds": "expireInSeconds",
        "refresh_token": "refreshToken",
        "scope": "scope",
    },
)
class ContainerRegistryTaskSourceTriggerAuthentication:
    def __init__(
        self,
        *,
        token: builtins.str,
        token_type: builtins.str,
        expire_in_seconds: typing.Optional[jsii.Number] = None,
        refresh_token: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#token ContainerRegistryTask#token}.
        :param token_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#token_type ContainerRegistryTask#token_type}.
        :param expire_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#expire_in_seconds ContainerRegistryTask#expire_in_seconds}.
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#refresh_token ContainerRegistryTask#refresh_token}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#scope ContainerRegistryTask#scope}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__471438e7c0d9a6eaeefc117fd4b1735fb94e95e1305d61a29734c0af18810fe7)
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument token_type", value=token_type, expected_type=type_hints["token_type"])
            check_type(argname="argument expire_in_seconds", value=expire_in_seconds, expected_type=type_hints["expire_in_seconds"])
            check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "token": token,
            "token_type": token_type,
        }
        if expire_in_seconds is not None:
            self._values["expire_in_seconds"] = expire_in_seconds
        if refresh_token is not None:
            self._values["refresh_token"] = refresh_token
        if scope is not None:
            self._values["scope"] = scope

    @builtins.property
    def token(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#token ContainerRegistryTask#token}.'''
        result = self._values.get("token")
        assert result is not None, "Required property 'token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#token_type ContainerRegistryTask#token_type}.'''
        result = self._values.get("token_type")
        assert result is not None, "Required property 'token_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expire_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#expire_in_seconds ContainerRegistryTask#expire_in_seconds}.'''
        result = self._values.get("expire_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def refresh_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#refresh_token ContainerRegistryTask#refresh_token}.'''
        result = self._values.get("refresh_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#scope ContainerRegistryTask#scope}.'''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerRegistryTaskSourceTriggerAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerRegistryTaskSourceTriggerAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskSourceTriggerAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f35309efc00a538b9acfef31ee80671e326c956c7e2b598f2a6629b1faf8cb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExpireInSeconds")
    def reset_expire_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpireInSeconds", []))

    @jsii.member(jsii_name="resetRefreshToken")
    def reset_refresh_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshToken", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @builtins.property
    @jsii.member(jsii_name="expireInSecondsInput")
    def expire_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expireInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenInput")
    def refresh_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refreshTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenTypeInput")
    def token_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="expireInSeconds")
    def expire_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expireInSeconds"))

    @expire_in_seconds.setter
    def expire_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a090d00486caa193e77df16593efd1711d6044e1e1dfe857e2676896c1ff74c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expireInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="refreshToken")
    def refresh_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshToken"))

    @refresh_token.setter
    def refresh_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc192c62d32e381784dae9779c2e33964cf03a8f6691802f960d0e714b3c926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbeebf8ee27a8f7fdb6926607a203542bfafe95f6c96ffb58ea84a19306d6a5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @token.setter
    def token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__446ba9207681702f407ee600f8e5b9f57e105953179ce88e63c429a36598d7d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenType")
    def token_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenType"))

    @token_type.setter
    def token_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b36ab9617a27a2d7bca6c77d6715131642894869af9d2b64c5a36e37253dc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerRegistryTaskSourceTriggerAuthentication]:
        return typing.cast(typing.Optional[ContainerRegistryTaskSourceTriggerAuthentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerRegistryTaskSourceTriggerAuthentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e540df209ba9796a14a67fea6763557be144c724a6155f006f8796327179a614)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerRegistryTaskSourceTriggerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskSourceTriggerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99f6b45dc8d2c98e0e4c4abe0e7978ff91a7acfe30b27c75326b37f59423d860)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerRegistryTaskSourceTriggerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc179f9b2df68cf01a50c314cdbfc0839c1caea601ded42e3ada51a0da356720)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerRegistryTaskSourceTriggerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d882367fa1e68468932787b95242e43a3fff3d415500273a9a969d280bd44771)
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
            type_hints = typing.get_type_hints(_typecheckingstub__106094454b24032a7b002b0900b9bbcd684820e1b75bbbf2a66181468e8bbf4a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__714d1a76638ad171caa797fea2b2bb4adf4f89ea29efe7f991359c9d47424ed3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerRegistryTaskSourceTrigger]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerRegistryTaskSourceTrigger]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerRegistryTaskSourceTrigger]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6df29cd9f5050dc137f6299b1f88f404cf566edffc626cc561c63e7ddb98a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerRegistryTaskSourceTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskSourceTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b069cc2e017c0d606c968e49fe1cd692c348be2ac76d5a5e90d92a019ccf62c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAuthentication")
    def put_authentication(
        self,
        *,
        token: builtins.str,
        token_type: builtins.str,
        expire_in_seconds: typing.Optional[jsii.Number] = None,
        refresh_token: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#token ContainerRegistryTask#token}.
        :param token_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#token_type ContainerRegistryTask#token_type}.
        :param expire_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#expire_in_seconds ContainerRegistryTask#expire_in_seconds}.
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#refresh_token ContainerRegistryTask#refresh_token}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#scope ContainerRegistryTask#scope}.
        '''
        value = ContainerRegistryTaskSourceTriggerAuthentication(
            token=token,
            token_type=token_type,
            expire_in_seconds=expire_in_seconds,
            refresh_token=refresh_token,
            scope=scope,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthentication", [value]))

    @jsii.member(jsii_name="resetAuthentication")
    def reset_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthentication", []))

    @jsii.member(jsii_name="resetBranch")
    def reset_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranch", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="authentication")
    def authentication(
        self,
    ) -> ContainerRegistryTaskSourceTriggerAuthenticationOutputReference:
        return typing.cast(ContainerRegistryTaskSourceTriggerAuthenticationOutputReference, jsii.get(self, "authentication"))

    @builtins.property
    @jsii.member(jsii_name="authenticationInput")
    def authentication_input(
        self,
    ) -> typing.Optional[ContainerRegistryTaskSourceTriggerAuthentication]:
        return typing.cast(typing.Optional[ContainerRegistryTaskSourceTriggerAuthentication], jsii.get(self, "authenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="branchInput")
    def branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryUrlInput")
    def repository_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceTypeInput")
    def source_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__162190f24654e228478ede05e8583e67815ac2d5a25d2a73190225bcade60352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__959792a3ac66ab30433265f95aa2e2668fe5d251c5e0b22ac1904e2c24b79c72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="events")
    def events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "events"))

    @events.setter
    def events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b22ee9cbd8ea2fbff51d1da0cf1e118f8fd2533279c1e9fc4c0d8560ec5a454)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "events", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9153fe786c45727daad85d9b1a0ffd2db907a46b1d8cba4fab8098ef03e1815e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryUrl")
    def repository_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryUrl"))

    @repository_url.setter
    def repository_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa819440066bb50037a5e92c582baa9c337f045066f61ee8a76a98bdffa17060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceType"))

    @source_type.setter
    def source_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3298490db82c1ee9952cbc34f5dca0de7c230bf0f2cd807ccfe3d410d68e426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerRegistryTaskSourceTrigger]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerRegistryTaskSourceTrigger]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerRegistryTaskSourceTrigger]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395df2a701641c44ff2fd2768ab127ee2ef501a61e1d330a1b9ba80d6cb00387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ContainerRegistryTaskTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#create ContainerRegistryTask#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#delete ContainerRegistryTask#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#read ContainerRegistryTask#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#update ContainerRegistryTask#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e09c783492b92e9f08b507088a77305fe9c4037041ce9edf75ba97f15fa61d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#create ContainerRegistryTask#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#delete ContainerRegistryTask#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#read ContainerRegistryTask#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#update ContainerRegistryTask#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerRegistryTaskTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerRegistryTaskTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb2c16b81de0cfbf6c1d524037d5117763289a65c2bb44a9c0476bf93d229ce8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f5ea8d79d67bd948157bc3acfa3784f1d7ac0e796c045f53df266bfc0f1e56c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55696c6450359cef594f7392efe2024e975344201470c9387ef1e4c03895417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2e2276dbe4505d3fecd2245284174a371fcaaabcd08165ae0b640d55074728)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__319d60199186d288908b6ab1a0111128044c3a59c31991ea196217cd74df3236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerRegistryTaskTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerRegistryTaskTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerRegistryTaskTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__086ab23f9aeda6c09184e2ddfc68cf7f167cbeb893b53624513dcf3e2dc28b77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskTimerTrigger",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "schedule": "schedule", "enabled": "enabled"},
)
class ContainerRegistryTaskTimerTrigger:
    def __init__(
        self,
        *,
        name: builtins.str,
        schedule: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#name ContainerRegistryTask#name}.
        :param schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#schedule ContainerRegistryTask#schedule}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#enabled ContainerRegistryTask#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f9a39d9724c218aca9bb27e99dc12cb133b1e5ae7c3e9c15492ecbad92c171e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "schedule": schedule,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#name ContainerRegistryTask#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#schedule ContainerRegistryTask#schedule}.'''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_registry_task#enabled ContainerRegistryTask#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerRegistryTaskTimerTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerRegistryTaskTimerTriggerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskTimerTriggerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b39260486a8eb0466912c365def55fd797b3f06ea5dda201c8a8f7e03777b350)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerRegistryTaskTimerTriggerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4339c49c9e0db6be12f6f7ae85dd6b89f368fe24891b6f77344874479500caed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerRegistryTaskTimerTriggerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c51557bfe75ffd76ebdebf8207dfc1e92a29d63236bfc8880b23efd2b1a39de2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccd2bf586eeff749adc68606cdd65cc5771cd2e0d0ac4b7b5c360c2c788454a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cd68334632c22e7ccada60a8da327b1e62e90dfce0ba210c86a799a1a9dd509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerRegistryTaskTimerTrigger]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerRegistryTaskTimerTrigger]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerRegistryTaskTimerTrigger]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b877e99506c1f92cdb9f2acfa0055ed86eedc723f65ed584a0fd5741717a445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerRegistryTaskTimerTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerRegistryTask.ContainerRegistryTaskTimerTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12e784db47dedcd40030824e28c33e78d72ebebcbc381ce391dcbdc4b3b1871f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3ba03e414b39ad216238c1e85871f18edba915e36ab4f45bd4cedf5fcbf83003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac46e2706b68ff63c1b7b3be033ba0f19fd23616a247046f387aec84c839f88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__725217c25fd9b8a4ffa85b99a087045df378f7c9c1c2191ab93c95100bdc1749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerRegistryTaskTimerTrigger]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerRegistryTaskTimerTrigger]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerRegistryTaskTimerTrigger]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__163b19b962c13f4711ee08787891ca0439f81a7cf472042c8c39c4fe1897b5a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ContainerRegistryTask",
    "ContainerRegistryTaskAgentSetting",
    "ContainerRegistryTaskAgentSettingOutputReference",
    "ContainerRegistryTaskBaseImageTrigger",
    "ContainerRegistryTaskBaseImageTriggerOutputReference",
    "ContainerRegistryTaskConfig",
    "ContainerRegistryTaskDockerStep",
    "ContainerRegistryTaskDockerStepOutputReference",
    "ContainerRegistryTaskEncodedStep",
    "ContainerRegistryTaskEncodedStepOutputReference",
    "ContainerRegistryTaskFileStep",
    "ContainerRegistryTaskFileStepOutputReference",
    "ContainerRegistryTaskIdentity",
    "ContainerRegistryTaskIdentityOutputReference",
    "ContainerRegistryTaskPlatform",
    "ContainerRegistryTaskPlatformOutputReference",
    "ContainerRegistryTaskRegistryCredential",
    "ContainerRegistryTaskRegistryCredentialCustom",
    "ContainerRegistryTaskRegistryCredentialCustomList",
    "ContainerRegistryTaskRegistryCredentialCustomOutputReference",
    "ContainerRegistryTaskRegistryCredentialOutputReference",
    "ContainerRegistryTaskRegistryCredentialSource",
    "ContainerRegistryTaskRegistryCredentialSourceOutputReference",
    "ContainerRegistryTaskSourceTrigger",
    "ContainerRegistryTaskSourceTriggerAuthentication",
    "ContainerRegistryTaskSourceTriggerAuthenticationOutputReference",
    "ContainerRegistryTaskSourceTriggerList",
    "ContainerRegistryTaskSourceTriggerOutputReference",
    "ContainerRegistryTaskTimeouts",
    "ContainerRegistryTaskTimeoutsOutputReference",
    "ContainerRegistryTaskTimerTrigger",
    "ContainerRegistryTaskTimerTriggerList",
    "ContainerRegistryTaskTimerTriggerOutputReference",
]

publication.publish()

def _typecheckingstub__84d76540b87bc714f3b57e5324d46904e3119e827985f1e092f095a1c71658db(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    container_registry_id: builtins.str,
    name: builtins.str,
    agent_pool_name: typing.Optional[builtins.str] = None,
    agent_setting: typing.Optional[typing.Union[ContainerRegistryTaskAgentSetting, typing.Dict[builtins.str, typing.Any]]] = None,
    base_image_trigger: typing.Optional[typing.Union[ContainerRegistryTaskBaseImageTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_step: typing.Optional[typing.Union[ContainerRegistryTaskDockerStep, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encoded_step: typing.Optional[typing.Union[ContainerRegistryTaskEncodedStep, typing.Dict[builtins.str, typing.Any]]] = None,
    file_step: typing.Optional[typing.Union[ContainerRegistryTaskFileStep, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[ContainerRegistryTaskIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    is_system_task: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_template: typing.Optional[builtins.str] = None,
    platform: typing.Optional[typing.Union[ContainerRegistryTaskPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
    registry_credential: typing.Optional[typing.Union[ContainerRegistryTaskRegistryCredential, typing.Dict[builtins.str, typing.Any]]] = None,
    source_trigger: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerRegistryTaskSourceTrigger, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ContainerRegistryTaskTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timer_trigger: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerRegistryTaskTimerTrigger, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__94e7fbd0331413dfa4163929492ecf41de3a150b3b22e6625bdb48c77b1bc189(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea8b459b4a5764bce27d98cacdb0704299abd483f78d2858410c82fe37e61e47(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerRegistryTaskSourceTrigger, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0b91e4178d9c89c316227302753803d7227d4185829c6eb2b32bf33a521d93(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerRegistryTaskTimerTrigger, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7796325ecea6d876e46236cb820724cc246555ba017ca07a8fe3e3c76e8ca9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8325729a2176a6ecbcb611a1122aa3b57339d7768af20cdb9a25bb45fecddb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054614a43ad0985d4f9b712a0dbe64c42659c3129f650d3b6746dce52c73cf72(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855d66dbcd027b4920d33c6c386a2e21ae1d5175af43ca419ba5d1a79fd2d8fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83dab352b2e7023d95bc6e2bf52b5d3be71332d5a4b325547286e3360e0ddbb9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92adfefce0fab929a09cb15ed5b93502699b84f8c314d27e3f751d33712c47a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9107a9cf2c535455eb30dc50562bb8e154902eae4c13be7f89e3377159a0cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__346253141edd3929bebbade889b1c432407d21d71b1bb86b253d1d2a500b5bdf(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203cfb5534e11ca1ae4b0ca2c58b014e21674975565c6225ecac98ddb3ace4e8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__343ece96c41e09b502d179fc6cb9a6abb17414a4dad50b3cfad01049c32fa9ff(
    *,
    cpu: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe6bb8979afd22abc815d39cae2f1b5872accecddf1d22528552936a7b71a14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c2f5db20de972eed4400b8143b5c82e345e568c91679ff14797e216fd502eba(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c700e84b87eb0daab8fc67b8583707e66cc29bd67d0a00fc23a8fb595b62a851(
    value: typing.Optional[ContainerRegistryTaskAgentSetting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941b5ab429c66cc7170d132ef15b827a0df8361d85527646bd5a7349f172fa77(
    *,
    name: builtins.str,
    type: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    update_trigger_endpoint: typing.Optional[builtins.str] = None,
    update_trigger_payload_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d663788770f465f2050b3d5c3955f3bd9335f452c4f765e9c4037bdc1b08394(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af52b25b6abde63b5682f41d45b4fdbbd529a7b45581b2005bf62554f6d1afce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9737e7c0f952e3daced42fb6b59be1deb07b8d2318b319e4d863073a3f02879f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e68758b65a358cc2dd3b6a7c04c9897ab8f3eb2f1632656507f7430e52c963(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2689ae29e4e774c5bb41825e6f1f794ce231ad7a52e43ee003658d43a0424a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b003e42c832c900eb2999652f7dd7c8888b487db94edcf75382a3742af8c862(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715f91d491c26800075275fc4b49d2c566410374f1756892772bd6f7ec3516ca(
    value: typing.Optional[ContainerRegistryTaskBaseImageTrigger],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9748c8b9d697cdf87d8e15e227dd5baffac2b3cc49949f9708cf9cf085b534(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    container_registry_id: builtins.str,
    name: builtins.str,
    agent_pool_name: typing.Optional[builtins.str] = None,
    agent_setting: typing.Optional[typing.Union[ContainerRegistryTaskAgentSetting, typing.Dict[builtins.str, typing.Any]]] = None,
    base_image_trigger: typing.Optional[typing.Union[ContainerRegistryTaskBaseImageTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_step: typing.Optional[typing.Union[ContainerRegistryTaskDockerStep, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encoded_step: typing.Optional[typing.Union[ContainerRegistryTaskEncodedStep, typing.Dict[builtins.str, typing.Any]]] = None,
    file_step: typing.Optional[typing.Union[ContainerRegistryTaskFileStep, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[ContainerRegistryTaskIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    is_system_task: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_template: typing.Optional[builtins.str] = None,
    platform: typing.Optional[typing.Union[ContainerRegistryTaskPlatform, typing.Dict[builtins.str, typing.Any]]] = None,
    registry_credential: typing.Optional[typing.Union[ContainerRegistryTaskRegistryCredential, typing.Dict[builtins.str, typing.Any]]] = None,
    source_trigger: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerRegistryTaskSourceTrigger, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ContainerRegistryTaskTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timer_trigger: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerRegistryTaskTimerTrigger, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a4cddb725f0ec00f75aa8ad68cd2a21e3c8c426e5aba67907ec3eb31b06c80(
    *,
    context_access_token: builtins.str,
    context_path: builtins.str,
    dockerfile_path: builtins.str,
    arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    image_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    push_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df1e3e4035aaa58865b1d322f11e79b620573de732ad7177d446c7d16c88c55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84dff7e27c0f9ab55771adf7fd42473f6a52078f66cc1f37e6cc10f5c175d7c0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d2b95c162e33dd51216857d0fd17b323cddf33be5cee0974a18a8a46cb3f34(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b63da8f22dd115d4ccfee84e911edad7471cc57c42ce2171b281392f585e129(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b97c3b8f02e042cc0baaf80a05e076b8d5b590e670cf7a600150a7b3e936916(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c34db1b3f87b5392bc5fc2c00a464c7a535a33996bf064d85cdf4d2118a83a1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819c5ff978e1c6c4689d22accd802aca839d4f5f4cbb769f199a4b7103512373(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eddd9c3dd0f702c2e56869ffb4b73dc09452ff042a703a9b5ba78cac94508fd1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c934edf8deeee60e4fdaa670b698d26b83ed3e762e928c3fb40352ab775f741(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81a42c5c01bea7e84cfe7ecb305944db2292ac4c5400a35291ba96c9247d8bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__473c8845743fca7d2e729594640055cfe30f933c8855937911deb291bfe85aba(
    value: typing.Optional[ContainerRegistryTaskDockerStep],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2d7c7b2a9deeb58a460b41eadc1bb8e5944b06aee0c85557cdde3d6b6c51e2(
    *,
    task_content: builtins.str,
    context_access_token: typing.Optional[builtins.str] = None,
    context_path: typing.Optional[builtins.str] = None,
    secret_values: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    value_content: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51fd0acda3101463afc04a7d0fa312cd40f2cb434f5fc5e9e9838df3f5d52028(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3af728da44b0831e9de0868d266e02658d3d679495695086f64c8ff3eb407bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b227dd435296b678e65bc438175e555a59b65f4a4f5f352b67cf344f19d9d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45f51271efa452d2fa138faabe827da3492e7d7d1d68717866721909242815c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__089e35cd520d02593fc2b6709efd9fbbd6a693d41c6e1683e5ddea3bd3de3ee7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2896eb28c0ac662110489142153526d187055c193ead6c202b694da5cc909386(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e784306dde41735d4bc8a1c29b5670e5abdcd6f44ac4adcfb5e00cfee1e2074b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d01825f6207bce3eb5b66e80c58e6e5908c94e10823a7863ae22f9f345450c6d(
    value: typing.Optional[ContainerRegistryTaskEncodedStep],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eeeaf8c0e78e74b0c2bc4afa4b08526974bab3d2a8d75f96617ca19e03be1c3(
    *,
    task_file_path: builtins.str,
    context_access_token: typing.Optional[builtins.str] = None,
    context_path: typing.Optional[builtins.str] = None,
    secret_values: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    value_file_path: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6157be53d0b513b57da7e783ecdb60e90e5225a38d63b5de4dc2a1d62c3d814(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb0dcd836a902545ee051ff09f866412fa01aa0ef7d25222efa3e3b0bd93f5dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3020e990fad310f79d4b085e3a995d2eddc55cf21265474fd74bda4aa69e42b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea7b67ff0a573cf969d933fc87a0d40614ca1f5600f1087ac1ed9b8d740ff12(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76f783ce7bd178532ebf2496b768ce7d4f8d6c2b025b571dbf0e4869fbd20aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d516a74883f19233cdecc8fcfe4835a261291f6cdb6ff7d1e4a40ad36f0d0c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ac71282db81fcedba408de1b835e116787be535f2ce9fb6f55de61caa311e6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ddd0fa7f037fd29d6e91cfd975346092b1932290c0525a597de7e42dc172508(
    value: typing.Optional[ContainerRegistryTaskFileStep],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8e5f6d04d631c02393ce2724036db15a37bd219baf1fc17e8d8a8eae7bb13e(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4378c811bfd0802cad7199ad07bf2b00251f4dc60e31436f2fd783a588f5e69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec69d2fa46af1af503bcde190a3d30663bec3c15379c11eb0c3bbccf8eaa535(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60a701c3cf4f3f85e5cc816b80f63f6f175846ffa24e5055feda4f1121463e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb0d76a9be638d198608853b55903481271320a8bd24aec4b6b2cfdbd9120e7(
    value: typing.Optional[ContainerRegistryTaskIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c88ff75fb6e805833fce44040ab0ac810672d9031ae20ed06773c9538b44519(
    *,
    os: builtins.str,
    architecture: typing.Optional[builtins.str] = None,
    variant: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b414f46314d9f03ce75a09a854aa488c09fbdf88b192150924ebd0da688f04df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9d7e9c6ec684ad163368250964b8246f8a2b674d945699940385b231b4420bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34816951c09d3cc3d5976c8b4dabe72d366736c760d136b37bb81f2b2f71bdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b3dce7c5597a1176e1025b5ef7d5c57b3728a8158aefd9498be91be8e1a8ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64211bad1b363371798af08f46183d04709afccfa7b33b6f5fa67baa844af05b(
    value: typing.Optional[ContainerRegistryTaskPlatform],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4199a3d1a43bf503481270d4db4901809e6134d3b75bb772314b8674880fb4e(
    *,
    custom: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerRegistryTaskRegistryCredentialCustom, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source: typing.Optional[typing.Union[ContainerRegistryTaskRegistryCredentialSource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__974ab38de78f589875ef1aff9507b870958437372140761f797166246588f461(
    *,
    login_server: builtins.str,
    identity: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__071d2c60e9655d03f2f1f118bf2a3aa482a7b6977feca52a5eec8d52fcbe3073(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edfdb943dad8af20c2ba990e5603bae1e17e8fa49e2500751e4d8ac9bd30ca7a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8582dd94b6f4b8fb2b70302faefd926516b19d52e40f9757b9b10f2a77293f2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__111f1de7c07ded26abcfb74383670c4fb05847ed1a748f73173fb3e247406f12(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2ca799343fb752ba234d200bb00b10f2e76792578492013166af607b9f0dcd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d563b349548c26f7c1a915ba7e589d67407d03979365d3418b8b4ebb52fd410(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerRegistryTaskRegistryCredentialCustom]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8122b6ff42c14471ceda741d3a840632536985886d8dfa2aa4ff2082c119f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee634af9087e37aa172cab04ef19e5f16229d9cb4ea310168b737a5c83e6002b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e7cc69eeb80d8097af695a1bce71280fbf8e0b32531442d1579cf91f41d2a52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f04283c7d89d6f713c0578346bf13d3b0e6a4f3874fb83d02ac5e2c1e2d8493d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c3d896d4a19aa8d13db3004d0a2946ed5f6246f0ef2b1cb620622ca0f19ee0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c53f103e2a6e1af9c7603a9ad4cbbe948fe9d5feb0d452ac909ba0983660447(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerRegistryTaskRegistryCredentialCustom]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b97b9f1649574a6dd3fd0a06abfd06b01c0a4acca86fb08a82c9bf76610309(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__527d496ce09b8871d45a9b0b8610dcfa8122c872c130a471ab5d6283906265a3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerRegistryTaskRegistryCredentialCustom, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b89b22f147aef23f77e0be811e0be0450207aa361b36ec22dc0d170e14fa189(
    value: typing.Optional[ContainerRegistryTaskRegistryCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__249aa9db1270b19364f7a1f0897ce303d30a0b2be875511d79608cc795bec4fb(
    *,
    login_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e679989f4bd5ac8e045c014ac35223cf08f75a77edf2ec9e0fd119f11f960573(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9367f25ec2c819a66c91b17bc80b89ab4da9e56f72cc564adb61e814f9b05c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3feaf5e82bad79f43b3121344a4985dff6f39358ae70d8c14d5ad4e5ee4e30f2(
    value: typing.Optional[ContainerRegistryTaskRegistryCredentialSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c50750f641cf5f1707c39d05c7201d6a1265ece2a3fbe644305b4a3df3da1b(
    *,
    events: typing.Sequence[builtins.str],
    name: builtins.str,
    repository_url: builtins.str,
    source_type: builtins.str,
    authentication: typing.Optional[typing.Union[ContainerRegistryTaskSourceTriggerAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    branch: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471438e7c0d9a6eaeefc117fd4b1735fb94e95e1305d61a29734c0af18810fe7(
    *,
    token: builtins.str,
    token_type: builtins.str,
    expire_in_seconds: typing.Optional[jsii.Number] = None,
    refresh_token: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f35309efc00a538b9acfef31ee80671e326c956c7e2b598f2a6629b1faf8cb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a090d00486caa193e77df16593efd1711d6044e1e1dfe857e2676896c1ff74c8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc192c62d32e381784dae9779c2e33964cf03a8f6691802f960d0e714b3c926(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbeebf8ee27a8f7fdb6926607a203542bfafe95f6c96ffb58ea84a19306d6a5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__446ba9207681702f407ee600f8e5b9f57e105953179ce88e63c429a36598d7d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b36ab9617a27a2d7bca6c77d6715131642894869af9d2b64c5a36e37253dc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e540df209ba9796a14a67fea6763557be144c724a6155f006f8796327179a614(
    value: typing.Optional[ContainerRegistryTaskSourceTriggerAuthentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f6b45dc8d2c98e0e4c4abe0e7978ff91a7acfe30b27c75326b37f59423d860(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc179f9b2df68cf01a50c314cdbfc0839c1caea601ded42e3ada51a0da356720(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d882367fa1e68468932787b95242e43a3fff3d415500273a9a969d280bd44771(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__106094454b24032a7b002b0900b9bbcd684820e1b75bbbf2a66181468e8bbf4a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714d1a76638ad171caa797fea2b2bb4adf4f89ea29efe7f991359c9d47424ed3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6df29cd9f5050dc137f6299b1f88f404cf566edffc626cc561c63e7ddb98a77(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerRegistryTaskSourceTrigger]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b069cc2e017c0d606c968e49fe1cd692c348be2ac76d5a5e90d92a019ccf62c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162190f24654e228478ede05e8583e67815ac2d5a25d2a73190225bcade60352(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959792a3ac66ab30433265f95aa2e2668fe5d251c5e0b22ac1904e2c24b79c72(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b22ee9cbd8ea2fbff51d1da0cf1e118f8fd2533279c1e9fc4c0d8560ec5a454(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9153fe786c45727daad85d9b1a0ffd2db907a46b1d8cba4fab8098ef03e1815e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa819440066bb50037a5e92c582baa9c337f045066f61ee8a76a98bdffa17060(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3298490db82c1ee9952cbc34f5dca0de7c230bf0f2cd807ccfe3d410d68e426(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395df2a701641c44ff2fd2768ab127ee2ef501a61e1d330a1b9ba80d6cb00387(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerRegistryTaskSourceTrigger]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e09c783492b92e9f08b507088a77305fe9c4037041ce9edf75ba97f15fa61d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2c16b81de0cfbf6c1d524037d5117763289a65c2bb44a9c0476bf93d229ce8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5ea8d79d67bd948157bc3acfa3784f1d7ac0e796c045f53df266bfc0f1e56c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55696c6450359cef594f7392efe2024e975344201470c9387ef1e4c03895417(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2e2276dbe4505d3fecd2245284174a371fcaaabcd08165ae0b640d55074728(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319d60199186d288908b6ab1a0111128044c3a59c31991ea196217cd74df3236(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__086ab23f9aeda6c09184e2ddfc68cf7f167cbeb893b53624513dcf3e2dc28b77(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerRegistryTaskTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f9a39d9724c218aca9bb27e99dc12cb133b1e5ae7c3e9c15492ecbad92c171e(
    *,
    name: builtins.str,
    schedule: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39260486a8eb0466912c365def55fd797b3f06ea5dda201c8a8f7e03777b350(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4339c49c9e0db6be12f6f7ae85dd6b89f368fe24891b6f77344874479500caed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c51557bfe75ffd76ebdebf8207dfc1e92a29d63236bfc8880b23efd2b1a39de2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd2bf586eeff749adc68606cdd65cc5771cd2e0d0ac4b7b5c360c2c788454a0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd68334632c22e7ccada60a8da327b1e62e90dfce0ba210c86a799a1a9dd509(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b877e99506c1f92cdb9f2acfa0055ed86eedc723f65ed584a0fd5741717a445(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerRegistryTaskTimerTrigger]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e784db47dedcd40030824e28c33e78d72ebebcbc381ce391dcbdc4b3b1871f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba03e414b39ad216238c1e85871f18edba915e36ab4f45bd4cedf5fcbf83003(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac46e2706b68ff63c1b7b3be033ba0f19fd23616a247046f387aec84c839f88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725217c25fd9b8a4ffa85b99a087045df378f7c9c1c2191ab93c95100bdc1749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__163b19b962c13f4711ee08787891ca0439f81a7cf472042c8c39c4fe1897b5a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerRegistryTaskTimerTrigger]],
) -> None:
    """Type checking stubs"""
    pass

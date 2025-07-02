r'''
# `azurerm_logic_app_workflow`

Refer to the Terraform Registry for docs: [`azurerm_logic_app_workflow`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow).
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


class LogicAppWorkflow(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflow",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow azurerm_logic_app_workflow}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        access_control: typing.Optional[typing.Union["LogicAppWorkflowAccessControl", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["LogicAppWorkflowIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        integration_service_environment_id: typing.Optional[builtins.str] = None,
        logic_app_integration_account_id: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LogicAppWorkflowTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workflow_schema: typing.Optional[builtins.str] = None,
        workflow_version: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow azurerm_logic_app_workflow} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#location LogicAppWorkflow#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#name LogicAppWorkflow#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#resource_group_name LogicAppWorkflow#resource_group_name}.
        :param access_control: access_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#access_control LogicAppWorkflow#access_control}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#enabled LogicAppWorkflow#enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#id LogicAppWorkflow#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#identity LogicAppWorkflow#identity}
        :param integration_service_environment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#integration_service_environment_id LogicAppWorkflow#integration_service_environment_id}.
        :param logic_app_integration_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#logic_app_integration_account_id LogicAppWorkflow#logic_app_integration_account_id}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#parameters LogicAppWorkflow#parameters}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#tags LogicAppWorkflow#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#timeouts LogicAppWorkflow#timeouts}
        :param workflow_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#workflow_parameters LogicAppWorkflow#workflow_parameters}.
        :param workflow_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#workflow_schema LogicAppWorkflow#workflow_schema}.
        :param workflow_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#workflow_version LogicAppWorkflow#workflow_version}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dc380563e6ea1e41143d97d08ca58823a8e2fb379ce21a9ba525613ba11b0ee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LogicAppWorkflowConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            access_control=access_control,
            enabled=enabled,
            id=id,
            identity=identity,
            integration_service_environment_id=integration_service_environment_id,
            logic_app_integration_account_id=logic_app_integration_account_id,
            parameters=parameters,
            tags=tags,
            timeouts=timeouts,
            workflow_parameters=workflow_parameters,
            workflow_schema=workflow_schema,
            workflow_version=workflow_version,
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
        '''Generates CDKTF code for importing a LogicAppWorkflow resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LogicAppWorkflow to import.
        :param import_from_id: The id of the existing LogicAppWorkflow that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LogicAppWorkflow to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ab6bea0d3746dc378ecac710a568098e5b9ac15ef2e2b360c777be81ba3732c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccessControl")
    def put_access_control(
        self,
        *,
        action: typing.Optional[typing.Union["LogicAppWorkflowAccessControlAction", typing.Dict[builtins.str, typing.Any]]] = None,
        content: typing.Optional[typing.Union["LogicAppWorkflowAccessControlContent", typing.Dict[builtins.str, typing.Any]]] = None,
        trigger: typing.Optional[typing.Union["LogicAppWorkflowAccessControlTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_management: typing.Optional[typing.Union["LogicAppWorkflowAccessControlWorkflowManagement", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#action LogicAppWorkflow#action}
        :param content: content block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#content LogicAppWorkflow#content}
        :param trigger: trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#trigger LogicAppWorkflow#trigger}
        :param workflow_management: workflow_management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#workflow_management LogicAppWorkflow#workflow_management}
        '''
        value = LogicAppWorkflowAccessControl(
            action=action,
            content=content,
            trigger=trigger,
            workflow_management=workflow_management,
        )

        return typing.cast(None, jsii.invoke(self, "putAccessControl", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#type LogicAppWorkflow#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#identity_ids LogicAppWorkflow#identity_ids}.
        '''
        value = LogicAppWorkflowIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#create LogicAppWorkflow#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#delete LogicAppWorkflow#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#read LogicAppWorkflow#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#update LogicAppWorkflow#update}.
        '''
        value = LogicAppWorkflowTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccessControl")
    def reset_access_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessControl", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetIntegrationServiceEnvironmentId")
    def reset_integration_service_environment_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegrationServiceEnvironmentId", []))

    @jsii.member(jsii_name="resetLogicAppIntegrationAccountId")
    def reset_logic_app_integration_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogicAppIntegrationAccountId", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWorkflowParameters")
    def reset_workflow_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkflowParameters", []))

    @jsii.member(jsii_name="resetWorkflowSchema")
    def reset_workflow_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkflowSchema", []))

    @jsii.member(jsii_name="resetWorkflowVersion")
    def reset_workflow_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkflowVersion", []))

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
    @jsii.member(jsii_name="accessControl")
    def access_control(self) -> "LogicAppWorkflowAccessControlOutputReference":
        return typing.cast("LogicAppWorkflowAccessControlOutputReference", jsii.get(self, "accessControl"))

    @builtins.property
    @jsii.member(jsii_name="accessEndpoint")
    def access_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="connectorEndpointIpAddresses")
    def connector_endpoint_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "connectorEndpointIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="connectorOutboundIpAddresses")
    def connector_outbound_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "connectorOutboundIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "LogicAppWorkflowIdentityOutputReference":
        return typing.cast("LogicAppWorkflowIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "LogicAppWorkflowTimeoutsOutputReference":
        return typing.cast("LogicAppWorkflowTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="workflowEndpointIpAddresses")
    def workflow_endpoint_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "workflowEndpointIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="workflowOutboundIpAddresses")
    def workflow_outbound_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "workflowOutboundIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="accessControlInput")
    def access_control_input(self) -> typing.Optional["LogicAppWorkflowAccessControl"]:
        return typing.cast(typing.Optional["LogicAppWorkflowAccessControl"], jsii.get(self, "accessControlInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["LogicAppWorkflowIdentity"]:
        return typing.cast(typing.Optional["LogicAppWorkflowIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationServiceEnvironmentIdInput")
    def integration_service_environment_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationServiceEnvironmentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="logicAppIntegrationAccountIdInput")
    def logic_app_integration_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logicAppIntegrationAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LogicAppWorkflowTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LogicAppWorkflowTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workflowParametersInput")
    def workflow_parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "workflowParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="workflowSchemaInput")
    def workflow_schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workflowSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="workflowVersionInput")
    def workflow_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workflowVersionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a450fcd97b3938b722b53daf79725b8ebd4aaea08b51fc582c8f385db4f83b8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73d16110d759c9e240dd6a4bef3bbc174f45aac236c472a23d53816e989ef0f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrationServiceEnvironmentId")
    def integration_service_environment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrationServiceEnvironmentId"))

    @integration_service_environment_id.setter
    def integration_service_environment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f08ce6f971a908db6b90d8b7cad0419e3661d6f35f26b3e81d5dcbe80e3defc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationServiceEnvironmentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d85d7c44b8759ed779ffc61c2ca7affbd7899d80139d7f4eaee52397c509f80d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logicAppIntegrationAccountId")
    def logic_app_integration_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logicAppIntegrationAccountId"))

    @logic_app_integration_account_id.setter
    def logic_app_integration_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed7dadc16ba9b378f95a4049c1054fc39619c47e1ebe787e9539615e6362b5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logicAppIntegrationAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a610e853b810d1ff95264ec00240e04915cc33a6126b77ee2ecb65c6d642dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3326b6a7e8edf66fcf88c325cc316af7d26023a44d465d091879c8b1d0d054)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29cd47d5bfa3e330a2e4582e105800604211bf2f3eef26376e28794b4111d966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d92b87a57d02ccdde8c662c1fc8f0221b14b1a49d91b07bf11d780e9b06601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workflowParameters")
    def workflow_parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "workflowParameters"))

    @workflow_parameters.setter
    def workflow_parameters(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7f0fa7d9b3173f2afcddb4986a54c229dfdb05722168246c2e4664bb6199013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workflowParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workflowSchema")
    def workflow_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workflowSchema"))

    @workflow_schema.setter
    def workflow_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb3b0b86a6bb4c17c65077862aed92015bd695636d531f73c6596e13812cb29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workflowSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workflowVersion")
    def workflow_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workflowVersion"))

    @workflow_version.setter
    def workflow_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4372881c391fcc9107ac1ae6fe7f6590f6f0da3fc16a85c333348780e071cdf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workflowVersion", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowAccessControl",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "content": "content",
        "trigger": "trigger",
        "workflow_management": "workflowManagement",
    },
)
class LogicAppWorkflowAccessControl:
    def __init__(
        self,
        *,
        action: typing.Optional[typing.Union["LogicAppWorkflowAccessControlAction", typing.Dict[builtins.str, typing.Any]]] = None,
        content: typing.Optional[typing.Union["LogicAppWorkflowAccessControlContent", typing.Dict[builtins.str, typing.Any]]] = None,
        trigger: typing.Optional[typing.Union["LogicAppWorkflowAccessControlTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_management: typing.Optional[typing.Union["LogicAppWorkflowAccessControlWorkflowManagement", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#action LogicAppWorkflow#action}
        :param content: content block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#content LogicAppWorkflow#content}
        :param trigger: trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#trigger LogicAppWorkflow#trigger}
        :param workflow_management: workflow_management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#workflow_management LogicAppWorkflow#workflow_management}
        '''
        if isinstance(action, dict):
            action = LogicAppWorkflowAccessControlAction(**action)
        if isinstance(content, dict):
            content = LogicAppWorkflowAccessControlContent(**content)
        if isinstance(trigger, dict):
            trigger = LogicAppWorkflowAccessControlTrigger(**trigger)
        if isinstance(workflow_management, dict):
            workflow_management = LogicAppWorkflowAccessControlWorkflowManagement(**workflow_management)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e2d9d8bbf388487048fd529e7ee5df1ac225e95f5a6b31fec4d65c960e54b91)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
            check_type(argname="argument workflow_management", value=workflow_management, expected_type=type_hints["workflow_management"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if content is not None:
            self._values["content"] = content
        if trigger is not None:
            self._values["trigger"] = trigger
        if workflow_management is not None:
            self._values["workflow_management"] = workflow_management

    @builtins.property
    def action(self) -> typing.Optional["LogicAppWorkflowAccessControlAction"]:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#action LogicAppWorkflow#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional["LogicAppWorkflowAccessControlAction"], result)

    @builtins.property
    def content(self) -> typing.Optional["LogicAppWorkflowAccessControlContent"]:
        '''content block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#content LogicAppWorkflow#content}
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional["LogicAppWorkflowAccessControlContent"], result)

    @builtins.property
    def trigger(self) -> typing.Optional["LogicAppWorkflowAccessControlTrigger"]:
        '''trigger block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#trigger LogicAppWorkflow#trigger}
        '''
        result = self._values.get("trigger")
        return typing.cast(typing.Optional["LogicAppWorkflowAccessControlTrigger"], result)

    @builtins.property
    def workflow_management(
        self,
    ) -> typing.Optional["LogicAppWorkflowAccessControlWorkflowManagement"]:
        '''workflow_management block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#workflow_management LogicAppWorkflow#workflow_management}
        '''
        result = self._values.get("workflow_management")
        return typing.cast(typing.Optional["LogicAppWorkflowAccessControlWorkflowManagement"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogicAppWorkflowAccessControl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowAccessControlAction",
    jsii_struct_bases=[],
    name_mapping={"allowed_caller_ip_address_range": "allowedCallerIpAddressRange"},
)
class LogicAppWorkflowAccessControlAction:
    def __init__(
        self,
        *,
        allowed_caller_ip_address_range: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param allowed_caller_ip_address_range: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#allowed_caller_ip_address_range LogicAppWorkflow#allowed_caller_ip_address_range}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8eda4ffeb5f01fc0deece537ea93211d39448fa8e93c2e1dc9c6cf17fb7a661)
            check_type(argname="argument allowed_caller_ip_address_range", value=allowed_caller_ip_address_range, expected_type=type_hints["allowed_caller_ip_address_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_caller_ip_address_range": allowed_caller_ip_address_range,
        }

    @builtins.property
    def allowed_caller_ip_address_range(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#allowed_caller_ip_address_range LogicAppWorkflow#allowed_caller_ip_address_range}.'''
        result = self._values.get("allowed_caller_ip_address_range")
        assert result is not None, "Required property 'allowed_caller_ip_address_range' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogicAppWorkflowAccessControlAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogicAppWorkflowAccessControlActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowAccessControlActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b910c72ea31bb3750e55c4c1315a0add10240e03ba6b0f293c50a35e19c4c34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="allowedCallerIpAddressRangeInput")
    def allowed_caller_ip_address_range_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedCallerIpAddressRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedCallerIpAddressRange")
    def allowed_caller_ip_address_range(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedCallerIpAddressRange"))

    @allowed_caller_ip_address_range.setter
    def allowed_caller_ip_address_range(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10644879fd23cafca953b83d19c1ba17c1b07bee18247d645cb5e3c1dd92828a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedCallerIpAddressRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogicAppWorkflowAccessControlAction]:
        return typing.cast(typing.Optional[LogicAppWorkflowAccessControlAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogicAppWorkflowAccessControlAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97ef76191f5e0bee75f8e3801ace24828bfe15c773e3687917132ede543fd58b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowAccessControlContent",
    jsii_struct_bases=[],
    name_mapping={"allowed_caller_ip_address_range": "allowedCallerIpAddressRange"},
)
class LogicAppWorkflowAccessControlContent:
    def __init__(
        self,
        *,
        allowed_caller_ip_address_range: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param allowed_caller_ip_address_range: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#allowed_caller_ip_address_range LogicAppWorkflow#allowed_caller_ip_address_range}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e02b45811689d38931e067684de95826aae3870d43cf10958071530322e0f62a)
            check_type(argname="argument allowed_caller_ip_address_range", value=allowed_caller_ip_address_range, expected_type=type_hints["allowed_caller_ip_address_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_caller_ip_address_range": allowed_caller_ip_address_range,
        }

    @builtins.property
    def allowed_caller_ip_address_range(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#allowed_caller_ip_address_range LogicAppWorkflow#allowed_caller_ip_address_range}.'''
        result = self._values.get("allowed_caller_ip_address_range")
        assert result is not None, "Required property 'allowed_caller_ip_address_range' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogicAppWorkflowAccessControlContent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogicAppWorkflowAccessControlContentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowAccessControlContentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77c5205dc16033fc890b0d753e7a2de274081709d0fee857bc986a1dbb919dd6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="allowedCallerIpAddressRangeInput")
    def allowed_caller_ip_address_range_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedCallerIpAddressRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedCallerIpAddressRange")
    def allowed_caller_ip_address_range(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedCallerIpAddressRange"))

    @allowed_caller_ip_address_range.setter
    def allowed_caller_ip_address_range(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b36499b513161c76f32ba1be720dd57c1e9ce279455b8c5e3fc63ddbaf47f654)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedCallerIpAddressRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogicAppWorkflowAccessControlContent]:
        return typing.cast(typing.Optional[LogicAppWorkflowAccessControlContent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogicAppWorkflowAccessControlContent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5444f63737c2f6a630bca2992093454ba8bbf4895ae35a0311959a511352e6f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogicAppWorkflowAccessControlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowAccessControlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__821c5acfc5f234331932557f51b3e474f1dda09a4e1a017de974f7086204ea48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        allowed_caller_ip_address_range: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param allowed_caller_ip_address_range: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#allowed_caller_ip_address_range LogicAppWorkflow#allowed_caller_ip_address_range}.
        '''
        value = LogicAppWorkflowAccessControlAction(
            allowed_caller_ip_address_range=allowed_caller_ip_address_range
        )

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putContent")
    def put_content(
        self,
        *,
        allowed_caller_ip_address_range: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param allowed_caller_ip_address_range: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#allowed_caller_ip_address_range LogicAppWorkflow#allowed_caller_ip_address_range}.
        '''
        value = LogicAppWorkflowAccessControlContent(
            allowed_caller_ip_address_range=allowed_caller_ip_address_range
        )

        return typing.cast(None, jsii.invoke(self, "putContent", [value]))

    @jsii.member(jsii_name="putTrigger")
    def put_trigger(
        self,
        *,
        allowed_caller_ip_address_range: typing.Sequence[builtins.str],
        open_authentication_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed_caller_ip_address_range: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#allowed_caller_ip_address_range LogicAppWorkflow#allowed_caller_ip_address_range}.
        :param open_authentication_policy: open_authentication_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#open_authentication_policy LogicAppWorkflow#open_authentication_policy}
        '''
        value = LogicAppWorkflowAccessControlTrigger(
            allowed_caller_ip_address_range=allowed_caller_ip_address_range,
            open_authentication_policy=open_authentication_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putTrigger", [value]))

    @jsii.member(jsii_name="putWorkflowManagement")
    def put_workflow_management(
        self,
        *,
        allowed_caller_ip_address_range: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param allowed_caller_ip_address_range: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#allowed_caller_ip_address_range LogicAppWorkflow#allowed_caller_ip_address_range}.
        '''
        value = LogicAppWorkflowAccessControlWorkflowManagement(
            allowed_caller_ip_address_range=allowed_caller_ip_address_range
        )

        return typing.cast(None, jsii.invoke(self, "putWorkflowManagement", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetContent")
    def reset_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContent", []))

    @jsii.member(jsii_name="resetTrigger")
    def reset_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrigger", []))

    @jsii.member(jsii_name="resetWorkflowManagement")
    def reset_workflow_management(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkflowManagement", []))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> LogicAppWorkflowAccessControlActionOutputReference:
        return typing.cast(LogicAppWorkflowAccessControlActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> LogicAppWorkflowAccessControlContentOutputReference:
        return typing.cast(LogicAppWorkflowAccessControlContentOutputReference, jsii.get(self, "content"))

    @builtins.property
    @jsii.member(jsii_name="trigger")
    def trigger(self) -> "LogicAppWorkflowAccessControlTriggerOutputReference":
        return typing.cast("LogicAppWorkflowAccessControlTriggerOutputReference", jsii.get(self, "trigger"))

    @builtins.property
    @jsii.member(jsii_name="workflowManagement")
    def workflow_management(
        self,
    ) -> "LogicAppWorkflowAccessControlWorkflowManagementOutputReference":
        return typing.cast("LogicAppWorkflowAccessControlWorkflowManagementOutputReference", jsii.get(self, "workflowManagement"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[LogicAppWorkflowAccessControlAction]:
        return typing.cast(typing.Optional[LogicAppWorkflowAccessControlAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[LogicAppWorkflowAccessControlContent]:
        return typing.cast(typing.Optional[LogicAppWorkflowAccessControlContent], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerInput")
    def trigger_input(self) -> typing.Optional["LogicAppWorkflowAccessControlTrigger"]:
        return typing.cast(typing.Optional["LogicAppWorkflowAccessControlTrigger"], jsii.get(self, "triggerInput"))

    @builtins.property
    @jsii.member(jsii_name="workflowManagementInput")
    def workflow_management_input(
        self,
    ) -> typing.Optional["LogicAppWorkflowAccessControlWorkflowManagement"]:
        return typing.cast(typing.Optional["LogicAppWorkflowAccessControlWorkflowManagement"], jsii.get(self, "workflowManagementInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogicAppWorkflowAccessControl]:
        return typing.cast(typing.Optional[LogicAppWorkflowAccessControl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogicAppWorkflowAccessControl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__994137f109684171dd01c2bd5067c8a5323ccb73d9ca53c2645457ffd608a6b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowAccessControlTrigger",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_caller_ip_address_range": "allowedCallerIpAddressRange",
        "open_authentication_policy": "openAuthenticationPolicy",
    },
)
class LogicAppWorkflowAccessControlTrigger:
    def __init__(
        self,
        *,
        allowed_caller_ip_address_range: typing.Sequence[builtins.str],
        open_authentication_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed_caller_ip_address_range: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#allowed_caller_ip_address_range LogicAppWorkflow#allowed_caller_ip_address_range}.
        :param open_authentication_policy: open_authentication_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#open_authentication_policy LogicAppWorkflow#open_authentication_policy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26b62439484ae56ee9642e1da862639a66b1938c911e39fceced61be86c20be2)
            check_type(argname="argument allowed_caller_ip_address_range", value=allowed_caller_ip_address_range, expected_type=type_hints["allowed_caller_ip_address_range"])
            check_type(argname="argument open_authentication_policy", value=open_authentication_policy, expected_type=type_hints["open_authentication_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_caller_ip_address_range": allowed_caller_ip_address_range,
        }
        if open_authentication_policy is not None:
            self._values["open_authentication_policy"] = open_authentication_policy

    @builtins.property
    def allowed_caller_ip_address_range(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#allowed_caller_ip_address_range LogicAppWorkflow#allowed_caller_ip_address_range}.'''
        result = self._values.get("allowed_caller_ip_address_range")
        assert result is not None, "Required property 'allowed_caller_ip_address_range' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def open_authentication_policy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy"]]]:
        '''open_authentication_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#open_authentication_policy LogicAppWorkflow#open_authentication_policy}
        '''
        result = self._values.get("open_authentication_policy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogicAppWorkflowAccessControlTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy",
    jsii_struct_bases=[],
    name_mapping={"claim": "claim", "name": "name"},
)
class LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy:
    def __init__(
        self,
        *,
        claim: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
    ) -> None:
        '''
        :param claim: claim block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#claim LogicAppWorkflow#claim}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#name LogicAppWorkflow#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7440e5f5e7f973c5d69c18b5f914d216d577d1c53132a8487f52aa6aa807cd90)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "claim": claim,
            "name": name,
        }

    @builtins.property
    def claim(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim"]]:
        '''claim block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#claim LogicAppWorkflow#claim}
        '''
        result = self._values.get("claim")
        assert result is not None, "Required property 'claim' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#name LogicAppWorkflow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#name LogicAppWorkflow#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#value LogicAppWorkflow#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__678df7d21176484c18601ad7aa1e1928c1ed059e5d4ed02485f98c9d36178fa0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#name LogicAppWorkflow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#value LogicAppWorkflow#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaimList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaimList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__549933df89ae2cebaa10d4ec48f9c793f27e70f192c0ba4f97c232d9996c2ab3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaimOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2505357d9c2e575826e6c5202848d1140fdfa7f9873b145f472b3e8aa1d6551c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaimOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ba8f1e9f01c3542224f5012bbc6c91f22ff8d5738f494662d2707c6239bc0bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3e4e3c9a3d0987b29427ca16a840e68a591239e493ce5f97d249d962d47be48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e60f0665466d0fec5aac13577432b19adf6b859c4524e1205af72a85833d1c40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac1d3f39ec34e32ea1e906117d9459ff4dcc63da71a9ff70c049d12d965ae4fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaimOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaimOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e68fbe87dc637fa59d588e41cf96507fd7389b12812f1eb3471c54a06bdc5d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4378ab1d9c385b93fef83e0dc0d9408ee24410649202364ce49ab8ceac54c5c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f39402c46af45989a1a1baf7493002ce213c11f59adf1bd681ffee3b9f67b251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d14cbff393359460172789b70c1f33a039f753fe83f765c23897b865c54bfc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52ad19f98481d80269d9902d7aa20f4c6c1205691fc100b5a7ceb282f15d7cfe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__526f0ae72392b5ce4a223bfd208df8e64d8343d463746e5d1764284d12dc818c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__665dbcbd34367fccc1624d008b1b14dd2927f0963646f09545d53c08c8eaae24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6550a82b3aef5539ec414e519fa5da1a799e0d375c4434755e06ee21c7a7f08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b622ad0691bae5304e0fa75fe6e44e9924f374d97ac3060e4f72db406a95b9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__372fe3b97ef867382468c8dd005c546b7bea057c13035bafdaedebbaac5dba79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a61140c31577a79e8ccd2be824beccb077823512128ab153bc66aabbadc1a45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putClaim")
    def put_claim(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04134c77f5c1747b84438636379c0ac457b9b2b1ee14e108f173b1981047a998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putClaim", [value]))

    @builtins.property
    @jsii.member(jsii_name="claim")
    def claim(
        self,
    ) -> LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaimList:
        return typing.cast(LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaimList, jsii.get(self, "claim"))

    @builtins.property
    @jsii.member(jsii_name="claimInput")
    def claim_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim]]], jsii.get(self, "claimInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5339d0d3c0abc788eafa175af02abfcdad033a75e8c9ede003d2737f933dd1fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bc774e2dcd28efca1c648ae182c49ffa0b20e1d5671fcb8cc532a94807da497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogicAppWorkflowAccessControlTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowAccessControlTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f75ba074641b0583fe646c1247c17b0f7607a34aeec1895588c763e67f07d5b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOpenAuthenticationPolicy")
    def put_open_authentication_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c84e3a6059a695f07862520d1c781f4e7ad2d234657816521309cf9e022ec10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOpenAuthenticationPolicy", [value]))

    @jsii.member(jsii_name="resetOpenAuthenticationPolicy")
    def reset_open_authentication_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOpenAuthenticationPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="openAuthenticationPolicy")
    def open_authentication_policy(
        self,
    ) -> LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyList:
        return typing.cast(LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyList, jsii.get(self, "openAuthenticationPolicy"))

    @builtins.property
    @jsii.member(jsii_name="allowedCallerIpAddressRangeInput")
    def allowed_caller_ip_address_range_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedCallerIpAddressRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="openAuthenticationPolicyInput")
    def open_authentication_policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy]]], jsii.get(self, "openAuthenticationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedCallerIpAddressRange")
    def allowed_caller_ip_address_range(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedCallerIpAddressRange"))

    @allowed_caller_ip_address_range.setter
    def allowed_caller_ip_address_range(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19956d89ea65517ea1493e8343e07e1d06224aede9c5a4f61059a1647bfabded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedCallerIpAddressRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogicAppWorkflowAccessControlTrigger]:
        return typing.cast(typing.Optional[LogicAppWorkflowAccessControlTrigger], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogicAppWorkflowAccessControlTrigger],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6b8a934aa0fe154cef3b751d38fd22f96482c97bd48c7a0b4af87498404bc05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowAccessControlWorkflowManagement",
    jsii_struct_bases=[],
    name_mapping={"allowed_caller_ip_address_range": "allowedCallerIpAddressRange"},
)
class LogicAppWorkflowAccessControlWorkflowManagement:
    def __init__(
        self,
        *,
        allowed_caller_ip_address_range: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param allowed_caller_ip_address_range: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#allowed_caller_ip_address_range LogicAppWorkflow#allowed_caller_ip_address_range}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2138f4326c090bd4c63b1fbce5700ded552aabaa920a15c1eadb22a40879a3ab)
            check_type(argname="argument allowed_caller_ip_address_range", value=allowed_caller_ip_address_range, expected_type=type_hints["allowed_caller_ip_address_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_caller_ip_address_range": allowed_caller_ip_address_range,
        }

    @builtins.property
    def allowed_caller_ip_address_range(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#allowed_caller_ip_address_range LogicAppWorkflow#allowed_caller_ip_address_range}.'''
        result = self._values.get("allowed_caller_ip_address_range")
        assert result is not None, "Required property 'allowed_caller_ip_address_range' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogicAppWorkflowAccessControlWorkflowManagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogicAppWorkflowAccessControlWorkflowManagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowAccessControlWorkflowManagementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9224c3c5cf38949b29ee6c3c3d9916a30e63900cd2d9c40a861341c3541c2d64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="allowedCallerIpAddressRangeInput")
    def allowed_caller_ip_address_range_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedCallerIpAddressRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedCallerIpAddressRange")
    def allowed_caller_ip_address_range(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedCallerIpAddressRange"))

    @allowed_caller_ip_address_range.setter
    def allowed_caller_ip_address_range(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0a0c0a0e667461c28f354fb0c65fe7fe09fafb8547d5e3ff2528b8fce6a8fd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedCallerIpAddressRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogicAppWorkflowAccessControlWorkflowManagement]:
        return typing.cast(typing.Optional[LogicAppWorkflowAccessControlWorkflowManagement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogicAppWorkflowAccessControlWorkflowManagement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fccd1fadff67607beb3092e4f4562f51b1861a52327a381cc3ef69ef876bb589)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "access_control": "accessControl",
        "enabled": "enabled",
        "id": "id",
        "identity": "identity",
        "integration_service_environment_id": "integrationServiceEnvironmentId",
        "logic_app_integration_account_id": "logicAppIntegrationAccountId",
        "parameters": "parameters",
        "tags": "tags",
        "timeouts": "timeouts",
        "workflow_parameters": "workflowParameters",
        "workflow_schema": "workflowSchema",
        "workflow_version": "workflowVersion",
    },
)
class LogicAppWorkflowConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        access_control: typing.Optional[typing.Union[LogicAppWorkflowAccessControl, typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["LogicAppWorkflowIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        integration_service_environment_id: typing.Optional[builtins.str] = None,
        logic_app_integration_account_id: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LogicAppWorkflowTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workflow_schema: typing.Optional[builtins.str] = None,
        workflow_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#location LogicAppWorkflow#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#name LogicAppWorkflow#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#resource_group_name LogicAppWorkflow#resource_group_name}.
        :param access_control: access_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#access_control LogicAppWorkflow#access_control}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#enabled LogicAppWorkflow#enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#id LogicAppWorkflow#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#identity LogicAppWorkflow#identity}
        :param integration_service_environment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#integration_service_environment_id LogicAppWorkflow#integration_service_environment_id}.
        :param logic_app_integration_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#logic_app_integration_account_id LogicAppWorkflow#logic_app_integration_account_id}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#parameters LogicAppWorkflow#parameters}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#tags LogicAppWorkflow#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#timeouts LogicAppWorkflow#timeouts}
        :param workflow_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#workflow_parameters LogicAppWorkflow#workflow_parameters}.
        :param workflow_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#workflow_schema LogicAppWorkflow#workflow_schema}.
        :param workflow_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#workflow_version LogicAppWorkflow#workflow_version}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(access_control, dict):
            access_control = LogicAppWorkflowAccessControl(**access_control)
        if isinstance(identity, dict):
            identity = LogicAppWorkflowIdentity(**identity)
        if isinstance(timeouts, dict):
            timeouts = LogicAppWorkflowTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ca82d4428c8f63f8c415877029178375fdeabfefd8fb419c10bcd3b6daf7570)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument access_control", value=access_control, expected_type=type_hints["access_control"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument integration_service_environment_id", value=integration_service_environment_id, expected_type=type_hints["integration_service_environment_id"])
            check_type(argname="argument logic_app_integration_account_id", value=logic_app_integration_account_id, expected_type=type_hints["logic_app_integration_account_id"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument workflow_parameters", value=workflow_parameters, expected_type=type_hints["workflow_parameters"])
            check_type(argname="argument workflow_schema", value=workflow_schema, expected_type=type_hints["workflow_schema"])
            check_type(argname="argument workflow_version", value=workflow_version, expected_type=type_hints["workflow_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
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
        if access_control is not None:
            self._values["access_control"] = access_control
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if integration_service_environment_id is not None:
            self._values["integration_service_environment_id"] = integration_service_environment_id
        if logic_app_integration_account_id is not None:
            self._values["logic_app_integration_account_id"] = logic_app_integration_account_id
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if workflow_parameters is not None:
            self._values["workflow_parameters"] = workflow_parameters
        if workflow_schema is not None:
            self._values["workflow_schema"] = workflow_schema
        if workflow_version is not None:
            self._values["workflow_version"] = workflow_version

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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#location LogicAppWorkflow#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#name LogicAppWorkflow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#resource_group_name LogicAppWorkflow#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_control(self) -> typing.Optional[LogicAppWorkflowAccessControl]:
        '''access_control block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#access_control LogicAppWorkflow#access_control}
        '''
        result = self._values.get("access_control")
        return typing.cast(typing.Optional[LogicAppWorkflowAccessControl], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#enabled LogicAppWorkflow#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#id LogicAppWorkflow#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["LogicAppWorkflowIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#identity LogicAppWorkflow#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["LogicAppWorkflowIdentity"], result)

    @builtins.property
    def integration_service_environment_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#integration_service_environment_id LogicAppWorkflow#integration_service_environment_id}.'''
        result = self._values.get("integration_service_environment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logic_app_integration_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#logic_app_integration_account_id LogicAppWorkflow#logic_app_integration_account_id}.'''
        result = self._values.get("logic_app_integration_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#parameters LogicAppWorkflow#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#tags LogicAppWorkflow#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["LogicAppWorkflowTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#timeouts LogicAppWorkflow#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["LogicAppWorkflowTimeouts"], result)

    @builtins.property
    def workflow_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#workflow_parameters LogicAppWorkflow#workflow_parameters}.'''
        result = self._values.get("workflow_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def workflow_schema(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#workflow_schema LogicAppWorkflow#workflow_schema}.'''
        result = self._values.get("workflow_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#workflow_version LogicAppWorkflow#workflow_version}.'''
        result = self._values.get("workflow_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogicAppWorkflowConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class LogicAppWorkflowIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#type LogicAppWorkflow#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#identity_ids LogicAppWorkflow#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83293e4812881b846e5a2f1296a177a1a8ef0b765fa5eac43fe17da67a705a5f)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#type LogicAppWorkflow#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#identity_ids LogicAppWorkflow#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogicAppWorkflowIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogicAppWorkflowIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb23df23d40449958df76c9f656cf9fc964dacb651cd4589e1f2ba95bfc8083d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a89d9c2c80ee0d196aefd080e887f1b3e4e0040709bcb9c6ee3908effb755260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc18b7e73b2be19628c6410ca87e2ffec2816ee9e581f44ac1882a9195379669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogicAppWorkflowIdentity]:
        return typing.cast(typing.Optional[LogicAppWorkflowIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LogicAppWorkflowIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e6bde54a37ca270085b61095ada9101bdafb0e0f3c5190fec78da77c5fb1cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class LogicAppWorkflowTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#create LogicAppWorkflow#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#delete LogicAppWorkflow#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#read LogicAppWorkflow#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#update LogicAppWorkflow#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14516642404bed7af0b722f8d30ac7d75b69e125b033547e7a1f52f37f364d61)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#create LogicAppWorkflow#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#delete LogicAppWorkflow#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#read LogicAppWorkflow#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_workflow#update LogicAppWorkflow#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogicAppWorkflowTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogicAppWorkflowTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppWorkflow.LogicAppWorkflowTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02679a5c461ce76e8314e76a095dc24d8a42ad301966c572d7abf11a5a2c761b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e01c9df3438545c468611535ae93761a95ae89c93494ab83548493f66377175d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c169eeda4773baa65193053221d9e9ff7bee584a44183b204f029b37c3aef6e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bee2e532b519ea9eddd9c80cafb9ee8034323f223f55ccbb037449bbe6518fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f220e8ffbaac6000afa18359b8d599bc5c22a6d8c43bd418e156b9d8f58cadd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppWorkflowTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppWorkflowTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppWorkflowTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df692d0d425dd7044fa1b37ea5ae99b80fce0b3cfdf8c180ad64f0bdd28202cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LogicAppWorkflow",
    "LogicAppWorkflowAccessControl",
    "LogicAppWorkflowAccessControlAction",
    "LogicAppWorkflowAccessControlActionOutputReference",
    "LogicAppWorkflowAccessControlContent",
    "LogicAppWorkflowAccessControlContentOutputReference",
    "LogicAppWorkflowAccessControlOutputReference",
    "LogicAppWorkflowAccessControlTrigger",
    "LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy",
    "LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim",
    "LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaimList",
    "LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaimOutputReference",
    "LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyList",
    "LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyOutputReference",
    "LogicAppWorkflowAccessControlTriggerOutputReference",
    "LogicAppWorkflowAccessControlWorkflowManagement",
    "LogicAppWorkflowAccessControlWorkflowManagementOutputReference",
    "LogicAppWorkflowConfig",
    "LogicAppWorkflowIdentity",
    "LogicAppWorkflowIdentityOutputReference",
    "LogicAppWorkflowTimeouts",
    "LogicAppWorkflowTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2dc380563e6ea1e41143d97d08ca58823a8e2fb379ce21a9ba525613ba11b0ee(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    access_control: typing.Optional[typing.Union[LogicAppWorkflowAccessControl, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[LogicAppWorkflowIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    integration_service_environment_id: typing.Optional[builtins.str] = None,
    logic_app_integration_account_id: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LogicAppWorkflowTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workflow_schema: typing.Optional[builtins.str] = None,
    workflow_version: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__8ab6bea0d3746dc378ecac710a568098e5b9ac15ef2e2b360c777be81ba3732c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a450fcd97b3938b722b53daf79725b8ebd4aaea08b51fc582c8f385db4f83b8d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d16110d759c9e240dd6a4bef3bbc174f45aac236c472a23d53816e989ef0f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f08ce6f971a908db6b90d8b7cad0419e3661d6f35f26b3e81d5dcbe80e3defc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85d7c44b8759ed779ffc61c2ca7affbd7899d80139d7f4eaee52397c509f80d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed7dadc16ba9b378f95a4049c1054fc39619c47e1ebe787e9539615e6362b5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a610e853b810d1ff95264ec00240e04915cc33a6126b77ee2ecb65c6d642dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3326b6a7e8edf66fcf88c325cc316af7d26023a44d465d091879c8b1d0d054(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29cd47d5bfa3e330a2e4582e105800604211bf2f3eef26376e28794b4111d966(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d92b87a57d02ccdde8c662c1fc8f0221b14b1a49d91b07bf11d780e9b06601(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f0fa7d9b3173f2afcddb4986a54c229dfdb05722168246c2e4664bb6199013(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb3b0b86a6bb4c17c65077862aed92015bd695636d531f73c6596e13812cb29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4372881c391fcc9107ac1ae6fe7f6590f6f0da3fc16a85c333348780e071cdf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2d9d8bbf388487048fd529e7ee5df1ac225e95f5a6b31fec4d65c960e54b91(
    *,
    action: typing.Optional[typing.Union[LogicAppWorkflowAccessControlAction, typing.Dict[builtins.str, typing.Any]]] = None,
    content: typing.Optional[typing.Union[LogicAppWorkflowAccessControlContent, typing.Dict[builtins.str, typing.Any]]] = None,
    trigger: typing.Optional[typing.Union[LogicAppWorkflowAccessControlTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow_management: typing.Optional[typing.Union[LogicAppWorkflowAccessControlWorkflowManagement, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8eda4ffeb5f01fc0deece537ea93211d39448fa8e93c2e1dc9c6cf17fb7a661(
    *,
    allowed_caller_ip_address_range: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b910c72ea31bb3750e55c4c1315a0add10240e03ba6b0f293c50a35e19c4c34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10644879fd23cafca953b83d19c1ba17c1b07bee18247d645cb5e3c1dd92828a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ef76191f5e0bee75f8e3801ace24828bfe15c773e3687917132ede543fd58b(
    value: typing.Optional[LogicAppWorkflowAccessControlAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02b45811689d38931e067684de95826aae3870d43cf10958071530322e0f62a(
    *,
    allowed_caller_ip_address_range: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c5205dc16033fc890b0d753e7a2de274081709d0fee857bc986a1dbb919dd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36499b513161c76f32ba1be720dd57c1e9ce279455b8c5e3fc63ddbaf47f654(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5444f63737c2f6a630bca2992093454ba8bbf4895ae35a0311959a511352e6f2(
    value: typing.Optional[LogicAppWorkflowAccessControlContent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821c5acfc5f234331932557f51b3e474f1dda09a4e1a017de974f7086204ea48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__994137f109684171dd01c2bd5067c8a5323ccb73d9ca53c2645457ffd608a6b6(
    value: typing.Optional[LogicAppWorkflowAccessControl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b62439484ae56ee9642e1da862639a66b1938c911e39fceced61be86c20be2(
    *,
    allowed_caller_ip_address_range: typing.Sequence[builtins.str],
    open_authentication_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7440e5f5e7f973c5d69c18b5f914d216d577d1c53132a8487f52aa6aa807cd90(
    *,
    claim: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678df7d21176484c18601ad7aa1e1928c1ed059e5d4ed02485f98c9d36178fa0(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__549933df89ae2cebaa10d4ec48f9c793f27e70f192c0ba4f97c232d9996c2ab3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2505357d9c2e575826e6c5202848d1140fdfa7f9873b145f472b3e8aa1d6551c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba8f1e9f01c3542224f5012bbc6c91f22ff8d5738f494662d2707c6239bc0bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e4e3c9a3d0987b29427ca16a840e68a591239e493ce5f97d249d962d47be48(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60f0665466d0fec5aac13577432b19adf6b859c4524e1205af72a85833d1c40(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1d3f39ec34e32ea1e906117d9459ff4dcc63da71a9ff70c049d12d965ae4fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e68fbe87dc637fa59d588e41cf96507fd7389b12812f1eb3471c54a06bdc5d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4378ab1d9c385b93fef83e0dc0d9408ee24410649202364ce49ab8ceac54c5c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39402c46af45989a1a1baf7493002ce213c11f59adf1bd681ffee3b9f67b251(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d14cbff393359460172789b70c1f33a039f753fe83f765c23897b865c54bfc4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ad19f98481d80269d9902d7aa20f4c6c1205691fc100b5a7ceb282f15d7cfe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__526f0ae72392b5ce4a223bfd208df8e64d8343d463746e5d1764284d12dc818c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665dbcbd34367fccc1624d008b1b14dd2927f0963646f09545d53c08c8eaae24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6550a82b3aef5539ec414e519fa5da1a799e0d375c4434755e06ee21c7a7f08(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b622ad0691bae5304e0fa75fe6e44e9924f374d97ac3060e4f72db406a95b9b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__372fe3b97ef867382468c8dd005c546b7bea057c13035bafdaedebbaac5dba79(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a61140c31577a79e8ccd2be824beccb077823512128ab153bc66aabbadc1a45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04134c77f5c1747b84438636379c0ac457b9b2b1ee14e108f173b1981047a998(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicyClaim, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5339d0d3c0abc788eafa175af02abfcdad033a75e8c9ede003d2737f933dd1fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc774e2dcd28efca1c648ae182c49ffa0b20e1d5671fcb8cc532a94807da497(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f75ba074641b0583fe646c1247c17b0f7607a34aeec1895588c763e67f07d5b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c84e3a6059a695f07862520d1c781f4e7ad2d234657816521309cf9e022ec10(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogicAppWorkflowAccessControlTriggerOpenAuthenticationPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19956d89ea65517ea1493e8343e07e1d06224aede9c5a4f61059a1647bfabded(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6b8a934aa0fe154cef3b751d38fd22f96482c97bd48c7a0b4af87498404bc05(
    value: typing.Optional[LogicAppWorkflowAccessControlTrigger],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2138f4326c090bd4c63b1fbce5700ded552aabaa920a15c1eadb22a40879a3ab(
    *,
    allowed_caller_ip_address_range: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9224c3c5cf38949b29ee6c3c3d9916a30e63900cd2d9c40a861341c3541c2d64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0a0c0a0e667461c28f354fb0c65fe7fe09fafb8547d5e3ff2528b8fce6a8fd6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fccd1fadff67607beb3092e4f4562f51b1861a52327a381cc3ef69ef876bb589(
    value: typing.Optional[LogicAppWorkflowAccessControlWorkflowManagement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca82d4428c8f63f8c415877029178375fdeabfefd8fb419c10bcd3b6daf7570(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    access_control: typing.Optional[typing.Union[LogicAppWorkflowAccessControl, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[LogicAppWorkflowIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    integration_service_environment_id: typing.Optional[builtins.str] = None,
    logic_app_integration_account_id: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LogicAppWorkflowTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workflow_schema: typing.Optional[builtins.str] = None,
    workflow_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83293e4812881b846e5a2f1296a177a1a8ef0b765fa5eac43fe17da67a705a5f(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb23df23d40449958df76c9f656cf9fc964dacb651cd4589e1f2ba95bfc8083d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89d9c2c80ee0d196aefd080e887f1b3e4e0040709bcb9c6ee3908effb755260(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc18b7e73b2be19628c6410ca87e2ffec2816ee9e581f44ac1882a9195379669(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e6bde54a37ca270085b61095ada9101bdafb0e0f3c5190fec78da77c5fb1cf(
    value: typing.Optional[LogicAppWorkflowIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14516642404bed7af0b722f8d30ac7d75b69e125b033547e7a1f52f37f364d61(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02679a5c461ce76e8314e76a095dc24d8a42ad301966c572d7abf11a5a2c761b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01c9df3438545c468611535ae93761a95ae89c93494ab83548493f66377175d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c169eeda4773baa65193053221d9e9ff7bee584a44183b204f029b37c3aef6e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bee2e532b519ea9eddd9c80cafb9ee8034323f223f55ccbb037449bbe6518fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f220e8ffbaac6000afa18359b8d599bc5c22a6d8c43bd418e156b9d8f58cadd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df692d0d425dd7044fa1b37ea5ae99b80fce0b3cfdf8c180ad64f0bdd28202cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppWorkflowTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

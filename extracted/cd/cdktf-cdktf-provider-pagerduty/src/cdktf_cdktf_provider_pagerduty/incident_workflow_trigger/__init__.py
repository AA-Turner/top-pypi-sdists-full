r'''
# `pagerduty_incident_workflow_trigger`

Refer to the Terraform Registry for docs: [`pagerduty_incident_workflow_trigger`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger).
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


class IncidentWorkflowTrigger(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.incidentWorkflowTrigger.IncidentWorkflowTrigger",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger pagerduty_incident_workflow_trigger}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        subscribed_to_all_services: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        type: builtins.str,
        workflow: builtins.str,
        condition: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union["IncidentWorkflowTriggerPermissions", typing.Dict[builtins.str, typing.Any]]] = None,
        services: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger pagerduty_incident_workflow_trigger} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param subscribed_to_all_services: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#subscribed_to_all_services IncidentWorkflowTrigger#subscribed_to_all_services}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#type IncidentWorkflowTrigger#type}.
        :param workflow: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#workflow IncidentWorkflowTrigger#workflow}.
        :param condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#condition IncidentWorkflowTrigger#condition}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#id IncidentWorkflowTrigger#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#permissions IncidentWorkflowTrigger#permissions}
        :param services: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#services IncidentWorkflowTrigger#services}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__474eb925a0279457b4e0352c4191021c338bb6318a1e44732f14465151060d24)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IncidentWorkflowTriggerConfig(
            subscribed_to_all_services=subscribed_to_all_services,
            type=type,
            workflow=workflow,
            condition=condition,
            id=id,
            permissions=permissions,
            services=services,
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
        '''Generates CDKTF code for importing a IncidentWorkflowTrigger resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IncidentWorkflowTrigger to import.
        :param import_from_id: The id of the existing IncidentWorkflowTrigger that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IncidentWorkflowTrigger to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eefe6cf911fc93f596b3399d34e880a96dda4a236be8ffb0e23975decd7a0496)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPermissions")
    def put_permissions(
        self,
        *,
        restricted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        team_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param restricted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#restricted IncidentWorkflowTrigger#restricted}.
        :param team_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#team_id IncidentWorkflowTrigger#team_id}.
        '''
        value = IncidentWorkflowTriggerPermissions(
            restricted=restricted, team_id=team_id
        )

        return typing.cast(None, jsii.invoke(self, "putPermissions", [value]))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

    @jsii.member(jsii_name="resetServices")
    def reset_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServices", []))

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
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> "IncidentWorkflowTriggerPermissionsOutputReference":
        return typing.cast("IncidentWorkflowTriggerPermissionsOutputReference", jsii.get(self, "permissions"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsInput")
    def permissions_input(
        self,
    ) -> typing.Optional["IncidentWorkflowTriggerPermissions"]:
        return typing.cast(typing.Optional["IncidentWorkflowTriggerPermissions"], jsii.get(self, "permissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="servicesInput")
    def services_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "servicesInput"))

    @builtins.property
    @jsii.member(jsii_name="subscribedToAllServicesInput")
    def subscribed_to_all_services_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "subscribedToAllServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="workflowInput")
    def workflow_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workflowInput"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @condition.setter
    def condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc00b782237d29628b2240d6b1503156c0ecc7aa374ae784afcddf0fe9765051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "condition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f3544004ee6d62f9c9641d4952afddffe30641eb4f265cc8604e9ab6f3bdc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="services")
    def services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "services"))

    @services.setter
    def services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03391dc83a495e4500e18c952bf3f17dc01ba4f75c49d85eef25c0a608b1eaa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "services", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subscribedToAllServices")
    def subscribed_to_all_services(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "subscribedToAllServices"))

    @subscribed_to_all_services.setter
    def subscribed_to_all_services(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc5bd22bbf36b3e8e19a944f0d15bb9446a75adfe2055b325e877dd4837a06a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscribedToAllServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c982757c19ebcef95828be5934361adf1f61a8788dfd522c601ca30f783bd945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workflow")
    def workflow(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workflow"))

    @workflow.setter
    def workflow(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c20e4d8d1ba71e02ae9ddf539589006d5dbc1f6fd260ea4c2c988cf7b1cc2f32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workflow", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.incidentWorkflowTrigger.IncidentWorkflowTriggerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "subscribed_to_all_services": "subscribedToAllServices",
        "type": "type",
        "workflow": "workflow",
        "condition": "condition",
        "id": "id",
        "permissions": "permissions",
        "services": "services",
    },
)
class IncidentWorkflowTriggerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        subscribed_to_all_services: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        type: builtins.str,
        workflow: builtins.str,
        condition: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union["IncidentWorkflowTriggerPermissions", typing.Dict[builtins.str, typing.Any]]] = None,
        services: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param subscribed_to_all_services: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#subscribed_to_all_services IncidentWorkflowTrigger#subscribed_to_all_services}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#type IncidentWorkflowTrigger#type}.
        :param workflow: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#workflow IncidentWorkflowTrigger#workflow}.
        :param condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#condition IncidentWorkflowTrigger#condition}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#id IncidentWorkflowTrigger#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#permissions IncidentWorkflowTrigger#permissions}
        :param services: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#services IncidentWorkflowTrigger#services}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(permissions, dict):
            permissions = IncidentWorkflowTriggerPermissions(**permissions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc1b9a0e5410c77807d0cc06e4212c46e8e67dae6e9398fe288cc5495b0bbf41)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument subscribed_to_all_services", value=subscribed_to_all_services, expected_type=type_hints["subscribed_to_all_services"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument workflow", value=workflow, expected_type=type_hints["workflow"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subscribed_to_all_services": subscribed_to_all_services,
            "type": type,
            "workflow": workflow,
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
        if condition is not None:
            self._values["condition"] = condition
        if id is not None:
            self._values["id"] = id
        if permissions is not None:
            self._values["permissions"] = permissions
        if services is not None:
            self._values["services"] = services

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
    def subscribed_to_all_services(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#subscribed_to_all_services IncidentWorkflowTrigger#subscribed_to_all_services}.'''
        result = self._values.get("subscribed_to_all_services")
        assert result is not None, "Required property 'subscribed_to_all_services' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#type IncidentWorkflowTrigger#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workflow(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#workflow IncidentWorkflowTrigger#workflow}.'''
        result = self._values.get("workflow")
        assert result is not None, "Required property 'workflow' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#condition IncidentWorkflowTrigger#condition}.'''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#id IncidentWorkflowTrigger#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions(self) -> typing.Optional["IncidentWorkflowTriggerPermissions"]:
        '''permissions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#permissions IncidentWorkflowTrigger#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional["IncidentWorkflowTriggerPermissions"], result)

    @builtins.property
    def services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#services IncidentWorkflowTrigger#services}.'''
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IncidentWorkflowTriggerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.incidentWorkflowTrigger.IncidentWorkflowTriggerPermissions",
    jsii_struct_bases=[],
    name_mapping={"restricted": "restricted", "team_id": "teamId"},
)
class IncidentWorkflowTriggerPermissions:
    def __init__(
        self,
        *,
        restricted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        team_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param restricted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#restricted IncidentWorkflowTrigger#restricted}.
        :param team_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#team_id IncidentWorkflowTrigger#team_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd3eae5931813111ac5fe244a946c08c069ff177c379f4d0816cfcc92e5fe032)
            check_type(argname="argument restricted", value=restricted, expected_type=type_hints["restricted"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if restricted is not None:
            self._values["restricted"] = restricted
        if team_id is not None:
            self._values["team_id"] = team_id

    @builtins.property
    def restricted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#restricted IncidentWorkflowTrigger#restricted}.'''
        result = self._values.get("restricted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/incident_workflow_trigger#team_id IncidentWorkflowTrigger#team_id}.'''
        result = self._values.get("team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IncidentWorkflowTriggerPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IncidentWorkflowTriggerPermissionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.incidentWorkflowTrigger.IncidentWorkflowTriggerPermissionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e9490fdc8110032564452e2380e538cc86db57a516c97626d17d814425ed923)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRestricted")
    def reset_restricted(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestricted", []))

    @jsii.member(jsii_name="resetTeamId")
    def reset_team_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeamId", []))

    @builtins.property
    @jsii.member(jsii_name="restrictedInput")
    def restricted_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "restrictedInput"))

    @builtins.property
    @jsii.member(jsii_name="teamIdInput")
    def team_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamIdInput"))

    @builtins.property
    @jsii.member(jsii_name="restricted")
    def restricted(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "restricted"))

    @restricted.setter
    def restricted(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fddaaa4f386817262952e90bf4dda11c4fd4d95cbc17b32afb452fdf89205237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restricted", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__010cdb35d8fb791c83308e4709544db3077ef27a2a08943002721a92e8fe0e32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IncidentWorkflowTriggerPermissions]:
        return typing.cast(typing.Optional[IncidentWorkflowTriggerPermissions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IncidentWorkflowTriggerPermissions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b840a7f7722a5fbcff7783b5b594b854cf917d29fc9adb08d4dcdd20f15e2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IncidentWorkflowTrigger",
    "IncidentWorkflowTriggerConfig",
    "IncidentWorkflowTriggerPermissions",
    "IncidentWorkflowTriggerPermissionsOutputReference",
]

publication.publish()

def _typecheckingstub__474eb925a0279457b4e0352c4191021c338bb6318a1e44732f14465151060d24(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    subscribed_to_all_services: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    type: builtins.str,
    workflow: builtins.str,
    condition: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Union[IncidentWorkflowTriggerPermissions, typing.Dict[builtins.str, typing.Any]]] = None,
    services: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__eefe6cf911fc93f596b3399d34e880a96dda4a236be8ffb0e23975decd7a0496(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc00b782237d29628b2240d6b1503156c0ecc7aa374ae784afcddf0fe9765051(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f3544004ee6d62f9c9641d4952afddffe30641eb4f265cc8604e9ab6f3bdc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03391dc83a495e4500e18c952bf3f17dc01ba4f75c49d85eef25c0a608b1eaa4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc5bd22bbf36b3e8e19a944f0d15bb9446a75adfe2055b325e877dd4837a06a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c982757c19ebcef95828be5934361adf1f61a8788dfd522c601ca30f783bd945(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20e4d8d1ba71e02ae9ddf539589006d5dbc1f6fd260ea4c2c988cf7b1cc2f32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc1b9a0e5410c77807d0cc06e4212c46e8e67dae6e9398fe288cc5495b0bbf41(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    subscribed_to_all_services: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    type: builtins.str,
    workflow: builtins.str,
    condition: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Union[IncidentWorkflowTriggerPermissions, typing.Dict[builtins.str, typing.Any]]] = None,
    services: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3eae5931813111ac5fe244a946c08c069ff177c379f4d0816cfcc92e5fe032(
    *,
    restricted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    team_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9490fdc8110032564452e2380e538cc86db57a516c97626d17d814425ed923(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fddaaa4f386817262952e90bf4dda11c4fd4d95cbc17b32afb452fdf89205237(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010cdb35d8fb791c83308e4709544db3077ef27a2a08943002721a92e8fe0e32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b840a7f7722a5fbcff7783b5b594b854cf917d29fc9adb08d4dcdd20f15e2b(
    value: typing.Optional[IncidentWorkflowTriggerPermissions],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `azurerm_lighthouse_definition`

Refer to the Terraform Registry for docs: [`azurerm_lighthouse_definition`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition).
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


class LighthouseDefinition(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.lighthouseDefinition.LighthouseDefinition",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition azurerm_lighthouse_definition}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        authorization: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LighthouseDefinitionAuthorization", typing.Dict[builtins.str, typing.Any]]]],
        managing_tenant_id: builtins.str,
        name: builtins.str,
        scope: builtins.str,
        description: typing.Optional[builtins.str] = None,
        eligible_authorization: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LighthouseDefinitionEligibleAuthorization", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        lighthouse_definition_id: typing.Optional[builtins.str] = None,
        plan: typing.Optional[typing.Union["LighthouseDefinitionPlan", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["LighthouseDefinitionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition azurerm_lighthouse_definition} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#authorization LighthouseDefinition#authorization}
        :param managing_tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#managing_tenant_id LighthouseDefinition#managing_tenant_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#name LighthouseDefinition#name}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#scope LighthouseDefinition#scope}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#description LighthouseDefinition#description}.
        :param eligible_authorization: eligible_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#eligible_authorization LighthouseDefinition#eligible_authorization}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#id LighthouseDefinition#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lighthouse_definition_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#lighthouse_definition_id LighthouseDefinition#lighthouse_definition_id}.
        :param plan: plan block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#plan LighthouseDefinition#plan}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#timeouts LighthouseDefinition#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d802e9a1ffecf069954f844072e4d8854e297140bdda1f229d1ebb42de59d469)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LighthouseDefinitionConfig(
            authorization=authorization,
            managing_tenant_id=managing_tenant_id,
            name=name,
            scope=scope,
            description=description,
            eligible_authorization=eligible_authorization,
            id=id,
            lighthouse_definition_id=lighthouse_definition_id,
            plan=plan,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope_, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a LighthouseDefinition resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LighthouseDefinition to import.
        :param import_from_id: The id of the existing LighthouseDefinition that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LighthouseDefinition to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a21ccce1aed9dac40851fbe742a647406c8dc53fa6f01492e27d3484b7268092)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthorization")
    def put_authorization(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LighthouseDefinitionAuthorization", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5120685bb5f3eb213aa5dee36eec0cf9a76b8e54ad77707042bd9245f17484b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthorization", [value]))

    @jsii.member(jsii_name="putEligibleAuthorization")
    def put_eligible_authorization(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LighthouseDefinitionEligibleAuthorization", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba5ef15899e5048967bc3e812daf4ebd3c5997d20af25e8121c9d9799040361b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEligibleAuthorization", [value]))

    @jsii.member(jsii_name="putPlan")
    def put_plan(
        self,
        *,
        name: builtins.str,
        product: builtins.str,
        publisher: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#name LighthouseDefinition#name}.
        :param product: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#product LighthouseDefinition#product}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#publisher LighthouseDefinition#publisher}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#version LighthouseDefinition#version}.
        '''
        value = LighthouseDefinitionPlan(
            name=name, product=product, publisher=publisher, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putPlan", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#create LighthouseDefinition#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#delete LighthouseDefinition#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#read LighthouseDefinition#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#update LighthouseDefinition#update}.
        '''
        value = LighthouseDefinitionTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEligibleAuthorization")
    def reset_eligible_authorization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEligibleAuthorization", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLighthouseDefinitionId")
    def reset_lighthouse_definition_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLighthouseDefinitionId", []))

    @jsii.member(jsii_name="resetPlan")
    def reset_plan(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlan", []))

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
    @jsii.member(jsii_name="authorization")
    def authorization(self) -> "LighthouseDefinitionAuthorizationList":
        return typing.cast("LighthouseDefinitionAuthorizationList", jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="eligibleAuthorization")
    def eligible_authorization(self) -> "LighthouseDefinitionEligibleAuthorizationList":
        return typing.cast("LighthouseDefinitionEligibleAuthorizationList", jsii.get(self, "eligibleAuthorization"))

    @builtins.property
    @jsii.member(jsii_name="plan")
    def plan(self) -> "LighthouseDefinitionPlanOutputReference":
        return typing.cast("LighthouseDefinitionPlanOutputReference", jsii.get(self, "plan"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "LighthouseDefinitionTimeoutsOutputReference":
        return typing.cast("LighthouseDefinitionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="authorizationInput")
    def authorization_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LighthouseDefinitionAuthorization"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LighthouseDefinitionAuthorization"]]], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="eligibleAuthorizationInput")
    def eligible_authorization_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LighthouseDefinitionEligibleAuthorization"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LighthouseDefinitionEligibleAuthorization"]]], jsii.get(self, "eligibleAuthorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lighthouseDefinitionIdInput")
    def lighthouse_definition_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lighthouseDefinitionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="managingTenantIdInput")
    def managing_tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managingTenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="planInput")
    def plan_input(self) -> typing.Optional["LighthouseDefinitionPlan"]:
        return typing.cast(typing.Optional["LighthouseDefinitionPlan"], jsii.get(self, "planInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LighthouseDefinitionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LighthouseDefinitionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0db530aa1cdda0778b432166625e2fdcdf60b67556877197d8aeaf8b2e10632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f08be2d4d7c4959e0fb5a7fbd7411df2a932271da94a34f9301b94ff0f91170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lighthouseDefinitionId")
    def lighthouse_definition_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lighthouseDefinitionId"))

    @lighthouse_definition_id.setter
    def lighthouse_definition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08873c384960a675e5de631ceda6b3c6267ffc50fb91a857b2e3765e12b544e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lighthouseDefinitionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managingTenantId")
    def managing_tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managingTenantId"))

    @managing_tenant_id.setter
    def managing_tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db19bf8ae347cc4454a58da559c682dd4208db73c44c68c89fd58e0883de3c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managingTenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3bb489bd8cd6b030ac9372b2dccfc8be1149c6606580c16a6a8cf154c52c579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a123068c16ec09394c4231119f4691983848d477d5bfe40033cc2f13ad98b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.lighthouseDefinition.LighthouseDefinitionAuthorization",
    jsii_struct_bases=[],
    name_mapping={
        "principal_id": "principalId",
        "role_definition_id": "roleDefinitionId",
        "delegated_role_definition_ids": "delegatedRoleDefinitionIds",
        "principal_display_name": "principalDisplayName",
    },
)
class LighthouseDefinitionAuthorization:
    def __init__(
        self,
        *,
        principal_id: builtins.str,
        role_definition_id: builtins.str,
        delegated_role_definition_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        principal_display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param principal_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#principal_id LighthouseDefinition#principal_id}.
        :param role_definition_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#role_definition_id LighthouseDefinition#role_definition_id}.
        :param delegated_role_definition_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#delegated_role_definition_ids LighthouseDefinition#delegated_role_definition_ids}.
        :param principal_display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#principal_display_name LighthouseDefinition#principal_display_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc5cd3734149ea82a8cd004fb301783d31a4bf1fa3edac605e734141fb836ec)
            check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
            check_type(argname="argument role_definition_id", value=role_definition_id, expected_type=type_hints["role_definition_id"])
            check_type(argname="argument delegated_role_definition_ids", value=delegated_role_definition_ids, expected_type=type_hints["delegated_role_definition_ids"])
            check_type(argname="argument principal_display_name", value=principal_display_name, expected_type=type_hints["principal_display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "principal_id": principal_id,
            "role_definition_id": role_definition_id,
        }
        if delegated_role_definition_ids is not None:
            self._values["delegated_role_definition_ids"] = delegated_role_definition_ids
        if principal_display_name is not None:
            self._values["principal_display_name"] = principal_display_name

    @builtins.property
    def principal_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#principal_id LighthouseDefinition#principal_id}.'''
        result = self._values.get("principal_id")
        assert result is not None, "Required property 'principal_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_definition_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#role_definition_id LighthouseDefinition#role_definition_id}.'''
        result = self._values.get("role_definition_id")
        assert result is not None, "Required property 'role_definition_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delegated_role_definition_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#delegated_role_definition_ids LighthouseDefinition#delegated_role_definition_ids}.'''
        result = self._values.get("delegated_role_definition_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def principal_display_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#principal_display_name LighthouseDefinition#principal_display_name}.'''
        result = self._values.get("principal_display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LighthouseDefinitionAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LighthouseDefinitionAuthorizationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.lighthouseDefinition.LighthouseDefinitionAuthorizationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b524afa73dca674c1a23a5f70eb24ef00ae0eb19156b8f4b94be87fc3689149b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LighthouseDefinitionAuthorizationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb1434bd82334a8604228551c57483979842d7d3ca81103c9720bdd6af3c3965)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LighthouseDefinitionAuthorizationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__726f1b90dcb4889d72976ce0d1021651bb2de925ad71ed283d7d6972508309db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a32856543cb85b8b295a25e753357df7504f30363979dea82f15cde1c3a619f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e65c69f248bd4c4f10f55b41f7b142a9f8a4f2a6c0255b39db82132392d30062)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LighthouseDefinitionAuthorization]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LighthouseDefinitionAuthorization]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LighthouseDefinitionAuthorization]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1bc9d0d81d832085d4477e96e591958ef87db4870857080fbc64e19b456a9f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LighthouseDefinitionAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.lighthouseDefinition.LighthouseDefinitionAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2552540e2c8dbe02dfc626385120afd3a0b41cc491318a4bb59127298a826ef5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDelegatedRoleDefinitionIds")
    def reset_delegated_role_definition_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelegatedRoleDefinitionIds", []))

    @jsii.member(jsii_name="resetPrincipalDisplayName")
    def reset_principal_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrincipalDisplayName", []))

    @builtins.property
    @jsii.member(jsii_name="delegatedRoleDefinitionIdsInput")
    def delegated_role_definition_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "delegatedRoleDefinitionIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="principalDisplayNameInput")
    def principal_display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalDisplayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="principalIdInput")
    def principal_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalIdInput"))

    @builtins.property
    @jsii.member(jsii_name="roleDefinitionIdInput")
    def role_definition_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleDefinitionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="delegatedRoleDefinitionIds")
    def delegated_role_definition_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "delegatedRoleDefinitionIds"))

    @delegated_role_definition_ids.setter
    def delegated_role_definition_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5dd3a18f4876ac9e84337540af6076fa42c3f682ce9feb89b665f02ba26f36e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delegatedRoleDefinitionIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principalDisplayName")
    def principal_display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalDisplayName"))

    @principal_display_name.setter
    def principal_display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5234e3cb113f82bf200d2a03f4b488b381f9eed28fd1bdc0e0bbc26b2881926a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principalDisplayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @principal_id.setter
    def principal_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31df6b68ca8664c67c3b89198551243b2b86bed7a36b492ac3ca89435d23fddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principalId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleDefinitionId")
    def role_definition_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleDefinitionId"))

    @role_definition_id.setter
    def role_definition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a8ebefd883e7e602e22fb57f50cd7b83210685a02c8700532d4d63383b25d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleDefinitionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LighthouseDefinitionAuthorization]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LighthouseDefinitionAuthorization]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LighthouseDefinitionAuthorization]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe17a89feb02a443bb47ba1053a49d104dcbd2bcebdc6d3dbc393f557b30395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.lighthouseDefinition.LighthouseDefinitionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "authorization": "authorization",
        "managing_tenant_id": "managingTenantId",
        "name": "name",
        "scope": "scope",
        "description": "description",
        "eligible_authorization": "eligibleAuthorization",
        "id": "id",
        "lighthouse_definition_id": "lighthouseDefinitionId",
        "plan": "plan",
        "timeouts": "timeouts",
    },
)
class LighthouseDefinitionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        authorization: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LighthouseDefinitionAuthorization, typing.Dict[builtins.str, typing.Any]]]],
        managing_tenant_id: builtins.str,
        name: builtins.str,
        scope: builtins.str,
        description: typing.Optional[builtins.str] = None,
        eligible_authorization: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LighthouseDefinitionEligibleAuthorization", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        lighthouse_definition_id: typing.Optional[builtins.str] = None,
        plan: typing.Optional[typing.Union["LighthouseDefinitionPlan", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["LighthouseDefinitionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#authorization LighthouseDefinition#authorization}
        :param managing_tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#managing_tenant_id LighthouseDefinition#managing_tenant_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#name LighthouseDefinition#name}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#scope LighthouseDefinition#scope}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#description LighthouseDefinition#description}.
        :param eligible_authorization: eligible_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#eligible_authorization LighthouseDefinition#eligible_authorization}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#id LighthouseDefinition#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lighthouse_definition_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#lighthouse_definition_id LighthouseDefinition#lighthouse_definition_id}.
        :param plan: plan block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#plan LighthouseDefinition#plan}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#timeouts LighthouseDefinition#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(plan, dict):
            plan = LighthouseDefinitionPlan(**plan)
        if isinstance(timeouts, dict):
            timeouts = LighthouseDefinitionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ecf8963fa1ae16ab003bc6c5465bb8c244d2b62a750d58e4d6765c1862c9af7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
            check_type(argname="argument managing_tenant_id", value=managing_tenant_id, expected_type=type_hints["managing_tenant_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument eligible_authorization", value=eligible_authorization, expected_type=type_hints["eligible_authorization"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lighthouse_definition_id", value=lighthouse_definition_id, expected_type=type_hints["lighthouse_definition_id"])
            check_type(argname="argument plan", value=plan, expected_type=type_hints["plan"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorization": authorization,
            "managing_tenant_id": managing_tenant_id,
            "name": name,
            "scope": scope,
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
        if eligible_authorization is not None:
            self._values["eligible_authorization"] = eligible_authorization
        if id is not None:
            self._values["id"] = id
        if lighthouse_definition_id is not None:
            self._values["lighthouse_definition_id"] = lighthouse_definition_id
        if plan is not None:
            self._values["plan"] = plan
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
    def authorization(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LighthouseDefinitionAuthorization]]:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#authorization LighthouseDefinition#authorization}
        '''
        result = self._values.get("authorization")
        assert result is not None, "Required property 'authorization' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LighthouseDefinitionAuthorization]], result)

    @builtins.property
    def managing_tenant_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#managing_tenant_id LighthouseDefinition#managing_tenant_id}.'''
        result = self._values.get("managing_tenant_id")
        assert result is not None, "Required property 'managing_tenant_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#name LighthouseDefinition#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#scope LighthouseDefinition#scope}.'''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#description LighthouseDefinition#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eligible_authorization(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LighthouseDefinitionEligibleAuthorization"]]]:
        '''eligible_authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#eligible_authorization LighthouseDefinition#eligible_authorization}
        '''
        result = self._values.get("eligible_authorization")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LighthouseDefinitionEligibleAuthorization"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#id LighthouseDefinition#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lighthouse_definition_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#lighthouse_definition_id LighthouseDefinition#lighthouse_definition_id}.'''
        result = self._values.get("lighthouse_definition_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plan(self) -> typing.Optional["LighthouseDefinitionPlan"]:
        '''plan block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#plan LighthouseDefinition#plan}
        '''
        result = self._values.get("plan")
        return typing.cast(typing.Optional["LighthouseDefinitionPlan"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["LighthouseDefinitionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#timeouts LighthouseDefinition#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["LighthouseDefinitionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LighthouseDefinitionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.lighthouseDefinition.LighthouseDefinitionEligibleAuthorization",
    jsii_struct_bases=[],
    name_mapping={
        "principal_id": "principalId",
        "role_definition_id": "roleDefinitionId",
        "just_in_time_access_policy": "justInTimeAccessPolicy",
        "principal_display_name": "principalDisplayName",
    },
)
class LighthouseDefinitionEligibleAuthorization:
    def __init__(
        self,
        *,
        principal_id: builtins.str,
        role_definition_id: builtins.str,
        just_in_time_access_policy: typing.Optional[typing.Union["LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        principal_display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param principal_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#principal_id LighthouseDefinition#principal_id}.
        :param role_definition_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#role_definition_id LighthouseDefinition#role_definition_id}.
        :param just_in_time_access_policy: just_in_time_access_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#just_in_time_access_policy LighthouseDefinition#just_in_time_access_policy}
        :param principal_display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#principal_display_name LighthouseDefinition#principal_display_name}.
        '''
        if isinstance(just_in_time_access_policy, dict):
            just_in_time_access_policy = LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicy(**just_in_time_access_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b80e7bd67a25ab7a8557d399b50fe5c87f80cacca76333fd96e92d596ff644a6)
            check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
            check_type(argname="argument role_definition_id", value=role_definition_id, expected_type=type_hints["role_definition_id"])
            check_type(argname="argument just_in_time_access_policy", value=just_in_time_access_policy, expected_type=type_hints["just_in_time_access_policy"])
            check_type(argname="argument principal_display_name", value=principal_display_name, expected_type=type_hints["principal_display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "principal_id": principal_id,
            "role_definition_id": role_definition_id,
        }
        if just_in_time_access_policy is not None:
            self._values["just_in_time_access_policy"] = just_in_time_access_policy
        if principal_display_name is not None:
            self._values["principal_display_name"] = principal_display_name

    @builtins.property
    def principal_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#principal_id LighthouseDefinition#principal_id}.'''
        result = self._values.get("principal_id")
        assert result is not None, "Required property 'principal_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_definition_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#role_definition_id LighthouseDefinition#role_definition_id}.'''
        result = self._values.get("role_definition_id")
        assert result is not None, "Required property 'role_definition_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def just_in_time_access_policy(
        self,
    ) -> typing.Optional["LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicy"]:
        '''just_in_time_access_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#just_in_time_access_policy LighthouseDefinition#just_in_time_access_policy}
        '''
        result = self._values.get("just_in_time_access_policy")
        return typing.cast(typing.Optional["LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicy"], result)

    @builtins.property
    def principal_display_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#principal_display_name LighthouseDefinition#principal_display_name}.'''
        result = self._values.get("principal_display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LighthouseDefinitionEligibleAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.lighthouseDefinition.LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "approver": "approver",
        "maximum_activation_duration": "maximumActivationDuration",
        "multi_factor_auth_provider": "multiFactorAuthProvider",
    },
)
class LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicy:
    def __init__(
        self,
        *,
        approver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover", typing.Dict[builtins.str, typing.Any]]]]] = None,
        maximum_activation_duration: typing.Optional[builtins.str] = None,
        multi_factor_auth_provider: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param approver: approver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#approver LighthouseDefinition#approver}
        :param maximum_activation_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#maximum_activation_duration LighthouseDefinition#maximum_activation_duration}.
        :param multi_factor_auth_provider: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#multi_factor_auth_provider LighthouseDefinition#multi_factor_auth_provider}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95d5824dba04702d36db95bc95190d27c8d197f8d63866d6564633e5e4987001)
            check_type(argname="argument approver", value=approver, expected_type=type_hints["approver"])
            check_type(argname="argument maximum_activation_duration", value=maximum_activation_duration, expected_type=type_hints["maximum_activation_duration"])
            check_type(argname="argument multi_factor_auth_provider", value=multi_factor_auth_provider, expected_type=type_hints["multi_factor_auth_provider"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if approver is not None:
            self._values["approver"] = approver
        if maximum_activation_duration is not None:
            self._values["maximum_activation_duration"] = maximum_activation_duration
        if multi_factor_auth_provider is not None:
            self._values["multi_factor_auth_provider"] = multi_factor_auth_provider

    @builtins.property
    def approver(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover"]]]:
        '''approver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#approver LighthouseDefinition#approver}
        '''
        result = self._values.get("approver")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover"]]], result)

    @builtins.property
    def maximum_activation_duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#maximum_activation_duration LighthouseDefinition#maximum_activation_duration}.'''
        result = self._values.get("maximum_activation_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_factor_auth_provider(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#multi_factor_auth_provider LighthouseDefinition#multi_factor_auth_provider}.'''
        result = self._values.get("multi_factor_auth_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.lighthouseDefinition.LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover",
    jsii_struct_bases=[],
    name_mapping={
        "principal_id": "principalId",
        "principal_display_name": "principalDisplayName",
    },
)
class LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover:
    def __init__(
        self,
        *,
        principal_id: builtins.str,
        principal_display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param principal_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#principal_id LighthouseDefinition#principal_id}.
        :param principal_display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#principal_display_name LighthouseDefinition#principal_display_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b4f2e6b4299d5beae745afde767d82f69daf5404b52ca34cf5aabafe9a30077)
            check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
            check_type(argname="argument principal_display_name", value=principal_display_name, expected_type=type_hints["principal_display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "principal_id": principal_id,
        }
        if principal_display_name is not None:
            self._values["principal_display_name"] = principal_display_name

    @builtins.property
    def principal_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#principal_id LighthouseDefinition#principal_id}.'''
        result = self._values.get("principal_id")
        assert result is not None, "Required property 'principal_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def principal_display_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#principal_display_name LighthouseDefinition#principal_display_name}.'''
        result = self._values.get("principal_display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApproverList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.lighthouseDefinition.LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApproverList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85fb47cff47f43904a8056309dddda068addeeaad87e08c8b576fedde9710b78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApproverOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bcbe029051787dc67a8bb88d6b1f4d746d77b30a5cb3e5a2bd4b642b5077c33)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApproverOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4082fb4ec1883fd553a4ec3a767b05c69d394b997d86d20538f7cdc444a86c05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f7c6bb07ca40954f2aedee3cd4a067f76d81fbba7a4c67f041d21300a0bdd51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92b91f7c289f8b6bd3f4baa5eee5919ade778313edde88e0173d75776e6bb320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e3445bf9772e6ff1eb59616cd27cffda87af2daa6dfeb79ce7f531af307bb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApproverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.lighthouseDefinition.LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApproverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfa9e17667eae2aaae6868999a11cd87660564fa8cede4d7ea995e195fa1d4d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPrincipalDisplayName")
    def reset_principal_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrincipalDisplayName", []))

    @builtins.property
    @jsii.member(jsii_name="principalDisplayNameInput")
    def principal_display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalDisplayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="principalIdInput")
    def principal_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalIdInput"))

    @builtins.property
    @jsii.member(jsii_name="principalDisplayName")
    def principal_display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalDisplayName"))

    @principal_display_name.setter
    def principal_display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9f40440ebb3f639eef287397cc79392fed7ab779e92d13a488dc82e2068957)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principalDisplayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @principal_id.setter
    def principal_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70bd1b4e32027916cc8dc8d26156090c53b7c92e08d01b8c8ef5fd64fc2cbf1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principalId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ae820d4ff83a35b0cf9ece54b77a56299f68a14b8c7636f99aa19ed382d8365)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.lighthouseDefinition.LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15e989c82dbf6004a08d56bef3f1ce69bb9c0f3090a33079bb96cbad9cbb1aac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApprover")
    def put_approver(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8cf9e9cf867c73aabecc7b25f7528afe58606b042eb9aa3908931af50834a8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putApprover", [value]))

    @jsii.member(jsii_name="resetApprover")
    def reset_approver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApprover", []))

    @jsii.member(jsii_name="resetMaximumActivationDuration")
    def reset_maximum_activation_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumActivationDuration", []))

    @jsii.member(jsii_name="resetMultiFactorAuthProvider")
    def reset_multi_factor_auth_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiFactorAuthProvider", []))

    @builtins.property
    @jsii.member(jsii_name="approver")
    def approver(
        self,
    ) -> LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApproverList:
        return typing.cast(LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApproverList, jsii.get(self, "approver"))

    @builtins.property
    @jsii.member(jsii_name="approverInput")
    def approver_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover]]], jsii.get(self, "approverInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumActivationDurationInput")
    def maximum_activation_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maximumActivationDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="multiFactorAuthProviderInput")
    def multi_factor_auth_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "multiFactorAuthProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumActivationDuration")
    def maximum_activation_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maximumActivationDuration"))

    @maximum_activation_duration.setter
    def maximum_activation_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea5ccd2f50875867d0db4c2a11e0d7a8982c8004a6fd82fdaf4922b04b1bbce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumActivationDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiFactorAuthProvider")
    def multi_factor_auth_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "multiFactorAuthProvider"))

    @multi_factor_auth_provider.setter
    def multi_factor_auth_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0c3ac890354d5720e598b0a6bf31951275dcd12e60efbb06a23415e78f8e90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiFactorAuthProvider", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicy]:
        return typing.cast(typing.Optional[LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd580685343430e40d6303d10d3ddf7aafc9d08fbdc0cb8c7b9d4c0d46452c3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LighthouseDefinitionEligibleAuthorizationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.lighthouseDefinition.LighthouseDefinitionEligibleAuthorizationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c35becee0adcbeb9ca0371a744f70c5fe347300ed42b2df66ae78150790e625)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LighthouseDefinitionEligibleAuthorizationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e36f4be2505ae3d1b961021183e7447125b17cc0ca9204e640abd3a7b6098a0e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LighthouseDefinitionEligibleAuthorizationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6cb04a3bd0fb61f771d91546d47e8a7f0e300d94a5b22fecad3619a2c624e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__056cac3386cc90a274469b242b7e77b665372a041272963cc49542319ed73bf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bf38eb6e8e92efc3f9f2164645253cd57ee2384caf3d6b4db7ad13b48aa9156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LighthouseDefinitionEligibleAuthorization]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LighthouseDefinitionEligibleAuthorization]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LighthouseDefinitionEligibleAuthorization]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1dfd519d73b782c46969304ea2803dc26afd7e86a18a993f782ed83adb4a58c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LighthouseDefinitionEligibleAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.lighthouseDefinition.LighthouseDefinitionEligibleAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa52617f656cc639449b505fe5e6300e5029ca6172802198b32b7318779990b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putJustInTimeAccessPolicy")
    def put_just_in_time_access_policy(
        self,
        *,
        approver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover, typing.Dict[builtins.str, typing.Any]]]]] = None,
        maximum_activation_duration: typing.Optional[builtins.str] = None,
        multi_factor_auth_provider: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param approver: approver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#approver LighthouseDefinition#approver}
        :param maximum_activation_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#maximum_activation_duration LighthouseDefinition#maximum_activation_duration}.
        :param multi_factor_auth_provider: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#multi_factor_auth_provider LighthouseDefinition#multi_factor_auth_provider}.
        '''
        value = LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicy(
            approver=approver,
            maximum_activation_duration=maximum_activation_duration,
            multi_factor_auth_provider=multi_factor_auth_provider,
        )

        return typing.cast(None, jsii.invoke(self, "putJustInTimeAccessPolicy", [value]))

    @jsii.member(jsii_name="resetJustInTimeAccessPolicy")
    def reset_just_in_time_access_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJustInTimeAccessPolicy", []))

    @jsii.member(jsii_name="resetPrincipalDisplayName")
    def reset_principal_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrincipalDisplayName", []))

    @builtins.property
    @jsii.member(jsii_name="justInTimeAccessPolicy")
    def just_in_time_access_policy(
        self,
    ) -> LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyOutputReference:
        return typing.cast(LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyOutputReference, jsii.get(self, "justInTimeAccessPolicy"))

    @builtins.property
    @jsii.member(jsii_name="justInTimeAccessPolicyInput")
    def just_in_time_access_policy_input(
        self,
    ) -> typing.Optional[LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicy]:
        return typing.cast(typing.Optional[LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicy], jsii.get(self, "justInTimeAccessPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="principalDisplayNameInput")
    def principal_display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalDisplayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="principalIdInput")
    def principal_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalIdInput"))

    @builtins.property
    @jsii.member(jsii_name="roleDefinitionIdInput")
    def role_definition_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleDefinitionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="principalDisplayName")
    def principal_display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalDisplayName"))

    @principal_display_name.setter
    def principal_display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bd7383e5aeb5120db0190666c48f280bf2543adb243bf800176859bcd4bb071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principalDisplayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @principal_id.setter
    def principal_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22d0061a4a0a7dd84cc0e9ae2a9f2c69bc1c047b437c902120b2e4fb40f7dc75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principalId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleDefinitionId")
    def role_definition_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleDefinitionId"))

    @role_definition_id.setter
    def role_definition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4d5933a5d461fa110bac37cb4b6d8eb3e68cc951137c4525e58002001668a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleDefinitionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LighthouseDefinitionEligibleAuthorization]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LighthouseDefinitionEligibleAuthorization]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LighthouseDefinitionEligibleAuthorization]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b19520f671f2a1aa7b3435d7e6219f1609c92517ce0135e023d0fca929016fea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.lighthouseDefinition.LighthouseDefinitionPlan",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "product": "product",
        "publisher": "publisher",
        "version": "version",
    },
)
class LighthouseDefinitionPlan:
    def __init__(
        self,
        *,
        name: builtins.str,
        product: builtins.str,
        publisher: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#name LighthouseDefinition#name}.
        :param product: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#product LighthouseDefinition#product}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#publisher LighthouseDefinition#publisher}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#version LighthouseDefinition#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6db2dc42c00ab4aa6b5653971ef3631906cb56325e8a6e2e09b02326a347e3d2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "product": product,
            "publisher": publisher,
            "version": version,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#name LighthouseDefinition#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#product LighthouseDefinition#product}.'''
        result = self._values.get("product")
        assert result is not None, "Required property 'product' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def publisher(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#publisher LighthouseDefinition#publisher}.'''
        result = self._values.get("publisher")
        assert result is not None, "Required property 'publisher' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#version LighthouseDefinition#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LighthouseDefinitionPlan(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LighthouseDefinitionPlanOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.lighthouseDefinition.LighthouseDefinitionPlanOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6550e7c32ee12d2e7dde43ba57fd365debb7b223b3ed73b9ec143724fb1bcb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="productInput")
    def product_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "productInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherInput")
    def publisher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4edb9b9eda37cd388252fb709dcbe1b9f65509755eb58a80211cf62a8302959)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="product")
    def product(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "product"))

    @product.setter
    def product(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9976be7284f4ab13aea99b32cd25635f4f05bfa0a0d3ad07f204656351030307)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "product", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisher"))

    @publisher.setter
    def publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95d055ea31a8997b92e09bafe5bab7840a4415b75ab695c84069130e26c99598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398c235380d7184b048e328fe83832cd7778f0a1cc9f7bc637791cfdeea5ee56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LighthouseDefinitionPlan]:
        return typing.cast(typing.Optional[LighthouseDefinitionPlan], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LighthouseDefinitionPlan]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de69f2a7aa9fc8fe9079461dd982e20ea3773e233a5e4d07cffae39873bb1a48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.lighthouseDefinition.LighthouseDefinitionTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class LighthouseDefinitionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#create LighthouseDefinition#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#delete LighthouseDefinition#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#read LighthouseDefinition#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#update LighthouseDefinition#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69773abaa35a6e7153427695bb264e565feaa8b680b62da57929086c523f5ca4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#create LighthouseDefinition#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#delete LighthouseDefinition#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#read LighthouseDefinition#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/lighthouse_definition#update LighthouseDefinition#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LighthouseDefinitionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LighthouseDefinitionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.lighthouseDefinition.LighthouseDefinitionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6a8fac83c2a6f23e5678561628ca4ea454916dee2d1d35439c19ded681aae65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4d1371bf9f64b1f4a07531c93d027b1665233a254e0aabc09199abc87e234a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaa0bb63c5e2d0ccf4f84a990b18db70408cc0d1328300bb539e524fa3f3a643)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbc7f7e1516c19ff16e935230aa4fef2111fbb9881fcc3690dab723abe1771c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb985f15f281fab01f5d46508e1e08aed1e7cbff6fb57f41d369d88b5a03d642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LighthouseDefinitionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LighthouseDefinitionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LighthouseDefinitionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65954935338aeaab0615262e5b9d7d843848fd1fff1b69aaaac3c7fa8f43281a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LighthouseDefinition",
    "LighthouseDefinitionAuthorization",
    "LighthouseDefinitionAuthorizationList",
    "LighthouseDefinitionAuthorizationOutputReference",
    "LighthouseDefinitionConfig",
    "LighthouseDefinitionEligibleAuthorization",
    "LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicy",
    "LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover",
    "LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApproverList",
    "LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApproverOutputReference",
    "LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyOutputReference",
    "LighthouseDefinitionEligibleAuthorizationList",
    "LighthouseDefinitionEligibleAuthorizationOutputReference",
    "LighthouseDefinitionPlan",
    "LighthouseDefinitionPlanOutputReference",
    "LighthouseDefinitionTimeouts",
    "LighthouseDefinitionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d802e9a1ffecf069954f844072e4d8854e297140bdda1f229d1ebb42de59d469(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    authorization: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LighthouseDefinitionAuthorization, typing.Dict[builtins.str, typing.Any]]]],
    managing_tenant_id: builtins.str,
    name: builtins.str,
    scope: builtins.str,
    description: typing.Optional[builtins.str] = None,
    eligible_authorization: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LighthouseDefinitionEligibleAuthorization, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    lighthouse_definition_id: typing.Optional[builtins.str] = None,
    plan: typing.Optional[typing.Union[LighthouseDefinitionPlan, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[LighthouseDefinitionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a21ccce1aed9dac40851fbe742a647406c8dc53fa6f01492e27d3484b7268092(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5120685bb5f3eb213aa5dee36eec0cf9a76b8e54ad77707042bd9245f17484b4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LighthouseDefinitionAuthorization, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba5ef15899e5048967bc3e812daf4ebd3c5997d20af25e8121c9d9799040361b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LighthouseDefinitionEligibleAuthorization, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0db530aa1cdda0778b432166625e2fdcdf60b67556877197d8aeaf8b2e10632(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f08be2d4d7c4959e0fb5a7fbd7411df2a932271da94a34f9301b94ff0f91170(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08873c384960a675e5de631ceda6b3c6267ffc50fb91a857b2e3765e12b544e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db19bf8ae347cc4454a58da559c682dd4208db73c44c68c89fd58e0883de3c0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3bb489bd8cd6b030ac9372b2dccfc8be1149c6606580c16a6a8cf154c52c579(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a123068c16ec09394c4231119f4691983848d477d5bfe40033cc2f13ad98b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc5cd3734149ea82a8cd004fb301783d31a4bf1fa3edac605e734141fb836ec(
    *,
    principal_id: builtins.str,
    role_definition_id: builtins.str,
    delegated_role_definition_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b524afa73dca674c1a23a5f70eb24ef00ae0eb19156b8f4b94be87fc3689149b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb1434bd82334a8604228551c57483979842d7d3ca81103c9720bdd6af3c3965(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__726f1b90dcb4889d72976ce0d1021651bb2de925ad71ed283d7d6972508309db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32856543cb85b8b295a25e753357df7504f30363979dea82f15cde1c3a619f9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e65c69f248bd4c4f10f55b41f7b142a9f8a4f2a6c0255b39db82132392d30062(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1bc9d0d81d832085d4477e96e591958ef87db4870857080fbc64e19b456a9f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LighthouseDefinitionAuthorization]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2552540e2c8dbe02dfc626385120afd3a0b41cc491318a4bb59127298a826ef5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5dd3a18f4876ac9e84337540af6076fa42c3f682ce9feb89b665f02ba26f36e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5234e3cb113f82bf200d2a03f4b488b381f9eed28fd1bdc0e0bbc26b2881926a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31df6b68ca8664c67c3b89198551243b2b86bed7a36b492ac3ca89435d23fddb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a8ebefd883e7e602e22fb57f50cd7b83210685a02c8700532d4d63383b25d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe17a89feb02a443bb47ba1053a49d104dcbd2bcebdc6d3dbc393f557b30395(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LighthouseDefinitionAuthorization]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ecf8963fa1ae16ab003bc6c5465bb8c244d2b62a750d58e4d6765c1862c9af7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    authorization: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LighthouseDefinitionAuthorization, typing.Dict[builtins.str, typing.Any]]]],
    managing_tenant_id: builtins.str,
    name: builtins.str,
    scope: builtins.str,
    description: typing.Optional[builtins.str] = None,
    eligible_authorization: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LighthouseDefinitionEligibleAuthorization, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    lighthouse_definition_id: typing.Optional[builtins.str] = None,
    plan: typing.Optional[typing.Union[LighthouseDefinitionPlan, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[LighthouseDefinitionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b80e7bd67a25ab7a8557d399b50fe5c87f80cacca76333fd96e92d596ff644a6(
    *,
    principal_id: builtins.str,
    role_definition_id: builtins.str,
    just_in_time_access_policy: typing.Optional[typing.Union[LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    principal_display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d5824dba04702d36db95bc95190d27c8d197f8d63866d6564633e5e4987001(
    *,
    approver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover, typing.Dict[builtins.str, typing.Any]]]]] = None,
    maximum_activation_duration: typing.Optional[builtins.str] = None,
    multi_factor_auth_provider: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4f2e6b4299d5beae745afde767d82f69daf5404b52ca34cf5aabafe9a30077(
    *,
    principal_id: builtins.str,
    principal_display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85fb47cff47f43904a8056309dddda068addeeaad87e08c8b576fedde9710b78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bcbe029051787dc67a8bb88d6b1f4d746d77b30a5cb3e5a2bd4b642b5077c33(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4082fb4ec1883fd553a4ec3a767b05c69d394b997d86d20538f7cdc444a86c05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7c6bb07ca40954f2aedee3cd4a067f76d81fbba7a4c67f041d21300a0bdd51(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b91f7c289f8b6bd3f4baa5eee5919ade778313edde88e0173d75776e6bb320(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e3445bf9772e6ff1eb59616cd27cffda87af2daa6dfeb79ce7f531af307bb3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfa9e17667eae2aaae6868999a11cd87660564fa8cede4d7ea995e195fa1d4d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9f40440ebb3f639eef287397cc79392fed7ab779e92d13a488dc82e2068957(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70bd1b4e32027916cc8dc8d26156090c53b7c92e08d01b8c8ef5fd64fc2cbf1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae820d4ff83a35b0cf9ece54b77a56299f68a14b8c7636f99aa19ed382d8365(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e989c82dbf6004a08d56bef3f1ce69bb9c0f3090a33079bb96cbad9cbb1aac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8cf9e9cf867c73aabecc7b25f7528afe58606b042eb9aa3908931af50834a8a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicyApprover, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea5ccd2f50875867d0db4c2a11e0d7a8982c8004a6fd82fdaf4922b04b1bbce7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0c3ac890354d5720e598b0a6bf31951275dcd12e60efbb06a23415e78f8e90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd580685343430e40d6303d10d3ddf7aafc9d08fbdc0cb8c7b9d4c0d46452c3d(
    value: typing.Optional[LighthouseDefinitionEligibleAuthorizationJustInTimeAccessPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c35becee0adcbeb9ca0371a744f70c5fe347300ed42b2df66ae78150790e625(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36f4be2505ae3d1b961021183e7447125b17cc0ca9204e640abd3a7b6098a0e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6cb04a3bd0fb61f771d91546d47e8a7f0e300d94a5b22fecad3619a2c624e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056cac3386cc90a274469b242b7e77b665372a041272963cc49542319ed73bf2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf38eb6e8e92efc3f9f2164645253cd57ee2384caf3d6b4db7ad13b48aa9156(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1dfd519d73b782c46969304ea2803dc26afd7e86a18a993f782ed83adb4a58c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LighthouseDefinitionEligibleAuthorization]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa52617f656cc639449b505fe5e6300e5029ca6172802198b32b7318779990b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd7383e5aeb5120db0190666c48f280bf2543adb243bf800176859bcd4bb071(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d0061a4a0a7dd84cc0e9ae2a9f2c69bc1c047b437c902120b2e4fb40f7dc75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4d5933a5d461fa110bac37cb4b6d8eb3e68cc951137c4525e58002001668a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b19520f671f2a1aa7b3435d7e6219f1609c92517ce0135e023d0fca929016fea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LighthouseDefinitionEligibleAuthorization]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db2dc42c00ab4aa6b5653971ef3631906cb56325e8a6e2e09b02326a347e3d2(
    *,
    name: builtins.str,
    product: builtins.str,
    publisher: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6550e7c32ee12d2e7dde43ba57fd365debb7b223b3ed73b9ec143724fb1bcb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4edb9b9eda37cd388252fb709dcbe1b9f65509755eb58a80211cf62a8302959(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9976be7284f4ab13aea99b32cd25635f4f05bfa0a0d3ad07f204656351030307(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d055ea31a8997b92e09bafe5bab7840a4415b75ab695c84069130e26c99598(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398c235380d7184b048e328fe83832cd7778f0a1cc9f7bc637791cfdeea5ee56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de69f2a7aa9fc8fe9079461dd982e20ea3773e233a5e4d07cffae39873bb1a48(
    value: typing.Optional[LighthouseDefinitionPlan],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69773abaa35a6e7153427695bb264e565feaa8b680b62da57929086c523f5ca4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a8fac83c2a6f23e5678561628ca4ea454916dee2d1d35439c19ded681aae65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d1371bf9f64b1f4a07531c93d027b1665233a254e0aabc09199abc87e234a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa0bb63c5e2d0ccf4f84a990b18db70408cc0d1328300bb539e524fa3f3a643(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbc7f7e1516c19ff16e935230aa4fef2111fbb9881fcc3690dab723abe1771c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb985f15f281fab01f5d46508e1e08aed1e7cbff6fb57f41d369d88b5a03d642(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65954935338aeaab0615262e5b9d7d843848fd1fff1b69aaaac3c7fa8f43281a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LighthouseDefinitionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

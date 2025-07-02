r'''
# `azurerm_api_management_custom_domain`

Refer to the Terraform Registry for docs: [`azurerm_api_management_custom_domain`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain).
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


class ApiManagementCustomDomain(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomain",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain azurerm_api_management_custom_domain}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        api_management_id: builtins.str,
        developer_portal: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementCustomDomainDeveloperPortal", typing.Dict[builtins.str, typing.Any]]]]] = None,
        gateway: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementCustomDomainGateway", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        management: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementCustomDomainManagement", typing.Dict[builtins.str, typing.Any]]]]] = None,
        portal: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementCustomDomainPortal", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scm: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementCustomDomainScm", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["ApiManagementCustomDomainTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain azurerm_api_management_custom_domain} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_management_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#api_management_id ApiManagementCustomDomain#api_management_id}.
        :param developer_portal: developer_portal block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#developer_portal ApiManagementCustomDomain#developer_portal}
        :param gateway: gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#gateway ApiManagementCustomDomain#gateway}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#id ApiManagementCustomDomain#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param management: management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#management ApiManagementCustomDomain#management}
        :param portal: portal block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#portal ApiManagementCustomDomain#portal}
        :param scm: scm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#scm ApiManagementCustomDomain#scm}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#timeouts ApiManagementCustomDomain#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9caf6ce4cef0ec185150e9a4060c35b5665c1d204da62bcd61e1782525c1273f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApiManagementCustomDomainConfig(
            api_management_id=api_management_id,
            developer_portal=developer_portal,
            gateway=gateway,
            id=id,
            management=management,
            portal=portal,
            scm=scm,
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
        '''Generates CDKTF code for importing a ApiManagementCustomDomain resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApiManagementCustomDomain to import.
        :param import_from_id: The id of the existing ApiManagementCustomDomain that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApiManagementCustomDomain to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0446830050a1b57b42ab5891f20916ead11ecd69315e6c8c6507881dd9344d95)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDeveloperPortal")
    def put_developer_portal(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementCustomDomainDeveloperPortal", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c59a5bba7e7a19e284f36f8e2a3367b394110acfd87993f9299981f42f775c3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeveloperPortal", [value]))

    @jsii.member(jsii_name="putGateway")
    def put_gateway(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementCustomDomainGateway", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3761930e66c603cfabd65ad9454e54601ce0e021a858b9a3a4539d0489b1f17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGateway", [value]))

    @jsii.member(jsii_name="putManagement")
    def put_management(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementCustomDomainManagement", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea0c5dbb88dc83c842faf61a6efb0dd7abbaa6a20f529d91266b25d35023252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putManagement", [value]))

    @jsii.member(jsii_name="putPortal")
    def put_portal(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementCustomDomainPortal", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecfae0e2c35563a7261b3c4e35ab6a0c835c7c3f72bddb9449b347c7595098af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPortal", [value]))

    @jsii.member(jsii_name="putScm")
    def put_scm(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementCustomDomainScm", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668a06c308eef12556820cc43856700521fff74ea0f773f9e0ecb8be1aa1b862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScm", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#create ApiManagementCustomDomain#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#delete ApiManagementCustomDomain#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#read ApiManagementCustomDomain#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#update ApiManagementCustomDomain#update}.
        '''
        value = ApiManagementCustomDomainTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDeveloperPortal")
    def reset_developer_portal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeveloperPortal", []))

    @jsii.member(jsii_name="resetGateway")
    def reset_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGateway", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetManagement")
    def reset_management(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagement", []))

    @jsii.member(jsii_name="resetPortal")
    def reset_portal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortal", []))

    @jsii.member(jsii_name="resetScm")
    def reset_scm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScm", []))

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
    @jsii.member(jsii_name="developerPortal")
    def developer_portal(self) -> "ApiManagementCustomDomainDeveloperPortalList":
        return typing.cast("ApiManagementCustomDomainDeveloperPortalList", jsii.get(self, "developerPortal"))

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> "ApiManagementCustomDomainGatewayList":
        return typing.cast("ApiManagementCustomDomainGatewayList", jsii.get(self, "gateway"))

    @builtins.property
    @jsii.member(jsii_name="management")
    def management(self) -> "ApiManagementCustomDomainManagementList":
        return typing.cast("ApiManagementCustomDomainManagementList", jsii.get(self, "management"))

    @builtins.property
    @jsii.member(jsii_name="portal")
    def portal(self) -> "ApiManagementCustomDomainPortalList":
        return typing.cast("ApiManagementCustomDomainPortalList", jsii.get(self, "portal"))

    @builtins.property
    @jsii.member(jsii_name="scm")
    def scm(self) -> "ApiManagementCustomDomainScmList":
        return typing.cast("ApiManagementCustomDomainScmList", jsii.get(self, "scm"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApiManagementCustomDomainTimeoutsOutputReference":
        return typing.cast("ApiManagementCustomDomainTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="apiManagementIdInput")
    def api_management_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiManagementIdInput"))

    @builtins.property
    @jsii.member(jsii_name="developerPortalInput")
    def developer_portal_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainDeveloperPortal"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainDeveloperPortal"]]], jsii.get(self, "developerPortalInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainGateway"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainGateway"]]], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="managementInput")
    def management_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainManagement"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainManagement"]]], jsii.get(self, "managementInput"))

    @builtins.property
    @jsii.member(jsii_name="portalInput")
    def portal_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainPortal"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainPortal"]]], jsii.get(self, "portalInput"))

    @builtins.property
    @jsii.member(jsii_name="scmInput")
    def scm_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainScm"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainScm"]]], jsii.get(self, "scmInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApiManagementCustomDomainTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApiManagementCustomDomainTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="apiManagementId")
    def api_management_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiManagementId"))

    @api_management_id.setter
    def api_management_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9298ebeeba6ad71251ccca738eccf5f84f3d90bdcd9d806a58729adb003d88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiManagementId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50fe38bb4fad8ad7e5361eb27ea91c3434f26b1b0d563021a44d1bf24c17218c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "api_management_id": "apiManagementId",
        "developer_portal": "developerPortal",
        "gateway": "gateway",
        "id": "id",
        "management": "management",
        "portal": "portal",
        "scm": "scm",
        "timeouts": "timeouts",
    },
)
class ApiManagementCustomDomainConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        api_management_id: builtins.str,
        developer_portal: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementCustomDomainDeveloperPortal", typing.Dict[builtins.str, typing.Any]]]]] = None,
        gateway: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementCustomDomainGateway", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        management: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementCustomDomainManagement", typing.Dict[builtins.str, typing.Any]]]]] = None,
        portal: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementCustomDomainPortal", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scm: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementCustomDomainScm", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["ApiManagementCustomDomainTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param api_management_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#api_management_id ApiManagementCustomDomain#api_management_id}.
        :param developer_portal: developer_portal block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#developer_portal ApiManagementCustomDomain#developer_portal}
        :param gateway: gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#gateway ApiManagementCustomDomain#gateway}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#id ApiManagementCustomDomain#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param management: management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#management ApiManagementCustomDomain#management}
        :param portal: portal block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#portal ApiManagementCustomDomain#portal}
        :param scm: scm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#scm ApiManagementCustomDomain#scm}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#timeouts ApiManagementCustomDomain#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ApiManagementCustomDomainTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a7e6d03296cdb652dda1d79a95992b3d153829472cbd957274b12363e08815b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument api_management_id", value=api_management_id, expected_type=type_hints["api_management_id"])
            check_type(argname="argument developer_portal", value=developer_portal, expected_type=type_hints["developer_portal"])
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument management", value=management, expected_type=type_hints["management"])
            check_type(argname="argument portal", value=portal, expected_type=type_hints["portal"])
            check_type(argname="argument scm", value=scm, expected_type=type_hints["scm"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_management_id": api_management_id,
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
        if developer_portal is not None:
            self._values["developer_portal"] = developer_portal
        if gateway is not None:
            self._values["gateway"] = gateway
        if id is not None:
            self._values["id"] = id
        if management is not None:
            self._values["management"] = management
        if portal is not None:
            self._values["portal"] = portal
        if scm is not None:
            self._values["scm"] = scm
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
    def api_management_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#api_management_id ApiManagementCustomDomain#api_management_id}.'''
        result = self._values.get("api_management_id")
        assert result is not None, "Required property 'api_management_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def developer_portal(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainDeveloperPortal"]]]:
        '''developer_portal block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#developer_portal ApiManagementCustomDomain#developer_portal}
        '''
        result = self._values.get("developer_portal")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainDeveloperPortal"]]], result)

    @builtins.property
    def gateway(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainGateway"]]]:
        '''gateway block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#gateway ApiManagementCustomDomain#gateway}
        '''
        result = self._values.get("gateway")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainGateway"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#id ApiManagementCustomDomain#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def management(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainManagement"]]]:
        '''management block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#management ApiManagementCustomDomain#management}
        '''
        result = self._values.get("management")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainManagement"]]], result)

    @builtins.property
    def portal(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainPortal"]]]:
        '''portal block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#portal ApiManagementCustomDomain#portal}
        '''
        result = self._values.get("portal")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainPortal"]]], result)

    @builtins.property
    def scm(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainScm"]]]:
        '''scm block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#scm ApiManagementCustomDomain#scm}
        '''
        result = self._values.get("scm")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementCustomDomainScm"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApiManagementCustomDomainTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#timeouts ApiManagementCustomDomain#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApiManagementCustomDomainTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementCustomDomainConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainDeveloperPortal",
    jsii_struct_bases=[],
    name_mapping={
        "host_name": "hostName",
        "certificate": "certificate",
        "certificate_password": "certificatePassword",
        "key_vault_certificate_id": "keyVaultCertificateId",
        "key_vault_id": "keyVaultId",
        "negotiate_client_certificate": "negotiateClientCertificate",
        "ssl_keyvault_identity_client_id": "sslKeyvaultIdentityClientId",
    },
)
class ApiManagementCustomDomainDeveloperPortal:
    def __init__(
        self,
        *,
        host_name: builtins.str,
        certificate: typing.Optional[builtins.str] = None,
        certificate_password: typing.Optional[builtins.str] = None,
        key_vault_certificate_id: typing.Optional[builtins.str] = None,
        key_vault_id: typing.Optional[builtins.str] = None,
        negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#host_name ApiManagementCustomDomain#host_name}.
        :param certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate ApiManagementCustomDomain#certificate}.
        :param certificate_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate_password ApiManagementCustomDomain#certificate_password}.
        :param key_vault_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_certificate_id ApiManagementCustomDomain#key_vault_certificate_id}.
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_id ApiManagementCustomDomain#key_vault_id}.
        :param negotiate_client_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#negotiate_client_certificate ApiManagementCustomDomain#negotiate_client_certificate}.
        :param ssl_keyvault_identity_client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#ssl_keyvault_identity_client_id ApiManagementCustomDomain#ssl_keyvault_identity_client_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731dd8c12498f4895fe15fa11b5337c5c0324c0f7a1819c44637478aaad438d3)
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument certificate_password", value=certificate_password, expected_type=type_hints["certificate_password"])
            check_type(argname="argument key_vault_certificate_id", value=key_vault_certificate_id, expected_type=type_hints["key_vault_certificate_id"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument negotiate_client_certificate", value=negotiate_client_certificate, expected_type=type_hints["negotiate_client_certificate"])
            check_type(argname="argument ssl_keyvault_identity_client_id", value=ssl_keyvault_identity_client_id, expected_type=type_hints["ssl_keyvault_identity_client_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_name": host_name,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if certificate_password is not None:
            self._values["certificate_password"] = certificate_password
        if key_vault_certificate_id is not None:
            self._values["key_vault_certificate_id"] = key_vault_certificate_id
        if key_vault_id is not None:
            self._values["key_vault_id"] = key_vault_id
        if negotiate_client_certificate is not None:
            self._values["negotiate_client_certificate"] = negotiate_client_certificate
        if ssl_keyvault_identity_client_id is not None:
            self._values["ssl_keyvault_identity_client_id"] = ssl_keyvault_identity_client_id

    @builtins.property
    def host_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#host_name ApiManagementCustomDomain#host_name}.'''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate ApiManagementCustomDomain#certificate}.'''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate_password ApiManagementCustomDomain#certificate_password}.'''
        result = self._values.get("certificate_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_certificate_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_certificate_id ApiManagementCustomDomain#key_vault_certificate_id}.'''
        result = self._values.get("key_vault_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_id ApiManagementCustomDomain#key_vault_id}.'''
        result = self._values.get("key_vault_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negotiate_client_certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#negotiate_client_certificate ApiManagementCustomDomain#negotiate_client_certificate}.'''
        result = self._values.get("negotiate_client_certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssl_keyvault_identity_client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#ssl_keyvault_identity_client_id ApiManagementCustomDomain#ssl_keyvault_identity_client_id}.'''
        result = self._values.get("ssl_keyvault_identity_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementCustomDomainDeveloperPortal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementCustomDomainDeveloperPortalList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainDeveloperPortalList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0fd60e9f138fdc486cca785ea0617e756ab26bb9efb62733797774f9796d1e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementCustomDomainDeveloperPortalOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d036cfa859c646b83f847ada566b57e16cf1d018074ff378be202c96cfd259c2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementCustomDomainDeveloperPortalOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9208983d08673131605a987d7a8051d8d6140203a516f514a0be1f1538c1540)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9737c342331517f0f8094eac5a291018cba38abcd832b1fd1fce2cf28900872)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0030fd36aef993c52024e89f01055dd319189846e019a7836f045bede63fcd2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainDeveloperPortal]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainDeveloperPortal]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainDeveloperPortal]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c2327e4cab9538a8d6745f22013dacdeb78fd12c6df8b2aebc082b28e00a43c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementCustomDomainDeveloperPortalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainDeveloperPortalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5e8a7150877cdcde15de8da50af1aa66358b162eb5a222c9a03eade653e52ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetCertificatePassword")
    def reset_certificate_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificatePassword", []))

    @jsii.member(jsii_name="resetKeyVaultCertificateId")
    def reset_key_vault_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultCertificateId", []))

    @jsii.member(jsii_name="resetKeyVaultId")
    def reset_key_vault_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultId", []))

    @jsii.member(jsii_name="resetNegotiateClientCertificate")
    def reset_negotiate_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegotiateClientCertificate", []))

    @jsii.member(jsii_name="resetSslKeyvaultIdentityClientId")
    def reset_ssl_keyvault_identity_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslKeyvaultIdentityClientId", []))

    @builtins.property
    @jsii.member(jsii_name="certificateSource")
    def certificate_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateSource"))

    @builtins.property
    @jsii.member(jsii_name="certificateStatus")
    def certificate_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateStatus"))

    @builtins.property
    @jsii.member(jsii_name="expiry")
    def expiry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiry"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="certificatePasswordInput")
    def certificate_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificatePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateIdInput")
    def key_vault_certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultCertificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultIdInput")
    def key_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificateInput")
    def negotiate_client_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negotiateClientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientIdInput")
    def ssl_keyvault_identity_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslKeyvaultIdentityClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5050a3ea99fa1822182e88acd43baf413893aa232911c0506306754f9b33e75b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificatePassword")
    def certificate_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificatePassword"))

    @certificate_password.setter
    def certificate_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b871fdb3cd49081baea8df08899d9942d05cbbc0b63622b7124d6c708ce14f1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificatePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b7c8c7afa842f2ff815d0cc9a146036fe67f7d01fe3f59f8791a9fc41cb685e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateId")
    def key_vault_certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultCertificateId"))

    @key_vault_certificate_id.setter
    def key_vault_certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3ec0dabc26b78e6c801f2d2e00595e5d880872eb40e948c7b03f9a7da7c61e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultCertificateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultId")
    def key_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultId"))

    @key_vault_id.setter
    def key_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e064e8b49b906c393cabfebbe928dff5d0b9542a2be0644083368ebdf7cc97cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificate")
    def negotiate_client_certificate(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negotiateClientCertificate"))

    @negotiate_client_certificate.setter
    def negotiate_client_certificate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a477cac98d1c08c9322e97a2d1ed1723f8cb33347ee17c52353b159cf293d05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negotiateClientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientId")
    def ssl_keyvault_identity_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslKeyvaultIdentityClientId"))

    @ssl_keyvault_identity_client_id.setter
    def ssl_keyvault_identity_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760072a2156ec5b4360903ab9f39e2648d7a505e353b801d1ca5a54301ca2aa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslKeyvaultIdentityClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainDeveloperPortal]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainDeveloperPortal]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainDeveloperPortal]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95099509ba41c07fc3e7f3aed541b472fb9c79bf8cdba6c86f0fded250c80265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainGateway",
    jsii_struct_bases=[],
    name_mapping={
        "host_name": "hostName",
        "certificate": "certificate",
        "certificate_password": "certificatePassword",
        "default_ssl_binding": "defaultSslBinding",
        "key_vault_certificate_id": "keyVaultCertificateId",
        "key_vault_id": "keyVaultId",
        "negotiate_client_certificate": "negotiateClientCertificate",
        "ssl_keyvault_identity_client_id": "sslKeyvaultIdentityClientId",
    },
)
class ApiManagementCustomDomainGateway:
    def __init__(
        self,
        *,
        host_name: builtins.str,
        certificate: typing.Optional[builtins.str] = None,
        certificate_password: typing.Optional[builtins.str] = None,
        default_ssl_binding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_vault_certificate_id: typing.Optional[builtins.str] = None,
        key_vault_id: typing.Optional[builtins.str] = None,
        negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#host_name ApiManagementCustomDomain#host_name}.
        :param certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate ApiManagementCustomDomain#certificate}.
        :param certificate_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate_password ApiManagementCustomDomain#certificate_password}.
        :param default_ssl_binding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#default_ssl_binding ApiManagementCustomDomain#default_ssl_binding}.
        :param key_vault_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_certificate_id ApiManagementCustomDomain#key_vault_certificate_id}.
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_id ApiManagementCustomDomain#key_vault_id}.
        :param negotiate_client_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#negotiate_client_certificate ApiManagementCustomDomain#negotiate_client_certificate}.
        :param ssl_keyvault_identity_client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#ssl_keyvault_identity_client_id ApiManagementCustomDomain#ssl_keyvault_identity_client_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c281634f087311cc558e2e6ec3c9952be8b2eab48323c38cdb3a61bf1927c85c)
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument certificate_password", value=certificate_password, expected_type=type_hints["certificate_password"])
            check_type(argname="argument default_ssl_binding", value=default_ssl_binding, expected_type=type_hints["default_ssl_binding"])
            check_type(argname="argument key_vault_certificate_id", value=key_vault_certificate_id, expected_type=type_hints["key_vault_certificate_id"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument negotiate_client_certificate", value=negotiate_client_certificate, expected_type=type_hints["negotiate_client_certificate"])
            check_type(argname="argument ssl_keyvault_identity_client_id", value=ssl_keyvault_identity_client_id, expected_type=type_hints["ssl_keyvault_identity_client_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_name": host_name,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if certificate_password is not None:
            self._values["certificate_password"] = certificate_password
        if default_ssl_binding is not None:
            self._values["default_ssl_binding"] = default_ssl_binding
        if key_vault_certificate_id is not None:
            self._values["key_vault_certificate_id"] = key_vault_certificate_id
        if key_vault_id is not None:
            self._values["key_vault_id"] = key_vault_id
        if negotiate_client_certificate is not None:
            self._values["negotiate_client_certificate"] = negotiate_client_certificate
        if ssl_keyvault_identity_client_id is not None:
            self._values["ssl_keyvault_identity_client_id"] = ssl_keyvault_identity_client_id

    @builtins.property
    def host_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#host_name ApiManagementCustomDomain#host_name}.'''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate ApiManagementCustomDomain#certificate}.'''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate_password ApiManagementCustomDomain#certificate_password}.'''
        result = self._values.get("certificate_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_ssl_binding(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#default_ssl_binding ApiManagementCustomDomain#default_ssl_binding}.'''
        result = self._values.get("default_ssl_binding")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_vault_certificate_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_certificate_id ApiManagementCustomDomain#key_vault_certificate_id}.'''
        result = self._values.get("key_vault_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_id ApiManagementCustomDomain#key_vault_id}.'''
        result = self._values.get("key_vault_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negotiate_client_certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#negotiate_client_certificate ApiManagementCustomDomain#negotiate_client_certificate}.'''
        result = self._values.get("negotiate_client_certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssl_keyvault_identity_client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#ssl_keyvault_identity_client_id ApiManagementCustomDomain#ssl_keyvault_identity_client_id}.'''
        result = self._values.get("ssl_keyvault_identity_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementCustomDomainGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementCustomDomainGatewayList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainGatewayList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b060f7519133b2c312e22e790f263cb3368cd1a5afe0f037c6465785ef740fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementCustomDomainGatewayOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f8f273cd9f6f498d2367a6b18bbe918740ef37c69ded04270cd2bc4233a1ea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementCustomDomainGatewayOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58601de5fc0dea4ad5a38e7008402fdb9eebc7a406f6962fd9c42fa8ebdfd55e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d52c4de18e672631792402f76aab11f7fd8b8fc417a1a594e652dcb2d6f60ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8400ea41f5f458db97ef4ef2bd5763165b2230dc72ccc4939b407ea5e8f94ac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainGateway]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainGateway]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainGateway]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b336182ef2bccc318e68546063b6bdb8aa387cff1bae77f52c5882967f7f9fd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementCustomDomainGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainGatewayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f71cb37e5a5111ef2cb9a8b1b071b7f59cf3310716bce855243a80445cb9c2e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetCertificatePassword")
    def reset_certificate_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificatePassword", []))

    @jsii.member(jsii_name="resetDefaultSslBinding")
    def reset_default_ssl_binding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultSslBinding", []))

    @jsii.member(jsii_name="resetKeyVaultCertificateId")
    def reset_key_vault_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultCertificateId", []))

    @jsii.member(jsii_name="resetKeyVaultId")
    def reset_key_vault_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultId", []))

    @jsii.member(jsii_name="resetNegotiateClientCertificate")
    def reset_negotiate_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegotiateClientCertificate", []))

    @jsii.member(jsii_name="resetSslKeyvaultIdentityClientId")
    def reset_ssl_keyvault_identity_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslKeyvaultIdentityClientId", []))

    @builtins.property
    @jsii.member(jsii_name="certificateSource")
    def certificate_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateSource"))

    @builtins.property
    @jsii.member(jsii_name="certificateStatus")
    def certificate_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateStatus"))

    @builtins.property
    @jsii.member(jsii_name="expiry")
    def expiry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiry"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="certificatePasswordInput")
    def certificate_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificatePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultSslBindingInput")
    def default_ssl_binding_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultSslBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateIdInput")
    def key_vault_certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultCertificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultIdInput")
    def key_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificateInput")
    def negotiate_client_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negotiateClientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientIdInput")
    def ssl_keyvault_identity_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslKeyvaultIdentityClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eabc43c4bc303b438a56268225fccf7da6b7b10958067ee04b67583bec78110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificatePassword")
    def certificate_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificatePassword"))

    @certificate_password.setter
    def certificate_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e30cdc5520f3b2fb9e5b2ac6fd034710120f1725c10a1811285aebdaeed4a5a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificatePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultSslBinding")
    def default_ssl_binding(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultSslBinding"))

    @default_ssl_binding.setter
    def default_ssl_binding(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6a25b3320926238318cfaf6ef9b2a85c63ca38832447e9b079f8903144a8d53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSslBinding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0f16d22e70cacc2be198592069d2acafab10727ceabab522c722bc923feabb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateId")
    def key_vault_certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultCertificateId"))

    @key_vault_certificate_id.setter
    def key_vault_certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f64c3ce7e4e548570283132fc6be53c56685459dbf00f09d77cba0c4f7e45ab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultCertificateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultId")
    def key_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultId"))

    @key_vault_id.setter
    def key_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c81386a54b0230de39103fc60de60f26ff4822e60a9686e2fa86c68ec5a315a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificate")
    def negotiate_client_certificate(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negotiateClientCertificate"))

    @negotiate_client_certificate.setter
    def negotiate_client_certificate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e823033699fb195357a7d9bf14c60befaffd45fd0a6b427478c72ca9e18ca9f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negotiateClientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientId")
    def ssl_keyvault_identity_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslKeyvaultIdentityClientId"))

    @ssl_keyvault_identity_client_id.setter
    def ssl_keyvault_identity_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8195f95024b34b0007cbe98358fff23d9fff6d36d82bdc777524bb24510a3319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslKeyvaultIdentityClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainGateway]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainGateway]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainGateway]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b9b4823c40964b38612a0086a849e8e52f5465b22edbf223775fc0159f5c666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainManagement",
    jsii_struct_bases=[],
    name_mapping={
        "host_name": "hostName",
        "certificate": "certificate",
        "certificate_password": "certificatePassword",
        "key_vault_certificate_id": "keyVaultCertificateId",
        "key_vault_id": "keyVaultId",
        "negotiate_client_certificate": "negotiateClientCertificate",
        "ssl_keyvault_identity_client_id": "sslKeyvaultIdentityClientId",
    },
)
class ApiManagementCustomDomainManagement:
    def __init__(
        self,
        *,
        host_name: builtins.str,
        certificate: typing.Optional[builtins.str] = None,
        certificate_password: typing.Optional[builtins.str] = None,
        key_vault_certificate_id: typing.Optional[builtins.str] = None,
        key_vault_id: typing.Optional[builtins.str] = None,
        negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#host_name ApiManagementCustomDomain#host_name}.
        :param certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate ApiManagementCustomDomain#certificate}.
        :param certificate_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate_password ApiManagementCustomDomain#certificate_password}.
        :param key_vault_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_certificate_id ApiManagementCustomDomain#key_vault_certificate_id}.
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_id ApiManagementCustomDomain#key_vault_id}.
        :param negotiate_client_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#negotiate_client_certificate ApiManagementCustomDomain#negotiate_client_certificate}.
        :param ssl_keyvault_identity_client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#ssl_keyvault_identity_client_id ApiManagementCustomDomain#ssl_keyvault_identity_client_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__887b666f4e6a367f4d4b26f0b72889e51b4b9b2cd8136b21937b3f8a6c2bb665)
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument certificate_password", value=certificate_password, expected_type=type_hints["certificate_password"])
            check_type(argname="argument key_vault_certificate_id", value=key_vault_certificate_id, expected_type=type_hints["key_vault_certificate_id"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument negotiate_client_certificate", value=negotiate_client_certificate, expected_type=type_hints["negotiate_client_certificate"])
            check_type(argname="argument ssl_keyvault_identity_client_id", value=ssl_keyvault_identity_client_id, expected_type=type_hints["ssl_keyvault_identity_client_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_name": host_name,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if certificate_password is not None:
            self._values["certificate_password"] = certificate_password
        if key_vault_certificate_id is not None:
            self._values["key_vault_certificate_id"] = key_vault_certificate_id
        if key_vault_id is not None:
            self._values["key_vault_id"] = key_vault_id
        if negotiate_client_certificate is not None:
            self._values["negotiate_client_certificate"] = negotiate_client_certificate
        if ssl_keyvault_identity_client_id is not None:
            self._values["ssl_keyvault_identity_client_id"] = ssl_keyvault_identity_client_id

    @builtins.property
    def host_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#host_name ApiManagementCustomDomain#host_name}.'''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate ApiManagementCustomDomain#certificate}.'''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate_password ApiManagementCustomDomain#certificate_password}.'''
        result = self._values.get("certificate_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_certificate_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_certificate_id ApiManagementCustomDomain#key_vault_certificate_id}.'''
        result = self._values.get("key_vault_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_id ApiManagementCustomDomain#key_vault_id}.'''
        result = self._values.get("key_vault_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negotiate_client_certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#negotiate_client_certificate ApiManagementCustomDomain#negotiate_client_certificate}.'''
        result = self._values.get("negotiate_client_certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssl_keyvault_identity_client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#ssl_keyvault_identity_client_id ApiManagementCustomDomain#ssl_keyvault_identity_client_id}.'''
        result = self._values.get("ssl_keyvault_identity_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementCustomDomainManagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementCustomDomainManagementList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainManagementList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03c4e5a1c23b3deb43e83abcc72afb7c6cbe4daaea80ad8ea6d5208ce595ddad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementCustomDomainManagementOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a2598c904cc0f43778b56ba3357a48d6fcf57db6e7e2a9e143d16abe2d3c65)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementCustomDomainManagementOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3e5c3320a53a0575de1364d8b20274dc4838be79a999ba5728f52718fb62d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6537c86319f2c720ba8825b40f8e4320badf81f22dbfd20ef8c2d00624b951c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c68a4e1ad8725a8f431560524453ffea6f74d73c6571e397a59e0783203317b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainManagement]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainManagement]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainManagement]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7e1a7fe0872a91583722bb126cb802b3d4ca1a553e085aef13980a8a247240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementCustomDomainManagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainManagementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65fdc1335ee6541787d8446a1e4c737014c4e13212d2bd28492ee6a07c25fdb5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetCertificatePassword")
    def reset_certificate_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificatePassword", []))

    @jsii.member(jsii_name="resetKeyVaultCertificateId")
    def reset_key_vault_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultCertificateId", []))

    @jsii.member(jsii_name="resetKeyVaultId")
    def reset_key_vault_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultId", []))

    @jsii.member(jsii_name="resetNegotiateClientCertificate")
    def reset_negotiate_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegotiateClientCertificate", []))

    @jsii.member(jsii_name="resetSslKeyvaultIdentityClientId")
    def reset_ssl_keyvault_identity_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslKeyvaultIdentityClientId", []))

    @builtins.property
    @jsii.member(jsii_name="certificateSource")
    def certificate_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateSource"))

    @builtins.property
    @jsii.member(jsii_name="certificateStatus")
    def certificate_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateStatus"))

    @builtins.property
    @jsii.member(jsii_name="expiry")
    def expiry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiry"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="certificatePasswordInput")
    def certificate_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificatePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateIdInput")
    def key_vault_certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultCertificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultIdInput")
    def key_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificateInput")
    def negotiate_client_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negotiateClientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientIdInput")
    def ssl_keyvault_identity_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslKeyvaultIdentityClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3971e15c25b6abf56ab6df84a44a848d419ac23dd66f7ded3386aea719537242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificatePassword")
    def certificate_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificatePassword"))

    @certificate_password.setter
    def certificate_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5765cc85854c2354aa1ee91e456442cfdb139ba4a09c241f2c3c5a3e96119815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificatePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c70ba375ee21812c66c2e659a6233c7c986ed4bd8df3d8bcb8798276d6c77ec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateId")
    def key_vault_certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultCertificateId"))

    @key_vault_certificate_id.setter
    def key_vault_certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44e043ddc778ed5ca9a201ce648beb92abae060f225ea38ef6f73a07444e94a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultCertificateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultId")
    def key_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultId"))

    @key_vault_id.setter
    def key_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__702fb3030348643be8686ea5b35bd81564856dd8cc386842f63403edfa28f603)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificate")
    def negotiate_client_certificate(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negotiateClientCertificate"))

    @negotiate_client_certificate.setter
    def negotiate_client_certificate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__312d79c2c3cd1f764b79592ffa2fa564ff360e67228bcaa464c1fd5bb64a78a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negotiateClientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientId")
    def ssl_keyvault_identity_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslKeyvaultIdentityClientId"))

    @ssl_keyvault_identity_client_id.setter
    def ssl_keyvault_identity_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff0b631da0445d2ec59f6641dbc647224b507c8362a17315be33a2be3856a840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslKeyvaultIdentityClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainManagement]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainManagement]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainManagement]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b23236720ede30510d0b6ddb1151b84557a2a2298ce1ebacd933818727260e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainPortal",
    jsii_struct_bases=[],
    name_mapping={
        "host_name": "hostName",
        "certificate": "certificate",
        "certificate_password": "certificatePassword",
        "key_vault_certificate_id": "keyVaultCertificateId",
        "key_vault_id": "keyVaultId",
        "negotiate_client_certificate": "negotiateClientCertificate",
        "ssl_keyvault_identity_client_id": "sslKeyvaultIdentityClientId",
    },
)
class ApiManagementCustomDomainPortal:
    def __init__(
        self,
        *,
        host_name: builtins.str,
        certificate: typing.Optional[builtins.str] = None,
        certificate_password: typing.Optional[builtins.str] = None,
        key_vault_certificate_id: typing.Optional[builtins.str] = None,
        key_vault_id: typing.Optional[builtins.str] = None,
        negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#host_name ApiManagementCustomDomain#host_name}.
        :param certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate ApiManagementCustomDomain#certificate}.
        :param certificate_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate_password ApiManagementCustomDomain#certificate_password}.
        :param key_vault_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_certificate_id ApiManagementCustomDomain#key_vault_certificate_id}.
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_id ApiManagementCustomDomain#key_vault_id}.
        :param negotiate_client_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#negotiate_client_certificate ApiManagementCustomDomain#negotiate_client_certificate}.
        :param ssl_keyvault_identity_client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#ssl_keyvault_identity_client_id ApiManagementCustomDomain#ssl_keyvault_identity_client_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9c9a52593058c0f56271130c0096fc3f5af7b33d89ceceef7b0aebd38d96cbe)
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument certificate_password", value=certificate_password, expected_type=type_hints["certificate_password"])
            check_type(argname="argument key_vault_certificate_id", value=key_vault_certificate_id, expected_type=type_hints["key_vault_certificate_id"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument negotiate_client_certificate", value=negotiate_client_certificate, expected_type=type_hints["negotiate_client_certificate"])
            check_type(argname="argument ssl_keyvault_identity_client_id", value=ssl_keyvault_identity_client_id, expected_type=type_hints["ssl_keyvault_identity_client_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_name": host_name,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if certificate_password is not None:
            self._values["certificate_password"] = certificate_password
        if key_vault_certificate_id is not None:
            self._values["key_vault_certificate_id"] = key_vault_certificate_id
        if key_vault_id is not None:
            self._values["key_vault_id"] = key_vault_id
        if negotiate_client_certificate is not None:
            self._values["negotiate_client_certificate"] = negotiate_client_certificate
        if ssl_keyvault_identity_client_id is not None:
            self._values["ssl_keyvault_identity_client_id"] = ssl_keyvault_identity_client_id

    @builtins.property
    def host_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#host_name ApiManagementCustomDomain#host_name}.'''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate ApiManagementCustomDomain#certificate}.'''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate_password ApiManagementCustomDomain#certificate_password}.'''
        result = self._values.get("certificate_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_certificate_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_certificate_id ApiManagementCustomDomain#key_vault_certificate_id}.'''
        result = self._values.get("key_vault_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_id ApiManagementCustomDomain#key_vault_id}.'''
        result = self._values.get("key_vault_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negotiate_client_certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#negotiate_client_certificate ApiManagementCustomDomain#negotiate_client_certificate}.'''
        result = self._values.get("negotiate_client_certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssl_keyvault_identity_client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#ssl_keyvault_identity_client_id ApiManagementCustomDomain#ssl_keyvault_identity_client_id}.'''
        result = self._values.get("ssl_keyvault_identity_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementCustomDomainPortal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementCustomDomainPortalList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainPortalList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a44f17cf87950ac59473759f8b129fbc2cde3bbcb80119e064fa0d3e52177336)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementCustomDomainPortalOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd43894fece25e38d802072d7618ba3771039ffd1cb26286662f3bb399d4b82f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementCustomDomainPortalOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5319556ef8de6fd3f47c20dd19787475a237466f77aac7473d60fcf37ead7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23b1953ca4a488226dccf01bb75a78b16d9b9cacbdb6c47764bccdce258fcd6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1fe58c0651da5ea6f644c0f0f1c921c0b396d8938812b977bde8b1aee12c7ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainPortal]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainPortal]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainPortal]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e558e86e475fbf852d980e909ccbd733af01ce60521c6de7470caec38aa9e60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementCustomDomainPortalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainPortalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6103d1b8a50fa1b4daeb02b3497992f48322d6ba9233a65cbfebb52bc865017)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetCertificatePassword")
    def reset_certificate_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificatePassword", []))

    @jsii.member(jsii_name="resetKeyVaultCertificateId")
    def reset_key_vault_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultCertificateId", []))

    @jsii.member(jsii_name="resetKeyVaultId")
    def reset_key_vault_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultId", []))

    @jsii.member(jsii_name="resetNegotiateClientCertificate")
    def reset_negotiate_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegotiateClientCertificate", []))

    @jsii.member(jsii_name="resetSslKeyvaultIdentityClientId")
    def reset_ssl_keyvault_identity_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslKeyvaultIdentityClientId", []))

    @builtins.property
    @jsii.member(jsii_name="certificateSource")
    def certificate_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateSource"))

    @builtins.property
    @jsii.member(jsii_name="certificateStatus")
    def certificate_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateStatus"))

    @builtins.property
    @jsii.member(jsii_name="expiry")
    def expiry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiry"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="certificatePasswordInput")
    def certificate_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificatePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateIdInput")
    def key_vault_certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultCertificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultIdInput")
    def key_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificateInput")
    def negotiate_client_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negotiateClientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientIdInput")
    def ssl_keyvault_identity_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslKeyvaultIdentityClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__592b60ce960414d6cc51d5622fd799d6b9a9d5867d17cc59bbb8b0b2237b2c17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificatePassword")
    def certificate_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificatePassword"))

    @certificate_password.setter
    def certificate_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8155f0edd800fa1c17d1b22ad9c0909acb6a684bccd2327115d02b2179b5e52b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificatePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126c435c652459420f539bf46bbcbb75db64d24b954854aeb2927fe1f9cbe59f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateId")
    def key_vault_certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultCertificateId"))

    @key_vault_certificate_id.setter
    def key_vault_certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c37d88aa5f93e5ec8043244d394f668bd1b690b8328b6bd71df805f07d63cb2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultCertificateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultId")
    def key_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultId"))

    @key_vault_id.setter
    def key_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca844e7119c139122e52bc9e0f3efb7575b35a6e7c28711e4ff2a922c5cedb97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificate")
    def negotiate_client_certificate(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negotiateClientCertificate"))

    @negotiate_client_certificate.setter
    def negotiate_client_certificate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6044b9fd8f6295d9723bfa8b57864327ee2626b9cb5c126c5fdceb65a583d6f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negotiateClientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientId")
    def ssl_keyvault_identity_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslKeyvaultIdentityClientId"))

    @ssl_keyvault_identity_client_id.setter
    def ssl_keyvault_identity_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62b4f6168e17070c755031d8c5e773dbdce998fe9f9b96fdddecb3dbb7dfaba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslKeyvaultIdentityClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainPortal]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainPortal]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainPortal]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd79be307cb644ae0589bde9972a378ba7470d7b6973dfdef8ef7d3e93be9cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainScm",
    jsii_struct_bases=[],
    name_mapping={
        "host_name": "hostName",
        "certificate": "certificate",
        "certificate_password": "certificatePassword",
        "key_vault_certificate_id": "keyVaultCertificateId",
        "key_vault_id": "keyVaultId",
        "negotiate_client_certificate": "negotiateClientCertificate",
        "ssl_keyvault_identity_client_id": "sslKeyvaultIdentityClientId",
    },
)
class ApiManagementCustomDomainScm:
    def __init__(
        self,
        *,
        host_name: builtins.str,
        certificate: typing.Optional[builtins.str] = None,
        certificate_password: typing.Optional[builtins.str] = None,
        key_vault_certificate_id: typing.Optional[builtins.str] = None,
        key_vault_id: typing.Optional[builtins.str] = None,
        negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#host_name ApiManagementCustomDomain#host_name}.
        :param certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate ApiManagementCustomDomain#certificate}.
        :param certificate_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate_password ApiManagementCustomDomain#certificate_password}.
        :param key_vault_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_certificate_id ApiManagementCustomDomain#key_vault_certificate_id}.
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_id ApiManagementCustomDomain#key_vault_id}.
        :param negotiate_client_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#negotiate_client_certificate ApiManagementCustomDomain#negotiate_client_certificate}.
        :param ssl_keyvault_identity_client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#ssl_keyvault_identity_client_id ApiManagementCustomDomain#ssl_keyvault_identity_client_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d841bf2bce42c9cd1c7739af1ff5cc74f3472a0463b7e45396bcbe661483cf95)
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument certificate_password", value=certificate_password, expected_type=type_hints["certificate_password"])
            check_type(argname="argument key_vault_certificate_id", value=key_vault_certificate_id, expected_type=type_hints["key_vault_certificate_id"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument negotiate_client_certificate", value=negotiate_client_certificate, expected_type=type_hints["negotiate_client_certificate"])
            check_type(argname="argument ssl_keyvault_identity_client_id", value=ssl_keyvault_identity_client_id, expected_type=type_hints["ssl_keyvault_identity_client_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_name": host_name,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if certificate_password is not None:
            self._values["certificate_password"] = certificate_password
        if key_vault_certificate_id is not None:
            self._values["key_vault_certificate_id"] = key_vault_certificate_id
        if key_vault_id is not None:
            self._values["key_vault_id"] = key_vault_id
        if negotiate_client_certificate is not None:
            self._values["negotiate_client_certificate"] = negotiate_client_certificate
        if ssl_keyvault_identity_client_id is not None:
            self._values["ssl_keyvault_identity_client_id"] = ssl_keyvault_identity_client_id

    @builtins.property
    def host_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#host_name ApiManagementCustomDomain#host_name}.'''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate ApiManagementCustomDomain#certificate}.'''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#certificate_password ApiManagementCustomDomain#certificate_password}.'''
        result = self._values.get("certificate_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_certificate_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_certificate_id ApiManagementCustomDomain#key_vault_certificate_id}.'''
        result = self._values.get("key_vault_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#key_vault_id ApiManagementCustomDomain#key_vault_id}.'''
        result = self._values.get("key_vault_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negotiate_client_certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#negotiate_client_certificate ApiManagementCustomDomain#negotiate_client_certificate}.'''
        result = self._values.get("negotiate_client_certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssl_keyvault_identity_client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#ssl_keyvault_identity_client_id ApiManagementCustomDomain#ssl_keyvault_identity_client_id}.'''
        result = self._values.get("ssl_keyvault_identity_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementCustomDomainScm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementCustomDomainScmList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainScmList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83ba4cde87701058ee49d441ebf518b203323b48b42fc0c3cf5d8494e23689e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApiManagementCustomDomainScmOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a4a4fe29b1b4e6f3837baa0b78c13095c25af4aeda5e19ef259837ddf1e155)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementCustomDomainScmOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e098a2c19afd298cbd4809f148609fbb0bb7a65cdaed85cbed7514a6858f95d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71a584a346d78a391dad57400f0211dfe41f0e4efb22ac853a4e5cd9b84b6147)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f43340c0480d451d57cf33db117d7a0d356c1a08c9ccb443f9c05e698dfa504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainScm]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainScm]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainScm]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a11b8f1674a474e4a50f1f1f20b57f46fbce2fbc41001a2a5a56dda58b789ef0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementCustomDomainScmOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainScmOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24b3347115b8898acfb1329d0a38c7053c8251e75b7e33598bd0c567b1654aeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetCertificatePassword")
    def reset_certificate_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificatePassword", []))

    @jsii.member(jsii_name="resetKeyVaultCertificateId")
    def reset_key_vault_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultCertificateId", []))

    @jsii.member(jsii_name="resetKeyVaultId")
    def reset_key_vault_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultId", []))

    @jsii.member(jsii_name="resetNegotiateClientCertificate")
    def reset_negotiate_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegotiateClientCertificate", []))

    @jsii.member(jsii_name="resetSslKeyvaultIdentityClientId")
    def reset_ssl_keyvault_identity_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslKeyvaultIdentityClientId", []))

    @builtins.property
    @jsii.member(jsii_name="certificateSource")
    def certificate_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateSource"))

    @builtins.property
    @jsii.member(jsii_name="certificateStatus")
    def certificate_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateStatus"))

    @builtins.property
    @jsii.member(jsii_name="expiry")
    def expiry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiry"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="certificatePasswordInput")
    def certificate_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificatePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateIdInput")
    def key_vault_certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultCertificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultIdInput")
    def key_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificateInput")
    def negotiate_client_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negotiateClientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientIdInput")
    def ssl_keyvault_identity_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslKeyvaultIdentityClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c277e2b3d9912ddca755bd96878f8c5b852e7c20a4c46da791cb808764bc8017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificatePassword")
    def certificate_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificatePassword"))

    @certificate_password.setter
    def certificate_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56f37bf83909b0be562f6f6ccc4319036226bd335fd6b28707387180eec7a5c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificatePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e27f5a20a2883816f904625c0b25072d1b71470cb948de8c2c428345c699d93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultCertificateId")
    def key_vault_certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultCertificateId"))

    @key_vault_certificate_id.setter
    def key_vault_certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c2a6794c8101135da28d6e68188366a3320d6b319a302f090051d34349c6c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultCertificateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultId")
    def key_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultId"))

    @key_vault_id.setter
    def key_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__468b8f8cf54d5834f6ff819515b31281e3bb90da1895df220d9f90ce15219420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negotiateClientCertificate")
    def negotiate_client_certificate(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negotiateClientCertificate"))

    @negotiate_client_certificate.setter
    def negotiate_client_certificate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec2bf7e1dbf33bb78d25b1cff530f07e65a4ae1ab80626c96390d5896a4296b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negotiateClientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslKeyvaultIdentityClientId")
    def ssl_keyvault_identity_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslKeyvaultIdentityClientId"))

    @ssl_keyvault_identity_client_id.setter
    def ssl_keyvault_identity_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac2c42cd8c9681f73dcf175ddeb6648ef6d317054e9c6d99f5c6e7ecf96c98a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslKeyvaultIdentityClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainScm]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainScm]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainScm]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98819702815c6d0b604f587839124061bcd8381a48b00915d9c0773565be579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ApiManagementCustomDomainTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#create ApiManagementCustomDomain#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#delete ApiManagementCustomDomain#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#read ApiManagementCustomDomain#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#update ApiManagementCustomDomain#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab32ba014ba7b0bb50a323d2bb58427eb174745ef6e7b8e3e451551c3041d83a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#create ApiManagementCustomDomain#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#delete ApiManagementCustomDomain#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#read ApiManagementCustomDomain#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_custom_domain#update ApiManagementCustomDomain#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementCustomDomainTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementCustomDomainTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementCustomDomain.ApiManagementCustomDomainTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c67e6e084ebf7839f73e6d845e6576ad5a107f85a5982b9ada8bd60ba3a4acc6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38c48f0b085303681845e7e4054a32d284314ed3b9d0cf40709c529590670cf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab1a1982bea9eeefbdb646449690a508d06a780706badb98827f3be0f323b227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__650f1ae3ad691bc98ca293d07be1be00723b653fff8c02968454144365f6c1f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad8e091e159f70fd401edc2f8f5a61aded49a1ffa476bdb79fe564aabc3896db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada824af49b5768b79d337781436facb983e1006ed81d86439d80f8b6b6f4ca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApiManagementCustomDomain",
    "ApiManagementCustomDomainConfig",
    "ApiManagementCustomDomainDeveloperPortal",
    "ApiManagementCustomDomainDeveloperPortalList",
    "ApiManagementCustomDomainDeveloperPortalOutputReference",
    "ApiManagementCustomDomainGateway",
    "ApiManagementCustomDomainGatewayList",
    "ApiManagementCustomDomainGatewayOutputReference",
    "ApiManagementCustomDomainManagement",
    "ApiManagementCustomDomainManagementList",
    "ApiManagementCustomDomainManagementOutputReference",
    "ApiManagementCustomDomainPortal",
    "ApiManagementCustomDomainPortalList",
    "ApiManagementCustomDomainPortalOutputReference",
    "ApiManagementCustomDomainScm",
    "ApiManagementCustomDomainScmList",
    "ApiManagementCustomDomainScmOutputReference",
    "ApiManagementCustomDomainTimeouts",
    "ApiManagementCustomDomainTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9caf6ce4cef0ec185150e9a4060c35b5665c1d204da62bcd61e1782525c1273f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    api_management_id: builtins.str,
    developer_portal: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCustomDomainDeveloperPortal, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gateway: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCustomDomainGateway, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    management: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCustomDomainManagement, typing.Dict[builtins.str, typing.Any]]]]] = None,
    portal: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCustomDomainPortal, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scm: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCustomDomainScm, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[ApiManagementCustomDomainTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__0446830050a1b57b42ab5891f20916ead11ecd69315e6c8c6507881dd9344d95(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59a5bba7e7a19e284f36f8e2a3367b394110acfd87993f9299981f42f775c3b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCustomDomainDeveloperPortal, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3761930e66c603cfabd65ad9454e54601ce0e021a858b9a3a4539d0489b1f17(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCustomDomainGateway, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea0c5dbb88dc83c842faf61a6efb0dd7abbaa6a20f529d91266b25d35023252(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCustomDomainManagement, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecfae0e2c35563a7261b3c4e35ab6a0c835c7c3f72bddb9449b347c7595098af(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCustomDomainPortal, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668a06c308eef12556820cc43856700521fff74ea0f773f9e0ecb8be1aa1b862(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCustomDomainScm, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9298ebeeba6ad71251ccca738eccf5f84f3d90bdcd9d806a58729adb003d88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fe38bb4fad8ad7e5361eb27ea91c3434f26b1b0d563021a44d1bf24c17218c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a7e6d03296cdb652dda1d79a95992b3d153829472cbd957274b12363e08815b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    api_management_id: builtins.str,
    developer_portal: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCustomDomainDeveloperPortal, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gateway: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCustomDomainGateway, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    management: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCustomDomainManagement, typing.Dict[builtins.str, typing.Any]]]]] = None,
    portal: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCustomDomainPortal, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scm: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementCustomDomainScm, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[ApiManagementCustomDomainTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731dd8c12498f4895fe15fa11b5337c5c0324c0f7a1819c44637478aaad438d3(
    *,
    host_name: builtins.str,
    certificate: typing.Optional[builtins.str] = None,
    certificate_password: typing.Optional[builtins.str] = None,
    key_vault_certificate_id: typing.Optional[builtins.str] = None,
    key_vault_id: typing.Optional[builtins.str] = None,
    negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0fd60e9f138fdc486cca785ea0617e756ab26bb9efb62733797774f9796d1e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d036cfa859c646b83f847ada566b57e16cf1d018074ff378be202c96cfd259c2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9208983d08673131605a987d7a8051d8d6140203a516f514a0be1f1538c1540(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9737c342331517f0f8094eac5a291018cba38abcd832b1fd1fce2cf28900872(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0030fd36aef993c52024e89f01055dd319189846e019a7836f045bede63fcd2a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2327e4cab9538a8d6745f22013dacdeb78fd12c6df8b2aebc082b28e00a43c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainDeveloperPortal]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e8a7150877cdcde15de8da50af1aa66358b162eb5a222c9a03eade653e52ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5050a3ea99fa1822182e88acd43baf413893aa232911c0506306754f9b33e75b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b871fdb3cd49081baea8df08899d9942d05cbbc0b63622b7124d6c708ce14f1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7c8c7afa842f2ff815d0cc9a146036fe67f7d01fe3f59f8791a9fc41cb685e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ec0dabc26b78e6c801f2d2e00595e5d880872eb40e948c7b03f9a7da7c61e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e064e8b49b906c393cabfebbe928dff5d0b9542a2be0644083368ebdf7cc97cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a477cac98d1c08c9322e97a2d1ed1723f8cb33347ee17c52353b159cf293d05(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760072a2156ec5b4360903ab9f39e2648d7a505e353b801d1ca5a54301ca2aa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95099509ba41c07fc3e7f3aed541b472fb9c79bf8cdba6c86f0fded250c80265(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainDeveloperPortal]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c281634f087311cc558e2e6ec3c9952be8b2eab48323c38cdb3a61bf1927c85c(
    *,
    host_name: builtins.str,
    certificate: typing.Optional[builtins.str] = None,
    certificate_password: typing.Optional[builtins.str] = None,
    default_ssl_binding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_vault_certificate_id: typing.Optional[builtins.str] = None,
    key_vault_id: typing.Optional[builtins.str] = None,
    negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b060f7519133b2c312e22e790f263cb3368cd1a5afe0f037c6465785ef740fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f8f273cd9f6f498d2367a6b18bbe918740ef37c69ded04270cd2bc4233a1ea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58601de5fc0dea4ad5a38e7008402fdb9eebc7a406f6962fd9c42fa8ebdfd55e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d52c4de18e672631792402f76aab11f7fd8b8fc417a1a594e652dcb2d6f60ad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8400ea41f5f458db97ef4ef2bd5763165b2230dc72ccc4939b407ea5e8f94ac0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b336182ef2bccc318e68546063b6bdb8aa387cff1bae77f52c5882967f7f9fd3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainGateway]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71cb37e5a5111ef2cb9a8b1b071b7f59cf3310716bce855243a80445cb9c2e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eabc43c4bc303b438a56268225fccf7da6b7b10958067ee04b67583bec78110(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e30cdc5520f3b2fb9e5b2ac6fd034710120f1725c10a1811285aebdaeed4a5a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a25b3320926238318cfaf6ef9b2a85c63ca38832447e9b079f8903144a8d53(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f16d22e70cacc2be198592069d2acafab10727ceabab522c722bc923feabb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64c3ce7e4e548570283132fc6be53c56685459dbf00f09d77cba0c4f7e45ab1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c81386a54b0230de39103fc60de60f26ff4822e60a9686e2fa86c68ec5a315a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e823033699fb195357a7d9bf14c60befaffd45fd0a6b427478c72ca9e18ca9f0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8195f95024b34b0007cbe98358fff23d9fff6d36d82bdc777524bb24510a3319(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b9b4823c40964b38612a0086a849e8e52f5465b22edbf223775fc0159f5c666(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainGateway]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887b666f4e6a367f4d4b26f0b72889e51b4b9b2cd8136b21937b3f8a6c2bb665(
    *,
    host_name: builtins.str,
    certificate: typing.Optional[builtins.str] = None,
    certificate_password: typing.Optional[builtins.str] = None,
    key_vault_certificate_id: typing.Optional[builtins.str] = None,
    key_vault_id: typing.Optional[builtins.str] = None,
    negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c4e5a1c23b3deb43e83abcc72afb7c6cbe4daaea80ad8ea6d5208ce595ddad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a2598c904cc0f43778b56ba3357a48d6fcf57db6e7e2a9e143d16abe2d3c65(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3e5c3320a53a0575de1364d8b20274dc4838be79a999ba5728f52718fb62d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6537c86319f2c720ba8825b40f8e4320badf81f22dbfd20ef8c2d00624b951c9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68a4e1ad8725a8f431560524453ffea6f74d73c6571e397a59e0783203317b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7e1a7fe0872a91583722bb126cb802b3d4ca1a553e085aef13980a8a247240(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainManagement]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65fdc1335ee6541787d8446a1e4c737014c4e13212d2bd28492ee6a07c25fdb5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3971e15c25b6abf56ab6df84a44a848d419ac23dd66f7ded3386aea719537242(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5765cc85854c2354aa1ee91e456442cfdb139ba4a09c241f2c3c5a3e96119815(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c70ba375ee21812c66c2e659a6233c7c986ed4bd8df3d8bcb8798276d6c77ec6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e043ddc778ed5ca9a201ce648beb92abae060f225ea38ef6f73a07444e94a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__702fb3030348643be8686ea5b35bd81564856dd8cc386842f63403edfa28f603(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312d79c2c3cd1f764b79592ffa2fa564ff360e67228bcaa464c1fd5bb64a78a8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0b631da0445d2ec59f6641dbc647224b507c8362a17315be33a2be3856a840(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b23236720ede30510d0b6ddb1151b84557a2a2298ce1ebacd933818727260e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainManagement]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c9a52593058c0f56271130c0096fc3f5af7b33d89ceceef7b0aebd38d96cbe(
    *,
    host_name: builtins.str,
    certificate: typing.Optional[builtins.str] = None,
    certificate_password: typing.Optional[builtins.str] = None,
    key_vault_certificate_id: typing.Optional[builtins.str] = None,
    key_vault_id: typing.Optional[builtins.str] = None,
    negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a44f17cf87950ac59473759f8b129fbc2cde3bbcb80119e064fa0d3e52177336(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd43894fece25e38d802072d7618ba3771039ffd1cb26286662f3bb399d4b82f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5319556ef8de6fd3f47c20dd19787475a237466f77aac7473d60fcf37ead7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b1953ca4a488226dccf01bb75a78b16d9b9cacbdb6c47764bccdce258fcd6b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1fe58c0651da5ea6f644c0f0f1c921c0b396d8938812b977bde8b1aee12c7ce(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e558e86e475fbf852d980e909ccbd733af01ce60521c6de7470caec38aa9e60(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainPortal]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6103d1b8a50fa1b4daeb02b3497992f48322d6ba9233a65cbfebb52bc865017(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592b60ce960414d6cc51d5622fd799d6b9a9d5867d17cc59bbb8b0b2237b2c17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8155f0edd800fa1c17d1b22ad9c0909acb6a684bccd2327115d02b2179b5e52b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126c435c652459420f539bf46bbcbb75db64d24b954854aeb2927fe1f9cbe59f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37d88aa5f93e5ec8043244d394f668bd1b690b8328b6bd71df805f07d63cb2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca844e7119c139122e52bc9e0f3efb7575b35a6e7c28711e4ff2a922c5cedb97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6044b9fd8f6295d9723bfa8b57864327ee2626b9cb5c126c5fdceb65a583d6f0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62b4f6168e17070c755031d8c5e773dbdce998fe9f9b96fdddecb3dbb7dfaba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd79be307cb644ae0589bde9972a378ba7470d7b6973dfdef8ef7d3e93be9cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainPortal]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d841bf2bce42c9cd1c7739af1ff5cc74f3472a0463b7e45396bcbe661483cf95(
    *,
    host_name: builtins.str,
    certificate: typing.Optional[builtins.str] = None,
    certificate_password: typing.Optional[builtins.str] = None,
    key_vault_certificate_id: typing.Optional[builtins.str] = None,
    key_vault_id: typing.Optional[builtins.str] = None,
    negotiate_client_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssl_keyvault_identity_client_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ba4cde87701058ee49d441ebf518b203323b48b42fc0c3cf5d8494e23689e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a4a4fe29b1b4e6f3837baa0b78c13095c25af4aeda5e19ef259837ddf1e155(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e098a2c19afd298cbd4809f148609fbb0bb7a65cdaed85cbed7514a6858f95d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a584a346d78a391dad57400f0211dfe41f0e4efb22ac853a4e5cd9b84b6147(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f43340c0480d451d57cf33db117d7a0d356c1a08c9ccb443f9c05e698dfa504(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11b8f1674a474e4a50f1f1f20b57f46fbce2fbc41001a2a5a56dda58b789ef0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementCustomDomainScm]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b3347115b8898acfb1329d0a38c7053c8251e75b7e33598bd0c567b1654aeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c277e2b3d9912ddca755bd96878f8c5b852e7c20a4c46da791cb808764bc8017(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56f37bf83909b0be562f6f6ccc4319036226bd335fd6b28707387180eec7a5c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e27f5a20a2883816f904625c0b25072d1b71470cb948de8c2c428345c699d93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c2a6794c8101135da28d6e68188366a3320d6b319a302f090051d34349c6c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468b8f8cf54d5834f6ff819515b31281e3bb90da1895df220d9f90ce15219420(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec2bf7e1dbf33bb78d25b1cff530f07e65a4ae1ab80626c96390d5896a4296b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac2c42cd8c9681f73dcf175ddeb6648ef6d317054e9c6d99f5c6e7ecf96c98a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98819702815c6d0b604f587839124061bcd8381a48b00915d9c0773565be579(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainScm]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab32ba014ba7b0bb50a323d2bb58427eb174745ef6e7b8e3e451551c3041d83a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67e6e084ebf7839f73e6d845e6576ad5a107f85a5982b9ada8bd60ba3a4acc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c48f0b085303681845e7e4054a32d284314ed3b9d0cf40709c529590670cf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab1a1982bea9eeefbdb646449690a508d06a780706badb98827f3be0f323b227(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__650f1ae3ad691bc98ca293d07be1be00723b653fff8c02968454144365f6c1f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8e091e159f70fd401edc2f8f5a61aded49a1ffa476bdb79fe564aabc3896db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada824af49b5768b79d337781436facb983e1006ed81d86439d80f8b6b6f4ca2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementCustomDomainTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

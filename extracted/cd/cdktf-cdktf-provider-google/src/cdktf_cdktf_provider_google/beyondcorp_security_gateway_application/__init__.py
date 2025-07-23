r'''
# `google_beyondcorp_security_gateway_application`

Refer to the Terraform Registry for docs: [`google_beyondcorp_security_gateway_application`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application).
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


class BeyondcorpSecurityGatewayApplication(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.beyondcorpSecurityGatewayApplication.BeyondcorpSecurityGatewayApplication",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application google_beyondcorp_security_gateway_application}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        application_id: builtins.str,
        endpoint_matchers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BeyondcorpSecurityGatewayApplicationEndpointMatchers", typing.Dict[builtins.str, typing.Any]]]],
        security_gateway_id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BeyondcorpSecurityGatewayApplicationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upstreams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BeyondcorpSecurityGatewayApplicationUpstreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application google_beyondcorp_security_gateway_application} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param application_id: User-settable Application resource ID. - Must start with a letter. - Must contain between 4-63 characters from '/a-z-/'. - Must end with a number or letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#application_id BeyondcorpSecurityGatewayApplication#application_id}
        :param endpoint_matchers: endpoint_matchers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#endpoint_matchers BeyondcorpSecurityGatewayApplication#endpoint_matchers}
        :param security_gateway_id: ID of the Security Gateway resource this belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#security_gateway_id BeyondcorpSecurityGatewayApplication#security_gateway_id}
        :param display_name: Optional. An arbitrary user-provided name for the Application resource. Cannot exceed 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#display_name BeyondcorpSecurityGatewayApplication#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#id BeyondcorpSecurityGatewayApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#project BeyondcorpSecurityGatewayApplication#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#timeouts BeyondcorpSecurityGatewayApplication#timeouts}
        :param upstreams: upstreams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#upstreams BeyondcorpSecurityGatewayApplication#upstreams}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbc5bd11ac1ce6cf9f33abf938547589a84fda544ac2a0d2611341af916d9112)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BeyondcorpSecurityGatewayApplicationConfig(
            application_id=application_id,
            endpoint_matchers=endpoint_matchers,
            security_gateway_id=security_gateway_id,
            display_name=display_name,
            id=id,
            project=project,
            timeouts=timeouts,
            upstreams=upstreams,
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
        '''Generates CDKTF code for importing a BeyondcorpSecurityGatewayApplication resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BeyondcorpSecurityGatewayApplication to import.
        :param import_from_id: The id of the existing BeyondcorpSecurityGatewayApplication that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BeyondcorpSecurityGatewayApplication to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__736631b0b0b291412bb9e5c788d083802619c2565f8d6c390ba354544164d351)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEndpointMatchers")
    def put_endpoint_matchers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BeyondcorpSecurityGatewayApplicationEndpointMatchers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a2c5acc042308437a47d2beaa8186bc3cec524a84e3097b75e15e2810935efc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEndpointMatchers", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#create BeyondcorpSecurityGatewayApplication#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#delete BeyondcorpSecurityGatewayApplication#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#update BeyondcorpSecurityGatewayApplication#update}.
        '''
        value = BeyondcorpSecurityGatewayApplicationTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUpstreams")
    def put_upstreams(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BeyondcorpSecurityGatewayApplicationUpstreams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5584f4e12f1f43ff2c44f8a2a6c8fb446fabeb77f713f341e01e6d124b39026b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUpstreams", [value]))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUpstreams")
    def reset_upstreams(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpstreams", []))

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
    @jsii.member(jsii_name="endpointMatchers")
    def endpoint_matchers(
        self,
    ) -> "BeyondcorpSecurityGatewayApplicationEndpointMatchersList":
        return typing.cast("BeyondcorpSecurityGatewayApplicationEndpointMatchersList", jsii.get(self, "endpointMatchers"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BeyondcorpSecurityGatewayApplicationTimeoutsOutputReference":
        return typing.cast("BeyondcorpSecurityGatewayApplicationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="upstreams")
    def upstreams(self) -> "BeyondcorpSecurityGatewayApplicationUpstreamsList":
        return typing.cast("BeyondcorpSecurityGatewayApplicationUpstreamsList", jsii.get(self, "upstreams"))

    @builtins.property
    @jsii.member(jsii_name="applicationIdInput")
    def application_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointMatchersInput")
    def endpoint_matchers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BeyondcorpSecurityGatewayApplicationEndpointMatchers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BeyondcorpSecurityGatewayApplicationEndpointMatchers"]]], jsii.get(self, "endpointMatchersInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGatewayIdInput")
    def security_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityGatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BeyondcorpSecurityGatewayApplicationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BeyondcorpSecurityGatewayApplicationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="upstreamsInput")
    def upstreams_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BeyondcorpSecurityGatewayApplicationUpstreams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BeyondcorpSecurityGatewayApplicationUpstreams"]]], jsii.get(self, "upstreamsInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__593cd6c5c0e8ea89e1078167eb6b31ebe0abc0f1cdf18448cd98c7e9e5fd1cd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f693650d9311e02def1afb8ac5860a3f2768bfa2688b2854c132b44abf009300)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63202678fd8d6cf0a549c07d7f7ffdedcd8828501c1521bbdf104043cf76c243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65c2469a3f1944e7effbb934f01b5513d1db3ad5d6b8fc50e2ea94abf0e9ac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGatewayId")
    def security_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGatewayId"))

    @security_gateway_id.setter
    def security_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fffb2067a3c2960dd170daec4a68c88bfd12598bbbd0ac99f2e2eecc1db2a4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGatewayId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.beyondcorpSecurityGatewayApplication.BeyondcorpSecurityGatewayApplicationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "application_id": "applicationId",
        "endpoint_matchers": "endpointMatchers",
        "security_gateway_id": "securityGatewayId",
        "display_name": "displayName",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
        "upstreams": "upstreams",
    },
)
class BeyondcorpSecurityGatewayApplicationConfig(
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
        application_id: builtins.str,
        endpoint_matchers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BeyondcorpSecurityGatewayApplicationEndpointMatchers", typing.Dict[builtins.str, typing.Any]]]],
        security_gateway_id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BeyondcorpSecurityGatewayApplicationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upstreams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BeyondcorpSecurityGatewayApplicationUpstreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param application_id: User-settable Application resource ID. - Must start with a letter. - Must contain between 4-63 characters from '/a-z-/'. - Must end with a number or letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#application_id BeyondcorpSecurityGatewayApplication#application_id}
        :param endpoint_matchers: endpoint_matchers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#endpoint_matchers BeyondcorpSecurityGatewayApplication#endpoint_matchers}
        :param security_gateway_id: ID of the Security Gateway resource this belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#security_gateway_id BeyondcorpSecurityGatewayApplication#security_gateway_id}
        :param display_name: Optional. An arbitrary user-provided name for the Application resource. Cannot exceed 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#display_name BeyondcorpSecurityGatewayApplication#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#id BeyondcorpSecurityGatewayApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#project BeyondcorpSecurityGatewayApplication#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#timeouts BeyondcorpSecurityGatewayApplication#timeouts}
        :param upstreams: upstreams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#upstreams BeyondcorpSecurityGatewayApplication#upstreams}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = BeyondcorpSecurityGatewayApplicationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__737bae195119be6189df221c6786500fdaa694075014c35c41f188c605dc9bd9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument endpoint_matchers", value=endpoint_matchers, expected_type=type_hints["endpoint_matchers"])
            check_type(argname="argument security_gateway_id", value=security_gateway_id, expected_type=type_hints["security_gateway_id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument upstreams", value=upstreams, expected_type=type_hints["upstreams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "endpoint_matchers": endpoint_matchers,
            "security_gateway_id": security_gateway_id,
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
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if upstreams is not None:
            self._values["upstreams"] = upstreams

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
    def application_id(self) -> builtins.str:
        '''User-settable Application resource ID.

        - Must start with a letter.
        - Must contain between 4-63 characters from '/a-z-/'.
        - Must end with a number or letter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#application_id BeyondcorpSecurityGatewayApplication#application_id}
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint_matchers(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BeyondcorpSecurityGatewayApplicationEndpointMatchers"]]:
        '''endpoint_matchers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#endpoint_matchers BeyondcorpSecurityGatewayApplication#endpoint_matchers}
        '''
        result = self._values.get("endpoint_matchers")
        assert result is not None, "Required property 'endpoint_matchers' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BeyondcorpSecurityGatewayApplicationEndpointMatchers"]], result)

    @builtins.property
    def security_gateway_id(self) -> builtins.str:
        '''ID of the Security Gateway resource this belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#security_gateway_id BeyondcorpSecurityGatewayApplication#security_gateway_id}
        '''
        result = self._values.get("security_gateway_id")
        assert result is not None, "Required property 'security_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Optional. An arbitrary user-provided name for the Application resource. Cannot exceed 64 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#display_name BeyondcorpSecurityGatewayApplication#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#id BeyondcorpSecurityGatewayApplication#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#project BeyondcorpSecurityGatewayApplication#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["BeyondcorpSecurityGatewayApplicationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#timeouts BeyondcorpSecurityGatewayApplication#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BeyondcorpSecurityGatewayApplicationTimeouts"], result)

    @builtins.property
    def upstreams(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BeyondcorpSecurityGatewayApplicationUpstreams"]]]:
        '''upstreams block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#upstreams BeyondcorpSecurityGatewayApplication#upstreams}
        '''
        result = self._values.get("upstreams")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BeyondcorpSecurityGatewayApplicationUpstreams"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BeyondcorpSecurityGatewayApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.beyondcorpSecurityGatewayApplication.BeyondcorpSecurityGatewayApplicationEndpointMatchers",
    jsii_struct_bases=[],
    name_mapping={"hostname": "hostname", "ports": "ports"},
)
class BeyondcorpSecurityGatewayApplicationEndpointMatchers:
    def __init__(
        self,
        *,
        hostname: builtins.str,
        ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param hostname: Required. Hostname of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#hostname BeyondcorpSecurityGatewayApplication#hostname}
        :param ports: Optional. Ports of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#ports BeyondcorpSecurityGatewayApplication#ports}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aeb844e2b338b1cd14edb60c950f9a28d821777d1609b299de34c17218d7238)
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hostname": hostname,
        }
        if ports is not None:
            self._values["ports"] = ports

    @builtins.property
    def hostname(self) -> builtins.str:
        '''Required. Hostname of the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#hostname BeyondcorpSecurityGatewayApplication#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Optional. Ports of the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#ports BeyondcorpSecurityGatewayApplication#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BeyondcorpSecurityGatewayApplicationEndpointMatchers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BeyondcorpSecurityGatewayApplicationEndpointMatchersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.beyondcorpSecurityGatewayApplication.BeyondcorpSecurityGatewayApplicationEndpointMatchersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e780fa01a0eb5d1e734cee3a9f915b1a8ff91d920311f3984809429b970eed7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BeyondcorpSecurityGatewayApplicationEndpointMatchersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177b7a4e82727a80182510a700965684ebddea2bfcac0ee6f22f02e80463824e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BeyondcorpSecurityGatewayApplicationEndpointMatchersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__364385b2503002430e822db5a52b712c08861fba0d7400e88feee921820f8989)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a147c3501213a5a526b1949718c84d096ddc0bd93d0bb2d593e874047ae389de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__982061f849e286266b143a53e9fffdf001808a27264a6bfa2cb89b6b2fe694fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BeyondcorpSecurityGatewayApplicationEndpointMatchers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BeyondcorpSecurityGatewayApplicationEndpointMatchers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BeyondcorpSecurityGatewayApplicationEndpointMatchers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a9821b8e2ac0b296fa8dc6e73e6b30b89dd01d95206f2a0ea1c8c2b31d7268d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BeyondcorpSecurityGatewayApplicationEndpointMatchersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.beyondcorpSecurityGatewayApplication.BeyondcorpSecurityGatewayApplicationEndpointMatchersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd27ae8459ac8aa11b4d5d1e086b43959433ab5148c1d20c2da60f7318c011ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPorts")
    def reset_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPorts", []))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d3ccbfe1cf232f24218681f31b374b5e6e9ebd03591f8960a7dbdab60b570fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e83e43e0ba9a4237040cb986dcadfe0e99668339644bddaf272c098c6c3419c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BeyondcorpSecurityGatewayApplicationEndpointMatchers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BeyondcorpSecurityGatewayApplicationEndpointMatchers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BeyondcorpSecurityGatewayApplicationEndpointMatchers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f9433c2b394fe72d6c6d94066c68a49a52add30d027e0ff1394d7ffdcde9b87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.beyondcorpSecurityGatewayApplication.BeyondcorpSecurityGatewayApplicationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BeyondcorpSecurityGatewayApplicationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#create BeyondcorpSecurityGatewayApplication#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#delete BeyondcorpSecurityGatewayApplication#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#update BeyondcorpSecurityGatewayApplication#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552bd8d881d245664ba1966204f0fe735addf1f65efbb4362dac9f469982cbc7)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#create BeyondcorpSecurityGatewayApplication#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#delete BeyondcorpSecurityGatewayApplication#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#update BeyondcorpSecurityGatewayApplication#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BeyondcorpSecurityGatewayApplicationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BeyondcorpSecurityGatewayApplicationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.beyondcorpSecurityGatewayApplication.BeyondcorpSecurityGatewayApplicationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95d53088a9fbfa2ebcab680ade03d72cea97d302f1c1e9c92eb8b9310c2b57f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__bfbcc02d0d08830b289004d2306db7025d607ea9b46b9600320874d377d2ea58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3ac26799c7a55d65d20b66c8a676b6d5c0e616672697e543e7981ef51a3fba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ec1a6e05816a051126b57a0aea0b53987a12053221408074409e4f5059f4b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BeyondcorpSecurityGatewayApplicationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BeyondcorpSecurityGatewayApplicationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BeyondcorpSecurityGatewayApplicationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bceb4a964510ec4807fbb7da3f50e407d1e32894867ce8dad71e689fb44eece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.beyondcorpSecurityGatewayApplication.BeyondcorpSecurityGatewayApplicationUpstreams",
    jsii_struct_bases=[],
    name_mapping={"egress_policy": "egressPolicy", "network": "network"},
)
class BeyondcorpSecurityGatewayApplicationUpstreams:
    def __init__(
        self,
        *,
        egress_policy: typing.Optional[typing.Union["BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["BeyondcorpSecurityGatewayApplicationUpstreamsNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param egress_policy: egress_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#egress_policy BeyondcorpSecurityGatewayApplication#egress_policy}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#network BeyondcorpSecurityGatewayApplication#network}
        '''
        if isinstance(egress_policy, dict):
            egress_policy = BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicy(**egress_policy)
        if isinstance(network, dict):
            network = BeyondcorpSecurityGatewayApplicationUpstreamsNetwork(**network)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e027ca2ba3bb146414babb53fde0d47d3057ad1a9fa4fd65210ff60a3f5308eb)
            check_type(argname="argument egress_policy", value=egress_policy, expected_type=type_hints["egress_policy"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if egress_policy is not None:
            self._values["egress_policy"] = egress_policy
        if network is not None:
            self._values["network"] = network

    @builtins.property
    def egress_policy(
        self,
    ) -> typing.Optional["BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicy"]:
        '''egress_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#egress_policy BeyondcorpSecurityGatewayApplication#egress_policy}
        '''
        result = self._values.get("egress_policy")
        return typing.cast(typing.Optional["BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicy"], result)

    @builtins.property
    def network(
        self,
    ) -> typing.Optional["BeyondcorpSecurityGatewayApplicationUpstreamsNetwork"]:
        '''network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#network BeyondcorpSecurityGatewayApplication#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional["BeyondcorpSecurityGatewayApplicationUpstreamsNetwork"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BeyondcorpSecurityGatewayApplicationUpstreams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.beyondcorpSecurityGatewayApplication.BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicy",
    jsii_struct_bases=[],
    name_mapping={"regions": "regions"},
)
class BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicy:
    def __init__(self, *, regions: typing.Sequence[builtins.str]) -> None:
        '''
        :param regions: Required. List of regions where the application sends traffic to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#regions BeyondcorpSecurityGatewayApplication#regions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6cf92df358664b9a4b60a78abf3f110085c291b8da90f6c729e8b8934024670)
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "regions": regions,
        }

    @builtins.property
    def regions(self) -> typing.List[builtins.str]:
        '''Required. List of regions where the application sends traffic to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#regions BeyondcorpSecurityGatewayApplication#regions}
        '''
        result = self._values.get("regions")
        assert result is not None, "Required property 'regions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.beyondcorpSecurityGatewayApplication.BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c767026d9c8b5973a6420cc75667095f9e62a55eab33b55512a6b9a5bbaa9a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="regionsInput")
    def regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "regionsInput"))

    @builtins.property
    @jsii.member(jsii_name="regions")
    def regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "regions"))

    @regions.setter
    def regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__302de0318353312951d667c0665a9e4737e679e5b3d659a7384f4d6b25ace741)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicy]:
        return typing.cast(typing.Optional[BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49dc344b2389da77656da97a1492cf766c7a6c0ad7cfb34fd27d6ca47a41ab10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BeyondcorpSecurityGatewayApplicationUpstreamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.beyondcorpSecurityGatewayApplication.BeyondcorpSecurityGatewayApplicationUpstreamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea8d2487ed490a450037ba5e2186f2721820d7249cbf15d005329e985b021872)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BeyondcorpSecurityGatewayApplicationUpstreamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc3dfc1563bb4669b2e9339cf88eabb8f3cee0d3b8c7491c11e9c239da338cdb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BeyondcorpSecurityGatewayApplicationUpstreamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a21454b047168df39e66b4d3b99fe574daeddf4a4d4b6a494cb3b8c0a0d48f8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e00e058a98b14fa0f4b095c90f55dd602541f57a69ab8735562e2d09e7f4665e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57651c0cd5916cd09edf43be846261808ec76b57c51932e56bc24332e116d46f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BeyondcorpSecurityGatewayApplicationUpstreams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BeyondcorpSecurityGatewayApplicationUpstreams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BeyondcorpSecurityGatewayApplicationUpstreams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd47bbda42e63839baabac20f6ea86071d0c582fb00511f31a627cd470ac8de6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.beyondcorpSecurityGatewayApplication.BeyondcorpSecurityGatewayApplicationUpstreamsNetwork",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class BeyondcorpSecurityGatewayApplicationUpstreamsNetwork:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Network name is of the format: 'projects/{project}/global/networks/{network}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#name BeyondcorpSecurityGatewayApplication#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0d7c7b1d0b021bfc3d1b01b4db22f4e46c9d39c62cba3dd91fd6127aeb92be7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Required. Network name is of the format: 'projects/{project}/global/networks/{network}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#name BeyondcorpSecurityGatewayApplication#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BeyondcorpSecurityGatewayApplicationUpstreamsNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BeyondcorpSecurityGatewayApplicationUpstreamsNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.beyondcorpSecurityGatewayApplication.BeyondcorpSecurityGatewayApplicationUpstreamsNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec08d069b063c9086364317ffd8cf1a829d522569fbbfb7446ba351366d3f5d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__215c89e44187f4776475da712947ff95383d80a587fa4c8c083d2ce8136dc131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BeyondcorpSecurityGatewayApplicationUpstreamsNetwork]:
        return typing.cast(typing.Optional[BeyondcorpSecurityGatewayApplicationUpstreamsNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BeyondcorpSecurityGatewayApplicationUpstreamsNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c91f6b0a91c07b693b8a01c1f0230a03a10f7b8a9faf22ab22ba90147d0780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BeyondcorpSecurityGatewayApplicationUpstreamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.beyondcorpSecurityGatewayApplication.BeyondcorpSecurityGatewayApplicationUpstreamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af4616a8db211758e128ac0c4fb34be4507b37b67f4c99b5640f59aabd8b1fd6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEgressPolicy")
    def put_egress_policy(self, *, regions: typing.Sequence[builtins.str]) -> None:
        '''
        :param regions: Required. List of regions where the application sends traffic to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#regions BeyondcorpSecurityGatewayApplication#regions}
        '''
        value = BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicy(
            regions=regions
        )

        return typing.cast(None, jsii.invoke(self, "putEgressPolicy", [value]))

    @jsii.member(jsii_name="putNetwork")
    def put_network(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Network name is of the format: 'projects/{project}/global/networks/{network}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_security_gateway_application#name BeyondcorpSecurityGatewayApplication#name}
        '''
        value = BeyondcorpSecurityGatewayApplicationUpstreamsNetwork(name=name)

        return typing.cast(None, jsii.invoke(self, "putNetwork", [value]))

    @jsii.member(jsii_name="resetEgressPolicy")
    def reset_egress_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressPolicy", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @builtins.property
    @jsii.member(jsii_name="egressPolicy")
    def egress_policy(
        self,
    ) -> BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicyOutputReference:
        return typing.cast(BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicyOutputReference, jsii.get(self, "egressPolicy"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(
        self,
    ) -> BeyondcorpSecurityGatewayApplicationUpstreamsNetworkOutputReference:
        return typing.cast(BeyondcorpSecurityGatewayApplicationUpstreamsNetworkOutputReference, jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="egressPolicyInput")
    def egress_policy_input(
        self,
    ) -> typing.Optional[BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicy]:
        return typing.cast(typing.Optional[BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicy], jsii.get(self, "egressPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(
        self,
    ) -> typing.Optional[BeyondcorpSecurityGatewayApplicationUpstreamsNetwork]:
        return typing.cast(typing.Optional[BeyondcorpSecurityGatewayApplicationUpstreamsNetwork], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BeyondcorpSecurityGatewayApplicationUpstreams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BeyondcorpSecurityGatewayApplicationUpstreams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BeyondcorpSecurityGatewayApplicationUpstreams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f196d0cb543094aa71d1a2ece836dd3011c059db9cb8a5b34ae111c59bf62692)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BeyondcorpSecurityGatewayApplication",
    "BeyondcorpSecurityGatewayApplicationConfig",
    "BeyondcorpSecurityGatewayApplicationEndpointMatchers",
    "BeyondcorpSecurityGatewayApplicationEndpointMatchersList",
    "BeyondcorpSecurityGatewayApplicationEndpointMatchersOutputReference",
    "BeyondcorpSecurityGatewayApplicationTimeouts",
    "BeyondcorpSecurityGatewayApplicationTimeoutsOutputReference",
    "BeyondcorpSecurityGatewayApplicationUpstreams",
    "BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicy",
    "BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicyOutputReference",
    "BeyondcorpSecurityGatewayApplicationUpstreamsList",
    "BeyondcorpSecurityGatewayApplicationUpstreamsNetwork",
    "BeyondcorpSecurityGatewayApplicationUpstreamsNetworkOutputReference",
    "BeyondcorpSecurityGatewayApplicationUpstreamsOutputReference",
]

publication.publish()

def _typecheckingstub__bbc5bd11ac1ce6cf9f33abf938547589a84fda544ac2a0d2611341af916d9112(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    application_id: builtins.str,
    endpoint_matchers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BeyondcorpSecurityGatewayApplicationEndpointMatchers, typing.Dict[builtins.str, typing.Any]]]],
    security_gateway_id: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BeyondcorpSecurityGatewayApplicationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upstreams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BeyondcorpSecurityGatewayApplicationUpstreams, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__736631b0b0b291412bb9e5c788d083802619c2565f8d6c390ba354544164d351(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2c5acc042308437a47d2beaa8186bc3cec524a84e3097b75e15e2810935efc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BeyondcorpSecurityGatewayApplicationEndpointMatchers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5584f4e12f1f43ff2c44f8a2a6c8fb446fabeb77f713f341e01e6d124b39026b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BeyondcorpSecurityGatewayApplicationUpstreams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__593cd6c5c0e8ea89e1078167eb6b31ebe0abc0f1cdf18448cd98c7e9e5fd1cd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f693650d9311e02def1afb8ac5860a3f2768bfa2688b2854c132b44abf009300(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63202678fd8d6cf0a549c07d7f7ffdedcd8828501c1521bbdf104043cf76c243(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65c2469a3f1944e7effbb934f01b5513d1db3ad5d6b8fc50e2ea94abf0e9ac1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fffb2067a3c2960dd170daec4a68c88bfd12598bbbd0ac99f2e2eecc1db2a4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737bae195119be6189df221c6786500fdaa694075014c35c41f188c605dc9bd9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    application_id: builtins.str,
    endpoint_matchers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BeyondcorpSecurityGatewayApplicationEndpointMatchers, typing.Dict[builtins.str, typing.Any]]]],
    security_gateway_id: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BeyondcorpSecurityGatewayApplicationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upstreams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BeyondcorpSecurityGatewayApplicationUpstreams, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aeb844e2b338b1cd14edb60c950f9a28d821777d1609b299de34c17218d7238(
    *,
    hostname: builtins.str,
    ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e780fa01a0eb5d1e734cee3a9f915b1a8ff91d920311f3984809429b970eed7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177b7a4e82727a80182510a700965684ebddea2bfcac0ee6f22f02e80463824e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__364385b2503002430e822db5a52b712c08861fba0d7400e88feee921820f8989(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a147c3501213a5a526b1949718c84d096ddc0bd93d0bb2d593e874047ae389de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982061f849e286266b143a53e9fffdf001808a27264a6bfa2cb89b6b2fe694fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9821b8e2ac0b296fa8dc6e73e6b30b89dd01d95206f2a0ea1c8c2b31d7268d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BeyondcorpSecurityGatewayApplicationEndpointMatchers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd27ae8459ac8aa11b4d5d1e086b43959433ab5148c1d20c2da60f7318c011ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d3ccbfe1cf232f24218681f31b374b5e6e9ebd03591f8960a7dbdab60b570fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e83e43e0ba9a4237040cb986dcadfe0e99668339644bddaf272c098c6c3419c(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f9433c2b394fe72d6c6d94066c68a49a52add30d027e0ff1394d7ffdcde9b87(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BeyondcorpSecurityGatewayApplicationEndpointMatchers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552bd8d881d245664ba1966204f0fe735addf1f65efbb4362dac9f469982cbc7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d53088a9fbfa2ebcab680ade03d72cea97d302f1c1e9c92eb8b9310c2b57f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfbcc02d0d08830b289004d2306db7025d607ea9b46b9600320874d377d2ea58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3ac26799c7a55d65d20b66c8a676b6d5c0e616672697e543e7981ef51a3fba3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ec1a6e05816a051126b57a0aea0b53987a12053221408074409e4f5059f4b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bceb4a964510ec4807fbb7da3f50e407d1e32894867ce8dad71e689fb44eece(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BeyondcorpSecurityGatewayApplicationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e027ca2ba3bb146414babb53fde0d47d3057ad1a9fa4fd65210ff60a3f5308eb(
    *,
    egress_policy: typing.Optional[typing.Union[BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[BeyondcorpSecurityGatewayApplicationUpstreamsNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6cf92df358664b9a4b60a78abf3f110085c291b8da90f6c729e8b8934024670(
    *,
    regions: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c767026d9c8b5973a6420cc75667095f9e62a55eab33b55512a6b9a5bbaa9a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__302de0318353312951d667c0665a9e4737e679e5b3d659a7384f4d6b25ace741(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49dc344b2389da77656da97a1492cf766c7a6c0ad7cfb34fd27d6ca47a41ab10(
    value: typing.Optional[BeyondcorpSecurityGatewayApplicationUpstreamsEgressPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea8d2487ed490a450037ba5e2186f2721820d7249cbf15d005329e985b021872(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3dfc1563bb4669b2e9339cf88eabb8f3cee0d3b8c7491c11e9c239da338cdb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21454b047168df39e66b4d3b99fe574daeddf4a4d4b6a494cb3b8c0a0d48f8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00e058a98b14fa0f4b095c90f55dd602541f57a69ab8735562e2d09e7f4665e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57651c0cd5916cd09edf43be846261808ec76b57c51932e56bc24332e116d46f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd47bbda42e63839baabac20f6ea86071d0c582fb00511f31a627cd470ac8de6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BeyondcorpSecurityGatewayApplicationUpstreams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0d7c7b1d0b021bfc3d1b01b4db22f4e46c9d39c62cba3dd91fd6127aeb92be7(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec08d069b063c9086364317ffd8cf1a829d522569fbbfb7446ba351366d3f5d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215c89e44187f4776475da712947ff95383d80a587fa4c8c083d2ce8136dc131(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c91f6b0a91c07b693b8a01c1f0230a03a10f7b8a9faf22ab22ba90147d0780(
    value: typing.Optional[BeyondcorpSecurityGatewayApplicationUpstreamsNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af4616a8db211758e128ac0c4fb34be4507b37b67f4c99b5640f59aabd8b1fd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f196d0cb543094aa71d1a2ece836dd3011c059db9cb8a5b34ae111c59bf62692(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BeyondcorpSecurityGatewayApplicationUpstreams]],
) -> None:
    """Type checking stubs"""
    pass

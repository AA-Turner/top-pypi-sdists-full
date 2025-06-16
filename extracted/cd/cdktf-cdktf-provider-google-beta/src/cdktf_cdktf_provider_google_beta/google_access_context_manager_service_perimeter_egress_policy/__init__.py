r'''
# `google_access_context_manager_service_perimeter_egress_policy`

Refer to the Terraform Registry for docs: [`google_access_context_manager_service_perimeter_egress_policy`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy).
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


class GoogleAccessContextManagerServicePerimeterEgressPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeterEgressPolicy.GoogleAccessContextManagerServicePerimeterEgressPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy google_access_context_manager_service_perimeter_egress_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        perimeter: builtins.str,
        egress_from: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        egress_to: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy google_access_context_manager_service_perimeter_egress_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param perimeter: The name of the Service Perimeter to add this resource to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#perimeter GoogleAccessContextManagerServicePerimeterEgressPolicy#perimeter}
        :param egress_from: egress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#egress_from GoogleAccessContextManagerServicePerimeterEgressPolicy#egress_from}
        :param egress_to: egress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#egress_to GoogleAccessContextManagerServicePerimeterEgressPolicy#egress_to}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#id GoogleAccessContextManagerServicePerimeterEgressPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#timeouts GoogleAccessContextManagerServicePerimeterEgressPolicy#timeouts}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#title GoogleAccessContextManagerServicePerimeterEgressPolicy#title}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__447be0f890426f3419a92b2164944be31fd3cb14321c7badc1ed76c878b6c01c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleAccessContextManagerServicePerimeterEgressPolicyConfig(
            perimeter=perimeter,
            egress_from=egress_from,
            egress_to=egress_to,
            id=id,
            timeouts=timeouts,
            title=title,
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
        '''Generates CDKTF code for importing a GoogleAccessContextManagerServicePerimeterEgressPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleAccessContextManagerServicePerimeterEgressPolicy to import.
        :param import_from_id: The id of the existing GoogleAccessContextManagerServicePerimeterEgressPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleAccessContextManagerServicePerimeterEgressPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7938fd9989518a5668dbde30c6c437bceb18f0aa36d949d96416839ab561e935)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEgressFrom")
    def put_egress_from(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        source_restriction: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: Identities can be an individual user, service account, Google group, or third-party identity. For third-party identity, only single identities are supported and other identity types are not supported.The v1 identities that have the prefix user, group and serviceAccount in https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#identities GoogleAccessContextManagerServicePerimeterEgressPolicy#identities}
        :param identity_type: Specifies the type of identities that are allowed access to outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#identity_type GoogleAccessContextManagerServicePerimeterEgressPolicy#identity_type}
        :param source_restriction: Whether to enforce traffic restrictions based on 'sources' field. If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#source_restriction GoogleAccessContextManagerServicePerimeterEgressPolicy#source_restriction}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#sources GoogleAccessContextManagerServicePerimeterEgressPolicy#sources}
        '''
        value = GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom(
            identities=identities,
            identity_type=identity_type,
            source_restriction=source_restriction,
            sources=sources,
        )

        return typing.cast(None, jsii.invoke(self, "putEgressFrom", [value]))

    @jsii.member(jsii_name="putEgressTo")
    def put_egress_to(
        self,
        *,
        external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param external_resources: A list of external resources that are allowed to be accessed. A request matches if it contains an external resource in this list (Example: s3://bucket/path). Currently '*' is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#external_resources GoogleAccessContextManagerServicePerimeterEgressPolicy#external_resources}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#operations GoogleAccessContextManagerServicePerimeterEgressPolicy#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', that match this to stanza. A request matches if it contains a resource in this list. If * is specified for resources, then this 'EgressTo' rule will authorize access to all resources outside the perimeter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#resources GoogleAccessContextManagerServicePerimeterEgressPolicy#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#roles GoogleAccessContextManagerServicePerimeterEgressPolicy#roles}
        '''
        value = GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo(
            external_resources=external_resources,
            operations=operations,
            resources=resources,
            roles=roles,
        )

        return typing.cast(None, jsii.invoke(self, "putEgressTo", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#create GoogleAccessContextManagerServicePerimeterEgressPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#delete GoogleAccessContextManagerServicePerimeterEgressPolicy#delete}.
        '''
        value = GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts(
            create=create, delete=delete
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetEgressFrom")
    def reset_egress_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressFrom", []))

    @jsii.member(jsii_name="resetEgressTo")
    def reset_egress_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressTo", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

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
    @jsii.member(jsii_name="accessPolicyId")
    def access_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessPolicyId"))

    @builtins.property
    @jsii.member(jsii_name="egressFrom")
    def egress_from(
        self,
    ) -> "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromOutputReference":
        return typing.cast("GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromOutputReference", jsii.get(self, "egressFrom"))

    @builtins.property
    @jsii.member(jsii_name="egressTo")
    def egress_to(
        self,
    ) -> "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOutputReference":
        return typing.cast("GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOutputReference", jsii.get(self, "egressTo"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleAccessContextManagerServicePerimeterEgressPolicyTimeoutsOutputReference":
        return typing.cast("GoogleAccessContextManagerServicePerimeterEgressPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="egressFromInput")
    def egress_from_input(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom"]:
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom"], jsii.get(self, "egressFromInput"))

    @builtins.property
    @jsii.member(jsii_name="egressToInput")
    def egress_to_input(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo"]:
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo"], jsii.get(self, "egressToInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="perimeterInput")
    def perimeter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "perimeterInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__214e41cf7fdece3db6874e486264b77bd932ed6883f2de4adb1a589d48691793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="perimeter")
    def perimeter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "perimeter"))

    @perimeter.setter
    def perimeter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38642aa28a05708376e9d55f69160a9908fa9fcfe25d949019ec3e20d5f280da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perimeter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab387f1d87ab68028e51ea166166a23fef74757d7b1e6577a7cb97a2451b79a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeterEgressPolicy.GoogleAccessContextManagerServicePerimeterEgressPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "perimeter": "perimeter",
        "egress_from": "egressFrom",
        "egress_to": "egressTo",
        "id": "id",
        "timeouts": "timeouts",
        "title": "title",
    },
)
class GoogleAccessContextManagerServicePerimeterEgressPolicyConfig(
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
        perimeter: builtins.str,
        egress_from: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        egress_to: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param perimeter: The name of the Service Perimeter to add this resource to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#perimeter GoogleAccessContextManagerServicePerimeterEgressPolicy#perimeter}
        :param egress_from: egress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#egress_from GoogleAccessContextManagerServicePerimeterEgressPolicy#egress_from}
        :param egress_to: egress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#egress_to GoogleAccessContextManagerServicePerimeterEgressPolicy#egress_to}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#id GoogleAccessContextManagerServicePerimeterEgressPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#timeouts GoogleAccessContextManagerServicePerimeterEgressPolicy#timeouts}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#title GoogleAccessContextManagerServicePerimeterEgressPolicy#title}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(egress_from, dict):
            egress_from = GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom(**egress_from)
        if isinstance(egress_to, dict):
            egress_to = GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo(**egress_to)
        if isinstance(timeouts, dict):
            timeouts = GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9553a24e92c4b64eb60d0d71dbc2f0e0f7f9ade58a085a78ed5e9dc30b2e6bd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument perimeter", value=perimeter, expected_type=type_hints["perimeter"])
            check_type(argname="argument egress_from", value=egress_from, expected_type=type_hints["egress_from"])
            check_type(argname="argument egress_to", value=egress_to, expected_type=type_hints["egress_to"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "perimeter": perimeter,
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
        if egress_from is not None:
            self._values["egress_from"] = egress_from
        if egress_to is not None:
            self._values["egress_to"] = egress_to
        if id is not None:
            self._values["id"] = id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if title is not None:
            self._values["title"] = title

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
    def perimeter(self) -> builtins.str:
        '''The name of the Service Perimeter to add this resource to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#perimeter GoogleAccessContextManagerServicePerimeterEgressPolicy#perimeter}
        '''
        result = self._values.get("perimeter")
        assert result is not None, "Required property 'perimeter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def egress_from(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom"]:
        '''egress_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#egress_from GoogleAccessContextManagerServicePerimeterEgressPolicy#egress_from}
        '''
        result = self._values.get("egress_from")
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom"], result)

    @builtins.property
    def egress_to(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo"]:
        '''egress_to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#egress_to GoogleAccessContextManagerServicePerimeterEgressPolicy#egress_to}
        '''
        result = self._values.get("egress_to")
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#id GoogleAccessContextManagerServicePerimeterEgressPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#timeouts GoogleAccessContextManagerServicePerimeterEgressPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts"], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Human readable title. Must be unique within the perimeter. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#title GoogleAccessContextManagerServicePerimeterEgressPolicy#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimeterEgressPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeterEgressPolicy.GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom",
    jsii_struct_bases=[],
    name_mapping={
        "identities": "identities",
        "identity_type": "identityType",
        "source_restriction": "sourceRestriction",
        "sources": "sources",
    },
)
class GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom:
    def __init__(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        source_restriction: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: Identities can be an individual user, service account, Google group, or third-party identity. For third-party identity, only single identities are supported and other identity types are not supported.The v1 identities that have the prefix user, group and serviceAccount in https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#identities GoogleAccessContextManagerServicePerimeterEgressPolicy#identities}
        :param identity_type: Specifies the type of identities that are allowed access to outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#identity_type GoogleAccessContextManagerServicePerimeterEgressPolicy#identity_type}
        :param source_restriction: Whether to enforce traffic restrictions based on 'sources' field. If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#source_restriction GoogleAccessContextManagerServicePerimeterEgressPolicy#source_restriction}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#sources GoogleAccessContextManagerServicePerimeterEgressPolicy#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92146faf7b908eb8de44ed38ce4c7f3eb367b221d2a85d5979c6a02d15aa1e2d)
            check_type(argname="argument identities", value=identities, expected_type=type_hints["identities"])
            check_type(argname="argument identity_type", value=identity_type, expected_type=type_hints["identity_type"])
            check_type(argname="argument source_restriction", value=source_restriction, expected_type=type_hints["source_restriction"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identities is not None:
            self._values["identities"] = identities
        if identity_type is not None:
            self._values["identity_type"] = identity_type
        if source_restriction is not None:
            self._values["source_restriction"] = source_restriction
        if sources is not None:
            self._values["sources"] = sources

    @builtins.property
    def identities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Identities can be an individual user, service account, Google group, or third-party identity.

        For third-party identity, only single identities
        are supported and other identity types are not supported.The v1 identities
        that have the prefix user, group and serviceAccount in
        https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#identities GoogleAccessContextManagerServicePerimeterEgressPolicy#identities}
        '''
        result = self._values.get("identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of identities that are allowed access to outside the perimeter.

        If left unspecified, then members of 'identities' field will
        be allowed access. Possible values: ["ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#identity_type GoogleAccessContextManagerServicePerimeterEgressPolicy#identity_type}
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_restriction(self) -> typing.Optional[builtins.str]:
        '''Whether to enforce traffic restrictions based on 'sources' field.

        If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#source_restriction GoogleAccessContextManagerServicePerimeterEgressPolicy#source_restriction}
        '''
        result = self._values.get("source_restriction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources"]]]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#sources GoogleAccessContextManagerServicePerimeterEgressPolicy#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeterEgressPolicy.GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1b4526ddff9bb8fd07c6283b5a7142e9e5c3a69f8a8da488cd686b1b333a676)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4829da2226ab35eff7499a72cda37ddb6c5b33e5b4cdbae189fc335a616b96dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSources", [value]))

    @jsii.member(jsii_name="resetIdentities")
    def reset_identities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentities", []))

    @jsii.member(jsii_name="resetIdentityType")
    def reset_identity_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityType", []))

    @jsii.member(jsii_name="resetSourceRestriction")
    def reset_source_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceRestriction", []))

    @jsii.member(jsii_name="resetSources")
    def reset_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSources", []))

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSourcesList":
        return typing.cast("GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSourcesList", jsii.get(self, "sources"))

    @builtins.property
    @jsii.member(jsii_name="identitiesInput")
    def identities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="identityTypeInput")
    def identity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceRestrictionInput")
    def source_restriction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources"]]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="identities")
    def identities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identities"))

    @identities.setter
    def identities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27667d23ba1b0c2b9497981224ff5f56cd452a51fee684340248405cf1389bf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityType")
    def identity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityType"))

    @identity_type.setter
    def identity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9e3698001bb92e2ee10f09b630acefc2d8c29f5cb2db68204232879fb1b106)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceRestriction")
    def source_restriction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceRestriction"))

    @source_restriction.setter
    def source_restriction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d70c697753fef7bfe7ed07245f6fd6c90c21c4e203a4bab39dbef8a9359e8f7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceRestriction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4225ce491995832fb638d719089e27194f4660013539e3e986d9bb266a32eb73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeterEgressPolicy.GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources",
    jsii_struct_bases=[],
    name_mapping={"access_level": "accessLevel", "resource": "resource"},
)
class GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_level: An AccessLevel resource name that allows resources outside the ServicePerimeter to be accessed from the inside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#access_level GoogleAccessContextManagerServicePerimeterEgressPolicy#access_level}
        :param resource: A Google Cloud resource that is allowed to egress the perimeter. Requests from these resources are allowed to access data outside the perimeter. Currently only projects are allowed. Project format: 'projects/{project_number}'. The resource may be in any Google Cloud organization, not just the organization that the perimeter is defined in. '*' is not allowed, the case of allowing all Google Cloud resources only is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#resource GoogleAccessContextManagerServicePerimeterEgressPolicy#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4705119176aa5be3b552fe7dc19bcb7d848d58be9d84179645e3f5957048040)
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_level is not None:
            self._values["access_level"] = access_level
        if resource is not None:
            self._values["resource"] = resource

    @builtins.property
    def access_level(self) -> typing.Optional[builtins.str]:
        '''An AccessLevel resource name that allows resources outside the ServicePerimeter to be accessed from the inside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#access_level GoogleAccessContextManagerServicePerimeterEgressPolicy#access_level}
        '''
        result = self._values.get("access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''A Google Cloud resource that is allowed to egress the perimeter.

        Requests from these resources are allowed to access data outside the perimeter.
        Currently only projects are allowed. Project format: 'projects/{project_number}'.
        The resource may be in any Google Cloud organization, not just the
        organization that the perimeter is defined in. '*' is not allowed, the
        case of allowing all Google Cloud resources only is not supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#resource GoogleAccessContextManagerServicePerimeterEgressPolicy#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeterEgressPolicy.GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fc0798415c34638eb45dfeccf614027432da57655755bbc33f972065c4a271f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__173162f29d5e65cfbae3aac0770e52a486e96995adeeeb0e51ca43fd510252b9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03df08a67ab07c4c69cb4edadc05a03848d83d6f7d16410b9212c9897b9d1a08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fe2c33aed00f72e62644c8d0a7f88f475baace6f2d0e1397b591f67df816688)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a264e6331aea02854e04d1fbd151fbc5cf41f2001a5a33eec472c3c2224d280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9bdb8e2cde4dad4d7f69199d83fef94e0e78cf8bd8c87fa09d649c0f3c23a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeterEgressPolicy.GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7596d3816c582059d2d14e93c52b7daae3da58188fe17a1dd15ed9163747388c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessLevel")
    def reset_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevel", []))

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @builtins.property
    @jsii.member(jsii_name="accessLevelInput")
    def access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevel")
    def access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevel"))

    @access_level.setter
    def access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84f01a0694dffc448be425379c3d581cf2c2d7dbe35aa6a4c91a86007f3d5972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3615bc7b41eb977ff6122a237ead34d20edeef27d434550f5c292e070a4c5260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57d602b8b84f886d26296425eb90bd926f1f1d40aa618c7142543872c1672f5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeterEgressPolicy.GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo",
    jsii_struct_bases=[],
    name_mapping={
        "external_resources": "externalResources",
        "operations": "operations",
        "resources": "resources",
        "roles": "roles",
    },
)
class GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo:
    def __init__(
        self,
        *,
        external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param external_resources: A list of external resources that are allowed to be accessed. A request matches if it contains an external resource in this list (Example: s3://bucket/path). Currently '*' is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#external_resources GoogleAccessContextManagerServicePerimeterEgressPolicy#external_resources}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#operations GoogleAccessContextManagerServicePerimeterEgressPolicy#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', that match this to stanza. A request matches if it contains a resource in this list. If * is specified for resources, then this 'EgressTo' rule will authorize access to all resources outside the perimeter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#resources GoogleAccessContextManagerServicePerimeterEgressPolicy#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#roles GoogleAccessContextManagerServicePerimeterEgressPolicy#roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65e3cd9115e8f7bf09d1edf936f5110783d2c28403306758fda52e920fda3a39)
            check_type(argname="argument external_resources", value=external_resources, expected_type=type_hints["external_resources"])
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if external_resources is not None:
            self._values["external_resources"] = external_resources
        if operations is not None:
            self._values["operations"] = operations
        if resources is not None:
            self._values["resources"] = resources
        if roles is not None:
            self._values["roles"] = roles

    @builtins.property
    def external_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of external resources that are allowed to be accessed.

        A request
        matches if it contains an external resource in this list (Example:
        s3://bucket/path). Currently '*' is not allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#external_resources GoogleAccessContextManagerServicePerimeterEgressPolicy#external_resources}
        '''
        result = self._values.get("external_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#operations GoogleAccessContextManagerServicePerimeterEgressPolicy#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resources, currently only projects in the form 'projects/', that match this to stanza.

        A request matches
        if it contains a resource in this list. If * is specified for resources,
        then this 'EgressTo' rule will authorize access to all resources outside
        the perimeter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#resources GoogleAccessContextManagerServicePerimeterEgressPolicy#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#roles GoogleAccessContextManagerServicePerimeterEgressPolicy#roles}
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeterEgressPolicy.GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations",
    jsii_struct_bases=[],
    name_mapping={
        "method_selectors": "methodSelectors",
        "service_name": "serviceName",
    },
)
class GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations:
    def __init__(
        self,
        *,
        method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method_selectors: method_selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#method_selectors GoogleAccessContextManagerServicePerimeterEgressPolicy#method_selectors}
        :param service_name: The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow. A single 'ApiOperation' with serviceName field set to '*' will allow all methods AND permissions for all services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#service_name GoogleAccessContextManagerServicePerimeterEgressPolicy#service_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7fce8b8789885e6de168503d4ce0bdfb59599d6253e99db036840aa425fa810)
            check_type(argname="argument method_selectors", value=method_selectors, expected_type=type_hints["method_selectors"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method_selectors is not None:
            self._values["method_selectors"] = method_selectors
        if service_name is not None:
            self._values["service_name"] = service_name

    @builtins.property
    def method_selectors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors"]]]:
        '''method_selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#method_selectors GoogleAccessContextManagerServicePerimeterEgressPolicy#method_selectors}
        '''
        result = self._values.get("method_selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors"]]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow.

        A single 'ApiOperation' with serviceName
        field set to '*' will allow all methods AND permissions for all services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#service_name GoogleAccessContextManagerServicePerimeterEgressPolicy#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeterEgressPolicy.GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6013f813f865df7bad004aa9d7ed9e52c39b9032c3df498a24435f36e127ab0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09bf98e3a2b771071aede2f426a65a06668da4213319ec04cb52854c87ef47eb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56e1400629f59f27df98ec68f650fa7fa04b212e2338b412903dc2780607692)
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
            type_hints = typing.get_type_hints(_typecheckingstub__443fb41a9577f41553f632bb74fcb1daaecd4e390e9db82851c2561b8a955d1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce9ddab52bd6df3a877b86a01a66a01d4d0cc98fa3463df6e87f9b0a276afbcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f07f36008df5b0b5f274a1b04a59aac1227403d7b2029ae00d5dd0dfb639363f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeterEgressPolicy.GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "permission": "permission"},
)
class GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors:
    def __init__(
        self,
        *,
        method: typing.Optional[builtins.str] = None,
        permission: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method: Value for 'method' should be a valid method name for the corresponding 'serviceName' in 'ApiOperation'. If '*' used as value for method, then ALL methods and permissions are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#method GoogleAccessContextManagerServicePerimeterEgressPolicy#method}
        :param permission: Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#permission GoogleAccessContextManagerServicePerimeterEgressPolicy#permission}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b417959aa188780e52058ffeec64b3ed1441724f97029830bde72c07c0a2eee8)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if permission is not None:
            self._values["permission"] = permission

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Value for 'method' should be a valid method name for the corresponding 'serviceName' in 'ApiOperation'.

        If '*' used as value for method,
        then ALL methods and permissions are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#method GoogleAccessContextManagerServicePerimeterEgressPolicy#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission(self) -> typing.Optional[builtins.str]:
        '''Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#permission GoogleAccessContextManagerServicePerimeterEgressPolicy#permission}
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeterEgressPolicy.GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4cba2dda3148380cea021fdd662ea862661b223563e6a5592cd7dbaebf86fe1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2451b5e3c2c7f25ddf39d94b05f4f2c6326f998828f0b9196a5ccded90aedfc7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac2e24fb54c0f860f2ca05448ee95c9c3396393aa4002c2db8826a44bae7a846)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56df7c12ccf1f65125ffb3ab355729c5fe327adbfe406869e943ff92310aef4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39398cec531a42e3c3db78ef8c7417ae077c5ac7254474c6392748e6a1891605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dee2b146b84b007972b740dbb4c4adb1c68b206c874468682b3d25a722d397c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeterEgressPolicy.GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af329b4e2f78b20457ff64d2ce1263b82c20ecfaafd928c8f185d550f2f59cb7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetPermission")
    def reset_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermission", []))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionInput")
    def permission_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionInput"))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b389343389c0da2893e8f3dceb7ec20c6b9d89c2b8d53e4f3c1e78c58d4405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d391a47f3df11862b45eae2df9fb1dfbb73765da98e358df05e6ec614209a3c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed9349c7355b64c6312bb04e884cbf2f114a478d94574f08400f8de23a14245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeterEgressPolicy.GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12ee78bd6837c8027eac3bf01e805084fbfcf8eee350c4e7a82ce56cdf859969)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMethodSelectors")
    def put_method_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9342520309e80eae9ae12dc07a2aa966dcccdf8935526cc18420f29842f2a27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMethodSelectors", [value]))

    @jsii.member(jsii_name="resetMethodSelectors")
    def reset_method_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethodSelectors", []))

    @jsii.member(jsii_name="resetServiceName")
    def reset_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceName", []))

    @builtins.property
    @jsii.member(jsii_name="methodSelectors")
    def method_selectors(
        self,
    ) -> GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectorsList:
        return typing.cast(GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectorsList, jsii.get(self, "methodSelectors"))

    @builtins.property
    @jsii.member(jsii_name="methodSelectorsInput")
    def method_selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors]]], jsii.get(self, "methodSelectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0096877979904687bebd654de9b95c3dda2c17531b04ea778ae29bf921a75e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ca2539690d59775648c376d1d350b30e7a280c066128ed4bb774386ea0ae787)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeterEgressPolicy.GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de7ab692e31ffa31d8e27c44dd8c5dc8c588e795e770bd84a24d4f3dee3afcf6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdec6722d54dd7b72d420d17384ebf7ef27814a08e26866e8f718d749e94c6d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperations", [value]))

    @jsii.member(jsii_name="resetExternalResources")
    def reset_external_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalResources", []))

    @jsii.member(jsii_name="resetOperations")
    def reset_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperations", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetRoles")
    def reset_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoles", []))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(
        self,
    ) -> GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsList:
        return typing.cast(GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="externalResourcesInput")
    def external_resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations]]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="externalResources")
    def external_resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalResources"))

    @external_resources.setter
    def external_resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcedf34ac967be3c87884b77776d3a8546fe04cd79c64a4a79796c283d129422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d682a1fe6f30ebce8770cb46df6bb49b2ebe596d8e8c3be375fab12c200645d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac32893c5ca3d28dd2c1ffb26e056434e725abf76f09b8334c19b7790f769a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7297b968ce53b5383da1177bae660680818480dd01186561d615e445ac8e5250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeterEgressPolicy.GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#create GoogleAccessContextManagerServicePerimeterEgressPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#delete GoogleAccessContextManagerServicePerimeterEgressPolicy#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49dc0feae35ec35031b046866345b34fce22eb7020e1c3f078756fd51db056d7)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#create GoogleAccessContextManagerServicePerimeterEgressPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeter_egress_policy#delete GoogleAccessContextManagerServicePerimeterEgressPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimeterEgressPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeterEgressPolicy.GoogleAccessContextManagerServicePerimeterEgressPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__031c160b95939bf15153d28ab6cbba7e3bdfb3d5699157e6f7b7dc66a043db29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d17ce9061f96bf63370c0d4ad9a403bf5f7bfca3adfb15a811ba09b5253ca73d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e9f16a09fae84b3140b7ccc1fff76c7c8c23b487c3aedb8a6f1e59db92b0ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e80ca691a7258dcbcc26db01bc8fb964624f2344b843af1193b5700c3599c0d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleAccessContextManagerServicePerimeterEgressPolicy",
    "GoogleAccessContextManagerServicePerimeterEgressPolicyConfig",
    "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom",
    "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromOutputReference",
    "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources",
    "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSourcesList",
    "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSourcesOutputReference",
    "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo",
    "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations",
    "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsList",
    "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors",
    "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectorsList",
    "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectorsOutputReference",
    "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsOutputReference",
    "GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOutputReference",
    "GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts",
    "GoogleAccessContextManagerServicePerimeterEgressPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__447be0f890426f3419a92b2164944be31fd3cb14321c7badc1ed76c878b6c01c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    perimeter: builtins.str,
    egress_from: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    egress_to: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__7938fd9989518a5668dbde30c6c437bceb18f0aa36d949d96416839ab561e935(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214e41cf7fdece3db6874e486264b77bd932ed6883f2de4adb1a589d48691793(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38642aa28a05708376e9d55f69160a9908fa9fcfe25d949019ec3e20d5f280da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab387f1d87ab68028e51ea166166a23fef74757d7b1e6577a7cb97a2451b79a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9553a24e92c4b64eb60d0d71dbc2f0e0f7f9ade58a085a78ed5e9dc30b2e6bd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    perimeter: builtins.str,
    egress_from: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    egress_to: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92146faf7b908eb8de44ed38ce4c7f3eb367b221d2a85d5979c6a02d15aa1e2d(
    *,
    identities: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    source_restriction: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b4526ddff9bb8fd07c6283b5a7142e9e5c3a69f8a8da488cd686b1b333a676(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4829da2226ab35eff7499a72cda37ddb6c5b33e5b4cdbae189fc335a616b96dc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27667d23ba1b0c2b9497981224ff5f56cd452a51fee684340248405cf1389bf5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9e3698001bb92e2ee10f09b630acefc2d8c29f5cb2db68204232879fb1b106(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d70c697753fef7bfe7ed07245f6fd6c90c21c4e203a4bab39dbef8a9359e8f7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4225ce491995832fb638d719089e27194f4660013539e3e986d9bb266a32eb73(
    value: typing.Optional[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4705119176aa5be3b552fe7dc19bcb7d848d58be9d84179645e3f5957048040(
    *,
    access_level: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc0798415c34638eb45dfeccf614027432da57655755bbc33f972065c4a271f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173162f29d5e65cfbae3aac0770e52a486e96995adeeeb0e51ca43fd510252b9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03df08a67ab07c4c69cb4edadc05a03848d83d6f7d16410b9212c9897b9d1a08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe2c33aed00f72e62644c8d0a7f88f475baace6f2d0e1397b591f67df816688(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a264e6331aea02854e04d1fbd151fbc5cf41f2001a5a33eec472c3c2224d280(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9bdb8e2cde4dad4d7f69199d83fef94e0e78cf8bd8c87fa09d649c0f3c23a3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7596d3816c582059d2d14e93c52b7daae3da58188fe17a1dd15ed9163747388c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f01a0694dffc448be425379c3d581cf2c2d7dbe35aa6a4c91a86007f3d5972(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3615bc7b41eb977ff6122a237ead34d20edeef27d434550f5c292e070a4c5260(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d602b8b84f886d26296425eb90bd926f1f1d40aa618c7142543872c1672f5e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimeterEgressPolicyEgressFromSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e3cd9115e8f7bf09d1edf936f5110783d2c28403306758fda52e920fda3a39(
    *,
    external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7fce8b8789885e6de168503d4ce0bdfb59599d6253e99db036840aa425fa810(
    *,
    method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6013f813f865df7bad004aa9d7ed9e52c39b9032c3df498a24435f36e127ab0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09bf98e3a2b771071aede2f426a65a06668da4213319ec04cb52854c87ef47eb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56e1400629f59f27df98ec68f650fa7fa04b212e2338b412903dc2780607692(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443fb41a9577f41553f632bb74fcb1daaecd4e390e9db82851c2561b8a955d1f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9ddab52bd6df3a877b86a01a66a01d4d0cc98fa3463df6e87f9b0a276afbcb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07f36008df5b0b5f274a1b04a59aac1227403d7b2029ae00d5dd0dfb639363f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b417959aa188780e52058ffeec64b3ed1441724f97029830bde72c07c0a2eee8(
    *,
    method: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4cba2dda3148380cea021fdd662ea862661b223563e6a5592cd7dbaebf86fe1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2451b5e3c2c7f25ddf39d94b05f4f2c6326f998828f0b9196a5ccded90aedfc7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2e24fb54c0f860f2ca05448ee95c9c3396393aa4002c2db8826a44bae7a846(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56df7c12ccf1f65125ffb3ab355729c5fe327adbfe406869e943ff92310aef4f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39398cec531a42e3c3db78ef8c7417ae077c5ac7254474c6392748e6a1891605(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee2b146b84b007972b740dbb4c4adb1c68b206c874468682b3d25a722d397c7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af329b4e2f78b20457ff64d2ce1263b82c20ecfaafd928c8f185d550f2f59cb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b389343389c0da2893e8f3dceb7ec20c6b9d89c2b8d53e4f3c1e78c58d4405(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d391a47f3df11862b45eae2df9fb1dfbb73765da98e358df05e6ec614209a3c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed9349c7355b64c6312bb04e884cbf2f114a478d94574f08400f8de23a14245(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ee78bd6837c8027eac3bf01e805084fbfcf8eee350c4e7a82ce56cdf859969(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9342520309e80eae9ae12dc07a2aa966dcccdf8935526cc18420f29842f2a27(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0096877979904687bebd654de9b95c3dda2c17531b04ea778ae29bf921a75e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca2539690d59775648c376d1d350b30e7a280c066128ed4bb774386ea0ae787(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7ab692e31ffa31d8e27c44dd8c5dc8c588e795e770bd84a24d4f3dee3afcf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdec6722d54dd7b72d420d17384ebf7ef27814a08e26866e8f718d749e94c6d7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressToOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcedf34ac967be3c87884b77776d3a8546fe04cd79c64a4a79796c283d129422(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d682a1fe6f30ebce8770cb46df6bb49b2ebe596d8e8c3be375fab12c200645d8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac32893c5ca3d28dd2c1ffb26e056434e725abf76f09b8334c19b7790f769a6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7297b968ce53b5383da1177bae660680818480dd01186561d615e445ac8e5250(
    value: typing.Optional[GoogleAccessContextManagerServicePerimeterEgressPolicyEgressTo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49dc0feae35ec35031b046866345b34fce22eb7020e1c3f078756fd51db056d7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031c160b95939bf15153d28ab6cbba7e3bdfb3d5699157e6f7b7dc66a043db29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17ce9061f96bf63370c0d4ad9a403bf5f7bfca3adfb15a811ba09b5253ca73d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e9f16a09fae84b3140b7ccc1fff76c7c8c23b487c3aedb8a6f1e59db92b0ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80ca691a7258dcbcc26db01bc8fb964624f2344b843af1193b5700c3599c0d5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimeterEgressPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

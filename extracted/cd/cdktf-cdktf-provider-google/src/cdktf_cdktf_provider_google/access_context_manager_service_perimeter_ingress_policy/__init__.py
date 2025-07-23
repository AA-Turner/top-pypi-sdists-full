r'''
# `google_access_context_manager_service_perimeter_ingress_policy`

Refer to the Terraform Registry for docs: [`google_access_context_manager_service_perimeter_ingress_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy).
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


class AccessContextManagerServicePerimeterIngressPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterIngressPolicy.AccessContextManagerServicePerimeterIngressPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy google_access_context_manager_service_perimeter_ingress_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        perimeter: builtins.str,
        id: typing.Optional[builtins.str] = None,
        ingress_from: typing.Optional[typing.Union["AccessContextManagerServicePerimeterIngressPolicyIngressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        ingress_to: typing.Optional[typing.Union["AccessContextManagerServicePerimeterIngressPolicyIngressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerServicePerimeterIngressPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy google_access_context_manager_service_perimeter_ingress_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param perimeter: The name of the Service Perimeter to add this resource to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#perimeter AccessContextManagerServicePerimeterIngressPolicy#perimeter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#id AccessContextManagerServicePerimeterIngressPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingress_from: ingress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#ingress_from AccessContextManagerServicePerimeterIngressPolicy#ingress_from}
        :param ingress_to: ingress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#ingress_to AccessContextManagerServicePerimeterIngressPolicy#ingress_to}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#timeouts AccessContextManagerServicePerimeterIngressPolicy#timeouts}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#title AccessContextManagerServicePerimeterIngressPolicy#title}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abff72d79c0e21ee4c55abb9fe7278c9ae20669f399c78563f7888e22c150088)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccessContextManagerServicePerimeterIngressPolicyConfig(
            perimeter=perimeter,
            id=id,
            ingress_from=ingress_from,
            ingress_to=ingress_to,
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
        '''Generates CDKTF code for importing a AccessContextManagerServicePerimeterIngressPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AccessContextManagerServicePerimeterIngressPolicy to import.
        :param import_from_id: The id of the existing AccessContextManagerServicePerimeterIngressPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AccessContextManagerServicePerimeterIngressPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b65e3da07848e8c7f942e22446215c1c650f6806b34f52e17e50937f2f2239b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIngressFrom")
    def put_ingress_from(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterIngressPolicyIngressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: Identities can be an individual user, service account, Google group, or third-party identity. For third-party identity, only single identities are supported and other identity types are not supported.The v1 identities that have the prefix user, group and serviceAccount in https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#identities AccessContextManagerServicePerimeterIngressPolicy#identities}
        :param identity_type: Specifies the type of identities that are allowed access from outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#identity_type AccessContextManagerServicePerimeterIngressPolicy#identity_type}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#sources AccessContextManagerServicePerimeterIngressPolicy#sources}
        '''
        value = AccessContextManagerServicePerimeterIngressPolicyIngressFrom(
            identities=identities, identity_type=identity_type, sources=sources
        )

        return typing.cast(None, jsii.invoke(self, "putIngressFrom", [value]))

    @jsii.member(jsii_name="putIngressTo")
    def put_ingress_to(
        self,
        *,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterIngressPolicyIngressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#operations AccessContextManagerServicePerimeterIngressPolicy#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'. A request matches if it contains a resource in this list. If '*' is specified for resources, then this 'IngressTo' rule will authorize access to all resources inside the perimeter, provided that the request also matches the 'operations' field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#resources AccessContextManagerServicePerimeterIngressPolicy#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#roles AccessContextManagerServicePerimeterIngressPolicy#roles}
        '''
        value = AccessContextManagerServicePerimeterIngressPolicyIngressTo(
            operations=operations, resources=resources, roles=roles
        )

        return typing.cast(None, jsii.invoke(self, "putIngressTo", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#create AccessContextManagerServicePerimeterIngressPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#delete AccessContextManagerServicePerimeterIngressPolicy#delete}.
        '''
        value = AccessContextManagerServicePerimeterIngressPolicyTimeouts(
            create=create, delete=delete
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIngressFrom")
    def reset_ingress_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressFrom", []))

    @jsii.member(jsii_name="resetIngressTo")
    def reset_ingress_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressTo", []))

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
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="ingressFrom")
    def ingress_from(
        self,
    ) -> "AccessContextManagerServicePerimeterIngressPolicyIngressFromOutputReference":
        return typing.cast("AccessContextManagerServicePerimeterIngressPolicyIngressFromOutputReference", jsii.get(self, "ingressFrom"))

    @builtins.property
    @jsii.member(jsii_name="ingressTo")
    def ingress_to(
        self,
    ) -> "AccessContextManagerServicePerimeterIngressPolicyIngressToOutputReference":
        return typing.cast("AccessContextManagerServicePerimeterIngressPolicyIngressToOutputReference", jsii.get(self, "ingressTo"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "AccessContextManagerServicePerimeterIngressPolicyTimeoutsOutputReference":
        return typing.cast("AccessContextManagerServicePerimeterIngressPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressFromInput")
    def ingress_from_input(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterIngressPolicyIngressFrom"]:
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterIngressPolicyIngressFrom"], jsii.get(self, "ingressFromInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressToInput")
    def ingress_to_input(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterIngressPolicyIngressTo"]:
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterIngressPolicyIngressTo"], jsii.get(self, "ingressToInput"))

    @builtins.property
    @jsii.member(jsii_name="perimeterInput")
    def perimeter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "perimeterInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AccessContextManagerServicePerimeterIngressPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AccessContextManagerServicePerimeterIngressPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__73bda1b1d77fffaa2440152bddc7632398d51344eab6d26d7b9d813f1cf3495f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="perimeter")
    def perimeter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "perimeter"))

    @perimeter.setter
    def perimeter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38b4cde92f343e008d7a8e569b9e17bcb71be37a6a2600f1831537c208bc61c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perimeter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf684441b031de6317e1a3de02d422bf9540495d077c5467f4b88c9062123a1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterIngressPolicy.AccessContextManagerServicePerimeterIngressPolicyConfig",
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
        "id": "id",
        "ingress_from": "ingressFrom",
        "ingress_to": "ingressTo",
        "timeouts": "timeouts",
        "title": "title",
    },
)
class AccessContextManagerServicePerimeterIngressPolicyConfig(
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
        id: typing.Optional[builtins.str] = None,
        ingress_from: typing.Optional[typing.Union["AccessContextManagerServicePerimeterIngressPolicyIngressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        ingress_to: typing.Optional[typing.Union["AccessContextManagerServicePerimeterIngressPolicyIngressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerServicePerimeterIngressPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param perimeter: The name of the Service Perimeter to add this resource to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#perimeter AccessContextManagerServicePerimeterIngressPolicy#perimeter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#id AccessContextManagerServicePerimeterIngressPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingress_from: ingress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#ingress_from AccessContextManagerServicePerimeterIngressPolicy#ingress_from}
        :param ingress_to: ingress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#ingress_to AccessContextManagerServicePerimeterIngressPolicy#ingress_to}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#timeouts AccessContextManagerServicePerimeterIngressPolicy#timeouts}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#title AccessContextManagerServicePerimeterIngressPolicy#title}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(ingress_from, dict):
            ingress_from = AccessContextManagerServicePerimeterIngressPolicyIngressFrom(**ingress_from)
        if isinstance(ingress_to, dict):
            ingress_to = AccessContextManagerServicePerimeterIngressPolicyIngressTo(**ingress_to)
        if isinstance(timeouts, dict):
            timeouts = AccessContextManagerServicePerimeterIngressPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61fde184e806164ab5593431a419656eeca3e70085413f868be8f05c73feb17d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument perimeter", value=perimeter, expected_type=type_hints["perimeter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ingress_from", value=ingress_from, expected_type=type_hints["ingress_from"])
            check_type(argname="argument ingress_to", value=ingress_to, expected_type=type_hints["ingress_to"])
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
        if id is not None:
            self._values["id"] = id
        if ingress_from is not None:
            self._values["ingress_from"] = ingress_from
        if ingress_to is not None:
            self._values["ingress_to"] = ingress_to
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#perimeter AccessContextManagerServicePerimeterIngressPolicy#perimeter}
        '''
        result = self._values.get("perimeter")
        assert result is not None, "Required property 'perimeter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#id AccessContextManagerServicePerimeterIngressPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingress_from(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterIngressPolicyIngressFrom"]:
        '''ingress_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#ingress_from AccessContextManagerServicePerimeterIngressPolicy#ingress_from}
        '''
        result = self._values.get("ingress_from")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterIngressPolicyIngressFrom"], result)

    @builtins.property
    def ingress_to(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterIngressPolicyIngressTo"]:
        '''ingress_to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#ingress_to AccessContextManagerServicePerimeterIngressPolicy#ingress_to}
        '''
        result = self._values.get("ingress_to")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterIngressPolicyIngressTo"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterIngressPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#timeouts AccessContextManagerServicePerimeterIngressPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterIngressPolicyTimeouts"], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Human readable title. Must be unique within the perimeter. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#title AccessContextManagerServicePerimeterIngressPolicy#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterIngressPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterIngressPolicy.AccessContextManagerServicePerimeterIngressPolicyIngressFrom",
    jsii_struct_bases=[],
    name_mapping={
        "identities": "identities",
        "identity_type": "identityType",
        "sources": "sources",
    },
)
class AccessContextManagerServicePerimeterIngressPolicyIngressFrom:
    def __init__(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterIngressPolicyIngressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: Identities can be an individual user, service account, Google group, or third-party identity. For third-party identity, only single identities are supported and other identity types are not supported.The v1 identities that have the prefix user, group and serviceAccount in https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#identities AccessContextManagerServicePerimeterIngressPolicy#identities}
        :param identity_type: Specifies the type of identities that are allowed access from outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#identity_type AccessContextManagerServicePerimeterIngressPolicy#identity_type}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#sources AccessContextManagerServicePerimeterIngressPolicy#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5edb7bc5846c7bc0bb00c6af2092c9655eecd7f82fbc837747d42dfa1abbbd19)
            check_type(argname="argument identities", value=identities, expected_type=type_hints["identities"])
            check_type(argname="argument identity_type", value=identity_type, expected_type=type_hints["identity_type"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identities is not None:
            self._values["identities"] = identities
        if identity_type is not None:
            self._values["identity_type"] = identity_type
        if sources is not None:
            self._values["sources"] = sources

    @builtins.property
    def identities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Identities can be an individual user, service account, Google group, or third-party identity.

        For third-party identity, only single identities
        are supported and other identity types are not supported.The v1 identities
        that have the prefix user, group and serviceAccount in
        https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#identities AccessContextManagerServicePerimeterIngressPolicy#identities}
        '''
        result = self._values.get("identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of identities that are allowed access from outside the perimeter.

        If left unspecified, then members of 'identities' field will be
        allowed access. Possible values: ["ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#identity_type AccessContextManagerServicePerimeterIngressPolicy#identity_type}
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterIngressPolicyIngressFromSources"]]]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#sources AccessContextManagerServicePerimeterIngressPolicy#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterIngressPolicyIngressFromSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterIngressPolicyIngressFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterIngressPolicyIngressFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterIngressPolicy.AccessContextManagerServicePerimeterIngressPolicyIngressFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6712ec2341bfc2af33431abd5f37efcae2be7e7a1205c5c241ff54b452ed1984)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterIngressPolicyIngressFromSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b56cd9ac909d4626987c9291a99b1fb320099092ca444a1196ea7a00abf79478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSources", [value]))

    @jsii.member(jsii_name="resetIdentities")
    def reset_identities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentities", []))

    @jsii.member(jsii_name="resetIdentityType")
    def reset_identity_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityType", []))

    @jsii.member(jsii_name="resetSources")
    def reset_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSources", []))

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> "AccessContextManagerServicePerimeterIngressPolicyIngressFromSourcesList":
        return typing.cast("AccessContextManagerServicePerimeterIngressPolicyIngressFromSourcesList", jsii.get(self, "sources"))

    @builtins.property
    @jsii.member(jsii_name="identitiesInput")
    def identities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="identityTypeInput")
    def identity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterIngressPolicyIngressFromSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterIngressPolicyIngressFromSources"]]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="identities")
    def identities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identities"))

    @identities.setter
    def identities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25efea348b8b54ad548fa8b27dff4bfb84389221d78e27c941c620e82b8a6014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityType")
    def identity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityType"))

    @identity_type.setter
    def identity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b1b5758c97ad2a2bc4b7ce2ca666d19920a2d27124ec4589b82fbe48fe3894b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterIngressPolicyIngressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterIngressPolicyIngressFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimeterIngressPolicyIngressFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a0a1795ef720c37ad6f08dc036af71d35f76555f505f6e8c444ba678ef21673)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterIngressPolicy.AccessContextManagerServicePerimeterIngressPolicyIngressFromSources",
    jsii_struct_bases=[],
    name_mapping={"access_level": "accessLevel", "resource": "resource"},
)
class AccessContextManagerServicePerimeterIngressPolicyIngressFromSources:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_level: An 'AccessLevel' resource name that allow resources within the 'ServicePerimeters' to be accessed from the internet. 'AccessLevels' listed must be in the same policy as this 'ServicePerimeter'. Referencing a nonexistent 'AccessLevel' will cause an error. If no 'AccessLevel' names are listed, resources within the perimeter can only be accessed via Google Cloud calls with request origins within the perimeter. Example 'accessPolicies/MY_POLICY/accessLevels/MY_LEVEL.' If * is specified, then all IngressSources will be allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#access_level AccessContextManagerServicePerimeterIngressPolicy#access_level}
        :param resource: A Google Cloud resource that is allowed to ingress the perimeter. Requests from these resources will be allowed to access perimeter data. Currently only projects and VPCs are allowed. Project format: 'projects/{projectNumber}' VPC network format: '//compute.googleapis.com/projects/{PROJECT_ID}/global/networks/{NAME}'. The project may be in any Google Cloud organization, not just the organization that the perimeter is defined in. '*' is not allowed, the case of allowing all Google Cloud resources only is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#resource AccessContextManagerServicePerimeterIngressPolicy#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d30f7c88c0bc35c6ed805ad59ab616d9fc01447f891ed05ca929ad00dccec67)
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_level is not None:
            self._values["access_level"] = access_level
        if resource is not None:
            self._values["resource"] = resource

    @builtins.property
    def access_level(self) -> typing.Optional[builtins.str]:
        '''An 'AccessLevel' resource name that allow resources within the 'ServicePerimeters' to be accessed from the internet.

        'AccessLevels' listed
        must be in the same policy as this 'ServicePerimeter'. Referencing a nonexistent
        'AccessLevel' will cause an error. If no 'AccessLevel' names are listed,
        resources within the perimeter can only be accessed via Google Cloud calls
        with request origins within the perimeter.
        Example 'accessPolicies/MY_POLICY/accessLevels/MY_LEVEL.'
        If * is specified, then all IngressSources will be allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#access_level AccessContextManagerServicePerimeterIngressPolicy#access_level}
        '''
        result = self._values.get("access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''A Google Cloud resource that is allowed to ingress the perimeter.

        Requests from these resources will be allowed to access perimeter data.
        Currently only projects and VPCs are allowed.
        Project format: 'projects/{projectNumber}'
        VPC network format:
        '//compute.googleapis.com/projects/{PROJECT_ID}/global/networks/{NAME}'.
        The project may be in any Google Cloud organization, not just the
        organization that the perimeter is defined in. '*' is not allowed, the case
        of allowing all Google Cloud resources only is not supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#resource AccessContextManagerServicePerimeterIngressPolicy#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterIngressPolicyIngressFromSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterIngressPolicyIngressFromSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterIngressPolicy.AccessContextManagerServicePerimeterIngressPolicyIngressFromSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdaa41aee0b715dc8d0718a8eb29a03305ac42d5d689cca4b4eba2681d09b13a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterIngressPolicyIngressFromSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e53955f6723ab53da07b84c2157bf93e24cf4c94d11da7ab76f6cdaebcc1b0c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterIngressPolicyIngressFromSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__865c7faa74f87519dbc48414d1a33ad0bc6c4f867c0158142e046dd10be2e279)
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
            type_hints = typing.get_type_hints(_typecheckingstub__426f375e5cbe10f9a822703d6a7b6a6e3be19b98808197459e49598e8591b127)
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
            type_hints = typing.get_type_hints(_typecheckingstub__544e59bba10aa0b5873fef93df588e3fc64c411bdd13b93714bef4fe710b1fb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterIngressPolicyIngressFromSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterIngressPolicyIngressFromSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterIngressPolicyIngressFromSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__075c90fe00529701f2bec197a13da57f6569e734324bf2fa2e0349c9c913d49a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterIngressPolicyIngressFromSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterIngressPolicy.AccessContextManagerServicePerimeterIngressPolicyIngressFromSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e525fd4a2a68b3af1a27c80a6f0ee3746b9361c6bf3b69d0b43d42a9a0310f35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0268a70b2002544608df53db34292e3ac48717c709973adb7f19a38632b6ed1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c87c83e12f05c7e3bfffa7e62a01dc21b88e3ca5aa4d8995ad93c18ed00af8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterIngressPolicyIngressFromSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterIngressPolicyIngressFromSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterIngressPolicyIngressFromSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc561957407ac19e4f48235d63658a9ae9cab4fc98a99a6fe4f7e8de8ddec72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterIngressPolicy.AccessContextManagerServicePerimeterIngressPolicyIngressTo",
    jsii_struct_bases=[],
    name_mapping={
        "operations": "operations",
        "resources": "resources",
        "roles": "roles",
    },
)
class AccessContextManagerServicePerimeterIngressPolicyIngressTo:
    def __init__(
        self,
        *,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterIngressPolicyIngressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#operations AccessContextManagerServicePerimeterIngressPolicy#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'. A request matches if it contains a resource in this list. If '*' is specified for resources, then this 'IngressTo' rule will authorize access to all resources inside the perimeter, provided that the request also matches the 'operations' field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#resources AccessContextManagerServicePerimeterIngressPolicy#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#roles AccessContextManagerServicePerimeterIngressPolicy#roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff63887461e3b3fd4d66e3721d29ca5f9eda8192002f5eafc93688c6e4196697)
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if operations is not None:
            self._values["operations"] = operations
        if resources is not None:
            self._values["resources"] = resources
        if roles is not None:
            self._values["roles"] = roles

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterIngressPolicyIngressToOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#operations AccessContextManagerServicePerimeterIngressPolicy#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterIngressPolicyIngressToOperations"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'.

        A request matches if it contains
        a resource in this list. If '*' is specified for resources,
        then this 'IngressTo' rule will authorize access to all
        resources inside the perimeter, provided that the request
        also matches the 'operations' field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#resources AccessContextManagerServicePerimeterIngressPolicy#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#roles AccessContextManagerServicePerimeterIngressPolicy#roles}
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterIngressPolicyIngressTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterIngressPolicy.AccessContextManagerServicePerimeterIngressPolicyIngressToOperations",
    jsii_struct_bases=[],
    name_mapping={
        "method_selectors": "methodSelectors",
        "service_name": "serviceName",
    },
)
class AccessContextManagerServicePerimeterIngressPolicyIngressToOperations:
    def __init__(
        self,
        *,
        method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method_selectors: method_selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#method_selectors AccessContextManagerServicePerimeterIngressPolicy#method_selectors}
        :param service_name: The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow. A single 'ApiOperation' with 'serviceName' field set to '*' will allow all methods AND permissions for all services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#service_name AccessContextManagerServicePerimeterIngressPolicy#service_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0e64277ccfdbd9dae2dbc28bc48e0ee3b4798520596fb10f7584bb1642974c3)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors"]]]:
        '''method_selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#method_selectors AccessContextManagerServicePerimeterIngressPolicy#method_selectors}
        '''
        result = self._values.get("method_selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors"]]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow.

        A single 'ApiOperation' with 'serviceName'
        field set to '*' will allow all methods AND permissions for all services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#service_name AccessContextManagerServicePerimeterIngressPolicy#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterIngressPolicyIngressToOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterIngressPolicy.AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e34d5baedb1817ea0c88e22571bce130d2d1c515d5cd4d0ba4f54ae97f02b4ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ed94badb0ea2667a40c5ff28caec1834cec7777ca784fc8bc9e37487bc5ad4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2422dcab9a601c266fecc075ab8062d38e4a95c1e0b469f5ce708349c71c58d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3f04e33170a5d81ff75957938c0f0c99e6f1d36c51478fc073fc9d1f896f21f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1faed1e8010dcbe4a51c3fc2125ad6cd0b21a6bc69b4a65cc1d62fc4ade61be3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterIngressPolicyIngressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterIngressPolicyIngressToOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterIngressPolicyIngressToOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a275adcacc9f941f67019795eecd10f0a5ed9ef5baeff0e655595f466e83e91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterIngressPolicy.AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "permission": "permission"},
)
class AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors:
    def __init__(
        self,
        *,
        method: typing.Optional[builtins.str] = None,
        permission: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method: Value for method should be a valid method name for the corresponding serviceName in 'ApiOperation'. If '*' used as value for 'method', then ALL methods and permissions are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#method AccessContextManagerServicePerimeterIngressPolicy#method}
        :param permission: Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#permission AccessContextManagerServicePerimeterIngressPolicy#permission}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb0fc4c7824ff9a4f92244d3cf26190d61e5f3009e21f6679ca694cc4ea1b1e0)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if permission is not None:
            self._values["permission"] = permission

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Value for method should be a valid method name for the corresponding serviceName in 'ApiOperation'.

        If '*' used as value for 'method', then
        ALL methods and permissions are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#method AccessContextManagerServicePerimeterIngressPolicy#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission(self) -> typing.Optional[builtins.str]:
        '''Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#permission AccessContextManagerServicePerimeterIngressPolicy#permission}
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterIngressPolicy.AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d78d2e845e25e498c22667b5f0a9bd615ffbe25a791079bfd44b463d347d28c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0ec4cad1b10bb52905830b382e9865ee5935ef6674dc38c4384bd1e5ad0668)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b81d95ddf0a88874c081ab5aa5ed25a0ded9938b23ff970e32f77d9b53d1d958)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac1cce20f8f75ce638e3a7417789eee930a17be9de672c036fcfe45c94d087ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fded7574ad4239a8b3fba89199615453435931bce77ab6378fb42fd0cd36aff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07ad659b53f1663cc6064b506c1ad48f102db1c4fb3da3b98621fa00c2878f07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterIngressPolicy.AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__180e6396243636f27706858d4ebe5aa43f4d6e4a219c12ff72d3e8a4816f9f9c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1055b610434a71c5e4271fd1c8d4923ea45be50d96d9c0e906999b45bb3f0dde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac11382bdfe0e1576628d50c6eaf55d704d53b41435af527a1360bb7978352b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a489c28f27c54756df3defd7a493c88cf80c5236ab5f22bf1013833a3db091d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterIngressPolicy.AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7940470faa09ca201a3c09405facdcd9085a6497c72a79f866254b5e2edb9c7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMethodSelectors")
    def put_method_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__431400b07bbd9f7afb129f30217b3ba985eca3ef701b0d94ccd99f4fd5814028)
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
    ) -> AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectorsList:
        return typing.cast(AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectorsList, jsii.get(self, "methodSelectors"))

    @builtins.property
    @jsii.member(jsii_name="methodSelectorsInput")
    def method_selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors]]], jsii.get(self, "methodSelectorsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c46315d161c7ded9b22bc7ab9076648a0617f75d15d87ae378484c0d005bfea0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterIngressPolicyIngressToOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterIngressPolicyIngressToOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterIngressPolicyIngressToOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28a411db340670680a2fb3886b786db24bd4d87b90c0f32ec250e1da0eb5cbf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterIngressPolicyIngressToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterIngressPolicy.AccessContextManagerServicePerimeterIngressPolicyIngressToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05f718bbadf3fa61150c9815aa42fe840a88aff1d3a6449358ea7598beddb21b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterIngressPolicyIngressToOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22e4d273e5f0331d3a806f2942e3593de97ed260c94ce4f5422d35df48b1a520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperations", [value]))

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
    ) -> AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsList:
        return typing.cast(AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterIngressPolicyIngressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterIngressPolicyIngressToOperations]]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b577a24fec756b4881f102e1b24b8dd870a6d7cb4e3fac0980cf4d8a2a2c7465)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bcea07434ee9a56786b0d85b758eb5f438c2417b8da560b129c3af5e01b0ad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterIngressPolicyIngressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterIngressPolicyIngressTo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimeterIngressPolicyIngressTo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f91c5f0f6549cbf18bd407d58d5d58163369d8fddbfb2e7508e0fcd3f7fddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterIngressPolicy.AccessContextManagerServicePerimeterIngressPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class AccessContextManagerServicePerimeterIngressPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#create AccessContextManagerServicePerimeterIngressPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#delete AccessContextManagerServicePerimeterIngressPolicy#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c7272e14410c69408297008b2f56570b86d5c03b667ee67f25bb3985afcd2a0)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#create AccessContextManagerServicePerimeterIngressPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_ingress_policy#delete AccessContextManagerServicePerimeterIngressPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterIngressPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterIngressPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterIngressPolicy.AccessContextManagerServicePerimeterIngressPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf905b0a6605d23391058d03b407749bef6330afe73e53cef1ac52636218ad3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbef6ea49a36b4485b5a66b1058811bb17dcbdcd04ac0bf2ae635f1ad695a678)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f9f6a419ae4d07e363c277f07e5665285f998cfee54219819a85b508490dd07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterIngressPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterIngressPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterIngressPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48fd5220c97baa26c4bcc7d6bd8280b19296041ed4fe61529369e328d75e5a69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AccessContextManagerServicePerimeterIngressPolicy",
    "AccessContextManagerServicePerimeterIngressPolicyConfig",
    "AccessContextManagerServicePerimeterIngressPolicyIngressFrom",
    "AccessContextManagerServicePerimeterIngressPolicyIngressFromOutputReference",
    "AccessContextManagerServicePerimeterIngressPolicyIngressFromSources",
    "AccessContextManagerServicePerimeterIngressPolicyIngressFromSourcesList",
    "AccessContextManagerServicePerimeterIngressPolicyIngressFromSourcesOutputReference",
    "AccessContextManagerServicePerimeterIngressPolicyIngressTo",
    "AccessContextManagerServicePerimeterIngressPolicyIngressToOperations",
    "AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsList",
    "AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors",
    "AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectorsList",
    "AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectorsOutputReference",
    "AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsOutputReference",
    "AccessContextManagerServicePerimeterIngressPolicyIngressToOutputReference",
    "AccessContextManagerServicePerimeterIngressPolicyTimeouts",
    "AccessContextManagerServicePerimeterIngressPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__abff72d79c0e21ee4c55abb9fe7278c9ae20669f399c78563f7888e22c150088(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    perimeter: builtins.str,
    id: typing.Optional[builtins.str] = None,
    ingress_from: typing.Optional[typing.Union[AccessContextManagerServicePerimeterIngressPolicyIngressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    ingress_to: typing.Optional[typing.Union[AccessContextManagerServicePerimeterIngressPolicyIngressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerServicePerimeterIngressPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2b65e3da07848e8c7f942e22446215c1c650f6806b34f52e17e50937f2f2239b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73bda1b1d77fffaa2440152bddc7632398d51344eab6d26d7b9d813f1cf3495f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38b4cde92f343e008d7a8e569b9e17bcb71be37a6a2600f1831537c208bc61c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf684441b031de6317e1a3de02d422bf9540495d077c5467f4b88c9062123a1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61fde184e806164ab5593431a419656eeca3e70085413f868be8f05c73feb17d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    perimeter: builtins.str,
    id: typing.Optional[builtins.str] = None,
    ingress_from: typing.Optional[typing.Union[AccessContextManagerServicePerimeterIngressPolicyIngressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    ingress_to: typing.Optional[typing.Union[AccessContextManagerServicePerimeterIngressPolicyIngressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerServicePerimeterIngressPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5edb7bc5846c7bc0bb00c6af2092c9655eecd7f82fbc837747d42dfa1abbbd19(
    *,
    identities: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterIngressPolicyIngressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6712ec2341bfc2af33431abd5f37efcae2be7e7a1205c5c241ff54b452ed1984(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b56cd9ac909d4626987c9291a99b1fb320099092ca444a1196ea7a00abf79478(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterIngressPolicyIngressFromSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25efea348b8b54ad548fa8b27dff4bfb84389221d78e27c941c620e82b8a6014(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b1b5758c97ad2a2bc4b7ce2ca666d19920a2d27124ec4589b82fbe48fe3894b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0a1795ef720c37ad6f08dc036af71d35f76555f505f6e8c444ba678ef21673(
    value: typing.Optional[AccessContextManagerServicePerimeterIngressPolicyIngressFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d30f7c88c0bc35c6ed805ad59ab616d9fc01447f891ed05ca929ad00dccec67(
    *,
    access_level: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdaa41aee0b715dc8d0718a8eb29a03305ac42d5d689cca4b4eba2681d09b13a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e53955f6723ab53da07b84c2157bf93e24cf4c94d11da7ab76f6cdaebcc1b0c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865c7faa74f87519dbc48414d1a33ad0bc6c4f867c0158142e046dd10be2e279(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426f375e5cbe10f9a822703d6a7b6a6e3be19b98808197459e49598e8591b127(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544e59bba10aa0b5873fef93df588e3fc64c411bdd13b93714bef4fe710b1fb3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075c90fe00529701f2bec197a13da57f6569e734324bf2fa2e0349c9c913d49a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterIngressPolicyIngressFromSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e525fd4a2a68b3af1a27c80a6f0ee3746b9361c6bf3b69d0b43d42a9a0310f35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0268a70b2002544608df53db34292e3ac48717c709973adb7f19a38632b6ed1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c87c83e12f05c7e3bfffa7e62a01dc21b88e3ca5aa4d8995ad93c18ed00af8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc561957407ac19e4f48235d63658a9ae9cab4fc98a99a6fe4f7e8de8ddec72(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterIngressPolicyIngressFromSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff63887461e3b3fd4d66e3721d29ca5f9eda8192002f5eafc93688c6e4196697(
    *,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterIngressPolicyIngressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0e64277ccfdbd9dae2dbc28bc48e0ee3b4798520596fb10f7584bb1642974c3(
    *,
    method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34d5baedb1817ea0c88e22571bce130d2d1c515d5cd4d0ba4f54ae97f02b4ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ed94badb0ea2667a40c5ff28caec1834cec7777ca784fc8bc9e37487bc5ad4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2422dcab9a601c266fecc075ab8062d38e4a95c1e0b469f5ce708349c71c58d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f04e33170a5d81ff75957938c0f0c99e6f1d36c51478fc073fc9d1f896f21f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1faed1e8010dcbe4a51c3fc2125ad6cd0b21a6bc69b4a65cc1d62fc4ade61be3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a275adcacc9f941f67019795eecd10f0a5ed9ef5baeff0e655595f466e83e91(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterIngressPolicyIngressToOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb0fc4c7824ff9a4f92244d3cf26190d61e5f3009e21f6679ca694cc4ea1b1e0(
    *,
    method: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d78d2e845e25e498c22667b5f0a9bd615ffbe25a791079bfd44b463d347d28c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0ec4cad1b10bb52905830b382e9865ee5935ef6674dc38c4384bd1e5ad0668(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81d95ddf0a88874c081ab5aa5ed25a0ded9938b23ff970e32f77d9b53d1d958(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1cce20f8f75ce638e3a7417789eee930a17be9de672c036fcfe45c94d087ba(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fded7574ad4239a8b3fba89199615453435931bce77ab6378fb42fd0cd36aff(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ad659b53f1663cc6064b506c1ad48f102db1c4fb3da3b98621fa00c2878f07(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180e6396243636f27706858d4ebe5aa43f4d6e4a219c12ff72d3e8a4816f9f9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1055b610434a71c5e4271fd1c8d4923ea45be50d96d9c0e906999b45bb3f0dde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac11382bdfe0e1576628d50c6eaf55d704d53b41435af527a1360bb7978352b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a489c28f27c54756df3defd7a493c88cf80c5236ab5f22bf1013833a3db091d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7940470faa09ca201a3c09405facdcd9085a6497c72a79f866254b5e2edb9c7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431400b07bbd9f7afb129f30217b3ba985eca3ef701b0d94ccd99f4fd5814028(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterIngressPolicyIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c46315d161c7ded9b22bc7ab9076648a0617f75d15d87ae378484c0d005bfea0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a411db340670680a2fb3886b786db24bd4d87b90c0f32ec250e1da0eb5cbf6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterIngressPolicyIngressToOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f718bbadf3fa61150c9815aa42fe840a88aff1d3a6449358ea7598beddb21b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e4d273e5f0331d3a806f2942e3593de97ed260c94ce4f5422d35df48b1a520(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterIngressPolicyIngressToOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b577a24fec756b4881f102e1b24b8dd870a6d7cb4e3fac0980cf4d8a2a2c7465(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bcea07434ee9a56786b0d85b758eb5f438c2417b8da560b129c3af5e01b0ad1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f91c5f0f6549cbf18bd407d58d5d58163369d8fddbfb2e7508e0fcd3f7fddb(
    value: typing.Optional[AccessContextManagerServicePerimeterIngressPolicyIngressTo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c7272e14410c69408297008b2f56570b86d5c03b667ee67f25bb3985afcd2a0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf905b0a6605d23391058d03b407749bef6330afe73e53cef1ac52636218ad3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbef6ea49a36b4485b5a66b1058811bb17dcbdcd04ac0bf2ae635f1ad695a678(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9f6a419ae4d07e363c277f07e5665285f998cfee54219819a85b508490dd07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48fd5220c97baa26c4bcc7d6bd8280b19296041ed4fe61529369e328d75e5a69(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterIngressPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
